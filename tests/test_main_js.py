import os
from bs4 import BeautifulSoup


def test_main_js_input_validation_wired():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    js_path = os.path.join(root, 'starter', 'static', 'main.js')
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Ensure immediate validation runs on input events
    assert 'addEventListener(\'input\'' in content or 'addEventListener("input"' in content
    assert 'validateBoard()' in content
