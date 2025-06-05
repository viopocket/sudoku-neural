import os

from solver import generate_full_grid, remove_numbers, solve, logical_solve, classify_difficulty_nn, extract_features, classify_difficulty
from tracking import get_summary, save_performance, get_last_performance, plot_progress, init_db, init_actions_db
from ui import run_ui
from adjuster import suggest_difficulty, get_nn_activations

def ensure_classifier():
    if not os.path.exists("difficulty_classifier.pkl"):
        print("difficulty_classifier.pkl not found. Generating training data and training model...")
        import csv

        # Step 1: Collect training data
        NUM_SAMPLES = 200
        with open("sudoku_difficulty_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["num_clues", "naked_single", "hidden_single", "naked_pair", "pointing_pair", "label"])
            for _ in range(NUM_SAMPLES):
                full_grid = generate_full_grid()
                puzzle = remove_numbers(full_grid, attempts=30)
                features = extract_features(puzzle)
                label = classify_difficulty(puzzle)
                writer.writerow(features + [label])

        # Step 2: Train the classifier
        import pandas as pd
        from sklearn.neural_network import MLPClassifier
        import joblib

        df = pd.read_csv("sudoku_difficulty_data.csv")
        X = df[["num_clues", "naked_single", "hidden_single", "naked_pair", "pointing_pair"]].values
        y = df["label"].values

        clf = MLPClassifier(hidden_layer_sizes=(10, 10), max_iter=1000, random_state=42)
        clf.fit(X, y)
        joblib.dump(clf, "difficulty_classifier.pkl")
        print("Model trained and saved as difficulty_classifier.pkl")

if __name__ == "__main__":
    ensure_classifier()
    init_db()
    init_actions_db()
    last = get_last_performance()
    if last:
        recent_difficulty, recent_time, recent_errors = last
    else:
        recent_difficulty = "Medium"
        recent_time = 50.0
        recent_errors = 1

    # AI suggests next difficulty
    suggested = suggest_difficulty(recent_difficulty, recent_time, recent_errors)
    print("\nAI-Suggested Difficulty:", suggested)

    # Generate and classify puzzle
    full_grid = generate_full_grid()
    puzzle = remove_numbers(full_grid, attempts=30)
    difficulty = classify_difficulty_nn(puzzle)
    print("\nClassified Difficulty (NN):", difficulty)

    print("Generated Puzzle:")
    for row in puzzle:
        print(row)

    # Prepare input vector for classifier NN (use puzzle features)
    input_vec = extract_features(puzzle)  # Always returns 5 features
    activations = get_nn_activations(input_vec)
    run_ui(puzzle, difficulty, suggested, nn_activations=activations)

    # Print solution
    print("\nSolution:")
    solve(puzzle)
    for row in puzzle:
        print(row)

    # Print score summary
    print("\nScore Summary:")
    for row in get_summary():
        print(f"Difficulty: {row[0]}, Avg Time: {row[1]:.2f}s, Avg Errors: {row[2]:.2f}")
    print("\nThank you for playing!")
    print("Visit us at: https://www.pocketfun.com/sudoku")
    plot_progress()
