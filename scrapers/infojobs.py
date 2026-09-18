from urllib.parse import quote
from bs4 import BeautifulSoup
from scrapers.http_utils import fetch, save_debug_html
from config import INFOJOBS_SEARCH_TERMS, INFOJOBS_PROVINCIA_PARANA

BASE_URL = "https://www.infojobs.com.br/empregos.aspx"

# (nome pra log, provincia_id ou None pra Brasil inteiro)
INFOJOBS_LOCATIONS = [
    ("Parana", INFOJOBS_PROVINCIA_PARANA),
    ("Brasil", None),
]


def scrape(debug: bool = False) -> list[dict]:
    jobs = []
    for term in INFOJOBS_SEARCH_TERMS:
        for local_nome, provincia_id in INFOJOBS_LOCATIONS:
            params = {"palabra": term}
            if provincia_id is not None:
                params["provincia"] = provincia_id

            html = fetch(BASE_URL, params=params)
            if not html:
                print(f"  [AVISO] InfoJobs não respondeu pra '{term}' em '{local_nome}'")
                continue

            if debug:
                save_debug_html(f"infojobs_{local_nome}_{term[:15]}", html)

            jobs += _parse(html)

    unique = {j["url"]: j for j in jobs}
    return list(unique.values())


def _parse(html: str) -> list[dict]:
    """
    ATENÇÃO — leia antes de mexer:
    O InfoJobs não tem API pública conhecida, então isso aqui é scraping de
    HTML de verdade. Os links de vaga seguem o padrão /vaga-de-...aspx
    (confirmado nas buscas manuais que você fez). Isso é confiável.

    O que NÃO está confiável aqui: local e modalidade (remoto/híbrido/
    presencial) da vaga. Eu não tive acesso ao HTML bruto da página de
    resultado pra escrever um seletor exato pra esses campos — só vi a
    versão em markdown/texto. Por isso essa versão só extrai título e link
    com certeza.

    Isso não quebra o filtro: o matcher.py trata local vazio como
    "modalidade desconhecida" e ainda assim notifica se o título bater
    com palavra-chave de cyber. Só perde a etiqueta bonita de prioridade
    (presencial PG / remoto Curitiba etc.) — tudo cai como "CONFIRA O
    LOCAL NO LINK ABAIXO".

    Se quiser refinar isso depois: abre uma dessas páginas de busca no
    navegador, aperta Ctrl+U (ver código-fonte), procura por um dos
    títulos de vaga que aparece na tela, e vê que tag/classe envolve o
    bloco inteiro do card (título + local + modalidade). Me manda esse
    trecho de HTML que eu escrevo o seletor certo.
    """
    jobs = []
    soup = BeautifulSoup(html, "html.parser")

    # pega todo link cujo href comece com /vaga-de- (padrão confirmado)
    links = soup.select('a[href^="/vaga-de-"]')

    for link in links:
        title = link.get_text(strip=True)
        href = link.get("href", "")
        if not title or not href:
            continue

        url = "https://www.infojobs.com.br" + href

        jobs.append({
            "title": title,
            "url": url,
            "location": "",       # não extraído nessa versão, ver docstring acima
            "company": "",        # idem
            "source": "InfoJobs",
        })

    return jobs
