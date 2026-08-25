import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(text: str) -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[AVISO] TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não configurados. Pulando envio.")
        print(text)
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, data=payload, timeout=15)
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem no Telegram: {e}")
        return False

def format_job_message(job: dict, motivo: str) -> str:
    prioridade_labels = {
        "prioridade_1_presencial_pg": "🥇 PRESENCIAL EM PG",
        "prioridade_2_hibrido_pg": "🥈 HÍBRIDO EM PG",
        "prioridade_3_remoto_pg": "🥉 HOME OFFICE (Ponta Grossa)",
        "prioridade_4_remoto_curitiba": "4️⃣ HOME OFFICE (Curitiba)",
        "prioridade_5_remoto_brasil": "5️⃣ HOME OFFICE (resto do Brasil)",
        "modalidade_desconhecida": "❓ CONFIRA O LOCAL NO LINK ABAIXO:",
    }
    label = prioridade_labels.get(motivo, "")
    return (
        f"{label}\n"
        f"💼<b>{job['title']}</b>\n"
        f"🏢 {job.get('company', 'N/A')}\n"
        f"📍 {job.get('location', 'N/A')}\n"
        f"🌐 fonte: {job.get('source', 'N/A')}\n"
        f"🔗 {job['url']}"
    )