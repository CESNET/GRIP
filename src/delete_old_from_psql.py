import os
import sys
import json
import psycopg2
import settings


conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
conn.autocommit = True
cur = conn.cursor()
sql = """
DELETE FROM actual 
WHERE detecttime < (now() at time zone 'utc') - interval '1 hour';

DELETE FROM history 
WHERE detecttime < (now() at time zone 'utc') - interval '12 hour';
"""
print(sql)
cur.execute(sql)
#rows = cur.fetchall()
#for row in rows:
#   print(row[0])

conn.closed
