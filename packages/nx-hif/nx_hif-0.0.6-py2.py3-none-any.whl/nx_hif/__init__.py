import networkx as nx
import json

def write_hif(G, path):
    pass

def add_incidence(G: nx.Graph, incidence):
    attrs = incidence.get("attrs", {})
    edge_id = incidence["edge"], 1
    node_id = incidence["node"], 0
    if "weight" in incidence:
        attrs["weight"] = incidence["weight"]
    if "direction" in incidence:
        attrs["direction"] = incidence["direction"]
    G.add_node(edge_id, bipartite=1, edge=incidence["edge"])
    G.add_node(node_id, bipartite=0, node=incidence["node"])
    G.add_edge(edge_id, node_id, **attrs)

def add_edge(G: nx.Graph, edge):
    attrs = edge.get("attrs", {})
    edge_id = edge["edge"], 1
    if "weight" in edge:
        attrs["weight"] = edge["weight"]
    if not G.has_node(edge_id):
        G.add_node(edge_id, bipartite=1, edge=edge["edge"])
    for attr_key, attr_value in attrs.items():
        G.nodes[edge_id][attr_key] = attr_value

def add_node(G: nx.Graph, node):
    attrs = node.get("attrs", {})
    node_id = node["node"], 0
    if "weight" in node:
        attrs["weight"] = node["weight"]
    if not G.has_node(node_id):
        G.add_node(node_id, bipartite=0, node=node["node"])
    node_attrs = G.nodes[node_id]
    for attr_key, attr_value in attrs.items():
        node_attrs[attr_key] = attr_value

def read_hif(path):
    with open(path) as file:
        data = json.loads(file.read())
    return read_hif_data(data)

def read_hif_data(data):
    G_attrs = data.get("metadata", {})
    if "network-type" in data:
        G_attrs["network-type"] = data["network-type"]
    G = nx.Graph(**G_attrs)
    for i in data["incidences"]:
        add_incidence(G, i)
    for e in data["edges"]:
        add_edge(G, e)
    for n in data["nodes"]:
        add_node(G, n)
    return G
