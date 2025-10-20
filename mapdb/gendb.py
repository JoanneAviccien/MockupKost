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

# Cluster Sarijadi
sarijadi_nodes = [
    "Polban",
    "Kosan Dy Culture Maranatha",
    "Kosan Maranatha",
    "Kosan The Setraria One Maranatha",
    "Kosan Grhya Sahitya Sarijadi",
    "Kosan Sarijadi Raya",
    "Kosan Sarijadi",
    "Kosan Bu Nita Sarijadi",
    "Kosan Erka Sarijadi",
    "Kosan Bapak Yusup Sarijadi",
    "Kosan 75 Sarijadi",
    "Kosan Sarijadi Ummu Asfar",
    "Kosan Sarijadi Cijerokaso",
    "Kosan Pariwisata 15",
    "Kosan Parwis 22",
    "Kosan Frank House",
    "Kosan Admasetiabudhi Garden View",
    "Kosan Summer House",
    "Kosan Rizka I",
    "Kosan Ana",
    "Kosan Budi Indah 3",
    "Kosan Orange",
    "Kosan Zidni",
    "Kosan Sarimadu Barat",
    "Kosan Bu Neneng",
    "Kosan Bu Hj Neneng",
    "Kosan Beat",
    "Kosan Bsp",
    "Kosan Jimin",
    "Kosan DaKost Single",
    "Kosan Sarimah",
    "Kosan Bu Sumi",
    "Kosan Umi",
    "Kosan Sari Asih",
    "Kosan Green Home Sari Asih",
    "Kosan Leskos",
    "Kosan A Fadhil",
    "Kosan Nyaman Murah",
    "Kosan Pondok Lathifah",
    "Kosan Djapa",
    "Kosan Aamir",
    "Kosan Pondok Arjuna",
    "Kosan Pondok Hijau",
    "Kosan Elite Ddr 203",
    "Kosan Willy",
    "Kosan Sri Yuningsih",
    "Kosan Graha 171",
    "Kosan Peach Home",
    "Kosan Amma 2",
    "Kosan Karizma Guesthouse",
    "Kosan Wisma Komando2",
    "Kosan Icarus 1",
    "Kosan Rumah De Ajeng",
    "Kosan Fortuna Residence",
    "Kosan Bu Moen",
    "Kosan Casa De Lemon",
    "Kosan Yugi Home 42",
    "Kosan Ami",
    "Kosan Pink",
    "Kosan Gentra",
    "Kosan Mitha",
    "Kosan ApiQ",
    "Kosan DI 3/25",
    "Kosan An",
    "Kosan Om Fari",
    "Kosan Ibu Fitri",
    "Kosan Paviliun Pondok Barokah",
    "Kosan Sri M",
    "Kosan Yana",
    "Kosan Bidan Merry",
    "Kosan Niji House",
    "Kosan Indilar",
    "Kosan Almeera",
    "Kosan Tulip 2",
    "Kosan Permai",
    "Kosan Ibu Nina",
    "Kosan Oma Nuy"
]

