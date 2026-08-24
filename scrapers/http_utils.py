import time
import os
import requests
from config import HEADERS

DEBUG_DIR = "debug_html"


def fetch(url: str, params: dict = None, retries: int = 3, timeout: int = 20, extra_headers: dict = None) -> str | None:
    headers = dict(HEADERS)
    if extra_headers:
        headers.update(extra_headers)
    for attempt in range(1, retries + 1):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=timeout)
            if resp.status_code == 200:
                return resp.text
            print(f"[AVISO] {url} retornou status {resp.status_code} (tentativa {attempt})")
        except Exception as e:
            print(f"[ERRO] Falha ao buscar {url}: {e} (tentativa {attempt})")
        time.sleep(2 * attempt)
    return None


def save_debug_html(source: str, html: str):
    os.makedirs(DEBUG_DIR, exist_ok=True)
    path = os.path.join(DEBUG_DIR, f"{source}.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
