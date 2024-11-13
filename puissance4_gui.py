import tkinter as tk
from tkinter import messagebox
from puissance4 import Game, Player


class GameUI:
    def __init__(self, game: Game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.buttons = [[None for _ in range(7)] for _ in range(6)]
        self.create_board()
        self.update_board()
        self.root.bind("<Key>", self.handle_keypress)
        self.root.mainloop()

    def create_board(self):
        for i in range(6):
            for j in range(7):
                button = tk.Button(
                    self.root,
                    text="",
                    width=4,
                    height=2,
                )
                button.grid(row=i, column=j)
                self.buttons[i][j] = button

    def update_board(self):
        for i in range(6):
            for j in range(7):
                value = self.game.board[i][j]
                if value == 1:
                    self.buttons[i][j].config(bg="red")
                elif value == 3:
                    self.buttons[i][j].config(bg="yellow")
                elif value == 8:
                    self.buttons[i][j].config(bg="blue")
                else:
                    self.buttons[i][j].config(bg="white")

    def handle_keypress(self, event):
        if event.keysym == "Escape":
            self.root.quit()
        elif event.keysym == "Return":
            self.perform_drop_token()
        else:
            if (
                self.game.board[self.game.cursor[0]][self.game.cursor[1]]
                not in self.game.players_pieces
            ):
                self.game.board[self.game.cursor[0]][self.game.cursor[1]] = 0
            self.game.moove_cursor()
            if (
                self.game.board[self.game.cursor[0]][self.game.cursor[1]]
                not in self.game.players_pieces
            ):
                self.game.board[self.game.cursor[0]][self.game.cursor[1]] = 1
            self.update_board()

    def perform_drop_token(self):
        self.game.drop_token()
        self.game.turn += 1
        self.update_board()
        if self.game.endgame == 1:
            winner = self.game.player_turn().player_name
            messagebox.showinfo("Game Over", f"{winner} wins the game!")
            self.root.quit()
        if self.game.endgame == 2:
            messagebox.showinfo("Game Over", "It's a tie!")
            self.root.quit()


def main():
    player1_name = "Player 1"  # input("Player1 Name: ")
    player2_name = "Player 2"  # input("Player2 Name: ")
    player1 = Player(player1_name, 8)
    player2 = Player(player2_name, 3)
    game = Game(player1, player2)
    game.board[game.cursor[0]][game.cursor[1]] = 1
    GameUI(game)


if __name__ == "__main__":
    main()
