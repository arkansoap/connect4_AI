import numpy as np
import time

from puissance4.game import Player, Game


def AI_play():
    player1_name = "Bot 1"  # input("Player1 Name: ")
    player2_name = "Bot 2"  # input("Player1 Name: ")
    player1 = Player(player1_name, 8)
    player2 = Player(player2_name, 3)
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        game.cursor = AI_choice(game.board, "random")
        game.drop_token()
        game.turn += 1
        time.sleep(1)


def AI_choice(board, strategy):
    if strategy == "random":
        return np.random.choice(6)
    if strategy == "plop":
        pass


def detect_series(board):
    pass


if __name__ == "__main__":
    AI_play()
