"""
Central Graph Representation for Canteen Management System.
Implements Adjacency List model with Vertices and Weighted Edges.
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple


class VertexType(Enum):
    ENTRANCE = "Entrance"
    BILLING = "Billing Counter"
    FOOD_COUNTER = "Food Counter"
    COLLECTION = "Collection Counter"
    TABLES = "Dining Tables"
    EXIT = "Exit"
    INFRASTRUCTURE = "Infrastructure Node"


class EdgeWeightMeaning(Enum):
    DISTANCE_METERS = "Distance (meters)"
    WALKING_TIME_MINS = "Walking Time (minutes)"
    WAITING_TIME_MINS = "Waiting Time (minutes)"
    TOTAL_SERVICE_COST = "Total Movement/Service Cost"
    NETWORK_CABLE_COST = "Infrastructure Cable/Path Cost"
    CAPACITY_STUDENTS_PER_MIN = "Capacity (students/min)"


class Vertex:
    def __init__(self, vertex_id: str, name: str, vertex_type: VertexType):
        self.id: str = vertex_id
        self.name: str = name
        self.type: VertexType = vertex_type

    def __repr__(self) -> str:
        return f"Vertex({self.id}: '{self.name}', type={self.type.value})"


class Edge:
    def __init__(self, source: str, destination: str, weight: float = 1.0, 
                 weight_meaning: EdgeWeightMeaning = EdgeWeightMeaning.WALKING_TIME_MINS):
        self.source: str = source
        self.destination: str = destination
        self.weight: float = weight
        self.weight_meaning: EdgeWeightMeaning = weight_meaning

    def __repr__(self) -> str:
        return f"Edge({self.source} -> {self.destination}, weight={self.weight} [{self.weight_meaning.value}])"


class Graph:
    """
    Central Canteen Adjacency List Graph representation.
    Supports directed and undirected, weighted and unweighted edges.
    """
    def __init__(self, is_directed: bool = False):
        self.is_directed: bool = is_directed
        self.vertices: Dict[str, Vertex] = {}
        self.adj_list: Dict[str, List[Edge]] = {}

    def add_vertex(self, vertex_id: str, name: str, vertex_type: VertexType) -> Vertex:
        if vertex_id not in self.vertices:
            v = Vertex(vertex_id, name, vertex_type)
            self.vertices[vertex_id] = v
            self.adj_list[vertex_id] = []
            return v
        return self.vertices[vertex_id]

    def add_edge(self, source: str, destination: str, weight: float = 1.0, 
                 weight_meaning: EdgeWeightMeaning = EdgeWeightMeaning.WALKING_TIME_MINS):
        if source not in self.vertices or destination not in self.vertices:
            raise ValueError(f"Both vertices '{source}' and '{destination}' must exist before adding edge.")

        edge = Edge(source, destination, weight, weight_meaning)
        self.adj_list[source].append(edge)

        if not self.is_directed:
            reverse_edge = Edge(destination, source, weight, weight_meaning)
            self.adj_list[destination].append(reverse_edge)

    def get_neighbors(self, vertex_id: str) -> List[Edge]:
        return self.adj_list.get(vertex_id, [])

    def get_all_vertices(self) -> List[Vertex]:
        return list(self.vertices.values())

    def get_all_edges(self) -> List[Edge]:
        edges = []
        seen = set()
        for u in self.adj_list:
            for edge in self.adj_list[u]:
                edge_pair = tuple(sorted([edge.source, edge.destination])) if not self.is_directed else (edge.source, edge.destination)
                if edge_pair not in seen:
                    seen.add(edge_pair)
                    edges.append(edge)
        return edges

    def without_vertex(self, vertex_id: str) -> 'Graph':
        """Returns a copy of this graph with one vertex (and all its edges) removed."""
        g = Graph(self.is_directed)
        for v_id, v in self.vertices.items():
            if v_id != vertex_id:
                g.add_vertex(v_id, v.name, v.type)
        for u in self.adj_list:
            if u == vertex_id:
                continue
            for e in self.adj_list[u]:
                if e.destination != vertex_id:
                    g.adj_list[u].append(Edge(e.source, e.destination, e.weight, e.weight_meaning))
        return g

    def print_adjacency_list(self) -> str:
        lines = []
        lines.append("=== CANTEEN CENTRAL GRAPH ADJACENCY LIST ===")
        for v_id, vertex in self.vertices.items():
            neighbors_str = ", ".join([f"{e.destination}(w={e.weight})" for e in self.adj_list[v_id]])
            lines.append(f"[{vertex.id}] {vertex.name} ({vertex.type.value}) -> [{neighbors_str}]")
        return "\n".join(lines)


def create_default_canteen_graph() -> Graph:
    """
    Creates the default canteen graph with 9 core counters/locations:
    Entrance, Billing, Chicken Counter, Biryani Counter, Puffs Counter,
    Drinks Counter, Collection Counter, Tables, Exit.
    """
    g = Graph(is_directed=False)  # Physical movement graph is undirected

    # Add Vertices
    g.add_vertex("ENTRANCE", "Canteen Entrance", VertexType.ENTRANCE)
    g.add_vertex("BILLING", "Billing Counter", VertexType.BILLING)
    g.add_vertex("CHICKEN", "Chicken Counter", VertexType.FOOD_COUNTER)
    g.add_vertex("BIRYANI", "Biryani Counter", VertexType.FOOD_COUNTER)
    g.add_vertex("PUFFS", "Puffs Counter", VertexType.FOOD_COUNTER)
    g.add_vertex("DRINKS", "Drinks Counter", VertexType.FOOD_COUNTER)
    g.add_vertex("COLLECTION", "Collection Counter", VertexType.COLLECTION)
    g.add_vertex("TABLES", "Dining Tables Area", VertexType.TABLES)
    g.add_vertex("EXIT", "Canteen Exit", VertexType.EXIT)

    # Add Movement Edges with walking/waiting times in minutes
    # Entrance -> Billing
    g.add_edge("ENTRANCE", "BILLING", weight=1.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    
    # Billing -> Food Counters
    g.add_edge("BILLING", "CHICKEN", weight=3.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("BILLING", "BIRYANI", weight=5.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("BILLING", "PUFFS", weight=2.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("BILLING", "DRINKS", weight=4.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)

    # Food Counters -> Collection Counter
    g.add_edge("CHICKEN", "COLLECTION", weight=3.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("BIRYANI", "COLLECTION", weight=2.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("PUFFS", "COLLECTION", weight=1.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("DRINKS", "COLLECTION", weight=2.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)

    # Collection -> Tables & Exit
    g.add_edge("COLLECTION", "TABLES", weight=2.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("TABLES", "EXIT", weight=1.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)
    g.add_edge("COLLECTION", "EXIT", weight=3.0, weight_meaning=EdgeWeightMeaning.WALKING_TIME_MINS)

    return g


def create_canteen_flow_network() -> Graph:
    """
    Directed flow network of the canteen (edge weight = capacity in students/min).
    Students flow: Entrance -> Billing -> Food Counters -> Collection -> (Tables ->) Exit.
    Used by Problem G9 (Max-Flow / Min-Cut).
    """
    g = Graph(is_directed=True)
    for v in create_default_canteen_graph().get_all_vertices():
        g.add_vertex(v.id, v.name, v.type)

    cap = EdgeWeightMeaning.CAPACITY_STUDENTS_PER_MIN
    g.add_edge("ENTRANCE", "BILLING", 20, cap)
    g.add_edge("BILLING", "CHICKEN", 6, cap)
    g.add_edge("BILLING", "BIRYANI", 5, cap)
    g.add_edge("BILLING", "PUFFS", 8, cap)
    g.add_edge("BILLING", "DRINKS", 7, cap)
    g.add_edge("CHICKEN", "COLLECTION", 5, cap)
    g.add_edge("BIRYANI", "COLLECTION", 4, cap)
    g.add_edge("PUFFS", "COLLECTION", 8, cap)
    g.add_edge("DRINKS", "COLLECTION", 6, cap)
    g.add_edge("COLLECTION", "TABLES", 10, cap)
    g.add_edge("TABLES", "EXIT", 8, cap)
    g.add_edge("COLLECTION", "EXIT", 9, cap)
    return g
