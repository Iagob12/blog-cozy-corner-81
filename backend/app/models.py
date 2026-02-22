from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class SectorEnum(str, Enum):
    FINANCEIRO = "Financeiro"
    TECNOLOGIA = "Tecnologia"
    VAREJO = "Varejo"
    CONSTRUCAO = "Construção"
    ENERGIA = "Energia"
    SAUDE = "Saúde"
    INDUSTRIAL = "Industrial"
    CONSUMO = "Consumo"

class StockData(BaseModel):
    ticker: str
    pl: float = Field(alias="P/L")
    roe: float = Field(alias="ROE")
    cagr: float = Field(alias="CAGR")
    divida: float = Field(alias="Dívida")
    setor: Optional[str] = None
    preco_atual: Optional[float] = None

class EfficiencyScore(BaseModel):
    ticker: str
    score: float
    roe: float
    cagr: float
    pl: float
    rank: int
    setor: Optional[str] = None
    preco: Optional[float] = None

class MacroContext(BaseModel):
    juros_selic: float
    inflacao_ipca: float
    setor_favorecido: List[str]
    setor_desfavorecido: List[str]
    peso_ajuste: dict

class Catalisador(BaseModel):
    tipo: str
    descricao: str
    impacto_estimado: str

class PDFAnalysis(BaseModel):
    ticker: str
    catalisadores: List[Catalisador]
    tese_qualitativa: str
    score_qualitativo: float
    alerta_dividendo_trap: bool

class SentimentAlert(BaseModel):
    ticker: str
    volume_mencoes: int
    media_historica: float
    ratio: float
    risco_manada: bool
    recomendacao: str

class PriceAlert(BaseModel):
    ticker: str
    preco_atual: float
    preco_teto: float
    margem_seguranca: float
    acao_recomendada: str

class TopPick(BaseModel):
    ticker: str
    efficiency_score: float
    macro_weight: float
    catalisadores: List[str]
    preco_teto: float
    preco_atual: Optional[float]
    upside_potencial: float
    sentiment_status: str
    recomendacao_final: str
    setor: Optional[str] = None
    roe: float
    cagr: float
    pl: float
    tempo_estimado_dias: int = 90
    sentiment_ratio: Optional[float] = None
    variacao_30d: Optional[float] = None
    rank: Optional[int] = None  # Posição no ranking
