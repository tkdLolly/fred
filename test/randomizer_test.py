import unittest

from randomizer import SevenBagRandomizer
from tetromino import tetromino_cells


class SevenBagTest(unittest.TestCase):
    def test_distribution(self):
        trials = 100
        randomizer = SevenBagRandomizer()
        for _ in range(trials):
            seven_pieces = set()
            for _ in range(7):
                seven_pieces.add(randomizer.generate_next_tetromino())
            self.assertEqual(seven_pieces, tetromino_cells)

    def test_get_possible_next_pieces_and_probabilities(self):
        randomizer = SevenBagRandomizer()
        piece_set = set(tetromino_cells)
        for i in reversed(range(1, 8)):
            prob = 1 / i
            self.assertEqual(randomizer.get_possible_next_pieces_and_probabilities(),
                             set((piece, prob) for piece in piece_set))
            piece = randomizer.generate_next_tetromino()
            piece_set -= {piece}
        self.assertEqual(randomizer.get_possible_next_pieces_and_probabilities(),
                         set((piece, 1 / 7) for piece in tetromino_cells))


if __name__ == '__main__':
    unittest.main()
