# Tic-Tac-Toe Game

# Function to print the game board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

# Function to check if a player has won
def check_win(board, player):
    # Check rows
    for row in board:
        if row.count(player) == 3:
            return True
    # Check columns
    for col in range(3):
        if [board[row][col] for row in range(3)].count(player) == 3:
            return True
    # Check diagonals
    if [board[i][i] for i in range(3)].count(player) == 3:
        return True
    if [board[i][2 - i] for i in range(3)].count(player) == 3:
        return True
    return False

# Function to check if the game is a draw
def check_draw(board):
    for row in board:
        if " " in row:
            return False
    return True

# Function to play the game
def play_game():
    board = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]
    current_player = "X"
    while True:
        print("Player", current_player, "turn:")
        row = int(input("Enter the row (0-2): "))
        col = int(input("Enter the column (0-2): "))
        if board[row][col] == " ":
            board[row][col] = current_player
            print_board(board)
            if check_win(board, current_player):
                print("Player", current_player, "wins!")
                break
            if check_draw(board):
                print("It's a draw!")
                break
            current_player = "O" if current_player == "X" else "X"
        else:
            print("Invalid move, try again!")

# Start the game
play_game()
