from algorithms import brute_force
import matplotlib.pyplot as plt
import streamlit as st
import random
import time

st.set_page_config(page_title="Closest Pair of Points", layout="wide")

if "points" not in st.session_state:
    st.session_state.points = []

st.sidebar.title("Controlos")

if st.sidebar.button("Gerar Pontos Aleatórios", use_container_width=True):
    st.session_state.points = [
        {"x": random.uniform(10, 90), "y": random.uniform(10, 90)}
        for _ in range(20)
    ]

if st.sidebar.button("Limpar Canvas", use_container_width=True):
    st.session_state.points = []

st.sidebar.subheader("Inserir Ponto Manualmente")
col1, col2 = st.sidebar.columns(2)
x_val = col1.number_input("X", min_value=0.0, max_value=100.0, value=50.0)
y_val = col2.number_input("Y", min_value=0.0, max_value=100.0, value=50.0)

if st.sidebar.button("Adicionar Ponto", use_container_width=True):
    st.session_state.points.append({"x": x_val, "y": y_val})

st.sidebar.divider()

st.title("Visualizador: Par de Pontos Mais Próximos")
st.write(
    "Utilize a barra lateral para adicionar pontos, gerar pontos aleatórios "
    "e executar o algoritmo de força bruta com animação passo-a-passo."
)

plot_placeholder = st.empty()
info_placeholder = st.empty()

def draw_state(points, compare=None, best=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.25)

    if points:
        xs = [p["x"] for p in points]
        ys = [p["y"] for p in points]
        ax.scatter(xs, ys, c="black", label="Pontos")

    if compare:
        ax.plot(
            [compare[0]["x"], compare[1]["x"]],
            [compare[0]["y"], compare[1]["y"]],
            c="blue",
            alpha=0.5,
            label="A comparar",
        )

    if best:
        ax.plot(
            [best[0]["x"], best[1]["x"]],
            [best[0]["y"], best[1]["y"]],
            c="red",
            linewidth=2,
            label="Par mais próximo (atual)",
        )

    if compare or best:
        ax.legend()

    return fig

fig_initial = draw_state(st.session_state.points)
plot_placeholder.pyplot(fig_initial)
plt.close(fig_initial)

if st.sidebar.button("Executar Força Bruta O(n²)", type="primary", use_container_width=True):
    if len(st.session_state.points) < 2:
        st.sidebar.warning("Adicione pelo menos dois pontos.")
    else:
        steps = brute_force(st.session_state.points)
        best_pair = None
        comparisons = 0
        
        info_placeholder.info("A executar algoritmo...")

        for step in steps:
            if step["type"] == "compare":
                comparisons += 1
                fig = draw_state(st.session_state.points, compare=(step["p1"], step["p2"]), best=best_pair)
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.05)
            elif step["type"] == "update":
                best_pair = (step["p1"], step["p2"])
            elif step["type"] == "done":
                fig = draw_state(st.session_state.points, best=step["best"])
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                
                info_placeholder.success(
                    f"**Concluído!** Distância mínima: {step['dist']:.4f} | "
                    f"Total de comparações: {comparisons}"
                )