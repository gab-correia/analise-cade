"""Utilidades de análise estatística."""

import pandas as pd


def calcular_kpis(dados: pd.DataFrame) -> pd.DataFrame:
    """Gera os indicadores solicitados para o ``relatorio.csv``."""

    total = len(dados)
    qtd_condenados = dados["condenacao"].sum()
    percentual_condenacao = (qtd_condenados / total * 100) if total else 0

    media_multa_reais = dados["valor_multa_reais"].mean()
    media_percentual = dados["percentual_faturamento"].mean()

    return pd.DataFrame(
        {
            "Metrica": [
                "Porcentagem de votos condenatórios (%)",
                "Multa média (R$)",
                "Percentual médio do faturamento (%)",
            ],
            "Valor": [
                percentual_condenacao,
                media_multa_reais,
                media_percentual,
            ],
        }
    )
