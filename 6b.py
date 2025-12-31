# ----------------------------------
# Tic-Tac-Toe using Minimax Algorithm
# ----------------------------------

import math

# Initialize board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Display the board
def display_board():
    print("\nBoard:")
    for row in board:
        print("|".join(row))
        print("-" * 5)

# Check for winner
def check_winner(player):
    # Rows and Columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    # Diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Check for draw
def is_draw():
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

# Minimax algorithm
def minimax(is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Computer move using minimax
def computer_move():
    best_score = -math.inf
    move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)

    board[move[0]][move[1]] = 'O'
    print(f"Computer placed O at {move}")

# Human move
def human_move():
    while True:
        try:
            r = int(input("Enter row (0-2): "))
            c = int(input("Enter column (0-2): "))
            if board[r][c] == ' ':
                board[r][c] = 'X'
                break
            else:
                print("Cell occupied. Try again.")
        except:
            print("Invalid input.")

# Main Game Loop
print("Tic-Tac-Toe: Human (X) vs Computer (O - Minimax)")
display_board()

while True:
    # Human turn
    human_move()
    display_board()

    if check_winner('X'):
        print("🎉 Human wins!")
        break
    if is_draw():
        print("🤝 Draw!")
        break

    # Computer turn
    computer_move()
    display_board()

    if check_winner('O'):
        print("💻 Computer wins!")
        break
    if is_draw():
        print("🤝 Draw!")
        break
