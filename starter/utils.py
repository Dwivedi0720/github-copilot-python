"""Utility helpers for the Flask Sudoku application."""

import random
from typing import List, Optional, Sequence, Tuple


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


def get_hint(
    puzzle: List[List[int]],
    solution: List[List[int]],
) -> Optional[Tuple[int, int, int]]:
    """
    Find and return a hint for the player.
    
    Selects a random empty cell (cell with value 0) from the puzzle
    and returns its position along with the correct value from the solution.
    
    Args:
        puzzle: Current state of the 9x9 Sudoku puzzle (with 0s for empty cells)
        solution: The complete 9x9 Sudoku solution
        
    Returns:
        A tuple of (row, col, value) for the hint, or None if no empty cells exist
    """
    empty_cells = []
    
    # Find all empty cells
    for i in range(len(puzzle)):
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                empty_cells.append((i, j))
    
    # Return None if no empty cells (puzzle is complete)
    if not empty_cells:
        return None
    
    # Select a random empty cell
    row, col = random.choice(empty_cells)
    value = solution[row][col]
    
    return row, col, value
