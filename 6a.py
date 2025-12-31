import random

# -----------------------------
# Initialize the board
# -----------------------------
board = [[' ' for _ in range(3)] for _ in range(3)]

# -----------------------------
# Display the board
# -----------------------------
def display_board():
    print("\nCurrent Board:")
    for row in board:
        print("|".join(row))
        print("-" * 5)

# -----------------------------
# Check for winner
# -----------------------------
def check_winner(player):
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# -----------------------------
# Check for draw
# -----------------------------
def is_draw():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# -----------------------------
# Human move
# -----------------------------
def human_move():
    while True:
        try:
            row = int(input("Enter row (0, 1, 2): "))
            col = int(input("Enter column (0, 1, 2): "))

            if board[row][col] == ' ':
                board[row][col] = 'X'
                break
            else:
                print("Cell already occupied. Try again.")
        except:
            print("Invalid input. Enter numbers between 0 and 2.")

# -----------------------------
# Computer move (Random)
# -----------------------------
def computer_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    row, col = random.choice(empty_cells)
    board[row][col] = 'O'
    print(f"Computer placed O at ({row}, {col})")

# -----------------------------
# Main Game Loop
# -----------------------------
print("Tic-Tac-Toe: Human (X) vs Computer (O)")
display_board()

while True:
    # Human turn
    human_move()
    display_board()

    if check_winner('X'):
        print("🎉 Human wins!")
        break

    if is_draw():
        print("🤝 It's a draw!")
        break

    # Computer turn
    computer_move()
    display_board()

    if check_winner('O'):
        print("💻 Computer wins!")
        break

    if is_draw():
        print("🤝 It's a draw!")
        break
