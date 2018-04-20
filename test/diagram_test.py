from graphviz import Digraph


# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

lineage = {
    "0": {
        "host": "ip-172-31-21-52",
        "direction": "INPUT",
        "src": "80.111.53.17",
        "sport": 44570,
        "dst": "172.31.21.52",
        "dport": 5000,
        "type": "TCP",
        "data": "POST /login HTTP/1.1Host: 34.246.59.142:5000User-Agent: python-requests/2.18.4Accept-Encoding: gzip, deflateAccept: */*Connection: keep-aliveContent-Length: 31Content-Type: application/x-www-form-urlencoded"
    },
    "1": {
        "host": "ip-172-31-21-52",
        "direction": "INPUT",
        "src": "80.111.53.17",
        "sport": 44570,
        "dst": "172.31.21.52",
        "dport": 5000,
        "type": "TCP",
        "data": "username=rmurphy&password=12345"
    },
    "2": {
        "host": "ip-172-31-21-52",
        "direction": "INPUT",
        "src": "127.0.0.1",
        "sport": 33386,
        "dst": "127.0.0.1",
        "dport": 5432,
        "type": "TCP",
        "data": ":userubuntudatabasefypclient_encoding'utf-8'"
    },
    "3": {
        "host": "ip-172-31-25-217",
        "direction": "INPUT",
        "src": "34.246.59.142",
        "sport": 49350,
        "dst": "172.31.25.217",
        "dport": 5432,
        "type": "TCP",
        "data": ":userubuntudatabasefypclient_encoding'utf-8'"
    },
    "4": {
        "host": "ip-172-31-21-52",
        "direction": "OUTPUT",
        "src": "127.0.0.1",
        "sport": 5432,
        "dst": "127.0.0.1",
        "dport": 33386,
        "type": "TCP",
        "data": "RSapplication_nameSclient_encodingUTF8SDateStyleISO, MDYSinteger_datetimesonSIntervalStylepostgresSis_superuseronSserver_encodingUTF8Sserver_version9.5.12S!session_authorizationubuntuS#standard_conforming_stringsonSTimeZoneUTCKQwmZI"
    },
    "5": {
        "host": "ip-172-31-25-217",
        "direction": "OUTPUT",
        "src": "172.31.25.217",
        "sport": 5432,
        "dst": "34.246.59.142",
        "dport": 49350,
        "type": "TCP",
        "data": "RSapplication_nameSclient_encodingUTF8SDateStyleISO, MDYSinteger_datetimesonSIntervalStylepostgresSis_superuseronSserver_encodingUTF8Sserver_version9.5.12S!session_authorizationubuntuS#standard_conforming_stringsonSTimeZoneUTCKQwmZI"
    },
    "6": {
        "host": "ip-172-31-21-52",
        "direction": "INPUT",
        "src": "127.0.0.1",
        "sport": 33386,
        "dst": "127.0.0.1",
        "dport": 5432,
        "type": "TCP",
        "data": "QjSELECT username FROM users WHERE username = lower('rmurphy') AND password = crypt('12345', password);"
    },
    "7": {
        "host": "ip-172-31-25-217",
        "direction": "INPUT",
        "src": "34.246.59.142",
        "sport": 49350,
        "dst": "172.31.25.217",
        "dport": 5432,
        "type": "TCP",
        "data": "QjSELECT username FROM users WHERE username = lower('rmurphy') AND password = crypt('12345', password);"
    },
    "8": {
        "host": "ip-172-31-21-52",
        "direction": "OUTPUT",
        "src": "127.0.0.1",
        "sport": 5432,
        "dst": "127.0.0.1",
        "dport": 33386,
        "type": "TCP",
        "data": "T!username@DrmurphyCSELECT 1ZI"
    },
    "9": {
        "host": "ip-172-31-25-217",
        "direction": "OUTPUT",
        "src": "172.31.25.217",
        "sport": 5432,
        "dst": "34.246.59.142",
        "dport": 49350,
        "type": "TCP",
        "data": "T!username@DrmurphyCSELECT 1ZI"
    },
    "10": {
        "host": "ip-172-31-21-52",
        "direction": "OUTPUT",
        "src": "172.31.21.52",
        "sport": 5000,
        "dst": "80.111.53.17",
        "dport": 44570,
        "type": "TCP",
        "data": "HTTP/1.1 200 OKX-Powered-By: ExpressContent-Type: application/json; charset=utf-8Content-Length: 212ETag: W/\"d4-FKD/cypjNbB97k9DejIyV1bVuoo\"Date: Fri, 20 Apr 2018 03:03:24 GMTConnection: keep-alive{\"success\":true,\"message\":\"Login successful\",\"token\":\"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJtdXJwaHkiLCJpYXQiOjE1MjQxOTM0MDQsImV4cCI6MTUyNDE5NzAwNH0.5o4R0WQsu8MaVYn9tcWibS8UiwUxMiC9tEqTcoDknSU\"}"
    }
}


def build_graph_from_lineage(filename, lineage):
    diagram = Digraph('G')
    nodes = {}
    ip_ownership = {}
    for key in lineage:
        temp = lineage[key]['src']
        temp1 = lineage[key]['dst']
        if temp != '127.0.0.1' and temp1 != '127.0.0.1':
            if lineage[key]['src'] not in nodes:
                nodes.update({lineage[key]['src']: ['{}-from'.format(key)]})
            else:
                nodes[lineage[key]['src']].append('{}-from'.format(key))

            if lineage[key]['dst'] not in nodes:
                nodes.update({lineage[key]['dst']: ['{}-to'.format(key)]})
            else:
                nodes[lineage[key]['dst']].append('{}-to'.format(key))

            if lineage[key]['direction'] == 'INPUT':
                ip_ownership.update({lineage[key]['dst']: lineage[key]['host']})
            else:
                ip_ownership.update({lineage[key]['src']: lineage[key]['host']})
        else:
            if lineage[key]['host'] not in nodes:
                nodes.update({lineage[key]['host']: ['{}-from'.format(key)]})
                nodes[lineage[key]['host']].append('{}-to'.format(key))
            else:
                nodes[lineage[key]['host']].append('{}-from'.format(key))
                nodes[lineage[key]['host']].append('{}-to'.format(key))

    to_delete = []
    for key in nodes:
        if key in ip_ownership.keys() and ip_ownership[key] in nodes:
            nodes[ip_ownership[key]] = nodes[ip_ownership[key]] + nodes[key]
            to_delete.append(key)

    for key in to_delete:
        nodes.pop(key)

    for host in nodes:
        with diagram.subgraph(name='cluster-{}'.format(host)) as subgraph:
            subgraph.attr(style='filled')
            subgraph.attr(color='lightgrey')
            subgraph.node_attr.update(style='filled', color='white')
            for node in nodes[host]:
                subgraph.node(node, label='Step-{}'.format(node.split('-')[0]))
            subgraph.attr(label=host)

    final_node = 0
    for key in lineage:
        diagram.edge('{}-from'.format(key), '{}-to'.format(key), label='data-{}'.format(key))
        if int(key) > 0:
            diagram.edge('{}-to'.format(int(key) - 1), '{}-from'.format(key), color='red')
        final_node = int(key)

    diagram.edge('start', '0-from')
    diagram.edge('{}-to'.format(final_node), 'end')

    diagram.node('start', shape='Mdiamond')
    diagram.node('end', shape='Msquare')

    diagram.view()



build_graph_from_lineage('test', lineage)
