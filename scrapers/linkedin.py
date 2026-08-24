from datetime import datetime, timedelta, timezone
from bs4 import BeautifulSoup
from scrapers.http_utils import fetch, save_debug_html
from config import MAX_JOB_AGE_DAYS

SEARCH_TERMS = [
    "analista de segurança da informação",
    "analista de cibersegurança",
    "cybersecurity analyst",
]

LOCATIONS = ["Ponta Grossa, Paraná, Brasil", "Curitiba, Paraná, Brasil", "Brasil"]

ENDPOINT = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"

_TPR_SECONDS = MAX_JOB_AGE_DAYS * 86400


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in SEARCH_TERMS:
        for location in LOCATIONS:
            html = fetch(ENDPOINT, params={
                "keywords": term,
                "location": location,
                "start": 0,
                "f_TPR": f"r{_TPR_SECONDS}",
            })
            if not html:
                continue
            if debug:
                save_debug_html(f"linkedin_{location.split(',')[0]}", html)
            jobs += _parse(html)

    unique = {j["url"]: j for j in jobs}
    return list(unique.values())


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
