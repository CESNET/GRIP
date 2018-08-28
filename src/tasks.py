from celery_app import app 
import json
import ast
import string
import sys

import settings
from import_main import import_idea_to_actual
from import_history import import_idea_to_history
from import_uniq_ip import import_idea_to_uniq
from grouping_real_time import grouping
from neo4j_db import Neo4jDB
from create_node_from_idea import create_node


# zpracovani do databaze
@app.task(serializer='json', name='add')
def add(msq):
    rawdata = json.loads(msq)
    idea = dict(rawdata)
    # cisteni, jestli ma minimum informaci
    if 'Node' in idea and 'Source' in idea and 'Category' in idea and 'Description' in idea and 'EventTime' in idea and 'CeaseTime' in idea and 'DetectTime' in idea and 'Target' in idea:
        if 'Availability.Sabotage' in idea['Category'] or 'Suspicious.TOR' in idea['Category'] or 'Availability.Outage' in idea['Category'] or [s for s in idea['Category'] if 'Vulnerable' in s or 'Other' in s]:
            sys.exit(0)
    else:
        sys.exit(0)

    source = []
    for ip4 in idea['Source']:
        if 'IP4' in ip4:
            source.extend(ip4['IP4'])
    if not source:
        sys.exit(0)

    import_idea_to_actual(idea)
    import_idea_to_history(idea)
    import_idea_to_uniq(idea)
   
    group = [] 
    group = grouping(idea)

    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])

    reasons = [#'Ideal match', 
               'Combination match with Attemp.Exploit', 'Combination match with Attempt.Login', 'Combination match with Intrusion.Botnet', 'Match with history']
    count = 0

    for g in group:
        if not g:
            continue
        neo.add_ip(source, g, create_node(idea).replace('"', '\"'), reasons[count])
        count += 1
        with open('text.txt', 'a') as file:
            file.write(str(idea['Source'][0]['IP4']) + '\n')


@app.task(serializer='json', name='find_ip')
def find_ip(ipaddr):
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_ip(ipaddr)

    with open('text.txt', 'a') as file:
        file.write(str(result[0]) + '\n')

    return str(result[0])


@app.task(serializer='json', name='find_group')
def find_group(group):
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_group(group)

    with open('text.txt', 'a') as file:
        file.write(str(result) + '\n')


@app.task(serializer='json', name='update')
def update():
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.update()

    with open('text.txt', 'a') as file:
        file.write('update\n')

