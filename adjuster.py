import sqlite3
from sklearn.neural_network import MLPClassifier
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import joblib

DB_PATH = "data/scores.db"

def suggest_difficulty(last_difficulty, last_time, last_errors):
    # If no DB or not enough data, default to Medium
    if not os.path.exists(DB_PATH):
        return "Easy"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT difficulty, time, errors FROM scores")
    data = c.fetchall()
    conn.close()
    if len(data) < 5:
        return "Easy"
    # Encode difficulties
    diff_map = {"Easy":0, "Medium":1, "Hard":2, "Expert":3}
    X = []
    y = []
    for d, t, e in data:
        if d in diff_map:
            X.append([diff_map[d], t, e])
            # Next difficulty is one step harder if time < 60 and errors < 2, else same or easier
            if t < 60 and e < 2 and diff_map[d] < 3:
                y.append(diff_map[d]+1)
            elif t > 120 or e > 4 and diff_map[d] > 0:
                y.append(diff_map[d]-1)
            else:
                y.append(diff_map[d])
    clf = MLPClassifier(hidden_layer_sizes=(5,), max_iter=500)
    clf.fit(X, y)
    plot_nn_decision_surface(clf)
    last = np.array([[diff_map.get(last_difficulty,1), last_time, last_errors]])
    pred = clf.predict(last)[0]
    rev_map = {v:k for k,v in diff_map.items()}
    return rev_map.get(pred, "Medium")

def get_action_features():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT AVG(time_delta), SUM(mistake), COUNT(*) FROM actions")
    row = c.fetchone()
    conn.close()
    if row:
        avg_time, total_mistakes, total_moves = row
        return [avg_time or 0, total_mistakes or 0, total_moves or 0]
    return [0, 0, 0]

def plot_nn_decision_surface(clf):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    d_range = np.arange(0, 4)
    t_range = np.linspace(10, 300, 8)
    e_range = np.arange(0, 10, 2)
    colors = ['g', 'b', 'r', 'k']
    for d in d_range:
        for t in t_range:
            for e in e_range:
                pred = clf.predict([[d, t, e]])[0]
                ax.scatter(d, t, e, c=colors[pred], marker='o')
    ax.set_xlabel('Difficulty')
    ax.set_ylabel('Time')
    ax.set_zlabel('Errors')
    plt.title("MLP Difficulty Suggestion Surface")
    plt.show()

def get_nn_activations(input_vec):
    clf = joblib.load("difficulty_classifier.pkl") # Use your adjuster model file
    activations = []
    X = np.array(input_vec).reshape(1, -1)
    layer_input = X

    # Input layer
    activations.append(layer_input[0].tolist())

    # Hidden layers and output
    for i in range(len(clf.coefs_)):
        layer_output = np.dot(layer_input, clf.coefs_[i]) + clf.intercepts_[i]
        # Apply activation function
        if clf.activation == 'relu':
            layer_output = np.maximum(0, layer_output)
        elif clf.activation == 'tanh':
            layer_output = np.tanh(layer_output)
        elif clf.activation == 'logistic':
            layer_output = 1 / (1 + np.exp(-layer_output))
        activations.append(layer_output[0].tolist())
        layer_input = layer_output
    return activations
