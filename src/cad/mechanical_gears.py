import math
from pathlib import Path

import build123d as bd


def gerar_engrenagem_tecnica(
    modulo: float = 2.0,
    num_dentes: int = 24,
    espessura: float = 12.0,
    diametro_eixo: float = 8.0,
    rasgo_chaveta: bool = True,
    angulo_pressao: float = 20.0,
    diretorio_saida: Path = Path("output"),
    nome_arquivo: str = "engrenagem_involuta.stl",
) -> Path:
    """Gera uma engrenagem mecânica com perfil involuto aproximado e rasgo de chaveta."""
    diretorio_saida.mkdir(parents=True, exist_ok=True)
    caminho = diretorio_saida / nome_arquivo

    raio_primitivo = (modulo * num_dentes) / 2.0
    adendo = modulo
    dedendo = 1.25 * modulo
    raio_externo = raio_primitivo + adendo
    raio_raiz = max(raio_primitivo - dedendo, diametro_eixo * 0.65)
    raio_base = raio_primitivo * math.cos(math.radians(angulo_pressao))

    passo_angular = (2 * math.pi) / num_dentes
    espessura_angular = passo_angular * 0.48  # Folga funcional para impressão 3D

    # Pontos do perfil involuto de 1 dente
    pontos_involuta_esq = []
    pontos_involuta_dir = []
    t_max = math.sqrt(max((raio_externo / raio_base) ** 2 - 1, 0.01))

    for i in range(8):
        t = (t_max * i) / 7
        r = raio_base * math.sqrt(1 + t * t)
        theta = t - math.atan(t)
        ang_dir = -espessura_angular / 2 + theta
        ang_esq = espessura_angular / 2 - theta
        pontos_involuta_dir.append((r * math.cos(ang_dir), r * math.sin(ang_dir)))
        pontos_involuta_esq.append((r * math.cos(ang_esq), r * math.sin(ang_esq)))

    with bd.BuildPart() as engrenagem:
        # 1. Corpo base da engrenagem (diâmetro de raiz)
        bd.Cylinder(
            radius=raio_raiz,
            height=espessura,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )

        # 2. Extrusão dos dentes involutos ao redor do perímetro
        with bd.BuildSketch() as sk_dente:
            perfil = (
                [(raio_raiz * math.cos(-espessura_angular / 2), raio_raiz * math.sin(-espessura_angular / 2))]
                + pontos_involuta_dir
                + list(reversed(pontos_involuta_esq))
                + [(raio_raiz * math.cos(espessura_angular / 2), raio_raiz * math.sin(espessura_angular / 2))]
            )
            bd.Polygon(*perfil, align=None)

        dente_solido = bd.extrude(sk_dente.sketch, amount=espessura)
        for idx in range(num_dentes):
            angulo_deg = math.degrees(idx * passo_angular)
            bd.add(dente_solido.rotate(bd.Axis.Z, angulo_deg))

        # 3. Cubo de reforço central
        raio_cubo = min(diametro_eixo * 1.15, raio_raiz * 0.85)
        if raio_cubo > diametro_eixo / 2 + 1.5:
            bd.Cylinder(
                radius=raio_cubo,
                height=espessura + 4.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )

        # 4. Furo central do eixo
        bd.Cylinder(
            radius=diametro_eixo / 2.0,
            height=espessura + 10.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            mode=bd.Mode.SUBTRACT,
        )

        # 5. Rasgo de chaveta padrão (opcional)
        if rasgo_chaveta and diametro_eixo >= 6.0:
            largura_chaveta = max(2.0, round(diametro_eixo * 0.25, 1))
            profundidade_chaveta = largura_chaveta * 0.55
            with bd.Locations((0, (diametro_eixo / 2.0) + (profundidade_chaveta / 2.0) - 0.2, 0)):
                bd.Box(
                    largura_chaveta,
                    profundidade_chaveta + 0.4,
                    espessura + 10.0,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    mode=bd.Mode.SUBTRACT,
                )

    bd.export_stl(engrenagem.part, str(caminho))
    return caminho
