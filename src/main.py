import streamlit as st
import pandas as pd
import numpy as np
import time
import sys
import os

# Ajuste de path para encontrar o engine.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from engine import Population

st.set_page_config(page_title="N-Queens Genetic Evolution", page_icon="👑", layout="wide")

# CSS para esconder o menu e ajustar as rainhas (suas configurações favoritas)
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

# --- Sidebar com Parâmetros ---
st.sidebar.header("Evolution Control")
gen_count = st.sidebar.number_input("Generations", min_value=1, value=100)
pop_size = st.sidebar.number_input("Population Size", min_value=10, value=50)
mutation_rate = st.sidebar.slider("Mutation Rate (%)", 0, 100, 10)  # Novo!
selection_tax = st.sidebar.slider("Selection Tax (Survival %)", 10, 90, 50)

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
if st.button("Run Experiment"):
    # Inicializa a população (garanta que seu engine.py aceite mutation_rate se possível)
    pop = Population(pop_size, selection_tax)

    # Containers para atualização em tempo real
    col1, col2 = st.columns([1, 1])
    with col1:
        board_plot = st.empty()
    with col2:
        st.subheader("Fitness Progress")
        chart_plot = st.empty()

    fitness_history = []

    for g in range(gen_count):
        pop.select_best()
        pop.breed_new_generation(mutation_rate)  # Se o seu engine suportar, passe mutation_rate aqui

        best_ind = pop.get_best()
        current_fitness = int(best_ind.fitness / 2)
        fitness_history.append(current_fitness)

        # Atualiza o Tabuleiro
        board_plot.markdown(render_board(best_ind.genes), unsafe_allow_html=True)

        # Atualiza o Gráfico de Linha
        chart_plot.line_chart(fitness_history)

        if current_fitness == 0:
            st.balloons()
            st.success(f"Perfect solution found at generation {g + 1}!")
            break

        time.sleep(0.01)