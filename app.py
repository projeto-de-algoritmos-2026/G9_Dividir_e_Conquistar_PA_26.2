import matplotlib.pyplot as plt
import streamlit as st
import random

st.set_page_config(page_title="Closest Pair of Points", layout="wide")

if 'points' not in st.session_state:
    st.session_state.points = []

st.sidebar.title("Controles")

if st.sidebar.button("Gerar Pontos Aleatórios", use_container_width=True):
    st.session_state.points = [{'x': random.uniform(10, 90), 'y': random.uniform(10, 90)} for _ in range(20)]

if st.sidebar.button("Limpar Canvas", use_container_width=True):
    st.session_state.points = []

st.sidebar.subheader("Inserir Ponto Manualmente")
col1, col2 = st.sidebar.columns(2)
x_val = col1.number_input("X", min_value=0.0, max_value=100.0, value=50.0)
y_val = col2.number_input("Y", min_value=0.0, max_value=100.0, value=50.0)
if st.sidebar.button("Adicionar Ponto"):
    st.session_state.points.append({'x': x_val, 'y': y_val})

st.title("Visualizador: Par de Pontos Mais Próximos")
st.write("Utilize a barra lateral para adicionar pontos e executar os algoritmos.")

plot_placeholder = st.empty()

def draw_static_points(points):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    if points:
        xs = [p['x'] for p in points]
        ys = [p['y'] for p in points]
        ax.scatter(xs, ys, c='black')
    return fig

fig = draw_static_points(st.session_state.points)
plot_placeholder.pyplot(fig)