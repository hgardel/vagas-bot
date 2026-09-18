from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from scrapers.http_utils import fetch, save_debug_html
from config import MAX_JOB_AGE_DAYS, LINKEDIN_MAX_PAGES

SEARCH_TERMS = [
    "analista de segurança da informação",
    "analista de cibersegurança",
    "cybersecurity analyst",
    "soc analyst",
    "analista soc",
    "blue team",
]

LOCATIONS = ["Ponta Grossa, Paraná, Brasil", "Curitiba, Paraná, Brasil", "Brasil"]

ENDPOINT = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

_TPR_SECONDS = MAX_JOB_AGE_DAYS * 86400
_RESULTS_PER_PAGE = 10  # fixo, definido pela própria API do LinkedIn


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in SEARCH_TERMS:
        for location in LOCATIONS:
            jobs += _scrape_all_pages(term, location, debug)

    unique = {j["url"]: j for j in jobs}
    return list(unique.values())


def _scrape_all_pages(term: str, location: str, debug: bool) -> list[dict]:
    """
    Busca até LINKEDIN_MAX_PAGES páginas (10 resultados cada) pra uma
    combinação de termo+local. Para cedo se uma página voltar vazia
    (fim dos resultados, ou LinkedIn bloqueando/limitando o IP).
    """
    all_jobs = []
    for page in range(LINKEDIN_MAX_PAGES):
        start = page * _RESULTS_PER_PAGE
        html = fetch(ENDPOINT, params={
            "keywords": term,
            "location": location,
            "start": start,
            "f_TPR": f"r{_TPR_SECONDS}",
        })

        if not html:
            # fetch() já tentou retries; se voltou None aqui é bloqueio/erro
            # persistente. Não adianta insistir nas próximas páginas dessa
            # busca.
            print(f"  [AVISO] LinkedIn não respondeu pra '{term}' em '{location}' "
                  f"(página {page}). Pode ser rate limit — parando essa busca.")
            break

        if debug:
            save_debug_html(f"linkedin_{location.split(',')[0]}_{term[:15]}_p{page}", html)

        page_jobs = _parse(html)
        if not page_jobs:
            # página vazia = acabaram os resultados dessa busca
            break

        all_jobs += page_jobs

        if len(page_jobs) < _RESULTS_PER_PAGE:
            # última página parcial, não tem mais o que buscar
            break

    return all_jobs


def _parse(html: str) -> list[dict]:
    jobs = []
    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("li")
    limite = datetime.now(timezone.utc) - timedelta(days=MAX_JOB_AGE_DAYS)

    for card in cards:
        title_el = card.find("h3", class_=lambda c: c and "base-search-card__title" in c)
        if not title_el:
            continue
        title = title_el.get_text(strip=True)

        link_el = card.find("a", href=True)
        url = link_el["href"].split("?")[0] if link_el else ""
        if not url:
            continue

        time_el = card.find("time")
        if time_el and time_el.get("datetime"):
            try:
                data_publicacao = datetime.fromisoformat(
                    time_el["datetime"].replace("Z", "+00:00")
                )
                if data_publicacao.tzinfo is None:
                    data_publicacao = data_publicacao.replace(tzinfo=timezone.utc)
                if data_publicacao < limite:
                    continue
            except ValueError:
                pass

        company_el = card.find("h4", class_=lambda c: c and "base-search-card__subtitle" in c)
        company = company_el.get_text(strip=True) if company_el else ""

        location_el = card.find("span", class_=lambda c: c and "job-search-card__location" in c)
        location = location_el.get_text(strip=True) if location_el else ""

        jobs.append({
            "title": title,
            "url": url,
            "location": location,
            "company": company,
            "source": "LinkedIn",
        })
    return jobs
