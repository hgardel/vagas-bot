import types

import pytest

import main

VAGA = {
    "title": "Analista SOC",
    "location": "Brasil",
    "modality": "remoto",
    "url": "https://exemplo.com/vaga/1",
}


@pytest.fixture
def ambiente(monkeypatch):
    salvos = []
    scraper_falso = types.SimpleNamespace(__name__="scraper_falso", scrape=lambda debug=False: [dict(VAGA)])
    monkeypatch.setattr(main, "SCRAPERS", [scraper_falso])
    monkeypatch.setattr(main, "load_seen", lambda: set())
    monkeypatch.setattr(main, "save_seen", lambda seen: salvos.append(set(seen)))
    monkeypatch.setattr(main.time, "sleep", lambda s: None)
    return salvos


def test_falha_de_envio_derruba_o_bot_mas_salva_vistos(monkeypatch, ambiente):
    monkeypatch.setattr(main, "send_telegram", lambda msg: False)

    with pytest.raises(SystemExit) as saida:
        main.main()

    assert saida.value.code == 1
    assert len(ambiente) == 1


def test_envio_ok_termina_sem_erro(monkeypatch, ambiente):
    monkeypatch.setattr(main, "send_telegram", lambda msg: True)

    main.main()

    assert VAGA["url"] in ambiente[0]
