"""Flask route definitions for the Sudoku application."""

from flask import Flask, jsonify, render_template, request
import sudoku_logic
from typing import Any, Dict

from utils import find_incorrect_positions, map_difficulty_to_clues, get_hint


def register_routes(app: Flask, current_state: Dict[str, Any]) -> None:
    """Register routes on the provided Flask app."""

    @app.route('/')
    def index() -> str:
        return render_template('index.html')

    @app.route('/new')
    def new_game() -> Any:
        clues_arg = request.args.get('clues')
        if clues_arg is not None:
            clues = int(clues_arg)
        else:
            difficulty = request.args.get('difficulty', 'Medium')
            clues = map_difficulty_to_clues(difficulty)
        puzzle, solution = sudoku_logic.generate_puzzle(clues)
        current_state['puzzle'] = puzzle
        current_state['solution'] = solution
        current_state['hints_used'] = 0
        return jsonify({'puzzle': puzzle})

    @app.route('/check', methods=['POST'])
    def check_solution() -> Any:
        data = request.json or {}
        board = data.get('board')
        solution = current_state.get('solution')
        if solution is None:
            return jsonify({'error': 'No game in progress'}), 400
        incorrect = find_incorrect_positions(board, solution)
        return jsonify({'incorrect': incorrect})

    @app.route('/hint', methods=['POST'])
    def hint() -> Any:
        """Provide a hint by filling one empty cell with the correct value."""
        puzzle = current_state.get('puzzle')
        solution = current_state.get('solution')
        
        if puzzle is None or solution is None:
            return jsonify({'error': 'No game in progress'}), 400
        
        # Get a hint (random empty cell with its solution value)
        hint_data = get_hint(puzzle, solution)
        
        if hint_data is None:
            return jsonify({'error': 'No empty cells available'}), 400
        
        row, col, value = hint_data
        
        # Fill the cell in the current puzzle state
        current_state['puzzle'][row][col] = value
        
        # Increment hints used counter
        current_state['hints_used'] = current_state.get('hints_used', 0) + 1
        
        return jsonify({
            'row': row,
            'col': col,
            'value': value,
            'hints_used': current_state['hints_used']
        })
