"""
nohup python -m puissance4.AI_training --n_games 3 --population_size 100000 &
"""

from typing import List
import logging
import traceback

from puissance4.game import Game, EMPTY_BOARD
from puissance4.player import AiBot

logger = logging.getLogger(__name__)


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
    logger.info(f"new player {new_player}")
    return new_player


def one_generation_process(population: List[AiBot], n_games: int):
    logger.debug(f"Population : {len(population)}")
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
            try:
                new_population.append(crossover(selected[i], selected[i + 1]))
            except Exception as e:
                logger.error(f"Error : {e}", exc_info=True)
                pass
    else:
        new_population.append(selected[0])

    return new_population


if __name__ == "__main__":

    import argparse

    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.FileHandler("logs/AI_training.log")],
    )

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--n_games",
        type=int,
        default=2,
        help="Number of games to play to evaluate the AI",
    )

    parser.add_argument(
        "--population_size",
        type=int,
        default=4,
        help="Number of players in the population",
    )

    args = parser.parse_args()

    logger.info(f"Arguments : {args}")
    logger.info("####### Starting AI training #######")
    population = initiate_population(args.population_size)
    while len(population) > 1:
        try:
            population = one_generation_process(population, args.n_games)
        except Exception as e:
            logger.error(f"Error : {e}", exc_info=True)
            break
        logger.info(f"New generation : {population}")
    best_bot: AiBot = population[0]
    best_bot.save()
    logger.info(f"Best bot : {best_bot}")
    logger.info("####### AI training finished #######")
