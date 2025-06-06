# cade_dashboard.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# -------------------------------------------------------------------
# 1. Simulate a CADE-style legal dataset
# -------------------------------------------------------------------
np.random.seed(42)
N_ROWS = 400

sectors = ["Agro-industry", "Energy", "Technology", "Pharma", "Finance", "Logistics"]
decisions = ["Condenação", "Arquivamento", "Acordo"]
infr_types = ["Cartel", "Abuso de posição dominante", "Ato de Concentração", "Conduta Unilateral"]

# helper for votes
def make_votes():
    conselheiros = np.random.randint(4, 7)
    favor = np.random.randint(0, conselheiros + 1)
    contra = conselheiros - favor
    return conselheiros, favor, contra

records = []
for pid in range(1, N_ROWS + 1):
    cons, fav, con = make_votes()
    note_followed = np.random.rand() < 0.6  # 60 % chance of following nota técnica
    decision_idx = np.random.choice([0, 1, 2], p=[0.5, 0.35, 0.15])
    records.append({
        "process_id": pid,
        "decision_date": datetime(2022, 1, 1) + pd.Timedelta(days=np.random.randint(0, 365*3)),
        "sector": np.random.choice(sectors),
        "tipo_infracao": np.random.choice(infr_types),
        "decision": decisions[decision_idx],
        "fine_value_reais": np.random.gamma(2.5, 1_200_000) if decision_idx == 0 else 0,
        "percent_revenue": np.round(np.random.uniform(0.3, 8.0), 2) if decision_idx == 0 else 0,
        "seguiu_nota_tecnica": note_followed,
        "num_conselheiros": cons,
        "votos_favoraveis": fav,
        "votos_contrarios": con,
    })

df = pd.DataFrame(records)

# -------------------------------------------------------------------
# 2. Sidebar – legal filters
# -------------------------------------------------------------------
st.sidebar.header("⚖️ Filtros Jurídicos")

sector_sel = st.sidebar.multiselect("Setor econômico", options=sectors, default=sectors)
infraction_sel = st.sidebar.multiselect("Tipo de infração", options=infr_types, default=infr_types)
decision_sel = st.sidebar.multiselect("Tipo de decisão", options=decisions, default=decisions)

nota_opt = st.sidebar.selectbox(
    "Seguiu Nota Técnica?",
    options=["Indiferente", "Sim", "Não"],
    index=0
)

date_min, date_max = st.sidebar.date_input(
    "Intervalo de datas",
    value=(df["decision_date"].min(), df["decision_date"].max()),
    min_value=df["decision_date"].min(),
    max_value=df["decision_date"].max()
)

# Apply filters
mask = (
    df["sector"].isin(sector_sel)
    & df["tipo_infracao"].isin(infraction_sel)
    & df["decision"].isin(decision_sel)
    & df["decision_date"].between(pd.to_datetime(date_min), pd.to_datetime(date_max))
)
if nota_opt != "Indiferente":
    mask &= df["seguiu_nota_tecnica"] == (nota_opt == "Sim")

filtered_df = df[mask]

# -------------------------------------------------------------------
# 3. KPIs específicos
# -------------------------------------------------------------------
st.title("📊 CADE – Painel Jurídico Interativo (dados simulados)")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Casos filtrados", f"{len(filtered_df):,}")
conden = filtered_df["decision"].eq("Condenação").sum()
col2.metric("Taxa de condenação", f"{conden/len(filtered_df)*100 if len(filtered_df) else 0:.1f}%")
nota_pct = filtered_df["seguiu_nota_tecnica"].mean() * 100 if len(filtered_df) else 0
col3.metric("Seguiu Nota Técnica", f"{nota_pct:.1f}%")
col4.metric("Multas totais (R$)", f"R$ {filtered_df['fine_value_reais'].sum():,.0f}")

st.divider()

# -------------------------------------------------------------------
# 4A. Distribuição de decisões por tipo de infração
# -------------------------------------------------------------------
st.subheader("Distribuição de decisões por tipo de infração")
decisions_by_inf = (
    filtered_df.groupby(["tipo_infracao", "decision"])
    .size()
    .reset_index(name="count")
)
fig1 = px.bar(
    decisions_by_inf,
    x="tipo_infracao",
    y="count",
    color="decision",
    barmode="group",
    labels={"tipo_infracao": "Tipo de Infração", "count": "Número de casos", "decision": "Decisão"}
)
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------------------------------------------
# 4B. Multas (R$) por setor
# -------------------------------------------------------------------
st.subheader("Multas aplicadas por setor")
fines_sector = (
    filtered_df.groupby("sector")["fine_value_reais"]
    .sum()
    .reset_index()
    .sort_values("fine_value_reais", ascending=False)
)
fig2 = px.bar(
    fines_sector, x="sector", y="fine_value_reais",
    labels={"sector": "Setor", "fine_value_reais": "Multas Totais (R$)"},
    text_auto=".2s"
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------------------------
# 4C. Boxplot de multas por decisão
# -------------------------------------------------------------------
st.subheader("Distribuição das multas por tipo de decisão")
if filtered_df["fine_value_reais"].gt(0).any():
    fig3 = px.box(
        filtered_df[filtered_df["fine_value_reais"] > 0],
        x="decision", y="fine_value_reais",
        labels={"decision": "Decisão", "fine_value_reais": "Multa (R$)"}
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.info("Nenhuma multa nos dados filtrados.")

# -------------------------------------------------------------------
# 4D. Dispersão de votos
# -------------------------------------------------------------------
st.subheader("Votos favoráveis vs. contrários")
fig4 = px.scatter(
    filtered_df,
    x="votos_favoraveis",
    y="votos_contrarios",
    color="decision",
    size="fine_value_reais",
    hover_data=["process_id", "tipo_infracao"],
    labels={"votos_favoraveis": "Votos Favoráveis", "votos_contrarios": "Votos Contrários"},
)
st.plotly_chart(fig4, use_container_width=True)

# -------------------------------------------------------------------
# 5. Dados brutos
# -------------------------------------------------------------------
with st.expander("🔍 Ver dados brutos"):
    st.dataframe(filtered_df.sort_values("decision_date").reset_index(drop=True))
