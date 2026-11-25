import pytest

from matcher import is_relevant

PG = "Ponta Grossa, PR"
SP = "São Paulo, SP"

CASOS = [
    # prioridades
    ("Analista SOC", PG, "remoto", (True, "prioridade_1_remoto")),
    ("Analista SOC", "Curitiba, PR", "remoto", (True, "prioridade_1_remoto")),
    ("Analista SOC", SP, "remoto", (True, "prioridade_1_remoto")),
    ("Security Analyst", "Brasil", "remoto", (True, "prioridade_1_remoto")),
    ("Analista SOC", PG, "híbrido", (True, "prioridade_2_hibrido_pg")),
    ("Analista SOC", PG, "presencial", (True, "prioridade_3_presencial_pg")),
    ("Analista SOC", SP, "híbrido", (True, "prioridade_4_hibrido_sp")),
    ("Analista SOC", SP, "presencial", (True, "prioridade_5_presencial_sp")),
    ("Analista SOC", SP, "", (True, "modalidade_desconhecida")),
    ("Suporte de TI", PG, "", (True, "modalidade_desconhecida")),
    # rejeições
    ("Analista SOC Sênior", PG, "presencial", (False, "excluido_por_senioridade")),
    ("Motorista", PG, "presencial", (False, "titulo_nao_bate")),
    ("SOC Analyst", "Lisbon, Portugal", "remoto", (False, "fora_do_brasil")),
    ("Analista SOC", "Curitiba, PR", "presencial", (False, "presencial_fora_de_pg_sp")),
    ("Analista SOC", "Curitiba, PR", "híbrido", (False, "hibrido_fora_de_pg_sp")),
    ("Suporte de TI", SP, "presencial", (False, "presencial_fora_de_pg_sp")),
    ("Suporte de TI", SP, "", (False, "nao_bateu_nenhuma_regra")),
    ("Suporte de TI", PG, "remoto", (False, "nao_bateu_nenhuma_regra")),
    # ordem das regras e bordas
    ("Analista SOC", PG, "remoto ou híbrido", (True, "prioridade_1_remoto")),
    ("Analista SOC", PG, "presencial ou híbrido", (True, "prioridade_2_hibrido_pg")),
    ("Analista SOC", "", "remoto", (True, "prioridade_1_remoto")),
    ("Analista SOC", "Ponta Grossa, PR (Remoto)", "", (True, "prioridade_1_remoto")),
    ("Técnico de Segurança do Trabalho", PG, "presencial", (False, "excluido_por_senioridade")),
]


@pytest.mark.parametrize("titulo, local, modalidade, esperado", CASOS)
def test_is_relevant(titulo, local, modalidade, esperado):
    assert is_relevant(titulo, local, modalidade) == esperado
