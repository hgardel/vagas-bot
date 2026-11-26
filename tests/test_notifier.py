import requests

import notifier

TOKEN = "TOKEN_SECRETO_123"


class RespostaFalsa:
    status_code = 401

    def json(self):
        return {"ok": False, "error_code": 401, "description": "Unauthorized"}

    def raise_for_status(self):
        raise requests.HTTPError(
            f"401 Client Error: Unauthorized for url: "
            f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        )


def configurar(monkeypatch):
    monkeypatch.setattr(notifier, "TELEGRAM_TOKEN", TOKEN)
    monkeypatch.setattr(notifier, "TELEGRAM_CHAT_ID", "123")


def test_falha_401_nao_vaza_token(monkeypatch, capsys):
    configurar(monkeypatch)
    monkeypatch.setattr(notifier.requests, "post", lambda *a, **k: RespostaFalsa())

    resultado = notifier.send_telegram("oi")

    saida = capsys.readouterr().out
    assert resultado is False
    assert TOKEN not in saida
    assert "401" in saida
    assert "Unauthorized" in saida


def test_falha_de_rede_nao_vaza_token(monkeypatch, capsys):
    configurar(monkeypatch)

    def post_com_timeout(*args, **kwargs):
        raise requests.ConnectionError(f"timeout em https://api.telegram.org/bot{TOKEN}/sendMessage")

    monkeypatch.setattr(notifier.requests, "post", post_com_timeout)

    resultado = notifier.send_telegram("oi")

    assert resultado is False
    assert TOKEN not in capsys.readouterr().out


def test_sem_credenciais_retorna_false(monkeypatch):
    monkeypatch.setattr(notifier, "TELEGRAM_TOKEN", "")
    monkeypatch.setattr(notifier, "TELEGRAM_CHAT_ID", "")

    assert notifier.send_telegram("oi") is False
