"""Streamlit dashboard for exploration."""
import streamlit as st
import pandas as pd


def run_dashboard(data: pd.DataFrame) -> None:
    st.title('Análise de Processos do CADE')

    setores = sorted(data['setor_economico'].dropna().unique())
    setor_sel = st.sidebar.multiselect('Setor econômico', setores, default=setores)

    df = data[data['setor_economico'].isin(setor_sel)]

    st.metric('Quantidade de casos', len(df))
    st.metric('% com condenação', f"{df['condenacao'].mean()*100:.1f}%")

    st.bar_chart(df['valor_multa_reais'])
