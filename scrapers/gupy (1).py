from scrapers.http_utils import fetch, save_debug_html
from config import GUPY_SEARCH_TERMS
import json

BASE_URL = "https://portal.gupy.io/api/job-search/jobs"
RESULTS_PER_PAGE = 12

# tipos de vaga que a Gupy retorna e que NÃO interessam (vem junto quando o
# termo bate na descrição, não no cargo em si)
TIPOS_IGNORADOS = {"vacancy_type_lecturer"}  # vaga de professor/docente


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in GUPY_SEARCH_TERMS:
        jobs += _scrape_all_pages(term, debug)

    unique = {j["url"]: j for j in jobs if j.get("url")}
    return list(unique.values())


def _scrape_all_pages(term: str, debug: bool) -> list[dict]:
    all_jobs = []
    offset = 0

    while True:
        raw = fetch(BASE_URL, params={
            "jobName": term,
            "limit": RESULTS_PER_PAGE,
            "offset": offset,
        })

        if not raw:
            print(f"  [AVISO] Gupy não respondeu pra '{term}' (offset {offset})")
            break

        if debug:
            save_debug_html(f"gupy_{term[:15]}_offset{offset}", raw)

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print(f"  [AVISO] Resposta do Gupy pra '{term}' não é JSON válido")
            break

        page_jobs = data.get("data", [])
        all_jobs += [_to_job_dict(item) for item in page_jobs if _to_job_dict(item)]

        total = data.get("pagination", {}).get("total", len(page_jobs))
        offset += RESULTS_PER_PAGE
        if offset >= total:
            break

    return all_jobs


def _to_job_dict(item: dict) -> dict | None:
    if item.get("type") in TIPOS_IGNORADOS:
        return None

    title = item.get("name", "")
    url = item.get("jobUrl", "")
    if not title or not url:
        return None

    city = item.get("city", "")
    state = item.get("state", "")
    location = f"{city} - {state}".strip(" -") if (city or state) else ""

    return {
        "title": title,
        "url": url,
        "location": location,
        "company": item.get("careerPageName", ""),
        "source": "Gupy",
        "modality": item.get("workplaceType", ""),
    }
