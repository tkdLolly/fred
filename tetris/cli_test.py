import unittest

from game import PCMode
from cli import CLI, HorizontalDivider, MoveLayer, PCModeLayer, Prompt, VerticalDivider


def main():
    cli = CLI()
    game = PCMode()
    pc_mode_layer = PCModeLayer(game)
    move_layer = MoveLayer(pc_mode_layer)
    prompt = Prompt()
    cli.layers = [pc_mode_layer, HorizontalDivider(), VerticalDivider(), prompt, move_layer]
    while True:
        move_layer.update_moves()
        cli.update()
        cli.clear_and_show()
        raw_input = input("pc> ")
        prompt.add_to_history("pc> {0}".format(raw_input))


if __name__ == "__main__":
    main()