import os
import sys
import json
import psycopg2
import settings


conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
cur = conn.cursor()
conn.autocommit = True



sql = """SELECT sourceip FROM uniq_ip  
         WHERE ( 23 = ANY (targetport) OR 2323 = ANY (targetport) );"""
cur.execute(sql)
rows = cur.fetchall()

for ip in rows:
    sql = "SELECT count(sourceip) FROM features WHERE sourceip = '%s';" % ip
    cur.execute(sql)
    result = cur.fetchone()
    if result == (1,):
        sql = "UPDATE features SET port_23_2323 = True WHERE sourceip = '%s';" % (ip)

    else:
        sql = "INSERT INTO features (sourceip, port_23_2323) VALUES ('%s', True);" % (ip)
    cur.execute(sql)

