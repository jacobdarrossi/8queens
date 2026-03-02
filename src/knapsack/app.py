import streamlit as st
import pandas as pd
import time
from .engine import KnapsackPopulation, KnapsackIndividual



def run_knapsack_app():
    st.title("🎒 Knapsack Problem: Genetic Optimization")
    st.markdown("### Solving resource allocation with multiple constraints")

    st.info("""
        **Goal:** Maximize value without exceeding **125kg** and **125L**.
    """)

    # Criando o DataFrame de referência com os dados do seu Individuo.java
    items_reference = []
    for i in range(25):
        items_reference.append({
            "Product": KnapsackIndividual.PRODUCT_NAMES[i],
            "Volume (L)": KnapsackIndividual.BASE_VALUES[i][0],
            "Weight (kg)": KnapsackIndividual.BASE_VALUES[i][1],
            "Value ($)": KnapsackIndividual.BASE_VALUES[i][2]
        })
    df_ref = pd.DataFrame(items_reference)

    with st.expander("See all available products (Reference Table)"):
        st.table(df_ref)

    # --- Sidebar Control ---
    st.sidebar.header("Evolution Control")
    gen_count = st.sidebar.number_input("Generations", min_value=1, value=100, help="Number of evolutionary cycles.")
    pop_size = st.sidebar.number_input("Initial Population", min_value=10, value=50,
                                       help="Number of individuals at start.")
    selection_tax = st.sidebar.slider("Selection Rate (%)", 10, 95, 50, help="Percentage of best kept for breeding.")
    mutation_rate = st.sidebar.slider("Mutation Rate (%)", 0, 100, 20, help="Probability of genetic mutation.")
    mutation_bits = st.sidebar.number_input("Mutation Bits", min_value=1, value=1,
                                            help="Genes flipped during mutation.")

    # Limits
    WEIGHT_LIMIT = 125
    VOLUME_LIMIT = 125

    if st.button("Start Genetic Algorithm", type="primary", use_container_width=True):
        pop = KnapsackPopulation(pop_size, selection_tax, mutation_rate, mutation_bits)

        # --- CRIAÇÃO DOS PLACEHOLDERS (Fora do loop para evitar o bug) ---
        col_metrics, col_chart = st.columns([1, 2])

        with col_metrics:
            st.subheader("Current Metrics")
            metric_val = st.empty()
            metric_weight = st.empty()
            metric_vol = st.empty()

        with col_chart:
            st.subheader("Total Value Evolution")
            chart_placeholder = st.empty()

        progress_bar = st.progress(0)
        status_text = st.empty()

        fitness_history = []

        # --- LOOP DE EVOLUÇÃO ---
        for g in range(gen_count):
            pop.select_best()
            pop.breed_new_generation()

            best_ind = pop.get_best()
            fitness_history.append(best_ind.value)

            # ATUALIZAÇÃO DOS PLACEHOLDERS (Em vez de criar novos elementos)
            metric_val.metric("Best Value Found", f"${best_ind.value}")

            w_delta = best_ind.weight - WEIGHT_LIMIT
            metric_weight.metric(
                "Total Weight",
                f"{best_ind.weight} / {WEIGHT_LIMIT}",
                delta=f"{w_delta}" if w_delta > 0 else None,
                delta_color="inverse"
            )

            v_delta = best_ind.volume - VOLUME_LIMIT
            metric_vol.metric(
                "Total Volume",
                f"{best_ind.volume} / {VOLUME_LIMIT}",
                delta=f"{v_delta}" if v_delta > 0 else None,
                delta_color="inverse"
            )

            # Atualiza o gráfico no mesmo lugar
            chart_placeholder.line_chart(fitness_history)

            progress_bar.progress((g + 1) / gen_count)
            status_text.text(f"Generation {g + 1}/{gen_count}")

            time.sleep(0.01)

        # --- RESULTADOS FINAIS (Fora do loop) ---
        st.success("Optimization Complete!")
        best_ind = pop.get_best()

        results_data = []
        for i, gene in enumerate(best_ind.genes):
            if gene == 1:
                item_info = best_ind.BASE_VALUES[i]
                results_data.append({
                    "Product": best_ind.PRODUCT_NAMES[i],
                    "Volume (L)": item_info[0],
                    "Weight (kg)": item_info[1],
                    "Value ($)": item_info[2]
                })

        st.subheader("Final Inventory Selection")
        st.table(pd.DataFrame(results_data))
        st.info(
            f"**Final Summary:** Total Value: ${best_ind.value} | Weight: {best_ind.weight}kg | Volume: {best_ind.volume}L")