import time

from puissance4.game import Game
from puissance4.AI_training import AiBot
from puissance4.player import Human


def play_game(player1, player2, wait: int = 0):
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        game.cursor = game.player_turn().choose_move(game.board)
        game.drop_token()
        game.turn += 1
        time.sleep(wait)


if __name__ == "__main__":
    human_name = input("Enter your name: ")
    bot_loaded = input("Enter the name of the bot you want to load : ")
    player1 = Human(human_name, 8)
    loaded_bot = AiBot.load(bot_loaded)

    play_game(player1, loaded_bot)
