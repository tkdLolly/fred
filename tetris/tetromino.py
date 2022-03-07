from cell import Cell
from control import Control
from rotation import Rotation

# Cells with a corresponding Tetromino
tetromino_cells = {Cell.I, Cell.J, Cell.L, Cell.O, Cell.S, Cell.T, Cell.Z}


########################
# 5x5 matrix utilities #
########################

def rotate_cw(matrix):
    """Rotate MATRIX clockwise and return it."""
    new_matrix = []
    matrix = matrix[::-1]
    for i in range(5):
        new_matrix.append([row[i] for row in matrix])
    return new_matrix


def rotate_ccw(matrix):
    """Rotate MATRIX counterclockwise and return it."""
    new_matrix = []
    for i in reversed(range(5)):  # 4, 3, 2, 1, 0
        new_matrix.append([row[i] for row in matrix])
    return new_matrix


def rotate_180(matrix):
    """Rotate MATRIX by 180 degrees and return it."""
    return [row[::-1] for row in matrix][::-1]


# 5x5 matrices (row by row) marking nonempty Cells of Tetrominos in default rotation NORTH state
templates = {
    Cell.I: [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.L: [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.O: [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.Z: [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.T: [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.J: [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
    Cell.S: [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Dictionary of Cell to corresponding list of Tetrominos in order of rotation 180, 270, 0, 90
tetrominos = dict()

# Match Controls to Rotations
controls_to_rotations = {
    Control.ROTATE_CW: Rotation.rotate_cw,
    Control.ROTATE_CCW: Rotation.rotate_ccw,
    Control.ROTATE_180: Rotation.rotate_180
}


class Tetromino:
    """
    A tetromino consisting of four cells.
    There are altogether seven types of tetrominos (T, I, L, J, S, Z, O).
    """

    def __init__(self, cell, rotation, matrix):
        """
        Each tetromino is initialized according to type of cell state.
        Each is associated with a 5x5 matrix indicating which cells it fills by default (rotation NORTH).
        It also stores its current rotation state.

        For example,
        the T piece is linked to Cell.T and the following matrix by default:
        ┌───┬───┬───┬───┬───┐
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 1 ┆ 0 ┆ 0 │
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 1 ┆ 1 ┆ 1 ┆ 0 │
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │
        └───┴───┴───┴───┴───┘
        """
        self.cell = cell
        self.rotation = rotation
        self.matrix = matrix

    def __eq__(self, other):
        assert isinstance(other, Tetromino)
        return self.cell is other.cell and self.rotation is other.rotation

    def __hash__(self):
        return self.cell + self.rotation * 9

    @staticmethod
    def get(cell, rotation):
        """Return the Tetromino specified by CELL and ROTATION."""
        return tetrominos[cell][rotation]

    def rotate_cw(self):
        """Return me rotated clockwise."""
        return self.get(self.cell, self.rotation.rotate_cw())

    def rotate_ccw(self):
        """Rotate me rotated counterclockwise."""
        return self.get(self.cell, self.rotation.rotate_ccw())

    def rotate_180(self):
        """Return me rotated 180 degrees. Not all Tetris games support this rotation."""
        return self.get(self.cell, self.rotation.rotate_180())

    def rotate(self, control):
        """Return me after rotation specified by CONTROL."""
        new_rotation = controls_to_rotations[control](self.rotation)
        return self.get(self.cell, new_rotation)

    def get_nonempty_coords(self):
        """
        Return the set of coordinates (row, column) of Cells of my matrix.

        For example:
        For the matrix below, the set {(1, 3), (2, 2), (2, 3), (2, 4)} is returned.
        ┌───┬───┬───┬───┬───┐
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │ Row 0
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 1 ┆ 0 ┆ 0 │ Row 1
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 1 ┆ 1 ┆ 1 ┆ 0 │ Row 2
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │ Row 3
        ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
        │ 0 ┆ 0 ┆ 0 ┆ 0 ┆ 0 │ Row 4
        └───┴───┴───┴───┴───┘
          0   1   2   3   4   Columns
        """
        nonempty_cells = set()
        for r in range(5):
            row = self.matrix[r]
            for c in range(5):
                if row[c]:
                    nonempty_cells.add((r, c))
        return nonempty_cells


# Generate all possible Tetrominos in all possible rotation states
for cell in tetromino_cells:
    template = templates[cell]
    tetromino_dict = {
        Rotation.SOUTH: Tetromino(cell, Rotation.SOUTH, rotate_180(template)),
        Rotation.WEST: Tetromino(cell, Rotation.WEST, rotate_ccw(template)),
        Rotation.NORTH: Tetromino(cell, Rotation.NORTH, template),
        Rotation.EAST: Tetromino(cell, Rotation.EAST, rotate_cw(template))
    }
    tetrominos[cell] = tetromino_dict
