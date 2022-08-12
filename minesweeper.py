# Author: Steven Chen
# Description: Portfolio project based on Minesweeper with a 10x10 grid and 10 mines.

import random
from subprocess import call
import sys
from exceptions import *
from cells import *


class Minesweeper:
    """class that represents the minesweeper board and contains functions for the game mechanics"""

    def __init__(self):
        self._game_over = False
        self._win = False
        self._loss = False
        self._turn_count = 0
        self._mine_count = 10
        self._board = [[] for _ in range(12)]
        self.init_cells()

    def set_game_over(self):
        """sets the game as over because of a win or loss"""

        self._game_over = True

    def still_playing(self):
        """returns True if the game is not over yet"""

        if self._game_over:
            return False
        else:
            return True

    def set_win(self):
        """sets the game as won when the verify function sees that every cell has been revealed except for the mines"""

        self._win = True

    def set_loss(self):
        """sets the game as lost when the verify function finds a revealed mine"""

        self._loss = True

    def game_result(self):
        """returns True if the game is won, otherwise returns False"""
        if self._win:
            return True
        else:
            return False

    def init_cells(self):
        """fills the game board cells with the appropriate GameCells or BorderCells"""

        for init_row in range(12):
            self.init_topbot(init_row)
            self.init_mid(init_row)

    # noinspection PyTypeChecker
    def init_topbot(self, border_row):
        """fills the top and bottom row with GameCells and BorderCells"""

        if border_row == 0 or border_row == 11:
            self._board[border_row].append(BorderCell("-X-"))
            for border_col in range(1, 11):
                if border_col == 10:
                    self._board[border_row].append(BorderCell("C" + str(border_col)))
                else:
                    self._board[border_row].append(BorderCell("C0" + str(border_col)))
            self._board[border_row].append(BorderCell("-X-"))

    # noinspection PyTypeChecker
    def init_mid(self, mid_row):
        """fills the middle rows with GameCells and BorderCells"""

        if mid_row == 10:
            self._board[mid_row].append(BorderCell("R" + str(mid_row)))
            for mid_col in range(10):
                self._board[mid_row].append(GameCell())
            self._board[mid_row].append(BorderCell("R" + str(mid_row)))
        else:
            self._board[mid_row].append(BorderCell("R0" + str(mid_row)))
            for mid_col in range(10):
                self._board[mid_row].append(GameCell())
            self._board[mid_row].append(BorderCell("R0" + str(mid_row)))

    def set_mines(self):
        """places mines on the game board"""

        placed_mines = 0
        while placed_mines < self._mine_count:
            mine_row = random.randint(1, 10)
            mine_col = random.randint(1, 10)
            if not self._board[mine_row][mine_col].is_mine():
                self._board[mine_row][mine_col].set_mine()
                placed_mines += 1

    def place_hints(self):
        """places the hint numbers around each mine"""

        for game_row in range(1, 11):
            for game_col in range(1, 11):
                if self._board[game_row][game_col].is_mine():
                    self.mine_surround(game_row, game_col)

    def mine_surround(self, mine_row: int, mine_col: int):
        """function that takes a cell with a mine and updates the cells around it with numbers"""

        # increase top
        self.increase_cell_counter(self._board[mine_row - 1][mine_col])
        # increase right
        self.increase_cell_counter(self._board[mine_row][mine_col + 1])
        # increase left
        self.increase_cell_counter(self._board[mine_row][mine_col - 1])
        # increase bottom
        self.increase_cell_counter(self._board[mine_row + 1][mine_col])
        # increase top-left
        self.increase_cell_counter(self._board[mine_row + 1][mine_col - 1])
        # increase top-right
        self.increase_cell_counter(self._board[mine_row + 1][mine_col + 1])
        # increase bottom-left
        self.increase_cell_counter(self._board[mine_row - 1][mine_col - 1])
        # increase bottom-right
        self.increase_cell_counter(self._board[mine_row - 1][mine_col + 1])

    def increase_cell_counter(self, counter_cell: GameCell):
        """takes a cell as parameter and updates the hint counter
        does nothing if the cell is a BorderCell, or has a mine
        :type counter_cell: GameCell"""

        if counter_cell.is_mine() or counter_cell is BorderCell:
            return
        else:
            counter_cell.increase_count()

    def reveal_cell(self, reveal_row, reveal_col):
        """reveals the given cell"""

        if self._board[reveal_row][reveal_col].is_revealed():
            raise InputRevealError
        elif not self._board[reveal_row][reveal_col].has_count() and not self._board[reveal_row][reveal_col].is_mine():
            self.reveal_expand(reveal_row, reveal_col)
        else:
            self._board[reveal_row][reveal_col].reveal()

    def reveal_expand(self, expand_row, expand_col):
        """if the user selects a blank cell, then this recursive function will reveal all the neighboring blanks"""

        if self._board[expand_row][expand_col].is_border():
            return
        elif self._board[expand_row][expand_col].is_flag():
            return
        elif self._board[expand_row][expand_col].is_revealed():
            return
        elif self._board[expand_row][expand_col].has_count():
            self._board[expand_row][expand_col].reveal()
            return
        else:
            self._board[expand_row][expand_col].reveal()
            # expand top
            self.reveal_expand(expand_row - 1, expand_col)
            # expand right
            self.reveal_expand(expand_row, expand_col + 1)
            # expand left
            self.reveal_expand(expand_row, expand_col - 1)
            # expand bottom
            self.reveal_expand(expand_row + 1, expand_col)

    def flag_cell(self, flag_row, flag_col):
        """places a flag on a cell so it cannot be revealed"""

        if self._board[flag_row][flag_col].is_flag():
            raise InputFlagError
        else:
            self._board[flag_row][flag_col].flag()

    def unflag_cell(self, unflag_row, unflag_col):
        """to be used with the get_input function. removes a flag from a cell so that it can be revealed"""

        if not self._board[unflag_row][unflag_col].is_flag():
            raise InputUnflagError
        else:
            self._board[unflag_row][unflag_col].unflag()

    def user_action(self, act_list):
        """gets all the user inputs and executes the corresponding action"""

        self._turn_count += 1
        act_row = int(act_list[0])
        act_col = int(act_list[1])
        act_opt = act_list[2]

        if act_opt:
            if act_opt.upper() == "F":
                try:
                    self.flag_cell(act_row, act_col)
                except InputFlagError:
                    raise
            elif act_opt.upper() == "U":
                try:
                    self.unflag_cell(act_row, act_col)
                except InputUnflagError:
                    raise
        else:
            try:
                self.reveal_cell(act_row, act_col)
            except InputRevealError:
                raise

    def print_board(self):
        """prints the game board"""

        print("Turn#: " + str(self._turn_count))
        for whole_row in range(0, 12):
            for whole_col in range(0, 12):
                if whole_col == 11:
                    print(self._board[whole_row][whole_col]._display)
                else:
                    print(self._board[whole_row][whole_col]._display, end="")
        print("")

    def get_input(self):
        """gets user input for the row and column number"""

        user_input = input("Please enter the row and column number: ").split()
        if len(user_input) == 2:
            user_input.append(None)

        try:
            self.check_input_list(user_input)
        except InputCheatError:
            raise
        except InputLengthError:
            raise
        except InputTypeError:
            raise
        except InputNumError:
            raise
        except InputOptionError:
            raise
        except InputFlagError:
            raise
        except InputUnflagError:
            raise
        except InputRevealError:
            raise

        return user_input

    def check_input_list(self, input_list):
        """checks number of strings the user inputted and that the row and column are numbers not letters"""

        if len(input_list) == 0 or len(input_list) > 3:
            raise InputLengthError
        if len(input_list) == 1:
            try:
                self.check_cheat_input(input_list[0])
                return
            except InputCheatError:
                raise
        try:
            user_row = int(input_list[0])
            user_col = int(input_list[1])
            user_opt = input_list[2]
            self.check_input_strings(user_row, user_col, user_opt)
        except ValueError:
            raise InputTypeError
        except InputNumError:
            raise
        except InputOptionError:
            raise

    def check_input_strings(self, s_row, s_col, s_opt):
        """checks row and col so that they are integers within 1-10 and that the option is a F or U"""

        if s_row < 1 or s_row > 10:
            raise InputNumError
        if s_col < 1 or s_col > 10:
            raise InputNumError
        if s_opt is not None:
            if s_opt.upper() != "F" and s_opt.upper() != "U":
                raise InputOptionError

    def check_cheat_input(self, cheat_string):
        """if the user only entered 1 string, check if it is a valid cheat code"""

        if cheat_string != "showall" and cheat_string != "winpls" and cheat_string != "reset":
            raise InputCheatError

    def activate_cheat(self, cheat_code):
        """takes a verified cheat string and activates the corresponding cheat"""

        if cheat_code == "showall":
            print("")
            self.print_cheat_board()
            print("")
        elif cheat_code == "winpls":
            self.cheat_reveal()
        elif cheat_code == "reset":
            reset_script()

    def print_cheat_board(self):
        """prints a board with all the mines (i.e. removes fog of war). does not affect the board in play"""

        for cheat_row in range(0, 12):
            for cheat_col in range(0, 12):
                cheat_cell = self._board[cheat_row][cheat_col]
                if cheat_col == 11:
                    if cheat_cell.is_mine():
                        print("[ * ]")
                    # below option used in debugging to check the hint numbers are displayed properly
                    # elif cheat_cell.has_count():
                    #     print("[ " + str(cheat_cell._counter) + " ]")
                    else:
                        print(self._board[cheat_row][cheat_col]._display)
                else:
                    if cheat_cell.is_mine():
                        print("[ * ]", end="")
                    # below option used in debugging to check the hint numbers are displayed properly
                    # elif cheat_cell.has_count() and not cheat_cell.is_border():
                    #     print("[ " + str(cheat_cell._counter) + " ]", end="")
                    else:
                        print(self._board[cheat_row][cheat_col]._display, end="")

    def cheat_reveal(self):
        """reveals every cell that does not contain a mine (this gives you an automatic win)"""

        for cheat_row in range(0, 12):
            for cheat_col in range(0, 12):
                cheat_cell = self._board[cheat_row][cheat_col]
                if cheat_cell is not BorderCell and not cheat_cell.is_mine():
                    cheat_cell.reveal()

    def get_board(self):
        """returns the current game board"""

        return self._board

    def verify_board(self, verify_board):
        """takes the current game board as input and verifies the state of the game"""

        revealed_count = 0
        for v_row in range(1, 11):
            for v_col in range(1, 11):
                if verify_board[v_row][v_col].is_mine() and verify_board[v_row][v_col].is_revealed():
                    self.set_loss()
                    self.set_game_over()
                elif verify_board[v_row][v_col].is_revealed():
                    revealed_count += 1

        if revealed_count == 90:
            self.set_win()
            self.set_game_over()

