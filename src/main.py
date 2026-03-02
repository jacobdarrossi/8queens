import streamlit as st

# Configuração da página
st.set_page_config(page_title="Genetic Algorithms Lab", page_icon="🧬", layout="wide")

# Estilização CSS para um visual mais limpo
st.markdown("""
    <style>
    .main-title { font-size: 45px; font-weight: bold; color: #4F8BF9; }
    .subtitle { font-size: 25px; color: #666; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# Sidebar - Navegação
st.sidebar.title("🧬 GA Portfolio")
st.sidebar.markdown("---")

# Opção "Home" adicionada para não carregar um projeto de cara
project = st.sidebar.selectbox(
    "Select the Challenge:",
    ["Welcome Page", "8-Queens Problem", "Knapsack Problem"]
)

st.sidebar.markdown("---")

# Lógica de Roteamento
if project == "Welcome Page":
    st.markdown('<p class="main-title">Genetic Algorithms Lab</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Bio-inspired computing for complex optimization</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### What are Genetic Algorithms?
        Genetic Algorithms (GAs) are search heuristics inspired by Charles Darwin’s theory of natural evolution. 
        They are used to find high-quality solutions to optimization and search problems by relying on biologically 
        inspired operators such as:

        * **Selection:** Choosing the fittest individuals to pass genes.
        * **Crossover:** Combining DNA from parents to create offspring.
        * **Mutation:** Introducing random changes to maintain diversity.

        ### 🚀 How to use this Lab
        Select a challenge in the **sidebar menu** to explore how GAs solve classic problems:
        1.  **8-Queens:** A constraint satisfaction problem.
        2.  **Knapsack:** A combinatorial optimization problem (Weight/Volume vs. Value).
        """)

    with col2:
        st.info(
            "💡 **Tip:** GAs are ideal for 'NP-Hard' problems where the search space is too vast for traditional methods.")

elif project == "8-Queens Problem":
    from queens.app import run_queens_app

    run_queens_app()

elif project == "Knapsack Problem":
    from knapsack.app import run_knapsack_app

    run_knapsack_app()