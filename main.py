
import sys
import time
from dsa.graph import Graph, VertexType, EdgeWeightMeaning, create_default_canteen_graph
from dsa.canteen_system import CanteenSystem
from dsa.graph_algorithms import simulate_parallel_kitchen_tasks


def print_banner():
    print("=" * 72)
    print("      CANTEEN MANAGEMENT SYSTEM — DATA STRUCTURES & ALGORITHMS      ")
    print("=" * 72)
    print(" Primary Focus: Graph Algorithms | Supporting DSA: Queue, MinHeap, Hash Table")
    print("=" * 72)


def print_menu():
    print("\n--- MAIN ALGORITHM & FEATURE MENU ---")
    print(" [1] View Central Canteen Graph (Adjacency List)")
    print(" [2] G1: Minimum Movements Route (BFS)")
    print(" [3] G2: Fastest Route - Walking & Waiting Time Optimization (Dijkstra)")
    print(" [4] G3: Check Counter Reachability (DFS)")
    print(" [5] G4: Detect Disconnected Canteen Sections (Connected Components)")
    print(" [6] G5: Order Workflow Dependency Ordering (Topological Sort)")
    print(" [7] G6: Detect Invalid Circular Workflows (Cycle Detection)")
    print(" [8] G7: Minimum-Cost Infrastructure Network (Prim & Kruskal MST)")
    print(" [9] G8: Parallel Food Counter Preparation Simulator (Dependency DAG)")
    print(" [10] S1-S5: Interactive Student Order, Inventory, Tables & Timeout Simulator")
    print(" [11] G9: Peak Throughput & Bottleneck (Max-Flow / Min-Cut, Edmonds-Karp)")
    print(" [12] G10: Critical Counters & Corridors (Tarjan Articulation Points & Bridges)")
    print(" [13] Run Complete Automated Test Suite (15 DSA Tests)")
    print(" [0] Exit Application")
    print("-" * 72)


