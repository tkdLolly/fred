from enum import Enum


class Control(Enum):
    """Game controls."""

    # Horizontal movement
    MOVE_LEFT = 0
    MOVE_RIGHT = 1

    # Downward movement
    SOFT_DROP = 10
    HARD_DROP = 11

    # Rotation
    ROTATE_CW = 20
    ROTATE_CCW = 21
    ROTATE_180 = 22

    # Hold
    HOLD = 30
