import sqlite3
import os
import matplotlib.pyplot as plt

DB_PATH = "data/scores.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY,
        difficulty TEXT,
        time REAL,
        errors INTEGER
    )""")
    conn.commit()
    conn.close()

def save_performance(difficulty, time, errors):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO scores (difficulty, time, errors) VALUES (?, ?, ?)",
              (difficulty, time, errors))
    conn.commit()
    conn.close()

def get_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""SELECT difficulty, AVG(time), AVG(errors)
                 FROM scores GROUP BY difficulty""")
    rows = c.fetchall()
    conn.close()
    return rows

def get_last_performance():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT difficulty, time, errors FROM scores ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row

def plot_progress():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, time, errors, difficulty FROM scores ORDER BY id")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No data to plot.")
        return
    ids = [row[0] for row in rows]
    times = [row[1] for row in rows]
    errors = [row[2] for row in rows]
    difficulties = [row[3] for row in rows]

    plt.figure(figsize=(10,5))
    plt.subplot(2,1,1)
    plt.plot(ids, times, marker='o')
    plt.title("Progres Sudoku")
    plt.ylabel("Timp (s)")
    plt.subplot(2,1,2)
    plt.plot(ids, errors, marker='x', color='red')
    plt.xlabel("Joc #")
    plt.ylabel("Erori")
    plt.tight_layout()
    plt.show()

def init_actions_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS actions (
        id INTEGER PRIMARY KEY,
        row INTEGER,
        col INTEGER,
        value INTEGER,
        time_delta REAL,
        mistake INTEGER
    )""")
    conn.commit()
    conn.close()

def save_action(row, col, value, time_delta, mistake):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO actions (row, col, value, time_delta, mistake) VALUES (?, ?, ?, ?, ?)",
              (row, col, value, time_delta, mistake))
    conn.commit()
    conn.close()

def plot_action_patterns():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT time_delta, mistake FROM actions")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("No action data to plot.")
        return

    time_deltas = [row[0] for row in rows if row[0] is not None]
    mistakes = [row[1] for row in rows if row[1] is not None]

    plt.figure(figsize=(12,5))

    # Histogram of time between moves
    plt.subplot(1,2,1)
    plt.hist(time_deltas, bins=20, color='skyblue', edgecolor='black')
    plt.title("Distribuția timpului între mutări")
    plt.xlabel("Secunde între mutări")
    plt.ylabel("Frecvență")

    # Pie chart of mistakes vs correct moves
    plt.subplot(1,2,2)
    correct = len(mistakes) - sum(mistakes)
    plt.pie([correct, sum(mistakes)], labels=["Corecte", "Greșeli"], autopct='%1.1f%%', colors=['lightgreen', 'salmon'])
    plt.title("Procentaj mutări corecte vs greșeli")

    plt.tight_layout()
    plt.show()
