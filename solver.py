import random
import copy
import numpy as np
import joblib

GRID_SIZE = 9
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

def generate_full_grid():
    # Simple backtracking Sudoku generator
    def fill(grid):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if grid[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for n in nums:
                        if is_valid(grid, i, j, n):
                            grid[i][j] = n
                            if fill(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    grid = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
    fill(grid)
    return grid

def is_valid(grid, row, col, num):
    for i in range(GRID_SIZE):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row, start_col = 3*(row//3), 3*(col//3)
    for i in range(3):
        for j in range(3):
            if grid[start_row+i][start_col+j] == num:
                return False
    return True

def remove_numbers(grid, attempts=30):
    puzzle = copy.deepcopy(grid)
    while attempts > 0:
        row, col = random.randint(0,8), random.randint(0,8)
        while puzzle[row][col] == 0:
            row, col = random.randint(0,8), random.randint(0,8)
        backup = puzzle[row][col]
        puzzle[row][col] = 0
        attempts -= 1
    return puzzle

def solve(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                for n in range(1, 10):
                    if is_valid(grid, i, j, n):
                        grid[i][j] = n
                        if solve(grid):
                            return True
                        grid[i][j] = 0
                return False
    return True

def logical_solve(puzzle):
    # Applies naked singles and hidden singles until stuck
    logic_grid = copy.deepcopy(puzzle)
    steps = {'naked_single': 0, 'hidden_single': 0, 'naked_pair': 0, 'pointing_pair': 0}
    progress = True

    def get_candidates(grid, row, col):
        if grid[row][col] != 0:
            return set()
        candidates = set(range(1, 10))
        # Remove used numbers in row and column
        candidates -= set(grid[row])
        candidates -= {grid[i][col] for i in range(9)}
        # Remove used numbers in box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                candidates.discard(grid[start_row + i][start_col + j])
        return candidates

    while progress:
        progress = False
        # Naked singles
        for i in range(9):
            for j in range(9):
                if logic_grid[i][j] == 0:
                    candidates = get_candidates(logic_grid, i, j)
                    if len(candidates) == 1:
                        logic_grid[i][j] = candidates.pop()
                        steps['naked_single'] += 1
                        progress = True
        # Hidden singles
        for unit in range(9):
            # Rows
            for num in range(1, 10):
                positions = [col for col in range(9) if logic_grid[unit][col] == 0 and num in get_candidates(logic_grid, unit, col)]
                if len(positions) == 1:
                    logic_grid[unit][positions[0]] = num
                    steps['hidden_single'] += 1
                    progress = True
            # Columns
            for num in range(1, 10):
                positions = [row for row in range(9) if logic_grid[row][unit] == 0 and num in get_candidates(logic_grid, row, unit)]
                if len(positions) == 1:
                    logic_grid[positions[0]][unit] = num
                    steps['hidden_single'] += 1
                    progress = True
            # Boxes
            start_row, start_col = 3 * (unit // 3), 3 * (unit % 3)
            for num in range(1, 10):
                positions = []
                for i in range(3):
                    for j in range(3):
                        r, c = start_row + i, start_col + j
                        if logic_grid[r][c] == 0 and num in get_candidates(logic_grid, r, c):
                            positions.append((r, c))
                if len(positions) == 1:
                    r, c = positions[0]
                    logic_grid[r][c] = num
                    steps['hidden_single'] += 1
                    progress = True

    return steps, logic_grid

def classify_difficulty(puzzle):
    # Classify based on logical steps needed to solve
    steps, logic_grid = logical_solve(puzzle)
    total_steps = steps['naked_single'] + steps['hidden_single']
    filled = all(all(cell != 0 for cell in row) for row in logic_grid)
    if not filled:
        return "Expert"
    if steps['naked_single'] > 0 and total_steps <= 30:
        return "Easy"
    elif steps['hidden_single'] > 0 or total_steps <= 60:
        return "Medium"
    else:
        return "Hard"

def extract_features(puzzle):
    num_clues = sum(cell != 0 for row in puzzle for cell in row)
    steps, _ = logical_solve(puzzle)
    return [
        num_clues,
        steps['naked_single'],
        steps['hidden_single'],
        steps['naked_pair'],
        steps['pointing_pair'],
    ]

def classify_difficulty_nn(puzzle):
    features = np.array(extract_features(puzzle)).reshape(1, -1)
    clf = joblib.load("difficulty_classifier.pkl")
    pred = clf.predict(features)[0]
    return pred
