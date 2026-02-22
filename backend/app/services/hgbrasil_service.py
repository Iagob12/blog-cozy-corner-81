"""
HG Brasil Finance API Service
API brasileira para cotações de ações B3
"""
import os
import requests
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class HGBrasilService:
    """
    Cliente para HG Brasil Finance API
    
    Documentação: https://hgbrasil.com/status/finance
    """
    
    def __init__(self):
        self.api_key = os.getenv("HGBRASIL_API_KEY", "c1d73757")
        self.base_url = "https://api.hgbrasil.com/finance"
        
        if self.api_key:
            logger.info("✓ HG Brasil Service inicializado (com key)")
        else:
            logger.warning("⚠️ HG Brasil Service inicializado SEM key (limitado)")
    
    async def get_quote(self, ticker: str) -> Optional[Dict]:
        """
        Busca cotação de uma ação
        
        Args:
            ticker: Código da ação (ex: PETR4)
        
        Returns:
            Dict com dados da cotação ou None se falhar
        """
        try:
            # Remove .SA se tiver
            ticker_clean = ticker.replace(".SA", "")
            
            # Monta URL
            url = f"{self.base_url}/stock_price"
            params = {
                "key": self.api_key,
                "symbol": ticker_clean
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verifica se tem dados
                if data.get("valid_key") and data.get("results"):
                    result = data["results"][ticker_clean]
                    
                    return {
                        "symbol": ticker_clean,
                        "regularMarketPrice": result.get("price", 0),
                        "regularMarketChange": result.get("change_percent", 0),
                        "regularMarketVolume": result.get("volume", 0),
                        "regularMarketTime": result.get("updated_at", ""),
                        "currency": "BRL",
                        "source": "hgbrasil"
                    }
                else:
                    logger.debug(f"[HGBRASIL] {ticker}: Sem dados válidos")
                    return None
            else:
                logger.debug(f"[HGBRASIL] {ticker}: Status {response.status_code}")
                return None
                
        except Exception as e:
            logger.debug(f"[HGBRASIL] {ticker}: Erro - {str(e)[:50]}")
            return None
    
    async def get_multiple_quotes(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Busca cotações de múltiplas ações
        
        HG Brasil não tem endpoint batch, então faz requisições individuais
        
        Args:
            tickers: Lista de códigos de ações
        
        Returns:
            Dict com ticker -> dados
        """
        results = {}
        
        for ticker in tickers:
            quote = await self.get_quote(ticker)
            if quote:
                results[ticker] = quote
        
        return results


# Singleton
_hgbrasil_service: Optional[HGBrasilService] = None


def get_hgbrasil_service() -> HGBrasilService:
    """Retorna instância singleton"""
    global _hgbrasil_service
    
    if _hgbrasil_service is None:
        _hgbrasil_service = HGBrasilService()
    
    return _hgbrasil_service