def print_welcome():
    """prints the welcome message to start the game"""

    print("\n")
    print("WELCOME to the best edition of Minesweeper ever created!")
    print("Instructions: After each prompt type the row number followed by the column number separated by a space.")
    print("Type '"'F'"' after the row and column to flag a cell (to prevent it from being revealed)")
    print("Type '"'U'"' after the row and column to un-flag a cell")
    print("Example input: 8 10 F \n")

def print_win():
    """prints the win message"""
    print("              _________________")
    print(" /\__/\     /")
    print("(  ´∀`)  <  a winner is you!!")
    print("(       )   \_________________")
    print(" |      |")
    print("(___)___)")
    print("\n")


def print_loss():
    """prints the loss message"""

    print("***********************************************************")
    print("")
    print("                        YOU DIED")
    print("")
    print("***********************************************************")
    print("\n")

def reset_script():
    """calls minesweeper script again to restart with a new process"""
    call(["python", "minesweeper-branch.py"])


if __name__ == "__main__":
    game = Minesweeper()
    game.set_mines()
    game.place_hints()
    print_welcome()
    game.print_board()

    while game.still_playing():
        while True:
            try:
                game_input = game.get_input()
                if len(game_input) == 1:
                    game.activate_cheat(game_input[0])
                else:
                    game.user_action(game_input)
            except InputCheatError:
                print("You entered an invalid cheat code")
                continue
            except InputLengthError:
                print("You entered an invalid number of strings")
                continue
            except InputTypeError:
                print("You entered an invalid row/column string")
                continue
            except InputNumError:
                print("You entered a row/column number that is out of bounds")
                continue
            except InputOptionError:
                print("You entered an invalid option string")
                continue
            except InputFlagError:
                print("That cell is already flagged")
                continue
            except InputUnflagError:
                print("That cell is already un-flagged")
                continue
            except InputRevealError:
                print("That cell has already been revealed")
                continue
            break

        print("")
        game.print_board()

        game.verify_board(game.get_board())

    if not game.still_playing():
        if game.game_result():
            print_win()
        else:
            print_loss()

    # ask player if they want to restart
    while True:
        reset_choice = input("Would you like to play again? Y/N ")
        if reset_choice.upper() == "Y" or reset_choice.upper() == "N":
            break

    if reset_choice.upper() == "Y":
        reset_script()
    else:
        sys.exit()
