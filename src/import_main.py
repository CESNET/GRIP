import os
import sys
import json
import psycopg2
import settings

from list_ip_addr import list_ip


def import_idea_to_actual(line):
    if 'Category' not in line:
        return 
    category = str(line['Category']).replace('[', '{').replace(']', '}').replace("'", "")
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
    sourceIP = str(source).replace('[', '{').replace(']', '}').replace("'", "")
    sourcePort = str(sourcep).replace('[', '{').replace(']', '}').replace("'", "")
    sourceProto = str(sourceprot).replace('[', '{').replace(']', '}').replace("'", "")

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
    targetIP = str(target).replace('[', '{').replace(']', '}').replace("'", "")
    targetPort = str(targetp).replace('[', '{').replace(']', '}').replace("'", "")
    targetProto = str(targetprot).replace('[', '{').replace(']', '}').replace("'", "")

    attach = ''
    if 'Attach' in line:
        if 'Content' in line['Attach'][0]:
            attach = line['Attach'][0]['Content'].encode('utf-8').decode('utf-8').replace("'", '"')


    conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                             user='" + settings.DB_USER + "'\
                             password='" + settings.DB_PASS + "'\
                             host='" + settings.DB_HOST + "'")
    conn.autocommit = True
    cur = conn.cursor()
    sql = """INSERT INTO actual
VALUES (
'""" + line['ID'] + """',
'""" + line['DetectTime'] + """',
'""" + category + """',
'""" + sourceIP + """',
'""" + sourcePort + """',
'""" + sourceProto + """',
'""" + targetIP + """',
'""" + targetPort + """',
'""" + targetProto + """',
'""" + attach + """');
"""
 
    cur.execute(sql)
    #rows = cur.fetchall()
    #for row in rows:
     #   print(row[0])

    
