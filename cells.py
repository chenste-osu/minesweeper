class GameCell:
    """class that represents a cell on the minesweeper board"""

    def __init__(self):
        self._display = "[   ]"
        self._counter = 0
        self._revealed = False
        self._mine = False
        self._border = False
        self._flag = False

    def increase_count(self):
        """increases the counter of the cell"""

        if not self.is_border():
            self._counter += 1

    def reveal(self):
        """reveals the cell (will be printed on game board)"""

        self._revealed = True
        if self.is_mine():
            self._display = "[ * ]"
        elif self._counter > 0 and not self.is_border():
            self._display = "[ " + str(self._counter) + " ]"
        elif not self.is_border():
            self._display = "[ ~ ]"

    def flag(self):
        """sets the cell to be flagged"""

        self._display = "[ F ]"
        self._flag = True

    def unflag(self):
        """un-flags the cell"""

        self._display = "[   ]"
        self._flag = False

    def set_mine(self):
        """sets a mine in the cell"""

        self._mine = True

    def is_mine(self):
        """returns True if the cell has a mine"""

        return self._mine

    def is_border(self):
        """returns True if the cell is a BorderCell"""

        return self._border

    def is_flag(self):
        """returns True if the cell is flagged"""

        return self._flag

    def is_revealed(self):
        """returns True if the cell is revealed"""

        return self._revealed

    def has_count(self):
        """returns True if the cell has a non-zero counter"""

        if self._counter > 0:
            return True

class BorderCell(GameCell):
    """class that represents a cell on the border of the board. these cells only display the row and column numbers"""

    def __init__(self, display_string):
        super().__init__()
        self._display = "[" + display_string + "]"
        self._border = True