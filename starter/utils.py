"""Utility helpers for the Flask Sudoku application."""

from typing import List, Sequence


def find_incorrect_positions(
    board: Sequence[Sequence[int]],
    solution: Sequence[Sequence[int]],
) -> List[List[int]]:
    """Return the list of incorrect board positions compared with the solution."""
    incorrect: List[List[int]] = []
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return incorrect
