import unittest
from copy import deepcopy

from cell import Cell
from control import Control
from field import Field, FieldWithTetromino
from rotation import Rotation
from rotation_system import SuperRotationSystem
from tetromino import Tetromino

SRS = SuperRotationSystem


class FieldTest(unittest.TestCase):
    def test_init_all_empty(self):
        field = Field()
        for row in range(field.height):
            self.assertTrue(field.is_row_empty(row))
            for column in range(field.width):
                self.assertTrue(field.is_cell_empty(row, column))

    def test_set_one_cell_nonempty(self):
        field = Field()

        # Iterate over all coords
        for row in range(field.height):
            for column in range(field.width):
                # Start with an empty field
                self.assertTrue(field.is_cell_empty(row, column))
                self.assertTrue(field.is_row_empty(row))

                # Iterate over all Cells
                for cell in Cell:
                    if cell is Cell.EMPTY:
                        continue  # Skip setting to EMPTY
                    field.set_cell(row, column, cell)  # Set Cell at ROW and COLUMN to nonempty CELL

                    # Iterate over all coords
                    for another_row in range(field.height):
                        for another_column in range(field.width):
                            if another_row == row and another_column == column:
                                self.assertFalse(field.is_cell_empty(another_row, another_column))
                            else:
                                self.assertTrue(field.is_cell_empty(another_row, another_column))
                        if another_row == row:
                            self.assertFalse(field.is_row_empty(another_row))
                        else:
                            self.assertTrue(field.is_row_empty(another_row))

                field.set_cell(row, column, Cell.EMPTY)  # Set Cell at ROW and COLUMN to EMPTY

                # Check field is empty
                for another_row in range(field.height):
                    for another_column in range(field.width):
                        self.assertTrue(field.is_cell_empty(another_row, another_column))
                    self.assertTrue(field.is_row_empty(another_row))

    def test_line_clear(self):
        field = Field()
        for num_rows in range(field.height + 1):
            for row in range(num_rows):
                for column in range(field.width):
                    field.set_cell(row, column, Cell.GREY)
            field.line_clear()
            for row in range(field.height):
                self.assertTrue(field.is_row_empty(row))


class FieldEqualityTest(unittest.TestCase):
    def test_init_equality(self):
        field_1 = Field()
        field_2 = Field()
        self.assertEqual(field_1, field_2)

    def test_set_cells_equality(self):
        field_1 = Field()
        field_2 = Field()
        for row in range(field_1.height):
            for column in range(field_1.width):
                cell = Cell((row + column) % 9)
                field_1.set_cell(row, column, cell)
                field_2.set_cell(row, column, cell)
        self.assertEqual(field_1, field_2)


class FieldConvertToGreyTest(unittest.TestCase):
    def test_init_convert_nothing(self):
        field_1 = Field()
        field_1_converted = field_1.convert_cells_to_grey()
        self.assertEqual(field_1, field_1_converted)

    def test_convert_to_grey(self):
        field_1 = Field()
        field_1_grey = Field()
        for row in range(field_1.height):
            for column in range(field_1.width):
                cell = Cell((row + column) % 9)
                if not cell.is_empty():
                    field_1.set_cell(row, column, cell)
                    field_1_grey.set_cell(row, column, Cell.GREY)
        field_1_converted = field_1.convert_cells_to_grey()
        self.assertEqual(field_1_converted, field_1_grey)


class FieldBottommostVisibleEmptyRowTest(unittest.TestCase):
    def test_init_row_22(self):
        field = Field()
        self.assertEqual(22, field.get_bottommost_visible_empty_row())


class FieldIsVisiblyEmptyTest(unittest.TestCase):
    def test_init_empty(self):
        field = Field()
        self.assertTrue(field.is_visibly_empty())

    def test_drop_I_not_visibly_empty(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.I, SRS)
        field = fwt.execute_control(Control.HARD_DROP)
        self.assertFalse(field.is_visibly_empty())


class FieldWithTetrominoInitTest(unittest.TestCase):
    def test_I_spawn_position(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

    def test_J_spawn_position(self):
        J = Tetromino.get(Cell.J, SRS.get_spawn_rotation())
        field = FieldWithTetromino(J)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 3), (2, 3), (2, 4), (2, 5)})

    def test_L_spawn_position(self):
        L = Tetromino.get(Cell.L, SRS.get_spawn_rotation())
        field = FieldWithTetromino(L)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 5), (2, 3), (2, 4), (2, 5)})

    def test_O_spawn_position(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        field = FieldWithTetromino(O)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

    def test_S_spawn_position(self):
        S = Tetromino.get(Cell.S, SRS.get_spawn_rotation())
        field = FieldWithTetromino(S)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 3), (2, 4)})

    def test_T_spawn_position(self):
        T = Tetromino.get(Cell.T, SRS.get_spawn_rotation())
        field = FieldWithTetromino(T)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (2, 3), (2, 4), (2, 5)})

    def test_Z_spawn_position(self):
        Z = Tetromino.get(Cell.Z, SRS.get_spawn_rotation())
        field = FieldWithTetromino(Z)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 3), (1, 4), (2, 4), (2, 5)})


