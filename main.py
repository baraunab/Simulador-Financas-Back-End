# importacao de bibliotecas
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime, date, timedelta

class SimulacaoInput(BaseModel):
    produto: Optional[str] = "Produto desconhecido"
    valor_inicial: float
    aporte_mensal: float
    data_inicio: date

    # Referências pro usuario decidir na hora oq ele quer 
    cdi_aa: Optional[float] = 0       # CDI ao ano (ex.: 0.135 = 13,5% a.a.)
    selic_aa: Optional[float] = 0     # SELIC ao ano (ex.: 0.1325 = 13,25% a.a.)
    prefixado_aa: Optional[float] = 0 # Taxa prefixada ao ano (ex.: 0.118 = 11,8% a.a.)

class SimulacaoOutput(BaseModel):
    produto: str
    dias: int
    meses: int
    taxa_aa_usada: float
    taxa_mensal_equivalente: float
    valor_liquido_investido: float
    rentabilidade_bruta: float
    iof: float
    aliquota_irpf: float
    irpf: float
    rentabilidade_liquida: float
    valor_final_liquido: float
    data_resgate: date

class SimulacaoOutput(BaseModel):
    produto: str
    dias: int
    meses: int
    taxa_aa_usada: float
    taxa_mensal_equivalente: float
    valor_liquido_investido: float
    rentabilidade_bruta: float
    iof: float
    aliquota_irpf: float
    irpf: float
    rentabilidade_liquida: float
    valor_final_liquido: float
    data_resgate: date

Produto = Literal[
    "CDB_102", "CDB_104", "CDB_106", "CDB_108",
    "TESOURO_SELIC", "TESOURO_PREFIXADO"
]

# -----------------------------
# Configurações fixas do modelo
# -----------------------------
PRAZO_DIAS = 180            # fixo
MESES = 6                   # aproximação  180 dias
ALIQ_IRPF = 0.225           # 22,5% (até 180 dias)
IOF_VALOR = 0.0             # >30 dias => IOF zero

def simular_mensal(valor_inicial: float, aporte_mensal: float, taxa_mensal: float, n_meses: int):
    """
    Juros compostos mensais com aporte no fim de cada mês.
    Retorna (montante_bruto_final, total_investido).
    """
    montante = float(valor_inicial)
    total_inv = float(valor_inicial)
    for _ in range(n_meses):
        montante *= (1 + taxa_mensal)
        if aporte_mensal > 0:
            montante += float(aporte_mensal)
            total_inv += float(aporte_mensal)
    return montante, total_inv

# perguntar do kinan se isso aqui ta certo
def taxa_mensal_equivalente(taxa_aa: float) -> float:
    # (1 + i_a) = (1 + i_m)^12  => i_m = (1 + i_a)^(1/12) - 1
    return (1.0 + float(taxa_aa)) ** (1.0 / 12.0) - 1.0

def taxa_anual_produto(produto: Literal, cdi_aa: Optional[float], selic_aa: Optional[float], pref_aa: Optional[float]) -> float:
    if produto.startswith("CDB_"):
        if cdi_aa is None:
            raise ValueError("Informe cdi_aa para simular CDB.")
        mult = {
            "CDB_102": 1.02, "CDB_104": 1.04,
            "CDB_106": 1.06, "CDB_108": 1.08
        }[produto]
        return float(cdi_aa) * mult
    elif produto == "TESOURO_SELIC":
        if selic_aa is None:
            raise ValueError("Informe selic_aa para Tesouro Selic.")
        return float(selic_aa)
    elif produto == "TESOURO_PREFIXADO":
        if pref_aa is None:
            raise ValueError("Informe prefixado_aa para Tesouro Prefixado.")
        return float(pref_aa)
    else:
        raise ValueError("Produto inválido.")

# instanciacao da biblioteca FastAPI
app = FastAPI(title="Simulador Financeiro (180d fixo)", version="1.0.0")

# routing pro endereco raiz
@app.get("/")
def read_root():
    return {"mensagem": "em manutencao"}

# routing para operacao do simulador
@app.post("/simular")
def simular(SimInput: SimulacaoInput):
    taxa_aa = taxa_anual_produto(SimInput.produto, SimInput.cdi_aa, SimInput.selic_aa, SimInput.prefixado_aa)
    i_m = taxa_mensal_equivalente(taxa_aa)
    
    bruto_final, total_inv = simular_mensal(
        float(SimInput.valor_inicial),
        float(SimInput.aporte_mensal),
        float(i_m),
        MESES
    )

    rendimento_bruto = max(bruto_final - total_inv, 0.0)

    # Tributação fixa para 180 dias
    iof = IOF_VALOR
    base_ir = max(rendimento_bruto - iof, 0.0)
    ir = base_ir * ALIQ_IRPF

    rendimento_liq = rendimento_bruto - iof - ir
    valor_final_liq = total_inv + rendimento_liq

    data_resgate = SimInput.data_inicio + timedelta(days=PRAZO_DIAS)
    SimOutput = SimulacaoOutput(
        produto=SimInput.produto,
        dias=PRAZO_DIAS,
        meses=MESES,
        taxa_aa_usada=round(taxa_aa, 10),
        taxa_mensal_equivalente=round(i_m, 10),
        valor_liquido_investido=round(total_inv, 2),
        rentabilidade_bruta=round(rendimento_bruto, 2),
        iof=round(iof, 2),
        aliquota_irpf=ALIQ_IRPF,
        irpf=round(ir, 2),
        rentabilidade_liquida=round(rendimento_liq, 2),
        valor_final_liquido=round(valor_final_liq, 2),
        data_resgate=data_resgate
    )
    
    return (SimOutput)
