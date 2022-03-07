import unittest

from cell import Cell


class CellTest(unittest.TestCase):
    def test_is_empty(self):
        for cell in Cell:
            if cell is Cell.EMPTY:
                self.assertTrue(cell.is_empty())
            else:
                self.assertFalse(cell.is_empty())


if __name__ == '__main__':
    unittest.main()
