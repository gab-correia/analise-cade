"""Main entrypoint for CADE analysis."""
from pathlib import Path
import pandas as pd
from analise_cade import preproc, llm_extraction, analysis


def main(input_path: str) -> None:
    df = preproc.load_data(input_path)
    df = preproc.filter_votes(df)

    # Placeholder for LLM processing
    df['condenacao'] = False  # TODO: replace with real extraction
    df['valor_multa_reais'] = pd.NA
    df['percentual_faturamento'] = pd.NA
    df['setor_economico'] = pd.NA

    output_dir = Path('output')
    output_dir.mkdir(exist_ok=True)

    df.to_excel(output_dir / 'output.xlsx', index=False)
    kpis = analysis.compute_kpis(df)
    kpis.to_csv(output_dir / 'relatorio.csv', index=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process CADE data')
    parser.add_argument('input', help='path to CSV or Excel file')
    args = parser.parse_args()
    main(args.input)
