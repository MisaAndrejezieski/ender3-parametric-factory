from dataclasses import dataclass
from math import ceil


@dataclass(frozen=True)
class FrenteDeNegocio:
    nome: str
    alvo: str
    stack_tecnica: str
    ticket_medio_brl: float
    custo_producao_brl: float
    esforco_manual_min: float

    @property
    def lucro_liquido(self) -> float:
        return self.ticket_medio_brl - self.custo_producao_brl

    @property
    def valor_hora_efetivo(self) -> float:
        if self.esforco_manual_min <= 0:
            raise ValueError("O esforço manual deve ser maior que zero.")
        return self.lucro_liquido / (self.esforco_manual_min / 60)


class PlanoRendaExtra3D:
    def __init__(self, meta_mensal_brl: float = 800.0) -> None:
        if meta_mensal_brl <= 0:
            raise ValueError("A meta mensal deve ser maior que zero.")
        self.meta_mensal_brl = meta_mensal_brl
        self.frentes = (
            FrenteDeNegocio(
                nome="Engenharia Reversa B2B",
                alvo="Pequenas indústrias e oficinas",
                stack_tecnica="Medição, CAD paramétrico e impressão 3D",
                ticket_medio_brl=450.0,
                custo_producao_brl=45.0,
                esforco_manual_min=180.0,
            ),
            FrenteDeNegocio(
                nome="Gerador Paramétrico sob demanda",
                alvo="Engenheiros e makers",
                stack_tecnica="Python, build123d e automação CAD",
                ticket_medio_brl=180.0,
                custo_producao_brl=18.0,
                esforco_manual_min=30.0,
            ),
            FrenteDeNegocio(
                nome="Venda Passiva de STLs",
                alvo="Comunidade maker e impressão 3D",
                stack_tecnica="Modelagem paramétrica e marketplaces STL",
                ticket_medio_brl=35.0,
                custo_producao_brl=3.0,
                esforco_manual_min=10.0,
            ),
        )

    def exibir_projecao(self) -> None:
        print(f"Meta mensal: R$ {self.meta_mensal_brl:.2f}")
        for frente in self.frentes:
            volume = ceil(self.meta_mensal_brl / frente.lucro_liquido)
            print(
                f"{frente.nome}: lucro por peça R$ {frente.lucro_liquido:.2f} | "
                f"ganho por hora ativa R$ {frente.valor_hora_efetivo:.2f} | "
                f"volume mensal para a meta: {volume} peça(s)"
            )