sarijadi_edges = [
    # Polban ke kosan Sarijadi
    ("Polban", "Kosan Dy Culture Maranatha", 350),
    ("Polban", "Kosan Maranatha", 370),
    ("Polban", "Kosan The Setraria One Maranatha", 380),
    ("Polban", "Kosan Grhya Sahitya Sarijadi", 420),
    ("Polban", "Kosan Sarijadi Raya", 450),
    ("Polban", "Kosan Sarijadi", 460),
    ("Polban", "Kosan Bu Nita Sarijadi", 480),
    ("Polban", "Kosan Erka Sarijadi", 500),
    ("Polban", "Kosan Bapak Yusup Sarijadi", 520),
    ("Polban", "Kosan 75 Sarijadi", 530),
    ("Polban", "Kosan Sarijadi Ummu Asfar", 550),
    ("Polban", "Kosan Sarijadi Cijerokaso", 580),
    ("Polban", "Kosan Pariwisata 15", 600),
    ("Polban", "Kosan Parwis 22", 610),
    ("Polban", "Kosan Frank House", 630),
    ("Polban", "Kosan Admasetiabudhi Garden View", 650),

    # Cluster Sarijadi (antar kosan berdekatan)
    ("Kosan Sarijadi", "Kosan Sarijadi Raya", 120),
    ("Kosan Sarijadi", "Kosan Bu Nita Sarijadi", 100),
    ("Kosan Sarijadi Raya", "Kosan Erka Sarijadi", 90),
    ("Kosan Bu Nita Sarijadi", "Kosan Bapak Yusup Sarijadi", 130),
    ("Kosan 75 Sarijadi", "Kosan Sarijadi Ummu Asfar", 80),
    ("Kosan Sarijadi Cijerokaso", "Kosan Grhya Sahitya Sarijadi", 150),
    ("Kosan Grhya Sahitya Sarijadi", "Kosan Dy Culture Maranatha", 200),
    ("Kosan Maranatha", "Kosan The Setraria One Maranatha", 70),
    ("Kosan Pariwisata 15", "Kosan Parwis 22", 60),
    ("Kosan Frank House", "Kosan Admasetiabudhi Garden View", 100),

    # Kosan umum Sarijadi (terhubung ke cluster Sarijadi)
    ("Kosan Summer House", "Kosan Sarijadi", 140),
    ("Kosan Rizka I", "Kosan Sarijadi Raya", 110),
    ("Kosan Ana", "Kosan Bu Nita Sarijadi", 90),
    ("Kosan Budi Indah 3", "Kosan 75 Sarijadi", 130),
    ("Kosan Orange", "Kosan Erka Sarijadi", 100),
    ("Kosan Zidni", "Kosan Pariwisata 15", 120),
    ("Kosan Sarimadu Barat", "Kosan Parwis 22", 100),
    ("Kosan Bu Neneng", "Kosan Bu Hj Neneng", 80),
    ("Kosan Bu Hj Neneng", "Kosan Sarijadi", 160),
    ("Kosan Beat", "Kosan Maranatha", 90),
    ("Kosan Bsp", "Kosan Admasetiabudhi Garden View", 140),
    ("Kosan Jimin", "Kosan Sarijadi Ummu Asfar", 100),
    ("Kosan DaKost Single", "Kosan Sarijadi", 120),
    
    # Connect isolated chains to main network
    ("Kosan Sarimah", "Kosan Bu Sumi", 90),
    ("Kosan Bu Sumi", "Kosan Umi", 80),
    ("Kosan Umi", "Kosan Sari Asih", 100),
    ("Kosan Sari Asih", "Kosan Green Home Sari Asih", 70),
    ("Kosan Green Home Sari Asih", "Kosan Sarijadi", 150),  # Connect to main network
    
    ("Kosan Leskos", "Kosan A Fadhil", 60),
    ("Kosan A Fadhil", "Kosan Nyaman Murah", 90),
    ("Kosan Nyaman Murah", "Kosan Sarijadi Raya", 120),  # Connect to main network
    
    ("Kosan Pondok Lathifah", "Kosan Djapa", 100),
    ("Kosan Djapa", "Kosan Bu Nita Sarijadi", 110),  # Connect to main network
    
    ("Kosan Aamir", "Kosan Pondok Arjuna", 80),
    ("Kosan Pondok Arjuna", "Kosan Pondok Hijau", 70),
    ("Kosan Pondok Hijau", "Kosan 75 Sarijadi", 100),  # Connect to main network
    
    ("Kosan Elite Ddr 203", "Kosan Willy", 90),
    ("Kosan Willy", "Kosan Frank House", 120),  # Connect to main network
    
    ("Kosan Sri Yuningsih", "Kosan Graha 171", 110),
    ("Kosan Graha 171", "Kosan Admasetiabudhi Garden View", 100),  # Connect to main network
    
    ("Kosan Peach Home", "Kosan Amma 2", 80),
    ("Kosan Amma 2", "Kosan Sarijadi Ummu Asfar", 90),  # Connect to main network
    
    ("Kosan Karizma Guesthouse", "Kosan Wisma Komando2", 100),
    ("Kosan Wisma Komando2", "Kosan Parwis 22", 120),  # Connect to main network
    
    ("Kosan Icarus 1", "Kosan Rumah De Ajeng", 90),
    ("Kosan Rumah De Ajeng", "Kosan Pariwisata 15", 100),  # Connect to main network
    
    ("Kosan Fortuna Residence", "Kosan 75 Sarijadi", 140),
    ("Kosan Bu Moen", "Kosan Casa De Lemon", 85),
    ("Kosan Casa De Lemon", "Kosan Sarijadi", 120),  # Connect to main network
    
    ("Kosan Yugi Home 42", "Kosan Ami", 70),
    ("Kosan Ami", "Kosan Sarijadi Raya", 100),  # Connect to main network
    
    ("Kosan Pink", "Kosan Gentra", 60),
    ("Kosan Gentra", "Kosan Erka Sarijadi", 90),  # Connect to main network
    
    ("Kosan Mitha", "Kosan ApiQ", 90),
    ("Kosan ApiQ", "Kosan Bapak Yusup Sarijadi", 100),  # Connect to main network
    
    ("Kosan DI 3/25", "Kosan An", 70),
    ("Kosan An", "Kosan Sarijadi Cijerokaso", 80),  # Connect to main network
    
    ("Kosan Om Fari", "Kosan Ibu Fitri", 80),
    ("Kosan Ibu Fitri", "Kosan Grhya Sahitya Sarijadi", 100),  # Connect to main network
    
    ("Kosan Paviliun Pondok Barokah", "Kosan Sri M", 100),
    ("Kosan Sri M", "Kosan Dy Culture Maranatha", 120),  # Connect to main network
    
    ("Kosan Yana", "Kosan Bidan Merry", 90),
    ("Kosan Bidan Merry", "Kosan The Setraria One Maranatha", 100),  # Connect to main network
    
    ("Kosan Niji House", "Kosan Indilar", 80),
    ("Kosan Indilar", "Kosan Maranatha", 90),  # Connect to main network
    
    ("Kosan Almeera", "Kosan Tulip 2", 70),
    ("Kosan Tulip 2", "Kosan Sarijadi Ummu Asfar", 80),  # Connect to main network
    
    ("Kosan Permai", "Kosan Ibu Nina", 80),
    ("Kosan Ibu Nina", "Kosan Oma Nuy", 70),
    ("Kosan Oma Nuy", "Kosan 75 Sarijadi", 90)  # Connect to main network
]

