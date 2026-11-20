# Vagas Bot - Alerta de Vagas de Cibersegurança via Telegram

Bot que busca vagas de cibersegurança júnior em LinkedIn e InfoJobs, filtra pelas suas regras (localização e senioridade) e avisa no Telegram quando achar algo novo.

## Ordem de prioridade das vagas

1. Presencial em Ponta Grossa
2. Híbrido em Ponta Grossa
3. Home office em Ponta Grossa
4. Home office em Curitiba
5. Home office no resto do Brasil

Vagas sem modalidade identificada chegam com o aviso "CONFIRA O LOCAL". Vagas de suporte de TI e desenvolvedor júnior só entram se forem presenciais em Ponta Grossa.

## Testar localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # cola seu TELEGRAM_TOKEN e TELEGRAM_CHAT_ID
python main.py --debug
```
