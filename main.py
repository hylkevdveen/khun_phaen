"""
Title: main.py
Author: H.F. van der Veen
Date: 23-05-2021
Description: Read and solve a Khun Phaen puzzle.
"""


import sys
from state import State
from khun_phaen_solver import khun_phaen_solver


def main(argv):
    """Read and solve a Khun Phaen puzzle."""
    if len(argv) != 1:
        start = State(argv[1])
    else:
        start = State()

    print("Khun Phaen start state:")
    print(start)

    khun_phaen_solver(start)


if __name__ == "__main__":
    main(sys.argv)
