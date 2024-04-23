import json
import networkx as nx
from networkx.readwrite import json_graph
from networkx.algorithms import community
import matplotlib.pyplot as plt
import logging
from random import random


def read_json_file(filename):
    """ Returns the textnetwork dict
    """
    with open(filename) as f:
        js_graph  = json.load(f)["textnetwork"]

    return js_graph

def _calculate_central_nodes(text_network, maxn=100):
    logging.info('Calculating centrality')
    bc = (nx.betweenness_centrality(text_network,weight='weight'))
    nx.set_node_attributes(text_network, bc, 'betweenness')
    maxn = maxn if maxn <= len(bc) else -1
    bc_threshold = sorted(bc.values(), reverse=True)[maxn]
    to_keep = [n for n in bc if bc[n] > bc_threshold]
    filtered_network = text_network.subgraph(to_keep)
    return filtered_network

def _create_and_assign_communities(text_network):
    logging.info("Assigning communities")
    communities_generator = community.girvan_newman(text_network)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    communities = {}
    for community_list in next_level_communities:
        for item in community_list:
            communities[item] = next_level_communities.index(community_list)
    return communities

def _draw_final_graph(text_network,communities):
    logging.info('Drawing')
    pos = nx.spring_layout(text_network,scale=2)
    color_list = []
    color_map = []
    community_count = max(communities.values())
    for i in range(0,community_count+1):
        color_list.append((random(), random(), random()))
    for node in text_network:
        color_index = communities[node]
        color_map.append(color_list[color_index])
    betweenness = nx.get_node_attributes(text_network,'betweenness')
    betweenness = [x * 10000 for x in betweenness.values()]
    nx.draw(text_network,with_labels=True,node_size=betweenness,font_size=8,node_color=color_map,width=4,edge_cmap=plt.cm.Blues)
    plt.draw()
    plt.show()


def draw_textnetwork(txtnet_graph):

    G = json_graph.node_link_graph(txtnet_graph)

    logging.basicConfig(format='%(asctime)s %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    text_network = _calculate_central_nodes(G)
    communities = _create_and_assign_communities(text_network)
    nx.write_gml(text_network, "text_network.gml")
    _draw_final_graph(text_network,communities)


#tn_graph = read_json_file("tt.json")
#draw_textnetwork(tn_graph)