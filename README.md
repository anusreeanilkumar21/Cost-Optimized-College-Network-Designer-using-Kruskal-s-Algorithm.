# Cost-Optimized College Network Designer Using Kruskal's Algorithm

A GUI-based Design and Analysis of Algorithms (DAA) project that demonstrates how **Kruskal's Algorithm** can find a minimum-cost set of connections for a college campus network.

The application models college buildings as vertices and possible network cable connections as weighted edges. It sorts the edges by installation cost and selects connections that join separate components, avoiding cycles.

> **Note:** Installation costs in the sample network are illustrative estimates in Indian rupees, not quotations from network providers.

## Table of Contents

- [Objectives](#objectives)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Requirements](#requirements)
- [Installation and Setup](#installation-and-setup)
- [How to Run](#how-to-run)
- [How to Use the Application](#how-to-use-the-application)
- [How the Algorithm Works](#how-the-algorithm-works)
- [Complexity Analysis](#complexity-analysis)
- [Sample Network and Expected Result](#sample-network-and-expected-result)
- [Testing Checklist](#testing-checklist)
- [Project Structure](#project-structure)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [Academic Project Information](#academic-project-information)

## Objectives

- Apply a Greedy algorithm to a practical network-design problem.
- Provide a graphical interface for entering buildings and connection costs.
- Visualize a weighted graph and show Kruskal's decisions step by step.
- Calculate the total cost of the selected connections.
- Demonstrate cycle detection using a Disjoint Set Union (DSU) data structure.
- Test normal inputs and boundary cases.

## Features

- Add college buildings.
- Define possible undirected connections between buildings with installation costs.
- View the connections and costs in a table.
- Display the network as a weighted graph.
- Process the algorithm one edge at a time or run all steps.
- Show selected and rejected edges using different visual styles.
- Calculate the total cost of accepted connections.
- Handle disconnected graphs by reporting that a spanning tree is not possible.
- Save a text cost report from the application.

Available controls depend on the version of `main.py` being used. Confirm each feature in the running application before describing it as demonstrated in a submission.

## Technology Stack

- **Python** — application logic and Kruskal's Algorithm
- **Tkinter** — desktop graphical user interface
- **Matplotlib** — graph visualization
- **Disjoint Set Union (DSU)** — efficient cycle detection using path compression and union by rank

## Requirements

- Windows
- Python 3
- Matplotlib

Tkinter is normally included with standard Windows Python installations.

## Installation and Setup

### 1. Open Command Prompt

Go to the project folder:

```bat
D:
cd \CollegeNetworkDesigner
```

### 2. Install Matplotlib

```bat
py -m pip install matplotlib
```

If the `py` command is unavailable, try:

```bat
python -m pip install matplotlib
```

### 3. Run the application

```bat
py main.py
```

Alternatively, run the file using its full path:

```bat
py "D:\CollegeNetworkDesigner\main.py"
```

## How to Use the Application

1. Launch the program using the command above.
2. Review the sample buildings and possible network connections.
3. Add buildings and enter possible connections with their estimated costs.
4. Start or reset the algorithm.
5. Use **Next Step** to examine one edge at a time, or **Run All Steps** to complete the calculation.
6. Observe which edges are selected and which are rejected because they would create a cycle.
7. Review the selected connections and total estimated cost.
8. Use the report-saving option, if available in your version, to save the result.

## How the Algorithm Works

Kruskal's Algorithm builds a Minimum Spanning Tree (MST) for a connected, weighted, undirected graph.

1. Sort all edges in ascending order of cost.
2. Initialize each building as its own connected component.
3. Consider the cheapest remaining edge.
4. Use DSU to check whether the two endpoints belong to different components.
5. If they are in different components, accept the edge and merge the components.
6. If they are already in the same component, reject the edge because it would create a cycle.
7. Stop after accepting `V - 1` edges, or when all edges have been considered.

Here, `V` is the number of buildings. If the graph is disconnected, a spanning tree cannot connect every building; Kruskal's process instead produces a minimum spanning forest.

### Pseudocode

```text
KRUSKAL(G):
    sort all edges by non-decreasing weight
    make each vertex its own DSU set
    MST = empty set
    total_cost = 0

    for each edge (u, v, weight) in sorted edges:
        if FIND(u) != FIND(v):
            add edge (u, v, weight) to MST
            UNION(u, v)
            total_cost = total_cost + weight

        if MST contains V - 1 edges:
            stop

    if MST contains V - 1 edges:
        report MST and total_cost
    else:
        report that the graph is disconnected
```

## Complexity Analysis

Let:

- `V` = number of buildings (vertices)
- `E` = number of possible connections (edges)
- `α(V)` = inverse Ackermann function, which grows extremely slowly

| Operation | Complexity |
|---|---:|
| Sorting the edges | `O(E log E)` |
| DSU operations across the edges | `O(E α(V))` amortized |
| Overall time complexity | `O(E log E)` |
| Space complexity | `O(V + E)` |

The overall time complexity is `O(E log E)` because sorting dominates the DSU work. The space complexity includes storing the graph, edge list and DSU structures. These bounds describe the core algorithm; GUI drawing and rendering add their own overhead.

## Sample Network and Expected Result

The sample network uses these illustrative costs:

| Building A | Building B | Cost (₹) |
|---|---|---:|
| Admin Block | Library | 20,000 |
| Admin Block | Computer Lab | 35,000 |
| Admin Block | Hostel | 25,000 |
| Library | Computer Lab | 10,000 |
| Library | Hostel | 30,000 |
| Library | Auditorium | 18,000 |
| Computer Lab | Auditorium | 12,000 |
| Hostel | Auditorium | 22,000 |

For this sample input, the expected minimum spanning tree contains four connections:

| Selected connection | Cost (₹) |
|---|---:|
| Library – Computer Lab | 10,000 |
| Computer Lab – Auditorium | 12,000 |
| Admin Block – Library | 20,000 |
| Hostel – Auditorium | 22,000 |
| **Total** | **64,000** |

The application should calculate this result from the entered graph; it should not hardcode the expected total.

## Testing Checklist

Run and record the actual outcome of each test before submitting the report.

| Test case | Input or action | Expected behavior |
|---|---|---|
| Connected graph | Use the sample network | MST with `V - 1` edges and total cost ₹64,000 |
| Cycle | Use a triangle with three edges | One edge is rejected if its endpoints are already connected |
| Disconnected graph | Multiple buildings with no path between all of them | Report that a spanning tree is impossible |
| One building | One vertex and no edges | Cost ₹0; no cable is required |
| Multiple isolated buildings | Several vertices and no edges | No spanning tree exists |
| Equal edge weights | Give several edges the same cost | Return a valid MST; more than one MST may be possible |
| Zero-cost edge | Add an edge with cost `0` | It can be selected if it joins separate components |
| Negative cost | Enter a negative value | Reject the input if negative costs are disallowed |
| Non-numeric cost | Enter text instead of a number | Display a validation error |
| Self-connection | Select the same building at both ends | Reject the connection |
| Duplicate connection | Add the same undirected pair twice | Reject the duplicate or handle it according to documented behavior |
| Remove a connection | Delete an edge and rerun | Recalculate the result from the updated graph |
| Remove a building | Remove a building, if supported | Remove/update its incident edges and recalculate |

**Testing note:** An expected result is not proof that a test passed. Record the observed result after running each test and capture screenshots of the real application.

## Project Structure

A simple project folder may look like this:

```text
CollegeNetworkDesigner/
├── main.py
├── README.md
└── screenshots/
    ├── initial-network.png
    ├── algorithm-step.png
    └── final-result.png
```

The `screenshots` folder is optional. Create it and add screenshots captured from your own running application.

## Limitations and Future Improvements

### Limitations

- The result depends on the accuracy of the costs entered by the user.
- A minimum spanning tree does not provide backup links for fault tolerance.
- Real network planning may require cable-route distances, bandwidth, reliability, construction restrictions and maintenance costs.
- The current model treats each connection as an undirected edge with one cost.

### Future Improvements

- Add building deletion and safe editing of all graph data.
- Export reports as CSV or PDF.
- Add graph import/export.
- Include alternative cable types and per-metre installation costs.
- Compare Kruskal's result with Prim's Algorithm.
- Add network redundancy analysis for backup connections.

## Academic Project Information

**Project title:** Cost-Optimized College Network Designer Using Kruskal's Algorithm  
**Subject:** Design and Analysis of Algorithms  
**Assignment:** Assignment 2 — GUI-Based Algorithm Implementation  
**Algorithm category:** Greedy Method  
**Core concept:** Minimum Spanning Tree

**Student name:** [Enter your name]  
**Register number:** [Enter your register number]  
**Department:** [Enter your department]  
**Institution:** [Enter your institution]  
**Academic year:** [Enter academic year]

---

This project demonstrates the application of Kruskal's Greedy Algorithm to a college network-design scenario. The GUI helps users understand edge sorting, cycle detection, minimum spanning trees and estimated installation-cost optimization.
