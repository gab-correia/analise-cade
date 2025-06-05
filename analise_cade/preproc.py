"""Rotinas de carregamento e pré-processamento dos documentos do CADE."""

from pathlib import Path

import pandas as pd


def carregar_dados(caminho: str) -> pd.DataFrame:
    """Lê o arquivo de entrada em CSV ou Excel.

    Parameters
    ----------
    caminho : str
        Caminho para o arquivo a ser lido.

    Returns
    -------
    pandas.DataFrame
        Dados brutos carregados.
    """

    # LINHA DE SELECAO DO INPUT
    caminho_arquivo = Path(caminho)
    if caminho_arquivo.suffix.lower() == ".csv":
        dados = pd.read_csv(caminho_arquivo, encoding="utf-8", low_memory=False)
    else:
        dados = pd.read_excel(caminho_arquivo)
    return dados


def filtrar_votos(dados: pd.DataFrame) -> pd.DataFrame:
    """Aplica os filtros básicos para obter apenas votos em processos
    administrativos."""

    tipos_validos = {
        "Voto",
        "Voto Processo Administrativo",
        "Voto Embargos de Declaração",
    }

    mascara = (
        dados["descricao_tipo_documento"].isin(tipos_validos)
        & (dados["descricao_tipo_processo"] == "Processo Administrativo")
    )

    return dados.loc[mascara].reset_index(drop=True)


def limpar_colunas(dados: pd.DataFrame) -> pd.DataFrame:
    """Remove colunas desnecessárias conforme o notebook inicial."""

    colunas_para_remover = [
        "id_colecao",
        "id_unique",
        "_version_",
        "clicks",
        "soundex",
        "vltfidf",
        "qtd_acesso",
        "documentos_citados",
        "tags",
        "numero_acordao",
        "numero_ata",
        "nucluster",
        "score",
        "sumario",
        "colecao",
        "palavras",
        "qtd_acesso_processo",
    ]

    colunas_existentes = [c for c in colunas_para_remover if c in dados.columns]
    return dados.drop(columns=colunas_existentes)


def selecionar_colunas(dados: pd.DataFrame) -> pd.DataFrame:
    """Mantém apenas o subconjunto de colunas úteis."""

    colunas_manter = [
        "id",
        "ano_documento",
        "assinaturas",
        "descricao_tipo_documento",
        "decisao_tribunal",
        "decisao_sg",
        "setor_economico",
        "id_unidade",
        "data_ordem",
        "data_processo",
        "data_documento",
        "mercado_relevante",
        "descricao_especificacao",
        "conteudo",
    ]

    return dados[colunas_manter].copy()
