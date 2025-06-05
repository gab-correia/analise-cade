"""Ponto de entrada principal para a análise do CADE."""

from pathlib import Path

import pandas as pd

from analise_cade import analysis, llm_extraction, preproc


def main(caminho_entrada: str) -> None:
    """Executa todas as etapas do pipeline."""

    dados = preproc.carregar_dados(caminho_entrada)
    dados = preproc.filtrar_votos(dados)
    dados = preproc.limpar_colunas(dados)
    dados = preproc.selecionar_colunas(dados)

    # Placeholder para processamento via LLM
    dados["condenacao"] = False  # TODO substituir pela extração real
    dados["valor_multa_reais"] = pd.NA
    dados["percentual_faturamento"] = pd.NA

    pasta_saida = Path("output")
    pasta_saida.mkdir(exist_ok=True)

    dados.to_excel(pasta_saida / "output.xlsx", index=False)
    kpis = analysis.calcular_kpis(dados)
    kpis.to_csv(pasta_saida / "relatorio.csv", index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Processa dados do CADE")
    parser.add_argument("input", help="caminho para arquivo CSV ou Excel")
    args = parser.parse_args()
    main(args.input)
