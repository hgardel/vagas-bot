from bs4 import BeautifulSoup
from scrapers.http_utils import fetch, save_debug_html

SEARCH_TERMS = [
    "analista de seguranca da informacao",
    "analista de cibersegurança",
    "analista soc",
]

BASE_URL = "https://www.bne.com.br/vagas-de-emprego"


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in SEARCH_TERMS:
        html = fetch(BASE_URL, params={"q": term})
        if not html:
            continue
        if debug:
            save_debug_html("bne", html)

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("[class*='vaga'], [class*='job'], article")

        for card in cards:
            title_el = card.find(["h2", "h3", "a"])
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not title:
                continue

            link_el = card.find("a", href=True)
            url = link_el["href"] if link_el else BASE_URL
            if url.startswith("/"):
                url = "https://www.bne.com.br" + url

            location_el = card.find(class_=lambda c: c and "local" in c.lower())
            location = location_el.get_text(strip=True) if location_el else ""

            jobs.append({
                "title": title,
                "url": url,
                "location": location,
                "company": "",
                "source": "BNE",
            })

    unique = {j["url"]: j for j in jobs}
    return list(unique.values())
