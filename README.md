# CANTEEN MANAGEMENT SYSTEM 

## Project Overview

This project models a campus canteen operational workflow as a Data Structures and Algorithms (DSA) management system in Python. The core focus is **Graph Algorithms** where canteen locations/counters are nodes/vertices and physical/walking paths are weighted edges. Supporting DSA structures handle order queueing, VIP priority serving, inventory management, table interval scheduling, ready order timeout deadlines, and dynamic kitchen cooking priority.

---

##  Key Graph Algorithms Implemented (G1 – G10)

| Problem ID | Problem Description | Algorithm Implemented | Time Complexity | Solution Summary & Application |
| :--- | :--- | :--- | :--- | :--- |
| **G1** | Minimum movements route between counters | **Breadth-First Search (BFS)** | O(V + E) | Unweighted graph search calculating minimum counter transitions (e.g., Billing -> Collection). |
| **G2** | Fastest route through counters | **Dijkstra's Shortest Path Algorithm** | O((V + E) \log V) | MinHeap-based weighted shortest path optimization considering walking & waiting times in minutes. |
| **G3** | Check counter reachability | **Depth-First Search (DFS)** | O(V + E) | Verifies if all required food counters in a student order are reachable from the Billing counter. |
| **G4** | Detect disconnected canteen sections | **Connected Components (DFS/BFS)** | O(V + E) | Identifies independent isolated clusters/sections within the canteen graph. |
| **G5** | Order workflow operation ordering | **Topological Sorting (Kahn's Algorithm)** | O(V + E) | Generates a valid linear task execution sequence for DAG workflow: `Place Order` -> `Payment` -> `Preparation` -> `Food Ready` -> `Collection`. |
| **G6** | Detect circular workflow dependencies | **Cycle Detection in Directed Graph** | O(V + E) | Uses DFS recursion stack to catch invalid circular workflow dependencies (e.g., `Payment` -> `Prep` -> `Collection` -> `Payment`). |
| **G7** | Minimum-cost canteen infrastructure network | **Prim's & Kruskal's MST** | $O(E \log E)$ / O(E \log V) | Computes minimum spanning tree for network cabling / path infrastructure linking all canteen nodes without cycles. |
| **G8** | Process independent counters in parallel | **Dependency Graph & Parallel Processing** | O(V + E) | Models multi-item orders as DAG where independent counters (Chicken, Biryani, Puffs, Drinks) prepare concurrently, reducing wait times. |
| **G9** | Peak throughput and bottleneck of the canteen | **Max-Flow / Min-Cut (Edmonds-Karp)** | O(V E^2) | Capacities (students/min) on a directed flow network. BFS finds shortest augmenting paths in the residual graph; the min-cut identifies the bottleneck corridors (Collection→Exit, Tables→Exit: 17 students/min). |
| **G10** | Counters/corridors whose closure splits the canteen | **Tarjan's Articulation Points & Bridges** | O(V + E) | DFS discovery-time / low-link values find critical counters (Billing, Collection) and critical corridors (Entrance–Billing). Closure impact is verified by re-running G4. |

---

## Supporting Non-Graph DSA Problems Implemented (S1 – S5)

| Problem ID | Supporting DSA Problem | Data Structure & Algorithm | Purpose & Function |
| :--- | :--- | :--- | :--- |
| **S1** | Wrong student collects an order | **FIFO Queue + Priority Queue + Hash Table** | FIFO Queue for normal student orders, MinHeap Priority Queue for VIP priority serving, and $O(1)$ Hash Table mapping `Token` -> `Student & Order Details`. |
| **S2** | Food unavailable after ordering | **Array/List + Searching + Hash Table** | Stock inventory management with O(1) searching, availability checking, stock auto-decrement, and out-of-stock marking. |
| **S3** | Table allocation & sitting time | **FIFO Queue + Interval Scheduling** | Dining table interval scheduler tracking entry/exit times with an automated waiting queue when tables are fully occupied. |
| **S4** | Food ready but not collected | **Priority Queue + Timeout Scheduler + Hash Table** | Attaches a collection deadline timer to ready orders. Automatically marks uncollected orders as expired upon deadline timeout. |
| **S5** | High-demand food at peak times | **Frequency Counting + Dynamic Priority Queue** | Tracks item order volume frequency in time windows and dynamically adjusts cooking priority scores in the kitchen MinHeap. |

---

## Project Structure

```
Smart-Canteen-Management-System/
├── dsa/
│   ├── __init__.py
│   ├── graph.py               # Adjacency List Graph + canteen & flow-network builders
│   ├── supporting_dsa.py      # Custom Queue, MinHeap PriorityQueue, HashTable, Inventory, TableScheduler
│   ├── graph_algorithms.py   # Pure Python implementations for G1–G10 algos
│   └── canteen_system.py     # Canteen System Orchestrator facade
├── main.py                    # Interactive Command-Line Menu application
├── test_dsa.py                # Automated Unit Test Suite
└── README.md                  # Detailed Documentation
```

---

## How to run Project

### 1. Automated Test Suite
Verify all 15 DSA implementations (G1–G10 and S1–S5) by running:
```bash
python test_dsa.py
```

### 2. Interactive Terminal CLI Application
Run:
```bash
python main.py
```

---

##  Verification Results

All 15 problems (G1–G10, S1–S5) are covered by the automated test suite:
- (verified) **BFS (G1)**: Correctly finds minimum edge movements.
- (verified)  **Dijkstra (G2)**: Computes optimal walking/waiting route.
- (verified) **DFS Reachability (G3)**: Validates target node reachability.
- (verified) **Connected Components (G4)**: Detects graph component count.
- (verified) **Topological Sort (G5)**: Produces valid linear workflow order.
- (verified) **Cycle Detection (G6)**: Catches directed cycles accurately.
- (verified) **Prim & Kruskal MST (G7)**: Calculates identical minimum spanning cost.
- (verified) **Parallel Kitchen Engine (G8)**: Simulates concurrent counter execution.
- (verified) **Max-Flow / Min-Cut (G9)**: Max throughput 17 students/min; cut capacity equals flow; flow conserved at every node.
- (verified) **Articulation Points & Bridges (G10)**: Billing and Collection are critical; closing either splits the canteen in two.
- (verified) **Supporting DSA (S1-S5)**: Priority Queue, Hash Table, Inventory, Table Interval Scheduling, and Timeout Deadlines verified.
