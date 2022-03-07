import unittest

from fumen import Fumen
from game import Game, PCMode
from random import Random


class GameTest(unittest.TestCase):
    def test_full_game(self):
        game = Game(seed=42)
        random = Random(42)
        while not game.has_game_ended:
            fields = list(game.next_fields)
            random_field = random.choice(fields)
            game.advance_to_field(random_field)
        self.assertTrue(game.has_game_ended)
        print(game)
        print(Fumen.encode(game.history))


class PCModeTest(unittest.TestCase):
    def test_full_game(self):
        game = PCMode(seed=42)
        random = Random(42)
        while not game.has_game_ended:
            fields = list(game.next_fields)
            random_field = random.choice(fields)
            game.advance_to_field(random_field)
        self.assertTrue(game.has_game_ended)
        print(game)
        print(Fumen.encode(game.history))

    def test_two_full_games(self):
        self.test_full_game()
        self.test_full_game()

    def test_first_pco(self):
        fields = [
            "v115@9gA8IeA8IeA8IeA8SeAgH",
            "v115@9gA8IeA8HeB8GeC8HeA8JeAgH",
            "v115@9gA8IeA8HeC8FeF8EeA8JeAgH",
            "v115@9gA8IeA8HeC8DeH8CeC8JeAgH",
            "v115@9gA8IeA8AeB8EeE8BeH8CeC8JeAgH",
            "v115@9gA8GeC8AeB8CeG8BeH8CeC8JeAgH",
            "v115@9gD8DeF8CeG8BeH8CeC8JeAgH",
            "v115@HhD8DeG8BeH8BeC8JeAgH",
            "v115@RhE8BeH8BeC8JeAgH",
            "v115@vhAAgH"
        ]
        game = PCMode()
        self.assertEqual(game.num_pcs, 0)
        self.assertEqual(game.pc_number, 1)
        self.assertEqual(game.num_pieces_placed_since_last_pc, 0)
        self.assertFalse(game.has_game_ended)
        for fumen_code, i in zip(fields, range(10)):
            self.assertEqual(game.num_pieces_placed_since_last_pc, i)
            field = Fumen.decode(fumen_code)[0]
            game.advance_to_field(field)
            self.assertFalse(game.has_game_ended)
        self.assertEqual(game.num_pcs, 1)
        self.assertEqual(game.pc_number, 2)
        self.assertEqual(game.num_pieces_placed_since_last_pc, 0)

if __name__ == '__main__':
    unittest.main()
