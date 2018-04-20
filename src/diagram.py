from graphviz import Digraph


def build_graph_from_lineage(filename, lineage):
    diagram = Digraph('G')
    nodes = {}
    ip_ownership = {}
    for key in lineage:
        if lineage[key]['src'] != '127.0.0.1' and lineage[key]['dst'] != '127.0.0.1':
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

    diagram.render(filename)