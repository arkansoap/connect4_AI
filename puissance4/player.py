import keras
import numpy as np
from typing import Literal
import time


class Player:
    def __init__(
        self,
        player_name: str,
        player_piece: int,
        player_type: Literal["Human", "AI"],
        victory: float = 0,
    ):
        self.player_name = player_name
        self.player_piece = player_piece
        self.player_type = player_type
        self.victory = victory

    def choose_move(self):
        pass


class Human(Player):
    def __init__(self, player_name, player_piece):
        super().__init__(player_name, player_piece, "Human")

    def choose_move(self, board):
        return int(input("choose a col : "))


class AiBot(Player):
    def __init__(
        self, player_name: str, player_piece: int, strategy: Literal["random", "NN"]
    ):
        super().__init__(player_name, player_piece, "AI")
        self.strategy = strategy
        self.evaluation = 0
        self.__post_init__()

    def __post_init__(self):
        if self.strategy == "NN":
            self.model = keras.Sequential()
            self.input_layer = self.model.add(
                keras.layers.Dense(64, activation="relu", input_shape=(42,))
            )
            self.hidden_layer = self.model.add(
                keras.layers.Dense(64, activation="relu")
            )
            self.output_layer = self.model.add(
                keras.layers.Dense(7, activation="softmax")
            )
            self.summary = self.model.summary()

    def choose_move(self, board):
        if self.strategy == "random":
            choosen_column = np.random.randint(0, 7)
        elif self.strategy == "NN":
            flattened_board = np.array(board).flatten().reshape(1, -1)
            probabilities = self.model.predict(flattened_board)
            # print(probabilities)
            # print(board)
            # time.sleep(3)

            # Mask full columns by setting their probabilities to a very low value
            for col in range(7):
                if board[0][col] != 0:
                    # Set to a value lower than any valid probability
                    probabilities[0][col] = -1

            choosen_column = np.argmax(probabilities)

        else:
            raise ValueError("Invalid strategy")

        return choosen_column

    def mutate_if_loose(self):
        # Mutate the model if the bot lost, just a little variation
        if self.victory == 0:
            for layer in self.model.layers:
                if len(layer.get_weights()) > 0:
                    layer.set_weights(
                        [
                            layer.get_weights()[0]
                            + np.random.randn(*layer.get_weights()[0].shape) * 0.1,
                            layer.get_weights()[1],
                        ]
                    )

            print("Mutated")
