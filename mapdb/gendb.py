import networkx as nx
import networkx.readwrite as json_graph
import json
import pandas as pd

def savegraphdb(graph, filepath):
    mapdb = json_graph.node_link_data(graph, edges="edges")
    with open(filepath, 'w') as f:
        json.dump(mapdb, f, indent=4)

def load_kosan_data(csv_path):
    """Load kosan data from CSV and create mapping for price and gender"""
    try:
        df = pd.read_csv(csv_path)
        print(f"Successfully loaded CSV with {len(df)} rows")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return {}
    
    kosan_data = {}
    
    for _, row in df.iterrows():
        try:
            kosan_name = str(row['Kost Name (as listed)']).strip()
            gender = str(row['Gender']).strip()
            original_price = row['Original Price (Rp)']
            discounted_price = row['Discounted Price (Rp)']
            
            # Use discounted price if available, otherwise use original price
            price = None
            if pd.notna(discounted_price) and str(discounted_price).strip() not in ['—', '', 'nan']:
                price = discounted_price
            elif pd.notna(original_price) and str(original_price).strip() not in ['—', '', 'nan']:
                price = original_price
            
            # Clean price string and convert to integer
            if price is not None:
                # Handle different price formats
                price_str = str(price).strip()
                # Remove dots (thousand separators) and commas
                price_str = price_str.replace('.', '').replace(',', '')
                
                try:
                    price_int = int(price_str)
                    kosan_data[kosan_name] = {
                        'price': price_int,
                        'gender': gender
                    }
                except ValueError as e:
                    print(f"Warning: Could not parse price for {kosan_name}: {price_str} - {e}")
                    # Still add the entry with price 0
                    kosan_data[kosan_name] = {
                        'price': 0,
                        'gender': gender
                    }
            else:
                # No valid price data, add with default values
                kosan_data[kosan_name] = {
                    'price': 0,
                    'gender': gender
                }
                
        except Exception as e:
            print(f"Error processing row: {e}")
            continue
    
    print(f"Successfully processed {len(kosan_data)} kosan entries")
    return kosan_data

def get_kosan_attributes(kosan_name, kosan_data):
    """Get price and gender attributes for a kosan node"""
    # Try exact match first
    if kosan_name in kosan_data:
        return kosan_data[kosan_name]
    
    # Try partial matching for cases where names might not match exactly
    kosan_lower = kosan_name.lower()
    for data_name, data in kosan_data.items():
        data_lower = data_name.lower()
        
        # Check if one contains the other (with some tolerance)
        if (kosan_lower in data_lower or data_lower in kosan_lower or
            any(word in data_lower for word in kosan_lower.split() if len(word) > 3)):
            return data
    
    # Try matching by removing common prefixes/suffixes
    kosan_clean = kosan_name.replace('Kosan ', '').replace('Kost ', '').lower()
    for data_name, data in kosan_data.items():
        data_clean = data_name.replace('Kosan ', '').replace('Kost ', '').lower()
        if kosan_clean in data_clean or data_clean in kosan_clean:
            return data
    
    # Default values if no match found
    return {'price': 0, 'gender': 'Unknown'}

# Load kosan data from CSV
print("Loading kosan data from CSV...")
kosan_data = load_kosan_data("datakosan.csv")

if not kosan_data:
    print("Warning: No kosan data loaded. Nodes will have default attributes.")
    kosan_data = {}

sarijadi = nx.Graph()
ciwaruga = nx.Graph()
gegerkalong = nx.Graph()

# Cluster Sarijadi - Reduced to ~30 nodes for better comprehension
sarijadi_nodes = [
    "Polban",
    # Main cluster near Polban
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
    # Secondary cluster
    "Kosan Summer House",
    "Kosan Rizka I",
    "Kosan Ana",
    "Kosan Orange",
    "Kosan Bu Neneng",
    "Kosan Beat",
    "Kosan Jimin",
    "Kosan DaKost Single",
    # Tertiary cluster
    "Kosan Sarimah",
    "Kosan Sari Asih",
    "Kosan Leskos",
    "Kosan Pondok Lathifah",
    "Kosan Elite Ddr 203",
    "Kosan Sri Yuningsih",
    "Kosan Peach Home"
]

