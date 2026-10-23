"""
Graph Algorithms Implementation for Canteen Management System.
Contains pure Python custom implementations for Problems G1 through G10.
"""

from typing import Dict, List, Optional, Set, Tuple
from dsa.graph import Graph, Edge, Vertex, VertexType, EdgeWeightMeaning
from dsa.supporting_dsa import FIFOQueue, PriorityQueue


# ==========================================
# G1: BREADTH-FIRST SEARCH (Unweighted Shortest Path)
# ==========================================
def bfs_shortest_path(graph: Graph, source: str, destination: str) -> Tuple[float, List[str], List[Dict]]:
    """
    Finds the minimum number of counter movements (edges) from source to destination using BFS.
    Time Complexity: O(V + E)
    Returns: (edge_count, path_vertices, step_by_step_trace)
    """
    if source not in graph.vertices or destination not in graph.vertices:
        return float('inf'), [], []

    visited: Set[str] = {source}
    parent: Dict[str, Optional[str]] = {source: None}
    distance: Dict[str, int] = {source: 0}
    queue = FIFOQueue[str]()
    queue.enqueue(source)

    trace = []
    step = 0

    while not queue.is_empty():
        curr = queue.dequeue()
        step += 1
        trace.append({
            "step": step,
            "current_vertex": curr,
            "visited_set": list(visited),
            "queue_state": queue.to_list()
        })

        if curr == destination:
            break

        for edge in graph.get_neighbors(curr):
            nxt = edge.destination
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = curr
                distance[nxt] = distance[curr] + 1
                queue.enqueue(nxt)

    if destination not in parent:
        return float('inf'), [], trace

    # Reconstruct path
    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return distance[destination], path, trace


# ==========================================
# G2: DIJKSTRA'S SHORTEST PATH (Weighted Minimum Time)
# ==========================================
def dijkstra_shortest_path(graph: Graph, source: str, destination: str) -> Tuple[float, List[str], List[Dict]]:
    """
    Finds the route with minimum total walking/waiting time using Dijkstra's Algorithm with MinHeap.
    Time Complexity: O((V + E) log V)
    Returns: (min_total_time, path_vertices, step_by_step_trace)
    """
    if source not in graph.vertices or destination not in graph.vertices:
        return float('inf'), [], []

    distances: Dict[str, float] = {v: float('inf') for v in graph.vertices}
    distances[source] = 0.0
    predecessor: Dict[str, Optional[str]] = {v: None for v in graph.vertices}
    visited: Set[str] = set()

    pq = PriorityQueue[str]()
    pq.push(0.0, source)

    trace = []
    step = 0

    while not pq.is_empty():
        pop_res = pq.pop()
        if not pop_res:
            break
        curr_dist, u = pop_res

        if u in visited:
            continue
        visited.add(u)
        step += 1

        trace.append({
            "step": step,
            "evaluated_vertex": u,
            "known_distance": curr_dist,
            "distances": dict(distances),
            "visited_set": list(visited)
        })

        if u == destination:
            break

        for edge in graph.get_neighbors(u):
            v = edge.destination
            weight = edge.weight
            if v not in visited:
                new_dist = distances[u] + weight
                if new_dist < distances[v]:
                    distances[v] = new_dist
                    predecessor[v] = u
                    pq.push(new_dist, v)

    if distances[destination] == float('inf'):
        return float('inf'), [], trace

    # Reconstruct shortest path
    path = []
    curr = destination
    while curr is not None:
        path.append(curr)
        curr = predecessor[curr]
    path.reverse()

    return distances[destination], path, trace


# ==========================================
# G3: DFS REACHABILITY CHECK
# ==========================================
def dfs_reachability(graph: Graph, source: str, required_counters: List[str]) -> Tuple[bool, List[str], List[str]]:
    """
    Checks whether all required food counters are reachable from the starting source (e.g. Billing).
    Time Complexity: O(V + E)
    Returns: (all_reachable, reachable_list, unreachable_list)
    """
    if source not in graph.vertices:
        return False, [], required_counters

    visited: Set[str] = set()

    def dfs(u: str):
        visited.add(u)
        for edge in graph.get_neighbors(u):
            if edge.destination not in visited:
                dfs(edge.destination)

    dfs(source)

    reachable = [c for c in required_counters if c in visited]
    unreachable = [c for c in required_counters if c not in visited]

    return len(unreachable) == 0, reachable, unreachable


