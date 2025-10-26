# 🚗 Pathfinding Algorithm Visualizer

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive web application that visualizes and compares classic pathfinding algorithms on real-world road networks using OpenStreetMap data. Built with Streamlit, NetworkX, and OSMnx.

[main](data/main.png)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Algorithms Implemented](#algorithms-implemented)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Architecture](#project-architecture)
- [Performance Analysis](#performance-analysis)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🎯 Overview

This project demonstrates a deep understanding of graph algorithms and their practical applications in solving real-world routing problems. The application downloads actual street network data from OpenStreetMap and allows users to compare four classic pathfinding algorithms: **Dijkstra's Algorithm**, **A* (A-Star)**, **Breadth-First Search (BFS)**, and **Bellman-Ford Algorithm**.

### Motivation

Understanding the trade-offs between different pathfinding algorithms is crucial in computer science and software engineering. This project provides an interactive way to visualize these differences and understand how algorithm choice impacts performance in real-world scenarios.

---

## ✨ Features

### 1. **Real-World Map Integration**
- Downloads and processes street network data from any location worldwide
- Uses OpenStreetMap's comprehensive road network database
- Caches downloaded maps for improved performance


### 2. **Dual Input Modes**
- **Dropdown Mode**: Select from pre-generated location suggestions (faster)
- **Custom Location Mode**: Enter any address or landmark manually

**data/dual_input.png**

### 3. **Algorithm Comparison**
- **Single Algorithm Mode**: Test one algorithm at a time
- **Compare All Algorithms Mode**: Run all four algorithms simultaneously and compare results

**data/comparison.png**

### 4. **Visual Path Rendering**
- Interactive map visualization with highlighted shortest paths
- Clear start (green) and destination (red) markers
- Clean, professional map aesthetics

**data/map.png**

### 5. **Performance Metrics**
- Distance traveled (in kilometers)
- Execution time (in seconds)
- Number of nodes visited
- Side-by-side algorithm comparison tables


### 6. **Comparative Analysis**
- Interactive bar charts comparing distance and execution time
- Automatic identification of fastest algorithm and shortest path
- Detailed results table with highlighting

**data/dist_comp.png**

**data/exe_comp.png**

---

## 🧮 Algorithms Implemented

### 1. **Dijkstra's Algorithm**
- **Type**: Single-source shortest path
- **Time Complexity**: O((V + E) log V) with binary heap
- **Space Complexity**: O(V)
- **Use Case**: Optimal for finding shortest paths in graphs with non-negative edge weights
- **Characteristics**: Guarantees optimal solution, explores nodes in order of distance from source

### 2. **A* (A-Star) Algorithm**
- **Type**: Informed search algorithm
- **Time Complexity**: O(E) in best case, O(b^d) in worst case
- **Space Complexity**: O(V)
- **Use Case**: Best for point-to-point routing with known destination
- **Characteristics**: Uses heuristic (Euclidean distance) to guide search, typically faster than Dijkstra for single target

### 3. **Breadth-First Search (BFS)**
- **Type**: Unweighted shortest path
- **Time Complexity**: O(V + E)
- **Space Complexity**: O(V)
- **Use Case**: Finding path with minimum number of edges (hops)
- **Characteristics**: Ignores edge weights, finds path with fewest intermediate nodes

### 4. **Bellman-Ford Algorithm**
- **Type**: Single-source shortest path
- **Time Complexity**: O(V × E)
- **Space Complexity**: O(V)
- **Use Case**: Handles graphs with negative edge weights, detects negative cycles
- **Characteristics**: Slower than Dijkstra but more versatile, works with negative weights

**data/comparison.png**

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Web application framework for rapid prototyping
- **NetworkX**: Graph analysis and algorithm implementation
- **OSMnx**: OpenStreetMap data processing and network analysis
- **Matplotlib**: Data visualization and map rendering
- **Pandas**: Data manipulation and analysis

### Key Libraries
```python
streamlit>=1.28.0
osmnx>=1.6.0
networkx>=3.1
matplotlib>=3.7.0
pandas>=2.0.0
```

---

## 📥 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection (for downloading map data)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/pathfinding-visualizer.git
cd pathfinding-visualizer
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
- Open your browser and navigate to `http://localhost:8501

---

## 🚀 Usage

### Basic Workflow

1. **Load a Map**
   - Enter a city or location name (e.g., "San Francisco, California, USA")
   - Click "Load Map" button
   - Wait for the network to download and process

2. **Select Start and Destination**
   - Choose input mode (Dropdown or Custom Location)
   - Select or enter start location
   - Select or enter destination location

3. **Choose Algorithm Mode**
   - **Single Algorithm**: Select one algorithm and click "Find Path"
   - **Compare All Algorithms**: Click "Compare All Algorithms" to test all four

4. **Analyze Results**
   - View path visualization on map
   - Compare metrics (distance, time, nodes)
   - Analyze performance differences

### Example Queries
```
Location: "Manhattan, New York, USA"
Start: "Times Square, New York"
Destination: "Central Park, New York"
```
```
Location: "London, United Kingdom"
Start: "Trafalgar Square, London"
Destination: "Tower Bridge, London"
```

---

## 🏗️ Project Architecture

### File Structure
```
pathfinding-visualizer/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # MIT License
│
├── .gitignore            # Git ignore rules
└── data/               # Screenshots and media
    ├── screenshot1.png
    ├── screenshot2.png
    └── ...
```

### Code Organization

#### 1. **Configuration**
```python
st.set_page_config(page_title="Shortest Path Visualizer", 
                   page_icon="🧭", 
                   layout="wide")
```

#### 2. **Helper Functions**

**`load_graph(place_name)`**
- Downloads street network from OpenStreetMap
- Adds edge speeds and travel times
- Implements caching for performance optimization

**`get_location_suggestions(G, num_suggestions=20)`**
- Extracts strategic nodes from graph
- Creates user-friendly location labels
- Samples nodes evenly across network

**`run_algorithm(G, start_node, end_node, algorithm)`**
- Executes selected pathfinding algorithm
- Measures execution time
- Calculates path length and metrics

**`compare_all_algorithms(G, start_node, end_node)`**
- Runs all four algorithms sequentially
- Collects performance data
- Handles algorithm failures gracefully

**`plot_shortest_path(G, route, orig_node, dest_node, algo_name)`**
- Renders map with highlighted route
- Adds start/end markers
- Displays using Matplotlib

**`plot_comparison_chart(results_df)`**
- Creates comparative bar charts
- Visualizes distance and time metrics
- Uses color-coded representation

#### 3. **User Interface Components**

- **Input Section**: Map loading and location selection
- **Algorithm Selection**: Single or comparison mode
- **Results Display**: Metrics, visualizations, and analysis
- **Footer**: Project credits and information

---

## 📊 Performance Analysis

### Algorithm Comparison Results

Based on typical urban road networks:

| Algorithm | Avg. Time | Path Optimality | Use Case |
|-----------|-----------|-----------------|----------|
| **A*** | ⚡ Fastest | ✅ Optimal | Point-to-point routing |
| **Dijkstra** | 🔄 Fast | ✅ Optimal | Multiple destinations |
| **BFS** | ⚡ Very Fast | ❌ Suboptimal | Minimum hops |
| **Bellman-Ford** | 🐢 Slowest | ✅ Optimal | Negative weights |


### Key Insights

1. **A* typically outperforms Dijkstra** for single-target searches due to heuristic guidance
2. **BFS finds paths quickly** but doesn't consider edge weights (distance)
3. **Bellman-Ford is significantly slower** for large graphs but handles edge cases
4. **Urban networks favor A*** due to good heuristic estimates

---

## 🔬 Technical Highlights

### Graph Theory Application
- **Directed/Undirected Graph Handling**: Works with OSM's directed road networks
- **Edge Weight Processing**: Considers actual road distances
- **Node Degree Analysis**: Handles complex intersections

### Optimization Techniques
- **Graph Caching**: Stores downloaded networks to avoid redundant API calls
- **Lazy Loading**: Generates location suggestions only when needed
- **Efficient Data Structures**: Uses NetworkX's optimized graph representations

### Error Handling
- Graceful handling of invalid locations
- Algorithm failure recovery
- Network timeout management
- User-friendly error messages

---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Multi-waypoint Routing**: Support for multiple stops
- [ ] **Time-based Routing**: Consider traffic patterns and time of day
- [ ] **Alternative Routes**: Show multiple path options
- [ ] **3D Visualization**: Elevation-aware routing
- [ ] **Export Functionality**: Download routes as GPX/KML files
- [ ] **Mobile Optimization**: Responsive design for mobile devices
- [ ] **Real-time Traffic**: Integration with live traffic data
- [ ] **Custom Heuristics**: Allow users to define A* heuristics

### Algorithm Additions
- [ ] Bidirectional Dijkstra
- [ ] Floyd-Warshall (all-pairs shortest path)
- [ ] Johnson's Algorithm
- [ ] Contraction Hierarchies

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add comments for complex logic
- Update documentation for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Contact

**Dhairya**

- GitHub: [@yourusername](https://github.com/DhairyaSavaliya)
- Email: dhairyasavaliya73@gmail.com

**Project Link**: [https://github.com/yourusername/pathfinding-visualizer](https://github.com/DhairyaSavaliya/Pathfinding-Algorithm-Visualizer)

---

## 🙏 Acknowledgments

- **OpenStreetMap Contributors**: For providing comprehensive map data
- **OSMnx Team**: For the excellent Python library
- **NetworkX Developers**: For robust graph algorithms
- **Streamlit Team**: For the intuitive web framework

---

## 📚 References

1. Dijkstra, E. W. (1959). "A note on two problems in connexion with graphs"
2. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
3. Bellman, R. (1958). "On a routing problem"
4. Boeing, G. (2017). "OSMnx: New methods for acquiring, constructing, analyzing, and visualizing complex street networks"

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for learning and exploration

</div>
