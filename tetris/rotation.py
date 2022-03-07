from enum import Enum


class Rotation(Enum):
    """
    There are altogther four rotation states, one for each cardinal direction.
    """
    SOUTH = 0
    WEST = 1
    NORTH = 2
    EAST = 3

    def rotate_cw(self):
        """Return the rotation state after rotating clockwise."""
        return Rotation((self.value + 1) % 4)

    def rotate_ccw(self):
        """Return the rotation state after rotating counterclockwise."""
        return Rotation((self.value - 1) % 4)

    def rotate_180(self):
        """Return the rotation state after rotating 180 degrees."""
        return Rotation((self.value + 2) % 4)