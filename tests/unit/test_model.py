from itertools import combinations

import pytest
from tetris.model import Piece, Grid


@pytest.mark.parametrize("piece", Piece)
def test_piece_well_defined(piece):
    """Tests that pieces occupy exactly 4 grid squares."""
    assert sum(p for row in piece.layout for p in row) == 4


def test_piece_layouts_unique():
    """Tests that pieces have unique layouts."""
    for p1, p2 in combinations(Piece, 2):
        assert p1.layout != p2.layout


@pytest.mark.parametrize("piece", Piece)
def test_add_single(piece):
    """Tests a single piece addition.

    When adding a piece to an empty grid, the resulting
    grid height should be the same as the piece's height.
    """
    grid = Grid()
    grid.add(piece, 0)
    assert grid.height == piece.height


def test_add_two_longs_stacking():
    """Tests adding two long pieces, one on top of the other."""
    grid = Grid()
    grid.add(Piece.I, 0)
    grid.add(Piece.I, 0)
    assert grid.height == 2


def test_add_two_zeds_stacking():
    """Tests adding two Z pieces, one on top of the other."""
    grid = Grid()
    grid.add(Piece.Z, 0)
    grid.add(Piece.Z, 0)
    assert grid.height == 4


def test_add_two_longs_adjacent():
    """Tests adding two long pieces, side by side."""
    grid = Grid()
    grid.add(Piece.I, 0)
    grid.add(Piece.I, 4)
    assert grid.height == 1


def test_add_interlocking():
    """Tests adding a T and a Z and S on its sides."""
    grid = Grid()
    grid.add(Piece.T, 2)
    grid.add(Piece.S, 0)
    grid.add(Piece.Z, 4)
    assert grid.height == 2


def test_add_and_complete_a_line():
    """Tests adding pieces that form a full line at the bottom."""
    grid = Grid()
    grid.add(Piece.T, 2)
    grid.add(Piece.T, 5)
    grid.add(Piece.S, 0)
    grid.add(Piece.Z, 7)
    assert grid.height == 1


def test_add_two_full_lines():
    """Tests adding pieces that form exactly two full lines."""
    grid = Grid()
    grid.add(Piece.I, 0)
    grid.add(Piece.I, 0)
    grid.add(Piece.Q, 4)
    grid.add(Piece.I, 6)
    grid.add(Piece.I, 6)
    assert grid.height == 0
