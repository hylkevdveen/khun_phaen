"""
Title: piece.py
Author: H.F. van der Veen
Date: 23-05-2021
Description: Class Piece stores information for single pieces of the Khun Phaen game.
"""


class Piece:
    """Class for storing information about a single piece of the Khun Phaen game."""

    def __init__(self, x, y, width, height):
        """Initialize a piece of the Khun Phaen game."""
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self.__khun = width == 2 and height == 2
        self._color = self.get_color()

    @property
    def coordinates(self):
        """Return a set of all coordinates that this piece covers."""
        coordinates = set()
        for i in range(self._width):
            for j in range(self._height):
                coordinates.add((self._x + i, self._y + j))
        return coordinates

    def get_color(self):
        """Decide which color the piece should be based on width and height."""
        if self._width == 1:
            if self._height == 1:
                return "YELLOW"
            return "GREEN"
        if self._height == 1:
            return "GREEN"
        return "RED"

    def __str__(self):
        """String method for printing Piece objects."""
        return f"({self._x}, {self._y}), {self._width}x{self._height}"

    def __hash__(self):
        """Hash function."""
        return hash((self._x, self._y, self._width, self._height))

    def __eq__(self, other):
        """Equality method for comparing Piece objects."""
        if self._x != other.x():
            return False
        if self._y != other.y():
            return False
        if self._width != other.width():
            return False
        return self._height == other.height()

    def __lt__(self, other):
        """Less than method for sorting Piece objects."""
        if self.__khun:
            return True
        if other.is_khun():
            return False
        if self._x < other.x():
            return True
        if self._x > other.x():
            return False
        if self._y < other.y():
            return True
        return False

    def move(self, x, y):
        """Generate coordinates for a move in an x or y direction."""
        coordinates = set()
        for i in range(self._width):
            for j in range(self._height):
                # Check bounds
                if 0 <= (new_x := self._x + x + i) <= 4 and 0 <= (new_y := self._y + y + j) <= 5:
                    coordinates.add((new_x, new_y))
                else:
                    return False
        return coordinates

    def x(self):
        return self._x

    def y(self):
        return self._y

    def width(self):
        return self._width

    def height(self):
        return self._height

    def is_khun(self):
        return self.__khun

    def color(self):
        return self._color
