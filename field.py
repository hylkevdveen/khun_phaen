"""
Title: field.py
Author: H.F. van der Veen
Date: 23-05-2021
Description: Class Field represents a state of the playing field of the Khun Phaen game.
"""

import re
from copy import deepcopy
from piece import Piece
from field_colors import colors


class Field:
    """Class to represent the playing field of Khun Phaen."""

    # Corners of the playing field
    X_MIN = 0
    Y_MIN = 0
    X_MAX = 4
    Y_MAX = 5

    # A set of all coordinates of the playing field
    _ALL_COORDS = set((i, j) for j in range(5) for i in range(4))

    # Template for a new printed field
    _EMPTY_FIELD = [['█'] + ['▀'] * 33 + ['█', '\n']] + \
                   [['█'] + [' '] * 33 + ['█', '\n'] for _ in range(19)] + \
                   [['█'] + ['▄'] * 33 + ['█', '\n']]

    def __init__(self, file='khun_phaen.txt', goal=None, pieces=None):
        """Initialize the playing field and all its pieces.

        To generate a field based on a pre-existing state, provide a goal and pieces and leave file at None
        """
        self.goal = goal

        if pieces:
            self.pieces = pieces
        else:
            self.pieces = set()
            self.read_setup(file)

    def __str__(self):
        """String method for printing the current field state."""
        ret = ""
        for row in self.draw_field():
            ret += ''.join(row)
        return ret

    def __hash__(self):
        """Hash method for a field."""
        return hash(tuple(hash(piece) for piece in self.sorted_pieces()))

    def covered_coordinates(self):
        """Return a set of all currently covered coordinates on the playing field."""
        ret = set()
        for piece in self.pieces:
            ret |= piece.coordinates
        return ret

    def free_coordinates(self):
        """Return a set of the currently free coordinates."""
        return self._ALL_COORDS - self.covered_coordinates()

    def sorted_pieces(self):
        """Return a sorted list of all pieces on the board. Khan will be the first item."""
        return sorted(self.pieces)

    def sorted_pieces_str(self):
        """Return a string version of the sorted pieces for comparison."""
        ret = ""
        for piece in self.sorted_pieces():
            ret += piece.__str__() + '|'
        return ret

    def read_setup(self, file):
        """Read the starting state of the Khun Phaen game from the given input file."""
        with open(file, 'r') as f:
            # Get the top left corner of the goal from the first line
            m = re.match(r"Goal: (\d), (\d)", f.readline())
            self.goal = (int(m.group(1)), int(m.group(2)))
            # Skip empty line
            f.readline()
            # Iterate over the starting state of the game
            for i in range(2, 21):
                for j, char in enumerate(f.readline()):
                    if char == 'O':
                        # Check height based on X
                        if i % 4 == 0:
                            height = 1
                            y = i - 1
                        else:
                            height = 2
                            y = i - 3
                        # Check width based on X
                        if (j + 3) % 8 == 0:
                            width = 1
                            x = j
                        else:
                            width = 2
                            x = j - 4
                        x = (x - 3) // 8
                        y = (y - 3) // 4
                        self.pieces.add(Piece(x, y, width, height))

    # =========================
    # METHODS FOR DRAWING FIELD
    # =========================

    def draw_field(self):
        """Draw the field based on the current pieces."""
        field = deepcopy(self._EMPTY_FIELD)
        for piece in sorted(self.pieces):
            self.draw_piece(field, piece)
        return field

    def draw_piece(self, field, piece):
        """Draw a single piece in the field."""
        origin = (1 + 4 * piece.y(), 2 + 8 * piece.x())
        width = piece.width()
        height = piece.height()
        color = piece.color()

        self.draw_sides(field, origin, width, height, color)
        self.draw_top_bottom(field, origin, width, height, color)
        self.draw_circle(field, origin, width, height, color)

    @staticmethod
    def draw_sides(field, origin, width, height, color):
        """Draw the sides of a single piece."""
        right = {
            1: 6,
            2: 14
        }[width]

        height = {
            1: 3,
            2: 7
        }[height]

        for i in range(height):
            field[origin[0] + i][origin[1]] = f"{colors[color]}█{colors['END']}"          # Left
            field[origin[0] + i][origin[1] + right] = f"{colors[color]}█{colors['END']}"  # Right

    @staticmethod
    def draw_top_bottom(field, origin, width, height, color):
        """Draw the top and bottom of a single piece."""
        bottom = {
            1: 2,
            2: 6
        }[height]

        width = {
            1: 6,
            2: 14
        }[width]

        for i in range(1, width):
            field[origin[0]][origin[1] + i] = f"{colors[color]}▀{colors['END']}"           # Top
            field[origin[0] + bottom][origin[1] + i] = f"{colors[color]}▄{colors['END']}"  # Bottom

    @staticmethod
    def draw_circle(field, origin, width, height, color):
        """Draw the X in a single piece."""
        x_offset = {
            1: 3,
            2: 7
        }[width]

        y_offset = {
            1: 1,
            2: 3
        }[height]

        field[origin[0] + y_offset][origin[1] + x_offset] = f"{colors[color]}●{colors['END']}"
