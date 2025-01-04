import math

def print_board(board):
    """Prints the Tic-Tac-Toe board."""
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def is_moves_left(board):
    """Checks if there are empty cells left on the board."""
    for row in board:
        if " " in row:
            return True
    return False

def evaluate(board):
    """Evaluates the board to determine the score."""
    # Check rows, columns, and diagonals for a win
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return 10 if row[0] == "X" else -10

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return 10 if board[0][col] == "X" else -10

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return 10 if board[0][0] == "X" else -10

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return 10 if board[0][2] == "X" else -10

    return 0

def minimax(board, depth, is_max):
    """The Minimax algorithm for finding the best move."""
    score = evaluate(board)

    if score == 10 or score == -10:
        return score

    if not is_moves_left(board):
        return 0

    if is_max:
        best = -math.inf

        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = " "
        return best
    else:
        best = math.inf

        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = " "
        return best

def find_best_move(board):
    """Finds the best move for the AI."""
    best_val = -math.inf
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                move_val = minimax(board, 0, False)
                board[i][j] = " "

                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

def main():
    """Main function to run the game."""
    board = [[" " for _ in range(3)] for _ in range(3)]

    print("Welcome to Tic-Tac-Toe! You are 'O', and the AI is 'X'.")
    print_board(board)

    while True:
        # Player's move
        player_row = int(input("Enter row (0, 1, 2): "))
        player_col = int(input("Enter column (0, 1, 2): "))

        if board[player_row][player_col] != " ":
            print("Invalid move. Try again.")
            continue

        board[player_row][player_col] = "O"
        print_board(board)

        if evaluate(board) == -10:
            print("You win!")
            break

        if not is_moves_left(board):
            print("It's a draw!")
            break

        # AI's move
        print("AI is making its move...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = "X"
        print_board(board)

        if evaluate(board) == 10:
            print("AI wins!")
            break

        if not is_moves_left(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()
