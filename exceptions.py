class InputLengthError(Exception):
    """exception when the user enters more than 3 strings (separated by space) or empty string"""
    pass


class InputTypeError(Exception):
    """exception when the user enters letters for row or column"""
    pass


class InputOptionError(Exception):
    """exception when the user enters something other than F or U for the option"""
    pass


class InputNumError(Exception):
    """exception when the user enters a row or column number that is out of bounds of the game board"""
    pass


class InputCheatError(Exception):
    """exception when the user enters an invalid cheat code"""
    pass


class InputFlagError(Exception):
    """exception when a cell is already flagged"""
    pass


class InputUnflagError(Exception):
    """exception when a cell is already unflagged"""
    pass


class InputRevealError(Exception):
    """exception when a cell is already revealed"""
    pass