sarijadi_edges = [
    # Direct connections from Polban to main cluster
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

    # Main cluster connections (core Sarijadi area)
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

    # Secondary cluster connections
    ("Kosan Summer House", "Kosan Sarijadi", 140),
    ("Kosan Rizka I", "Kosan Sarijadi Raya", 110),
    ("Kosan Ana", "Kosan Bu Nita Sarijadi", 90),
    ("Kosan Orange", "Kosan Erka Sarijadi", 100),
    ("Kosan Bu Neneng", "Kosan Sarijadi", 160),
    ("Kosan Beat", "Kosan Maranatha", 90),
    ("Kosan Jimin", "Kosan Sarijadi Ummu Asfar", 100),
    ("Kosan DaKost Single", "Kosan Sarijadi", 120),

    # Tertiary cluster connections
    ("Kosan Sarimah", "Kosan Sari Asih", 90),
    ("Kosan Sari Asih", "Kosan Sarijadi", 150),
    ("Kosan Leskos", "Kosan Sarijadi Raya", 120),
    ("Kosan Pondok Lathifah", "Kosan Bu Nita Sarijadi", 110),
    ("Kosan Elite Ddr 203", "Kosan Frank House", 120),
    ("Kosan Sri Yuningsih", "Kosan Admasetiabudhi Garden View", 100),
    ("Kosan Peach Home", "Kosan Sarijadi Ummu Asfar", 90),
    
    # Additional connections to improve peripheral node connectivity
    ("Kosan Sarimah", "Kosan Summer House", 130),
    ("Kosan Sari Asih", "Kosan Rizka I", 140),
    ("Kosan Leskos", "Kosan Ana", 110),
    ("Kosan Pondok Lathifah", "Kosan Orange", 120),
    ("Kosan Elite Ddr 203", "Kosan Bu Neneng", 100),
    ("Kosan Sri Yuningsih", "Kosan Beat", 90),
    ("Kosan Peach Home", "Kosan Jimin", 80),
    
    # Cross-connections between peripheral nodes
    ("Kosan Sarimah", "Kosan Leskos", 160),
    ("Kosan Sari Asih", "Kosan Pondok Lathifah", 140),
    ("Kosan Elite Ddr 203", "Kosan Sri Yuningsih", 150),
    ("Kosan Peach Home", "Kosan DaKost Single", 120),
    
    # Additional connections to main cluster
    ("Kosan Sarimah", "Kosan Sarijadi Raya", 180),
    ("Kosan Leskos", "Kosan Bu Nita Sarijadi", 130),
    ("Kosan Pondok Lathifah", "Kosan Erka Sarijadi", 140),
    ("Kosan Elite Ddr 203", "Kosan Admasetiabudhi Garden View", 110),
    ("Kosan Sri Yuningsih", "Kosan Frank House", 90),
    ("Kosan Peach Home", "Kosan 75 Sarijadi", 100)
]

# Cluster Gegerkalong - Reduced for consistency
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

# Cluster Ciwaruga (Cibogo + Cihanjuang) - Reduced for consistency
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

# Add attributes to Sarijadi nodes
for node in sarijadi_nodes:
    if node == "Polban":
        sarijadi.nodes[node]['price'] = 0
        sarijadi.nodes[node]['gender'] = 'N/A'
    else:
        attrs = get_kosan_attributes(node, kosan_data)
        sarijadi.nodes[node]['price'] = attrs['price']
        sarijadi.nodes[node]['gender'] = attrs['gender']

# Gegerkalong Graph
gegerkalong.add_nodes_from(gegerkalong_nodes)
gegerkalong.add_weighted_edges_from(gegerkalong_edges)

# Add attributes to Gegerkalong nodes
for node in gegerkalong_nodes:
    if node == "Polban":
        gegerkalong.nodes[node]['price'] = 0
        gegerkalong.nodes[node]['gender'] = 'N/A'
    else:
        attrs = get_kosan_attributes(node, kosan_data)
        gegerkalong.nodes[node]['price'] = attrs['price']
        gegerkalong.nodes[node]['gender'] = attrs['gender']

# Ciwaruga Graph
ciwaruga.add_nodes_from(ciwaruga_nodes)
ciwaruga.add_weighted_edges_from(ciwaruga_edges)

# Add attributes to Ciwaruga nodes
for node in ciwaruga_nodes:
    if node == "Polban":
        ciwaruga.nodes[node]['price'] = 0
        ciwaruga.nodes[node]['gender'] = 'N/A'
    else:
        attrs = get_kosan_attributes(node, kosan_data)
        ciwaruga.nodes[node]['price'] = attrs['price']
        ciwaruga.nodes[node]['gender'] = attrs['gender']

# Save graphs to JSON files
savegraphdb(sarijadi, "sarijadi.json")
savegraphdb(gegerkalong, "gegerkalong.json")
savegraphdb(ciwaruga, "ciwaruga.json")

print("Graph databases created successfully!")
print(f"Sarijadi cluster: {sarijadi.number_of_nodes()} nodes, {sarijadi.number_of_edges()} edges")
print(f"Gegerkalong cluster: {gegerkalong.number_of_nodes()} nodes, {gegerkalong.number_of_edges()} edges")
print(f"Ciwaruga cluster: {ciwaruga.number_of_nodes()} nodes, {ciwaruga.number_of_edges()} edges")

# Print sample nodes with attributes
print("\nSample Sarijadi nodes with attributes:")
for i, node in enumerate(list(sarijadi.nodes())[:5]):
    attrs = sarijadi.nodes[node]
    print(f"  {node}: price={attrs.get('price', 'N/A')}, gender={attrs.get('gender', 'N/A')}")

print("\nSample Gegerkalong nodes with attributes:")
for i, node in enumerate(list(gegerkalong.nodes())[:5]):
    attrs = gegerkalong.nodes[node]
    print(f"  {node}: price={attrs.get('price', 'N/A')}, gender={attrs.get('gender', 'N/A')}")

print("\nSample Ciwaruga nodes with attributes:")
for i, node in enumerate(list(ciwaruga.nodes())[:5]):
    attrs = ciwaruga.nodes[node]
    print(f"  {node}: price={attrs.get('price', 'N/A')}, gender={attrs.get('gender', 'N/A')}")