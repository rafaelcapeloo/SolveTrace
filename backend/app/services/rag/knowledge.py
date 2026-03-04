"""
RAG Knowledge Base — algorithm patterns and techniques.
Seeded data for the ChromaDB vector store.
"""

ALGORITHM_PATTERNS = [
    {
        "id": "dp_basics",
        "title": "Dynamic Programming Fundamentals",
        "content": """Dynamic Programming (DP) is a technique for solving problems by breaking them into overlapping subproblems.

Key characteristics: Optimal substructure + Overlapping subproblems.
Approaches: Top-down (memoization) or Bottom-up (tabulation).

Template (bottom-up):
```python
dp = [base_case] * (n + 1)
for i in range(1, n + 1):
    dp[i] = transition(dp[i-1], ...)
return dp[n]
```

Common types: 1D DP, 2D DP, interval DP, bitmask DP, digit DP.
Time complexity usually O(n * states), Space O(states).""",
        "tags": ["dynamic_programming", "memoization", "tabulation"],
    },
    {
        "id": "two_pointers",
        "title": "Two Pointers Technique",
        "content": """Two pointers technique uses two indices to traverse a data structure, typically used on sorted arrays.

Types:
1. Opposite direction: left=0, right=n-1 (e.g., Two Sum on sorted array)
2. Same direction: slow/fast (e.g., removing duplicates, linked list cycle)
3. Sliding window variant: fixed/variable window

Template:
```python
left, right = 0, len(arr) - 1
while left < right:
    if condition: left += 1
    else: right -= 1
```

Time: O(n), Space: O(1). Works when problem has monotonic property.""",
        "tags": ["two_pointers", "array", "sorted"],
    },
    {
        "id": "binary_search",
        "title": "Binary Search and Variants",
        "content": """Binary search eliminates half the search space each step. Works on sorted/monotonic data.

Classic template:
```python
lo, hi = 0, n - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if arr[mid] == target: return mid
    elif arr[mid] < target: lo = mid + 1
    else: hi = mid - 1
```

Binary search on answer: When the answer has a monotonic property (if x works, all y > x work).
Key: Define a `check(mid)` predicate function.

Time: O(log n), Space: O(1).""",
        "tags": ["binary_search", "sorted", "search"],
    },
    {
        "id": "graph_bfs",
        "title": "BFS — Breadth-First Search",
        "content": """BFS explores nodes level by level using a queue. Ideal for shortest path in unweighted graphs.

Template:
```python
from collections import deque
queue = deque([start])
visited = {start}
dist = {start: 0}
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            visited.add(neighbor)
            dist[neighbor] = dist[node] + 1
            queue.append(neighbor)
```

Variants: Multi-source BFS, 0-1 BFS (deque with 0-weight and 1-weight edges).
Time: O(V + E), Space: O(V).""",
        "tags": ["graph", "bfs", "shortest_path", "queue"],
    },
    {
        "id": "graph_dfs",
        "title": "DFS — Depth-First Search",
        "content": """DFS explores as deep as possible before backtracking. Uses recursion or explicit stack.

Template (recursive):
```python
def dfs(node, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, visited)
```

Applications: Connected components, topological sort, cycle detection, bridge finding.
Time: O(V + E), Space: O(V) for recursion stack.""",
        "tags": ["graph", "dfs", "recursion", "backtracking"],
    },
    {
        "id": "sliding_window",
        "title": "Sliding Window Technique",
        "content": """Sliding window maintains a window [left, right] over a sequence, expanding/shrinking to find optimal subarray.

Fixed window:
```python
for i in range(n):
    window_sum += arr[i]
    if i >= k - 1:
        result = max(result, window_sum)
        window_sum -= arr[i - k + 1]
```

Variable window (shrink when condition violated):
```python
left = 0
for right in range(n):
    # expand: add arr[right]
    while condition_violated:
        # shrink: remove arr[left]
        left += 1
    result = max(result, right - left + 1)
```

Time: O(n), Space: O(1) or O(k).""",
        "tags": ["sliding_window", "array", "subarray", "two_pointers"],
    },
    {
        "id": "greedy",
        "title": "Greedy Algorithms",
        "content": """Greedy makes locally optimal choices hoping for global optimum. Must prove greedy choice property.

Common patterns:
1. Sort + sweep (interval scheduling, activity selection)
2. Priority queue (Huffman, meeting rooms)
3. Exchange argument (prove swapping doesn't help)

Template (interval scheduling):
```python
intervals.sort(key=lambda x: x[1])  # Sort by end time
end = -inf
count = 0
for start, finish in intervals:
    if start >= end:
        count += 1
        end = finish
```

Key: Always ask "Can I prove the greedy choice is safe?" """,
        "tags": ["greedy", "sorting", "optimization"],
    },
    {
        "id": "backtracking",
        "title": "Backtracking",
        "content": """Backtracking explores all possibilities by making choices and undoing them (backtracking) when a dead end is reached.

Template:
```python
def backtrack(state, choices):
    if is_solution(state):
        results.append(state.copy())
        return
    for choice in choices:
        if is_valid(state, choice):
            state.add(choice)
            backtrack(state, remaining_choices)
            state.remove(choice)  # undo
```

Optimization: Pruning — skip branches that can't lead to valid solutions.
Applications: N-Queens, Sudoku, permutations, combinations, subsets.
Time: Usually exponential O(k^n) or O(n!), but pruning helps.""",
        "tags": ["backtracking", "recursion", "brute_force", "pruning"],
    },
    {
        "id": "divide_conquer",
        "title": "Divide and Conquer",
        "content": """Divide and Conquer splits a problem into smaller subproblems, solves them independently, and combines results.

Template:
```python
def solve(arr, lo, hi):
    if lo == hi: return base_case(arr[lo])
    mid = (lo + hi) // 2
    left_result = solve(arr, lo, mid)
    right_result = solve(arr, mid + 1, hi)
    return combine(left_result, right_result)
```

Classic examples: Merge sort, quicksort, closest pair of points, Karatsuba multiplication.
Master theorem: T(n) = aT(n/b) + O(n^d).""",
        "tags": ["divide_and_conquer", "recursion", "merge_sort"],
    },
    {
        "id": "union_find",
        "title": "Union-Find (Disjoint Set Union)",
        "content": """Union-Find tracks equivalence classes / connected components efficiently.

Template:
```python
parent = list(range(n))
rank = [0] * n

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]

def union(x, y):
    px, py = find(x), find(y)
    if px == py: return False
    if rank[px] < rank[py]: px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]: rank[px] += 1
    return True
```

Applications: Kruskal's MST, cycle detection, connected components.
Time: Nearly O(1) amortized per operation (inverse Ackermann).""",
        "tags": ["union_find", "dsu", "graph", "connected_components"],
    },
    {
        "id": "trie",
        "title": "Trie (Prefix Tree)",
        "content": """A Trie stores strings for efficient prefix-based operations.

Template:
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True

    def search(self, word):
        node = self.root
        for c in word:
            if c not in node.children: return False
            node = node.children[c]
        return node.is_end
```

Applications: Autocomplete, spell checking, XOR problems.
Time: O(L) per operation where L = string length.""",
        "tags": ["trie", "string", "prefix"],
    },
    {
        "id": "segment_tree",
        "title": "Segment Tree",
        "content": """Segment Tree handles range queries and point/range updates efficiently.

Build: O(n), Query: O(log n), Update: O(log n).

Applications: Range sum/min/max, lazy propagation for range updates.
Variants: Persistent segment tree, 2D segment tree, merge sort tree.

Key insight: Each node represents a range of the array. Children split the range in half.""",
        "tags": ["segment_tree", "range_query", "data_structure"],
    },
    {
        "id": "monotonic_stack",
        "title": "Monotonic Stack",
        "content": """Monotonic stack maintains elements in increasing/decreasing order. Useful for "next greater/smaller element" problems.

Template (next greater element):
```python
stack = []
result = [-1] * n
for i in range(n):
    while stack and arr[stack[-1]] < arr[i]:
        result[stack.pop()] = arr[i]
    stack.append(i)
```

Applications: Histogram area, stock span, trapping rain water.
Time: O(n), Space: O(n).""",
        "tags": ["monotonic_stack", "stack", "array"],
    },
    {
        "id": "topological_sort",
        "title": "Topological Sort",
        "content": """Topological sort orders vertices of a DAG such that for every edge u→v, u comes before v.

Kahn's Algorithm (BFS-based):
```python
from collections import deque
in_degree = [0] * n
for u in graph:
    for v in graph[u]:
        in_degree[v] += 1
queue = deque(v for v in range(n) if in_degree[v] == 0)
order = []
while queue:
    u = queue.popleft()
    order.append(u)
    for v in graph[u]:
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
```

If len(order) < n, the graph has a cycle.
Applications: Task scheduling, course prerequisites, build systems.""",
        "tags": ["topological_sort", "graph", "dag", "bfs"],
    },
    {
        "id": "dijkstra",
        "title": "Dijkstra's Shortest Path",
        "content": """Dijkstra finds shortest paths from a source in a weighted graph with non-negative edges.

Template:
```python
import heapq
dist = [float('inf')] * n
dist[source] = 0
pq = [(0, source)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue
    for v, w in graph[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(pq, (dist[v], v))
```

Time: O((V + E) log V) with binary heap.
Doesn't work with negative edges — use Bellman-Ford instead.""",
        "tags": ["dijkstra", "graph", "shortest_path", "priority_queue"],
    },
    {
        "id": "bit_manipulation",
        "title": "Bit Manipulation",
        "content": """Bit manipulation uses bitwise operators for efficient computation.

Key operations:
- Check bit i: `(n >> i) & 1`
- Set bit i: `n | (1 << i)`
- Clear bit i: `n & ~(1 << i)`
- Toggle bit i: `n ^ (1 << i)`
- Count bits: `bin(n).count('1')`
- Lowest set bit: `n & (-n)`
- Remove lowest set bit: `n & (n - 1)`

Applications: Bitmask DP, subset enumeration, XOR tricks.
XOR properties: a ^ a = 0, a ^ 0 = a, commutative + associative.""",
        "tags": ["bit_manipulation", "bitmask", "xor"],
    },
    {
        "id": "prefix_sum",
        "title": "Prefix Sum",
        "content": """Prefix sum enables O(1) range sum queries after O(n) preprocessing.

Template:
```python
prefix = [0] * (n + 1)
for i in range(n):
    prefix[i + 1] = prefix[i] + arr[i]

# Sum of arr[l..r] (inclusive)
range_sum = prefix[r + 1] - prefix[l]
```

2D prefix sum for matrix range queries:
```python
prefix[i][j] = matrix[i-1][j-1] + prefix[i-1][j] + prefix[i][j-1] - prefix[i-1][j-1]
```

Applications: Range queries, subarray sum equals k, difference arrays.""",
        "tags": ["prefix_sum", "array", "range_query"],
    },
    {
        "id": "hashing",
        "title": "Hash Map Patterns",
        "content": """Hash maps provide O(1) average lookup/insert for counting, grouping, and tracking.

Common patterns:
1. Frequency counting: `Counter(arr)`
2. Two Sum pattern: seen[target - num] = index
3. Grouping: anagram groups with sorted key
4. Sliding window with hash map for character counts

Applications: Two Sum, subarray sum, longest substring without repeating chars.
Collision warning: For competitive programming, consider custom hash to avoid hash attacks.""",
        "tags": ["hash_map", "counting", "array"],
    },
]
