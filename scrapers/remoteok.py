"""
Scraper do RemoteOK (remoteok.com).

Usa a API pública em JSON (https://remoteok.com/api), que é bem mais
estável que raspar HTML — não deve quebrar com facilidade. A maioria das
vagas lá é remoto "mundial" ou restrito a outros países; o matcher.py
descarta automaticamente qualquer uma que não pareça aberta pro Brasil,
então é normal esse scraper trazer poucas notificações — é bônus, não
substituto do LinkedIn/BNE.
"""
import json
from scrapers.http_utils import fetch, save_debug_html

API_URL = "https://remoteok.com/api"

TAGS_RELEVANTES = ["security", "cyber", "cybersecurity", "infosec"]
TITLE_KEYWORDS = ["security", "cyber", "soc", "segurança"]


def scrape(debug: bool = False) -> list[dict]:
    html = fetch(API_URL, extra_headers={"Accept": "application/json"})
    if not html:
        return []
    if debug:
        save_debug_html("remoteok", html)

    try:
        data = json.loads(html)
    except json.JSONDecodeError:
        return []

    jobs = []
    for item in data:
        if not isinstance(item, dict) or "position" not in item:
            continue  # o primeiro item da lista é um aviso legal, não vaga

        title = item.get("position", "")
        tags = [t.lower() for t in item.get("tags", [])]
        title_lower = title.lower()

        bate_tag = any(t in tags for t in TAGS_RELEVANTES)
        bate_titulo = any(k in title_lower for k in TITLE_KEYWORDS)
        if not (bate_tag or bate_titulo):
            continue

        url = item.get("url", "") or f"https://remoteok.com/remote-jobs/{item.get('id', '')}"
        location = item.get("location", "") or "Worldwide"

        jobs.append({
            "title": title,
            "url": url,
            "location": location,
            "company": item.get("company", ""),
            "source": "RemoteOK",
            "modality": "remoto",
        })

    return jobs
