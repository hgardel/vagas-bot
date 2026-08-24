"""
Scraper do Remotar (remotar.com.br) — portal brasileiro focado 100% em
vagas remotas.

EXPERIMENTAL: ainda não testado contra o site real. Se vier "0 vagas
brutas", roda com --debug e olha debug_html/remotar.html — se aparecer
assinatura de Cloudflare (__CF$cv$params) igual aconteceu com Catho e
Vagas.com.br, esse site também não vai dar pra automatizar e o certo é
tirar da lista (mesma decisão que tomamos pros outros dois).
"""
from bs4 import BeautifulSoup
from scrapers.http_utils import fetch, save_debug_html

SEARCH_TERMS = [
    "analista de segurança da informação",
    "analista de cibersegurança",
    "analista soc",
]

BASE_URL = "https://www.remotar.com.br/vagas"


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in SEARCH_TERMS:
        html = fetch(BASE_URL, params={"q": term})
        if not html:
            continue
        if debug:
            save_debug_html("remotar", html)

        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select("[class*='vaga'], [class*='job'], article, li")

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
                url = "https://www.remotar.com.br" + url

            jobs.append({
                "title": title,
                "url": url,
                "location": "Brasil (Remoto)",
                "company": "",
                "source": "Remotar",
                "modality": "remoto",
            })

    unique = {j["url"]: j for j in jobs}
    return list(unique.values())
