def print_board(board):
    print("---------")
    for row in board:
        print(f"| {' '.join(row)} |")
    print("---------")

def check_state(board):
    lines = [
        board[0], board[1], board[2],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    x_wins = any(line == ["X", "X", "X"] for line in lines)
    o_wins = any(line == ["O", "O", "O"] for line in lines)
    empty_exists = any("_" in row for row in board)

    if x_wins and o_wins:
        return "Impossible"
    if x_wins:
        return "X wins"
    if o_wins:
        return "O wins"
    if empty_exists:
        return "Game not finished"
    return "Draw"

def get_move(board, player):
    while True:
        user_input = input(f"Enter coordinates for {player}: ").split()
        if len(user_input) != 2 or not all(c.isdigit() for c in user_input):
            print("You should enter numbers!")
            continue

        row, col = map(int, user_input)
        if not (1 <= row <= 3 and 1 <= col <= 3):
            print("Coordinates should be from 1 to 3!")
            continue

        row_index = row - 1
        col_index = col - 1
        if board[row_index][col_index] != "_":
            print("This cell is occupied! Choose another one!")
            continue

        return row_index, col_index

def main():
    board = [["_"] * 3 for _ in range(3)]
    print_board(board)
    current_player = "X"

    while True:
        row, col = get_move(board, current_player)
        board[row][col] = current_player
        print_board(board)

        state = check_state(board)
        if state in ["X wins", "O wins", "Draw"]:
            print(state)
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
