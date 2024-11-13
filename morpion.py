"""Morpion

command : sudo venv/bin/python3.9 -m morpion
"""

import keyboard
import subprocess


def emptyboard():
    return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


def printboard(board):
    subprocess.call("clear")
    for row in board:
        print(row)


def init():
    board = emptyboard()
    cursor = [1, 1]
    return board, cursor


def moove_cursor(cursor):
    if keyboard.is_pressed("q"):
        cursor[1] -= 1
    elif keyboard.is_pressed("d"):
        cursor[1] += 1
    elif keyboard.is_pressed("z"):
        cursor[0] -= 1
    elif keyboard.is_pressed("s"):
        cursor[0] += 1
    for i in [0, 1]:
        if cursor[i] < 0:
            cursor[i] = 2
        if cursor[i] > 2:
            cursor[i] = 0
    return cursor


def save_board(board, cursor, player, turn):
    if board[cursor[0]][cursor[1]] in [4, 8]:
        print("Case already played")
        turn -= 1
        game = 0
        return board, game, turn
    board[cursor[0]][cursor[1]] = player[1]
    printboard(board)
    game = check_endgame(board, player)
    return board, game, turn


def check_victory(board, player):
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] == player[1]:
            print(f"{player[0]} win")
            return 1
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] == player[1]:
            print(f"{player[0]} win")
            return 1
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] == player[1]:
        print(f"{player[0]} win")
        return 1
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] == player[1]:
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
        player_piece = 4
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
            board, game, turn = save_board(board, cursor, player, turn)
            turn += 1
        else:
            if board[cursor[0]][cursor[1]] not in [4, 8]:
                board[cursor[0]][cursor[1]] = 0
            cursor = moove_cursor(cursor)
            if board[cursor[0]][cursor[1]] not in [4, 8]:
                board[cursor[0]][cursor[1]] = 1
            printboard(board)


if __name__ == "__main__":
    main()
