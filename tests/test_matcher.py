import pytest

from matcher import is_relevant

PG = "Ponta Grossa, PR"
SP = "São Paulo, SP"

CASOS = [
    # prioridades
    ("Analista SOC", PG, "presencial", (True, "prioridade_1_presencial_pg")),
    ("Analista SOC", PG, "híbrido", (True, "prioridade_2_hibrido_pg")),
    ("Analista SOC", PG, "remoto", (True, "prioridade_3_remoto_pg")),
    ("Analista SOC", "Curitiba, PR", "remoto", (True, "prioridade_4_remoto_curitiba")),
    ("Security Analyst", "Brasil", "remoto", (True, "prioridade_5_remoto_brasil")),
    ("Analista SOC", SP, "", (True, "modalidade_desconhecida")),
    ("Suporte de TI", PG, "", (True, "modalidade_desconhecida")),
    # rejeições
    ("Analista SOC Sênior", PG, "presencial", (False, "excluido_por_senioridade")),
    ("Motorista", PG, "presencial", (False, "titulo_nao_bate")),
    ("SOC Analyst", "Lisbon, Portugal", "remoto", (False, "fora_do_brasil")),
    ("Analista SOC", SP, "presencial", (False, "presencial_fora_de_pg")),
    ("Analista SOC", "Curitiba, PR", "híbrido", (False, "hibrido_fora_de_pg")),
    ("Suporte de TI", SP, "", (False, "nao_bateu_nenhuma_regra")),
    ("Suporte de TI", PG, "remoto", (False, "nao_bateu_nenhuma_regra")),
    # ordem das regras e bordas
    ("Analista SOC", PG, "remoto ou híbrido", (True, "prioridade_3_remoto_pg")),
    ("Analista SOC", PG, "presencial ou híbrido", (True, "prioridade_2_hibrido_pg")),
    ("Analista SOC", "", "remoto", (True, "prioridade_5_remoto_brasil")),
    ("Analista SOC", "Ponta Grossa, PR (Remoto)", "", (True, "prioridade_3_remoto_pg")),
    ("Técnico de Segurança do Trabalho", PG, "presencial", (False, "excluido_por_senioridade")),
]


@pytest.mark.parametrize("titulo, local, modalidade, esperado", CASOS)
def test_is_relevant(titulo, local, modalidade, esperado):
    assert is_relevant(titulo, local, modalidade) == esperado
