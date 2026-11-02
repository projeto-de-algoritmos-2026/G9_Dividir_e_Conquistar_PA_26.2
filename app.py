from algorithms import brute_force, divide_and_conquer
import matplotlib.pyplot as plt
import streamlit as st
import random
import time
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Closest Pair of Points", layout="wide")

if "random_points" not in st.session_state:
    st.session_state.random_points = []

if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = "canvas_0"


if st.sidebar.button("Gerar Pontos Aleatórios", use_container_width=True):
    st.session_state.random_points = [
        {"x": random.uniform(5, 95), "y": random.uniform(5, 95)}
        for _ in range(20)
    ]
    st.rerun()

if st.sidebar.button("Limpar Canvas", use_container_width=True):
    st.session_state.random_points = []
    st.session_state.canvas_key = f"canvas_{time.time()}" 
    st.rerun()

st.sidebar.divider()

st.title("Visualizador: Par de Pontos Mais Próximos")
st.write("Clique no quadro branco abaixo para adicionar pontos ou gere pontos aleatoriamente na barra lateral.")

canvas_result = st_canvas(
    fill_color="black",
    stroke_width=6,
    stroke_color="black",
    background_color="white",
    height=400,
    width=800,
    drawing_mode="point",
    key=st.session_state.canvas_key,
)

all_points = list(st.session_state.random_points)
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data["objects"]:
        x = (obj['left'] / 800.0) * 100.0
        y = 100.0 - ((obj['top'] / 400.0) * 100.0)
        all_points.append({'x': x, 'y': y})

plot_placeholder = st.empty()
info_placeholder = st.empty()

def draw_state(points, compare=None, best=None, line_x=None):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, alpha=0.25)

    if points:
        xs = [p["x"] for p in points]
        ys = [p["y"] for p in points]
        ax.scatter(xs, ys, c="black", label="Pontos")

    if line_x is not None:
        ax.axvline(x=line_x, color="gray", linestyle="--", alpha=0.5, label="Divisão (D&C)")

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
            label="Par mais próximo",
        )

    if compare or best or line_x is not None:
        ax.legend(loc="upper right")

    return fig

# Renderização inicial estática para mostrar os pontos antes da animação
fig_initial = draw_state(all_points)
plot_placeholder.pyplot(fig_initial)
plt.close(fig_initial)

if st.sidebar.button("Executar Força Bruta O(n²)", type="secondary", use_container_width=True):
    if len(all_points) < 2:
        st.sidebar.warning("Adicione pelo menos dois pontos.")
    else:
        steps = brute_force(all_points)
        best_pair = None
        comparisons = 0
        info_placeholder.info("A executar Força Bruta...")

        for step in steps:
            if step["type"] == "compare":
                comparisons += 1
                fig = draw_state(all_points, compare=(step["p1"], step["p2"]), best=best_pair)
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.05)
            elif step["type"] == "update":
                best_pair = (step["p1"], step["p2"])
            elif step["type"] == "done":
                fig = draw_state(all_points, best=step["best"])
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                info_placeholder.success(f"**Força Bruta Concluída!** Distância: {step['dist']:.4f} | Comparações: {comparisons}")

if st.sidebar.button("Executar Dividir e Conquistar O(n log n)", type="primary", use_container_width=True):
    if len(all_points) < 2:
        st.sidebar.warning("Adicione pelo menos dois pontos.")
    else:
        steps = divide_and_conquer(all_points)
        best_pair = None
        current_line = None
        comparisons = 0
        info_placeholder.info("A executar Dividir e Conquistar...")

        for step in steps:
            if step["type"] == "line":
                current_line = step["x"]
                fig = draw_state(all_points, best=best_pair, line_x=current_line)
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.2)
            elif step["type"] == "compare":
                comparisons += 1
                fig = draw_state(all_points, compare=(step["p1"], step["p2"]), best=best_pair, line_x=current_line)
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                time.sleep(0.05)
            elif step["type"] == "update":
                best_pair = (step["p1"], step["p2"])
            elif step["type"] == "done":
                fig = draw_state(all_points, best=step["best"])
                plot_placeholder.pyplot(fig)
                plt.close(fig)
                info_placeholder.success(f"**D&C Concluído!** Distância: {step['dist']:.4f} | Comparações: {comparisons}")