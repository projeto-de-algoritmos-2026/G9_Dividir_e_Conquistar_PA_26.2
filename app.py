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

st.title("Visualizador: Par de Pontos Mais Próximos")
st.write("Utilize a barra lateral para adicionar pontos e executar os algoritmos.")