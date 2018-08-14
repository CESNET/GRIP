import ast
import datetime
import json
import operator
import settings
import psycopg2


true = True

################################################################################################## 

##################################################################################################

def get_list():
    conn = psycopg2.connect("dbname='" + settings.DB_NAME + "'\
                             user='" + settings.DB_USER + "'\
                             password='" + settings.DB_PASS + "'\
                             host='" + settings.DB_HOST + "'")
    cur = conn.cursor()
    conn.autocommit = True

    sql = """SELECT attach FROM history;"""
    cur.execute(sql)
    rows = cur.fetchall()


    file_write = open(settings.PWD + 'attach_types.txt', 'w')
    count = 0

    attach_types = []
    attach_types_set = set()
    result = []
    filik = settings.PWD + 'count_of_attach.txt'


    for row in rows:
        if row[0] != '':
            count += 1
            line = row[0]
            if len(line.split('|')) > 1:
                try:
                    sign = line.split('|')[4]
                    attach_types.append(sign)
                    attach_types_set.add(sign)
                except:
                    file_write.write(str(line) + '\n')
            elif line.startswith('Drop RPF'):
                try:
                    attach_types.append('Drop RPF')
                    attach_types_set.add('Drop RPF')
                except:
                    file_write.write(str(line) + '\n')
            elif len(line.split('\t')) > 1:
                try:
                    sign = line.split('\t')[4] + ' ' + line.split('\t')[5]
                    attach_types.append(sign)
                    attach_types_set.add(sign)
                except:
                    file_write.write(str(line) + '\n')
            else:
                try:
                    sign = json.dumps(line.replace("u'", '"').replace("'", '"'))
                    sign = json.loads(sign)
                    sign = (ast.literal_eval(sign))
                    attach_types.append(sign['alert']['signature'])
                    attach_types_set.add(sign['alert']['signature'])
                except:
                    file_write.write(str(line) + '\n')

    counter = 0
    result_list = []
    for item in attach_types_set:
        for i in attach_types:
            if item == i:
                counter += 1
        if counter > 100:
            result_list.append(item)
        result.append({'name': item, 'count': counter})
        counter = 0

    return result_list

    result.sort(key=operator.itemgetter('count'), reverse=True)

    for i in result:
        print(i) 
    print(str(count))
    return
