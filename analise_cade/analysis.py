"""Statistical analysis utilities."""
import pandas as pd


def compute_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """Compute required KPIs for the relatorio.csv output."""
    total = len(df)
    condenados = df['condenacao'].sum()
    pct_condenacao = condenados / total * 100 if total else 0

    media_multa_reais = df['valor_multa_reais'].mean()
    media_pct_faturamento = df['percentual_faturamento'].mean()

    return pd.DataFrame({
        'Metrica': [
            'Porcentagem de votos condenatorios (%)',
            'Multa media (R$)',
            'Percentual medio do faturamento (%)',
        ],
        'Valor': [
            pct_condenacao,
            media_multa_reais,
            media_pct_faturamento,
        ],
    })