class FieldWithTetrominoValidOffsetsTest(unittest.TestCase):
    def test_I_valid_offsets_test(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})
        self.assertTrue(field.are_current_offsets_valid())

        # Set orthogonally adjacent Cells to GREY
        for row, column in [(1, 3), (1, 4), (1, 5), (1, 6), (2, 2), (2, 7), (3, 3), (3, 4), (3, 5), (3, 6)]:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        # Check cannot move left
        field.execute_control(Control.MOVE_LEFT)
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        # Check cannot move right
        field.execute_control(Control.MOVE_RIGHT)
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        # Check cannot soft drop
        field.execute_control(Control.SOFT_DROP)
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        # Check adjacent offsets invalid
        field.offset_row -= 1
        self.assertFalse(field.are_current_offsets_valid())
        field.offset_row += 2
        self.assertFalse(field.are_current_offsets_valid())
        field.offset_row -= 1
        field.offset_column -= 1
        self.assertFalse(field.are_current_offsets_valid())
        field.offset_column += 2
        self.assertFalse(field.are_current_offsets_valid())


class FieldWithTetrominoFloatingTest(unittest.TestCase):
    def test_J_WEST_laputa_test(self):
        J = Tetromino.get(Cell.J, SRS.get_spawn_rotation())
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CCW)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (2, 4), (3, 3), (3, 4)})
        for offset_row in range(18):
            field = field.execute_control(Control.SOFT_DROP)
            # self.assertTrue(field._is_tetromino_floating())
            self.assertFalse(field.is_valid_placement())
        field = field.execute_control(Control.SOFT_DROP)
        # self.assertFalse(field._is_tetromino_floating())
        self.assertTrue(field.is_valid_placement())
        field = field.execute_control(Control.SOFT_DROP)
        # self.assertFalse(field._is_tetromino_floating())
        self.assertTrue(field.is_valid_placement())

    def test_S_NORTH_laputa_test(self):
        S = Tetromino.get(Cell.S, SRS.get_spawn_rotation())
        field = FieldWithTetromino(S)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 3), (2, 4)})
        for offset_row in range(19):
            field = field.execute_control(Control.SOFT_DROP)
            # self.assertTrue(field._is_tetromino_floating())
        field = field.execute_control(Control.SOFT_DROP)
        # self.assertFalse(field._is_tetromino_floating())
        self.assertTrue(field.is_valid_placement())
        field = field.execute_control(Control.SOFT_DROP)
        # self.assertFalse(field._is_tetromino_floating())
        self.assertTrue(field.is_valid_placement())

    def test_Z_NORTH_set_and_remove_support_test(self):
        Z = Tetromino.get(Cell.Z, SRS.get_spawn_rotation())
        field = FieldWithTetromino(Z)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 3), (1, 4), (2, 4), (2, 5)})
        # self.assertTrue(field._is_tetromino_floating())
        self.assertFalse(field.is_valid_placement())
        for row, column in {(2, 3), (3, 4), (3, 5)}:
            supported_field = deepcopy(field)
            supported_field.set_cell(row, column, Cell.I)
            # self.assertFalse(supported_field._is_tetromino_floating())
            supported_field.set_cell(row, column, Cell.EMPTY)
            # self.assertTrue(supported_field._is_tetromino_floating())
            self.assertFalse(supported_field.is_valid_placement())
        for row, column in {(3, 3), (4, 4), (4, 5)}:
            supported_field = deepcopy(field)
            supported_field.set_cell(row, column, Cell.I)
            # self.assertTrue(supported_field._is_tetromino_floating())
            self.assertFalse(supported_field.is_valid_placement())
            supported_field = supported_field.execute_control(Control.SOFT_DROP)
            # self.assertFalse(supported_field._is_tetromino_floating())
            self.assertTrue(supported_field.is_valid_placement())
            supported_field.set_cell(row, column, Cell.EMPTY)
            # self.assertTrue(supported_field._is_tetromino_floating())
            self.assertFalse(supported_field.is_valid_placement())


