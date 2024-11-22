import numpy as np
import time
import keras

from puissance4.game import Player, Game


class AiBot(Player):

    def __init__(self, player_name: str, player_piece: int):
        super().__init__(player_name, player_piece)
        self.model = keras.Sequential()
        self.input_laye = self.model.add(
            keras.layers.Dense(64, activation="relu", input_shape=(42,))
        )
        self.hidden_layer = self.model.add(keras.layers.Dense(64, activation="relu"))
        self.output_layer = self.model.add(keras.layers.Dense(7, activation="softmax"))

    def predict(self, board):
        return self.model.predict(board)


def AI_choice(board, strategy):
    if strategy == "random":
        return np.random.choice(6)
    if strategy == "NN":
        pass


def fitness_function(player1, player2):
    game = Game(player1, player2)


def AI_play():
    player1_name = "Bot 1"  # input("Player1 Name: ")
    player2_name = "Bot 2"  # input("Player1 Name: ")
    player1 = AiBot(player1_name, 8)
    player2 = AiBot(player2_name, 3)
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        game.cursor = AI_choice(game.board, "random")
        game.drop_token()
        game.turn += 1
        time.sleep(1)


if __name__ == "__main__":
    AI_play()
