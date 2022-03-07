from cell import Cell
from control import Control
from database import pc_mode_fetch_possible_next_fields
from field import Field
from fumen import Fumen
from itertools import product
from randomizer import SevenBagRandomizer

# Allowed controls
CONTROLS = set(Control) - {Control.ROTATE_180}
CONTROLS_NO_HOLD = CONTROLS - {Control.HOLD}


class Game:
    """Integrate Field and Randomizer and handle game settings."""

    def __init__(self, randomizer_type=SevenBagRandomizer, seed=None):
        # Fields
        self.field = Field()

        # Randomizer
        self.randomizer = randomizer_type(seed)
        self.num_pieces_placed = 0

        # Queue
        self.queue_visibility = 6  # Include current piece, exclude hold piece
        self.queue = []  # Index 0 for current piece, the rest queue
        self._queue_fill()

        # Hold
        self.is_hold_enabled = True  # Enabled for entire game
        self.has_held_once = False  # Has held once before piece placement
        self.hold_piece = Cell.EMPTY

        # Is game ongoing
        self.has_game_ended = False
        self.next_fields = self.get_possible_next_fields()
        self.check_and_set_has_game_ended()

        self.history = [self.field]

    def __repr__(self):
        return str(self.get_state_representation())

    def get_available_controls(self):
        """Return a set of available controls."""
        if self.has_game_ended:
            return set()
        if self.has_held_once:
            return CONTROLS_NO_HOLD
        return CONTROLS

    def get_possible_next_fields(self):
        """Return a set of possible Fields using the current piece plus the current Field if holding is possible."""
        fwt = self.field.spawn_tetromino(self.queue[0])
        fields = fwt.get_possible_fields(convert_to_grey=True)
        if not self.has_held_once:
            fields.add(self.field)
        return fields

    def advance_to_field(self, field):
        """
        Change my current field to FIELD assuming it is a possible option.
        If FIELD is the same as the current field, hold my current piece. Otherwise,
        update my NUM_PIECES_PLACED, QUEUE, and HAS_HELD_ONCE;
        set my HAS_GAME_ENDED to True if game has ended; and
        add the new Field to my HISTORY.
        """
        # If the same field, then hold the current piece.
        if field == self.field:
            self.has_held_once = True
            if self.hold_piece.is_empty():
                self.hold_piece = self.queue.pop(0)
                self._queue_fill()
            else:
                self.hold_piece, self.queue[0] = self.queue[0], self.hold_piece
        else:
            self.field = field

            self.num_pieces_placed += 1

            self.queue.pop(0)
            self._queue_fill()

            self.has_held_once = False

            fwt = self.field.spawn_tetromino(self.queue[0])
            self.has_game_ended = not fwt.are_current_offsets_valid()

            self.history.append(self.field)

        self.next_fields = self.get_possible_next_fields()
        self.check_and_set_has_game_ended()

    ################
    # AI Utilities #
    ################

    def check_and_set_has_game_ended(self):
        """End the game when no possible next fields exist."""
        self.has_game_ended = len(self.next_fields) == 0

    def get_state_representation(self):
        """A state is a 5-tuple."""
        #return "field={0}, pieces={1}, queue={2}, hold={3}, held={4}".format(self.field, self.num_pieces_placed, tuple(self.queue), self.hold_piece, self.has_held_once)
        return self.field, self.num_pieces_placed, tuple(self.queue), self.hold_piece, self.has_held_once

    def get_possible_next_states(self):
        """Return a dict of Fields to (State, probability) pairs. Next states either placed my current piece or held."""
        states_dict = dict()

        # If the game has ended, there are no next states
        if self.has_game_ended:
            return states_dict

        piece_prob_pairs = self.get_possible_next_pieces_and_probabilities()

        # Either place the current piece
        new_num_pieces_placed = self.num_pieces_placed + 1
        for field, piece_prob_pair in product(self.get_possible_next_fields(), piece_prob_pairs):
            if field not in states_dict:
                states_dict[field] = set()

            piece, prob = piece_prob_pair
            new_queue = tuple(self.queue[1:] + [piece])
            state_prob_pair = ((field, new_num_pieces_placed, new_queue, self.hold_piece, False), prob)
            states_dict[field].add(state_prob_pair)

        # Or use hold if available
        if not self.has_held_once:
            states_dict[self.field] = set()

            new_hold_piece = self.queue[0]
            if self.hold_piece.is_empty():
                for piece, prob in piece_prob_pairs:
                    new_queue = tuple(self.queue[1:] + [piece])
                    states_dict[self.field].add(((self.field, self.num_pieces_placed, new_queue, new_hold_piece, True)
                                                 , prob))
            else:
                new_queue = tuple([self.hold_piece] + self.queue[1:])
                states_dict[self.field].add(((self.field, self.num_pieces_placed, new_queue, new_hold_piece, True), 1))

        return states_dict

    def get_possible_next_pieces_and_probabilities(self):
        """Return a set of (Cell, probability) tuples for each of the next pieces that can appear"""
        return self.randomizer.get_possible_next_pieces_and_probabilities()

    ###########
    # Private #
    ###########

    def _queue_fill(self):
        """Fill my Queue with as many Cells as promised by my queue_visibility."""
        num_pieces = self.queue_visibility - len(self.queue)
        for _ in range(num_pieces):
            next_piece = self.randomizer.generate_next_tetromino()
            self.queue.append(next_piece)


