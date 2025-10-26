import streamlit as st
import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import time

# =============================
# Streamlit Page Configuration
# =============================
st.set_page_config(page_title="Shortest Path Visualizer", page_icon="🧭", layout="wide")

st.title("🚗 Pathfinding Algorithm Visualizer")
st.write(
    """
    Compare classic pathfinding algorithms — **Dijkstra**, **A\***, **BFS**, and **Bellman-Ford** —  
    on real-world road networks using **OpenStreetMap** data.
    """
)

# =============================
# Helper Functions
# =============================

@st.cache_data(show_spinner=False)
def load_graph(place_name):
    """Download and cache the street network graph for the given place."""
    try:
        G = ox.graph_from_place(place_name, network_type="drive")
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        return G
    except Exception as e:
        st.error(f"❌ Could not load map for '{place_name}'. Error: {e}")
        return None


def get_location_suggestions(G, num_suggestions=20):
    """Extract street intersections as location suggestions."""
    suggestions = []
    nodes = list(G.nodes(data=True))
    
    # Sample nodes evenly distributed across the graph
    step = max(1, len(nodes) // num_suggestions)
    sampled_nodes = nodes[::step][:num_suggestions]
    
    for node_id, data in sampled_nodes:
        lat, lon = data['y'], data['x']
        # Try to get street name if available
        street_name = f"Node {node_id} ({lat:.4f}, {lon:.4f})"
        
        # Check if node has street information in connected edges
        if G.out_edges(node_id):
            edge_data = G.get_edge_data(node_id, list(G.successors(node_id))[0], 0)
            if 'name' in edge_data:
                name = edge_data['name']
                if isinstance(name, list):
                    name = name[0]
                street_name = f"{name} ({lat:.4f}, {lon:.4f})"
        
        suggestions.append({
            'display': street_name,
            'node_id': node_id,
            'lat': lat,
            'lon': lon
        })
    
    return suggestions


def plot_shortest_path(G, route, orig_node, dest_node, algo_name):
    """Plot the map with the shortest path using OSMnx."""
    fig, ax = ox.plot_graph_route(
        G,
        route,
        route_linewidth=4,
        node_size=0,
        bgcolor="white",
        show=False,
        close=False,
    )
    # Add start and end markers
    orig_data = G.nodes[orig_node]
    dest_data = G.nodes[dest_node]
    
    ax.scatter([orig_data['x']], [orig_data['y']], c="green", s=100, label="Start", zorder=5)
    ax.scatter([dest_data['x']], [dest_data['y']], c="red", s=100, label="Destination", zorder=5)
    ax.legend()
    st.pyplot(fig)
    st.info(f"🧩 Visualized using **{algo_name} Algorithm**")


def run_algorithm(G, start_node, end_node, algorithm):
    """Run the selected pathfinding algorithm."""
    start_time = time.time()

    if algorithm == "Dijkstra":
        path = nx.shortest_path(G, start_node, end_node, weight="length", method="dijkstra")
    elif algorithm == "A*":
        path = nx.astar_path(G, start_node, end_node, weight="length")
    elif algorithm == "BFS":
        # BFS finds unweighted shortest path (by number of edges)
        path = nx.shortest_path(G, start_node, end_node, weight=None)
    elif algorithm == "Bellman-Ford":
        path = nx.shortest_path(G, start_node, end_node, weight="length", method="bellman-ford")
    else:
        raise ValueError("Unknown algorithm selected")

    exec_time = time.time() - start_time
    
    # Calculate path length
    if algorithm == "BFS":
        # For BFS, still calculate actual distance even though algorithm doesn't use it
        path_length = sum(G[path[i]][path[i+1]][0].get('length', 0) for i in range(len(path)-1))
    else:
        path_length = nx.path_weight(G, path, weight="length")
    
    return path, path_length, exec_time


def compare_all_algorithms(G, start_node, end_node):
    """Run all algorithms and return comparison data."""
    algorithms = ["Dijkstra", "A*", "BFS", "Bellman-Ford"]
    results = []
    
    for algo in algorithms:
        try:
            path, dist, exec_time = run_algorithm(G, start_node, end_node, algo)
            results.append({
                'Algorithm': algo,
                'Distance (km)': dist / 1000,
                'Time (seconds)': exec_time,
                'Nodes': len(path),
                'Path': path
            })
        except Exception as e:
            st.warning(f"⚠️ {algo} failed: {e}")
    
    return results


def plot_comparison_chart(results_df):
    """Plot comparison charts for algorithms."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    
    # Color palette for 4 algorithms
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3']
    
    # Distance comparison
    axes[0].bar(results_df['Algorithm'], results_df['Distance (km)'], color=colors[:len(results_df)])
    axes[0].set_ylabel('Distance (km)')
    axes[0].set_title('Distance Comparison')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].tick_params(axis='x', rotation=45)
    
    # Time comparison
    axes[1].bar(results_df['Algorithm'], results_df['Time (seconds)'], color=colors[:len(results_df)])
    axes[1].set_ylabel('Time (seconds)')
    axes[1].set_title('Execution Time Comparison')
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    st.pyplot(fig)


# =============================
# Input Section
# =============================
place_name = st.text_input("🏙️ Enter a city or area name:", "San Francisco, California, USA")

if st.button("Load Map"):
    with st.spinner("Downloading road network..."):
        G = load_graph(place_name)
        if G:
            st.session_state["G"] = G
            # Generate location suggestions
            with st.spinner("Generating location suggestions..."):
                suggestions = get_location_suggestions(G)
                st.session_state["suggestions"] = suggestions
            st.success(f"✅ Successfully loaded map of {place_name} with {len(suggestions)} location suggestions!")
        else:
            st.stop()

# Proceed only if map is loaded
if "G" in st.session_state:
    G = st.session_state["G"]
    suggestions = st.session_state.get("suggestions", [])

    st.subheader("📍 Choose Start & Destination")
    
    # Mode selection
    input_mode = st.radio("Select input mode:", ["Use Dropdown (Suggested Locations)", "Enter Custom Location"])
    
    if input_mode == "Use Dropdown (Suggested Locations)":
        if suggestions:
            # Create display options
            location_options = [s['display'] for s in suggestions]
            
            col1, col2 = st.columns(2)
            with col1:
                start_idx = st.selectbox("🟢 Start Location", range(len(location_options)), 
                                        format_func=lambda x: location_options[x])
                start_node = suggestions[start_idx]['node_id']
            
            with col2:
                end_idx = st.selectbox("🔴 Destination Location", range(len(location_options)), 
                                      format_func=lambda x: location_options[x],
                                      index=min(5, len(location_options)-1))
                end_node = suggestions[end_idx]['node_id']
        else:
            st.warning("⚠️ No suggestions available. Please reload the map.")
            st.stop()
    else:
        # Custom location input
        col1, col2 = st.columns(2)
        with col1:
            start_location = st.text_input("Enter Start Location", "Golden Gate Bridge, San Francisco")
        with col2:
            end_location = st.text_input("Enter Destination Location", "Union Square, San Francisco")

    # Algorithm selection
    st.subheader("🧮 Algorithm Selection")
    mode = st.radio("Choose mode:", ["Single Algorithm", "Compare All Algorithms"])
    
    if mode == "Single Algorithm":
        algo = st.selectbox("Select Algorithm", ["Dijkstra", "A*", "BFS", "Bellman-Ford"])

    if st.button("🚀 Find Path" if mode == "Single Algorithm" else "🚀 Compare All Algorithms", type="primary"):
        try:
            # Get nodes based on input mode
            if input_mode == "Enter Custom Location":
                with st.spinner("Geocoding locations..."):
                    orig_point = ox.geocode(start_location)
                    dest_point = ox.geocode(end_location)
                    start_node = ox.distance.nearest_nodes(G, orig_point[1], orig_point[0])
                    end_node = ox.distance.nearest_nodes(G, dest_point[1], dest_point[0])
            
            if mode == "Single Algorithm":
                # Single algorithm execution
                with st.spinner(f"Computing shortest path using {algo}..."):
                    path, dist, exec_time = run_algorithm(G, start_node, end_node, algo)

                    st.success(f"✅ Path found using {algo}!")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📏 Distance", f"{dist/1000:.2f} km")
                    with col2:
                        st.metric("⏱️ Time Taken", f"{exec_time:.4f} sec")
                    with col3:
                        st.metric("🧩 Nodes Visited", len(path))

                    # Plot result
                    plot_shortest_path(G, path, start_node, end_node, algo)
            
            else:
                # Compare all algorithms
                with st.spinner("Running all algorithms..."):
                    results = compare_all_algorithms(G, start_node, end_node)
                    
                    if results:
                        st.success("✅ All algorithms completed!")
                        
                        # Create DataFrame for display
                        df = pd.DataFrame(results)
                        display_df = df[['Algorithm', 'Distance (km)', 'Time (seconds)', 'Nodes']].copy()
                        
                        # Display results table
                        st.subheader("📊 Comparison Results")
                        st.dataframe(display_df.style.highlight_min(subset=['Distance (km)', 'Time (seconds)'], 
                                                                     color='lightgreen'), use_container_width=True)
                        
                        # Plot comparison charts
                        st.subheader("📈 Visual Comparison")
                        plot_comparison_chart(display_df)
                        
                        # Show best algorithm
                        fastest = display_df.loc[display_df['Time (seconds)'].idxmin(), 'Algorithm']
                        shortest = display_df.loc[display_df['Distance (km)'].idxmin(), 'Algorithm']
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.info(f"⚡ **Fastest Algorithm:** {fastest}")
                        with col2:
                            st.info(f"📏 **Shortest Distance:** {shortest}")
                        
                        # Plot the shortest path
                        shortest_result = results[display_df['Distance (km)'].idxmin()]
                        st.subheader("🗺️ Shortest Path Visualization")
                        plot_shortest_path(G, shortest_result['Path'], start_node, end_node, shortest_result['Algorithm'])

        except Exception as e:
            st.error(f"❌ Could not compute path: {e}")
            st.exception(e)

# =============================
# Footer
# =============================
st.markdown(
    """
    ---
    🧠 **Developed by:** Dhairya  
    🎓 Demonstrates understanding of **Graph Algorithms** (Dijkstra, A\*, BFS, Bellman-Ford)  
    Built with **Streamlit + NetworkX + OSMnx**
    """
)