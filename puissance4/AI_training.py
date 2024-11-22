import numpy as np
import time
import keras

from puissance4.game import Game
from puissance4.player import AiBot


def fitness_function(player1, player2):
    game = Game(player1, player2)


def AI_training():
    player1_name = "Random Bot"
    player2_name = "NN Bot"
    player1 = AiBot(player1_name, 8, "NN")
    player2 = AiBot(player2_name, 3, "random")
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        game.cursor = game.player_turn().choose_move(game.board)
        game.drop_token()
        game.turn += 1
        time.sleep(3)
    # TODO:
    # - faire jouer deux bots NN
    # - déterminer le gagnant
    # - attribuer récompense / malus


if __name__ == "__main__":
    AI_training()