class PCMode(Game):
    def __init__(self, seed=None):
        super().__init__(seed=seed)
        self.num_pcs = 0
        self.pc_number = 1
        self.num_pieces_placed_since_last_pc = 0

    def get_possible_next_fields(self):
        """Return a set of possible Fields using the current piece plus the current Field if holding is possible."""
        return pc_mode_fetch_possible_next_fields(self.field, self.queue[0])

    def set_pc_number(self):
        """Called only when my Field is empty."""
        self.pc_number = (self.num_pieces_placed * 5) % 7 + 1

    def advance_to_field(self, field):
        """
        Change my current field to FIELD assuming it is a possible option.
        Update my NUM_PIECES_PLACED, QUEUE, and HAS_HELD_ONCE. Set my HAS_GAME_ENDED to True if game has ended.
        """
        super(PCMode, self).advance_to_field(field)

        self.num_pieces_placed %= 70    # 70-piece loop

        if field.is_visibly_empty():
            self.num_pcs += 1
            self.set_pc_number()
            self.num_pieces_placed_since_last_pc = 0
        else:
            self.num_pieces_placed_since_last_pc += 1

        if self.num_pieces_placed_since_last_pc == 10:
            self.has_game_ended = True


class GameWithControls(Game):
    def __init__(self):
        super().__init__()
        self.fwt = None

    def spawn_tetromino(self):
        """Spawn Tetromino into my Field and store as my FWT. Does not remove next piece from my queue."""
        next_piece = self.queue[0]
        self.fwt = self.field.spawn_tetromino(next_piece)
        if not self.fwt.are_current_offsets_valid():
            self.has_game_ended = True

    ####################
    # Control handling #
    ####################

    def execute_control(self, control, ignore_lines_cleared=False):
        def execute_hold():
            if self.hold_piece is Cell.EMPTY:
                self.hold_piece = self.queue.pop(0)
                self._queue_fill()
            else:
                self.hold_piece, self.queue[0] = self.queue[0], self.hold_piece
            self.has_held_once = True
            self.spawn_tetromino()

        def execute_hard_drop():
            # Execute HD and pop a piece from queue. The resulting Field is stored as my Field and my FWT is None.
            self.field, lines_cleared = self.fwt.execute_control(Control.HARD_DROP, ignore_lines_cleared)
            self.fwt = None
            self.queue.pop(0)
            self._queue_fill()
            self.has_held_once = False

        if control is Control.HOLD:
            execute_hold()
        elif control is Control.HARD_DROP:
            execute_hard_drop()
        else:
            self.fwt = self.fwt.execute_control(control)

    def execute_controls(self, list_of_controls, ignore_lines_cleared=False):
        for control in list_of_controls:
            self.execute_control(control, ignore_lines_cleared)
