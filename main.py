# importacao de bibliotecas
from fastapi import FastAPI
from pydantic import BaseModel

# modelagem da estrutura de dados cdb recebida pelo frontend
class Cdb(BaseModel):
    investimento: float
    taxa: float
    vencimento: int
    res: int

# modelagem da estrutura de dados tesouro recebida pelo frontend
class Tesouro(BaseModel):
    investimento: float
    taxa: float
    aporte_mensal: float
    vencimento: int
    
# TODO: implementar calculo do tesouro
def calcular_tesouro(tesouro: Tesouro):
    return {"mensagem": "nao implementado"}

# TODO: implementar calculo do cdb
def calcular_cdb(tesouro: Tesouro):
    return {"mensagem": "nao implementado"}

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
