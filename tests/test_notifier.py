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


def test_falha_401_nao_vaza_token(monkeypatch, capsys):
    monkeypatch.setattr(notifier, "TELEGRAM_TOKEN", TOKEN)
    monkeypatch.setattr(notifier, "TELEGRAM_CHAT_ID", "123")
    monkeypatch.setattr(notifier.requests, "post", lambda *a, **k: RespostaFalsa())

    resultado = notifier.send_telegram("oi")

    assert resultado is False
    assert TOKEN not in capsys.readouterr().out
