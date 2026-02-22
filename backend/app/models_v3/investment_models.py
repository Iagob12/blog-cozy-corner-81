"""
Investment Data Models - Estruturas de dados para o sistema de investimentos
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime


@dataclass
class StockData:
    """Dados fundamentalistas de uma ação"""
    ticker: str
    nome: str
    setor: str
    roe: float  # Return on Equity (%)
    cagr: float  # Compound Annual Growth Rate (%)
    pl: float  # Preço/Lucro
    divida_ebitda: float  # Dívida Líquida / EBITDA
    margem_liquida: float  # Margem Líquida (%)
    data_csv: datetime  # Timestamp do CSV
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['data_csv'] = self.data_csv.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StockData':
        """Cria instância a partir de dicionário"""
        if isinstance(data['data_csv'], str):
            data['data_csv'] = datetime.fromisoformat(data['data_csv'])
        return cls(**data)
    
    def atende_criterios(self) -> bool:
        """Verifica se atende critérios mínimos"""
        return (
            self.roe >= 15.0 and
            self.cagr >= 12.0 and
            self.pl < 15.0 and
            self.divida_ebitda < 2.5
        )


@dataclass
class ReleaseData:
    """Dados de Release de Resultados trimestral"""
    ticker: str
    trimestre: str  # "Q4 2025"
    data_relatorio: datetime  # Data do relatório
    pdf_path: str
    texto_completo: str
    metricas: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['data_relatorio'] = self.data_relatorio.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReleaseData':
        """Cria instância a partir de dicionário"""
        if isinstance(data['data_relatorio'], str):
            data['data_relatorio'] = datetime.fromisoformat(data['data_relatorio'])
        return cls(**data)
    
    def is_recente(self, meses: int = 6) -> bool:
        """Verifica se relatório tem menos de X meses"""
        idade = datetime.now() - self.data_relatorio
        return idade.days < (meses * 30)


@dataclass
class PriceData:
    """Dados de preço em tempo real"""
    ticker: str
    preco_atual: float
    timestamp: datetime  # Hora da consulta
    fonte: str  # "brapi", "alphavantage", etc
    variacao_dia: float = 0.0
    volume: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PriceData':
        """Cria instância a partir de dicionário"""
        if isinstance(data['timestamp'], str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
    
    def is_atual(self, horas: int = 24) -> bool:
        """Verifica se preço tem menos de X horas"""
        idade = datetime.now() - self.timestamp
        return idade.total_seconds() < (horas * 3600)


@dataclass
class SetorQuente:
    """Setor identificado no Prompt 1"""
    setor: str
    estagio_ciclo: str  # "começo", "meio", "fim"
    catalisador: str
    tempo_estimado_meses: int
    confianca: str  # "ALTA", "MÉDIA", "BAIXA"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SetorQuente':
        return cls(**data)


@dataclass
class AntiManadaAnalise:
    """Resultado da análise anti-manada (Prompt 6)"""
    ticker: str
    data_analise: datetime
    status: str  # "APROVADO", "REPROVADO"
    estagio_movimento: str  # "COMEÇO", "MEIO", "FIM"
    cobertura_midia: str  # "BAIXA", "MÉDIA", "ALTA"
    movimento_preco: str  # "ACUMULAÇÃO", "SUBIDA_SAUDÁVEL", etc
    fundamento_vs_euforia: str  # "FUNDAMENTO", "MISTO", "EUFORIA"
    posicionamento_institucional: str  # "COMPRANDO", "NEUTRO", "VENDENDO"
    conclusao: str  # "ENTRAR AGORA", "ESPERAR CORREÇÃO", etc
    justificativa: str
    confianca_analise: str  # "ALTA", "MÉDIA", "BAIXA"
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['data_analise'] = self.data_analise.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AntiManadaAnalise':
        if isinstance(data['data_analise'], str):
            data['data_analise'] = datetime.fromisoformat(data['data_analise'])
        return cls(**data)
    
    def is_aprovado(self) -> bool:
        """Verifica se foi aprovado"""
        return self.status == "APROVADO"


@dataclass
class AnaliseCompleta:
    """Análise completa de uma ação (resultado final)"""
    rank: int
    ticker: str
    nome: str
    setor: str
    
    # Preços
    preco_atual: float
    preco_entrada: float
    preco_teto: float
    upside_percent: float
    
    # Timestamps (CRÍTICO para validação)
    data_csv: datetime
    data_relatorio: datetime
    data_preco: datetime
    
    # Análise
    recomendacao: str  # "COMPRA FORTE", "COMPRA", "MONITORAR"
    confianca: str  # "ALTA", "MÉDIA", "BAIXA"
    tempo_estimado_dias: int
    
    # Detalhes
    catalisadores: List[str] = field(default_factory=list)
    riscos: List[str] = field(default_factory=list)
    analise_release: str = ""
    saude_financeira: str = ""
    qualidade_gestao: str = ""
    
    # Anti-manada
    anti_manada_status: str = "PENDENTE"  # "APROVADO", "REPROVADO", "PENDENTE"
    anti_manada_justificativa: str = ""
    
    # Fundamentos
    roe: float = 0.0
    cagr: float = 0.0
    pl: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        data = asdict(self)
        data['data_csv'] = self.data_csv.isoformat()
        data['data_relatorio'] = self.data_relatorio.isoformat()
        data['data_preco'] = self.data_preco.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AnaliseCompleta':
        """Cria instância a partir de dicionário"""
        if isinstance(data['data_csv'], str):
            data['data_csv'] = datetime.fromisoformat(data['data_csv'])
        if isinstance(data['data_relatorio'], str):
            data['data_relatorio'] = datetime.fromisoformat(data['data_relatorio'])
        if isinstance(data['data_preco'], str):
            data['data_preco'] = datetime.fromisoformat(data['data_preco'])
        return cls(**data)
    
    def is_dados_atualizados(self) -> bool:
        """Verifica se todos os dados estão atualizados"""
        agora = datetime.now()
        
        # CSV: máximo 24 horas
        csv_ok = (agora - self.data_csv).total_seconds() < (24 * 3600)
        
        # Preço: máximo 24 horas
        preco_ok = (agora - self.data_preco).total_seconds() < (24 * 3600)
        
        # Release: máximo 6 meses
        release_ok = (agora - self.data_relatorio).days < (6 * 30)
        
        return csv_ok and preco_ok and release_ok
    
    def get_idade_dados(self) -> Dict[str, str]:
        """Retorna idade de cada dado em formato legível"""
        agora = datetime.now()
        
        csv_horas = (agora - self.data_csv).total_seconds() / 3600
        preco_horas = (agora - self.data_preco).total_seconds() / 3600
        release_dias = (agora - self.data_relatorio).days
        
        return {
            "csv": f"{csv_horas:.1f}h atrás",
            "preco": f"{preco_horas:.1f}h atrás",
            "release": f"{release_dias} dias atrás"
        }


@dataclass
class RankingFinal:
    """Ranking final com todas as análises"""
    data_geracao: datetime
    total_analisadas: int
    total_aprovadas: int
    ranking: List[AnaliseCompleta] = field(default_factory=list)
    setores_quentes: List[SetorQuente] = field(default_factory=list)
    log_execucao: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "data_geracao": self.data_geracao.isoformat(),
            "total_analisadas": self.total_analisadas,
            "total_aprovadas": self.total_aprovadas,
            "ranking": [a.to_dict() for a in self.ranking],
            "setores_quentes": [s.to_dict() for s in self.setores_quentes],
            "log_execucao": self.log_execucao
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'RankingFinal':
        """Cria instância a partir de dicionário"""
        if isinstance(data['data_geracao'], str):
            data['data_geracao'] = datetime.fromisoformat(data['data_geracao'])
        
        data['ranking'] = [AnaliseCompleta.from_dict(a) for a in data.get('ranking', [])]
        data['setores_quentes'] = [SetorQuente.from_dict(s) for s in data.get('setores_quentes', [])]
        
        return cls(**data)
    
    def get_top_n(self, n: int = 15) -> List[AnaliseCompleta]:
        """Retorna top N análises"""
        return self.ranking[:n]
    
    def filtrar_por_confianca(self, confianca: str = "ALTA") -> List[AnaliseCompleta]:
        """Filtra por nível de confiança"""
        return [a for a in self.ranking if a.confianca == confianca]
    
    def filtrar_por_setor(self, setor: str) -> List[AnaliseCompleta]:
        """Filtra por setor"""
        return [a for a in self.ranking if a.setor.lower() == setor.lower()]
