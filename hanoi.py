class TowersOfHanoiAgent:
    def __init__(self):
        self.moves = []

    def plan(self, n, source, auxiliary, target):
        """
        Recursive planning function
        """
        if n == 1:
            self.moves.append(f"Move disk 1 from {source} to {target}")
            return

        # Move n-1 disks to auxiliary peg
        self.plan(n - 1, source, target, auxiliary)

        # Move the largest disk to target peg
        self.moves.append(f"Move disk {n} from {source} to {target}")

        # Move n-1 disks from auxiliary to target peg
        self.plan(n - 1, auxiliary, source, target)

    def solve(self, n):
        """
        Solves the problem and outputs the plan
        """
        self.moves.clear()
        self.plan(n, "Source", "Auxiliary", "Target")
        return self.moves


# Driver Code
if __name__ == "__main__":
    agent = TowersOfHanoiAgent()
    number_of_disks = 3

    solution = agent.solve(number_of_disks)

    print(f"Solution for {number_of_disks} disks:\n")
    for step in solution:
        print(step)
