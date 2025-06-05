"""Dashboard interativo em Streamlit."""

import pandas as pd
import streamlit as st


def executar_dashboard(dados: pd.DataFrame) -> None:
    """Exibe gráficos básicos para exploração dos resultados."""

    st.title("Análise de Processos do CADE")

    setores = sorted(dados["setor_economico"].dropna().unique())
    setor_sel = st.sidebar.multiselect("Setor econômico", setores, default=setores)

    df = dados[dados["setor_economico"].isin(setor_sel)]

    st.metric('Quantidade de casos', len(df))
    st.metric('% com condenação', f"{df['condenacao'].mean()*100:.1f}%")

    st.bar_chart(df['valor_multa_reais'])
