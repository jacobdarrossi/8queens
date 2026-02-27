import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import os

# Ensure Python finds engine.py in the src/ folder
sys.path.append(os.path.dirname(__file__))

from engine import Population

# Page Configuration - Set to 'wide' to help with horizontal space
st.set_page_config(page_title="N-Queens Genetic Evolution", page_icon="👑", layout="wide")

# Custom CSS for medium-sized crowns and zero-scroll layout
# Custom CSS for UI Cleanliness, Mega Crowns, and Centering
st.markdown("""
    <style>
    /* Remove Streamlit Header (Deploy button and Menu) */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .stTable {
        display: flex;
        justify-content: center;
    }

    /* Cell and Board Styling */
    td {
        padding: 0px !important;
        margin: 0px !important;
        height: 65px !important; 
        width: 65px !important;  
        vertical-align: middle !important;
        text-align: center !important;
        border: none !important;
        overflow: hidden;
    }
    table {
        border-collapse: collapse !important;
        margin-left: auto;
        margin-right: auto;
        table-layout: fixed;
    }
    .q-text {
        font-size: 45px !important; 
        line-height: 65px !important;
        display: block;
        width: 100%;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("👑 N-Queens: Genetic Evolution")

# --- Sidebar ---
st.sidebar.header("Evolution Parameters")
gen_count = st.sidebar.number_input("Generations", min_value=1, value=50, help="Cycles of evolution.")
pop_size = st.sidebar.number_input("Population Size", min_value=2, value=20, help="Total boards per generation.")
select_perc = st.sidebar.slider("Selection Tax (%)", 10, 90, 50, help="Percentage of survivors.")


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


# --- Execution Logic ---
if st.button("Start Evolution"):
    pop = Population(pop_size, select_perc)

    progress_bar = st.progress(0)
    status_text = st.empty()
    board_plot = st.empty()

    metrics_col1, metrics_col2 = st.columns(2)
    best_fitness_val = metrics_col1.empty()
    current_gen_val = metrics_col2.empty()

    for g in range(gen_count):
        pop.select_best()
        pop.breed_new_generation()

        best_ind = pop.get_best()

        progress = (g + 1) / gen_count
        progress_bar.progress(progress)
        status_text.text(f"Generation {g + 1}/{gen_count}")

        # Display fitness (Pairs of attacking queens)
        best_fitness_val.metric("Best Fitness (Collisions)", int(best_ind.fitness / 2))
        current_gen_val.metric("Current Gen", g + 1)

        board_plot.markdown(render_board(best_ind.genes), unsafe_allow_html=True)

        time.sleep(0.05)

        if best_ind.fitness == 0:
            st.balloons()
            st.success("Perfect Solution Found!")
            break

    if pop.get_best().fitness > 0:
        st.warning("Finished. Increase population or generations to find a perfect 0-collision solution.")