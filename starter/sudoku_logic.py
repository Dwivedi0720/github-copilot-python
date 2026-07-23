import copy
import random

SIZE = 9
EMPTY = 0
MAX_SOLUTIONS_TO_CHECK = 2  # Stop counting after finding 2 solutions


def deep_copy(board):
    """Create a deep copy of a Sudoku board."""
    return copy.deepcopy(board)


def create_empty_board():
    """Create an empty 9x9 Sudoku board filled with zeros."""
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def is_safe(board, row, col, num):
    """Check if placing num at (row, col) is safe according to Sudoku rules."""
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def fill_board(board):
    """Fill a board with a valid Sudoku solution using backtracking."""
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def count_solutions(puzzle, max_count=MAX_SOLUTIONS_TO_CHECK):
    """
    Count the number of solutions for a given puzzle.
    
    Stops counting after finding max_count solutions to optimize performance.
    This allows us to verify that exactly one solution exists without
    exhaustively exploring all possibilities.
    
    Args:
        puzzle: A 9x9 Sudoku puzzle (list of lists)
        max_count: Maximum number of solutions to find before stopping
        
    Returns:
        The number of solutions found (up to max_count)
    """
    board = deep_copy(puzzle)
    solution_count = [0]  # Use list to allow modification in nested function
    
    def solve(board):
        """Recursively solve the puzzle and count all solutions."""
        # Stop early if we've already found enough solutions
        if solution_count[0] >= max_count:
            return
        
        # Find next empty cell
        for row in range(SIZE):
            for col in range(SIZE):
                if board[row][col] == EMPTY:
                    for num in range(1, SIZE + 1):
                        if is_safe(board, row, col, num):
                            board[row][col] = num
                            solve(board)
                            board[row][col] = EMPTY
                    return
        
        # No empty cells found - we've found a complete solution
        solution_count[0] += 1
    
    solve(board)
    return solution_count[0]


def is_valid_puzzle(puzzle):
    """
    Verify that a puzzle has exactly one unique solution.
    
    Args:
        puzzle: A 9x9 Sudoku puzzle (list of lists)
        
    Returns:
        True if puzzle has exactly one solution, False otherwise
    """
    return count_solutions(puzzle, max_count=2) == 1


def remove_cells(board, clues):
    """
    Remove cells from a solved board to create a valid puzzle with one solution.
    
    This function intelligently removes cells, verifying that each removal
    maintains the property of having exactly one unique solution.
    
    Args:
        board: A completed Sudoku solution (9x9 board)
        clues: Number of cells to keep in the puzzle
    """
    solution = deep_copy(board)
    cells_to_remove = SIZE * SIZE - clues
    removed_count = 0
    
    while removed_count < cells_to_remove:
        # Randomly select a cell to remove
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        
        # Skip if already empty
        if board[row][col] == EMPTY:
            continue
        
        # Store the original value
        original_value = board[row][col]
        board[row][col] = EMPTY
        
        # Verify the puzzle still has exactly one solution
        if is_valid_puzzle(board):
            removed_count += 1
        else:
            # Restore the cell if removal creates multiple solutions
            board[row][col] = original_value


def generate_puzzle(clues=35, max_attempts=5):
    """
    Generate a Sudoku puzzle with exactly one unique solution.
    
    Attempts to create a puzzle with the specified number of clues.
    If the puzzle doesn't have exactly one solution, retries.
    
    Args:
        clues: Number of given cells in the puzzle (default 35)
        max_attempts: Maximum number of generation attempts (default 5)
        
    Returns:
        A tuple of (puzzle, solution) where:
        - puzzle: 9x9 board with empty cells (0s) for cells to fill
        - solution: 9x9 completed Sudoku solution
    """
    for attempt in range(max_attempts):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        
        # Remove cells to create the puzzle
        remove_cells(board, clues)
        puzzle = deep_copy(board)
        
        # Verify the puzzle has exactly one solution
        if is_valid_puzzle(puzzle):
            return puzzle, solution
    
    # Fallback: return the last generated puzzle even if validation failed
    # This ensures the game doesn't break, though the puzzle may have multiple solutions
    return puzzle, solution
