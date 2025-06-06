
se eu quiser usar 

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configura o Gemini
genai.configure(api_key=API_KEY)
modelo = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config={"temperature": 0.1}  
)

para preencher valores dessas variaveis:
decisao_tribunal, seguiu_nota_tecnica, tipo_infracao_concorrencial, multa, tipo_de_multa, valor_multa_reais

com base em um texto recebido, qual o melhor jeito de fazer ?