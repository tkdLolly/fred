from copy import deepcopy

from cell import Cell
from control import Control
from rotation_system import SuperRotationSystem
from tetromino import Tetromino
from utils import flatten, subtract_lists_of_offsets, bfs


class Field:
    """
    The Field is a 10 wide, 24 high matrix of Cells.
    Rows 3 to 22 comprise the visible 20-row field.
    Rows 0 to 2 reside above the visible field and row 23 lies below.

      0   1   2   3   4   5   6   7   8   9   Column
    ┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┐
    │  0┆  1┆  2┆  3┆  4│  5┆  6┆  7┆  8┆  9│ Row  0    Hidden row
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
    │ 10┆ 11┆ 12┆ 13┆ 14│ 15┆ 16┆ 17┆ 18┆ 19│ Row  1    Hidden row
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
    │ 20┆ 21┆ 22┆ 23┆ 24│ 25┆ 26┆ 27┆ 28┆ 29│ Row  2    Hidden row
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
    │ 30┆ 31┆ 32┆ 33┆ 34│ 35┆ 36┆ 37┆ 38┆ 39│ Row  3    Top of visible field
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
                   Rows 4 - 21                          Visible field
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
    │220┆221┆222┆223┆224│225┆226┆227┆228┆229│ Row 22    Bottom of visible field
    ├┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┼┄┄┄┤
    │230┆231┆232┆233┆234│235┆236┆237┆238┆239│ Row 23    Hidden row
    └───┴───┴───┴───┴───┴───┴───┴───┴───┴───┘
    """
    width = 10
    height = 24

    def __init__(self, field=None):
        """
        Initialise my field to be a list of lists of Cells given by FIELD.
        If FIELD is not provided, initialise my field to be an empty Field.
        """
        if field is None:
            # Use 24 rows of 10 long lists
            self.field = [[Cell.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        else:
            # Copy the provided FIELD
            self.field = deepcopy(field)

    def __repr__(self):
        from fumen import Fumen     # bypass circular dependency
        return Fumen.encode([self])

    def __eq__(self, other):
        """Return True if the OTHER field has the same field as mine."""
        assert isinstance(other, Field)
        return self.field == other.field

    def __hash__(self):
        """Returns a unique hash for different fields"""
        hash = 0
        for cell in flatten(self.field):
            hash *= 9   # 9 types of Cells
            hash += cell.value
        return hash

    ##############################
    # Individual Cell operations #
    ##############################

    def get_cell(self, row, column):
        """Return the Cell at ROW and COLUMN."""
        return self.field[row][column]

    def set_cell(self, row, column, cell):
        """Set the Cell specified by ROW and COLUMN to CELL."""
        assert isinstance(cell, Cell)
        self.field[row][column] = cell

    def is_cell_empty(self, row, column):
        """Return True if the Cell at ROW and COLUMN of my Field is empty or False otherwise."""
        return self.field[row][column].is_empty()

    ##################
    # Row operations #
    ##################

    def get_row(self, row):
        """
        Get the list of Blocks in the ROW of the field.
        The field has 24 rows starting with the 0th row at the top
        ending with the 23rd row at the bottom.
        """
        assert 0 <= row < self.height
        return self.field[row]

    def is_row_empty(self, row):
        """Return True if the ROW of the field is all empty or False otherwise."""
        return all(cell.is_empty() for cell in self.get_row(row))

    def is_row_filled(self, row):
        """Return True if the ROW of the field is all filled i.e. no Cell in the ROW is EMPTY."""
        return not any(cell.is_empty() for cell in self.get_row(row))

    def line_clear(self):
        """
        Remove completely filled rows from my field and add empty rows from the top of my field.
        Return the number of rows removed.
        """
        new_field = []
        lines_cleared = 0
        for row in range(self.height):
            if not self.is_row_filled(row):
                new_field.append(self.get_row(row))
            else:
                lines_cleared += 1
                new_field.insert(0, [Cell.EMPTY for _ in range(self.width)])
        self.field = new_field
        return lines_cleared

    #################################
    # Convert to FieldWithTetromino #
    #################################

    def spawn_tetromino(self, cell, rotation_system=SuperRotationSystem):
        """Return a FieldWithTetromino object using ROTATION_SYSTEM with the Tetromino linked to CELL and my field."""
        tetromino = Tetromino.get(cell, rotation_system.get_spawn_rotation())
        return FieldWithTetromino(tetromino, self.field, rotation_system)

    ###########
    # Utility #
    ###########

    def is_visibly_empty(self):
        """Return True if the visible field is completely empty or False otherwise."""
        return all(self.is_row_empty(row) for row in range(3, self.height - 1))

    def index_to_coords(self, index):
        """Return the row and column corresponding to INDEX from 0 to 239 inclusive."""
        row = index // self.width
        column = index % self.width
        return row, column

    def convert_cells_to_grey(self):
        """Return a new Field where all nonempty cells are converted to GREY."""
        new_field = Field(self.field)
        for row in range(new_field.height):
            for column in range(new_field.width):
                if not new_field.is_cell_empty(row, column):
                    new_field.set_cell(row, column, Cell.GREY)
        return new_field

    def get_bottommost_visible_empty_row(self):
        for row in reversed(range(self.height - 1)):
            if self.is_row_empty(row):
                return row
        return -1


class FieldWithTetromino(Field):
    """A Field with a Tetromino yet to be placed. Allows the Tetromino to be moved before being placed."""

    def __init__(self, tetromino, field=None, rotation_system=SuperRotationSystem):
        """
        Initializes a Field with a Tetromino requires a RotationSystem to handle spawning and rotations.
        SRS is used by default.
        Copies are made with deepcopy(self).
        """
        super().__init__(field)
        self.tetromino = tetromino
        self.rotation_system = rotation_system
        self.offset_row, self.offset_column = self.rotation_system.get_spawn_offsets(tetromino)

    def __eq__(self, other):
        assert isinstance(other, FieldWithTetromino)
        return self.field == other.field and self.tetromino == other.tetromino and \
            (self.offset_row, self.offset_column) == (other.offset_row, other.offset_column) and \
            self.rotation_system == other.rotation_system

    def __hash__(self):
        hash = 0
        for cell in flatten(self.field):
            hash *= 9   # 9 types of Cells
            hash += cell.value
        hash *= self.height
        hash += self.offset_row
        hash *= self.width
        hash += self.offset_column
        return hash

    #####################
    # Tetromino control #
    #####################

    def execute_control(self, control, ignore_lines_cleared=True):
        """
        Execute the game control CONTROL.
        Return a new FieldWithTetromino with its Tetromino moved or rotated and its offsets adjusted accordingly
        or a tuple of the resulting Field and the number of lines cleared
            if the Control is HARD_DROP and IGNORE_LINES_CLEARED is False.
        """
        assert control in self._controls_to_execute_fns
        field = self._controls_to_execute_fns[control](self)
        lines_cleared = field.line_clear()
        if Control is Control.HARD_DROP and not ignore_lines_cleared:
            return field, lines_cleared
        return field

    def execute_controls(self, list_of_controls, ignore_lines_cleared=True):
        """
        All Controls in LIST_OF_CONTROLS are executed in that order until the list ends or HARD_DROP is encountered.
        Return the resulting FieldWithTetromino
        or a tuple of the Field and the number of lines cleared
            if HARD_DROP is encountered and IGNORE_LINES_CLEARED is False.
        """
        field = self
        for control in list_of_controls:
            field = field.execute_control(control, ignore_lines_cleared)
            if control is Control.HARD_DROP:
                break
        return field

    #############
    # Utilities #
    #############

    def get_tetromino_nonempty_coords(self):
        """Return a set of (row, column) coordinates of the cells of my Tetromino using my offsets."""
        return self._get_tetromino_nonempty_coords_with_offsets(self.offset_row, self.offset_column)

    def is_valid_placement(self):
        """Return True if my Tetromino is currently in a position where it can be placed on the spot."""

        def is_tetromino_floating():
            """Returns True if my Tetromino is floating with my offsets. My Tetromino should not be placed if floating."""
            tetromino_coords = self.get_tetromino_nonempty_coords()
            one_below_tetromino_coords = subtract_lists_of_offsets(tetromino_coords, [(-1, 0) for _ in range(4)])
            for row, column in one_below_tetromino_coords:
                if (row, column) in tetromino_coords:
                    continue
                elif row == self.height - 1 or not self.is_cell_empty(row, column):
                    return False
            return True

        return self.are_current_offsets_valid() and not is_tetromino_floating()

    def are_current_offsets_valid(self):
        return self._are_offsets_valid(self.offset_row, self.offset_column)

    def get_possible_fields(self, convert_to_grey=False):
        """
        Return the set of all possible FieldWithTetrominos where the Tetromino can be placed on the spot
        (Tetromino is not floating and is not overlapping with existing non-empty Cells)
        that are attainable by controlling my Tetromino from my current position.
        """
        soft_drops = max(0, self.get_bottommost_visible_empty_row() - self.offset_row - 2)
        start_field = self.execute_controls([Control.SOFT_DROP for _ in range(soft_drops)])
        list_of_actions = [
            lambda fwt: fwt._execute_move_left(),
            lambda fwt: fwt._execute_move_right(),
            lambda fwt: fwt._execute_soft_drop(),
            lambda fwt: fwt._execute_hard_drop(),
            lambda fwt: fwt._execute_rotate_cw(),
            lambda fwt: fwt._execute_rotate_ccw()
            # lambda fwt: fwt._execute_rotate_180()   # Not in SRS
        ]
        fwts = bfs(start_field, list_of_actions)
        valid_placement_fwts = filter(lambda fwt: fwt.is_valid_placement(), fwts)
        fields = set()
        for fwt in valid_placement_fwts:
            field = fwt._place_tetromino()
            field.line_clear()
            fields.add(field)
        if convert_to_grey:
            return set(field.convert_cells_to_grey() for field in fields)
        return fields

    def get_possible_fields_below_height(self, height, convert_to_grey=False):
        """Same as get_possible_fields but limit fields to HEIGHT. For example, PCMode is limited to height 4."""
        possible_fields = self.get_possible_fields(convert_to_grey)
        return {f for f in possible_fields if f.get_bottommost_visible_empty_row() + height + 2 >= f.height}

    ###########
    # Private #
    ###########

    # Tetromino offset utilities
    def _get_tetromino_nonempty_coords_with_offsets(self, offset_row, offset_column):
        """Return a set of (row, column) coordinates of the cells of my Tetromino using OFFSETS."""
        tetromino_coords = self.tetromino.get_nonempty_coords()
        offset_coords = set()
        for row, column in tetromino_coords:
            offset_coords.add((row + offset_row, column + offset_column))
        return offset_coords

    def _are_offsets_valid(self, offset_row, offset_column):
        """Return True if OFFSETS keep my Tetromino within my Field and without overlapping with nonempty Cells."""

        def is_tetromino_contained_in_field_with_offsets(offset_row, offset_column):
            """Return True if OFFSETS keep my Tetromino within my Field."""
            tetromino_coords = self._get_tetromino_nonempty_coords_with_offsets(offset_row, offset_column)
            for row, column in tetromino_coords:
                if not (0 <= row < self.height - 1 and 0 <= column < self.width):  # The last row is below the field
                    return False
            return True

        def is_tetromino_obstructed_with_offsets(offset_row, offset_column):
            """
            Return True if OFFSETS causes my Tetromino to overlap with non-empty Cells of my Field and False otherwise.
            """
            coords = self._get_tetromino_nonempty_coords_with_offsets(offset_row, offset_column)
            for row, column in coords:
                if not self.is_cell_empty(row, column):
                    return True
            return False

        return is_tetromino_contained_in_field_with_offsets(offset_row, offset_column) and \
               not is_tetromino_obstructed_with_offsets(offset_row, offset_column)

    # Convert to Field
    def _place_tetromino(self):
        """
        Place my Tetromino in the position specified by my Offsets.
        Assumes the current position is valid. My Tetromino is possibly floating.
        Returns the new Field object with my Tetromino placed in the current location.
        Does NOT clear lines.
        """
        tetromino_coords = self.get_tetromino_nonempty_coords()
        new_field = Field(self.field)
        for row, column in tetromino_coords:
            new_field.set_cell(row, column, self.tetromino.cell)
        return new_field

    # Control handling
    def _adopt_offsets_if_valid(self, offset_row, offset_column):
        """
        Return True and set my offsets to OFFSETS if doing so does not cause my Tetromino to overlap with
        nonempty Cells in my Field or return False and keep my original offsets otherwise.
        """
        if self._are_offsets_valid(offset_row, offset_column):
            self.offset_row, self.offset_column = offset_row, offset_column
            return True
        return False

    def _execute_translation(self, new_offset_row, new_offset_column):
        """Return a new FieldWithTetromino with my Tetromino moved appropriately if possible by adjusting offsets."""
        new_field = deepcopy(self)
        new_field._adopt_offsets_if_valid(new_offset_row, new_offset_column)
        return new_field

    def _execute_rotation(self, control):
        """Return a new FieldWithTetromino with my Tetromino rotated and kicked appropriately."""
        assert control in {Control.ROTATE_CW, Control.ROTATE_CCW, Control.ROTATE_180}
        kicks = self.rotation_system.get_kick_tests(self.tetromino, control)
        for column_kick, row_kick in kicks:
            new_field = FieldWithTetromino(self.tetromino.rotate(control), self.field, self.rotation_system)
            if new_field._adopt_offsets_if_valid(self.offset_row + row_kick, self.offset_column + column_kick):
                return new_field
        return deepcopy(self)   # All kick tests failed

    def _execute_move_left(self):
        """Return a new FieldWithTetromino with my Tetromino moved left one Cell if possible by adjusting offsets."""
        return self._execute_translation(self.offset_row, self.offset_column - 1)

    def _execute_move_right(self):
        """Return a new FieldWithTetromino with my Tetromino moved right one Cell if possible by adjusting offsets."""
        return self._execute_translation(self.offset_row, self.offset_column + 1)

    def _execute_soft_drop(self):
        """Return a new FieldWithTetromino with my Tetromino moved down one Cell if possible by adjusting offsets."""
        return self._execute_translation(self.offset_row + 1, self.offset_column)

    def _execute_hard_drop(self):
        """
        Return a new FieldWithTetromino with my Tetromino moved as far down as possible by adjusting offsets.
        Does NOT place my Tetromino.
        """
        new_field = deepcopy(self)
        for row in range(1, self.height):
            if not new_field._adopt_offsets_if_valid(self.offset_row + row, self.offset_column):
                return new_field

    def _execute_hard_drop_and_place_tetromino(self):
        """Returns a new Field with my Tetromino moved as far down as possible by adjusting offsets then placed."""
        new_field = self._execute_hard_drop()
        return new_field._place_tetromino()

    def _execute_rotate_cw(self):
        """Return a new FieldWithTetromino with my Tetromino rotated clockwise and kicked appropriately."""
        return self._execute_rotation(Control.ROTATE_CW)

    def _execute_rotate_ccw(self):
        """Return a new FieldWithTetromino with my Tetromino rotated counterclockwise and kicked appropriately."""
        return self._execute_rotation(Control.ROTATE_CCW)

    def _execute_rotate_180(self):
        """Return a new FieldWithTetromino with my Tetromino rotated 180 degrees and kicked appropriately."""
        return self._execute_rotation(Control.ROTATE_180)

    _controls_to_execute_fns = {
        Control.MOVE_LEFT: _execute_move_left,
        Control.MOVE_RIGHT: _execute_move_right,
        Control.SOFT_DROP: _execute_soft_drop,
        Control.HARD_DROP: _execute_hard_drop_and_place_tetromino,
        Control.ROTATE_CW: _execute_rotate_cw,
        Control.ROTATE_CCW: _execute_rotate_ccw,
        Control.ROTATE_180: _execute_rotate_180
    }
