from src.cad.industrial_case import gerar_case_eletronico
from src.finance.roadmap import FrenteDeNegocio


def test_frente_de_negocio_calcula_lucro_e_valor_hora() -> None:
    frente = FrenteDeNegocio(
        nome="Peça técnica",
        alvo="Oficina",
        stack_tecnica="CAD e impressão 3D",
        ticket_medio_brl=120.0,
        custo_producao_brl=30.0,
        esforco_manual_min=45.0,
    )

    assert frente.lucro_liquido == 90.0
    assert frente.valor_hora_efetivo == 120.0


def test_gerar_case_eletronico_exporta_stl(tmp_path) -> None:
    arquivo = gerar_case_eletronico(diretorio_saida=tmp_path)

    assert arquivo.exists()
    assert arquivo.stat().st_size > 0
