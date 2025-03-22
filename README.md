# MetroLine
A python project to find metro line routes with least amount of transfers or time requirement

## Used libraries:

typing - Dict, List, Tuple, Optional

collections - defaultdict, deque

heapq

## Explanation of Used Libraries

**defaultdict:** A dictionary-like object that provides a default value for nonexistent keys. If you try to access a key that doesn’t exist, it automatically creates a new entry with a default value.

**deque:** A double-ended queue. It allows fast appends and pops from both left and right, making it ideal for queue-like operations.

**heapq:** A library that provides functions to implement a heap queue, which can also be called priority queue. It helps with maintaining a sorted order in a list, where the smallest element is always at the front (min-heap by default).

**Dict:** A generic type for dictionaries, where the key-value pairs are specified (e.g., Dict[str, int] means a dictionary with string keys and integer values).

**List:** A generic type for lists, specifying the type of elements in the list (e.g., List[int] means a list of integers).

**Tuple:** A generic type for tuples, used for immutable, ordered collections of elements, where you can specify the types of elements (e.g., Tuple[int, str] for a tuple of an integer and a string).

**Optional:** A type hint used to specify that a value can either be of a given type or None (e.g., Optional[str] means it can be a string or None).

## How the used algorithms work

**BFS Algorithm:** BFS algorithm starts at the initial node, explores all its neighbors by adding them to a queue and processes each node level by level by removing it from the front of the queue. This process continues until the queue is empty or the target node is found, ensuring the shortest path is found in an unweighted graph by visiting nodes layer by layer. If the graph is weighed, this will not give the best/shortest route.

**A\* Algorithm:** A* algorithm is a pathfinding and graph traversal algorithm that starts at the initial node and explores neighboring nodes by selecting the one with the lowest cost, which is determined by the sum of the actual cost from the start node and an estimated cost to the goal node. This process continues until the goal is reached, ensuring an optimal path in terms of both cost and distance when the estimate is both accurate and never overestimates the actual cost.

### Why These Algorithms?

The A* algorithm is ideal because it efficiently finds the shortest path by considering both travel time and an estimate of remaining time, making it faster than Dijkstra's, which lacks a heuristic. BFS is useful for minimizing transfers, as it guarantees the shortest path in terms of hops, exploring all routes with the same number of transfers first. Unlike DFS, which can be inefficient, BFS ensures an optimal solution by exploring all potential routes at each level.

