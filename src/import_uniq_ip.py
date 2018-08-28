import os
import sys
import json
import psycopg2
import settings
import datetime

from list_ip_addr import list_ip


def import_idea_to_uniq(line):
    conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                             user='" + settings.DB_USER + "'\
                             password='" + settings.DB_PASS + "'\
                             host='" + settings.DB_HOST + "'")
    conn.autocommit = True
    cur = conn.cursor()

    cc = []
    bots = []
    spam = []
    port = []

    source = []
    sourcep = []
    sourceprot = []
    if 'Source' not in line:
        return
    for i in line['Source']:
        if 'IP4' in i:
            source.extend(list_ip(i['IP4']))
        if 'Port' in i:
            sourcep.extend(i['Port'])
        if 'Proto' in i:
            sourceprot.extend(i['Proto'])
        if 'Type' in i:
            if 'CC' in i['Type']:
                cc.extend(list_ip(i['IP4']))
            if 'Botnet' in i['Type']:
                bots.extend(list_ip(i['IP4']))
            if 'Spam' in i['Type']:
                spam.extend(list_ip(i['IP4']))
    #sourceIP = str(source).replace('[', '{').replace(']', '}').replace("'", "")
    sourcePort = str(sourcep).replace('[', '{').replace(']', '}').replace("'", "")
    sourceProto = str(sourceprot).replace('[', '{').replace(']', '}').replace("'", "")

    if 'Category' not in line:
        return
    category = str(line['Category']).replace('[', '{').replace(']', '}').replace("'", "")

    target = []
    targetp = []
    targetprot = []
    if 'Target' not in line:
        return
    for i in line['Target']:
        if 'IP4' in i:
            target.extend(list_ip(i['IP4']))
        if 'Port' in i:
            targetp.extend(i['Port'])
        if 'Proto' in i:
            targetprot.extend(i['Proto'])
        if 'Type' in i:
            if 'CC' in i['Type']:
                cc.extend(list_ip(i['IP4']))
            if 'Botnet' in i['Type']:
                bots.extend(list_ip(i['IP4']))
            if 'Spam' in i['Type']:
                spam.extend(list_ip(i['IP4']))
    targetIP = len(target)
    targetPort = str(targetp).replace('[', '{').replace(']', '}').replace("'", "")
    targetProto = str(targetprot).replace('[', '{').replace(']', '}').replace("'", "")

    attach = ''
    if 'Attach' in line:
        if 'Content' in line['Attach'][0]:
            attach = line['Attach'][0]['Content'].encode('utf-8').decode('utf-8').replace("'", '').replace('{', '').replace('}', '')


#_CC, BOTS, SPAM____________________________________________________________________________
    
    for ip in cc:
        sql = "SELECT count(sourceip) FROM features WHERE sourceip = '%s';" % ip
        cur.execute(sql)
        result = cur.fetchone()
        if result == (1,):
            sql = "UPDATE features SET cc = True WHERE sourceip = '%s';" % (ip)

        else:
            sql = "INSERT INTO features (sourceip, cc) VALUES ('%s', True);" % (ip)
        cur.execute(sql)

    for ip in bots:
        sql = "SELECT count(sourceip) FROM features WHERE sourceip = '%s';" % ip
        cur.execute(sql)
        result = cur.fetchone()
        if result == (1,):
            sql = "UPDATE features SET bot = True WHERE sourceip = '%s';" % (ip)

        else:
            sql = "INSERT INTO features (sourceip, bot) VALUES ('%s', True);" % (ip)
        cur.execute(sql)

    for ip in spam:
        sql = "SELECT count(sourceip) FROM features WHERE sourceip = '%s';" % ip
        cur.execute(sql)
        result = cur.fetchone()
        if result == (1,):
            sql = "UPDATE features SET spam = True WHERE sourceip = '%s';" % (ip)

        else:
            sql = "INSERT INTO features (sourceip, spam) VALUES ('%s', True);" % (ip)
        cur.execute(sql)

#_SAMOTNE_PLNENI__________________________________________________________________________________________________

    for ip in source:
        sql = "SELECT count(sourceip) FROM uniq_ip WHERE sourceip = '%s';" % ip
        cur.execute(sql)
        result = cur.fetchone()
        if result == (1,):
            sql = "UPDATE uniq_ip SET id = (SELECT id || '{%s}'),\
detecttime = (SELECT detecttime || '{%s}'),\
category = array_sort_unique((SELECT category || '%s')::text[]),\
sourceport = array_sort_unique((SELECT sourceport || '%s')::integer[]),\
sourceproto = array_sort_unique((SELECT sourceproto || '%s')::text[]),\
targetip = targetip + %d,\
targetport = array_sort_unique((SELECT targetport || '%s')::integer[]),\
targetproto = array_sort_unique((SELECT targetproto || '%s')::text[]),\
attach = (SELECT attach || '{%s}') \
WHERE sourceip = '%s';" % (line['ID'], line['DetectTime'], category, sourcePort, sourceProto, targetIP, targetPort, targetProto, attach, ip)

        else:
            sql = "INSERT INTO uniq_ip VALUES (\
'%s',\
'{%s}',\
'{%s}',\
'%s',\
'%s',\
'%s',\
%d,\
'%s',\
'%s',\
'{%s}');" % (ip, line['ID'], line['DetectTime'], category, sourcePort, sourceProto, targetIP, targetPort, targetProto, attach)

        cur.execute(sql)


# update uniq_ip set 
# targetip = array_sort_unique(targetip::inet[]), 
# targetport = array_sort_unique(targetport::integer[]), 
# targetproto = array_sort_unique(targetproto::text[]), 
# sourceport = array_sort_unique(sourceport::integer[]), 
# sourceproto = array_sort_unique(sourceproto::text[]) 
# where array_length(targetip, 1) = 983040;
