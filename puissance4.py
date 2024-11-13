"""Puisance4

command : sudo venv/bin/python3.9 -m puissance4
"""

import keyboard
import subprocess
import time

EMPTY_BOARD = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


class Player:
    def __init__(self, player_name: str, player_piece: int):
        self.player_name = player_name
        self.player_piece = player_piece


class Game:

    def __init__(self, player1: Player, player2: Player):
        self.board = EMPTY_BOARD
        self.cursor = [0, 1]
        self.player1 = player1
        self.player2 = player2
        self.players_pieces = [player1.player_piece, player2.player_piece]
        self.endgame = 0
        self.turn = 0

    def printboard(self):
        subprocess.call("clear")
        for row in self.board:
            print(row)

    def moove_cursor(self):
        if keyboard.is_pressed("q"):
            self.cursor[1] -= 1
        elif keyboard.is_pressed("d"):
            self.cursor[1] += 1
        if self.cursor[1] < 0:
            self.cursor[1] = 6
        if self.cursor[1] > 6:
            self.cursor[1] = 0

    def drop_token(self):
        if self.check_col_full() == 1:
            self.turn -= 1
            return
        for i in reversed(range(6)):
            if self.board[i][self.cursor[1]] in self.players_pieces:
                pass
            else:
                self.board[i][self.cursor[1]] = self.player_turn().player_piece
                break
        self.printboard()
        print(f"coord_token : {i}{self.cursor[1]}")
        player = self.player_turn()
        print(f"{player.player_name} plays")
        print(f"tour {self.turn}")
        print("game_state", self.endgame)
        self.check_endgame()

    def check_victory(self, player: Player):
        for i in range(6):  # Assuming board height is 6
            for j in range(7):  # Assuming board width is 7
                # horizontal
                if j <= 3:  # Adjust to prevent out-of-range
                    if (
                        self.board[i][j] == player.player_piece
                        and self.board[i][j + 1] == player.player_piece
                        and self.board[i][j + 2] == player.player_piece
                        and self.board[i][j + 3] == player.player_piece
                    ):
                        return 1
                # vertical
                if i <= 2:  # Adjust to prevent out-of-range
                    if (
                        self.board[i][j] == player.player_piece
                        and self.board[i + 1][j] == player.player_piece
                        and self.board[i + 2][j] == player.player_piece
                        and self.board[i + 3][j] == player.player_piece
                    ):
                        return 1
                # diagonal (bottom-left to top-right)
                if i <= 2 and j <= 3:  # Adjust to prevent out-of-range
                    if (
                        self.board[i][j] == player.player_piece
                        and self.board[i + 1][j + 1] == player.player_piece
                        and self.board[i + 2][j + 2] == player.player_piece
                        and self.board[i + 3][j + 3] == player.player_piece
                    ):
                        return 1
                # diagonal (top-left to bottom-right)
                if i >= 3 and j <= 3:  # Adjust to prevent out-of-range
                    if (
                        self.board[i][j] == player.player_piece
                        and self.board[i - 1][j + 1] == player.player_piece
                        and self.board[i - 2][j + 2] == player.player_piece
                        and self.board[i - 3][j + 3] == player.player_piece
                    ):
                        return 1

    def check_col_full(self):
        if self.board[0][self.cursor[1]] in self.players_pieces:
            print("Column full, please choose another one")
            return 1

    def check_draw(self):
        for row in self.board:
            if 0 in row:
                return 0
        print("Draw")
        return 1

    def check_endgame(self):
        if self.check_victory(self.player_turn()) == 1:
            print(self.player_turn().player_name, "win the game")
            self.endgame = 1
        elif self.check_draw() == 1:
            print("Draw !! board full")
            self.endgame = 2
        return 0

    def player_turn(self):
        if self.turn % 2 == 0:
            return self.player2
        else:
            return self.player1


def main():
    """To play in a terminal"""
    player1_name = "Player 1"  # input("Player1 Name: ")
    player2_name = "Player 2"  # input("Player1 Name: ")
    player1 = Player(player1_name, 8)
    player2 = Player(player2_name, 3)
    game = Game(player1, player2)
    game.board[game.cursor[0]][game.cursor[1]] = 1
    touch = None
    game.printboard()
    while game.endgame != 1:
        touch = keyboard.read_event()
        if touch.event_type == "down":
            if touch.name == "esc":
                game.endgame = 1
            elif touch.name == "enter":
                game.drop_token()
                game.turn += 1
            else:
                if (
                    game.board[game.cursor[0]][game.cursor[1]]
                    not in game.players_pieces
                ):
                    game.board[game.cursor[0]][game.cursor[1]] = 0
                game.moove_cursor()
                if (
                    game.board[game.cursor[0]][game.cursor[1]]
                    not in game.players_pieces
                ):
                    game.board[game.cursor[0]][game.cursor[1]] = 1
                game.printboard()


if __name__ == "__main__":
    main()
