import os
import sys
import json
import psycopg2
import settings

from get_attach_list_db import get_list


conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
cur = conn.cursor()
conn.autocommit = True


#-----------------------------------------------------------------------------------------------

print("Port 23 and 2323 scanning")
sql = """SELECT sourceip
         FROM uniq_ip
         WHERE ( 23 = ANY (targetport) AND 2323 = ANY (targetport) )
             AND ( 'Recon.Scanning' = ANY (category) OR 'Attempt.Login' = ANY (category));"""

port23 = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    port23.add(row[0])

print(str(len(port23)))


#-----------------------------------------------------------------------------------------------

print("\nAtleast 3 same suspected ports")

sql = """SELECT sourceip
         FROM uniq_ip
         WHERE array_length(array_intersect(targetport, ARRAY[23, 2323, 21, 22, 80]), 1) >= 3
      ;"""

cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print(row[0])


#-----------------------------------------------------------------------------------------------

attach_arr = get_list()

for attach_type in attach_arr:
    print("\nAttachment match: " + attach_type)
    sql = """SELECT sourceip
             FROM actual
             WHERE ( attach LIKE '%""" + attach_type + """%' )
                 ;"""

    cur.execute(sql)
    rows = cur.fetchall()
    ips = set()
    for row in rows:
        ips.update(row[0])

    print(str(ips))


#-----------------------------------------------------------------------------------------------

print("\nBotnets & C&C")
sql = """SELECT sourceip
         FROM features
         WHERE ( bot = True OR cc = True );"""

botnet = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    botnet.add(row[0])

print(str(botnet))

#-----------------------------------------------------------------------------------------------

print("\nBotnet MIRAI")
sql = """SELECT sourceip
         FROM uniq_ip
         WHERE ( 23 = ANY (targetport) AND 2323 = ANY (targetport) )
             AND ( 'Recon.Scanning' = ANY (category) OR 'Attempt.Login' = ANY (category));"""

mirai = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    mirai.add(row[0])

print(str(mirai))

#-----------------------------------------------------------------------------------------------

print("\nBotnet MIRAI from features")
sql = """SELECT sourceip
         FROM features
         WHERE ( port_23_2323 = True 
             AND ( bot = True OR cc = True ));"""

mirai = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    mirai.add(row[0])

print(str(mirai))
