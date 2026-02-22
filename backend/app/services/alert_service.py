from typing import Dict
from app.models import PriceAlert, EfficiencyScore

class AlertService:
    """Sistema de Alertas de Preço"""
    
    def __init__(self, margem_seguranca: float = 0.15):
        self.margem_seguranca = margem_seguranca
    
    def calculate_fair_value(self, efficiency_score: EfficiencyScore, 
                            preco_atual: float) -> float:
        """Calcula o valor justo"""
        multiplier = 1 + (efficiency_score.score / 20)
        fair_value = preco_atual * multiplier
        return round(fair_value, 2)
    
    def calculate_ceiling_price(self, fair_value: float, 
                                target_return: float = 0.05) -> float:
        """Calcula o preço teto"""
        ceiling = fair_value / (1 + target_return + self.margem_seguranca)
        return round(ceiling, 2)
    
    def generate_recommendation(self, preco_atual: float, 
                               preco_teto: float) -> tuple:
        """Gera recomendação"""
        ratio = preco_atual / preco_teto
        
        if ratio <= 0.95:
            return "COMPRAR", "Preço abaixo do teto."
        elif ratio <= 1.05:
            return "AGUARDAR", "Preço próximo ao teto."
        else:
            upside = ((preco_teto / preco_atual) - 1) * 100
            if upside < -10:
                return "VENDER", "Preço muito acima do teto."
            else:
                return "AGUARDAR", "Preço acima do teto."
    
    def create_alert(self, ticker: str, preco_atual: float, 
                    efficiency_score: EfficiencyScore,
                    target_return: float = 0.05) -> PriceAlert:
        """Cria alerta de preço"""
        fair_value = self.calculate_fair_value(efficiency_score, preco_atual)
        preco_teto = self.calculate_ceiling_price(fair_value, target_return)
        
        margem = round(((preco_teto / preco_atual) - 1) * 100, 2)
        acao, _ = self.generate_recommendation(preco_atual, preco_teto)
        
        return PriceAlert(
            ticker=ticker,
            preco_atual=preco_atual,
            preco_teto=preco_teto,
            margem_seguranca=margem,
            acao_recomendada=acao
        )
    
    async def monitor_prices(self, tickers: Dict[str, float], 
                           efficiency_scores: Dict[str, EfficiencyScore]) -> list:
        """Monitora múltiplos ativos"""
        alerts = []
        
        for ticker, preco_atual in tickers.items():
            if ticker in efficiency_scores:
                alert = self.create_alert(
                    ticker, 
                    preco_atual, 
                    efficiency_scores[ticker]
                )
                alerts.append(alert)
        
        return alerts
