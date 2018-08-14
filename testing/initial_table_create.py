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
CREATE TABLE IF NOT EXISTS actual (
id text,
detecttime timestamp without time zone,
category text[],
sourceip inet[],
sourceport integer[],
sourceproto text[],
targetip inet[],
targetport integer[],
targetproto text[],
attach text);

CREATE TABLE IF NOT EXISTS uniq_ip (
sourceip inet UNIQUE NOT NULL PRIMARY KEY,
id text[],
detecttime timestamp without time zone[],
category text[],
sourceport integer[],
sourceproto text[],
targetip integer,
targetport integer[],
targetproto text[],
attach text[]);

CREATE TABLE IF NOT EXISTS history (
id text,
detecttime timestamp without time zone,
category text[],
sourceip inet[],
sourceport integer[],
sourceproto text[],
targetip inet[],
targetport integer[],
targetproto text[],
attach text);

CREATE TABLE IF NOT EXISTS features (
sourceip inet NOT NULL PRIMARY KEY UNIQUE,
cc boolean DEFAULT FALSE,
bot boolean DEFAULT FALSE,
port_23_2323 boolean DEFAULT FALSE,
spam boolean DEFAULT FALSE);
"""
print(sql)
cur.execute(sql)
#rows = cur.fetchall()
#for row in rows:
#   print(row[0])

conn.closed
