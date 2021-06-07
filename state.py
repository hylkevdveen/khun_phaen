"""
Title: state.py
Author: H.F. van der Veen
Date: 23-05-2021
Description: Class State saves all states of the Khun Phaen game, inherits from Field.
"""


import time
from field import Field


class State(Field):
    """Class to save the possible states in. Inherits from Field."""
    def __init__(self, file="khun_phaen.txt", parent=None, depth=1, goal=None, pieces=None):
        if pieces:
            super().__init__(None, goal, pieces)
        else:
            super().__init__(file)
        self._parent = parent
        self._depth = depth

    def parent(self):
        """Return the previous state."""
        return self._parent

    def depth(self):
        """Return node depth."""
        return self._depth

    def is_solved(self):
        """Return True if the current state is the solution (if Khun Phaen is at the goal coordinates)."""
        return (khun := self.sorted_pieces()[0]).x() == self.goal[0] and khun.y() == self.goal[1]

    def print_solution(self, max_depth):
        """Recursively print the solution to the puzzle. Only call once the goal has been reached."""
        if self._parent is not None:
            self._parent.print_solution(max_depth)
            # Overwrite previous step
            print('\033[26A', end='\r')
        # Print each step with a sleep
        print(f"Step {self._depth:>3}/{max_depth}", end="\n\n")
        print(self)
        time.sleep(0.5)
