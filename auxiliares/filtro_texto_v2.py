import re
from langchain.text_splitter import TokenTextSplitter

def preprocessar_e_chunk(texto, max_caracteres=8000):
    # 1. Filtragem Estratégica
    secoes_relevantes = re.compile(
        r'(?i)(REPRESENTADOS?\(?AS?\)?:|DISPOSITIVO|CONCLUSÕES|MULTA|CONDENAÇÃO|MOTIVO DA MULTA)'
    )
    elementos_remocao = re.compile(
        r'\[ACESSO RESTRITO\]|SEI \d+/\d+|Timbre|©.*?$|\bArt\. \d+'
    )

    # 2. Processamento por Linha
    linhas_filtradas = []
    secao_ativa = False
    
    for linha in texto.split('\n'):
        linha_limpa = elementos_remocao.sub('', linha).strip()
        if secoes_relevantes.search(linha_limpa):
            secao_ativa = True
            linhas_filtradas.append(f"\n{linha_limpa.upper()}\n{'-'*50}")
        elif secao_ativa and linha_limpa:
            linhas_filtradas.append(linha_limpa)
    
    texto_filtrado = '\n'.join(linhas_filtradas)
    
    # 3. Chunking por Caracteres (1 token ≈ 4 caracteres no Gemini)
    chunks = []
    start = 0
    while start < len(texto_filtrado):
        end = start + max_caracteres
        chunk = texto_filtrado[start:end]
        chunks.append(chunk)
        start = end - 200  # Overlap de 200 caracteres (50 tokens)

    return chunks


# Uso com o arquivo do processo
with open('texto_teste.txt', 'r', encoding='utf-8') as arquivo:
    texto_processo = arquivo.read()

resultado = preprocessar_e_chunk(texto_processo)

print(resultado)
