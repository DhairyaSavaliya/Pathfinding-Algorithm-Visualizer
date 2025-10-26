import networkx as nx

def astar_shortest_path(G, source, target):
    try:
        path = nx.astar_path(G, source, target, weight='length')
        return path
    except nx.NetworkXNoPath:
        return None
