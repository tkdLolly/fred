import csv
from csv import DictReader, DictWriter
import os
import shutil
from tempfile import NamedTemporaryFile

from fumen import Fumen


########
# Move #
########

def get_move_path(field, piece):
    """Path to text file containing possible next Fields from FIELD. Each line is a Fumen code."""
    fumen_code = Fumen.encode([field])[5:]
    fumen_code = fumen_code.replace("/", "-")  # "/" is FS separator
    if not os.path.exists("../move/{0}".format(fumen_code)):
        os.mkdir("../move/{0}".format(fumen_code))
    return "../move/{0}/{1}.txt".format(fumen_code, piece.name)


def pc_mode_fetch_possible_next_fields(field, piece):
    """Return a set of possible Fields from FIELD using PIECE."""
    move_path = get_move_path(field, piece)
    if os.path.exists(move_path):
        with open(move_path, 'r') as move_file:
            fields = set()
            for fumen_code in move_file:
                fumen_code.replace("-", "/")  # "/" is FS separator
                fields.add(Fumen.decode(fumen_code.strip())[0])
            return fields

    fwt = field.spawn_tetromino(piece)
    fields = fwt.get_possible_fields_below_height(4, convert_to_grey=True)

    with open(move_path, 'x') as move_file:
        for field in fields:
            move_file.write(Fumen.encode([field]) + '\n')

    return fields


##########
# Values #
##########

def pc_mode_load_q_values():
    q_value_dict = dict()
    with open("../values/values.csv", 'r', newline='') as values_file:
        reader = csv.reader(values_file, delimiter=',')
        for row in reader:
            if not row:
                continue
            state_and_next_field, value = row
            q_value_dict[state_and_next_field] = value
    return q_value_dict


def pc_mode_save_q_values(nonzero_q_values_dict):
    with open("../values/values.csv", 'w', newline='') as values_file:
        writer = csv.writer(values_file, delimiter=',')
        writer.writerows(nonzero_q_values_dict.items())
