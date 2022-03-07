import unittest

from cell import Cell
from control import Control
from rotation import Rotation
from tetromino import Tetromino


class TetrominoInitTest(unittest.TestCase):
    def test_I_init(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        self.assertEqual(I.cell, Cell.I)
        self.assertEqual(I.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_J_init(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        self.assertEqual(J.cell, Cell.J)
        self.assertEqual(J.matrix,
                         [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_L_init(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        self.assertEqual(L.cell, Cell.L)
        self.assertEqual(L.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_O_init(self):
        O = Tetromino.get(Cell.O, Rotation.NORTH)
        self.assertEqual(O.cell, Cell.O)
        self.assertEqual(O.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_S_init(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        self.assertEqual(S.cell, Cell.S)
        self.assertEqual(S.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_T_init(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        self.assertEqual(T.cell, Cell.T)
        self.assertEqual(T.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_Z_init(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        self.assertEqual(Z.cell, Cell.Z)
        self.assertEqual(Z.matrix,
                         [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])


class TetrominoRotateCWTest(unittest.TestCase):
    def test_I_rotate_cw(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_90 = I.rotate_cw()
        self.assertEqual(I_90, Tetromino.get(Cell.I, Rotation.EAST))
        self.assertEqual(I_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0]])
        I_180 = I_90.rotate_cw()
        self.assertEqual(I_180, Tetromino.get(Cell.I, Rotation.SOUTH))
        self.assertEqual(I_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [1, 1, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        I_270 = I_180.rotate(Control.ROTATE_CW)
        self.assertEqual(I_270, Tetromino.get(Cell.I, Rotation.WEST))
        self.assertEqual(I_270.matrix,
                         [[0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        I_0 = I_270.rotate_cw()
        self.assertEqual(I_0, I)

    def test_J_rotate_cw(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        J_90 = J.rotate_cw()
        self.assertEqual(J_90, Tetromino.get(Cell.J, Rotation.EAST))
        self.assertEqual(J_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        J_180 = J_90.rotate_cw()
        self.assertEqual(J_180, Tetromino.get(Cell.J, Rotation.SOUTH))
        self.assertEqual(J_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]])
        J_270 = J_180.rotate_cw()
        self.assertEqual(J_270, Tetromino.get(Cell.J, Rotation.WEST))
        self.assertEqual(J_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]])
        J_0 = J_270.rotate_cw()
        self.assertEqual(J_0, J)

    def test_L_rotate_cw(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        L_90 = L.rotate_cw()
        self.assertEqual(L_90, Tetromino.get(Cell.L, Rotation.EAST))
        self.assertEqual(L_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]])
        L_180 = L_90.rotate_cw()
        self.assertEqual(L_180, Tetromino.get(Cell.L, Rotation.SOUTH))
        self.assertEqual(L_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]])
        L_270 = L_180.rotate_cw()
        self.assertEqual(L_270, Tetromino.get(Cell.L, Rotation.WEST))
        self.assertEqual(L_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        L_0 = L_270.rotate_cw()
        self.assertEqual(L_0, L)

    def test_O_rotate_cw(self):
        O = Tetromino.get(Cell.O, Rotation.NORTH)
        O_90 = O.rotate_cw()
        self.assertEqual(O_90, Tetromino.get(Cell.O, Rotation.EAST))
        self.assertEqual(O_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]])
        O_180 = O_90.rotate_cw()
        self.assertEqual(O_180, Tetromino.get(Cell.O, Rotation.SOUTH))
        self.assertEqual(O_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]])
        O_270 = O_180.rotate_cw()
        self.assertEqual(O_270, Tetromino.get(Cell.O, Rotation.WEST))
        self.assertEqual(O_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
        O_0 = O_270.rotate_cw()
        self.assertEqual(O_0, O)

    def test_S_rotate_cw(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        S_90 = S.rotate_cw()
        self.assertEqual(S_90, Tetromino.get(Cell.S, Rotation.EAST))
        self.assertEqual(S_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 0]])
        S_180 = S_90.rotate_cw()
        self.assertEqual(S_180, Tetromino.get(Cell.S, Rotation.SOUTH))
        self.assertEqual(S_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 0, 0, 0]])
        S_270 = S_180.rotate_cw()
        self.assertEqual(S_270, Tetromino.get(Cell.S, Rotation.WEST))
        self.assertEqual(S_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        S_0 = S_270.rotate_cw()
        self.assertEqual(S_0, S)

    def test_T_rotate_cw(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        T_90 = T.rotate_cw()
        self.assertEqual(T_90, Tetromino.get(Cell.T, Rotation.EAST))
        self.assertEqual(T_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        T_180 = T_90.rotate_cw()
        self.assertEqual(T_180, Tetromino.get(Cell.T, Rotation.SOUTH))
        self.assertEqual(T_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        T_270 = T_180.rotate_cw()
        self.assertEqual(T_270, Tetromino.get(Cell.T, Rotation.WEST))
        self.assertEqual(T_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        T_0 = T_270.rotate_cw()
        self.assertEqual(T_0, T)

    def test_Z_rotate_cw(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        Z_90 = Z.rotate_cw()
        self.assertEqual(Z_90, Tetromino.get(Cell.Z, Rotation.EAST))
        self.assertEqual(Z_90.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 1, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0]])
        Z_180 = Z_90.rotate_cw()
        self.assertEqual(Z_180, Tetromino.get(Cell.Z, Rotation.SOUTH))
        self.assertEqual(Z_180.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0, 0, 0, 0, 0]])
        Z_270 = Z_180.rotate_cw()
        self.assertEqual(Z_270, Tetromino.get(Cell.Z, Rotation.WEST))
        self.assertEqual(Z_270.matrix,
                         [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]])
        Z_0 = Z_270.rotate_cw()
        self.assertEqual(Z_0, Z)

    def test_maware(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_maware = I
        for _ in range(9 * 4):
            I_maware = I_maware.rotate_cw()
        self.assertEqual(I, I_maware)


class TetrominoRotateCCWTest(unittest.TestCase):
    def test_I_rotate_ccw(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_270 = I.rotate_ccw()
        self.assertEqual(I_270, Tetromino.get(Cell.I, Rotation.WEST))
        I_180 = I_270.rotate_ccw()
        self.assertEqual(I_180, Tetromino.get(Cell.I, Rotation.SOUTH))
        I_90 = I_180.rotate(Control.ROTATE_CCW)
        self.assertEqual(I_90, Tetromino.get(Cell.I, Rotation.EAST))
        I_0 = I_90.rotate_ccw()
        self.assertEqual(I_0, I)

    def test_J_rotate_ccw(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        J_270 = J.rotate_ccw()
        self.assertEqual(J_270, Tetromino.get(Cell.J, Rotation.WEST))
        J_180 = J_270.rotate_ccw()
        self.assertEqual(J_180, Tetromino.get(Cell.J, Rotation.SOUTH))
        J_90 = J_180.rotate_ccw()
        self.assertEqual(J_90, Tetromino.get(Cell.J, Rotation.EAST))
        J_0 = J_90.rotate_ccw()
        self.assertEqual(J_0, J)

    def test_L_rotate_ccw(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        L_270 = L.rotate_ccw()
        self.assertEqual(L_270, Tetromino.get(Cell.L, Rotation.WEST))
        L_180 = L_270.rotate_ccw()
        self.assertEqual(L_180, Tetromino.get(Cell.L, Rotation.SOUTH))
        L_90 = L_180.rotate_ccw()
        self.assertEqual(L_90, Tetromino.get(Cell.L, Rotation.EAST))
        L_0 = L_90.rotate_ccw()
        self.assertEqual(L_0, L)

    def test_O_rotate_ccw(self):
        O = Tetromino.get(Cell.O, Rotation.NORTH)
        O_270 = O.rotate_ccw()
        self.assertEqual(O_270, Tetromino.get(Cell.O, Rotation.WEST))
        O_180 = O_270.rotate_ccw()
        self.assertEqual(O_180, Tetromino.get(Cell.O, Rotation.SOUTH))
        O_90 = O_180.rotate_ccw()
        self.assertEqual(O_90, Tetromino.get(Cell.O, Rotation.EAST))
        O_0 = O_90.rotate_ccw()
        self.assertEqual(O_0, O)

    def test_S_rotate_ccw(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        S_270 = S.rotate_ccw()
        self.assertEqual(S_270, Tetromino.get(Cell.S, Rotation.WEST))
        S_180 = S_270.rotate_ccw()
        self.assertEqual(S_180, Tetromino.get(Cell.S, Rotation.SOUTH))
        S_90 = S_180.rotate_ccw()
        self.assertEqual(S_90, Tetromino.get(Cell.S, Rotation.EAST))
        S_0 = S_90.rotate_ccw()
        self.assertEqual(S_0, S)

    def test_T_rotate_ccw(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        T_270 = T.rotate_ccw()
        self.assertEqual(T_270, Tetromino.get(Cell.T, Rotation.WEST))
        T_180 = T_270.rotate_ccw()
        self.assertEqual(T_180, Tetromino.get(Cell.T, Rotation.SOUTH))
        T_90 = T_180.rotate_ccw()
        self.assertEqual(T_90, Tetromino.get(Cell.T, Rotation.EAST))
        T_0 = T_90.rotate_ccw()
        self.assertEqual(T_0, T)

    def test_Z_rotate_cw(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        Z_270 = Z.rotate_ccw()
        self.assertEqual(Z_270, Tetromino.get(Cell.Z, Rotation.WEST))
        Z_180 = Z_270.rotate_ccw()
        self.assertEqual(Z_180, Tetromino.get(Cell.Z, Rotation.SOUTH))
        Z_90 = Z_180.rotate_ccw()
        self.assertEqual(Z_90, Tetromino.get(Cell.Z, Rotation.EAST))
        Z_0 = Z_90.rotate_ccw()
        self.assertEqual(Z_0, Z)

    def test_maware(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_maware = I
        for _ in range(9 * 4):
            I_maware = I_maware.rotate_ccw()
        self.assertEqual(I, I_maware)


class TetrominoRotate180Test(unittest.TestCase):
    def test_I_rotate_180(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_180 = I.rotate_180()
        self.assertEqual(I_180, Tetromino.get(Cell.I, Rotation.SOUTH))
        I_0 = I_180.rotate(Control.ROTATE_180)
        self.assertEqual(I_0, I)
        I = Tetromino.get(Cell.I, Rotation.EAST)
        I_270 = I.rotate_180()
        self.assertEqual(I_270, Tetromino.get(Cell.I, Rotation.WEST))
        I_90 = I_270.rotate_180()
        self.assertEqual(I_90, I)

    def test_J_rotate_180(self):
        J = Tetromino.get(Cell.J, Rotation.NORTH)
        J_180 = J.rotate_180()
        self.assertEqual(J_180, Tetromino.get(Cell.J, Rotation.SOUTH))
        J_0 = J_180.rotate_180()
        self.assertEqual(J_0, J)
        J = Tetromino.get(Cell.J, Rotation.EAST)
        J_270 = J.rotate_180()
        self.assertEqual(J_270, Tetromino.get(Cell.J, Rotation.WEST))
        J_90 = J_270.rotate_180()
        self.assertEqual(J_90, J)

    def test_L_rotate_180(self):
        L = Tetromino.get(Cell.L, Rotation.NORTH)
        L_180 = L.rotate_180()
        self.assertEqual(L_180, Tetromino.get(Cell.L, Rotation.SOUTH))
        L_0 = L_180.rotate_180()
        self.assertEqual(L_0, L)
        L = Tetromino.get(Cell.L, Rotation.EAST)
        L_270 = L.rotate_180()
        self.assertEqual(L_270, Tetromino.get(Cell.L, Rotation.WEST))
        L_90 = L_270.rotate_180()
        self.assertEqual(L_90, L)

    def test_O_rotate_180(self):
        O = Tetromino.get(Cell.O, Rotation.NORTH)
        O_180 = O.rotate_180()
        self.assertEqual(O_180, Tetromino.get(Cell.O, Rotation.SOUTH))
        O_0 = O_180.rotate_180()
        self.assertEqual(O_0, O)
        O = Tetromino.get(Cell.O, Rotation.EAST)
        O_270 = O.rotate_180()
        self.assertEqual(O_270, Tetromino.get(Cell.O, Rotation.WEST))
        O_90 = O_270.rotate_180()
        self.assertEqual(O_90, O)

    def test_S_rotate_180(self):
        S = Tetromino.get(Cell.S, Rotation.NORTH)
        S_180 = S.rotate_180()
        self.assertEqual(S_180, Tetromino.get(Cell.S, Rotation.SOUTH))
        S_0 = S_180.rotate_180()
        self.assertEqual(S_0, S)
        S = Tetromino.get(Cell.S, Rotation.EAST)
        S_270 = S.rotate_180()
        self.assertEqual(S_270, Tetromino.get(Cell.S, Rotation.WEST))
        S_90 = S_270.rotate_180()
        self.assertEqual(S_90, S)

    def test_T_rotate_180(self):
        T = Tetromino.get(Cell.T, Rotation.NORTH)
        T_180 = T.rotate_180()
        self.assertEqual(T_180, Tetromino.get(Cell.T, Rotation.SOUTH))
        T_0 = T_180.rotate_180()
        self.assertEqual(T_0, T)
        T = Tetromino.get(Cell.T, Rotation.EAST)
        T_270 = T.rotate_180()
        self.assertEqual(T_270, Tetromino.get(Cell.T, Rotation.WEST))
        T_90 = T_270.rotate_180()
        self.assertEqual(T_90, T)

    def test_Z_rotate_180(self):
        Z = Tetromino.get(Cell.Z, Rotation.NORTH)
        Z_180 = Z.rotate_180()
        self.assertEqual(Z_180, Tetromino.get(Cell.Z, Rotation.SOUTH))
        Z_0 = Z_180.rotate_180()
        self.assertEqual(Z_0, Z)
        Z = Tetromino.get(Cell.Z, Rotation.EAST)
        Z_270 = Z.rotate_180()
        self.assertEqual(Z_270, Tetromino.get(Cell.Z, Rotation.WEST))
        Z_90 = Z_270.rotate_180()
        self.assertEqual(Z_90, Z)

    def test_maware(self):
        I = Tetromino.get(Cell.I, Rotation.NORTH)
        I_maware = I
        for _ in range(9 * 4):
            I_maware = I_maware.rotate_180()
        self.assertEqual(I, I_maware)


if __name__ == '__main__':
    unittest.main()
