"""Command line integration module."""
import fileinput
import os.path
import sys
from typing import List

from tetris.model import Piece, Grid


def parse_piece_adds(line: str) -> List:
    """Parse pieces and columns from an input line."""
    return [(Piece[s[0]], int(s[1:])) for s in line.split()]


def parse_from_piped_input():
    """Parse from piped input."""
    with fileinput.input() as f:
        return [parse_piece_adds(l) for l in f]


def parse_from_file(filename):
    """Parse from a file provided as first argument."""
    with open(filename, "r") as f:
        return [parse_piece_adds(l) for l in f]


def parse_from_args(args):
    """Parse from script arguments."""
    return map(parse_piece_adds, args)


def get_grid_height(piece_additions):
    """Get grid height after adding some pieces."""
    grid = Grid()
    for piece, col in piece_additions:
        grid.add(piece, col)
    return grid.height


def run():
    """Parse pieces from provided arguments and print out grid heights."""
    if len(sys.argv) == 2 and os.path.isfile(sys.argv[1]):
        inputs = parse_from_file(sys.argv[1])
    elif len(sys.argv) > 1:
        inputs = parse_from_args(sys.argv[1:])
    elif not sys.stdin.isatty():
        inputs = parse_from_piped_input()
    else:
        raise ValueError("No input provided!")

    for piece_additions in inputs:
        print(get_grid_height(piece_additions))


if __name__ == "__main__":
    run()
