import networkx as nx
import networkx.readwrite as json_graph
import json

def savegraphdb(graph, filepath):
    mapdb = json_graph.node_link_data(graph, edges="edges")
    with open(filepath, 'w') as f:
        json.dump(mapdb, f, indent=4)

sarijadi = nx.Graph()
ciwaruga = nx.Graph()
gegerkalong = nx.Graph()

nodes_1 = [
    "Polban",
    "Kosan A Sarijadi Asri",
    "Kosan B Sekeloa Indah",
    "Kosan C Cigadung Raya",
    "Kosan D Ciumbuleuit",
    "Kosan E Villa Sarijadi",
    "Kosan F Sarijadi Baru",
    "Kosan G Cigadung Permai",
    "Kosan H Sarijadi Indah",
    "Kosan I Ciumbuleuit Asri",
    "Kosan J Villa Sekeloa",
    "Kosan K Cigadung Hijau",
    "Kosan L Sarijadi Raya",
    "Kosan M Ciumbuleuit Baru",
    "Kosan N Sarijadi Permai",
    "Kosan O Villa Cigadung",
    "Kosan P Sarijadi Asih",
    "Kosan Q Ciumbuleuit Raya",
    "Kosan R Sarijadi Sentosa",
    "Kosan S Cigadung Asri",
    "Kosan T Villa Ciumbuleuit"
]

sarijadi.add_nodes_from(nodes_1)

edges_1 = [
    ("Polban", "Kosan A Sarijadi Asri", 300),
    ("Polban", "Kosan B Sekeloa Indah", 500),
    ("Polban", "Kosan C Cigadung Raya", 600),
    ("Kosan A Sarijadi Asri", "Kosan B Sekeloa Indah", 250),
    ("Kosan A Sarijadi Asri", "Kosan C Cigadung Raya", 400),
    ("Kosan B Sekeloa Indah", "Kosan D Ciumbuleuit", 300),
    ("Kosan C Cigadung Raya", "Kosan E Villa Sarijadi", 350),
    ("Kosan D Ciumbuleuit", "Kosan F Sarijadi Baru", 200),
    ("Kosan E Villa Sarijadi", "Kosan G Cigadung Permai", 300),
    ("Kosan F Sarijadi Baru", "Kosan H Sarijadi Indah", 250),
    ("Kosan G Cigadung Permai", "Kosan I Ciumbuleuit Asri", 200),
    ("Kosan H Sarijadi Indah", "Kosan J Villa Sekeloa", 150),
    ("Kosan I Ciumbuleuit Asri", "Kosan K Cigadung Hijau", 300),
    ("Kosan J Villa Sekeloa", "Kosan L Sarijadi Raya", 200),
    ("Kosan K Cigadung Hijau", "Kosan M Ciumbuleuit Baru", 250),
    ("Kosan L Sarijadi Raya", "Kosan N Sarijadi Permai", 180),
    ("Kosan M Ciumbuleuit Baru", "Kosan O Villa Cigadung", 300),
    ("Kosan N Sarijadi Permai", "Kosan P Sarijadi Asih", 220),
    ("Kosan O Villa Cigadung", "Kosan Q Ciumbuleuit Raya", 270),
    ("Kosan P Sarijadi Asih", "Kosan R Sarijadi Sentosa", 200),
    ("Kosan Q Ciumbuleuit Raya", "Kosan S Cigadung Asri", 250),
    ("Kosan R Sarijadi Sentosa", "Kosan T Villa Ciumbuleuit", 300),
    ("Polban", "Kosan E Villa Sarijadi", 500),
    ("Kosan C Cigadung Raya", "Kosan H Sarijadi Indah", 400),
    ("Kosan F Sarijadi Baru", "Kosan K Cigadung Hijau", 350),
    ("Kosan I Ciumbuleuit Asri", "Kosan N Sarijadi Permai", 400),
    ("Kosan L Sarijadi Raya", "Kosan Q Ciumbuleuit Raya", 350),
    ("Kosan O Villa Cigadung", "Kosan T Villa Ciumbuleuit", 400)
]

sarijadi.add_weighted_edges_from(edges_1)

