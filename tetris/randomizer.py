import random
from tetromino import tetromino_cells


class Randomizer:
    """Tetromino randomizer with optional SEED."""
    def __init__(self, seed=None):
        random.seed(seed)
        self.random = random.random()

    def generate_next_tetromino(self):
        """Generate and return the Cell representing the next Tetromino."""
        pass

    def get_possible_next_pieces_and_probabilities(self):
        """Return a set of (Cell, float) tuples for each piece that could appear next with the probability of each."""
        pass


class SevenBagRandomizer(Randomizer):
    """7-bag randomizer. (Random Generator: https://tetris.wiki/Random_Generator)"""

    seven_bag = list(tetromino_cells)   # [I, J, L, O, S, T, Z] Cells in any order

    def __init__(self, seed=None):
        super().__init__(seed)
        self.queue = []
        self._generate_next_bag()

    def generate_next_tetromino(self):
        # If my queue is empty, generate a seven-bag first and extend my queue ith it.
        if not self.queue:
            self._generate_next_bag()

        # Pop the frontmost Cell from my queue and return it.
        return self.queue.pop(0)

    def get_possible_next_pieces_and_probabilities(self):
        if not self.queue:
            self._generate_next_bag()
        prob = 1 / len(self.queue)
        return set((cell, prob) for cell in self.queue)

    def _generate_next_bag(self):
        """Generate the next bag of Cells and extend my queue with it."""
        random.shuffle(self.seven_bag)
        self.queue.extend(self.seven_bag)
