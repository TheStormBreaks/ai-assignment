import heapq

# -----------------------------
# A* Algorithm Implementation
# -----------------------------
def a_star(grid):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    # Manhattan distance heuristic
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Priority queue: (f_cost, g_cost, current_node, path)
    open_list = []
    heapq.heappush(open_list, (0, 0, start, [start]))

    visited = set()

    while open_list:
        f_cost, g_cost, current, path = heapq.heappop(open_list)

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        x, y = current
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            if 0 <= nx < rows and 0 <= ny < cols:
                if grid[nx][ny] == 0 and neighbor not in visited:
                    new_g = g_cost + 1
                    new_f = new_g + heuristic(neighbor, goal)
                    heapq.heappush(
                        open_list,
                        (new_f, new_g, neighbor, path + [neighbor])
                    )

    return None


# -----------------------------
# Driver Code
# -----------------------------
grid = [
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0]
]

path = a_star(grid)

if path:
    print("Shortest Path Found:")
    for step in path:
        print(step)
else:
    print("No path found")
