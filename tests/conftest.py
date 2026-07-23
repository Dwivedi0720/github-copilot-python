import os
import sys
import pytest

# Add the starter directory to Python's import path
sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "starter"))
)

import app as flask_app


@pytest.fixture
def client():
    # Reset game state before every test
    flask_app.CURRENT["puzzle"] = None
    flask_app.CURRENT["solution"] = None

    flask_app.app.config["TESTING"] = True

    with flask_app.app.test_client() as client:
        yield client