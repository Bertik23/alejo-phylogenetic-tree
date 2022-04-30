import networkx as nx
import matplotlib.pyplot as plt
import json
from pyvis.network import Network

with open("data.json", "r") as f:
    data = json.load(f)

# print(data)

def pltWay():
    g = nx.Graph()
    edges = []
    for r in data["plants"]:
        edges.append((r["plantID"], r["parentID"]))
    # print(edges)
    g.add_edges_from(edges)
    nx.draw_networkx(g, with_labels=False)
    plt.show()

def pyvisWay():
    net = Network()
    edges = []
    nodes = []
    for r in data["plants"]:
        nodes.append(r["plantID"])
        edges.append((r["plantID"], r["parentID"]))
    net.add_nodes(nodes)
    net.add_edges(edges)
    net.show("visualisation.html")

if __name__ == '__main__':
    pyvisWay()