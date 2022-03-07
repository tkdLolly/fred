from itertools import permutations

from cell import Cell
from rotation import Rotation
from utils import subtract_lists_of_offsets


class RotationSystem:
    """
    A rotation system includes specification for piece spawning positions and rotation kick checks.
    The Field is assumed to always be 10 wide and 24 high.
    """

    @staticmethod
    def get_spawn_offsets(tetromino):
        """
        Return a tuple of offsets (offset_row, offset_column) from the top left of the Field
        to the top left of the Tetromino matrix that specifies where a Tetromino should spawn in a Field.

        For example,
        spawning an S tetromino with offsets of (1, 4) would result in the following Field:
        ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
        │   ┆   ┆   ┆   ┆   ┆   ┆   ┆   ┆   ┆   │   0 - 10
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆   │  10 - 20
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆ 0 ┆ 0 ┆ 1 ┆ 1 ┆ 0 ┆   │  20 - 30
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆ 0 ┆ 1 ┆ 1 ┆ 0 ┆ 0 ┆   │  30 - 40  First visible row
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆   │  40 - 50
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 ┆   │  50 - 60
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │   ┆   ┆   ┆   ┆   ┆   ┆   ┆   ┆   ┆   │  60 - 70
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        """
        pass

    @staticmethod
    def get_spawn_rotation():
        """Return the default rotation state of Tetrominos when they spawn."""
        pass

    @staticmethod
    def get_kick_tests(tetromino, control):
        """Return kick test offsets (dx, dy) for TETROMINO after the rotation specified by CONTROL."""
        pass


class SuperRotationSystem(RotationSystem):
    """SRS includes specification for piece spawning positions and rotation kick checks."""

    @staticmethod
    def get_spawn_offsets(tetromino):
        """The offsets in SRS are static."""
        return 0, 2

    @staticmethod
    def get_spawn_rotation():
        """The default rotation state in SRS is always NORTH."""
        return Rotation.NORTH

    #############################
    # SRS kick test offset data #
    #############################
    # The following is provided by https://harddrop.com/wiki/SRS
    JLSTZ_offset_data = {
        Rotation.NORTH: [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
        Rotation.EAST: [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
        Rotation.SOUTH: [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
        Rotation.WEST: [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
    }
    I_offset_data = {
        Rotation.NORTH: [(0, 0), (-1, 0), (2, 0), (-1, 0), (2, 0)],
        Rotation.EAST: [(-1, 0), (0, 0), (0, 0), (0, -1), (0, 2)],
        Rotation.SOUTH: [(-1, -1), (1, -1), (-2, -1), (1, 0), (-2, 0)],
        Rotation.WEST: [(0, -1), (0, -1), (0, -1), (0, 1), (0, -2)]
    }
    O_offset_data = {
        Rotation.NORTH: [(0, 0)],
        Rotation.EAST: [(0, 1)],
        Rotation.SOUTH: [(-1, 1)],
        Rotation.WEST: [(-1, 0)]
    }

    # Maps from (old_rotation, new_rotation) to list of kick translations (offset_row, offset_column)
    JLSTZ_kicks = dict()
    I_kicks = dict()
    O_kicks = dict()

    # Generate all kick translations
    for old_rotation, new_rotation in permutations(Rotation, 2):
        if new_rotation is old_rotation.rotate_180():   # SRS has no 180 kicks
            JLSTZ_kicks[(old_rotation, new_rotation)] = []
            I_kicks[(old_rotation, new_rotation)] = []
            O_kicks[(old_rotation, new_rotation)] = []
            continue

        old_offsets = JLSTZ_offset_data[old_rotation]
        new_offsets = JLSTZ_offset_data[new_rotation]
        JLSTZ_kicks[(old_rotation, new_rotation)] = subtract_lists_of_offsets(old_offsets, new_offsets)

        old_offsets = I_offset_data[old_rotation]
        new_offsets = I_offset_data[new_rotation]
        I_kicks[(old_rotation, new_rotation)] = subtract_lists_of_offsets(old_offsets, new_offsets)

        old_offsets = O_offset_data[old_rotation]
        new_offsets = O_offset_data[new_rotation]
        O_kicks[(old_rotation, new_rotation)] = subtract_lists_of_offsets(old_offsets, new_offsets)

    # Map from Cell to kick dictionary
    tetromino_kicks = {
        Cell.I: I_kicks,
        Cell.J: JLSTZ_kicks,
        Cell.L: JLSTZ_kicks,
        Cell.O: O_kicks,
        Cell.S: JLSTZ_kicks,
        Cell.T: JLSTZ_kicks,
        Cell.Z: JLSTZ_kicks
    }

    @staticmethod
    def get_kick_tests(tetromino, control):
        """Return a list of kick translations (dx, dy) for TETROMINO after the rotation specified by CONTROL."""
        current_rotation = tetromino.rotation
        new_tetromino = tetromino.rotate(control)
        new_rotation = new_tetromino.rotation
        kicks = SuperRotationSystem.tetromino_kicks[tetromino.cell]
        return kicks[(current_rotation, new_rotation)]
