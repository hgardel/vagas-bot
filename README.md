# Vagas Bot - Alerta de Vagas de Cibersegurança via Telegram

Bot que busca vagas de cibersegurança júnior em LinkedIn, filtra pelas suas regras e avisa no Telegram quando achar algo novo. Roda sozinho no GitHub Actions, de graça, 6x por dia.

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

## Subir pro GitHub

```bash
git init
git add .
git commit -m "primeiro commit do vagas-bot"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

Depois, em **Settings → Secrets and variables → Actions**, crie os
secrets `TELEGRAM_TOKEN` e `TELEGRAM_CHAT_ID`.

## Ajustando as regras

- `config.py`: palavras-chave, cidades, exclusões
- `matcher.py`: lógica de prioridade por proximidade
- Pra adicionar um novo site: crie `scrapers/novosite.py` com uma função
  `scrape(debug=False)` retornando lista de dicts com `title`, `url`,
  `location`, `company`, `source` (e opcionalmente `modality`), e
  registre em `main.py` na lista `SCRAPERS`.

## Sites removidos e por quê

- **Catho**, **Vagas.com.br**: usam Cloudflare, bloqueiam requisição
  automatizada (confirmado pelo `__CF$cv$params` na resposta). Contornar
  isso exigiria simular um navegador completo — não vale a pena.
- **Indeed**: bloqueio 403 constante, mesmo motivo.
- **Remotar**: ainda experimental, pode ter o mesmo problema — confira o
  `debug_html/remotar.html` na primeira rodada.
