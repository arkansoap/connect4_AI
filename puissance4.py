"""Morpion

command : sudo venv/bin/python3.9 -m puissance4
"""

import keyboard
import subprocess


def emptyboard():
    return [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]


def printboard(board):
    subprocess.call("clear")
    for row in board:
        print(row)


def init():
    board = emptyboard()
    cursor = [0, 1]
    return board, cursor


def moove_cursor(cursor):
    if keyboard.is_pressed("q"):
        cursor[1] -= 1
    elif keyboard.is_pressed("d"):
        cursor[1] += 1
    if cursor[1] < 0:
        cursor[1] = 6
    if cursor[1] > 6:
        cursor[1] = 0
    return cursor


def drop_token(board, cursor, player):
    for i in reversed(range(6)):
        print(i)
        if board[i][cursor[1]] in [3, 8]:
            pass
        else:
            board[i][cursor[1]] = player[1]
            break
    printboard(board)
    game = check_endgame(board, player)
    return board, game


def check_4_follow(board):
    if board():
        pass


def check_victory(board, player):
    for i in range(6):  # Assuming board height is 6
        for j in range(7):  # Assuming board width is 7
            # horizontal
            if j <= 3:  # Adjust to prevent out-of-range
                if (
                    board[i][j] == player[1]
                    and board[i][j + 1] == player[1]
                    and board[i][j + 2] == player[1]
                    and board[i][j + 3] == player[1]
                ):
                    print(f"{player[0]} win")
                    return 1
            # vertical
            if i <= 2:  # Adjust to prevent out-of-range
                if (
                    board[i][j] == player[1]
                    and board[i + 1][j] == player[1]
                    and board[i + 2][j] == player[1]
                    and board[i + 3][j] == player[1]
                ):
                    print(f"{player[0]} win")
                    return 1
            # diagonal (bottom-left to top-right)
            if i <= 2 and j <= 3:  # Adjust to prevent out-of-range
                if (
                    board[i][j] == player[1]
                    and board[i + 1][j + 1] == player[1]
                    and board[i + 2][j + 2] == player[1]
                    and board[i + 3][j + 3] == player[1]
                ):
                    print(f"{player[0]} win")
                    return 1
            # diagonal (top-left to bottom-right)
            if i >= 3 and j <= 3:  # Adjust to prevent out-of-range
                if (
                    board[i][j] == player[1]
                    and board[i - 1][j + 1] == player[1]
                    and board[i - 2][j + 2] == player[1]
                    and board[i - 3][j + 3] == player[1]
                ):
                    print(f"{player[0]} win")
                    return 1


def check_draw(board):
    for row in board:
        if 0 in row:
            return 0
    print("Draw")
    return 1


def check_endgame(board, player):
    if check_victory(board, player) == 1:
        return 1
    elif check_draw(board) == 1:
        return 1
    return 0


def player_turn(turn):
    if turn % 2 == 0:
        player = "player 1"
        player_piece = 3
    else:
        player = "player 2"
        player_piece = 8
    return [player, player_piece]


def main():
    game = 0
    turn = 0
    board, cursor = init()
    board[cursor[0]][cursor[1]] = 1
    touch = None
    printboard(board)
    while game != 1:
        player = player_turn(turn)
        print(f"{player[0]} plays")
        print(f"tour {turn}")
        touch = keyboard.read_event()
        if touch.name == "esc":
            game = 1
        elif keyboard.is_pressed("enter"):
            board, game = drop_token(board, cursor, player)
            turn += 1
        else:
            if board[cursor[0]][cursor[1]] not in [3, 8]:
                board[cursor[0]][cursor[1]] = 0
            cursor = moove_cursor(cursor)
            if board[cursor[0]][cursor[1]] not in [3, 8]:
                board[cursor[0]][cursor[1]] = 1
            printboard(board)


if __name__ == "__main__":
    main()
