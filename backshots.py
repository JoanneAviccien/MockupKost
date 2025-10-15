import networkx as nx
import networkx.readwrite as json_graph
import numpy as np
import matplotlib.pyplot as plt
import json

#fungsi untuk dijkstra
def polbanpath(tujuanawal, polban, graph):
    shortest_path = nx.dijkstra_path(graph, source=tujuanawal, target=polban)
    shortest_path_length = nx.dijkstra_path_length(graph, source=tujuanawal, target=polban)
    return shortest_path, shortest_path_length

def showhighlightpath(graph,ax,pos,shortest_path):
    weight_label = nx.get_edge_attributes(graph, 'weight')
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    
    nx.draw_networkx_edge_labels(graph, ax=ax, pos=pos, edge_labels=weight_label, label_pos=0.3, font_weight='light', font_size=5, font_color='gray')
    nx.draw_networkx(graph,ax=ax,pos=pos, edge_color='blue',font_weight='light', font_size=5)
    nx.draw_networkx(graph,ax=ax,pos=pos,edgelist=path_edges, node_color='orange', edge_color='orange', font_weight='light', font_size=5, font_color='gray')
    
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    ax.clear()
    
    bg_image = plt.imread('bg.png')
    ax.imshow(bg_image, extent=[x_min, x_max, y_min, y_max], aspect='auto', alpha=0.5, zorder=0)
    
    nx.draw_networkx_edge_labels(graph, ax=ax, pos=pos, edge_labels=weight_label, label_pos=0.3, font_weight='light', font_size=5, font_color='gray')
    nx.draw_networkx(graph,ax=ax,pos=pos, edge_color='blue',font_weight='light', font_size=5)
    nx.draw_networkx(graph,ax=ax,pos=pos,edgelist=path_edges, node_color='orange', edge_color='orange', font_weight='light', font_size=5, font_color='gray')
    
    plt.title(f"Rute {shortest_path[0]} Ke {shortest_path[-1]}")
    ax.set_axis_on()

def loadgraphdb(filepath):
    with open(filepath, 'r') as f:
        mapdb = json.load(f)
    return json_graph.node_link_graph(mapdb, edges="edges")

def get_kosan_nodes(graph):
    """
    Extract all kosan nodes from the graph
    Returns a list of node names that contain 'Kosan'
    """
    return [node for node in graph.nodes() if 'Kosan' in str(node)]

def calculate_all_paths_to_polban(graph):
    """
    Calculate shortest paths from all kosan nodes to Polban
    Returns a dictionary with kosan names as keys and (path, distance) as values
    """
    kosan_nodes = get_kosan_nodes(graph)
    paths_data = {}
    
    for kosan in kosan_nodes:
        try:
            path, distance = polbanpath(kosan, 'Polban', graph)
            paths_data[kosan] = {
                'path': path,
                'distance': distance,
                'formatted_distance': f"{distance:.2f} meter"
            }
        except nx.NetworkXNoPath:
            paths_data[kosan] = {
                'path': None,
                'distance': float('inf'),
                'formatted_distance': "Tidak ada jalur"
            }
    
    # Sort by distance
    return dict(sorted(paths_data.items(), key=lambda x: x[1]['distance']))



# now_viewing2 = loadgraphdb('mapdb/ciwaruga.json')
# pos = nx.spring_layout(now_viewing2, seed=15)
# shortpath, shortest_path_length = polbanpath('Kosan O Ciwaruga Bahagia','Polban', now_viewing2)
# showhighlightpath(now_viewing2,pos,shortpath)

# now_viewing3 = loadgraphdb('mapdb/gegerkalong.json')
# pos = nx.spring_layout(now_viewing3, seed=40)
# shortpath, shortest_path_length = polbanpath('Kosan F Gegerkalong Hijau','Polban', now_viewing3)
# showhighlightpath(now_viewing3,pos,shortpath)