# ==========================================
# G4: CONNECTED COMPONENTS (Detect Disconnected Sections)
# ==========================================
def find_connected_components(graph: Graph) -> Tuple[int, List[List[str]]]:
    """
    Finds the number of independent connected sections in the canteen graph.
    Time Complexity: O(V + E)
    Returns: (num_components, components_list)
    """
    visited: Set[str] = set()
    components: List[List[str]] = []

    for vertex_id in graph.vertices:
        if vertex_id not in visited:
            component = []
            queue = FIFOQueue[str]()
            queue.enqueue(vertex_id)
            visited.add(vertex_id)

            while not queue.is_empty():
                curr = queue.dequeue()
                component.append(curr)
                for edge in graph.get_neighbors(curr):
                    nxt = edge.destination
                    if nxt not in visited:
                        visited.add(nxt)
                        queue.enqueue(nxt)
            
            components.append(component)

    return len(components), components


# ==========================================
# G5: TOPOLOGICAL SORTING (Workflow Dependencies)
# ==========================================
def topological_sort(workflow_graph: Graph) -> Tuple[bool, List[str], str]:
    """
    Computes a valid execution sequence for order workflow dependencies using Kahn's Algorithm.
    Time Complexity: O(V + E)
    Returns: (is_valid_dag, sorted_order, log_message)
    """
    in_degree: Dict[str, int] = {v: 0 for v in workflow_graph.vertices}

    for u in workflow_graph.vertices:
        for edge in workflow_graph.get_neighbors(u):
            in_degree[edge.destination] += 1

    queue = FIFOQueue[str]()
    for v, deg in in_degree.items():
        if deg == 0:
            queue.enqueue(v)

    topo_order = []
    while not queue.is_empty():
        curr = queue.dequeue()
        topo_order.append(curr)

        for edge in workflow_graph.get_neighbors(curr):
            nxt = edge.destination
            in_degree[nxt] -= 1
            if in_degree[nxt] == 0:
                queue.enqueue(nxt)

    if len(topo_order) != len(workflow_graph.vertices):
        return False, [], "Workflow contains a circular dependency cycle! Topological ordering impossible."

    return True, topo_order, "Valid topological workflow sequence generated successfully."
# ==========================================
# G6: CYCLE DETECTION IN DIRECTED GRAPH
# ==========================================
def detect_cycle_directed(directed_graph: Graph) -> Tuple[bool, List[str]]:
    """
    Detects circular workflow dependencies using DFS recursion stack.
    Time Complexity: O(V + E)
    Returns: (has_cycle, cycle_path)
    """
    visited: Set[str] = set()
    rec_stack: Set[str] = set()
    path_stack: List[str] = []
    cycle_nodes: List[str] = []

    def dfs(u: str) -> bool:
        visited.add(u)
        rec_stack.add(u)
        path_stack.append(u)

        for edge in directed_graph.get_neighbors(u):
            v = edge.destination
            if v not in visited:
                if dfs(v):
                    return True
            elif v in rec_stack:
                # Cycle found! Extract cycle path
                cycle_start_idx = path_stack.index(v)
                cycle_nodes.extend(path_stack[cycle_start_idx:] + [v])
                return True

        path_stack.pop()
        rec_stack.remove(u)
        return False

    for node in directed_graph.vertices:
        if node not in visited:
            if dfs(node):
                return True, cycle_nodes

    return False, []


# ==========================================
# G7: MINIMUM SPANNING TREE (Kruskal's & Prim's Algorithms)
# ==========================================
class UnionFind:
    """Disjoint Set Union (DSU) for Kruskal's MST algorithm."""
    def __init__(self, vertices: List[str]):
        self.parent: Dict[str, str] = {v: v for v in vertices}
        self.rank: Dict[str, int] = {v: 0 for v in vertices}

    def find(self, i: str) -> str:
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: str, j: str) -> bool:
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False


