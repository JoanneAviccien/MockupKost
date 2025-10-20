import networkx as nx
import networkx.readwrite as json_graph
import json

def test_graph_connectivity(graph, graph_name):
    """Test if all nodes in a graph are connected to Polban"""
    print(f"\n=== Testing {graph_name} ===")
    print(f"Nodes: {graph.number_of_nodes()}")
    print(f"Edges: {graph.number_of_edges()}")
    
    # Check if Polban exists
    if "Polban" not in graph.nodes():
        print("❌ ERROR: Polban not found in graph!")
        return False
    
    # Check connectivity from Polban to all other nodes
    disconnected_nodes = []
    for node in graph.nodes():
        if node != "Polban":
            try:
                # Check if there's a path from Polban to this node
                if not nx.has_path(graph, "Polban", node):
                    disconnected_nodes.append(node)
            except:
                disconnected_nodes.append(node)
    
    if disconnected_nodes:
        print(f"❌ Found {len(disconnected_nodes)} disconnected nodes:")
        for node in disconnected_nodes:
            print(f"   - {node}")
        return False
    else:
        print("✅ All nodes are connected to Polban!")
        return True

def load_graph_from_json(filepath):
    """Load graph from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return json_graph.node_link_graph(data)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

# Test all three graphs
print("Testing Graph Connectivity")
print("=" * 50)

# Test Sarijadi
sarijadi = load_graph_from_json("sarijadi.json")
if sarijadi:
    test_graph_connectivity(sarijadi, "Sarijadi")

# Test Gegerkalong  
gegerkalong = load_graph_from_json("gegerkalong.json")
if gegerkalong:
    test_graph_connectivity(gegerkalong, "Gegerkalong")

# Test Ciwaruga
ciwaruga = load_graph_from_json("ciwaruga.json")
if ciwaruga:
    test_graph_connectivity(ciwaruga, "Ciwaruga")

print("\n" + "=" * 50)
print("Connectivity test completed!")

