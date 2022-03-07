from itertools import groupby

from cell import Cell
from field import Field
from utils import base64_encode, poll, base64_sanitize

###################
# Fumen utilities #
###################

BLANK_FIELD = Field()


class Fumen:
    """
    Original by Mihys: https://fumen.zui.jp/
    Documentation by knewjade: https://docs.google.com/presentation/d/1P5xt0vPGuxSb9hbRW6hvQFYKFoIccfNTJkWTdjtyigc
    Tool for recording a list of Fields (frames) in an a compact and transmissible manner.

    The functions encode and decode guarantee that any list of Fields in that order
    can be stored as a Fumen code (string) and retrieved without loss in information.
    May NOT generate the same Fumen codes as the official implementation for lists of multiple Fields.

    Lightweight implementation to be easily used with Fields (simple frames).
    This does NOT support piece placement and assumes default flag settings always
    (piece, rotation, location, raise, mirror, comment are OFF; guideline, lock are ON).
    """
    PREFIX = "v115@"
    FLAGS = "AgH"
    SUFFIX = "AAA"

    @staticmethod
    def decode(fumen_code):
        """Return a list of Fields obtained from decoding FUMEN_CODE."""
        original_fumen_code = fumen_code

        def decode_poll_value(poll_value):
            return poll_value // 240, poll_value % 240

        def compute_curr_cell(prev_cell, diff):
            return Cell(prev_cell.value + diff - 8)

        def compute_curr_field(prev_field, difference_from_prev_field):
            curr_field = Field()
            curr_cell_index = 0
            for diff, count in difference_from_prev_field:
                for _ in range(count + 1):
                    row, column = prev_field.index_to_coords(curr_cell_index)
                    prev_cell = prev_field.get_cell(row, column)
                    curr_cell = compute_curr_cell(prev_cell, diff)
                    curr_field.set_cell(row, column, curr_cell)
                    curr_cell_index += 1
            return curr_field

        # Check and discard prefix. Must do this before sanitizing
        assert fumen_code[:len(Fumen.PREFIX)] == Fumen.PREFIX
        fumen_code = fumen_code[len(Fumen.PREFIX):]

        # Ignore '?', '#' and other illegal characters
        fumen_code = base64_sanitize(fumen_code)

        list_of_fields = []
        prev_field = BLANK_FIELD
        flags_checked = False  # have I encountered "AgH"

        while fumen_code:
            new_fields = []
            cells_processed = 0
            difference_from_prev_field = []
            while cells_processed < 240:
                # Retrieve (diff, count) pairs from poll(2)
                poll_value, fumen_code = poll(2, fumen_code)
                diff, count = decode_poll_value(poll_value)
                difference_from_prev_field.append((diff, count))
                cells_processed += count + 1
            assert cells_processed == 240, original_fumen_code  # Illegal fumen code check

            # Find new field with (diff, count) pairs
            curr_field = compute_curr_field(prev_field, difference_from_prev_field)
            new_fields.append(curr_field)

            # poll(2) == vh signifies a repeating Field. Check the following digit to see how many times to repeat
            if prev_field == curr_field:
                value, fumen_code = poll(1, fumen_code)
                for _ in range(value):
                    new_fields.append(Field(curr_field.field))  # Make a copy of the current field

            # AgH / AAA check for each new field
            for _ in range(len(new_fields)):
                if not flags_checked:
                    flags_checked = True
                    assert fumen_code[:3] == Fumen.FLAGS
                else:
                    assert fumen_code[:3] == Fumen.SUFFIX
                fumen_code = fumen_code[3:]  # Discard flags

            prev_field = curr_field
            list_of_fields.extend(new_fields)

        return list_of_fields

    @staticmethod
    def encode(list_of_fields):
        """
        Return the Fumen code obtained by encoding LIST_OF_FIELDS.
        This does not implement the shorthand for multiple repeated Fields and
        instead uses "vhA" + ["AgH" or "AAA"] for each consecutive pair.
        The original Fumen is able to decode these codes but will encode them with the shorthand.
        """

        def encode_poll_value(diff, count):
            return diff * 240 + count

        def cell_diff(curr_cell, prev_cell):
            return curr_cell.value - prev_cell.value + 8

        def compute_difference_fields(curr_field, prev_field):
            diffs = []
            for index in range(240):
                row, column = prev_field.index_to_coords(index)
                prev_cell = prev_field.get_cell(row, column)
                curr_cell = curr_field.get_cell(row, column)
                diff = cell_diff(curr_cell, prev_cell)
                diffs.append(diff)
            return [(diff, len(list(group)) - 1) for diff, group in groupby(diffs)]

        fumen_code = [Fumen.PREFIX]
        prev_field = BLANK_FIELD
        flags_inserted = False  # have I used "AgH"

        while list_of_fields:
            curr_field = list_of_fields[0]

            # Compute (diff, count) pairs
            difference_from_prev_field = compute_difference_fields(curr_field, prev_field)

            for diff, count in difference_from_prev_field:
                poll_value = encode_poll_value(diff, count)
                base64_poll_value = base64_encode(poll_value, 2)
                fumen_code.append("".join(reversed(base64_poll_value)))

            if prev_field == curr_field:
                fumen_code.append("A")

            if not flags_inserted:
                flags_inserted = True
                fumen_code.append(Fumen.FLAGS)
            else:
                fumen_code.append(Fumen.SUFFIX)

            prev_field = curr_field
            list_of_fields = list_of_fields[1:]

        return "".join(fumen_code)
