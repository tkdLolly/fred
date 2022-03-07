from cell import Cell
from cli import CLI, HorizontalDivider, MoveLayer, PCModeLayer, Prompt, VerticalDivider
from field import Field
from fumen import Fumen
from game import PCMode


def main():
    cli = CLI()
    game = PCMode()
    pc_mode_layer = PCModeLayer(game)
    move_layer = MoveLayer(pc_mode_layer)
    prompt = Prompt()
    cli.layers = [pc_mode_layer, HorizontalDivider(), move_layer, prompt, VerticalDivider()]

    def handle_input(raw_input):
        tokens = raw_input.split(" ")
        cmd = tokens[0]
        if cmd not in CMDS.keys():
            prompt.add_to_history("Error: bad command")
            return 0
        return CMDS[cmd](tokens[1:])

    def execute_hint(tokens):
        pass    # TODO

    def execute_move(tokens):
        # Hold
        if len(tokens) == 1:
            token = tokens[0]
            if token == "hold":
                pc_mode_layer.game.advance_to_field(pc_mode_layer.game.field)
                prompt.add_to_history("Move: hold")
                return 0

        # Place piece
        elif len(tokens) == 4:
            curr_piece = pc_mode_layer.game.queue[0]
            field = Field(pc_mode_layer.game.field.field)

            # Check valid coords
            for token in tokens:
                index = int(token)
                if not 0 <= index < 240:
                    prompt.add_to_history("Move: bad indices")
                    return 0
                row, column = field.index_to_coords(index)
                field.set_cell(row, column, curr_piece)

            # Update fields
            field.line_clear()
            pc_mode_layer.display_field = field
            field = field.convert_cells_to_grey()

            # Check reachable field
            if field not in pc_mode_layer.game.next_fields:
                prompt.add_to_history("Move: unreachable field")
                return 0

            pc_mode_layer.game.advance_to_field(field)
            prompt.add_to_history("Move: {0}".format(" ".join(tokens)))
            return 0

        prompt.add_to_history("Bad move")
        return 0

    def execute_quit(tokens):
        return -1

    def execute_reset(tokens):
        pass    # TODO

    CMDS = {
        "hint": execute_hint,
        "move": execute_move,
        "quit": execute_quit,
        "reset": execute_reset
    }

    while True:
        move_layer.update_moves()
        cli.update()
        cli.clear_and_show()
        raw_input = input("pc> ")
        prompt.add_to_history("pc> {0}".format(raw_input))
        if handle_input(raw_input):
            return


if __name__ == '__main__':
    main()
