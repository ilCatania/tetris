from itertools import combinations

import pytest
from tetris.model import Piece, Grid


@pytest.mark.parametrize("piece", Piece)
def test_piece_well_defined(piece):
    """Tests that pieces occupy exactly 4 grid squares."""
    assert sum(p for row in piece.layout for p in row) == 4


def test_piece_layouts_unique():
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