class FieldWithTetrominoMoveLeftTest(unittest.TestCase):
    def test_I_move_left(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()  # Spawn position
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        new_field = field.execute_control(Control.MOVE_LEFT)  # Move left through execute_control
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})  # Check old coords have not changed
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, {(2, 2), (2, 3), (2, 4), (2, 5)})  # Check new coords have changed

        new_new_field = new_field.execute_control(Control.MOVE_LEFT)  # Move left through execute_move_left
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})  # Check old coords have not changed
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, {(2, 2), (2, 3), (2, 4), (2, 5)})  # Check old coords have not changed
        new_new_coords = new_new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_new_coords, {(2, 1), (2, 2), (2, 3), (2, 4)})  # Check new coords have changed

        touch_the_wall_field = new_new_field.execute_control(Control.MOVE_LEFT)
        touch_the_wall_coords = touch_the_wall_field.get_tetromino_nonempty_coords()
        self.assertEqual(touch_the_wall_coords, {(2, 0), (2, 1), (2, 2), (2, 3)})
        hit_the_wall_field = touch_the_wall_field.execute_control(
            Control.MOVE_LEFT)  # Hit the wall, should not move from cur. pos.
        hit_the_wall_coords = hit_the_wall_field.get_tetromino_nonempty_coords()
        self.assertEqual(hit_the_wall_coords, {(2, 0), (2, 1), (2, 2), (2, 3)})

        self.assertIsInstance(hit_the_wall_field, FieldWithTetromino)


class FieldWithTetrominoMoveRightTest(unittest.TestCase):
    def test_I_move_right(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()  # Spawn position
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        new_field = field.execute_control(Control.MOVE_RIGHT)  # Move right through execute_control
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})  # Check old coords have not changed
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, {(2, 4), (2, 5), (2, 6), (2, 7)})  # Check new coords have changed

        new_new_field = new_field.execute_control(Control.MOVE_RIGHT)  # Move right through execute_move_right
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})  # Check old coords have not changed
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, {(2, 4), (2, 5), (2, 6), (2, 7)})  # Check old coords have not changed
        new_new_coords = new_new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_new_coords, {(2, 5), (2, 6), (2, 7), (2, 8)})  # Check new coords have changed

        touch_the_wall_field = new_new_field.execute_control(Control.MOVE_RIGHT)
        touch_the_wall_coords = touch_the_wall_field.get_tetromino_nonempty_coords()
        self.assertEqual(touch_the_wall_coords, {(2, 6), (2, 7), (2, 8), (2, 9)})
        hit_the_wall_field = touch_the_wall_field.execute_control(
            Control.MOVE_RIGHT)  # Hit the wall, should not move from cur. pos.
        hit_the_wall_coords = hit_the_wall_field.get_tetromino_nonempty_coords()
        self.assertEqual(hit_the_wall_coords, {(2, 6), (2, 7), (2, 8), (2, 9)})

        self.assertIsInstance(hit_the_wall_field, FieldWithTetromino)


class FieldWithTetrominoSoftDropTest(unittest.TestCase):
    def test_I_soft_drop(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()  # Spawn position
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        for row in range(3, 23):
            field = field.execute_control(Control.SOFT_DROP)
            coords = field.get_tetromino_nonempty_coords()
            self.assertEqual(coords, {(row, 3), (row, 4), (row, 5), (row, 6)})

        field = field.execute_control(Control.SOFT_DROP)  # Hit the bottom
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(22, 3), (22, 4), (22, 5), (22, 6)})

        self.assertIsInstance(field, FieldWithTetromino)


