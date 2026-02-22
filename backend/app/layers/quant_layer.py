import pandas as pd
from typing import List
from app.models import StockData, EfficiencyScore

class QuantLayer:
    """Camada 1: Filtro Quantitativo"""
    
    def __init__(self, min_roe: float = 15, min_cagr: float = 12, max_pl: float = 15):
        self.min_roe = min_roe
        self.min_cagr = min_cagr
        self.max_pl = max_pl
    
    def load_stocks_from_csv(self, csv_path: str) -> List[StockData]:
        """Carrega dados do CSV"""
        df = pd.read_csv(csv_path)
        stocks = []
        for _, row in df.iterrows():
            try:
                stock = StockData(
                    ticker=row['Ticker'],
                    **{'P/L': row['P/L'], 'ROE': row['ROE'], 
                       'CAGR': row['CAGR'], 'Dívida': row['Dívida']}
                )
                if 'Setor' in row:
                    stock.setor = row['Setor']
                if 'Preço' in row:
                    stock.preco_atual = row['Preço']
                stocks.append(stock)
            except Exception as e:
                print(f"Erro ao processar {row.get('Ticker', 'unknown')}: {e}")
        return stocks
    
    def filter_elite_stocks(self, stocks: List[StockData]) -> List[StockData]:
        """Aplica os filtros fundamentalistas"""
        elite = []
        for stock in stocks:
            if (stock.roe > self.min_roe and 
                stock.cagr > self.min_cagr and 
                stock.pl < self.max_pl and
                stock.pl > 0):
                elite.append(stock)
        return elite
    
    def calculate_efficiency_score(self, stock: StockData) -> float:
        """Efficiency Score = (CAGR + ROE) / P/L"""
        if stock.pl <= 0:
            return 0
        score = (stock.cagr + stock.roe) / stock.pl
        return round(score, 2)
    
    def rank_stocks(self, stocks: List[StockData]) -> List[EfficiencyScore]:
        """Rankeia os ativos pelo Efficiency Score"""
        scored_stocks = []
        
        for stock in stocks:
            score = self.calculate_efficiency_score(stock)
            scored_stocks.append(
                EfficiencyScore(
                    ticker=stock.ticker,
                    score=score,
                    roe=stock.roe,
                    cagr=stock.cagr,
                    pl=stock.pl,
                    rank=0,
                    setor=stock.setor if hasattr(stock, 'setor') else None,
                    preco=stock.preco_atual if hasattr(stock, 'preco_atual') else None
                )
            )
        
        scored_stocks.sort(key=lambda x: x.score, reverse=True)
        
        for i, stock in enumerate(scored_stocks, 1):
            stock.rank = i
        
        return scored_stocks
    
    def process(self, csv_path: str) -> List[EfficiencyScore]:
        """Pipeline completo da Camada 1"""
        stocks = self.load_stocks_from_csv(csv_path)
        elite_stocks = self.filter_elite_stocks(stocks)
        ranked_stocks = self.rank_stocks(elite_stocks)
        return ranked_stocks
