# sudoku-neural
 Python project for an interactive Sudoku game with AI-driven difficulty adjustment and user performance tracking

 Main Features
Sudoku Puzzle Generation & Solving:
Uses backtracking and logical techniques to generate, solve, and analyze Sudoku puzzles (solver.py).

Difficulty Classification:
Classifies puzzles using both logic-based heuristics and a neural network classifier (solver.classify_difficulty_nn).
The classifier is trained on features extracted from puzzles and stored in difficulty_classifier.pkl.

AI Difficulty Adjustment:
Suggests the next puzzle’s difficulty based on user performance using a neural network (adjuster.suggest_difficulty).

User Performance Tracking:
Stores game results and actions in an SQLite database (tracking.py), and provides plotting functions for progress and action patterns.

Graphical User Interface:
Implements a Pygame-based UI for playing Sudoku and visualizing the neural network (ui.run_ui).

Data Collection & Training Scripts:
Includes scripts to collect training data (collect_training_data.py) and train the difficulty classifier (train_difficulty_classifier.py).

Workflow (main.py)
Ensures the difficulty classifier exists (trains if missing).
Initializes databases.
Loads the last user performance.
Uses AI to suggest the next difficulty.
Generates and classifies a new puzzle.
Runs the UI for the user to play.
On exit, prints the solution, score summary, and progress plots.
Data & Models
Training Data:
sudoku_difficulty_data.csv contains features and labels for training the classifier.

Model:
difficulty_classifier.pkl is a trained neural network for puzzle difficulty classification.

Database:
scores.db stores user scores and actions.
