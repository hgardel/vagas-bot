"""
Lógica de decisão: essa vaga interessa ou não, e qual a prioridade dela?

Ordem de prioridade:
1. Presencial em Ponta Grossa
2. Híbrido em Ponta Grossa
3. Home office em Ponta Grossa
4. Home office em Curitiba
5. Home office no resto do Brasil
"""
import unicodedata
import re
from config import ALL_CYBER_KEYWORDS, KEYWORDS_ADS, EXCLUDE_KEYWORDS, CIDADE_BASE_PRESENCIAL


def _normalize(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return text


def _contains_any(text: str, keywords: list) -> bool:
    text_norm = _normalize(text)
    return any(_normalize(kw) in text_norm for kw in keywords)


def _contains_any_word(text: str, keywords: list) -> bool:
    text_norm = _normalize(text)
    for kw in keywords:
        kw_norm = _normalize(kw).strip()
        pattern = r"\b" + re.escape(kw_norm) + r"\b"
        if re.search(pattern, text_norm):
            return True
    return False


REMOTE_HINTS = ["remoto", "remote", "home office", "anywhere", "trabalho remoto"]
ONSITE_HINTS = ["presencial", "on-site", "onsite", "no local"]
HYBRID_HINTS = ["hibrido", "hybrid"]

_UF_BRASIL = [
    "ac", "al", "ap", "am", "ba", "ce", "df", "es", "go", "ma", "mt", "ms",
    "mg", "pa", "pb", "pr", "pe", "pi", "rj", "rn", "rs", "ro", "rr", "sc",
    "sp", "se", "to",
]


def _has_word(location_norm: str, word: str) -> bool:
    return re.search(r"\b" + re.escape(word) + r"\b", location_norm) is not None


def _looks_brazilian(location: str) -> bool:
    loc_norm = _normalize(location)
    if "brasil" in loc_norm or "brazil" in loc_norm:
        return True
    return any(_has_word(loc_norm, uf) for uf in _UF_BRASIL)


def _detect_modality(title: str, location: str, modality: str) -> str:
    combined = _normalize(f"{title} {location} {modality}")
    if any(h in combined for h in REMOTE_HINTS):
        return "remoto"
    if any(h in combined for h in HYBRID_HINTS):
        return "hibrido"
    if any(h in combined for h in ONSITE_HINTS):
        return "presencial"
    return "desconhecido"


def is_relevant(title: str, location: str, modality: str = "") -> tuple[bool, str]:
    location_norm = _normalize(location)

    if _contains_any_word(title, EXCLUDE_KEYWORDS):
        return False, "excluido_por_senioridade"

    is_cyber = _contains_any(title, ALL_CYBER_KEYWORDS)
    is_ads = _contains_any(title, KEYWORDS_ADS)

    if not (is_cyber or is_ads):
        return False, "titulo_nao_bate"

    modalidade_detectada = _detect_modality(title, location, modality)
    esta_em_pg = "ponta grossa" in location_norm
    esta_em_curitiba = _has_word(location_norm, "curitiba")
    eh_brasil = _looks_brazilian(location)

    if location.strip() and not eh_brasil:
        return False, "fora_do_brasil"

    if modalidade_detectada == "presencial":
        if esta_em_pg:
            return True, "prioridade_1_presencial_pg"
        return False, "presencial_fora_de_pg"

    if modalidade_detectada == "hibrido":
        if esta_em_pg:
            return True, "prioridade_2_hibrido_pg"
        return False, "hibrido_fora_de_pg"

    if modalidade_detectada == "remoto" and is_cyber:
        if esta_em_pg:
            return True, "prioridade_3_remoto_pg"
        if esta_em_curitiba:
            return True, "prioridade_4_remoto_curitiba"
        return True, "prioridade_5_remoto_brasil"

    if modalidade_detectada == "desconhecido" and (is_cyber or (is_ads and esta_em_pg)):
        return True, "modalidade_desconhecida"

    return False, "nao_bateu_nenhuma_regra"
