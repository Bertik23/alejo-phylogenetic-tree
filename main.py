import networkx as nx
import matplotlib.pyplot as plt
import json
from pyvis.network import Network, Options
from random import choice

def rgb_to_hex(r, g, b, a=255):
    return "#" + "".join(hex(int(x * 255))[2:] for x in (r, g, b, a))

def getGenomeDistance(plant0, plant1):
    return max(
        abs(max(plant0["spawnEnergy"], plant1["spawnEnergy"]) / min(plant0["spawnEnergy"], plant1["spawnEnergy"])),
        abs(max(plant0["energyGain"], plant1["energyGain"]) / min(plant0["energyGain"], plant1["energyGain"])),
        abs(max(plant0["stemSpeed"], plant1["stemSpeed"]) / min(plant0["stemSpeed"], plant1["stemSpeed"])),
        abs(max(plant0["stemMaxSize"], plant1["stemMaxSize"]) / min(plant0["stemMaxSize"], plant1["stemMaxSize"])),
        abs(max(plant0["leafALength"], plant1["leafALength"]) / min(plant0["leafALength"], plant1["leafALength"])),
        abs(max(plant0["leafAWidth"], plant1["leafAWidth"]) / min(plant0["leafAWidth"], plant1["leafAWidth"])),
        abs(max(plant0["leafAHeightf"], plant1["leafAHeightf"]) / min(plant0["leafAHeightf"], plant1["leafAHeightf"])),
        abs(max(plant0["leafAGrowthSpeed"], plant1["leafAGrowthSpeed"]) / min(plant0["leafAGrowthSpeed"], plant1["leafAGrowthSpeed"])),
        abs(max(plant0["leafAOrientation"], plant1["leafAOrientation"]) / min(plant0["leafAOrientation"], plant1["leafAOrientation"])),
        abs(max(plant0["leafAInclination"], plant1["leafAInclination"]) / min(plant0["leafAInclination"], plant1["leafAInclination"])),
        abs(max(plant0["leafBLength"], plant1["leafBLength"]) / min(plant0["leafBLength"], plant1["leafBLength"])),
        abs(max(plant0["leafBWidth"], plant1["leafBWidth"]) / min(plant0["leafBWidth"], plant1["leafBWidth"])),
        abs(max(plant0["leafBHeight"], plant1["leafBHeight"]) / min(plant0["leafBHeight"], plant1["leafBHeight"])),
        abs(max(plant0["leafBGrowthSpeed"], plant1["leafBGrowthSpeed"]) / min(plant0["leafBGrowthSpeed"], plant1["leafBGrowthSpeed"])),
        abs(max(plant0["leafBOrientation"], plant1["leafBOrientation"]) / min(plant0["leafBOrientation"], plant1["leafBOrientation"])),
        abs(max(plant0["leafBInclination"], plant1["leafBInclination"]) / min(plant0["leafBInclination"], plant1["leafBInclination"])),
        abs(max(plant0["flowerColor"]["r"], plant1["flowerColor"]["r"]) / min(plant0["flowerColor"]["r"], plant1["flowerColor"]["r"])),
        abs(max(plant0["flowerColor"]["g"], plant1["flowerColor"]["g"]) / min(plant0["flowerColor"]["g"], plant1["flowerColor"]["g"])),
        abs(max(plant0["flowerColor"]["b"], plant1["flowerColor"]["b"]) / min(plant0["flowerColor"]["b"], plant1["flowerColor"]["b"])),
        abs(max(plant0["flowerColor"]["a"], plant1["flowerColor"]["a"]) / min(plant0["flowerColor"]["a"], plant1["flowerColor"]["a"]))
    )

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

def pyvisWay(genomeDistance=1):
    net = Network(width="100%", height="100%", bgcolor="#222222", font_color="#FAFAFA")
    edges = []
    modifiedData = {r["plantID"]: r for r in data["plants"]}
    roots = []
    groups = []
    for key, r in modifiedData.items():
        net.add_node(
            key,
            label=r["userLabel"] if r["userLabel"] != "" else " ",
            # color=rgb_to_hex(*r["flowerColor"].values()),
            value=r["deathTime"]-r["spawnTime"],
            group=""
        )
        if key != r["parentID"]:
            edges.append((r["plantID"], r["parentID"]))
        else:
            modifiedData[key]["group"] = key
            roots.append(key)

    for q in roots:
        if getGenomeDistance(modifiedData[q], modifiedData[modifiedData[modifiedData[q]["parentID"]]["group"]]) > genomeDistance:
            modifiedData[q]["group"] = q
            groups.append(q)
        else:
            modifiedData[q]["group"] = modifiedData[modifiedData[q]["parentID"]]["group"]
        roots.extend(modifiedData[q]["offspring"])

    for node in net.nodes:
        node["group"] = modifiedData[node["id"]]["group"]

    net.add_edges(edges)
    # net.show_buttons()
    print(groups)
    net.set_options(json.dumps({"groups":{x: {"color": {"background": "#"+''.join([choice('0123456789ABCDEF') for _ in range(6)])}} for x in groups}}))
    net.show("visualisation.html")

if __name__ == '__main__':
    pyvisWay(3)