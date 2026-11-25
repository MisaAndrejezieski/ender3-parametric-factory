from pathlib import Path

if __package__:
    from .cad.industrial_case import gerar_case_eletronico
    from .finance.roadmap import PlanoRendaExtra3D
else:
    from cad.industrial_case import gerar_case_eletronico
    from finance.roadmap import PlanoRendaExtra3D


def main() -> None:
    PlanoRendaExtra3D(meta_mensal_brl=800.0).exibir_projecao()
    arquivo = gerar_case_eletronico(
        comprimento=110.0,
        largura=75.0,
        altura=42.0,
        diretorio_saida=Path("output"),
        nome_arquivo="case_esp32_110x75x42.stl",
    )
    print(f"Arquivo STL gerado: {arquivo.resolve()}")


if __name__ == "__main__":
    main()
