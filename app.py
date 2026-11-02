from algorithms import brute_force
import matplotlib.pyplot as plt
import random
import streamlit as st

st.set_page_config(page_title="Closest Pair of Points", layout="wide")

if "points" not in st.session_state:
    st.session_state.points = []

if "steps" not in st.session_state:
    st.session_state.steps = []

st.sidebar.title("Controles")

if st.sidebar.button("Gerar Pontos Aleatórios", use_container_width=True):
    st.session_state.points = [
        {"x": random.uniform(10, 90), "y": random.uniform(10, 90)}
        for _ in range(20)
    ]
    st.session_state.steps = []

if st.sidebar.button("Limpar Canvas", use_container_width=True):
    st.session_state.points = []
    st.session_state.steps = []

st.sidebar.subheader("Inserir Ponto Manualmente")
col1, col2 = st.sidebar.columns(2)
x_val = col1.number_input("X", min_value=0.0, max_value=100.0, value=50.0)
y_val = col2.number_input("Y", min_value=0.0, max_value=100.0, value=50.0)

if st.sidebar.button("Adicionar Ponto", use_container_width=True):
    st.session_state.points.append({"x": x_val, "y": y_val})
    st.session_state.steps = []

st.sidebar.divider()

if st.sidebar.button("Executar força bruta", use_container_width=True):
    if len(st.session_state.points) < 2:
        st.session_state.steps = []
        st.sidebar.warning("Adicione pelo menos dois pontos.")
    else:
        st.session_state.steps = brute_force(st.session_state.points)

st.title("Visualizador: Par de Pontos Mais Próximos")
st.write(
    "Utilize a barra lateral para adicionar pontos, gerar pontos aleatórios "
    "e executar o algoritmo de força bruta."
)


def draw_points(points, steps):
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

    # Destaca o par mais próximo quando o algoritmo já foi executado.
    done_step = next(
        (step for step in reversed(steps) if step.get("type") == "done"),
        None,
    )
    if done_step and done_step.get("best"):
        p1, p2 = done_step["best"]
        ax.plot(
            [p1["x"], p2["x"]],
            [p1["y"], p2["y"]],
            marker="o",
            linewidth=2,
            label="Par mais próximo",
        )
        ax.legend()

    return fig


st.pyplot(draw_points(st.session_state.points, st.session_state.steps))

if st.session_state.steps:
    done_step = next(
        (step for step in reversed(st.session_state.steps) if step.get("type") == "done"),
        None,
    )

    if done_step:
        st.subheader("Resultado")
        if done_step.get("best"):
            p1, p2 = done_step["best"]
            st.write(f"**Ponto 1:** ({p1['x']:.2f}, {p1['y']:.2f})")
            st.write(f"**Ponto 2:** ({p2['x']:.2f}, {p2['y']:.2f})")
            st.metric("Distância mínima", f"{done_step['dist']:.4f}")
        else:
            st.info("Não foi possível encontrar um par de pontos.")

        comparisons = sum(
            1 for step in st.session_state.steps if step.get("type") == "compare"
        )
        st.write(f"Quantidade de pares comparados: **{comparisons}**")

        with st.expander("Ver etapas registradas pelo algoritmo"):
            for index, step in enumerate(st.session_state.steps, start=1):
                if step["type"] == "compare":
                    p1, p2 = step["p1"], step["p2"]
                    st.write(
                        f"{index}. Comparação: ({p1['x']:.2f}, {p1['y']:.2f}) "
                        f"com ({p2['x']:.2f}, {p2['y']:.2f})"
                    )
                elif step["type"] == "update":
                    st.write(
                        f"{index}. Nova menor distância encontrada: "
                        f"{step['dist']:.4f}"
                    )
                elif step["type"] == "done":
                    st.write(f"{index}. Algoritmo finalizado.")