# Cluster Gegerkalong
gegerkalong_nodes = [
    "Polban",
    "Kosan Gegerkalong Hilir",
    "Kosan Adem Gegerkalong",
    "Kosan Geger Kalong Hilir Belakang",
    "Kosan Verta Living",
    "Kosan Westlondoncoliving",
    "Kosan DHomey 1",
    "Kosan TCA Tujuh",
    "Kosan E House",
    "Kosan Blue Sky",
    "Kosan G",
    "Kosan Rennicks"
]

gegerkalong_edges = [
    # Polban ke kosan Gegerkalong
    ("Polban", "Kosan Gegerkalong Hilir", 700),
    ("Polban", "Kosan Adem Gegerkalong", 720),
    ("Polban", "Kosan Geger Kalong Hilir Belakang", 750),

    # Cluster Gegerkalong (antar kosan berdekatan)
    ("Kosan Gegerkalong Hilir", "Kosan Adem Gegerkalong", 90),
    ("Kosan Adem Gegerkalong", "Kosan Geger Kalong Hilir Belakang", 110),
    ("Kosan Gegerkalong Hilir", "Kosan Verta Living", 180),
    ("Kosan Verta Living", "Kosan Westlondoncoliving", 150),

    # Kosan umum Gegerkalong (terhubung ke cluster Gegerkalong)
    ("Kosan DHomey 1", "Kosan Gegerkalong Hilir", 140),
    ("Kosan TCA Tujuh", "Kosan Adem Gegerkalong", 130),
    ("Kosan E House", "Kosan Westlondoncoliving", 120),
    ("Kosan Blue Sky", "Kosan Verta Living", 100),
    ("Kosan G", "Kosan Gegerkalong Hilir", 110),
    ("Kosan Rennicks", "Kosan Gegerkalong Hilir", 190)
]

