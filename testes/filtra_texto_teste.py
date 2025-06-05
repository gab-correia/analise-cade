import re

def preprocessar_texto_legal(texto):
    # Compilar regex uma vez para performance
    padroes = {
        'secoes_relevantes': re.compile(
            r'(REPRESENTADOS?\(?AS?\)?:|DISPOSITIVO|CONCLUSÕES|MULTA|CONDENAÇÃO|MOTIVO DA MULTA)',
            re.IGNORECASE
        ),
        'elementos_remocao': re.compile(
            r'\[ACESSO RESTRITO\]|SEI \d+/\d+|Timbre|Processo Admin.*?\d{4}-\d{2}|'
            r'©.*?$|\b(?:Art\.|Lei|Parágrafo único)\b.*?\.',
            re.IGNORECASE
        ),
        'limpeza_basica': re.compile(
            r'http\S+|www\S+|[\d.,]+%|\d{2}/\d{2}/\d{4}|'
            r'[^\w\sáàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]',
            re.IGNORECASE
        )
    }

    # Filtragem estratégica por seções
    linhas_filtradas = []
    secao_relevante = False

    for linha in texto.split('\n'):
        # Remover elementos indesejados
        linha = padroes['elementos_remocao'].sub('', linha).strip()
        
        # Identificar seções-chave
        if padroes['secoes_relevantes'].search(linha):
            secao_relevante = True
            linhas_filtradas.append('\n' + linha.upper() + '\n' + '-'*50)
        elif secao_relevante and linha.strip() == '':
            secao_relevante = False
        elif secao_relevante:
            # Limpeza básica mantendo estrutura
            linha_limpa = padroes['limpeza_basica'].sub(' ', linha)
            linha_limpa = re.sub(r'\s+', ' ', linha_limpa).strip()
            if linha_limpa:
                linhas_filtradas.append(linha_limpa)

    # Pós-processamento estratégico
    texto_preprocessado = '\n'.join(linhas_filtradas)
    
    # Normalização final
    texto_preprocessado = re.sub(
        r'\b(?:R\$\s*)?\d{1,3}(?:\.\d{3})*(?:,\d{2})|\d+%',
        '[VALOR]', texto_preprocessado
    )
    
    return texto_preprocessado[:6000]  # Limite seguro para LLMs


# Uso com o arquivo do processo
with open('texto_teste.txt', 'r', encoding='utf-8') as arquivo:
    texto_processo = arquivo.read()

resultado = preprocessar_texto_legal(texto_processo)

print(resultado)
