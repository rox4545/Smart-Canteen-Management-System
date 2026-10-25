from typing import Dict, List, Optional, Tuple
from dsa.graph import Graph, create_default_canteen_graph, create_canteen_flow_network
from dsa.supporting_dsa import (
    FIFOQueue, PriorityQueue, HashTable, InventoryManager, TableScheduler,
    ReadyOrderTimeoutManager, DemandTracker
)
from dsa.graph_algorithms import (
    bfs_shortest_path, dijkstra_shortest_path, dfs_reachability,
    find_connected_components, topological_sort, detect_cycle_directed,
    kruskal_mst, prim_mst, simulate_parallel_kitchen_tasks,
    edmonds_karp_max_flow, find_articulation_points_and_bridges
)


class Order:
    def __init__(self, token: str, student_name: str, item_ids: List[str], is_vip: bool = False, timestamp: float = 0.0):
        self.token: str = token
        self.student_name: str = student_name
        self.item_ids: List[str] = item_ids
        self.is_vip: bool = is_vip
        self.timestamp: float = timestamp
        self.status: str = "PLACED" 

    def __repr__(self) -> str:
        vip_str = "[VIP] " if self.is_vip else ""
        return f"Order({vip_str}Token={self.token}, Student={self.student_name}, Items={self.item_ids}, Status={self.status})"


