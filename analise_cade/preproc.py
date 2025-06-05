"""Data loading and preprocessing utilities for CADE documents."""
import pandas as pd
from pathlib import Path

# LINHA DE SELECAO DO INPUT
def load_data(filepath: str) -> pd.DataFrame:
    """Load raw CADE CSV or Excel file."""
    path = Path(filepath)
    if path.suffix.lower() == '.csv':
        df = pd.read_csv(path, encoding='utf-8')
    else:
        df = pd.read_excel(path)
    return df

def filter_votes(df: pd.DataFrame) -> pd.DataFrame:
    """Filter DataFrame for relevant vote documents."""
    tipos_validos = {
        'Voto',
        'Voto Processo Administrativo',
        'Voto Embargos de Declaração',
    }
    mask = df['descricao_tipo_documento'].isin(tipos_validos)
    return df.loc[mask].reset_index(drop=True)
