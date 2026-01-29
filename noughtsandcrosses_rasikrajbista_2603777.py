import random
import os.path
import json

random.seed()


def draw_board(board):
    """Draws the current state of the board."""
    print()
    for row in range(3):
        print(" ", board[row][0], "|", board[row][1], "|", board[row][2])
        if row < 2:
            print(" ---+---+---")
    print()


def welcome(board):
    """Prints the welcome message and displays the board."""
    print("Welcome to the Unbeatable Noughts and Crosses Game!")
    print("The human player is X and the computer is O.")
    draw_board(board)


def initialise_board(board):
    """Sets all board cells to a single space."""
    for row in range(3):
        for col in range(3):
            board[row][col] = ' '
    return board


def get_player_move(board):
    """Asks the player for a valid move and returns row and column."""
    while True:
        move = input("Enter the cell number (1-9) to place X: ")
        if move.isdigit():
            cell = int(move)
            if 1 <= cell <= 9:
                row = (cell - 1) // 3
                col = (cell - 1) % 3
                if board[row][col] == ' ':
                    return row, col
        print("Invalid move. Try again.")


def choose_computer_move(board):
    # Winning move
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'O'
                if check_for_win(board, 'O'):
                    board[r][c] = ' '
                    return r, c
                board[r][c] = ' '

    # Blocking move
    for r in range(3):
        for c in range(3):
            if board[r][c] == ' ':
                board[r][c] = 'X'
                if check_for_win(board, 'X'):
                    board[r][c] = ' '
                    return r, c
                board[r][c] = ' '

    # Take center
    if board[1][1] == ' ':
        return 1, 1

    # Take a corner
    corners = [(0,0),(0,2),(2,0),(2,2)]
    random.shuffle(corners)
    for r, c in corners:
        if board[r][c] == ' ':
            return r, c

    # Take any side
    sides = [(0,1),(1,0),(1,2),(2,1)]
    random.shuffle(sides)
    for r, c in sides:
        if board[r][c] == ' ':
            return r, c



def check_for_win(board, mark):
    """Checks whether the given mark has won."""
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == mark:
            return True
        if board[0][i] == board[1][i] == board[2][i] == mark:
            return True

    if board[0][0] == board[1][1] == board[2][2] == mark:
        return True
    if board[0][2] == board[1][1] == board[2][0] == mark:
        return True

    return False


def check_for_draw(board):
    """Checks whether the game is a draw."""
    for row in range(3):
        for col in range(3):
            if board[row][col] == ' ':
                return False
    return True


def play_game(board):
    """Controls the main game loop."""
    initialise_board(board)
    draw_board(board)

    while True:
        row, col = get_player_move(board)
        board[row][col] = 'X'
        draw_board(board)

        if check_for_win(board, 'X'):
            print("You win!")
            return 1

        if check_for_draw(board):
            print("It's a draw!")
            return 0

        row, col = choose_computer_move(board)
        board[row][col] = 'O'
        print("Computer plays:")
        draw_board(board)

        if check_for_win(board, 'O'):
            print("Computer wins!")
            return -1

        if check_for_draw(board):
            print("It's a draw!")
            return 0


def menu():
    """Displays the menu and returns the user's choice."""
    print("1 - Play the game")
    print("2 - Save score")
    print("3 - Load and display leaderboard")
    print("q - Quit")

    choice = input("Enter your choice: ").lower()
    while choice not in ['1', '2', '3', 'q']:
        choice = input("Invalid choice. Try again: ").lower()

    return choice


def load_scores():
    if not os.path.exists("leaderboard.txt"):
        return {}

    try:
        with open("leaderboard.txt", "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}



def save_score(score):
    """Saves the player's score to leaderboard.txt."""
    name = input("Enter your name: ")

    scores = {}
    if os.path.exists("leaderboard.txt"):
        with open("leaderboard.txt", "r", encoding="utf-8") as file:
            scores = json.load(file)

    scores[name] = scores.get(name, 0) + score


    with open("leaderboard.txt", "w", encoding="utf-8") as file:
        json.dump(scores, file)


def display_leaderboard(leaders):
    print("\nLeaderboard:")
    sorted_scores = sorted(leaders.items(), key=lambda x: x[1], reverse=True)
    for name, score in sorted_scores:
        print(name, ":", score)

