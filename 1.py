import random

# Grid size
GRID_SIZE = 5

# Start and goal positions
x, y = 0, 0
goal = (4, 4)

# Store path
path = [(x, y)]

while (x, y) != goal:
    coin = random.choice(["H", "T"])

    if coin == "H" and y < GRID_SIZE - 1:
        # Heads → move right
        y += 1
    elif coin == "T" and x < GRID_SIZE - 1:
        # Tails → move down
        x += 1

    path.append((x, y))

print("Agent path:")
for step in path:
    print(step)

print("\nGoal reached!")
