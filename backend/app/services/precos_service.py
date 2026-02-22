"""
Serviço Unificado de Preços
Tenta Brapi primeiro, se falhar usa HG Brasil
"""
import asyncio
from typing import Dict, List
import logging

from app.services.brapi_service import BrapiService
from app.services.hgbrasil_service import get_hgbrasil_service

logger = logging.getLogger(__name__)


class PrecosService:
    """
    Serviço que busca preços de ações usando múltiplas fontes
    
    Ordem de prioridade:
    1. Brapi (mais completo, mas pode dar 401)
    2. HG Brasil (backup confiável)
    """
    
    def __init__(self):
        self.brapi = BrapiService()
        self.hgbrasil = get_hgbrasil_service()
        logger.info("✓ Serviço Unificado de Preços inicializado (Brapi + HG Brasil)")
    
    async def get_quote(self, ticker: str) -> Dict:
        """
        Busca cotação de uma ação
        Tenta Brapi primeiro, se falhar usa HG Brasil
        """
        # Tenta Brapi
        try:
            quote = await self.brapi.get_quote(ticker)
            if quote and quote.get("regularMarketPrice", 0) > 0:
                return quote
        except Exception as e:
            logger.debug(f"Brapi falhou para {ticker}: {e}")
        
        # Se Brapi falhou, tenta HG Brasil
        try:
            quote = await self.hgbrasil.get_quote(ticker)
            if quote and quote.get("regularMarketPrice", 0) > 0:
                logger.debug(f"✓ {ticker}: Usando HG Brasil (Brapi falhou)")
                return quote
        except Exception as e:
            logger.debug(f"HG Brasil falhou para {ticker}: {e}")
        
        # Se ambos falharam, retorna None
        return None
    
    async def get_multiple_quotes(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Busca cotações de múltiplas ações
        Tenta Brapi em batch, se falhar usa HG Brasil individual
        """
        results = {}
        
        # Tenta Brapi em batch (mais rápido)
        try:
            brapi_results = await self.brapi.get_multiple_quotes(tickers)
            
            # Verifica quais tickers tiveram sucesso
            for ticker, quote in brapi_results.items():
                if quote and quote.get("regularMarketPrice", 0) > 0:
                    results[ticker] = quote
            
            # Se conseguiu todos, retorna
            if len(results) == len(tickers):
                logger.info(f"✓ {len(results)}/{len(tickers)} preços obtidos (Brapi)")
                return results
            
            # Se alguns falharam, tenta HG Brasil para os que faltam
            tickers_faltando = [t for t in tickers if t not in results]
            if tickers_faltando:
                logger.info(f"⚠️ Brapi: {len(results)}/{len(tickers)} OK, tentando HG Brasil para {len(tickers_faltando)} restantes")
        
        except Exception as e:
            logger.warning(f"⚠️ Brapi falhou completamente: {e}")
            tickers_faltando = tickers
        
        # Tenta HG Brasil para os que faltam
        if tickers_faltando:
            for ticker in tickers_faltando:
                try:
                    quote = await self.hgbrasil.get_quote(ticker)
                    if quote and quote.get("regularMarketPrice", 0) > 0:
                        results[ticker] = quote
                        logger.debug(f"✓ {ticker}: HG Brasil OK")
                except Exception as e:
                    logger.debug(f"✗ {ticker}: HG Brasil falhou - {e}")
        
        total_sucesso = len(results)
        total_tentados = len(tickers)
        
        logger.info(f"✓ {total_sucesso}/{total_tentados} preços obtidos (Brapi + HG Brasil)")
        
        return results


# Singleton
_precos_service = None


def get_precos_service() -> PrecosService:
    """Retorna instância singleton"""
    global _precos_service
    
    if _precos_service is None:
        _precos_service = PrecosService()
    
    return _precos_service
