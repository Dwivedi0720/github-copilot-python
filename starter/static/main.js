// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let hintCount = 0;

const INVALID_CLASS = 'invalid';

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      // Mark block background class for 3x3 blocks
      const blockIndex = Math.floor(i / 3) * 3 + Math.floor(j / 3);
      input.classList.add(`block-${blockIndex}`);
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        validateBoard();
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function getBoardFromInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];

  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function findInvalidPositions(board) {
  const invalid = new Set();

  for (let row = 0; row < SIZE; row++) {
    for (let col = 0; col < SIZE; col++) {
      const value = board[row][col];
      if (!value) {
        continue;
      }

      for (let x = 0; x < SIZE; x++) {
        if (x !== col && board[row][x] === value) {
          invalid.add(row * SIZE + col);
          invalid.add(row * SIZE + x);
        }
      }

      for (let y = 0; y < SIZE; y++) {
        if (y !== row && board[y][col] === value) {
          invalid.add(row * SIZE + col);
          invalid.add(y * SIZE + col);
        }
      }

      const startRow = row - (row % 3);
      const startCol = col - (col % 3);
      for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
          const currentRow = startRow + i;
          const currentCol = startCol + j;
          if (
            (currentRow !== row || currentCol !== col) &&
            board[currentRow][currentCol] === value
          ) {
            invalid.add(row * SIZE + col);
            invalid.add(currentRow * SIZE + currentCol);
          }
        }
      }
    }
  }

  return invalid;
}

function updateInvalidHighlights(invalidPositions) {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');

  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (invalidPositions.has(idx)) {
      input.classList.add(INVALID_CLASS);
      input.classList.remove('correct');
    } else {
      input.classList.remove(INVALID_CLASS);
    }
  }
}

function validateBoard() {
  const board = getBoardFromInputs();
  const invalidPositions = findInvalidPositions(board);
  updateInvalidHighlights(invalidPositions);
  // If board is complete and there are no invalid positions, trigger completion
  checkForCompletion();
}

function stopTimer() {
  if (window.timerId) {
    clearInterval(window.timerId);
    window.timerId = null;
  }
}

function resetTimer() {
  stopTimer();
  window.elapsedSeconds = 0;
  updateTimerDisplay();
}

function startTimer() {
  resetTimer();
  window.timerId = setInterval(() => {
    window.elapsedSeconds = (window.elapsedSeconds || 0) + 1;
    updateTimerDisplay();
  }, 1000);
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60).toString().padStart(2, '0');
  const s = (seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function updateTimerDisplay() {
  const el = document.getElementById('timer');
  if (!el) return;
  el.innerText = formatTime(window.elapsedSeconds || 0);
}

function checkForCompletion() {
  const board = getBoardFromInputs();
  // Check for any empty cells
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      if (!board[i][j]) {
        return false;
      }
    }
  }

  const invalidPositions = findInvalidPositions(board);
  if (invalidPositions.size === 0) {
    const msg = document.getElementById('message');
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! Puzzle Solved!';
    // Stop any running timer (if present)
    stopTimer();

    // Disable inputs to prevent further editing
    const boardDiv = document.getElementById('sudoku-board');
    const inputs = boardDiv.getElementsByTagName('input');
    for (let idx = 0; idx < inputs.length; idx++) {
      inputs[idx].disabled = true;
    }

    // On completion, ask for player's name and save score
    try {
      const difficulty = document.getElementById('difficulty').value;
      const time = window.elapsedSeconds || 0;
      const name = window.prompt(`You solved the puzzle in ${formatTime(time)}. Enter your name for the leaderboard:`) || 'Anonymous';
      saveScoreToLeaderboard(name, time, difficulty, hintCount);
      // Update leaderboard UI if visible
      renderLeaderboard();
    } catch (e) {
      // ignore prompt failures in tests
    }

    return true;
  }
  return false;
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.classList.add('prefilled');
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
  validateBoard();
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  hintCount = 0;
  updateHintCounter();
  // Reset and start timer for new game
  resetTimer();
  startTimer();
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    msg.style.color = '#388e3c';
    msg.innerText = 'Congratulations! Puzzle Solved!';
    // Ensure timer stops when user explicitly checks and solved
    stopTimer();

    // Save score flow as above
    try {
      const difficulty = document.getElementById('difficulty').value;
      const time = window.elapsedSeconds || 0;
      const name = window.prompt(`You solved the puzzle in ${formatTime(time)}. Enter your name for the leaderboard:`) || 'Anonymous';
      saveScoreToLeaderboard(name, time, difficulty, hintCount);
      renderLeaderboard();
    } catch (e) {
      // ignore in tests
    }
  } else {
    msg.style.color = '#d32f2f';
    msg.innerText = 'Some cells are incorrect.';
  }
}

