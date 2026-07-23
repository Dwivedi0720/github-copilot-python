"""Application entrypoint for the Flask Sudoku game."""

from flask import Flask

from config import Config
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
}

register_routes(app, CURRENT)

if __name__ == '__main__':
    app.run(debug=True)
