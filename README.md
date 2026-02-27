# 👑 N-Queens Genetic Evolution

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seu-app.streamlit.app)

An interactive visualization of the **N-Queens Puzzle** solved through a **Genetic Algorithm**. This project is a modern Python reconstruction of an academic engine originally developed in Java 13 years ago.

## 📜 The Story
This repository is more than just an algorithm; it's a bridge between my past and present as a developer. 
* **Original (2011):** Developed in Java using the SWT (Standard Widget Toolkit).
* **Modern Version (2026):** Re-engineered in Python, utilizing high-performance libraries like NumPy and Pandas for data handling, and Streamlit for a reactive web interface.

## 🧠 How it Works
The challenge is to place 8 queens on an 8x8 chessboard so that no two queens threaten each other. The Genetic Algorithm solves this by:
1. **Population:** Creating a set of random boards.
2. **Fitness:** Calculating the number of collisions (conflicts) on each board.
3. **Selection:** Choosing the best boards based on the Selection Tax.
4. **Crossover:** Breeding the best individuals to create a new generation.
5. **Evolution:** Repeating the process until a perfect solution (Fitness = 0) is found.

## 🛠️ Tech Stack
* **Language:** [Python 3.13+](https://www.python.org/)
* **Interface:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [NumPy](https://numpy.org/) & [Pandas](https://pandas.pydata.org/)
* **Engine:** Pure Python (Logic migrated from original Java source)

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/8queens-evolution.git](https://github.com/your-username/8queens-evolution.git)
   cd 8queens-evolution