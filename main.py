import sys
import time
from matcher import is_relevant
from storage import load_seen, save_seen
from notifier import send_telegram, format_job_message

from scrapers import bne, linkedin, remoteok
# Catho e Vagas.com.br removidos: ambos usam proteção Cloudflare que
# bloqueia requisições automatizadas. Indeed também removido (403
# constante). Ver README pra detalhes.
#
# RemoteOK: usa API JSON pública, mais estável.
# Remotar: experimental, ainda não calibrado — se vier sempre "0 vagas
# brutas" e o debug_html mostrar assinatura de Cloudflare, remova daqui.

SCRAPERS = [bne, linkedin, remoteok]


def main():
    debug = "--debug" in sys.argv

    seen = load_seen()
    novas_encontradas = 0

    for scraper_module in SCRAPERS:
        nome = scraper_module.__name__.split(".")[-1]
        print(f"--- Buscando em: {nome} ---")
        try:
            jobs = scraper_module.scrape(debug=debug)
        except Exception as e:
            print(f"[ERRO] Scraper {nome} falhou: {e}")
            continue

        print(f"  {len(jobs)} vagas brutas encontradas em {nome}")

        for job in jobs:
            if job["url"] in seen:
                continue

            relevante, motivo = is_relevant(
                job["title"], job.get("location", ""), job.get("modality", "")
            )

            if relevante:
                msg = format_job_message(job, motivo)
                enviado = send_telegram(msg)
                if enviado:
                    novas_encontradas += 1
                    print(f"  [NOVA] {job['title']} -> {motivo}")
                    seen.add(job["url"])
                else:
                    print(f"  [FALHOU ENVIO] {job['title']} -> vai tentar de novo na próxima rodada")
            else:
                seen.add(job["url"])

        time.sleep(2)

    save_seen(seen)
    print(f"\nConcluído. {novas_encontradas} vaga(s) nova(s) notificada(s).")


if __name__ == "__main__":
    main()
