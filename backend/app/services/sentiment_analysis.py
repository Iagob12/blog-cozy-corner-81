from app.models import SentimentAlert

class SentimentAnalyzer:
    """Módulo Anti-Manada"""
    
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.historical_data = {}
    
    async def fetch_mentions_count(self, ticker: str) -> int:
        """Busca quantidade de menções"""
        import random
        base_mentions = 50
        variation = random.randint(-20, 200)
        return base_mentions + variation
    
    def get_historical_average(self, ticker: str) -> float:
        """Retorna a média histórica de menções"""
        if ticker not in self.historical_data:
            self.historical_data[ticker] = 50.0
        return self.historical_data[ticker]
    
    def update_historical_data(self, ticker: str, current_mentions: int):
        """Atualiza média móvel"""
        if ticker not in self.historical_data:
            self.historical_data[ticker] = float(current_mentions)
        else:
            alpha = 0.1
            self.historical_data[ticker] = (alpha * current_mentions + 
                                           (1 - alpha) * self.historical_data[ticker])
    
    def calculate_risk_level(self, ratio: float) -> tuple:
        """Calcula nível de risco"""
        if ratio >= self.threshold:
            return True, "ALERTA: Possível distribuição. Considere realizar lucros."
        elif ratio >= self.threshold * 0.7:
            return False, "ATENÇÃO: Volume acima do normal. Monitore."
        else:
            return False, "Normal: Volume dentro da média."
    
    async def analyze(self, ticker: str) -> SentimentAlert:
        """Pipeline completo de análise de sentimento"""
        current_mentions = await self.fetch_mentions_count(ticker)
        historical_avg = self.get_historical_average(ticker)
        
        ratio = current_mentions / historical_avg if historical_avg > 0 else 1.0
        risco_manada, recomendacao = self.calculate_risk_level(ratio)
        
        self.update_historical_data(ticker, current_mentions)
        
        return SentimentAlert(
            ticker=ticker,
            volume_mencoes=current_mentions,
            media_historica=historical_avg,
            ratio=round(ratio, 2),
            risco_manada=risco_manada,
            recomendacao=recomendacao
        )
