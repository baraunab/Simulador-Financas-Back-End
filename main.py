# importacao de bibliotecas
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

class SimulacaoInput(BaseModel):
    produto: Optional[str] = "Produto desconhecido"
    valor_inicial: float
    aporte_mensal: float
    data_inicio: str

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
    data_resgate: str

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
    data_resgate: str

# instanciacao da biblioteca FastAPI
app = FastAPI(title="Simulador Financeiro (180d fixo)", version="1.0.0")

# routing pro endereco raiz
@app.get("/")
def read_root():
    return {"mensagem": "em manutencao"}

# routing para operacao do simulador
@app.post("/simular")
def simular(SimInput: SimulacaoInput):
    return (SimInput)
