from graphviz import Digraph
import re
diagram = Digraph('G')

# NOTE: the subgraph name needs to begin with 'cluster' (all lowercase)
#       so that Graphviz recognizes it as a special cluster subgraph

lineage = {0: {'host': 'ip-172-31-21-52', 'direction': 'INPUT', 'src': '80.111.53.17', 'sport': 60672, 'dst': '172.31.21.52', 'dport': 5000, 'type': 'TCP', 'data': 'POST /login HTTP/1.1Host: ec2-34-246-59-142.eu-west-1.compute.amazonaws.com:5000User-Agent: python-requests/2.18.4Accept-Encoding: gzip, deflateAccept: */*Connection: keep-aliveContent-Length: 31Content-Type: application/x-www-form-urlencoded'}, 1: {'host': 'ip-172-31-21-52', 'direction': 'INPUT', 'src': '80.111.53.17', 'sport': 60672, 'dst': '172.31.21.52', 'dport': 5000, 'type': 'TCP', 'data': 'username=rmurphy&password=12345'}, 2: {'host': 'ip-172-31-21-52', 'direction': 'INPUT', 'src': '127.0.0.1', 'sport': 41232, 'dst': '127.0.0.1', 'dport': 5432, 'type': 'TCP', 'data': ":userubuntudatabasefypclient_encoding'utf-8'"}, 3: {'host': 'ip-172-31-22-145', 'direction': 'INPUT', 'src': '34.246.59.142', 'sport': 60762, 'dst': '172.31.22.145', 'dport': 5432, 'type': 'TCP', 'data': ":userubuntudatabasefypclient_encoding'utf-8'"}, 4: {'host': 'ip-172-31-22-145', 'direction': 'OUTPUT', 'src': '172.31.22.145', 'sport': 5432, 'dst': '34.246.59.142', 'dport': 60762, 'type': 'TCP', 'data': 'RSapplication_nameSclient_encodingUTF8SDateStyleISO, MDYSinteger_datetimesonSIntervalStylepostgresSis_superuseronSserver_encodingUTF8Sserver_version9.5.12S!session_authorizationubuntuS#standard_conforming_stringsonSTimeZoneUTCK^PdZI'}, 5: {'host': 'ip-172-31-21-52', 'direction': 'OUTPUT', 'src': '127.0.0.1', 'sport': 5432, 'dst': '127.0.0.1', 'dport': 41232, 'type': 'TCP', 'data': 'RSapplication_nameSclient_encodingUTF8SDateStyleISO, MDYSinteger_datetimesonSIntervalStylepostgresSis_superuseronSserver_encodingUTF8Sserver_version9.5.12S!session_authorizationubuntuS#standard_conforming_stringsonSTimeZoneUTCK^PdZI'}, 6: {'host': 'ip-172-31-21-52', 'direction': 'INPUT', 'src': '127.0.0.1', 'sport': 41232, 'dst': '127.0.0.1', 'dport': 5432, 'type': 'TCP', 'data': "QjSELECT username FROM users WHERE username = lower('rmurphy') AND password = crypt('12345', password);"}, 7: {'host': 'ip-172-31-22-145', 'direction': 'INPUT', 'src': '34.246.59.142', 'sport': 60762, 'dst': '172.31.22.145', 'dport': 5432, 'type': 'TCP', 'data': "QjSELECT username FROM users WHERE username = lower('rmurphy') AND password = crypt('12345', password);"}, 8: {'host': 'ip-172-31-22-145', 'direction': 'OUTPUT', 'src': '172.31.22.145', 'sport': 5432, 'dst': '34.246.59.142', 'dport': 60762, 'type': 'TCP', 'data': 'T!username@DrmurphyCSELECT 1ZI'}, 9: {'host': 'ip-172-31-21-52', 'direction': 'OUTPUT', 'src': '127.0.0.1', 'sport': 5432, 'dst': '127.0.0.1', 'dport': 41232, 'type': 'TCP', 'data': 'T!username@DrmurphyCSELECT 1ZI'}, 10: {'host': 'ip-172-31-21-52', 'direction': 'OUTPUT', 'src': '172.31.21.52', 'sport': 5000, 'dst': '80.111.53.17', 'dport': 60672, 'type': 'TCP', 'data': 'HTTP/1.1 200 OKX-Powered-By: ExpressContent-Type: application/json; charset=utf-8Content-Length: 212ETag: W/"d4-0ZgZX+ro2JLKIuu5o2VQxUJsNrc"Date: Thu, 12 Apr 2018 05:52:59 GMTConnection: keep-alive{"success":true,"message":"Login successful","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InJtdXJwaHkiLCJpYXQiOjE1MjM1MTIzNzksImV4cCI6MTUyMzUxNTk3OX0.5oBKVJFZV9RlNtc0UqLIGBHchlcWM07vIbA3KaswLYA"}'}}

