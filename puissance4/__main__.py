import time

from puissance4.game import Game
from puissance4.AI_training import AiBot
from puissance4.player import Human


def play_game(player1, player2, wait: int = 0):
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        game.player_turn().choose_move(game.board)
        game.drop_token()
        game.turn += 1
        time.sleep(wait)


if __name__ == "__main__":
    player1_name = "Human"
    player2_name = "Bot"
    player1 = Human(player1_name, 8)
    player2 = AiBot(player2_name, 3)
    play_game(player1, player2)
