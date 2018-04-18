from graphviz import Digraph
import re

def build_graph_from_lineage(filename, lineage):
    diagram = Digraph('G')
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
                ip_ownership.update({lineage[key]['src']: lineage[key]['host']})
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

    final_node = 0
    for key in lineage:
        diagram.edge('{}-from'.format(key), '{}-to'.format(key),
                     label=re.sub("(.{64})", "\\1\n", lineage[key]['data'], 0,
                                  re.DOTALL))
        if key > 0:
            diagram.edge('{}-to'.format(key - 1), '{}-from'.format(key))
        final_node = key

    diagram.edge('start', '0-from')
    diagram.edge('{}-to'.format(final_node), 'end')

    diagram.node('start', shape='Mdiamond')
    diagram.node('end', shape='Msquare')

    diagram.render(filename, 'graphs')