class FieldWithTetrominoHardDropTest(unittest.TestCase):
    def test_I_hard_drop_to_bottom(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        field = FieldWithTetromino(I)
        coords = field.get_tetromino_nonempty_coords()  # Spawn position
        self.assertEqual(coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        new_field = field.execute_control(Control.HARD_DROP)  # Hard drop through execute_hard_drop
        self.assertIsInstance(new_field, Field)
        self.assertNotIsInstance(new_field, FieldWithTetromino)
        for row in range(new_field.height - 2):
            self.assertTrue(new_field.is_row_empty(row))
        self.assertEqual(new_field.get_row(new_field.height - 2),
                         [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.I, Cell.I,
                          Cell.I, Cell.I, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY])
        self.assertTrue(new_field.is_row_empty(new_field.height - 1))

    def test_O_hard_drop_to_bottom(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        field = FieldWithTetromino(O)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

        new_field = field.execute_control(Control.HARD_DROP)  # Hard drop through execute_control
        for row in range(new_field.height - 3):
            self.assertTrue(new_field.is_row_empty(row))
        for row in range(new_field.height - 3, new_field.height - 1):
            self.assertEqual(new_field.get_row(row),
                             [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.O,
                              Cell.O, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY])
        self.assertTrue(new_field.is_row_empty(new_field.height - 1))

    def test_O_hard_drop_with_obstruction(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        field = FieldWithTetromino(O)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

        greys = {(10, 4), (13, 5), (15, 5), (18, 4), (20, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        new_field = field._execute_hard_drop()
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, {(8, 4), (8, 5), (9, 4), (9, 5)})

    def test_O_hard_drop_in_place(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        field = FieldWithTetromino(O)
        coords = field.get_tetromino_nonempty_coords()
        self.assertEqual(coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

        field.set_cell(3, 5, Cell.GREY)
        new_field = field._execute_hard_drop()
        new_coords = new_field.get_tetromino_nonempty_coords()
        self.assertEqual(new_coords, coords)


class FieldWithTetrominoRotateCWTest(unittest.TestCase):
    def test_I_rotate_CW(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        I_0_field = FieldWithTetromino(I)
        I_0_coords = I_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_0_coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        I_90_field = I_0_field.execute_control(Control.ROTATE_CW)
        I_90_coords = I_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_90_coords, {(1, 5), (2, 5), (3, 5), (4, 5)})

        I_180_field = I_90_field.execute_control(Control.ROTATE_CW)
        I_180_coords = I_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_180_coords, {(3, 3), (3, 4), (3, 5), (3, 6)})

        I_270_field = I_180_field.execute_control(Control.ROTATE_CW)
        I_270_coords = I_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_270_coords, {(1, 4), (2, 4), (3, 4), (4, 4)})

        I_360_field = I_270_field.execute_control(Control.ROTATE_CW)
        I_360_coords = I_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_360_coords, I_0_coords)

    def test_O_rotate_CW(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        O_0_field = FieldWithTetromino(O)
        O_0_coords = O_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_0_coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

        O_90_field = O_0_field.execute_control(Control.ROTATE_CW)
        O_90_coords = O_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_90_coords, O_0_coords)

        O_180_field = O_90_field.execute_control(Control.ROTATE_CW)
        O_180_coords = O_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_180_coords, O_0_coords)

        O_270_field = O_180_field.execute_control(Control.ROTATE_CW)
        O_270_coords = O_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_270_coords, O_0_coords)

        O_360_field = O_270_field.execute_control(Control.ROTATE_CW)
        O_360_coords = O_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_360_coords, O_0_coords)

    def test_T_rotate_CW(self):
        T = Tetromino.get(Cell.T, SRS.get_spawn_rotation())
        T_0_field = FieldWithTetromino(T)
        T_0_coords = T_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_0_coords, {(1, 4), (2, 3), (2, 4), (2, 5)})

        T_90_field = T_0_field.execute_control(Control.ROTATE_CW)
        T_90_coords = T_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_90_coords, {(1, 4), (2, 4), (2, 5), (3, 4)})

        T_180_field = T_90_field.execute_control(Control.ROTATE_CW)
        T_180_coords = T_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_180_coords, {(2, 3), (2, 4), (2, 5), (3, 4)})

        T_270_field = T_180_field.execute_control(Control.ROTATE_CW)
        T_270_coords = T_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_270_coords, {(1, 4), (2, 3), (2, 4), (3, 4)})

        T_360_field = T_270_field.execute_control(Control.ROTATE_CW)
        T_360_coords = T_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_360_coords, T_0_coords)


class FieldWithTetrominoRotateCCWTest(unittest.TestCase):
    def test_I_rotate_CCW(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        I_360_field = FieldWithTetromino(I)
        I_360_coords = I_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_360_coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        I_270_field = I_360_field.execute_control(Control.ROTATE_CCW)
        I_270_coords = I_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_270_coords, {(1, 4), (2, 4), (3, 4), (4, 4)})

        I_180_field = I_270_field.execute_control(Control.ROTATE_CCW)
        I_180_coords = I_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_180_coords, {(3, 3), (3, 4), (3, 5), (3, 6)})

        I_90_field = I_180_field.execute_control(Control.ROTATE_CCW)
        I_90_coords = I_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_90_coords, {(1, 5), (2, 5), (3, 5), (4, 5)})

        I_0_field = I_90_field.execute_control(Control.ROTATE_CCW)
        I_0_coords = I_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_0_coords, I_360_coords)

    def test_O_rotate_CCW(self):
        O = Tetromino.get(Cell.O, SRS.get_spawn_rotation())
        O_360_field = FieldWithTetromino(O)
        O_360_coords = O_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_360_coords, {(1, 4), (1, 5), (2, 4), (2, 5)})

        O_270_field = O_360_field.execute_control(Control.ROTATE_CCW)
        O_270_coords = O_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_270_coords, O_360_coords)

        O_180_field = O_270_field.execute_control(Control.ROTATE_CCW)
        O_180_coords = O_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_180_coords, O_360_coords)

        O_90_field = O_180_field.execute_control(Control.ROTATE_CCW)
        O_90_coords = O_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_90_coords, O_360_coords)

        O_0_field = O_90_field.execute_control(Control.ROTATE_CCW)
        O_0_coords = O_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(O_0_coords, O_360_coords)

    def test_T_rotate_CCW(self):
        T = Tetromino.get(Cell.T, SRS.get_spawn_rotation())
        T_360_field = FieldWithTetromino(T)
        T_360_coords = T_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_360_coords, {(1, 4), (2, 3), (2, 4), (2, 5)})

        T_270_field = T_360_field.execute_control(Control.ROTATE_CCW)
        T_270_coords = T_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_270_coords, {(1, 4), (2, 3), (2, 4), (3, 4)})

        T_180_field = T_270_field.execute_control(Control.ROTATE_CCW)
        T_180_coords = T_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_180_coords, {(2, 3), (2, 4), (2, 5), (3, 4)})

        T_90_field = T_180_field.execute_control(Control.ROTATE_CCW)
        T_90_coords = T_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_90_coords, {(1, 4), (2, 4), (2, 5), (3, 4)})

        T_0_field = T_90_field.execute_control(Control.ROTATE_CCW)
        T_0_coords = T_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(T_0_coords, T_360_coords)


