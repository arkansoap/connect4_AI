from puissance4.game import Game, Human
from puissance4.AI_training import AiBot, AI_choice


def play_game(player1, player2):
    game = Game(player1, player2)
    game.printboard()
    while game.endgame != 1:
        game.printboard()
        if game.player_turn().player_type == "Human":
            game.cursor = int(input("choose a col : "))
        elif game.player_turn().player_type == "AI":
            game.cursor = AI_choice(game.board, "random")
        game.drop_token()
        game.turn += 1


if __name__ == "__main__":
    player1_name = "Human"  # input("Player1 Name: ")
    player2_name = "Bot"  # input("Player1 Name: ")
    player1 = Human(player1_name, 8)
    player2 = AiBot(player2_name, 3)
    play_game(player1, player2)
