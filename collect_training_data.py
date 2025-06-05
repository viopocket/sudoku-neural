import csv
from solver import generate_full_grid, remove_numbers, extract_features, classify_difficulty

NUM_SAMPLES = 200  # You can increase this for more data

with open("sudoku_difficulty_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["num_clues", "naked_single", "hidden_single", "naked_pair", "pointing_pair", "label"])
    for _ in range(NUM_SAMPLES):
        full_grid = generate_full_grid()
        puzzle = remove_numbers(full_grid, attempts=30)
        features = extract_features(puzzle)
        label = classify_difficulty(puzzle)  # Use your current logic-based classifier for labeling
        writer.writerow(features + [label])
print("Data collection complete.")