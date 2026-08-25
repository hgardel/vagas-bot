"""
Configurações do bot de vagas.
Edite as listas abaixo pra ajustar o que ele procura.
"""
import os
from dotenv import load_dotenv
load_dotenv()

# --- Palavras-chave POSITIVAS (título da vaga precisa bater em pelo menos 1) ---
KEYWORDS_CYBER_PT = [
    "analista de segurança",
    "analista de cibersegurança",
    "analista de segurança da informação",
    "segurança da informação",
    "analista soc",
    "analista de ti",
]

KEYWORDS_CYBER_EN = [
    "cybersecurity analyst",
    "security analyst",
    "information security analyst",
    "soc analyst",
    "cyber security analyst",
    "it security analyst",
    "junior cybersecurity",
]

ALL_CYBER_KEYWORDS = KEYWORDS_CYBER_PT + KEYWORDS_CYBER_EN

# Termos de ADS (só valem pra vaga presencial em PG)
KEYWORDS_ADS = [
    "desenvolvedor jr",
    "desenvolvedor junior",
    "programador jr",
    "programador junior",
    "analista de sistemas jr",
    "suporte de ti",
    "suporte tecnico",
    "estagio de ti",
    "estagiario de ti",
]

# --- Termos NEGATIVOS (se aparecer no título, descarta) ---
EXCLUDE_KEYWORDS = [
    "senior", "sênior", "sr.", "sr ", "sr",
    "pleno", "lead", "especialista", "mid-level", "mid level", "midlevel",
    "coordenador", "gerente", "gestor", "head",
    # área de segurança do trabalho/ocupacional é confundida com
    # segurança da informação por causa da palavra "segurança" sozinha
    "seguranca do trabalho", "segurança do trabalho",
    "tecnico de seguranca do trabalho", "técnico de segurança do trabalho",
    "engenheiro de seguranca do trabalho", "engenheiro de segurança do trabalho",
    "safety analyst", "safety officer", "occupational safety",
    "seguranca patrimonial", "segurança patrimonial",
    "vigilante", "porteiro",
]

# --- Regras de localização e prioridade ---
CIDADE_BASE_PRESENCIAL = "ponta grossa"
CIDADES_REMOTO_PRIORITARIAS = ["curitiba"]  # mantido por compatibilidade

# Estados vizinhos do Paraná, usados na camada 5 de prioridade
UF_ESTADOS_VIZINHOS = ["sc", "sp", "rs"]

# --- Telegram ---
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# --- Idade máxima da vaga (em dias) ---
MAX_JOB_AGE_DAYS = 14

# --- Arquivo de controle de vagas já vistas ---
SEEN_JOBS_FILE = "seen_jobs.json"

# --- User-Agent pra requests ---
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}
