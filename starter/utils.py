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


def map_difficulty_to_clues(difficulty: str) -> int:
    """Map difficulty levels to a default number of puzzle clues."""
    difficulty_map = {
        'Easy': 42,
        'Medium': 33,
        'Hard': 25,
    }
    return difficulty_map.get(difficulty, 33)
