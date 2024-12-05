""" 
    A deep  learning algo to learn how to play
    tic tac toe.
    Step1: Create the tic-tac-toe environment
"""

# Winning patterns - Used for check_winning()
_rows = [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)]
_columns = [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)]
_diagonals = [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]
winning_patterns = [_rows, _columns, _diagonals]


class Game:

    def __init__(self):
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]

    def reset_board(self):
        self.game_board = [[" " for _ in range(3)] for _ in range(3)]

    def check_draw(self):
        if all(cell != " " for row in self.game_board for cell in row):
            self.winner = "DRAW"
            print("Game was a {} !!!".format(self.winner))
            exit()

    def check_winner(self, player: str):
        # my idea is to check if designated player
        # is present on any of the winning_patterns instead of hardcode the ifs
        verify_cells_for_winning = 0
        for pattern in winning_patterns:
            for list_of_coords in pattern:
                for coord in list_of_coords:
                    row, col = coord
                    if not (self.game_board[row][col] == player):
                        break
                    verify_cells_for_winning += 1
                    if verify_cells_for_winning == 3:
                        self.winner = player
                        print("And we have a winner: {} !!".format(self.winner))
                # reset verification after all the coords were verified
                verify_cells_for_winning = 0

    def display_board(self):
        for row in self.game_board:
            print("|".join(row))
        print()

    def make_move(self, player: str, coordinates: tuple):
        # Validate input
        if not isinstance(coordinates, tuple) or len(coordinates) != 2:
            raise ValueError("Coordinates must be a tuple with two ints (row, col)")

        row, col = coordinates

        if not (0 <= row < 3 and 0 <= col < 3):
            raise ValueError("Coordinates must be within range 0 to 2")
        if self.game_board[row][col] != " ":
            raise ValueError("Cell is occupied.")

        self.game_board[row][col] = player
        self.check_winner(player)
        self.check_draw()
        self.display_board()


# Main execution
if __name__ == "__main__":
    print("Let's start playing TicTacToe!")
    my_game = Game()
    my_game.make_move("X", (1, 1))
    my_game.make_move("O", (1, 0))
    my_game.make_move("X", (0, 0))
    my_game.make_move("O", (0, 2))
    my_game.make_move("X", (0, 1))
    my_game.make_move("O", (2, 2))
    my_game.make_move("O", (2, 1))
    my_game.make_move("X", (1, 2))
    my_game.make_move("X", (2, 0))
