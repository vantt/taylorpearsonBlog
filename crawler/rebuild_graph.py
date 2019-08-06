#!/usr/bin/env python3
import json
import json_lines
import csv
import networkx as nx
from networkx.readwrite import json_graph

prefix = 'taylorpearsonBlog'
input_file = 'data/' + prefix + '.jsonl'
output_dir = 'data/graph_result'


def build_graph(file_name):
    graph = nx.DiGraph()

    # rebuild the Graph from crawled data (json-lines)
    with open(file_name, 'rb') as f:
        for item in json_lines.reader(f):
            node_id = str(item['id'])

            # create Node
            if node_id in graph.nodes:
                if 'title' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['title'] = item['title']

                if 'url' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['url'] = item['url']

                if 'description' not in graph.nodes[node_id]:
                    graph.nodes[node_id]['description'] = item['title'] + ' ' + item['url']
            else:
                graph.add_node(node_id,
                               label=node_id,
                               title=item['title'],
                               url=item['url'],
                               description=item['title'] + ' ' + item['url'])

            # create Links
            for to_id, to_url in item['links'].items():
                to_id = str(to_id)

                if to_id in graph.nodes:
                    if 'url' not in graph.nodes[to_id]:
                        graph.nodes[to_id]['url'] = to_url
                else:
                    graph.add_node(to_id, label=to_id, url=to_url)

                if node_id != to_id:
                    graph.add_edge(node_id, to_id)

    # fixing the graph
    removing_nodes = []
    for node, data in graph.nodes(data=True):
        if 'title' not in data or 'url' not in data:
            removing_nodes.append(node)

    for node in removing_nodes:
        graph.remove_node(node)

    return graph


def compute_centrality(graph):
    centrality_values = nx.hits(graph)
    for node_id, centrality in centrality_values[0].items():
        graph.nodes[node_id]['hub'] = centrality
    for node_id, centrality in centrality_values[1].items():
        graph.nodes[node_id]['authority'] = centrality

    centrality_values = nx.pagerank(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['pagerank'] = centrality

    centrality_values = nx.in_degree_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['in_degree'] = centrality

    centrality_values = nx.out_degree_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['out_degree'] = centrality

    centrality_values = nx.closeness_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['closeness'] = centrality

    centrality_values = nx.betweenness_centrality(graph)
    for node_id, centrality in centrality_values.items():
        graph.nodes[node_id]['betweenness'] = centrality

    for node_id, data in graph.nodes(data=True):
        graph.nodes[node_id]['score'] = data['betweenness'] * data['closeness'] * data['pagerank'] * data['authority']

    # centrality_values = nx.eigenvector_centrality(graph)
    # for node_id, centrality in centrality_values.items():
    #     graph.nodes[node_id]['eigenvector'] = centrality


def export_graph(graph, directory):
    # write to GraphML file
    nx.write_graphml(graph, directory + "/" + prefix + ".graphml")

    # write to Gexf file
    nx.write_gexf(graph, directory + "/" + prefix + ".gexf")

    # write to JSON file
    json.dump(json_graph.node_link_data(graph), open(directory + "/" + prefix + ".json", 'w'), indent=2)

    # write to CSV files
    with open(directory + "/" + prefix + '_pages.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            ['id', 'label', 'title', 'url',
             'hub', 'authority', 'pagerank',
             'in_degree', 'out_degree', 'closeness',
             'betweenness'])
        for node, data in graph.nodes(data=True):
            writer.writerow([node, data['label'], data['title'], data['url'],
                             data['hub'], data['authority'], data['pagerank'],
                             data['in_degree'], data['out_degree'],
                             data['closeness'], data['betweenness']])

    with open(directory + "/" + prefix + '_pages_links.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['from', 'to'])
        for f, t, a in graph.edges(data=True):
            writer.writerow([f, t])


my_graph = build_graph(input_file)
compute_centrality(my_graph)
export_graph(my_graph, output_dir)
