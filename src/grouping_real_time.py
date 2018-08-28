import os
import sys
import json
import psycopg2
import settings


def grouping(idea):
    group = []

    conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                             user='" + settings.DB_USER + "'\
                             password='" + settings.DB_PASS + "'\
                             host='" + settings.DB_HOST + "'")
    cur = conn.cursor()
    conn.autocommit = True


    #-----------------------------------------------------------------------------------------
    # Ideal match
    sql = "SELECT unnest(sourceip) \
            FROM actual \
            WHERE ( category && ARRAY" + str(idea['Category']) + ") \
                AND ( targetport = ARRAY" + str(idea['Target'][0]['Port']) + " ) \
                AND ( targetip && ARRAY[inet '" + "', inet '".join(idea['Target'][0]['IP4']) + "']) \
                AND id != '" + str(idea['ID']) + "';"

    ideal = set()
    #cur.execute(sql)
    #rows = cur.fetchall()
    #for row in rows:
    #    ideal.add(row[0])

    #group.append(ideal)


    #-----------------------------------------------------------------------------------------
    # Combination match
    combo_arr = ['Attempt.Exploit',
                 'Attempt.Login',
                 'Intrusion.Botnet']

    for combo_type in combo_arr:
        sql = "SELECT unnest(sourceip) \
                FROM actual \
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

        group.append(combo)


    #-----------------------------------------------------------------------------------------
    # Match with history

    source = []
    for i in idea['Source']:
        if 'IP4' in i:
            source.extend(i['IP4'])
    sourceIP = str(source).replace('[', '').replace(']', '')#.replace("'", "")

    target = []
    targetp = []
    for i in idea['Target']:
        if 'IP4' in i:
            target.extend(i['IP4'])
        if 'Port' in i:
            targetp.extend(i['Port'])
    targetIP = str(target).replace('[', '').replace(']', '')#.replace("'", "")
    targetPort = str(targetp).replace('[', '').replace(']', '').replace("'", "")

    for ip in source:
        cur.execute("SELECT * \
            FROM features \
            WHERE sourceip = '" + str(ip) + "';")
        result = cur.fetchone()
        if result == None:
            result = ['', False, False, False, False]

        cur.execute("SELECT * FROM features \
                         WHERE sourceip = '" + str(ip) + "' \
                             AND cc = " + str(result[1]) + " \
                             AND bot = " + str(result[2]) + " \
                             AND port_23_2323 = " + str(result[3]) + " \
                             AND spam = " + str(result[4]) + ";")
        result = cur.fetchall()
        if result == (1,):
            result = True
        else:
            result = False

        sql = "SELECT unnest(sourceip)\
                FROM history \
                WHERE '" + str(ip) + "' = ANY (sourceip) \
                    AND ((ARRAY[" + str(sourceIP) + "]::inet[] = sourceip ) \
                        OR " + str(result) + ") \
                    AND ( array_length( array_intersect(ARRAY[" + str(targetPort) + "], targetport), 1) > 3) \
                    AND floor(log(array_length(targetip, 1))+1) = floor(log(array_length(ARRAY[" + str(targetIP) + "]::inet[], 1))+1) \
                    AND id != '" + str(idea['ID']) + "';"

        cur.execute(sql)
        rows = cur.fetchall()
        combo = set()
        for row in rows:
            combo.add(row[0])

        group.append(combo)

        #-------------------------------------------------------------------------------------

        return group
