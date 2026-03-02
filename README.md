# 🧬 Genetic Algorithms Applied Lab

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://jacobdarrossi-genetic-algotithms-lab.streamlit.app/)

An interactive laboratory for **Evolutionary Computing**, focusing on solving complex optimization problems through **Genetic Algorithms (GA)**. This project is a modern Python re-engineering of academic engines originally developed in Java.

🔗 **Live Demo:** [https://jacobdarrossi-genetic-algotithms-lab.streamlit.app/](https://jacobdarrossi-genetic-algotithms-lab.streamlit.app/)

## 📜 The Story
This repository bridges a decade of development experience:
* **Original (2013/2014):** Developed in Java using the SWT (Standard Widget Toolkit) during my early academic years.
* **Modern Version (2026):** Re-imagined in Python 3.13+, utilizing **Streamlit** for reactive interfaces and **Pandas** for real-time data visualization of genetic convergence.

## 🧠 Implemented Challenges

### 1. 👑 N-Queens Puzzle
The classic constraint satisfaction problem: place 8 queens on a chessboard so that no two queens threaten each other.
* **Fitness:** Minimizing the number of conflicting pairs (collisions).
* **Visualization:** Real-time rendering of the best board in each generation.

### 2. 🎒 Knapsack Problem
A combinatorial optimization challenge: maximize the total value of items within strict **Weight** and **Volume** limits.
* **Fitness:** A multi-constraint function that penalizes capacity violations (125kg / 125L) while maximizing ROI based on a 25-product matrix.
* **Metrics:** Live tracking of weight, volume, and currency accumulation.



## 🛠️ Tech Stack
* **Language:** [Python 3.13+](https://www.python.org/)
* **Interface:** [Streamlit](https://streamlit.io/)
* **Data Processing:** [NumPy](https://numpy.org/) & [Pandas](https://pandas.pydata.org/)


## 📂 Project Structure
```text
/src
├── main.py              # Central entry point & Landing Page
├── queens/
│   ├── engine.py        # GA Logic for N-Queens
│   └── app.py           # Queens UI Module
└── knapsack/
    ├── engine.py        # GA Logic for Knapsack
    └── app.py           # Knapsack UI Module

## 🚀 How to Run Locally

1. **Clone the repository:**
    ```bash
    git clone [https://github.com/jacobdarrossi/genetic-algorithms-lab.git](https://github.com/jacobdarrossi/genetic-algorithms-lab.git)
    cd genetic-algorithms-lab
    ```
2. **Set up a virtual environment:**

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\Scripts\activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run App:**
    ```bash
    streamlit run src/main.py
    ```