from enum import Enum


class Cell(Enum):
    """
    A Cell is a unit in a Field representing one of nine types of block states
    including seven types of tetrominos (T, I, L, J, S, Z, O),
    an empty state, and a garbage state.

    This is not to be confused with an entire Tetromino.
    """
    EMPTY = 0  # EMPTY
    I = 1
    L = 2
    O = 3
    Z = 4
    T = 5
    J = 6
    S = 7
    GREY = 8  # GREY / GARBAGE

    def __repr__(self):
        return self.name

    def __str__(self):
        if self is Cell.GREY:
            return "-"
        if self is Cell.EMPTY:
            return " "
        return self.name

    def is_empty(self):
        """Return True if I am EMPTY or False otherwise."""
        return self is Cell.EMPTY