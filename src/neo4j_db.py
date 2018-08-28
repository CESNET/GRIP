import datetime
import random
import string

import settings
from neo4j.v1 import GraphDatabase


class Neo4jDB(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self._driver.close()


    def add_ip(self, ip, lists, message, reason):
        #all_IPs = listIp(ips)

        with self._driver.session() as session:
            #for ip in all_IPs:
                ip = session.write_transaction(self._add_ip_as_node, ip, lists, message, reason)
        return ip


    def find_ip(self, ip):
        with self._driver.session() as session:
            message = session.read_transaction(self._find_ip_as_node, ip)
            return message


    def find_group(self, group):
        with self._driver.session() as session:
            message = session.read_transaction(self._find_group_as_node, group)
            return message


    def update(self):
        with self._driver.session() as session:
            message = session.write_transaction(self._update_nodes)
            return message


    @staticmethod
    def _add_ip_as_node(tx, ip, lists, message, reason):
        date = datetime.datetime.now()
        random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))

        for ip in lists:
            result = tx.run("MATCH (ip:Ip {name:\"" + ip + "\"}) "
                            "RETURN ip")
            exist = result.single()

        #    if exist == None:
        #        result = tx.run("CREATE (ip:Ip {name:\"" + ip + "\"}) "
        #                        "CREATE (note:Note {" + message + "}) "
        #                        "CREATE (note)-[:DESCRIBES]->(ip) "
        #                        "RETURN ip")

         #   else:
            result = tx.run("CREATE (note:Note {" + message + "}) "
                                "WITH note "
                                "MERGE (ip:Ip {name:\"" + ip + "\"}) "
                                "CREATE (note)-[:DESCRIBES]->(ip) "
                                "RETURN ip")

        if lists != None:
            result = tx.run("CREATE (group:Group {name:\"" + random_string + "\", last_mod:\"" + str(date) + "\", reason: \"" + reason + "\"}) "
                            "RETURN group")
            for ip in lists:
                result = tx.run("MATCH (ip:Ip {name:\"" + ip + "\"}) "
                                "MATCH (group:Group {name:\"" + random_string + "\"}) "
                                "CREATE (ip)-[:PART_OF]->(group) "
                                "RETURN ip")


    @staticmethod
    def _find_ip_as_node(tx, ip):
        result = []
        for record in tx.run("MATCH (ip:Ip {name:\"" + ip + "\"}) "
                             "MATCH (ip)-[:PART_OF]->(group) "
                             "RETURN group.last_mod, group.reason ORDER BY group.last_mod, group.reason"):
            result.append((record['group.last_mod'], record['group.reason']))
        return result


    @staticmethod
    def _find_group_as_node(tx, group):
        result = []
        for record in tx.run("MATCH (g:Group {name:\"" + group + "\"}) "
                             "MATCH (ip)-[:PART_OF]->(group) "
                             "RETURN ip.name ORDER BY ip.name"):
            result.append(record['ip.name'])
        return result


    @staticmethod
    def _update_nodes(tx):
        date = datetime.datetime.now()-datetime.timedelta(days=1)
        result = tx.run("MATCH (group:Group) "
                        "WHERE group.last_mod<\"" + str(date) + "\" "
                        "DETACH DELETE group")
        #result = tx.run("MATCH (d:Note)-[:DESCRIBES]->(a:Ip) "
        #                "WHERE NOT (a)-[:PART_OF]->() "
        #                "DETACH DELETE a, d")
        return result
