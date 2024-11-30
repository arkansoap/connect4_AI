import numpy as np
import time
from typing import List
import keras

from puissance4.game import Game, EMPTY_BOARD
from puissance4.player import AiBot


def AI_evaluation(player1: AiBot, player2: AiBot, n_games: int = 10):

    player1.player_piece = 4
    player2.player_piece = 8

    for i in range(n_games):

        game = Game(player1, player2)
        game.reset()
        game.printboard()
        while game.endgame != 1:
            game.printboard()
            game.cursor = game.player_turn().choose_move(game.board)
            game.drop_token()
            game.turn += 1

        for player in [player1, player2]:
            if player.victory == 1:
                player.evaluation += player.victory + (player.victory / game.turn) * 10
            elif player.victory == 0.5:
                player.evaluation += player.victory
            elif player.victory == 0:
                player.mutate_if_loose()
        print(f"game {i}")
        print(f"player1 : victory {player1.victory} | evaluation {player1.evaluation}")
        print(f"player2 : victory {player2.victory} | evaluation {player2.evaluation}")
        # time.sleep(3)

    print("player1", player1.evaluation)
    print("player2", player2.evaluation)


def initiate_population(size: int):
    population = []
    for i in range(size):
        player = AiBot(f"player_{i}", 3, "NN")
        population.append(player)
    return population


def selection(population: List[AiBot], n: int):
    selected = []
    for i in range(n):
        selected.append(max(population, key=lambda x: x.evaluation))
        population.remove(selected[-1])
    return selected


def crossover(player1: AiBot, player2: AiBot):
    new_player = AiBot(
        f"player_{player1.player_name.strip('player_')}{player2.player_name.strip('player_')}",
        3,
        "NN",
    )
    new_player.model.set_weights(player1.model.get_weights())
    for i in range(len(new_player.model.get_weights())):
        new_player.model.get_weights()[i] = (
            new_player.model.get_weights()[i] + player2.model.get_weights()[i]
        ) / 2
    print("new player", new_player)
    print("new player weights", new_player.model.get_weights())
    return new_player


def one_generation_process(population: List[AiBot], n_games: int):
    if len(population) % 2 != 0:
        population.pop(population.index(min(population, key=lambda x: x.evaluation)))
    population_size = len(population)
    side1 = population[: population_size // 2]
    side2 = population[population_size // 2 :]
    for player1, player2 in zip(side1, side2):
        AI_evaluation(player1=player1, player2=player2, n_games=n_games)

    selected = selection(population, population_size // 2)
    new_population = []
    if len(selected) > 1:
        for i in range(0, len(selected), 2):
            new_population.append(crossover(selected[i], selected[i + 1]))
    else:
        new_population.append(selected[0])

    print(
        "Best player of the generation ",
        max(new_population, key=lambda x: x.evaluation),
    )
    print(
        "name of the best player ",
        max(new_population, key=lambda x: x.evaluation).player_name,
    )
    print(
        "weights", max(new_population, key=lambda x: x.evaluation).model.get_weights()
    )
    return new_population


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--n_games",
        type=int,
        default=1,
        help="Number of games to play to evaluate the AI",
    )

    parser.add_argument(
        "--population_size",
        type=int,
        default=4,
        help="Number of players in the population",
    )

    args = parser.parse_args()

    population = initiate_population(args.population_size)
    while len(population) > 1:
        population = one_generation_process(population, args.n_games)
        print("New generation", population)
    best_bot: AiBot = population[0]
    best_bot.save()
