from array import array
from enum import Enum


def _row(*args):
    """Shorthand method to create grid rows."""
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
        self.grid = []  # rows are ordered bottom to top

    def _add_row(self):
        """Adds an empty row to the grid."""
        self.grid.append(_row(*(0 for ii in range(self.width))))

    def _ensure_height(self, height: int):
        """Ensures the grid has at least input height, adding rows if necessary."""
        for _ in range(height - len(self.grid)):
            self._add_row()

    def _update_grid(self, piece: Piece, row: int, col: int):
        """Updates the grid to include the input piece."""
        self._ensure_height(row + piece.height)
        for r, grid_row in enumerate(self.grid[row: row + piece.height]):
            for col_offset, p in enumerate(piece.layout[r]):
                grid_row[col + col_offset] += p

    def _delete_full_lines(self):
        """Deletes full lines from the grid."""
        self.grid = [row for row in self.grid if not all(row)]

    def _get_landing_row(self, piece: Piece, col: int):
        """Determines the landing row of a piece being added.

        When a new piece is added to the grid, determine on which
        row it will stop falling.
        """
        # find a grid row that fits the bottom row of the piece
        for gr_idx in range(len(self.grid)):
            for pr_idx, piece_row in enumerate(piece.layout):
                if pr_idx + gr_idx >= len(self.grid):
                    # no more row above on the grid, so the piece
                    # will drop here
                    return gr_idx
                grid_row_slice = self.grid[gr_idx + pr_idx][col: col + piece.width]
                if any(p and g for p, g in zip(piece_row, grid_row_slice)):
                    # we found a collision
                    break
                # if we're on the last row of the piece and there
                # were no collisions, the piece will drop here
                if pr_idx + 1 == piece.height:
                    return gr_idx

        # if we made it here, we'll just need to add at the top of the grid
        return len(self.grid)

    def add(self, piece: Piece, col: int):
        landing_row = self._get_landing_row(piece, col)
        self._update_grid(piece, landing_row, col)
        self._delete_full_lines()

    @property
    def height(self) -> int:
        return len(self.grid)
