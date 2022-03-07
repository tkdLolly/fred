import os
from itertools import product

from fumen import Fumen
from game import PCMode


class CLI:
    length_x = 120
    length_y = 35

    def __init__(self):
        self.layers = []
        self.display = [[" " for _ in range(self.length_x)] for _ in range(self.length_y)]

    def update(self):
        for layer in self.layers:
            for x, y in product(range(layer.offset_x, layer.offset_x + layer.length_x),
                                range(layer.offset_y, layer.offset_y + layer.length_y)):
                self.display[y][x] = layer.get_char(x, y)

    def clear_and_show(self):
        os.system("cls")
        for row in self.display:
            print("".join(row))


class Layer:
    length_x = 0
    length_y = 0
    offset_x = 0
    offset_y = 0

    def get_char(self, x, y):
        pass


class PCModeLayer(Layer):
    length_x = 52
    length_y = 14
    offset_x = 0
    offset_y = 0

    game = None
    display_field = None

    def __init__(self, game):
        assert isinstance(game, PCMode)
        self.game = game
        self.display_field = game.field

    def get_char(self, x, y):
        # Title
        if x in range(0, 5) and y == 0:
            return "Field"[x]

        # Field grid
        if (x, y) == (8, 1):
            return "┌"
        elif (x, y) == (48, 1):
            return "┐"
        elif (x, y) == (8, 9):
            return "└"
        elif (x, y) == (48, 9):
            return "┘"
        elif 8 < x < 48 and x % 4 and y in range(1, 10, 2):
            return "─"
        elif x in range(8, 49, 4) and y in range(2, 9, 2):
            return "│"
        elif x in range(12, 45, 4) and y == 1:
            return "┬"
        elif x == 8 and y in range(3, 8, 2):
            return "├"
        elif x == 48 and y in range(3, 8, 2):
            return "┤"
        elif x in range(12, 45, 4) and y == 9:
            return "┴"
        elif x in range(8, 49, 4) and y in range(3, 8, 2):
            return "┼"

        # Row labels
        elif x == 3 and y in range(2, 9, 2):
            return "12"[(y + 2) // 6]
        elif x == 4 and y in range(2, 9, 2):
            return "9012"[y // 2 - 1]
        elif x == 5 and y in range(2, 9, 2):
            return "0"

        # Column labels
        elif x in range(10, 47, 4) and y == 10:
            return "0123456789"[x // 4 - 2]

        # Field cells
        elif x in range(10, 47, 4) and y in range(2, 9, 2):
            row = y // 2 + 18
            column = x // 4 - 2
            cell = self.display_field.get_cell(row, column)
            return str(cell)

        # Queue
        elif x in range(13, 18) and y == 12:
            return "Next:"[x - 13]
        elif x in range(19, 30, 2) and y == 12:
            return str(self.game.queue[x // 2 - 9])

        # Hold
        elif x in range(2, 7) and y == 12:
            return "Hold:"[x - 2]
        elif (x, y) == (8, 12):
            return str(self.game.hold_piece)

        # PC Number
        elif x in range(44, 50) and y == 12:
            pc_num = self.game.pc_number
            return ["1st PC", "2nd PC", "3rd PC", "4th PC", "5th PC", "6th PC", "7th PC"][pc_num - 1][x - 44]

        else:
            return " "


class HorizontalDivider(Layer):
    length_x = 52
    length_y = 1
    offset_x = 0
    offset_y = 14

    def get_char(self, x, y):
        return "═"


class VerticalDivider(Layer):
    length_x = 1
    length_y = 35
    offset_x = 52
    offset_y = 0

    def get_char(self, x, y):
        return "║"


class Prompt(Layer):
    length_x = 52
    length_y = 20
    offset_x = 0
    offset_y = 15

    def __init__(self):
        self.history = ["" for _ in range(self.length_y)]

    def add_to_history(self, line):
        self.history.append(line)
        self.history.pop(0)

    def get_char(self, x, y):
        y -= self.offset_y
        if y < len(self.history):
            line = self.history[y]
            if x < len(line):
                return line[x]

        return " "


class MoveLayer(Layer):
    length_x = 67
    length_y = 35
    offset_x = 53
    offset_y = 0

    def __init__(self, pc_mode_layer):
        self.pc_mode_layer = pc_mode_layer
        self.moves = []

    def get_char(self, x, y):
        x -= self.offset_x

        # Title
        if x in range(0, 5) and y == 0:
            return "Moves"[x]

        # Moves
        elif y in range(1, len(self.moves) + 1):
            move = self.moves[y - 1]
            if 0 <= x - 2 < len(move):
                return move[x - 2]

        return " "

    def update_moves(self):
        self.moves = list(Fumen.encode([field]) for field in self.pc_mode_layer.game.get_possible_next_fields())
