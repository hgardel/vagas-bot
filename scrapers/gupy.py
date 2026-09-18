"""
STUB — ainda não funcional. Falta um dado que só dá pra pegar no navegador.

O que eu sabia (de documentação de terceiros, não confirmado ao vivo):
existe/existia uma API pública em employability-portal.gupy.io/api/v1/jobs.
Você não achou esse domínio sendo chamado no DevTools, então ou o Gupy
trocou de endpoint, ou o front-end atual usa outro caminho. Não vou
adivinhar — isso quebraria silenciosamente e você não saberia por quê.

COMO ACHAR O ENDPOINT CERTO (5 minutos):
1. Abre https://portal.gupy.io/job-search/term=blue%20team no navegador.
2. Aperta F12 (DevTools) → aba "Network" (ou "Rede").
3. Filtra por "Fetch/XHR" (tem esse filtro no topo da aba Network).
4. Aperta F5 pra recarregar a página com o DevTools já aberto.
5. Vai aparecer uma lista de requisições. Procura uma que tenha "job" ou
   "search" no nome, com resposta em JSON (aba "Response" ou "Preview").
6. Clica nela, vê a "Request URL" completa (com todos os parâmetros)
   e o método (GET ou POST). Se for POST, também precisa do "Request
   Payload"/"Request Body".
7. Me manda essa URL completa (e o body, se for POST) que eu termino
   esse arquivo.

Enquanto isso, use a busca manual mesmo — o que você já fez (procurar
"blue team", "soc analyst" etc. direto no portal.gupy.io) já funciona e
achou vaga boa (Bemol Digital). Não é ideal automatizar tudo, mas não
trava sua busca.
"""


def scrape(debug: bool = False) -> list[dict]:
    print("  [INFO] Gupy scraper ainda não implementado — falta o endpoint. "
          "Veja o topo deste arquivo.")
    return []