#
nodes = {}
ip_ownership = {}
for key in lineage:
    if lineage[key]['src'] is not '127.0.0.1' and lineage[key]['dst']:
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
            ip_ownership.update({lineage[key]['src']:lineage[key]['host']})
    else:
        if lineage[key]['host'] not in nodes:
            nodes.update({lineage[key]['host']: ['{}-from'.format(key)]})
            nodes[lineage[key]['host']].append('{}-to'.format(key))
        else:
            nodes[lineage[key]['host']].append('{}-from'.format(key))
            nodes[lineage[key]['host']].append('{}-to'.format(key))

print(nodes)
to_delete = []
for key in nodes:
    if key in ip_ownership.keys() and ip_ownership[key] in nodes:
        nodes[ip_ownership[key]] = nodes[ip_ownership[key]] + nodes[key]
        to_delete.append(key)

for key in to_delete:
    nodes.pop(key)

print(nodes)

for host in nodes:
    print(host)
    with diagram.subgraph(name='cluster-{}'.format(host)) as subgraph:
        subgraph.attr(style='filled')
        subgraph.attr(color='lightgrey')
        subgraph.node_attr.update(style='filled', color='white')
        for node in nodes[host]:
            subgraph.node(node)
        subgraph.attr(label=host)

import re

final_node = 0
for key in lineage:
    diagram.edge('{}-from'.format(key), '{}-to'.format(key), label=re.sub("(.{64})", "\\1\n", lineage[key]['data'], 0,
                                                                          re.DOTALL))
    if key > 0:
        diagram.edge('{}-to'.format(key - 1), '{}-from'.format(key))
    final_node = key

diagram.edge('start', '0-from')
diagram.edge('{}-to'.format(final_node), 'end')

diagram.node('start', shape='Mdiamond')
diagram.node('end', shape='Msquare')

diagram.view()
#
#
# g = Digraph('G')
# with g.subgraph(name='cluster_0') as c:
#     c.attr(style='filled')
#     c.attr(color='lightgrey')
#     c.node_attr.update(style='filled', color='white')
#     c.node('a0')
#     c.node('a1')
#     c.attr(label='Client')
#
# with g.subgraph(name='cluster_1') as c:
#     c.attr(style='filled')
#     c.attr(color='lightgrey')
#     c.node_attr.update(style='filled', color='white')
#     c.edges([('b0', 'b1'), ('b1', 'b2'), ('b3', 'b4')])
#     c.attr(label='Server 1')
#
# with g.subgraph(name='cluster_2') as c:
#     c.attr(style='filled')
#     c.attr(color='lightgrey')
#     c.node_attr.update(style='filled', color='white')
#     c.edges([('c0', 'c1')])
#     c.attr(label='Server 2')
#
# g.edge('start', 'a0')
# g.edge('a0', 'b0')
# g.edge('b2', 'c0')
# g.edge('c1', 'b3')
# g.edge('b4', 'a1')
# g.edge('a1', 'end')
#
# g.node('start', shape='Mdiamond')
# g.node('end', shape='Msquare')
#
# g.view()