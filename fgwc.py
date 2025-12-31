from collections import deque

# Check if a state is valid
def is_valid(state):
    F, W, G, C = state

    # Wolf eats Goat
    if W == G and F != W:
        return False

    # Goat eats Cabbage
    if G == C and F != G:
        return False

    return True


# Generate all possible next states
def get_next_states(state):
    F, W, G, C = state
    next_states = []

    # Farmer crosses alone
    new_state = (1 - F, W, G, C)
    if is_valid(new_state):
        next_states.append(new_state)

    # Farmer crosses with Wolf
    if F == W:
        new_state = (1 - F, 1 - W, G, C)
        if is_valid(new_state):
            next_states.append(new_state)

    # Farmer crosses with Goat
    if F == G:
        new_state = (1 - F, W, 1 - G, C)
        if is_valid(new_state):
            next_states.append(new_state)

    # Farmer crosses with Cabbage
    if F == C:
        new_state = (1 - F, W, G, 1 - C)
        if is_valid(new_state):
            next_states.append(new_state)

    return next_states


# Breadth-First Search
def bfs():
    start = (0, 0, 0, 0)
    goal = (1, 1, 1, 1)

    queue = deque([(start, [start])])
    visited = set()

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)

            for state in get_next_states(current):
                queue.append((state, path + [state]))

    return None


# Driver Code
solution = bfs()

if solution:
    print("Solution Path:\n")
    for step in solution:
        print(step)
else:
    print("No solution found")
