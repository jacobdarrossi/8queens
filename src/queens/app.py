import streamlit as st
import pandas as pd
import time
import sys
import os

# Ajuste de path para encontrar o engine.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .engine import Population


def run_queens_app():
    st.markdown("""
        <style>
        header {visibility: hidden;}
        footer {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        .stTable { display: flex; justify-content: center; }
        td {
            padding: 0px !important; height: 65px !important; width: 65px !important;
            vertical-align: middle !important; text-align: center !important; border: none !important;
        }
        .q-text { font-size: 45px !important; line-height: 65px !important; display: block; }
        </style>
        """, unsafe_allow_html=True)

    st.title("👑 N-Queens: Evolution Lab")
    st.info("The goal is to place 8 queens on the board so that no two queens threaten each other.")

    # --- Sidebar com Parâmetros e Helpers ---
    st.sidebar.header("Evolution Control")

    gen_count = st.sidebar.number_input(
        "Generations",
        min_value=1,
        value=100,
        help="The maximum number of evolutionary cycles. More generations allow more time for finding a perfect solution."
    )

    pop_size = st.sidebar.number_input(
        "Population Size",
        min_value=10,
        value=50,
        help="Number of individuals (boards) in each generation. Larger populations increase genetic diversity but require more processing."
    )

    mutation_rate = st.sidebar.slider(
        "Mutation Rate (%)",
        0, 100, 10,
        help="Probability of a random change in an individual's DNA. This prevents the algorithm from getting stuck in local optima by introducing new genetic traits."
    )

    selection_tax = st.sidebar.slider(
        "Selection Tax (Survival %)",
        10, 90, 50,
        help="The percentage of the best individuals that will survive to breed the next generation. High values preserve traits, while low values favor aggressive competition."
    )

    #

    def render_board(genes):
        n = len(genes)
        display_board = pd.DataFrame("", index=range(n), columns=range(n))
        for row, col in enumerate(genes):
            display_board.iloc[row, col] = '<span class="q-text">👑</span>'

        def style_chess(df):
            styles = pd.DataFrame('', index=df.index, columns=df.columns)
            for r in range(n):
                for c in range(n):
                    color = '#f0d9b5' if (r + c) % 2 == 0 else '#b58863'
                    styles.iloc[r, c] = f'background-color: {color}; height: 65px; width: 65px;'
            return styles

        return display_board.style.apply(style_chess, axis=None).to_html(escape=False)

    # --- Lógica de Execução ---
    if st.button("Run Experiment", type="primary", use_container_width=True):
        pop = Population(pop_size, selection_tax)

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Current Best Candidate")
            board_plot = st.empty()
        with col2:
            st.subheader("Fitness Progress")
            st.caption("Lower is better (0 = Solution)")
            chart_plot = st.empty()

        fitness_history = []

        for g in range(gen_count):
            pop.select_best()
            pop.breed_new_generation(mutation_rate)

            best_ind = pop.get_best()
            # Fitness logic: dividing by 2 to show actual collisions
            current_fitness = int(best_ind.fitness / 2)
            fitness_history.append(current_fitness)

            board_plot.markdown(render_board(best_ind.genes), unsafe_allow_html=True)
            chart_plot.line_chart(fitness_history)

            if current_fitness == 0:
                st.balloons()
                st.success(f"Perfect solution found at generation {g + 1}!")
                break

            time.sleep(0.01)