import unittest

from cell import Cell
from field import Field
from fumen import Fumen


class FumenDecodeTest(unittest.TestCase):
    def test_vhAAgH(self):
        test_string = "v115@vhAAgH"
        list_of_fields = Fumen.decode(test_string)
        self.assertEqual(list_of_fields, [Field()])

    def test_empty_fields(self):
        test_two_empty_fields = "v115@vhBAgHAAA"
        list_of_fields = Fumen.decode(test_two_empty_fields)
        self.assertEqual(list_of_fields, [Field(), Field()])


class FumenEncodeTest(unittest.TestCase):
    def test_init_field(self):
        test_list_of_fields = [Field()]
        self.assertEqual(Fumen.encode(test_list_of_fields), "v115@vhAAgH")


class FumenEncodeDecodeTest(unittest.TestCase):
    def test_diagonal_field_recovery(self):
        field = Field()
        for row in range(field.height):
            for column in range(field.width):
                cell = Cell((row + column) % 9)
                field.set_cell(row, column, cell)
        self.assertEqual(Fumen.decode(Fumen.encode([field])), [field])

    def test_regular_color_field(self):
        field = Field()
        for index in range(240):
            row, column = field.index_to_coords(index)
            cell = Cell(index % 9)
            field.set_cell(row, column, cell)
        self.assertEqual(Fumen.decode(Fumen.encode([field])), [field])

    def test_list_of_fields(self):
        field_1 = Field()
        for row in range(field_1.height):
            for column in range(field_1.width):
                cell = Cell((row + column) % 9)
                field_1.set_cell(row, column, cell)

        field_2 = Field()
        for index in range(240):
            row, column = field_2.index_to_coords(index)
            cell = Cell(index % 9)
            field_2.set_cell(row, column, cell)

        self.assertEqual(Fumen.decode(Fumen.encode([field_1, field_2])), [field_1, field_2])
        self.assertEqual(Fumen.decode(Fumen.encode([field_2, field_1])), [field_2, field_1])
        self.assertEqual(Fumen.decode(Fumen.encode([field_1, field_1, field_2, field_2])), [field_1, field_1, field_2, field_2])
        self.assertEqual(Fumen.decode(Fumen.encode([field_2, field_2, field_2, field_1])), [field_2, field_2, field_2, field_1])


if __name__ == '__main__':
    unittest.main()
