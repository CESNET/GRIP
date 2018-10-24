from flask import Flask, current_app, render_template, request, redirect, url_for, jsonify
from neo4j.v1 import GraphDatabase
import settings
###-CLASSES-----------------------------------------------------------------------------------------

      
            
class WebApp(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
class Neo4jDB(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))


    def close(self):
        self._driver.close()


    def find_list(self):
        with self._driver.session() as session:
            result = session.read_transaction(self._find_list)
        return result


    def find_ip(self, ip):
        with self._driver.session() as session:
            result = session.read_transaction(self._find_ip, ip)
        return result


    def find_group(self, group):
        with self._driver.session() as session:
            result = session.read_transaction(self._find_group, group)
        return result


    @staticmethod
    def _find_list(tx):
        result = []
        for record in tx.run("MATCH (group:Group) "
                             "RETURN group.name, group.reason ORDER BY group.name, group.reason"):
            result.append((record['group.name'], record['group.reason']))
        return result


    @staticmethod
    def _find_ip(tx, ip):
        result = []
        for record in tx.run("MATCH (ip:Ip {name:\"" + ip + "\"}) "
                             "MATCH (ip)-[PART_OF]->(group) "
                             "RETURN group.name, group.reason ORDER BY group.name, group.reason"):
            result.append((record['group.name'], record['group.reason']))
        return result


    @staticmethod
    def _find_group(tx, group):
        result = []
        for record in tx.run("MATCH (group:Group {name:\"" + group + "\"}) "
                             "MATCH (ip:Ip)-[PART_OF]->(group) "
                             "RETURN ip.name ORDER BY ip.name"):
            result.append(record['ip.name'])
        return result


app = WebApp(__name__)
                   

###-FUNCTIONS---------------------------------------------------------------------------------------

def find_list_db():
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_list()
    return result
   

def find_ip_db(ip):
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_ip(ip)
    return result
    
    
def find_groups_db(botnet):
    neo = Neo4jDB(settings.NEO4J['host'], settings.NEO4J['user'], settings.NEO4J['password'])
    result = neo.find_group(botnet)
    return result


###-ROUTING-----------------------------------------------------------------------------------------

@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


@app.route('/groups/', methods=['GET'])
def find_list():
   
    if request.args.get('addr') != None:
        addr = request.args.get('addr').split('.')
        return redirect(url_for('find_ip', ip1=int(addr[0]), ip2=int(addr[1]), ip3=int(addr[2]), ip4=int(addr[3])))

    # make task
    list = find_list_db()
    
 
    #if list:
    return jsonify(list)
    
    #return render_template('error.html', err="Unexpected error while listing groups.")     



@app.route('/groups/<int:ip1>.<int:ip2>.<int:ip3>.<int:ip4>', methods=['GET'])
def find_ip(ip1, ip2, ip3, ip4):
  
    # is addr an IP address?
    parts = [ip1, ip2, ip3, ip4]
    if not parts[3]:
        return render_template('error.html', err="Wrong format of given IP address.")
    for i in range(4):
        if int(parts[i]) < 0 or int(parts[i]) > 255:
            return render_template('error.html', err="Wrong format of given IP address.")
        
    # make task
    ip = str(ip1) + '.' + str(ip2) + '.' + str(ip3) + '.' + str(ip4)
    list = find_ip_db(ip)
    
 
    #if list:
    return jsonify(list)
    
    #return render_template('error.html', err="Unexpected error while listing groups with given IP.")     


@app.route('/group/<string:botnet>', methods=['GET'])
def find_groups(botnet):
  
    list = find_groups_db(botnet)
 
    #if list:
    return jsonify(list) 
    
    #return render_template('error.html', err="Unexpected error while listing IPs of given group name.")     




if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, threaded=True)  
    
      
