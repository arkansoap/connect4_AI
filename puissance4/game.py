"""Puisance4

command : sudo venv/bin/python3.9 -m puissance4
"""

import subprocess
from typing import Literal, Union

from puissance4.player import Human, AiBot

EMPTY_BOARD = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]


class Game:

    def __init__(self, player1: Union[AiBot, Human], player2: Union[AiBot, Human]):
        self.board = EMPTY_BOARD
        self.cursor: Literal[0, 1, 2, 3, 4, 5, 6] = 3
        self.player1 = player1
        self.player2 = player2
        self.players_pieces = [player1.player_piece, player2.player_piece]
        self.endgame = 0
        self.turn = 0

    def printboard(self):
        subprocess.call("clear")
        player = self.player_turn()
        print(f"{player.player_name} plays")
        print(f"tour {self.turn}")
        print("game_state", self.endgame)

        for row in self.board:
            print(row)

    def drop_token(self):
        if self.check_col_full() == 1:
            self.turn -= 1
            return
        for i in reversed(range(6)):
            if self.board[i][self.cursor] in self.players_pieces:
                pass
            else:
                self.board[i][self.cursor] = self.player_turn().player_piece
                break
        self.check_endgame()

    def check_victory(self, player: Union[AiBot, Human]):
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
        if self.board[0][self.cursor] in self.players_pieces:
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
            self.printboard()
            print(self.player_turn().player_name, "win the game")
            self.player_turn().victory = 1
            self.endgame = 1
        elif self.check_draw() == 1:
            self.printboard()
            print("Draw !! board full")
            self.player1.victory = 0, 5
            self.player2.victory = 0, 5
            self.endgame = 2
        return 0

    def player_turn(self):
        if self.turn % 2 == 0:
            return self.player1
        else:
            return self.player2