def kruskal_mst(graph: Graph) -> Tuple[float, List[Edge]]:
    """
    Computes the Minimum Spanning Tree for canteen network/cabling using Kruskal's Algorithm.
    Time Complexity: O(E log E)
    Returns: (total_min_cost, mst_edges)
    """
    all_edges = graph.get_all_edges()
    sorted_edges = sorted(all_edges, key=lambda e: e.weight)

    uf = UnionFind(list(graph.vertices.keys()))
    mst_edges = []
    total_cost = 0.0

    for edge in sorted_edges:
        if uf.union(edge.source, edge.destination):
            mst_edges.append(edge)
            total_cost += edge.weight

    return total_cost, mst_edges


def prim_mst(graph: Graph, start_vertex: str = "BILLING") -> Tuple[float, List[Edge]]:
    """
    Computes the Minimum Spanning Tree using Prim's Algorithm with Priority Queue.
    Time Complexity: O(E log V)
    Returns: (total_min_cost, mst_edges)
    """
    if start_vertex not in graph.vertices:
        return 0.0, []

    visited: Set[str] = {start_vertex}
    pq = PriorityQueue[Edge]()
    mst_edges = []
    total_cost = 0.0

    for edge in graph.get_neighbors(start_vertex):
        pq.push(edge.weight, edge)

    while not pq.is_empty() and len(visited) < len(graph.vertices):
        pop_res = pq.pop()
        if not pop_res:
            break
        weight, edge = pop_res

        if edge.destination in visited:
            continue

        visited.add(edge.destination)
        mst_edges.append(edge)
        total_cost += weight

        for nxt_edge in graph.get_neighbors(edge.destination):
            if nxt_edge.destination not in visited:
                pq.push(nxt_edge.weight, nxt_edge)

    return total_cost, mst_edges


