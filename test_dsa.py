


import sys
import unittest
from dsa.graph import Graph, VertexType, EdgeWeightMeaning, create_default_canteen_graph, create_canteen_flow_network
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
from dsa.canteen_system import CanteenSystem


class TestCanteenDSA(unittest.TestCase):

    def setUp(self):
        self.system = CanteenSystem()
        self.graph = self.system.graph

    
    def test_G1_bfs_shortest_path(self):
        """Problem G1: Unweighted BFS minimum movement path."""
        dist, path, trace = bfs_shortest_path(self.graph, "BILLING", "COLLECTION")
        self.assertEqual(dist, 2) 
        self.assertIn("BILLING", path)
        self.assertIn("COLLECTION", path)
        print(f"[PASS] G1 Passed: BFS path Billing->Collection = {path} (Dist={dist} edges)")

    def test_G2_dijkstra_shortest_path(self):
        """Problem G2: Weighted Dijkstra fastest route."""
        time_mins, path, trace = dijkstra_shortest_path(self.graph, "BILLING", "COLLECTION")
       
        self.assertEqual(time_mins, 3.0)
        self.assertEqual(path, ["BILLING", "PUFFS", "COLLECTION"])
        print(f"[PASS] G2 Passed: Dijkstra fastest route Billing->Collection = {path} ({time_mins} mins)")

    def test_G3_dfs_reachability(self):
        """Problem G3: DFS Counter Reachability."""
        required = ["CHICKEN", "BIRYANI", "PUFFS", "DRINKS", "COLLECTION"]
        all_reachable, reachable, unreachable = dfs_reachability(self.graph, "BILLING", required)
        self.assertTrue(all_reachable)
        self.assertEqual(len(unreachable), 0)
        print(f"[PASS] G3 Passed: All required counters {reachable} are reachable from Billing")

    def test_G4_connected_components(self):
        """Problem G4: Connected Components in graph."""
        num_comp, components = find_connected_components(self.graph)
        self.assertEqual(num_comp, 1)  
        
        self.graph.add_vertex("NEW_ANNEX", "Annex Counter", VertexType.FOOD_COUNTER)
        num_comp2, components2 = find_connected_components(self.graph)
        self.assertEqual(num_comp2, 2)
        print(f"[PASS] G4 Passed: Connected components detected correctly (Single={num_comp}, Disconnected={num_comp2})")

    def test_G5_topological_sort(self):
        """Problem G5: Topological Sort for DAG order workflow."""
        workflow = Graph(is_directed=True)
        workflow.add_vertex("ORDER", "Place Order", VertexType.BILLING)
        workflow.add_vertex("PAYMENT", "Payment", VertexType.BILLING)
        workflow.add_vertex("PREP", "Preparation", VertexType.FOOD_COUNTER)
        workflow.add_vertex("READY", "Food Ready", VertexType.COLLECTION)
        workflow.add_vertex("COLLECT", "Collection", VertexType.COLLECTION)

        workflow.add_edge("ORDER", "PAYMENT")
        workflow.add_edge("PAYMENT", "PREP")
        workflow.add_edge("PREP", "READY")
        workflow.add_edge("READY", "COLLECT")

        valid, seq, msg = topological_sort(workflow)
        self.assertTrue(valid)
        self.assertEqual(seq, ["ORDER", "PAYMENT", "PREP", "READY", "COLLECT"])
        print(f"[PASS] G5 Passed: Topological sort valid sequence = {' -> '.join(seq)}")

    def test_G6_cycle_detection(self):
        """Problem G6: Cycle detection in directed workflow."""
        cyclic_workflow = Graph(is_directed=True)
        cyclic_workflow.add_vertex("PAYMENT", "Payment", VertexType.BILLING)
        cyclic_workflow.add_vertex("PREP", "Preparation", VertexType.FOOD_COUNTER)
        cyclic_workflow.add_vertex("COLLECT", "Collection", VertexType.COLLECTION)

 
        cyclic_workflow.add_edge("PAYMENT", "PREP")
        cyclic_workflow.add_edge("PREP", "COLLECT")
        cyclic_workflow.add_edge("COLLECT", "PAYMENT")

        has_cycle, cycle_nodes = detect_cycle_directed(cyclic_workflow)
        self.assertTrue(has_cycle)
        self.assertGreater(len(cycle_nodes), 0)
        print(f"[PASS] G6 Passed: Invalid circular workflow detected: {cycle_nodes}")

    def test_G7_minimum_spanning_tree(self):
        """Problem G7: Prim and Kruskal Minimum Spanning Tree."""
        k_cost, k_edges = kruskal_mst(self.graph)
        p_cost, p_edges = prim_mst(self.graph, "BILLING")
        self.assertAlmostEqual(k_cost, p_cost)
        print(f"[PASS] G7 Passed: Kruskal MST cost = {k_cost}, Prim MST cost = {p_cost} (Identical Cost!)")

    def test_G8_parallel_kitchen_tasks(self):
        """Problem G8: Parallel Food Preparation Simulator."""
        items = {
            "CHICKEN": ["Chicken Roll"],
            "BIRYANI": ["Chicken Biryani"],
            "PUFFS": ["Egg Puff"],
            "DRINKS": ["Cold Coffee"]
        }
        res = simulate_parallel_kitchen_tasks("TK-999", items)
        self.assertEqual(res["parallel_completion_time_mins"], 10.0)  
        self.assertEqual(res["sequential_completion_time_mins"], 21.0) 
        self.assertEqual(res["time_saved_mins"], 11.0)
        print(f"[PASS] G8 Passed: Parallel preparation completed in {res['parallel_completion_time_mins']} mins vs {res['sequential_completion_time_mins']} mins sequential (Saved {res['time_saved_mins']} mins!)")

    def test_G9_max_flow_min_cut(self):
        """Problem G9: Edmonds-Karp max throughput and min-cut bottleneck."""
        res = self.system.analyze_throughput_bottleneck("ENTRANCE", "EXIT")
        self.assertEqual(res["max_flow"], 17.0)
        
        self.assertEqual(sum(c for _, _, c in res["min_cut_edges"]), res["max_flow"])
        self.assertEqual({(u, v) for u, v, _ in res["min_cut_edges"]},
                         {("COLLECTION", "EXIT"), ("TABLES", "EXIT")})
        
        net = create_canteen_flow_network()
        for node in net.vertices:
            if node in ("ENTRANCE", "EXIT"):
                continue
            inflow = sum(f for u, v, f, c in res["edge_flows"] if v == node)
            outflow = sum(f for u, v, f, c in res["edge_flows"] if u == node)
            self.assertAlmostEqual(inflow, outflow)
        
        self.assertEqual(edmonds_karp_max_flow(net, "ENTRANCE", "NOPE")["max_flow"], 0.0)
        self.assertEqual(edmonds_karp_max_flow(net, "EXIT", "EXIT")["max_flow"], 0.0)
        print(f"[PASS] G9 Passed: Max throughput = {res['max_flow']} students/min, bottleneck = {res['min_cut_edges']}")

    def test_G10_articulation_points_and_bridges(self):
        """Problem G10: Tarjan critical counters and corridors."""
        res = self.system.analyze_critical_counters()
        self.assertEqual(res["articulation_points"], ["BILLING", "COLLECTION"])
        self.assertEqual(res["bridges"], [("ENTRANCE", "BILLING")])
 
        for node, info in res["closure_impact"].items():
            self.assertEqual(info["components_after_closure"], 2)
       
        n, _ = find_connected_components(self.graph.without_vertex("CHICKEN"))
        self.assertEqual(n, 1)

        line = Graph(is_directed=False)
        for v in "ABC":
            line.add_vertex(v, v, VertexType.FOOD_COUNTER)
        line.add_edge("A", "B")
        line.add_edge("B", "C")
        pts, brs, _ = find_articulation_points_and_bridges(line)
        self.assertEqual(pts, ["B"])
        self.assertEqual(len(brs), 2)
        print(f"[PASS] G10 Passed: Critical counters = {res['articulation_points']}, bridges = {res['bridges']}")

   
    def test_S1_queue_and_hashtable(self):
        """Problem S1: FIFO Queue, Priority Queue, and Hash Table lookup."""
        ht = HashTable[str, str]()
        ht.put("TK-101", "Manoj - Biryani")
        self.assertEqual(ht.get("TK-101"), "Manoj - Biryani")

        fq = FIFOQueue[str]()
        fq.enqueue("Normal Student 1")
        fq.enqueue("Normal Student 2")
        self.assertEqual(fq.dequeue(), "Normal Student 1")

        pq = PriorityQueue[str]()
        pq.push(2.0, "Regular Order")
        pq.push(1.0, "VIP Order")
        self.assertEqual(pq.pop()[1], "VIP Order") 
        print("[PASS] S1 Passed: FIFO Queue, Priority Queue, and Hash Table operating correctly.")

    def test_S2_inventory_manager(self):
        """Problem S2: Inventory stock searching & decrement."""
        inv = self.system.inventory
        food = inv.get_item("CHK_BIRYANI")
        self.assertIsNotNone(food)
        initial_qty = food.quantity

        succ, msg, order = self.system.create_order("Test Student", ["CHK_BIRYANI"])
        self.assertTrue(succ)
        self.assertEqual(food.quantity, initial_qty - 1)
        print(f"[PASS] S2 Passed: Inventory item stock decremented from {initial_qty} to {food.quantity}")

    def test_S3_table_scheduler(self):
        """Problem S3: Table Allocation & Interval Scheduling."""
        ts = TableScheduler(num_tables=2)
        allocated1, msg1 = ts.allocate_table("TK-101", duration_mins=10, current_time=0)
        allocated2, msg2 = ts.allocate_table("TK-102", duration_mins=15, current_time=0)
        allocated3, msg3 = ts.allocate_table("TK-103", duration_mins=10, current_time=0)

        self.assertTrue(allocated1)
        self.assertTrue(allocated2)
        self.assertFalse(allocated3) 
        self.assertEqual(ts.waiting_queue.size(), 1)

        
        released, rel_msg = ts.release_table("T1", current_time=5)
        self.assertTrue(released)
        self.assertEqual(ts.tables["T1"].current_token, "TK-103")
        print(f"[PASS] S3 Passed: Table interval scheduling & waiting queue transition verified.")

    def test_S4_ready_order_timeout(self):
        """Problem S4: Ready Order Deadline Timeout Expiry."""
        mgr = ReadyOrderTimeoutManager()
        mgr.add_ready_order("TK-201", "Alex", ["Veg Puff"], current_time=0.0, timeout_mins=5.0)

        
        collected, c_msg = mgr.collect_order("TK-201")
        self.assertTrue(collected)

        
        mgr.add_ready_order("TK-202", "Sam", ["Cold Coffee"], current_time=0.0, timeout_mins=5.0)
        expired = mgr.check_expired_orders(current_time=6.0)
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0].token, "TK-202")
        print("[PASS] S4 Passed: Order timeout deadline & expiration verified.")

    def test_S5_demand_frequency_tracking(self):
        """Problem S5: Dynamic Kitchen Priority based on demand frequency."""
        dt = DemandTracker()
        for _ in range(5):
            dt.record_order("CHK_BIRYANI")

        dt.record_order("VEG_PUFF") 

        prio_biryani = dt.get_dynamic_cooking_priority("CHK_BIRYANI", base_prep_time=10.0)
        prio_puff = dt.get_dynamic_cooking_priority("VEG_PUFF", base_prep_time=2.0)

        self.assertLess(prio_biryani, 10.0)  
        print(f"[PASS] S5 Passed: Dynamic cooking priority adjusted: Biryani score = {prio_biryani} (High demand priority boost!)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
