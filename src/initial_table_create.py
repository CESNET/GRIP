import os
import sys
import json
import psycopg2
import settings

conn = psycopg2.connect("dbname='postgres'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
conn.autocommit = True
cur = conn.cursor()
sql = """
CREATE DATABASE grip;
"""

conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
conn.autocommit = True
cur = conn.cursor()
sql = """
CREATE TABLE IF NOT EXISTS actual (
id text UNIQUE NOT NULL PRIMARY KEY,
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
id text UNIQUE NOT NULL PRIMARY KEY,
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


CREATE FUNCTION array_sort_unique (ANYARRAY) RETURNS ANYARRAY
LANGUAGE SQL
AS $body$
SELECT ARRAY(
SELECT DISTINCT $1[s.i]
FROM generate_series(array_lower($1,1), array_upper($1,1)) AS s(i)
ORDER BY 1
);
$body$;

create function array_intersect(a1 int[], a2 int[]) returns int[] as $$
    declare
        ret int[];
    begin
        if a1 is null then
            return a2;
        elseif a2 is null then
            return a1;
        end if;
        select array_agg(e) into ret
        from (
            select unnest(a1)
            intersect
            select unnest(a2)
        ) as dt(e);
        return ret;
    end;
    $$ language plpgsql;


"""
print(sql)
cur.execute(sql)
#rows = cur.fetchall()
#for row in rows:
#   print(row[0])

conn.closed
