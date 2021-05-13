"""Tetris model and logic module."""
from array import array
from enum import Enum


def _row(*args):
    """Create grid rows."""
    return array("B", args)


class Piece(str, Enum):
    """Tetris piece.

    Pieces are identified by their letter (e.g. Q for
    the square) and represented by matrices in the form
    [ [bottom row], .., [ top row ] ]
    """

    Q = "Q", [_row(1, 1), _row(1, 1)]
    Z = "Z", [_row(0, 1, 1), _row(1, 1, 0)]
    S = "S", [_row(1, 1, 0), _row(0, 1, 1)]
    T = "T", [_row(0, 1, 0), _row(1, 1, 1)]
    I = "I", [_row(1, 1, 1, 1)]
    L = "L", [_row(1, 1), _row(1, 0), _row(1, 0)]
    J = "J", [_row(1, 1), _row(0, 1), _row(0, 1)]

    def __new__(cls, value, layout):
        """Populate properties on this tetris piece."""
        p = str.__new__(cls, value)
        p._value_ = value
        p.layout = layout
        p.height = len(layout)
        p.width = len(layout[0])
        return p


class Grid:
    """Tetris grid representation.

    Rows are stored bottom first in the grid.
    """

    def __init__(self, width: int = 10):
        """Initialize a new empty grid with the required width."""
        self.width = width
        self.grid = []

    def _add_row(self):
        """Add an empty row to the grid."""
        self.grid.append(_row(*(0 for ii in range(self.width))))

    def _ensure_height(self, height: int):
        """Ensure the grid has at least input height, adding rows if necessary."""
        for _ in range(height - len(self.grid)):
            self._add_row()

    def _update_grid(self, piece: Piece, row: int, col: int):
        """Update the grid to include the input piece."""
        self._ensure_height(row + piece.height)
        for r, grid_row in enumerate(self.grid[row: row + piece.height]):
            for col_offset, p in enumerate(piece.layout[r]):
                grid_row[col + col_offset] += p

    def _delete_full_lines(self):
        """Delete full lines from the grid."""
        self.grid = [row for row in self.grid if not all(row)]

    def _get_landing_row(self, piece: Piece, col: int):
        """Determine the landing row of a piece being added.

        When a new piece is added to the grid, determine on which
        row it will stop falling.
        """
        # look at grid rows starting from the top, and stop if the
        # piece collides with anything on the row
        for grid_row_idx in reversed(range(len(self.grid))):
            for piece_row_idx, piece_row in enumerate(piece.layout):
                if piece_row_idx + grid_row_idx >= len(self.grid):
                    # no more rows above on the grid, so
                    # nothing else to check
                    break
                grid_row_slice = self.grid[grid_row_idx + piece_row_idx][col: col + piece.width]
                if any(p and g for p, g in zip(piece_row, grid_row_slice)):
                    # we found a collision, so the piece will stop
                    # on the row above current
                    return grid_row_idx + 1

        # no collisions, the piece drops to the bottom
        return 0

    def add(self, piece: Piece, col: int):
        """Add a piece to the grid."""
        landing_row = self._get_landing_row(piece, col)
        self._update_grid(piece, landing_row, col)
        self._delete_full_lines()

    @property
    def height(self) -> int:
        """Return current grid height."""
        return len(self.grid)
