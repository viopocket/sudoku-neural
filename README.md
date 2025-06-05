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
  The neural network visualization now reflects the **real activations** of the classifier model for the current puzzle.  
  *(See: `ui.run_ui` and `draw_nn_diagram`)*

- **Data Collection & Training Scripts**  
  Includes scripts to collect training data (`collect_training_data.py`) and train the difficulty classifier (`train_difficulty_classifier.py`).  
  The main script (`main.py`) automates this process if the classifier is missing.

---

## How It Works: Step-by-Step Flow

1. **Startup & Classifier Check**
   - When you run `main.py`, the program checks if the neural network model for puzzle classification (`difficulty_classifier.pkl`) exists.
   - If it’s missing, the system automatically generates training data and trains the model—no manual steps required.

2. **Database Initialization**
   - The program initializes SQLite databases to track your scores and actions.

3. **Load Last Performance**
   - Your most recent game performance (difficulty, time, errors) is loaded from the database to personalize your experience.

4. **AI Suggests Next Difficulty**
   - A neural network in `adjuster.py` analyzes your recent performance and suggests the next puzzle’s difficulty, adapting the challenge to your skill level.

5. **Puzzle Generation & Classification**
   - A new Sudoku puzzle is generated.
   - The neural network classifier in `solver.py` analyzes the puzzle’s features and predicts its difficulty (Easy, Medium, Hard, Expert).

6. **Neural Network Activations for Visualization**
   - Features from the generated puzzle are extracted and fed into the classifier neural network.
   - The activations (values at each layer of the network) are captured for visualization.

7. **Gameplay in the UI**
   - The Pygame-based UI launches, displaying the Sudoku puzzle and a live visualization of the neural network’s activations for the current puzzle.
   - You play the puzzle; your moves, errors, and time are tracked.

8. **Performance Tracking & Analysis**
   - After you finish, your performance is saved to the database.
   - The solution to the puzzle is displayed.
   - A summary of your performance and progress plots are shown.

---

## Visual Summary

```mermaid
flowchart TD
    A[Start / main.py] --> B{Classifier Exists?}
    B -- No --> C[Generate Training Data<br>and Train Model]
    C --> D[Initialize Databases]
    B -- Yes --> D
    D --> E[Load Last Performance]
    E --> F[AI Suggests Next Difficulty<br>(adjuster.py, NN)]
    F --> G[Generate Sudoku Puzzle]
    G --> H[Classify Puzzle Difficulty<br>(solver.py, NN)]
    H --> I[Extract Features & Activations]
    I --> J[Run Game UI<br>with Live NN Visualization]
    J --> K[Track & Save Performance]
    K --> L[Show Solution, Summary, and Progress]
    L --> M[End]

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

