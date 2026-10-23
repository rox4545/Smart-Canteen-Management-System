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

