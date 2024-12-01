import keras
import numpy as np
from typing import Literal
import json
import logging_setup

logger = logging_setup.setup_logger()


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

    def choose_move(self, board):
        pass


class Human(Player):
    def __init__(self, player_name, player_piece):
        super().__init__(player_name, player_piece, "Human")

    def choose_move(self, board):
        move = int(input("choose a col : "))
        return move


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
            # self.summary = self.model.summary()

    def choose_move(self, board):
        if self.strategy == "random":
            choosen_column = np.random.randint(0, 7)
        elif self.strategy == "NN":
            flattened_board = np.array(board).flatten().reshape(1, -1)
            probabilities = self.model.predict(flattened_board)

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

            logger.info(f"{self.player_name} Mutated after loosing")

    def save(self):
        filepath = f"puissance4/saved_bot/{self.player_name}.json"
        bot_data = {
            "player_name": self.player_name,
            "player_piece": self.player_piece,
            "strategy": self.strategy,
            "evaluation": self.evaluation,
            "victory": self.victory,
        }
        with open(filepath, "w") as f:
            json.dump(bot_data, f)
        if self.strategy == "NN":
            self.model.save(f"puissance4/saved_bot/{self.player_name}.h5")

    @classmethod
    def load(cls, bot_name):
        filepath = f"puissance4/saved_bot/{bot_name}.json"
        with open(filepath, "r") as f:
            bot_data = json.load(f)
        bot = cls(
            bot_data["player_name"], bot_data["player_piece"], bot_data["strategy"]
        )
        bot.evaluation = bot_data["evaluation"]
        bot.victory = bot_data["victory"]
        if bot.strategy == "NN":
            bot.model = keras.models.load_model(f"puissance4/saved_bot/{bot_name}.h5")
        return bot
