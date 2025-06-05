# SudokuAI

A smart, adaptive Sudoku game with AI-driven difficulty adjustment, neural network-based puzzle classification, and user performance tracking.

---

## Main Features

- **Sudoku Puzzle Generation & Solving**  
  Generates, solves, and analyzes Sudoku puzzles using backtracking and logical techniques.  
  *(See: `solver.py`)*

- **Difficulty Classification**  
  Classifies puzzles using both logic-based heuristics and a neural network classifier.  
  The neural network is trained on extracted puzzle features and stored in `difficulty_classifier.pkl`.  
  *(See: `solver.classify_difficulty_nn`)*

- **AI Difficulty Adjustment**  
  Suggests the next puzzle’s difficulty based on your recent performance using a neural network.  
  *(See: `adjuster.suggest_difficulty`)*

- **User Performance Tracking**  
  Stores game results and actions in an SQLite database, and provides plotting functions for progress and action patterns.  
  *(See: `tracking.py`)*

- **Graphical User Interface**  
  Play Sudoku and visualize the neural network in a Pygame-based UI.  
  *(See: `ui.run_ui`)*

- **Data Collection & Training Scripts**  
  Includes scripts to collect training data (`collect_training_data.py`) and train the difficulty classifier (`train_difficulty_classifier.py`).

---

## Workflow (`main.py`)

1. Ensures the difficulty classifier exists (trains if missing).
2. Initializes databases.
3. Loads the last user performance.
4. Uses AI to suggest the next puzzle difficulty.
5. Generates and classifies a new puzzle.
6. Runs the UI for gameplay.
7. On exit, prints the solution, score summary, and progress plots.

---

## Data & Models

- **Training Data:**  
  `sudoku_difficulty_data.csv` — Features and labels for training the classifier.

- **Model:**  
  `difficulty_classifier.pkl` — Trained neural network for puzzle difficulty classification.

- **Database:**  
  `scores.db` — Stores user scores and actions.

---

## Getting Started

1. Install requirements:
    ```sh
    pip install -r requirements.txt
    ```
2. Run `main.py`:
    ```sh
    python main.py
    ```
   The system will automatically generate training data and train the classifier if needed.

---

*Enjoy playing and improving your Sudoku skills with AI!*