nodes_2 = [
    "Polban",
    "Kosan A Ciwaruga Asri",
    "Kosan B Ciwaruga Indah",
    "Kosan C Ciwaruga Baru",
    "Kosan D Ciwaruga Raya",
    "Kosan E Ciwaruga Permai",
    "Kosan F Ciwaruga Hijau",
    "Kosan G Ciwaruga Sentosa",
    "Kosan H Ciwaruga Asih",
    "Kosan I Ciwaruga Sari",
    "Kosan J Ciwaruga Mekar",
    "Kosan K Ciwaruga Jaya",
    "Kosan L Ciwaruga Wangi",
    "Kosan M Ciwaruga Asoka",
    "Kosan N Ciwaruga Harmoni",
    "Kosan O Ciwaruga Bahagia",
    "Kosan P Ciwaruga Ceria",
    "Kosan Q Ciwaruga Cermai",
    "Kosan R Ciwaruga Segar",
    "Kosan S Ciwaruga Sejahtera",
    "Kosan T Ciwaruga Sempurna"
]

ciwaruga.add_nodes_from(nodes_2)

edges_2 = [
    ("Polban", "Kosan A Ciwaruga Asri", 400),
    ("Polban", "Kosan B Ciwaruga Indah", 500),
    ("Polban", "Kosan C Ciwaruga Baru", 600),
    ("Kosan A Ciwaruga Asri", "Kosan B Ciwaruga Indah", 200),
    ("Kosan A Ciwaruga Asri", "Kosan C Ciwaruga Baru", 300),
    ("Kosan B Ciwaruga Indah", "Kosan D Ciwaruga Raya", 250),
    ("Kosan C Ciwaruga Baru", "Kosan E Ciwaruga Permai", 350),
    ("Kosan D Ciwaruga Raya", "Kosan F Ciwaruga Hijau", 200),
    ("Kosan E Ciwaruga Permai", "Kosan G Ciwaruga Sentosa", 250),
    ("Kosan F Ciwaruga Hijau", "Kosan H Ciwaruga Asih", 180),
    ("Kosan G Ciwaruga Sentosa", "Kosan I Ciwaruga Sari", 200),
    ("Kosan H Ciwaruga Asih", "Kosan J Ciwaruga Mekar", 150),
    ("Kosan I Ciwaruga Sari", "Kosan K Ciwaruga Jaya", 250),
    ("Kosan J Ciwaruga Mekar", "Kosan L Ciwaruga Wangi", 200),
    ("Kosan K Ciwaruga Jaya", "Kosan M Ciwaruga Asoka", 300),
    ("Kosan L Ciwaruga Wangi", "Kosan N Ciwaruga Harmoni", 220),
    ("Kosan M Ciwaruga Asoka", "Kosan O Ciwaruga Bahagia", 280),
    ("Kosan N Ciwaruga Harmoni", "Kosan P Ciwaruga Ceria", 200),
    ("Kosan O Ciwaruga Bahagia", "Kosan Q Ciwaruga Cermai", 250),
    ("Kosan P Ciwaruga Ceria", "Kosan R Ciwaruga Segar", 180),
    ("Kosan Q Ciwaruga Cermai", "Kosan S Ciwaruga Sejahtera", 200),
    ("Kosan R Ciwaruga Segar", "Kosan T Ciwaruga Sempurna", 250),
    ("Polban", "Kosan E Ciwaruga Permai", 550),
    ("Kosan C Ciwaruga Baru", "Kosan H Ciwaruga Asih", 400),
    ("Kosan F Ciwaruga Hijau", "Kosan K Ciwaruga Jaya", 300),
    ("Kosan I Ciwaruga Sari", "Kosan N Ciwaruga Harmoni", 350),
    ("Kosan L Ciwaruga Wangi", "Kosan Q Ciwaruga Cermai", 300),
    ("Kosan O Ciwaruga Bahagia", "Kosan T Ciwaruga Sempurna", 400)
]

ciwaruga.add_weighted_edges_from(edges_2)

