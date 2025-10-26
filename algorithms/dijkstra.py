import networkx as nx

def dijkstra_shortest_path(G, source, target):
    try:
        path = nx.dijkstra_path(G, source, target, weight='length')
        return path
    except nx.NetworkXNoPath:
        return None
