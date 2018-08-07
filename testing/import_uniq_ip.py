import os
import sys
import json
import psycopg2
import settings


def listIp(idea):
    result = []
    for ip in idea:
        if '-' in ip:
            parts = ip.split('-')
            if parts[1].isdigit():
                for i in range(int(parts[0].split('.')[3]), int(parts[1])+1):
                    result.append(parts[0].split('.')[0] + '.' + parts[0].split('.')[1] + '.' + parts[0].split('.')[2] + '.' + str(i))
            else:
                for i in range(int(parts[0].split('.')[0]), int(parts[1].split('.')[0])+1):
                    for j in range(int(parts[0].split('.')[1]), int(parts[1].split('.')[1])+1):
                        for k in range(int(parts[0].split('.')[2]), int(parts[1].split('.')[2])+1):
                            for l in range(int(parts[0].split('.')[3]), int(parts[1].split('.')[3])+1):
                                result.append(str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l))
        elif '/' in ip:
            parts = ip.split('/')
            if int(parts[1]) < 8:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [2**(8-(int(parts[1])%8)), 0, 0, 0])]
                for i in range(0, 2**(8-int(parts[1])%8)):
                    for j in range(0, 256):
                        for k in range(0, 256):
                            for l in range(0, 256):
                                result.append(str(int(mask[0])+i) + '.' + str(j) + '.' + str(k) + '.' + str(l))
            elif int(parts[1]) < 16:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 2**(8-(int(parts[1])%8)), 0, 0])]
                for j in range(0, 2**(8-int(parts[1])%8)):
                    for k in range(0, 256):
                        for l in range(0, 256):
                                result.append(str(parts[0].split('.')[0]) + '.' + str(int(mask[1])+j) + '.' + str(k) + '.' + str(l))
            elif int(parts[1]) < 24:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 255, 2**(8-(int(parts[1])%8)), 0])]
                for k in range(0, 2**(8-int(parts[1])%8)):
                    for l in range(0, 256):
                                result.append(str(parts[0].split('.')[0]) + '.' + str(parts[0].split('.')[1]) + '.' + str(int(mask[2])+k) + '.' + str(l))
            elif int(parts[1]) < 32:
                mask = [str(int(bin(int(ioctet) & moctet), 2)) for ioctet, moctet in zip(parts[0].split('.'), [255, 255, 255, 2**(8-(int(parts[1])%8))])]
                for l in range(0, 2**(8-int(parts[1])%8)):
                    result.append(str(parts[0].split('.')[0]) + '.' + str(parts[0].split('.')[1]) + '.' + str(parts[0].split('.')[2]) + '.' + str(int(mask[3])+l))
        else:
            result.append(ip)
    return result



for filename in os.listdir(settings.HOME + 'alerts/'):
    f = open(settings.HOME + 'alerts/' + filename, 'r')
    stream = f.read()

    line = json.loads(stream)


    conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                             user='" + settings.DB_USER + "'\
                             password='" + settings.DB_PASS + "'\
                             host='" + settings.DB_HOST + "'")
    conn.autocommit = True
    cur = conn.cursor()

    source = []
    sourcep = []
    sourceprot = []
    if 'Source' not in line:
        continue
    for i in line['Source']:
        if 'IP4' in i:
            source.extend(listIp(i['IP4']))
        if 'Port' in i:
            sourcep.extend(i['Port'])
        if 'Proto' in i:
            sourceprot.extend(i['Proto'])
    #sourceIP = str(source).replace('[', '{').replace(']', '}').replace("'", "")
    sourcePort = str(sourcep).replace('[', '{').replace(']', '}').replace("'", "")
    sourceProto = str(sourceprot).replace('[', '{').replace(']', '}').replace("'", "")

    if 'Category' not in line:
        continue
    category = str(line['Category']).replace('[', '{').replace(']', '}').replace("'", "")

    target = []
    targetp = []
    targetprot = []
    if 'Target' not in line:
        continue
    for i in line['Target']:
        if 'IP4' in i:
            target.extend(listIp(i['IP4']))
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


    sql = """DROP FUNCTION IF EXISTS array_sort_unique (ANYARRAY);
CREATE OR REPLACE FUNCTION array_sort_unique (ANYARRAY) RETURNS ANYARRAY
LANGUAGE SQL
AS $body$
SELECT ARRAY(
SELECT DISTINCT $1[s.i]
FROM generate_series(array_lower($1,1), array_upper($1,1)) AS s(i)
ORDER BY 1
);
$body$;"""
    cur.execute(sql)

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
targetip = array_sort_unique((SELECT targetip || '%s')::inet[]),\
targetport = array_sort_unique((SELECT targetport || '%s')::integer[]),\
targetproto = array_sort_unique((SELECT targetproto || '%s')::text[]),\
attach = (SELECT attach || '{%s}')\
WHERE sourceip = '%s';" % (line['ID'], line['DetectTime'], category, sourcePort, sourceProto, targetIP, targetPort, targetProto, attach, ip)

        else:
            sql = "INSERT INTO uniq_ip VALUES (\
'%s',\
'{%s}',\
'{%s}',\
'%s',\
'%s',\
'%s',\
'%s',\
'%s',\
'%s',\
'{%s}');" % (ip, line['ID'], line['DetectTime'], category, sourcePort, sourceProto, targetIP, targetPort, targetProto, attach)

        print(sql)
        cur.execute(sql)

    f.closed

# update uniq_ip set 
# targetip = array_sort_unique(targetip::inet[]), 
# targetport = array_sort_unique(targetport::integer[]), 
# targetproto = array_sort_unique(targetproto::text[]), 
# sourceport = array_sort_unique(sourceport::integer[]), 
# sourceproto = array_sort_unique(sourceproto::text[]) 
# where array_length(targetip, 1) = 983040;