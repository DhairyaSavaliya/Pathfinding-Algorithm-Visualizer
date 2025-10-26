import osmnx as ox

def plot_graph_with_route(G, path, ax=None, label=None):
    ox.plot_graph_route(
        G, path,
        route_linewidth=3,
        node_size=0,
        bgcolor='white',
        ax=ax,
        route_color=None,
        orig_dest_node_color='red'
    )
