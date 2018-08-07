import os
import sys
import json
import psycopg2
import settings

idea = sys.argv[1]
idea = json.loads(idea)

conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                         user='" + settings.DB_USER + "'\
                         password='" + settings.DB_PASS + "'\
                         host='" + settings.DB_HOST + "'")
cur = conn.cursor()
conn.autocommit = True


#-----------------------------------------------------------------------------------------------

print("Ideal match")
sql = "SELECT unnest(sourceip) \
        FROM idea1 \
        WHERE ( category && ARRAY" + str(idea['Category']) + ") \
            AND ( targetport = ARRAY" + str(idea['Target'][0]['Port']) + " ) \
            AND ( targetip && ARRAY[inet '" + "', inet '".join(idea['Target'][0]['IP4']) + "']) \
            AND id != '" + str(idea['ID']) + "';"

ideal = set()
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    ideal.add(row[0])

print(str(len(ideal)))
print(str(ideal))


#-----------------------------------------------------------------------------------------------

combo_arr = ['Attempt.Exploit',
             'Attempt.Login',
             'Intrusion.Botnet']

for combo_type in combo_arr:
    print("\nCombination match: Recon.Scanning + " + combo_type)
    sql = "SELECT unnest(sourceip) \
            FROM idea1 \
            WHERE (( 'Recon.Scanning' = ANY (category) \
                AND '" + combo_type + "' = ANY (ARRAY" + str(idea['Category']) + ") ) \
                OR ( '" + combo_type + "' = ANY (category) \
                AND 'Recon.Scanning' = ANY (ARRAY" + str(idea['Category']) + " ) )) \
                AND ( targetip && ARRAY[inet '" + "',inet '".join(idea['Target'][0]['IP4']) + "'] ) \
                AND id != '" + str(idea['ID']) + "';"

    cur.execute(sql)
    rows = cur.fetchall()
    combo = set()
    for row in rows:
        combo.add(row[0])

    print(str(combo))


#----------------------------------------------------------------------------------------------

print("\nMatch with history") 

source = []
for i in idea['Source']:
    if 'IP4' in i:
        source.extend(i['IP4'])
sourceIP = str(source).replace('[', '{').replace(']', '}').replace("'", "") 

target = []
targetp = []
for i in idea['Target']:
    if 'IP4' in i:
        target.extend(i['IP4'])
    if 'Port' in i:
        targetp.extend(i['Port'])
targetIP = str(target).replace('[', '{').replace(']', '}').replace("'", "")   
targetPort = str(targetp).replace('[', '{').replace(']', '}').replace("'", "")  

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

for ip in source:
    cur.execute("SELECT * \
        FROM features \
        WHERE sourceip = '" + str(ip) + "';")
    result = cur.fetchone()

    sql = "SELECT unnest(sourceip)\
            FROM history \
            WHERE '" + str(ip) + "' = ANY (sourceip) \
                AND (('" + str(sourceIP) + "' == sourceip ) \
                    OR \
                    ( SELECT sourceip FROM features \
                        WHERE cc = " + str(result[1]) + " \
                        AND bot = " + str(result[2]) + " \
                        AND port_23_2323 = " + str(result[3]) + " \
                        AND spam = " + str(result[4]) + "\
                    )) \
                AND ( array_length( array_intersect(" + str(targetP) + ", targetport), 1) > 3) ) \
                AND floor(log(array_length(targetip, 1))+1) = floor(log(array_length(" + str(targetIP) + ", 1))+1) \
                AND id != '" + str(idea['ID']) + "';"

    cur.execute(sql)
    rows = cur.fetchall()
    combo = set()
    for row in rows:
        combo.add(row[0])

    print(str(combo))