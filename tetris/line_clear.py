from enum import Enum


class LineClear(Enum):
    """Types of line clear. Attack, combo, and score tables should include entries for every type."""

    SINGLE = 1
    DOUBLE = 2
    TRIPLE = 3
    TETRIS = 4

    # TODO
    # T_SPIN_SINGLE = 6
    # T_SPIN_DOUBLE = 7
    # T_SPIN_TRIPLE = 8

    PERFECT_CLEAR = 10