class FieldWithTetrominoRotate180Test(unittest.TestCase):
    """SRS does not support 180 degree rotations so there is no change in offset and Tetromino Rotation state"""

    def test_I_rotate_180(self):
        I = Tetromino.get(Cell.I, SRS.get_spawn_rotation())
        I_0_field = FieldWithTetromino(I)
        I_0_coords = I_0_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_0_coords, {(2, 3), (2, 4), (2, 5), (2, 6)})

        I_180_field = I_0_field.execute_control(Control.ROTATE_180)
        I_180_coords = I_180_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_180_coords, I_0_coords)

        I_360_field = I_180_field.execute_control(Control.ROTATE_180)
        I_360_coords = I_360_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_360_coords, I_0_coords)

        I_90_field = I_0_field.execute_control(Control.ROTATE_CW)
        I_90_coords = I_90_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_90_coords, {(1, 5), (2, 5), (3, 5), (4, 5)})

        I_270_field = I_90_field.execute_control(Control.ROTATE_180)
        I_270_coords = I_270_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_270_coords, I_90_coords)

        I_450_field = I_270_field.execute_control(Control.ROTATE_180)
        I_450_coords = I_450_field.get_tetromino_nonempty_coords()
        self.assertEqual(I_450_coords, I_90_coords)


class FieldWithTetrominoUsefulKicksTest(unittest.TestCase):
    # Supplied by https://harddrop.com/wiki/SRS

    ###########
    # I tests #
    ###########

    def test_I_NORTH_rotate_cw_4th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        cyans = {(2, 3), (2, 4), (2, 5), (2, 6)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (3, 1), (3, 2), (3, 4), (4, 1), (4, 2), (4, 4), (4, 5), (4, 6),
                 (5, 1), (5, 2), (5, 4), (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(2, 3), (3, 3), (4, 3), (5, 3)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    def test_I_EAST_rotate_cw_5th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        field = field.execute_control(Control.ROTATE_CW)
        cyans = {(1, 5), (2, 5), (3, 5), (4, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(1, 2), (2, 2), (3, 2), (3, 3), (3, 8), (3, 9), (4, 2), (4, 3), (4, 4), (4, 9)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(4, 5), (4, 6), (4, 7), (4, 8)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    def test_I_EAST_rotate_ccw_5th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        field = field.execute_control(Control.ROTATE_CCW)
        field = field.execute_control(Control.ROTATE_CCW)
        field = field.execute_control(Control.ROTATE_CCW)
        cyans = {(1, 5), (2, 5), (3, 5), (4, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(1, 8), (2, 1), (2, 2), (2, 3), (2, 8), (3, 1), (3, 2), (3, 8), (4, 1), (4, 6), (4, 7), (4, 8)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CCW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(4, 2), (4, 3), (4, 4), (4, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    def test_I_SOUTH_rotate_ccw_4th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        field = field.execute_control(Control.ROTATE_CCW)
        field = field.execute_control(Control.ROTATE_CCW)
        cyans = {(3, 3), (3, 4), (3, 5), (3, 6)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(2, 6), (2, 7), (2, 8), (3, 7), (3, 8), (4, 3), (4, 5), (4, 7), (4, 8), (5, 3), (5, 4), (5, 5), (5, 7),
                 (5, 8), (6, 3), (6, 4), (6, 5), (6, 7), (6, 8)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CCW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(3, 6), (4, 6), (5, 6), (6, 6)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    def test_I_WEST_rotate_cw_4th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        cyans = {(1, 4), (2, 4), (3, 4), (4, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(2, 1), (2, 6), (2, 7), (2, 8), (3, 1), (3, 7), (3, 8), (4, 1), (4, 2), (4, 3), (4, 8)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(4, 4), (4, 5), (4, 6), (4, 7)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    def test_I_WEST_rotate_ccw_4th_test(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        field = FieldWithTetromino(I)
        field = field.execute_control(Control.ROTATE_CCW)
        cyans = {(1, 4), (2, 4), (3, 4), (4, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), cyans)

        greys = {(3, 0), (3, 1), (3, 6), (3, 7), (4, 0), (4, 5), (4, 6), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CCW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_cyans = {(4, 1), (4, 2), (4, 3), (4, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_cyans)

    ###########
    # J tests #
    ###########

    def test_J_NORTH_rotate_cw_2nd_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        blues = {(1, 3), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(0, 2), (0, 3), (1, 2), (2, 2), (3, 2), (3, 4), (3, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(1, 3), (1, 4), (2, 3), (3, 3)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_NORTH_rotate_cw_4th_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        blues = {(1, 3), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(0, 4), (0, 5), (0, 6), (1, 5), (1, 6), (2, 6), (3, 2), (3, 3), (3, 6), (4, 2), (4, 3), (4, 5), (4, 6),
                 (5, 2), (5, 3), (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(3, 4), (3, 5), (4, 4), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_EAST_rotate_cw_2nd_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CW)
        blues = {(1, 4), (1, 5), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(1, 6), (1, 7), (2, 7), (3, 5), (3, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(2, 4), (2, 5), (2, 6), (3, 6)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_EAST_rotate_cw_3rd_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CW)
        blues = {(1, 4), (1, 5), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(2, 5), (2, 6), (2, 7), (3, 7), (4, 4), (4, 5), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(3, 4), (3, 5), (3, 6), (4, 6)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_SOUTH_rotate_cw_5th_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        blues = {(2, 3), (2, 4), (2, 5), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(1, 2), (1, 4), (1, 5), (1, 6), (2, 2), (2, 6), (3, 2), (3, 3), (3, 4), (3, 6), (4, 2), (4, 3), (4, 4),
                 (4, 6), (5, 2), (5, 3), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(3, 5), (4, 5), (5, 4), (5, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_WEST_rotate_cw_2nd_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        blues = {(1, 4), (2, 4), (3, 3), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (3, 1), (3, 2)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(1, 2), (2, 2), (2, 3), (2, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    def test_J_WEST_rotate_cw_3rd_test(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        field = FieldWithTetromino(J)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        blues = {(1, 4), (2, 4), (3, 3), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), blues)

        greys = {(1, 1), (1, 2), (1, 3), (2, 1), (2, 3), (3, 1)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_blues = {(2, 2), (3, 2), (3, 3), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_blues)

    ###########
    # L tests #
    ###########

    def test_L_NORTH_rotate_cw_2nd_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        oranges = {(1, 5), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(0, 2), (0, 3), (1, 2), (2, 2), (3, 2), (3, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(1, 3), (2, 3), (3, 3), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    def test_L_NORTH_rotate_cw_5th_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        oranges = {(1, 5), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(1, 2), (1, 3), (2, 2), (3, 2), (3, 4), (3, 5), (3, 6), (4, 2), (4, 4), (4, 5), (4, 6), (5, 2), (5, 5),
                 (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(3, 3), (4, 3), (5, 3), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    def test_L_EAST_rotate_cw_2nd_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        field = field.execute_control(Control.ROTATE_CW)
        oranges = {(1, 4), (2, 4), (3, 4), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(1, 6), (1, 7), (2, 7), (3, 3), (3, 6), (3, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(2, 4), (2, 5), (2, 6), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    def test_L_EAST_rotate_cw_3rd_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        field = field.execute_control(Control.ROTATE_CW)
        oranges = {(1, 4), (2, 4), (3, 4), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(2, 6), (2, 7), (3, 3), (3, 7), (4, 3), (4, 5), (4, 6), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(3, 4), (3, 5), (3, 6), (4, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    def test_L_SOUTH_rotate_cw_5th_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        oranges = {(2, 3), (2, 4), (2, 5), (3, 3)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 2), (4, 3), (4, 4), (4, 6), (5, 2), (5, 3), (5, 4), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(3, 4), (3, 5), (4, 5), (5, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    def test_L_WEST_rotate_cw_3rd_test(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        field = FieldWithTetromino(L)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        oranges = {(1, 3), (1, 4), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), oranges)

        greys = {(2, 1), (2, 2), (2, 3), (2, 5), (3, 1), (3, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_oranges = {(2, 4), (3, 2), (3, 3), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_oranges)

    ###########
    # S tests #
    ###########

    def test_S_NORTH_rotate_cw_4th_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        greens = {(1, 4), (1, 5), (2, 3), (2, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(0, 2), (0, 3), (1, 2), (2, 2), (3, 2), (3, 4), (3, 5), (3, 6), (4, 2), (4, 5), (4, 6), (5, 2), (5, 3),
                 (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(3, 3), (4, 3), (4, 4), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    def test_S_NORTH_rotate_cw_5th_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        greens = {(1, 4), (1, 5), (2, 3), (2, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(1, 2), (1, 3), (2, 2), (3, 2), (3, 3), (3, 5), (3, 6), (4, 2), (4, 3), (4, 6), (5, 2), (5, 3), (5, 4),
                 (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(3, 4), (4, 4), (4, 5), (5, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    def test_S_EAST_rotate_cw_2nd_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        field = field.execute_control(Control.ROTATE_CW)
        greens = {(1, 4), (2, 4), (2, 5), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(1, 6), (1, 7), (2, 7), (3, 3), (3, 6), (3, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(2, 5), (2, 6), (3, 4), (3, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    def test_S_EAST_rotate_cw_3rd_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        field = field.execute_control(Control.ROTATE_CW)
        greens = {(1, 4), (2, 4), (2, 5), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(3, 3), (3, 4), (3, 7), (4, 3), (4, 6), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(3, 5), (3, 6), (4, 4), (4, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    def test_S_SOUTH_rotate_cw_4th_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        greens = {(2, 4), (2, 5), (3, 3), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(1, 5), (1, 6), (2, 2), (2, 3), (2, 6), (3, 2), (3, 5), (3, 6), (4, 2), (4, 5), (4, 6), (5, 2), (5, 3),
                 (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(3, 3), (4, 3), (4, 4), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    def test_S_WEST_rotate_cw_2nd_test(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        field = FieldWithTetromino(S)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        greens = {(1, 3), (2, 3), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), greens)

        greys = {(1, 1), (1, 2), (1, 5), (2, 1), (2, 5), (3, 1), (3, 2), (3, 3), (3, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_greens = {(1, 3), (1, 4), (2, 2), (2, 3)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_greens)

    ###########
    # T tests #
    ###########

    def test_T_NORTH_rotate_cw_2nd_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        purples = {(1, 4), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(0, 2), (0, 3), (1, 2), (2, 2), (3, 2), (3, 4), (3, 5), (3, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(1, 3), (2, 3), (2, 4), (3, 3)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_NORTH_rotate_cw_5th_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        purples = {(1, 4), (2, 3), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(1, 2), (1, 3), (2, 2), (3, 2), (3, 4), (3, 5), (3, 6), (4, 2), (4, 5), (4, 6), (5, 2), (5, 4), (5, 5),
                 (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(3, 3), (4, 3), (4, 4), (5, 3)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_EAST_rotate_cw_1st_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(1, 4), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(1, 2), (1, 3), (2, 2), (2, 6), (3, 2), (3, 3), (3, 5), (3, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(2, 3), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_EAST_rotate_cw_3rd_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(1, 4), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(2, 3), (2, 6), (2, 7), (3, 3), (3, 7), (4, 3), (4, 4), (4, 6), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(3, 4), (3, 5), (3, 6), (4, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_SOUTH_rotate_cw_4th_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(2, 3), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(1, 4), (1, 5), (1, 6), (2, 6), (3, 6), (4, 2), (4, 3), (4, 6), (5, 2), (5, 3), (5, 4), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(3, 5), (4, 4), (4, 5), (5, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_SOUTH_rotate_cw_5th_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(2, 3), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(1, 4), (1, 5), (1, 6), (2, 6), (3, 5), (3, 6), (4, 2), (4, 5), (4, 6), (5, 2), (5, 3), (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(3, 4), (4, 3), (4, 4), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_WEST_rotate_cw_2nd_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(1, 4), (2, 3), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(2, 1), (2, 2), (2, 5), (3, 1), (3, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(2, 3), (3, 2), (3, 3), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    def test_T_WEST_rotate_cw_3rd_test(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        field = FieldWithTetromino(T)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        purples = {(1, 4), (2, 3), (2, 4), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), purples)

        greys = {(1, 1), (1, 2), (2, 1), (2, 5), (3, 1), (3, 2), (3, 3), (3, 5)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_purples = {(1, 3), (2, 2), (2, 3), (2, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_purples)

    ###########
    # Z tests #
    ###########

    def test_Z_NORTH_rotate_cw_1st_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        reds = {(1, 3), (1, 4), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(0, 5), (0, 6), (1, 6), (2, 6), (3, 2), (3, 3), (3, 5), (3, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(1, 5), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)

    def test_Z_NORTH_rotate_cw_4th_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        reds = {(1, 3), (1, 4), (2, 4), (2, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(2, 3), (3, 2), (3, 3), (3, 4), (3, 6), (4, 2), (4, 3), (4, 6), (5, 2), (5, 3), (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(3, 5), (4, 4), (4, 5), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)

    def test_Z_EAST_rotate_cw_2nd_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        field = field.execute_control(Control.ROTATE_CW)
        reds = {(1, 5), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(2, 3), (2, 6), (2, 7), (3, 3), (3, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(2, 4), (2, 5), (3, 5), (3, 6)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)

    def test_Z_EAST_rotate_cw_3rd_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        field = field.execute_control(Control.ROTATE_CW)
        reds = {(1, 5), (2, 4), (2, 5), (3, 4)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(2, 3), (3, 3), (3, 6), (3, 7), (4, 2), (4, 3), (4, 7)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(3, 4), (3, 5), (4, 5), (4, 6)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)

    def test_Z_SOUTH_rotate_cw_5th_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        reds = {(2, 3), (2, 4), (3, 4), (3, 5)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(1, 2), (1, 5), (2, 2), (2, 5), (2, 6), (3, 2), (3, 3), (3, 6), (4, 2), (4, 3), (4, 6), (5, 2), (5, 3),
                 (5, 5), (5, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(3, 5), (4, 4), (4, 5), (5, 4)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)

    def test_Z_WEST_rotate_cw_1st_test(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        field = FieldWithTetromino(Z)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        field = field.execute_control(Control.ROTATE_CW)
        reds = {(1, 4), (2, 3), (2, 4), (3, 3)}
        self.assertEqual(field.get_tetromino_nonempty_coords(), reds)

        greys = {(1, 2), (1, 5), (1, 6), (2, 2), (2, 6), (3, 2), (3, 4), (3, 5), (3, 6)}
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        self.assertTrue(field.are_current_offsets_valid())

        new_field = field.execute_control(Control.ROTATE_CW)
        self.assertTrue(new_field.are_current_offsets_valid())
        new_reds = {(1, 3), (1, 4), (2, 4), (2, 5)}
        self.assertEqual(new_field.get_tetromino_nonempty_coords(), new_reds)


class FieldWithTetrominoComprehensiveControlTest(unittest.TestCase):
    def test_opening_TSD(self):
        field = Field()

        field = field.spawn_tetromino(Cell.I)
        field = field.execute_controls([Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.L)
        field = field.execute_controls([Control.ROTATE_CW, Control.ROTATE_CW, Control.MOVE_LEFT, Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.Z)
        field = field.execute_controls([Control.ROTATE_CW, Control.MOVE_RIGHT, Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.J)
        field = field.execute_controls([Control.ROTATE_CCW, Control.MOVE_RIGHT, Control.MOVE_RIGHT, Control.MOVE_RIGHT,
                                        Control.MOVE_RIGHT, Control.MOVE_RIGHT, Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.O)
        field = field.execute_controls([Control.MOVE_LEFT, Control.MOVE_LEFT, Control.MOVE_LEFT, Control.MOVE_LEFT,
                                        Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.S)
        field = field.execute_controls([Control.HARD_DROP])

        field = field.spawn_tetromino(Cell.T)
        field = field.execute_controls([Control.MOVE_RIGHT, Control.MOVE_RIGHT, Control.MOVE_RIGHT, Control.MOVE_RIGHT,
                                        Control.ROTATE_CCW, Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP,
                                        Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP,
                                        Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP,
                                        Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP,
                                        Control.SOFT_DROP, Control.SOFT_DROP, Control.SOFT_DROP, Control.ROTATE_CCW,
                                        Control.HARD_DROP])

        for row in range(field.height - 4):
            self.assertTrue(field.is_row_empty(row))
        self.assertEqual(field.get_row(field.height - 3), [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.S,
                                                           Cell.S, Cell.Z, Cell.EMPTY, Cell.EMPTY, Cell.EMPTY])
        self.assertEqual(field.get_row(field.height - 2), [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY, Cell.S, Cell.S, Cell.Z,
                                                           Cell.Z, Cell.EMPTY, Cell.EMPTY, Cell.J])
        self.assertTrue(field.is_row_empty(field.height - 1))


class FieldWithTetrominoGetPossibleFieldsTest(unittest.TestCase):
    def test_I_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.I)
        self.assertEqual(17, len(fwt.get_possible_fields()))

    def test_J_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.J)
        self.assertEqual(34, len(fwt.get_possible_fields()))

    def test_L_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.L)
        self.assertEqual(34, len(fwt.get_possible_fields()))

    def test_O_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.O)
        self.assertEqual(9, len(fwt.get_possible_fields()))

    def test_S_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.S)
        self.assertEqual(17, len(fwt.get_possible_fields()))

    def test_T_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.T)
        self.assertEqual(34, len(fwt.get_possible_fields()))

    def test_Z_init_field(self):
        field = Field()
        fwt = field.spawn_tetromino(Cell.Z)
        self.assertEqual(17, len(fwt.get_possible_fields()))

    def test_do_not_prune_too_much_by_soft_drop(self):
        field = Field()
        greys = [(19, 3), (19, 6), (20, 3), (20, 6), (21, 3), (21, 6), (22, 3), (22, 6)]
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        fwt = field.spawn_tetromino(Cell.O)
        self.assertEqual(9, len(fwt.get_possible_fields()))


class FieldWithTetrominoGetPossibleFieldsBelowHeightTest(unittest.TestCase):
    def test_screwed_field(self):
        field = Field()
        greys = [(19, 3), (19, 4), (20, 2), (20, 3), (20, 4), (20, 5), (20, 6), (20, 7), (21, 4), (21, 5), (22, 3),
                 (22, 4)]
        for row, column in greys:
            field.set_cell(row, column, Cell.GREY)
        fwt = field.spawn_tetromino(Cell.I)
        self.assertEqual(9, len(fwt.get_possible_fields_below_height(4)))
        fwt = field.spawn_tetromino(Cell.O)
        self.assertEqual(5, len(fwt.get_possible_fields_below_height(4)))


if __name__ == '__main__':
    unittest.main()
