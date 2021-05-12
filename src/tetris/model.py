from array import array
from enum import Enum


def _row(*args):
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
    T = "T", [_row(1, 1, 1), _row(0, 1, 0)]
    I = "I", [_row(1, 1, 1, 1)]
    L = "L", [_row(1, 1), _row(1, 0), _row(1, 0)]
    J = "J", [_row(1, 1), _row(0, 1), _row(0, 1)]

    def __new__(cls, value, layout):
        """Populates properties on this tetris piece."""
        p = str.__new__(cls, value)
        p._value_ = value
        p.layout = layout
        p.height = len(layout)
        p.width = len(layout[0])
        return p


class Grid:
    def __init__(self, width: int = 10):
        self.width = width
        self.grid = []

    def _add_row(self):
        """Adds an empty row to the grid."""
        self.grid.append(_row(*(0 for ii in range(self.width))))

    def _ensure_height(self, height: int):
        """Ensures the grid has at least input height.

        Adds rows if necessary."""
        for _ in range(height - len(self.grid)):
            self._add_row()

    def _update_grid(self, piece: Piece, row: int, col: int):
        """Updates the grid to include the input piece."""
        self._ensure_height(row + piece.height)
        for r, grid_row in enumerate(self.grid[row: row + piece.height]):
            for col_offset, p in enumerate(piece.layout[r]):
                grid_row[col + col_offset] += p

    def add(self, piece: Piece, col: int):
        self._update_grid(piece, 0, col)

    @property
    def height(self) -> int:
        return len(self.grid)