class CanteenSystem:

    def __init__(self):

        self.graph: Graph = create_default_canteen_graph()

        self.inventory: InventoryManager = InventoryManager()
        self.token_table: HashTable[str, Order] = HashTable(capacity=67)
        self.normal_order_queue: FIFOQueue[Order] = FIFOQueue()
        self.vip_order_queue: PriorityQueue[Order] = PriorityQueue()  
        self.table_scheduler: TableScheduler = TableScheduler(num_tables=6)
        self.ready_timeout_mgr: ReadyOrderTimeoutManager = ReadyOrderTimeoutManager()
        self.demand_tracker: DemandTracker = DemandTracker()

        self._token_counter: int = 100
        self._seed_default_inventory()

    def _seed_default_inventory(self):

        self.inventory.add_item("CHK_BIRYANI", "Chicken Biryani", 180.0, 25, "BIRYANI")
        self.inventory.add_item("VEG_BIRYANI", "Veg Biryani", 140.0, 20, "BIRYANI")
        self.inventory.add_item("EGG_PUFF", "Egg Puff", 25.0, 40, "PUFFS")
        self.inventory.add_item("VEG_PUFF", "Veg Puff", 20.0, 50, "PUFFS")
        self.inventory.add_item("CHK_ROLL", "Chicken Roll", 70.0, 15, "CHICKEN")
        self.inventory.add_item("CHK_65", "Chicken 65", 120.0, 15, "CHICKEN")
        self.inventory.add_item("MANGO_LUSSI", "Mango Lassi", 40.0, 30, "DRINKS")
        self.inventory.add_item("COLD_COFFEE", "Cold Coffee", 50.0, 30, "DRINKS")

    def create_order(self, student_name: str, item_ids: List[str], is_vip: bool = False, current_time: float = 0.0) -> Tuple[bool, str, Optional[Order]]:

        success, msg = self.inventory.process_order_inventory(item_ids)
        if not success:
            return False, f"Order Rejected: {msg}", None

        self._token_counter += 1
        token = f"TK-{self._token_counter}"
        order = Order(token, student_name, item_ids, is_vip, current_time)

        self.token_table.put(token, order)

        for item_id in item_ids:
            self.demand_tracker.record_order(item_id)

        if is_vip:
            self.vip_order_queue.push(current_time, order)
            queue_type = "VIP Priority Queue"
        else:
            self.normal_order_queue.enqueue(order)
            queue_type = "FIFO Normal Queue"

        return True, f"Order placed successfully! Generated Token [{token}]. Enqueued into {queue_type}.", order

    def process_next_order_kitchen(self, current_time: float = 0.0) -> Tuple[bool, str, Optional[Dict]]:

        order: Optional[Order] = None

        if not self.vip_order_queue.is_empty():
            pop_res = self.vip_order_queue.pop()
            if pop_res:
                _, order = pop_res
        elif not self.normal_order_queue.is_empty():
            order = self.normal_order_queue.dequeue()

        if not order:
            return False, "No pending orders in queue.", None

        order.status = "PREPARING"

        items_by_counter: Dict[str, List[str]] = {}
        for item_id in order.item_ids:
            food = self.inventory.get_item(item_id)
            if food:
                c_id = food.counter_id
                if c_id not in items_by_counter:
                    items_by_counter[c_id] = []
                items_by_counter[c_id].append(food.name)

        parallel_res = simulate_parallel_kitchen_tasks(order.token, items_by_counter)
        completion_time = current_time + parallel_res["parallel_completion_time_mins"]

        order.status = "READY"
        ready_item_names = [self.inventory.get_item(iid).name for iid in order.item_ids if self.inventory.get_item(iid)]
        self.ready_timeout_mgr.add_ready_order(order.token, order.student_name, ready_item_names, completion_time, timeout_mins=10.0)

        return True, f"Order [{order.token}] prepared in parallel! Ready for collection at T+{completion_time} mins.", parallel_res

    def collect_order(self, token: str, current_time: float = 0.0) -> Tuple[bool, str]:

        self.ready_timeout_mgr.check_expired_orders(current_time)
        return self.ready_timeout_mgr.collect_order(token)

    def find_counter_route_bfs(self, start_id: str, dest_id: str) -> Dict:
        dist, path, trace = bfs_shortest_path(self.graph, start_id, dest_id)
        return {
            "algorithm": "BFS",
            "source": start_id,
            "destination": dest_id,
            "movement_count": dist,
            "path": path,
            "trace": trace
        }

    def find_fastest_route_dijkstra(self, start_id: str, dest_id: str) -> Dict:
        dist, path, trace = dijkstra_shortest_path(self.graph, start_id, dest_id)
        return {
            "algorithm": "Dijkstra",
            "source": start_id,
            "destination": dest_id,
            "total_time_mins": dist,
            "path": path,
            "trace": trace
        }

    def check_reachability(self, start_id: str, required_counters: List[str]) -> Dict:
        all_reachable, reachable, unreachable = dfs_reachability(self.graph, start_id, required_counters)
        return {
            "all_reachable": all_reachable,
            "reachable": reachable,
            "unreachable": unreachable
        }

    def check_disconnected_sections(self) -> Dict:
        num_comp, comp_list = find_connected_components(self.graph)
        return {
            "num_components": num_comp,
            "components": comp_list
        }

    def compute_workflow_topo_sort(self, workflow_dag: Graph) -> Dict:
        valid, order, msg = topological_sort(workflow_dag)
        return {
            "is_valid": valid,
            "topological_sequence": order,
            "message": msg
        }

    def check_circular_dependencies(self, workflow_graph: Graph) -> Dict:
        has_cycle, cycle_nodes = detect_cycle_directed(workflow_graph)
        return {
            "has_cycle": has_cycle,
            "cycle_nodes": cycle_nodes,
            "status": "INVALID CIRCULAR WORKFLOW DETECTED!" if has_cycle else "VALID ACYCLIC WORKFLOW"
        }

    def compute_network_mst(self) -> Dict:
        k_cost, k_edges = kruskal_mst(self.graph)
        p_cost, p_edges = prim_mst(self.graph, "BILLING")
        return {
            "kruskal_total_cost": k_cost,
            "kruskal_edges": [(e.source, e.destination, e.weight) for e in k_edges],
            "prim_total_cost": p_cost,
            "prim_edges": [(e.source, e.destination, e.weight) for e in p_edges]
        }

    def analyze_throughput_bottleneck(self, source: str = "ENTRANCE", sink: str = "EXIT") -> Dict:
        flow_net = create_canteen_flow_network()
        return edmonds_karp_max_flow(flow_net, source, sink)

    def analyze_critical_counters(self) -> Dict:
        points, bridges, table = find_articulation_points_and_bridges(self.graph)
        impact = {}
        for p in points:
            n_comp, comps = find_connected_components(self.graph.without_vertex(p))
            impact[p] = {"components_after_closure": n_comp, "sections": comps}
        return {
            "articulation_points": points,
            "bridges": bridges,
            "closure_impact": impact,
            "low_link_table": table
        }
