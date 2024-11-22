import keras
import numpy as np
from typing import Literal


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

    def choose_move(self, board):
        if self.strategy == "random":
            return np.random.randint(0, 7)
        elif self.strategy == "NN":
            flattened_board = np.array(board).flatten().reshape(1, -1)
            return np.argmax(self.model.predict(flattened_board))
        else:
            raise ValueError("Invalid strategy")
