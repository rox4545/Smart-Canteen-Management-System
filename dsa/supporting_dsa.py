"""
Supporting Data Structures & Algorithms for Canteen Management System.
Implements custom Queue, MinHeap Priority Queue, Hash Table, Inventory,
Interval Table Scheduler, Timeout Deadline Queue, and Demand Tracker.
"""

import time
from typing import Any, Dict, Generic, List, Optional, Tuple, TypeVar

K = TypeVar('K')
V = TypeVar('V')


# ==========================================
# 1. CUSTOM HASH TABLE (Problem S1, S2, S4)
# ==========================================
class HashNode(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key: K = key
        self.value: V = value
        self.next: Optional['HashNode[K, V]'] = None

class HashTable(Generic[K, V]):
    """Custom Separate Chaining Hash Table."""
    def __init__(self, capacity: int = 31):
        self.capacity: int = capacity
        self.size: int = 0
        self.buckets: List[Optional[HashNode[K, V]]] = [None] * self.capacity

    def _hash(self, key: K) -> int:
        return abs(hash(key)) % self.capacity

    def put(self, key: K, value: V) -> None:
        index = self._hash(key)
        head = self.buckets[index]
        curr = head
        while curr:
            if curr.key == key:
                curr.value = value
                return
            curr = curr.next
        
        new_node = HashNode(key, value)
        new_node.next = head
        self.buckets[index] = new_node
        self.size += 1

    def get(self, key: K) -> Optional[V]:
        index = self._hash(key)
        curr = self.buckets[index]
        while curr:
            if curr.key == key:
                return curr.value
            curr = curr.next
        return None

    def remove(self, key: K) -> bool:
        index = self._hash(key)
        curr = self.buckets[index]
        prev = None
        while curr:
            if curr.key == key:
                if prev:
                    prev.next = curr.next
                else:
                    self.buckets[index] = curr.next
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    def contains(self, key: K) -> bool:
        return self.get(key) is not None

    def keys(self) -> List[K]:
        all_keys = []
        for bucket in self.buckets:
            curr = bucket
            while curr:
                all_keys.append(curr.key)
                curr = curr.next
        return all_keys

    def values(self) -> List[V]:
        all_values = []
        for bucket in self.buckets:
            curr = bucket
            while curr:
                all_values.append(curr.value)
                curr = curr.next
        return all_values


# ==========================================
# 2. CUSTOM FIFO QUEUE (Problem S1, S3)
# ==========================================
class QueueNode(Generic[V]):
    def __init__(self, value: V):
        self.value: V = value
        self.next: Optional['QueueNode[V]'] = None

class FIFOQueue(Generic[V]):
    """Custom Linked-List FIFO Queue."""
    def __init__(self):
        self.head: Optional[QueueNode[V]] = None
        self.tail: Optional[QueueNode[V]] = None
        self._size: int = 0

    def enqueue(self, item: V) -> None:
        new_node = QueueNode(item)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def dequeue(self) -> Optional[V]:
        if not self.head:
            return None
        val = self.head.value
        self.head = self.head.next
        if not self.head:
            self.tail = None
        self._size -= 1
        return val

    def peek(self) -> Optional[V]:
        return self.head.value if self.head else None

    def is_empty(self) -> bool:
        return self._size == 0

    def size(self) -> int:
        return self._size

    def to_list(self) -> List[V]:
        res = []
        curr = self.head
        while curr:
            res.append(curr.value)
            curr = curr.next
        return res


# ==========================================
# 3. CUSTOM MIN-HEAP PRIORITY QUEUE (Problem S1, S4, S5)
# ==========================================
class PriorityQueueEntry(Generic[V]):
    def __init__(self, priority: float, data: V):
        self.priority: float = priority  # Lower number = Higher priority
        self.data: V = data

    def __lt__(self, other: 'PriorityQueueEntry[V]') -> bool:
        return self.priority < other.priority

class PriorityQueue(Generic[V]):
    """Custom Binary Min-Heap Priority Queue."""
    def __init__(self):
        self.heap: List[PriorityQueueEntry[V]] = []

    def push(self, priority: float, data: V) -> None:
        entry = PriorityQueueEntry(priority, data)
        self.heap.append(entry)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> Optional[Tuple[float, V]]:
        if not self.heap:
            return None
        self._swap(0, len(self.heap) - 1)
        min_entry = self.heap.pop()
        if self.heap:
            self._sift_down(0)
        return (min_entry.priority, min_entry.data)

    def peek(self) -> Optional[Tuple[float, V]]:
        if not self.heap:
            return None
        return (self.heap[0].priority, self.heap[0].data)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    def size(self) -> int:
        return len(self.heap)

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self._swap(idx, parent)
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx

            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            if smallest != idx:
                self._swap(idx, smallest)
                idx = smallest
            else:
                break

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def to_list(self) -> List[Tuple[float, V]]:
        return [(e.priority, e.data) for e in sorted(self.heap)]


# ==========================================
# 4. INVENTORY MANAGEMENT (Problem S2)
# ==========================================
class FoodItem:
    def __init__(self, item_id: str, name: str, price: float, initial_quantity: int, counter_id: str):
        self.id: str = item_id
        self.name: str = name
        self.price: float = price
        self.quantity: int = initial_quantity
        self.counter_id: str = counter_id
        self.status: str = "AVAILABLE" if initial_quantity > 0 else "FINISHED"

    def order_item(self, qty: int = 1) -> bool:
        if self.quantity >= qty:
            self.quantity -= qty
            if self.quantity == 0:
                self.status = "FINISHED"
            return True
        return False

    def restock(self, qty: int) -> None:
        self.quantity += qty
        if self.quantity > 0:
            self.status = "AVAILABLE"

    def __repr__(self) -> str:
        return f"FoodItem({self.name}, Stock={self.quantity}, Price=Rs.{self.price}, Status={self.status}, Counter={self.counter_id})"


class InventoryManager:
    """Manages canteen food inventory using custom Hash Table for O(1) lookup."""
    def __init__(self):
        self.items: HashTable[str, FoodItem] = HashTable(capacity=31)

    def add_item(self, item_id: str, name: str, price: float, quantity: int, counter_id: str) -> FoodItem:
        food = FoodItem(item_id, name, price, quantity, counter_id)
        self.items.put(item_id, food)
        return food

    def get_item(self, item_id: str) -> Optional[FoodItem]:
        return self.items.get(item_id)

    def check_availability(self, item_id: str, qty: int = 1) -> Tuple[bool, str]:
        food = self.get_item(item_id)
        if not food:
            return False, f"Item '{item_id}' not found in inventory."
        if food.quantity < qty:
            return False, f"Item '{food.name}' is OUT OF STOCK (Available: {food.quantity})."
        return True, f"Item '{food.name}' is available."

    def process_order_inventory(self, item_ids: List[str]) -> Tuple[bool, str]:
        # Validate all first
        for item_id in item_ids:
            avail, msg = self.check_availability(item_id)
            if not avail:
                return False, msg

        # Decrement stock
        for item_id in item_ids:
            food = self.get_item(item_id)
            if food:
                food.order_item(1)

        return True, "Inventory checked and stock reserved successfully."

    def get_all_items(self) -> List[FoodItem]:
        return self.items.values()


# ==========================================
# 5. TABLE MANAGEMENT & INTERVAL SCHEDULING (Problem S3)
# ==========================================
class DiningTable:
    def __init__(self, table_id: str, capacity: int = 4):
        self.id: str = table_id
        self.capacity: int = capacity
        self.is_occupied: bool = False
        self.current_token: Optional[str] = None
        self.occupied_until: float = 0.0  # Timestamp or minutes offset

class TableScheduler:
    """Manages table allocations and waiting queue using Interval Scheduling + Queue."""
    def __init__(self, num_tables: int = 6):
        self.tables: Dict[str, DiningTable] = {
            f"T{i+1}": DiningTable(f"T{i+1}") for i in range(num_tables)
        }
        self.waiting_queue: FIFOQueue[Dict[str, Any]] = FIFOQueue()

    def allocate_table(self, token: str, duration_mins: float = 15.0, current_time: float = 0.0) -> Tuple[bool, str]:
        # Auto release expired tables
        self.update_tables(current_time)

        for table_id, table in self.tables.items():
            if not table.is_occupied:
                table.is_occupied = True
                table.current_token = token
                table.occupied_until = current_time + duration_mins
                return True, f"Table {table_id} allocated for Token {token} until T+{table.occupied_until} mins."

        # No table free, enqueue student
        self.waiting_queue.enqueue({"token": token, "duration": duration_mins, "request_time": current_time})
        return False, f"All tables occupied. Token {token} added to table waiting queue (Position: {self.waiting_queue.size()})."

    def release_table(self, table_id: str, current_time: float = 0.0) -> Tuple[bool, str]:
        if table_id in self.tables and self.tables[table_id].is_occupied:
            freed_token = self.tables[table_id].current_token
            self.tables[table_id].is_occupied = False
            self.tables[table_id].current_token = None
            self.tables[table_id].occupied_until = 0.0

            # Assign to next waiting student
            msg = f"Table {table_id} freed from Token {freed_token}."
            if not self.waiting_queue.is_empty():
                next_waiter = self.waiting_queue.dequeue()
                self.tables[table_id].is_occupied = True
                self.tables[table_id].current_token = next_waiter["token"]
                self.tables[table_id].occupied_until = current_time + next_waiter["duration"]
                msg += f" Assigned immediately to waiting Token {next_waiter['token']}."
            return True, msg
        return False, f"Table {table_id} was already free."

    def update_tables(self, current_time: float) -> None:
        for t in self.tables.values():
            if t.is_occupied and current_time >= t.occupied_until:
                self.release_table(t.id, current_time)


# ==========================================
# 6. UNCOLLECTED READY-ORDER TIMEOUT SCHEDULER (Problem S4)
# ==========================================
class ReadyOrder:
    def __init__(self, token: str, student_name: str, items: List[str], ready_time: float, deadline_time: float):
        self.token: str = token
        self.student_name: str = student_name
        self.items: List[str] = items
        self.ready_time: float = ready_time
        self.deadline_time: float = deadline_time
        self.status: str = "READY"  # READY, COLLECTED, EXPIRED

class ReadyOrderTimeoutManager:
    """Manages order readiness deadlines using Priority Queue & Hash Table."""
    def __init__(self):
        self.ready_orders: HashTable[str, ReadyOrder] = HashTable()
        self.deadline_pq: PriorityQueue[str] = PriorityQueue()  # Priority = deadline_time, Data = token

    def add_ready_order(self, token: str, student_name: str, items: List[str], current_time: float, timeout_mins: float = 10.0) -> ReadyOrder:
        deadline = current_time + timeout_mins
        ro = ReadyOrder(token, student_name, items, current_time, deadline)
        self.ready_orders.put(token, ro)
        self.deadline_pq.push(deadline, token)
        return ro

    def collect_order(self, token: str) -> Tuple[bool, str]:
        ro = self.ready_orders.get(token)
        if not ro:
            return False, f"Token {token} not found in Ready Collection Queue."
        if ro.status == "EXPIRED":
            return False, f"Token {token} has EXPIRED! Food was discarded/reallocated as per canteen policy."
        if ro.status == "COLLECTED":
            return False, f"Token {token} has ALREADY been collected."

        ro.status = "COLLECTED"
        return True, f"Token {token} successfully collected by {ro.student_name}! Enjoy your meal."

    def check_expired_orders(self, current_time: float) -> List[ReadyOrder]:
        expired_list = []
        while not self.deadline_pq.is_empty():
            peek = self.deadline_pq.peek()
            if peek and peek[0] <= current_time:
                _, token = self.deadline_pq.pop()
                ro = self.ready_orders.get(token)
                if ro and ro.status == "READY":
                    ro.status = "EXPIRED"
                    expired_list.append(ro)
            else:
                break
        return expired_list


# ==========================================
# 7. HIGH DEMAND FREQUENCY COUNTING & DYNAMIC PRIORITY SCHEDULING (Problem S5)
# ==========================================
class DemandTracker:
    """Tracks order frequency in time windows to dynamically adjust cooking priority."""
    def __init__(self):
        self.frequency_table: HashTable[str, int] = HashTable()

    def record_order(self, item_id: str) -> None:
        curr_freq = self.frequency_table.get(item_id) or 0
        self.frequency_table.put(item_id, curr_freq + 1)

    def get_demand_count(self, item_id: str) -> int:
        return self.frequency_table.get(item_id) or 0

    def get_dynamic_cooking_priority(self, item_id: str, base_prep_time: float) -> float:
        """
        Dynamic Priority Formula:
        Priority Score = (Base Prep Time) / (1 + 0.5 * Frequency)
        Lower score = Higher cooking priority in Kitchen MinHeap.
        """
        freq = self.get_demand_count(item_id)
        priority_score = base_prep_time / (1 + 0.5 * freq)
        return round(priority_score, 2)
