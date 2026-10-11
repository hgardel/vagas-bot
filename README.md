# Vagas Bot - Alerta de Vagas de Cibersegurança via Telegram

Bot que busca vagas de cibersegurança júnior em LinkedIn e InfoJobs, filtra pelas suas regras (localização e senioridade) e avisa no Telegram quando achar algo novo.

## Ordem de prioridade das vagas

1. Presencial em Ponta Grossa
2. Home office em Ponta Grossa
3. Home office em Curitiba
4. Home office no resto do Paraná
5. Home office em SC/SP/RS
6. Home office no resto do Brasil

## Testar localmente

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # cola seu TELEGRAM_TOKEN e TELEGRAM_CHAT_ID
python main.py --debug
```
