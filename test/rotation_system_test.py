import unittest

from cell import Cell
from control import Control
from rotation import Rotation
from rotation_system import subtract_lists_of_offsets, SuperRotationSystem
from tetromino import Tetromino

SRS = SuperRotationSystem


class RotationSystemSubtractListsOfOffsetsTest(unittest.TestCase):
    def test_subtract_lists(self):
        list_1 = SRS.JLSTZ_offset_data[Rotation.NORTH]
        list_2 = SRS.JLSTZ_offset_data[Rotation.EAST]
        self.assertEqual(subtract_lists_of_offsets(list_1, list_2), [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)])


# The following is provided by https://harddrop.com/wiki/SRS
JLSTZ_kicks = {
    (Rotation.NORTH, Rotation.EAST): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (Rotation.EAST, Rotation.NORTH): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (Rotation.EAST, Rotation.SOUTH): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (Rotation.SOUTH, Rotation.EAST): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (Rotation.SOUTH, Rotation.WEST): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (Rotation.WEST, Rotation.SOUTH): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (Rotation.WEST, Rotation.NORTH): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (Rotation.NORTH, Rotation.WEST): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]
}


class RotationSystemKicksTest(unittest.TestCase):
    def test_JLSTZ_kicks(self):
        for rotation in Rotation:
            J = Tetromino.get(Cell.J, rotation)
            cw_kicks = SRS.get_kick_tests(J, Control.ROTATE_CW)
            self.assertEqual(cw_kicks, JLSTZ_kicks[(rotation, rotation.rotate_cw())])
            ccw_kicks = SRS.get_kick_tests(J, Control.ROTATE_CCW)
            self.assertEqual(ccw_kicks, JLSTZ_kicks[(rotation, rotation.rotate_ccw())])


if __name__ == '__main__':
    unittest.main()
