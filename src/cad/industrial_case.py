from pathlib import Path

from build123d import Align, Axis, Box, Cylinder, Pos, Rot, export_stl, fillet, offset


def gerar_case_eletronico(
    comprimento: float = 90.0,
    largura: float = 60.0,
    altura: float = 35.0,
    parede: float = 2.4,
    furo_parafuso: float = 4.2,
    diretorio_saida: Path = Path("output"),
    nome_arquivo: str = "case_tecnico.stl",
) -> Path:
    if min(comprimento, largura, altura, parede, furo_parafuso) <= 0:
        raise ValueError("As dimensões e os diâmetros devem ser maiores que zero.")
    if parede * 2 >= min(comprimento, largura, altura):
        raise ValueError("A espessura da parede é incompatível com as dimensões.")

    corpo = Box(
        comprimento,
        largura,
        altura,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    tampa_superior = corpo.faces().sort_by(Axis.Z)[-1]
    corpo = offset(corpo, amount=-parede, openings=tampa_superior)
    corpo = fillet(corpo.edges().filter_by(Axis.Z), radius=min(3.0, parede))

    aba_projecao = max(parede * 2, 8.0)
    aba_espessura = parede
    for lado in (-1, 1):
        posicao_y = lado * (largura / 2 + aba_projecao / 2 - parede / 2)
        aba = Pos(0, posicao_y, 0) * Box(
            comprimento * 0.7,
            aba_projecao,
            aba_espessura,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        corpo += aba

    espacamento_x = comprimento * 0.7 / 2 - max(furo_parafuso, 3.0)
    for x in (-espacamento_x, espacamento_x):
        for y in (-largura / 2 - aba_projecao / 2, largura / 2 + aba_projecao / 2):
            furo = Pos(x, y, -1) * Cylinder(
                furo_parafuso / 2,
                aba_espessura + 2,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )
            corpo -= furo

    diametro_cabo = min(12.0, largura / 3, altura / 3)
    furo_cabo = (
        Pos(comprimento / 2 - parede - 1, 0, altura / 2)
        * Rot(0, 90, 0)
        * Cylinder(
            diametro_cabo / 2,
            parede + 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
    )
    corpo -= furo_cabo

    diretorio_saida = Path(diretorio_saida)
    diretorio_saida.mkdir(parents=True, exist_ok=True)
    arquivo_saida = diretorio_saida / nome_arquivo
    export_stl(corpo, str(arquivo_saida))
    return arquivo_saida