def run_interactive_cli():
    system = CanteenSystem()

    while True:
        print_banner()
        print_menu()
        choice = input("Select an option (0-13): ").strip()

        if choice == "0":
            print("\nExiting Canteen Management System. Thank you!")
            break

        elif choice == "1":
            print("\n" + system.graph.print_adjacency_list())

        elif choice == "2":
            print("\n--- G1: BREADTH-FIRST SEARCH (BFS) ---")
            start = input("Enter Source Vertex (default 'BILLING'): ").strip().upper() or "BILLING"
            dest = input("Enter Destination Vertex (default 'COLLECTION'): ").strip().upper() or "COLLECTION"
            
            res = system.find_counter_route_bfs(start, dest)
            print(f"\n[BFS RESULT]")
            print(f" Source: {res['source']} -> Destination: {res['destination']}")
            print(f" Minimum Movements (Edges): {res['movement_count']}")
            print(f" Optimal Counter Path: {' -> '.join(res['path'])}")
            print("\nStep-by-step Queue Trace:")
            for t in res["trace"]:
                print(f"  Step {t['step']}: Evaluated Node = {t['current_vertex']} | Visited = {t['visited_set']} | Queue = {t['queue_state']}")

        elif choice == "3":
            print("\n--- G2: DIJKSTRA'S SHORTEST PATH (FASTEST ROUTE) ---")
            start = input("Enter Source Vertex (default 'BILLING'): ").strip().upper() or "BILLING"
            dest = input("Enter Destination Vertex (default 'COLLECTION'): ").strip().upper() or "COLLECTION"
            
            res = system.find_fastest_route_dijkstra(start, dest)
            print(f"\n[DIJKSTRA RESULT]")
            print(f" Source: {res['source']} -> Destination: {res['destination']}")
            print(f" Minimum Total Time: {res['total_time_mins']} minutes")
            print(f" Fastest Route Path: {' -> '.join(res['path'])}")
            print("\nStep-by-step MinHeap Distance Relaxation:")
            for t in res["trace"]:
                print(f"  Step {t['step']}: Evaluated Node = {t['evaluated_vertex']} (Min Dist={t['known_distance']} mins)")

        elif choice == "4":
            print("\n--- G3: DFS REACHABILITY CHECK ---")
            start = input("Enter Source Vertex (default 'BILLING'): ").strip().upper() or "BILLING"
            counters = ["CHICKEN", "BIRYANI", "PUFFS", "DRINKS", "COLLECTION"]
            res = system.check_reachability(start, counters)
            print(f"\nReachability from {start}:")
            print(f" All Counters Reachable? {res['all_reachable']}")
            print(f" Reachable Counters: {res['reachable']}")
            print(f" Unreachable Counters: {res['unreachable']}")

        elif choice == "5":
            print("\n--- G4: CONNECTED COMPONENTS ---")
            res = system.check_disconnected_sections()
            print(f"\nTotal Independent Sections: {res['num_components']}")
            for idx, comp in enumerate(res['components'], 1):
                print(f" Section #{idx}: {comp}")

        elif choice == "6":
            print("\n--- G5: TOPOLOGICAL SORTING (WORKFLOW DAG) ---")
            wf = Graph(is_directed=True)
            wf.add_vertex("ORDER", "Place Order", VertexType.BILLING)
            wf.add_vertex("PAYMENT", "Payment Counter", VertexType.BILLING)
            wf.add_vertex("PREPARATION", "Food Preparation", VertexType.FOOD_COUNTER)
            wf.add_vertex("FOOD_READY", "Food Ready Signal", VertexType.COLLECTION)
            wf.add_vertex("COLLECTION", "Student Collection", VertexType.COLLECTION)

            wf.add_edge("ORDER", "PAYMENT")
            wf.add_edge("PAYMENT", "PREPARATION")
            wf.add_edge("PREPARATION", "FOOD_READY")
            wf.add_edge("FOOD_READY", "COLLECTION")

            res = system.compute_workflow_topo_sort(wf)
            print(f"\n{res['message']}")
            print(f"Valid Sequence: {' -> '.join(res['topological_sequence'])}")

        elif choice == "7":
            print("\n--- G6: CYCLE DETECTION (INVALID WORKFLOW CHECK) ---")
            bad_wf = Graph(is_directed=True)
            bad_wf.add_vertex("PAYMENT", "Payment", VertexType.BILLING)
            bad_wf.add_vertex("PREPARATION", "Preparation", VertexType.FOOD_COUNTER)
            bad_wf.add_vertex("COLLECTION", "Collection", VertexType.COLLECTION)
            bad_wf.add_edge("PAYMENT", "PREPARATION")
            bad_wf.add_edge("PREPARATION", "COLLECTION")
            bad_wf.add_edge("COLLECTION", "PAYMENT")  # Circular link!

            res = system.check_circular_dependencies(bad_wf)
            print(f"\nWorkflow Status: {res['status']}")
            print(f"Cycle Nodes Detected: {res['cycle_nodes']}")

        elif choice == "8":
            print("\n--- G7: MINIMUM SPANNING TREE (PRIM & KRUSKAL MST) ---")
            res = system.compute_network_mst()
            print(f"\n[KRUSKAL MST] Total Cost = {res['kruskal_total_cost']}")
            for e in res['kruskal_edges']:
                print(f"  Connection: {e[0]} <---> {e[1]} (Cost={e[2]})")

            print(f"\n[PRIM MST] Total Cost = {res['prim_total_cost']}")
            for e in res['prim_edges']:
                print(f"  Connection: {e[0]} <---> {e[1]} (Cost={e[2]})")

        elif choice == "9":
            print("\n--- G8: PARALLEL FOOD COUNTER PREPARATION SIMULATOR ---")
            items = {
                "CHICKEN": ["Chicken Roll", "Chicken 65"],
                "BIRYANI": ["Chicken Biryani"],
                "PUFFS": ["Egg Puff"],
                "DRINKS": ["Cold Coffee"]
            }
            res = simulate_parallel_kitchen_tasks("TK-501", items)
            print(f"\nParallel Execution for Order #{res['order_id']}:")
            for b in res["parallel_branches"]:
                print(f"  Counter [{b['counter']}]: Preparing {b['items']} (Est Time: {b['prep_time_mins']} mins)")
            print(f"\nTotal Completion Time (Parallel): {res['parallel_completion_time_mins']} mins")
            print(f"Sequential Time (Old way): {res['sequential_completion_time_mins']} mins")
            print(f"Time Saved by Parallel Processing: {res['time_saved_mins']} mins!")

        elif choice == "10":
            print("\n--- S1-S5: INTERACTIVE CANTEEN ORDERING & TABLE SIMULATOR ---")
            print("\nStock Available:")
            for item in system.inventory.get_all_items():
                print(f"  - [{item.id}] {item.name} (Rs.{item.price}, Stock={item.quantity}, Counter={item.counter_id})")

            name = input("\nEnter Student Name: ").strip() or "Student User"
            is_vip_in = input("Is VIP Student Priority? (y/n): ").strip().lower() == 'y'
            item_choice = input("Enter Item IDs separated by comma (e.g. CHK_BIRYANI, COLD_COFFEE): ").strip()
            item_list = [i.strip().upper() for i in item_choice.split(",") if i.strip()] or ["CHK_BIRYANI", "COLD_COFFEE"]

            succ, msg, order = system.create_order(name, item_list, is_vip=is_vip_in, current_time=0.0)
            print(f"\n{msg}")

            if succ and order:
                print("\nProcessing kitchen preparation...")
                proc_succ, proc_msg, p_res = system.process_next_order_kitchen(current_time=0.0)
                print(f"{proc_msg}")

                # Table Allocation
                tb_succ, tb_msg = system.table_scheduler.allocate_table(order.token, duration_mins=15.0, current_time=0.0)
                print(f"Table Allocation: {tb_msg}")

                # Student Collects Order
                collect_succ, col_msg = system.collect_order(order.token, current_time=2.0)
                print(f"Collection Result: {col_msg}")

        elif choice == "11":
            print("\n--- G9: MAX-FLOW / MIN-CUT (EDMONDS-KARP) ---")
            res = system.analyze_throughput_bottleneck("ENTRANCE", "EXIT")
            print("\nAugmenting paths found (BFS shortest path in residual graph):")
            for i, a in enumerate(res["augmenting_paths"], 1):
                print(f"  #{i}: {' -> '.join(a['path'])} | +{a['bottleneck']} students/min | Total = {a['total_flow']}")
            print(f"\nMaximum Throughput: {res['max_flow']} students/min")
            print("\nFlow on each corridor (flow / capacity):")
            for u, v, f, c in res["edge_flows"]:
                print(f"  {u} -> {v}: {f}/{c}")
            print("\nBottleneck (Min-Cut) edges - widen these to increase throughput:")
            for u, v, c in res["min_cut_edges"]:
                print(f"  {u} -> {v} (capacity {c})")

        elif choice == "12":
            print("\n--- G10: ARTICULATION POINTS & BRIDGES (TARJAN) ---")
            res = system.analyze_critical_counters()
            print(f"\nCritical Counters (Articulation Points): {res['articulation_points']}")
            print(f"Critical Corridors (Bridges): {res['bridges']}")
            print("\nImpact of closing each critical counter (re-running G4):")
            for node, info in res["closure_impact"].items():
                print(f"  Close {node}: canteen splits into {info['components_after_closure']} sections -> {info['sections']}")
            print("\nDiscovery / Low-link table:")
            for v, t in res["low_link_table"].items():
                print(f"  {v}: disc={t['disc']}, low={t['low']}")

        elif choice == "13":
            print("\nExecuting complete unit test suite...")
            import test_dsa
            unittest = test_dsa.unittest
            suite = unittest.TestLoader().loadTestsFromModule(test_dsa)
            unittest.TextTestRunner(verbosity=2).run(suite)

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run_interactive_cli()
