from collections import deque
import heapq

# Graph represented as adjacency list with costs
graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 3)],
    'D': [],
    'E': [('F', 1)],
    'F': []
}

def uninformed_search(graph, start, goal, strategy, limit=None):
    visited = set()

    # BFS
    if strategy == "BFS":
        frontier = deque([(start, [start])])

        while frontier:
            node, path = frontier.popleft()
            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor, _ in graph[node]:
                    frontier.append((neighbor, path + [neighbor]))

    # DFS
    elif strategy == "DFS":
        frontier = [(start, [start])]

        while frontier:
            node, path = frontier.pop()
            if node == goal:
                return path

            if node not in visited:
                visited.add(node)
                for neighbor, _ in graph[node]:
                    frontier.append((neighbor, path + [neighbor]))

    # UCS
    elif strategy == "UCS":
        frontier = [(0, start, [start])]

        while frontier:
            cost, node, path = heapq.heappop(frontier)
            if node == goal:
                return path, cost

            if node not in visited:
                visited.add(node)
                for neighbor, edge_cost in graph[node]:
                    heapq.heappush(
                        frontier,
                        (cost + edge_cost, neighbor, path + [neighbor])
                    )

    # Depth-Limited Search
    elif strategy == "DLS":
        def recursive_dls(node, path, depth):
            if node == goal:
                return path
            if depth == 0:
                return None

            for neighbor, _ in graph[node]:
                if neighbor not in path:
                    result = recursive_dls(
                        neighbor,
                        path + [neighbor],
                        depth - 1
                    )
                    if result:
                        return result
            return None

        return recursive_dls(start, [start], limit)

    else:
        return "Invalid strategy"

    return None

# Driver Code
start_node = 'A'
goal_node = 'F'

print("BFS Path:", uninformed_search(graph, start_node, goal_node, "BFS"))
print("DFS Path:", uninformed_search(graph, start_node, goal_node, "DFS"))
print("UCS Path & Cost:", uninformed_search(graph, start_node, goal_node, "UCS"))
print("DLS Path (limit=3):", uninformed_search(graph, start_node, goal_node, "DLS", limit=3))