function updateHintCounter() {
  document.getElementById('hints-counter').innerText = `Hints used: ${hintCount}`;
}

async function getHint() {
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
  });
  
  const data = await res.json();
  const msg = document.getElementById('message');
  
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  
  const { row, col, value, hints_used } = data;
  
  // Update hint counter
  hintCount = hints_used;
  updateHintCounter();
  
  // Update the puzzle display
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = row * SIZE + col;
  const inp = inputs[idx];
  
  // Fill the cell with the hint value
  inp.value = value;
  inp.disabled = true;
  
  // Apply hint styling
  inp.classList.add('hint');
  
  // Clear any previous messages
  msg.innerText = '';

  // Re-validate board and detect completion after applying hint
  validateBoard();
}

// --- Leaderboard and Dark Mode Helpers ---
function getLeaderboard() {
  try {
    const raw = localStorage.getItem('sudoku_leaderboard') || '[]';
    return JSON.parse(raw);
  } catch (e) {
    return [];
  }
}

function saveLeaderboard(arr) {
  localStorage.setItem('sudoku_leaderboard', JSON.stringify(arr));
}

function saveScoreToLeaderboard(name, timeSeconds, difficulty, hints) {
  const list = getLeaderboard();
  list.push({name, time: timeSeconds, difficulty, hints});
  list.sort((a, b) => a.time - b.time);
  const top = list.slice(0, 10);
  saveLeaderboard(top);
}

function renderLeaderboard() {
  const el = document.getElementById('leaderboard');
  const tableBody = document.querySelector('#leaderboard-table tbody');
  const list = getLeaderboard();
  tableBody.innerHTML = '';
  list.forEach((item, idx) => {
    const tr = document.createElement('tr');
    const timeStr = formatTime(item.time || 0);
    tr.innerHTML = `<td>${idx + 1}</td><td>${escapeHtml(item.name)}</td><td>${timeStr}</td><td>${escapeHtml(item.difficulty)}</td><td>${item.hints}</td>`;
    tableBody.appendChild(tr);
  });
  if (el) el.classList.remove('hidden');
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function toggleLeaderboard(show) {
  const el = document.getElementById('leaderboard');
  if (!el) return;
  if (show) {
    renderLeaderboard();
  } else {
    el.classList.add('hidden');
  }
}

// Dark mode
function applyDarkMode(enabled) {
  if (enabled) {
    document.body.classList.add('dark');
  } else {
    document.body.classList.remove('dark');
  }
  localStorage.setItem('sudoku_dark_mode', enabled ? '1' : '0');
}

function loadDarkModePreference() {
  const val = localStorage.getItem('sudoku_dark_mode');
  applyDarkMode(val === '1');
}

// Wire buttons
window.addEventListener('load', () => {
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint-btn').addEventListener('click', getHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('dark-mode-toggle').addEventListener('click', () => {
    const enabled = !document.body.classList.contains('dark');
    applyDarkMode(enabled);
  });
  document.getElementById('show-leaderboard').addEventListener('click', () => toggleLeaderboard(true));
  document.getElementById('close-leaderboard').addEventListener('click', () => toggleLeaderboard(false));
  loadDarkModePreference();
  // initialize
  newGame();
});