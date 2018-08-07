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

cur.execute("""drop function if exists array_intersect(int[], int[]);
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
    $$ language plpgsql;""")


sql = """SELECT sourceip
         FROM uniq_ip
         WHERE array_length(array_intersect(targetport, ARRAY[23, 2323, 21, 22, 80]), 1) >= 3
      ;"""

cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    print(row[0])


#-----------------------------------------------------------------------------------------------

attach_arr = ['ET SCAN Potential SSH Scan OUTBOUND',
              'SipVicious Brute Force SIP Tool',
              'Netcore/Netis Router Backdoor Communication Attempt',
              'ET DOS Possible NTP DDoS Inbound Frequent Un-Authed MON_LIST Requests IMPL 0x03',
              'ET DOS Possible Memcached DDoS Amplification Query (set)',
              'Version Request (UDP)',
              'Comm. with host known as malware source']

for attach_type in attach_arr:
    print("\nAttachment match: " + attach_type)
    sql = """SELECT sourceip
             FROM uniq_ip
             WHERE ( attach LIKE '%""" + attach_type + """%' )
                 ;"""

    cur.execute(sql)
    rows = cur.fetchall()
    ips = set()
    for row in rows:
        ips.add(row[0])

    print(str(ips))


#-----------------------------------------------------------------------------------------------

print("Botnets C&C")
sql = """SELECT sourceip
         FROM uniq_ip
         WHERE ( 23 = ANY (targetport) AND 2323 = ANY (targetport) )
             AND ( 'Recon.Scanning' = ANY (category) OR 'Attempt.Login' = ANY (category));"""

port23 = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    port23.add(row[0])