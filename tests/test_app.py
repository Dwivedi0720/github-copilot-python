import json


def test_index_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<title>Sudoku Game</title>' in response.data


def test_new_game_generates_puzzle(client):
    response = client.get('/new?clues=30')
    assert response.status_code == 200
    data = response.get_json()
    assert 'puzzle' in data
    assert isinstance(data['puzzle'], list)
    assert len(data['puzzle']) == 9
    assert all(len(row) == 9 for row in data['puzzle'])


def test_check_solution_without_game_returns_error(client):
    payload = {'board': [[0] * 9 for _ in range(9)]}
    response = client.post('/check', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'No game in progress'


def test_check_solution_returns_incorrect_positions(client):
    # Start a new game to populate CURRENT['solution']
    response = client.get('/new?clues=35')
    assert response.status_code == 200
    puzzle_data = response.get_json()['puzzle']

    # Create an invalid board by changing one cell
    board = [row.copy() for row in puzzle_data]
    board[0][0] = 1 if board[0][0] != 1 else 2

    response = client.post('/check', json={'board': board})
    assert response.status_code == 200
    data = response.get_json()
    assert 'incorrect' in data
    assert isinstance(data['incorrect'], list)
    assert [0, 0] in data['incorrect']
