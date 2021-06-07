"""
Title: khun_phaen_solver.py
Author: H.F. van der Veen
Date: 23-05-2021
Description: Solve a Khun Phaen puzzle.
"""

from fringe import Fringe
from state import State
from piece import Piece


def generate_possible_moves(state, queue, seen):
    """Generate all valid moves and add to the queue and seen.

    For each piece, check if any of the directions is a valid move. An invalid move can be one that places the piece
    outside the field borders, or makes it overlap with a different piece. Also previously seen states are invalid.
    """
    # Generate all moves
    for piece in state.pieces:
        other_pieces = state.pieces ^ {piece}
        # Empty coordinates + this piece's coordinates are valid to move to
        valid_coords = state.free_coordinates() | piece.coordinates
        # Try to move in all directions
        for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            # If move is valid
            if (move := piece.move(x, y)) and len(move - valid_coords) == 0:
                # Generate a new state with the moved piece
                new_state = State(None, state, state.depth() + 1, state.goal,
                                  other_pieces | {Piece(piece.x() + x, piece.y() + y, piece.width(), piece.height())})
                # Check if we have already seen this new state
                if hash(new_state) not in seen:
                    queue.push(new_state)
                    seen.add(hash(new_state))


def khun_phaen_solver(puzzle):
    """Solve the Khun Phaen puzzle provided as input.

    This is done using breadth-first search, as the puzzle is quite small. For each state that is popped from the
    beginning of the queue all possible moves (that have not been encountered) are added to the queue and hashed and
    added to the set of seen states.
    """
    # Initialize queue and puzzle
    queue = Fringe("FIFO")
    state = puzzle
    seen = {hash(state)}

    generate_possible_moves(state, queue, seen)

    # Keep exploring the puzzle until a solution is found or no solution is possible.
    while not queue.is_empty():
        state = queue.pop()

        if state.is_solved():
            print("Solved!")
            state.print_solution(state.depth())
            queue.print_stats()
            return

        generate_possible_moves(state, queue, seen)

    print("Not solved :(")
    queue.print_stats()
