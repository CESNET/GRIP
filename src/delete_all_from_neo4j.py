from neo4j.v1 import GraphDatabase
import settings

###-CLASSES-----------------------------------------------------------------------------------------


class Neo4jDB(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self._driver.close()

    def find_group(self, group):
        with self._driver.session() as session:
            result = session.read_transaction(self._find_group, group)
        return result


    @staticmethod
    def _find_group(tx, group):
        result = []
        tx.run("MATCH (n) "
               "DETACH DELETE n")
            



def find_list_db():
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_group('')
    return result

find_list_db()
