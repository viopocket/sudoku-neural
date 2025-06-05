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