# ==========================================
# G8: PARALLEL FOOD PREPARATION DEPENDENCY SIMULATION
# ==========================================
def simulate_parallel_kitchen_tasks(order_id: str, items_by_counter: Dict[str, List[str]]) -> Dict:
    """
    Models multi-item order preparation as a DAG where independent counters (Chicken, Biryani, Puffs, Drinks)
    prepare food concurrently in parallel, then join at Collection.
    Time Complexity: O(V + E)
    """
    dep_graph = Graph(is_directed=True)
    dep_graph.add_vertex("ORDER_MGMT", f"Order #{order_id} Received", VertexType.BILLING)
    dep_graph.add_vertex("COLLECTION", "Collection Counter Join", VertexType.COLLECTION)

    # Counter preparation time estimates
    prep_times = {
        "CHICKEN": 8.0,
        "BIRYANI": 10.0,
        "PUFFS": 2.0,
        "DRINKS": 1.0
    }

    parallel_branches = []

    for counter, items in items_by_counter.items():
        if not items:
            continue
        c_node = f"PREP_{counter}"
        dep_graph.add_vertex(c_node, f"Prepare {', '.join(items)} at {counter}", VertexType.FOOD_COUNTER)
        
        c_time = prep_times.get(counter, 5.0)
        dep_graph.add_edge("ORDER_MGMT", c_node, weight=0.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
        dep_graph.add_edge(c_node, "COLLECTION", weight=c_time, weight_meaning=EdgeWeightMeaning.WAITING_TIME_MINS)

        parallel_branches.append({
            "counter": counter,
            "items": items,
            "prep_time_mins": c_time
        })

    # Parallel bottleneck is the max prep time among all active counters
    max_prep_time = max([b["prep_time_mins"] for b in parallel_branches]) if parallel_branches else 0.0
    sequential_time = sum([b["prep_time_mins"] for b in parallel_branches])

    return {
        "order_id": order_id,
        "dependency_graph": dep_graph,
        "parallel_branches": parallel_branches,
        "parallel_completion_time_mins": max_prep_time,
        "sequential_completion_time_mins": sequential_time,
        "time_saved_mins": round(sequential_time - max_prep_time, 2)
    }



# ==========================================
# G9: MAX-FLOW / MIN-CUT (Edmonds-Karp)
# ==========================================
def edmonds_karp_max_flow(flow_graph: Graph, source: str, sink: str) -> Dict:
    """
    Computes the maximum student throughput (students/min) from source to sink using
    Edmonds-Karp (Ford-Fulkerson where each augmenting path is the BFS shortest path),
    then derives the Min-Cut, i.e. the bottleneck edges that limit throughput.
    Edge weight = capacity.
    Time Complexity: O(V * E^2)
    Returns dict: max_flow, edge_flows, min_cut_edges, source_side, augmenting_paths
    """
    if source not in flow_graph.vertices or sink not in flow_graph.vertices or source == sink:
        return {"max_flow": 0.0, "edge_flows": [], "min_cut_edges": [],
                "source_side": [], "augmenting_paths": []}

    # Residual capacity matrix as nested hash maps (reverse edges start at 0)
    residual: Dict[str, Dict[str, float]] = {v: {} for v in flow_graph.vertices}
    original: Dict[Tuple[str, str], float] = {}
    for u in flow_graph.vertices:
        for e in flow_graph.get_neighbors(u):
            residual[u][e.destination] = residual[u].get(e.destination, 0.0) + e.weight
            residual[e.destination].setdefault(u, 0.0)
            original[(u, e.destination)] = original.get((u, e.destination), 0.0) + e.weight

    max_flow = 0.0
    augmenting_paths: List[Dict] = []

    while True:
        # BFS for the shortest augmenting path in the residual graph
        parent: Dict[str, Optional[str]] = {source: None}
        queue = FIFOQueue[str]()
        queue.enqueue(source)
        while not queue.is_empty() and sink not in parent:
            u = queue.dequeue()
            for v, cap in residual[u].items():
                if cap > 0 and v not in parent:
                    parent[v] = u
                    queue.enqueue(v)

        if sink not in parent:
            break

        # Find bottleneck capacity along the path
        path = []
        v = sink
        bottleneck = float('inf')
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, residual[u][v])
            path.append(v)
            v = u
        path.append(source)
        path.reverse()

        # Augment: reduce forward residual, increase backward residual
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= bottleneck
            residual[v][u] += bottleneck

        max_flow += bottleneck
        augmenting_paths.append({"path": path, "bottleneck": bottleneck, "total_flow": max_flow})

    # Min-Cut: vertices still reachable from source in the final residual graph
    reachable: Set[str] = {source}
    queue = FIFOQueue[str]()
    queue.enqueue(source)
    while not queue.is_empty():
        u = queue.dequeue()
        for v, cap in residual[u].items():
            if cap > 0 and v not in reachable:
                reachable.add(v)
                queue.enqueue(v)

    min_cut_edges = [(u, v, c) for (u, v), c in original.items()
                     if u in reachable and v not in reachable]
    edge_flows = [(u, v, max(0.0, c - residual[u][v]), c) for (u, v), c in original.items()]

    return {
        "max_flow": max_flow,
        "edge_flows": edge_flows,
        "min_cut_edges": min_cut_edges,
        "source_side": sorted(reachable),
        "augmenting_paths": augmenting_paths
    }


# ==========================================
# G10: ARTICULATION POINTS & BRIDGES (Tarjan)
# ==========================================
def find_articulation_points_and_bridges(graph: Graph) -> Tuple[List[str], List[Tuple[str, str]], Dict]:
    """
    Finds critical counters (articulation points) and critical corridors (bridges) whose
    closure would disconnect the canteen, using Tarjan's discovery-time / low-link DFS.
    Intended for an undirected graph.
    Time Complexity: O(V + E)
    Returns: (articulation_points, bridges, low_link_table)
    """
    disc: Dict[str, int] = {}
    low: Dict[str, int] = {}
    articulation: Set[str] = set()
    bridges: List[Tuple[str, str]] = []
    timer = [0]

    def dfs(u: str, parent: Optional[str]) -> None:
        timer[0] += 1
        disc[u] = low[u] = timer[0]
        children = 0

        for edge in graph.get_neighbors(u):
            v = edge.destination
            if v == parent:
                continue
            if v in disc:
                low[u] = min(low[u], disc[v])          # back edge
            else:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append((u, v))             # no back edge above u
                if parent is not None and low[v] >= disc[u]:
                    articulation.add(u)

        if parent is None and children > 1:
            articulation.add(u)                        # DFS root with 2+ subtrees

    for vertex_id in graph.vertices:
        if vertex_id not in disc:
            dfs(vertex_id, None)

    table = {v: {"disc": disc[v], "low": low[v]} for v in disc}
    return sorted(articulation), bridges, table
