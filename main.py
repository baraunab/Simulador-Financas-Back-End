# importacao de bibliotecas
from fastapi import FastAPI
from pydantic import BaseModel

# modelagem da estrutura de dados cdb recebida pelo frontend
class Cdb(BaseModel):
    investimento: float
    lucro_liquido: float
    taxa: float
    vencimento: str

# modelagem da estrutura de dados tesouro recebida pelo frontend
class Tesouro(BaseModel):
    investimento: float
    aporte_mensal: float
    lucro_bruto: float
    lucro_liquido: float
    titulo: str
    vencimento: str
    
# TODO: implementar calculo do tesouro
def calcular_tesouro(tesouro: Tesouro):
    return {"mensagem": "tesouro nao implementado"}

# TODO: implementar calculo do cdb
def calcular_cdb(cdb: Cdb):
    return {"mensagem": "cdb nao implementado"}

# instanciacao da biblioteca FastAPI
app = FastAPI()

# routing pro endereco raiz
@app.get("/")
def read_root():
    return {"mensagem": "em manutencao"}

# routing para operacao do simulador
@app.post("/cdb")
def calcular(cdb: Cdb):
    return calcular_cdb(cdb)

# routing para operacao do simulador
@app.post("/tesouro")
def calcular(tesouro: Tesouro):
    return calcular_tesouro(tesouro)