# Cluster Ciwaruga (Cibogo + Cihanjuang)
ciwaruga_nodes = [
    "Polban",
    "Kosan Cibogo SM91",
    "Kosan Cibogo Atas",
    "Kosan Vika Cibogo Pperintis Sarijadi",
    "Kosan Na Jeges 98 Babakan",
    "Kosan Chelsea Home",
    "Kosan My Home",
    "Kosan Ikhwan",
    "Kosan Sariwangi Cihanjuang",
    "Kosan Cihanjuang",
    "Kosan Sariwangi Indah",
    "Kosan Nyonya Residence",
    "Kosan Aibay",
    "Kosan Mutiara"
]

ciwaruga_edges = [
    # Polban ke kosan Ciwaruga (Cibogo)
    ("Polban", "Kosan Cibogo SM91", 800),
    ("Polban", "Kosan Cibogo Atas", 820),
    ("Polban", "Kosan Vika Cibogo Pperintis Sarijadi", 850),

    # Polban ke kosan Ciwaruga (Cihanjuang)
    ("Polban", "Kosan Sariwangi Cihanjuang", 1200),
    ("Polban", "Kosan Cihanjuang", 1250),
    ("Polban", "Kosan Sariwangi Indah", 1300),

    # Cluster Cibogo (antar kosan berdekatan)
    ("Kosan Cibogo SM91", "Kosan Cibogo Atas", 100),
    ("Kosan Cibogo Atas", "Kosan Vika Cibogo Pperintis Sarijadi", 120),
    ("Kosan Vika Cibogo Pperintis Sarijadi", "Kosan Na Jeges 98 Babakan", 200),

    # Cluster Cihanjuang (antar kosan berdekatan)
    ("Kosan Sariwangi Cihanjuang", "Kosan Cihanjuang", 150),
    ("Kosan Cihanjuang", "Kosan Sariwangi Indah", 180),

    # Kosan umum Ciwaruga (terhubung ke cluster terdekat)
    ("Kosan Chelsea Home", "Kosan Cibogo SM91", 170),
    ("Kosan My Home", "Kosan Cibogo Atas", 150),
    ("Kosan Ikhwan", "Kosan Cibogo SM91", 180),
    ("Kosan Nyonya Residence", "Kosan Sariwangi Indah", 200),
    ("Kosan Aibay", "Kosan Cihanjuang", 160),
    ("Kosan Mutiara", "Kosan Sariwangi Cihanjuang", 130)
]

# Create graphs for each cluster
# Sarijadi Graph
sarijadi.add_nodes_from(sarijadi_nodes)
sarijadi.add_weighted_edges_from(sarijadi_edges)

# Gegerkalong Graph
gegerkalong.add_nodes_from(gegerkalong_nodes)
gegerkalong.add_weighted_edges_from(gegerkalong_edges)

# Ciwaruga Graph
ciwaruga.add_nodes_from(ciwaruga_nodes)
ciwaruga.add_weighted_edges_from(ciwaruga_edges)

# Save graphs to JSON files
savegraphdb(sarijadi, "sarijadi.json")
savegraphdb(gegerkalong, "gegerkalong.json")
savegraphdb(ciwaruga, "ciwaruga.json")

print("Graph databases created successfully!")
print(f"Sarijadi cluster: {sarijadi.number_of_nodes()} nodes, {sarijadi.number_of_edges()} edges")
print(f"Gegerkalong cluster: {gegerkalong.number_of_nodes()} nodes, {gegerkalong.number_of_edges()} edges")
print(f"Ciwaruga cluster: {ciwaruga.number_of_nodes()} nodes, {ciwaruga.number_of_edges()} edges")