# Tambahkan node (string)
nodes_3 = [
    "Polban",
    "Kosan A Gegerkalong Asri",
    "Kosan B Gegerkalong Indah",
    "Kosan C Gegerkalong Baru",
    "Kosan D Gegerkalong Raya",
    "Kosan E Gegerkalong Permai",
    "Kosan F Gegerkalong Hijau",
    "Kosan G Gegerkalong Sentosa",
    "Kosan H Gegerkalong Asih",
    "Kosan I Gegerkalong Sari",
    "Kosan J Gegerkalong Mekar",
    "Kosan K Gegerkalong Jaya",
    "Kosan L Gegerkalong Wangi",
    "Kosan M Gegerkalong Asoka",
    "Kosan N Gegerkalong Harmoni",
    "Kosan O Gegerkalong Bahagia",
    "Kosan P Gegerkalong Ceria",
    "Kosan Q Gegerkalong Cermai",
    "Kosan R Gegerkalong Segar",
    "Kosan S Gegerkalong Sejahtera",
    "Kosan T Gegerkalong Sempurna"
]

gegerkalong.add_nodes_from(nodes_3)

# Tambahkan edge
edges_3 = [
    ("Polban", "Kosan A Gegerkalong Asri", 450),
    ("Polban", "Kosan B Gegerkalong Indah", 550),
    ("Polban", "Kosan C Gegerkalong Baru", 650),
    ("Kosan A Gegerkalong Asri", "Kosan B Gegerkalong Indah", 200),
    ("Kosan A Gegerkalong Asri", "Kosan C Gegerkalong Baru", 300),
    ("Kosan B Gegerkalong Indah", "Kosan D Gegerkalong Raya", 250),
    ("Kosan C Gegerkalong Baru", "Kosan E Gegerkalong Permai", 350),
    ("Kosan D Gegerkalong Raya", "Kosan F Gegerkalong Hijau", 200),
    ("Kosan E Gegerkalong Permai", "Kosan G Gegerkalong Sentosa", 250),
    ("Kosan F Gegerkalong Hijau", "Kosan H Gegerkalong Asih", 180),
    ("Kosan G Gegerkalong Sentosa", "Kosan I Gegerkalong Sari", 200),
    ("Kosan H Gegerkalong Asih", "Kosan J Gegerkalong Mekar", 150),
    ("Kosan I Gegerkalong Sari", "Kosan K Gegerkalong Jaya", 250),
    ("Kosan J Gegerkalong Mekar", "Kosan L Gegerkalong Wangi", 200),
    ("Kosan K Gegerkalong Jaya", "Kosan M Gegerkalong Asoka", 300),
    ("Kosan L Gegerkalong Wangi", "Kosan N Gegerkalong Harmoni", 220),
    ("Kosan M Gegerkalong Asoka", "Kosan O Gegerkalong Bahagia", 280),
    ("Kosan N Gegerkalong Harmoni", "Kosan P Gegerkalong Ceria", 200),
    ("Kosan O Gegerkalong Bahagia", "Kosan Q Gegerkalong Cermai", 250),
    ("Kosan P Gegerkalong Ceria", "Kosan R Gegerkalong Segar", 180),
    ("Kosan Q Gegerkalong Cermai", "Kosan S Gegerkalong Sejahtera", 200),
    ("Kosan R Gegerkalong Segar", "Kosan T Gegerkalong Sempurna", 250),
    ("Polban", "Kosan E Gegerkalong Permai", 600),
    ("Kosan C Gegerkalong Baru", "Kosan H Gegerkalong Asih", 400),
    ("Kosan F Gegerkalong Hijau", "Kosan K Gegerkalong Jaya", 300),
    ("Kosan I Gegerkalong Sari", "Kosan N Gegerkalong Harmoni", 350),
    ("Kosan L Gegerkalong Wangi", "Kosan Q Gegerkalong Cermai", 300),
    ("Kosan O Gegerkalong Bahagia", "Kosan T Gegerkalong Sempurna", 400)
]

gegerkalong.add_weighted_edges_from(edges_3)

savegraphdb(sarijadi, './sarijadi.json')
savegraphdb(ciwaruga, './ciwaruga.json')
savegraphdb(gegerkalong, './gegerkalong.json')