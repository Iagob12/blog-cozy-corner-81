"""
Cliente yfinance com rate limit control e retry
"""
import asyncio
from typing import Optional, Dict
from datetime import datetime, timedelta
import yfinance as yf
import logging

logger = logging.getLogger(__name__)


class YFinanceClient:
    """
    Cliente yfinance com:
    - Rate limit control
    - Retry com backoff exponencial
    - Cache de resultados
    - Circuit breaker
    """
    
    def __init__(self):
        self.cache = {}  # Cache de resultados
        self.cache_duration = timedelta(hours=1)  # Cache válido por 1 hora
        
        self.ultimo_request = None
        self.delay_entre_requests = 5.0  # 5 segundos entre requests (aumentado)
        
        self.max_retries = 3
        self.retry_delay_base = 10  # 10 segundos base (aumentado)
        
        self.rate_limit_ate = None
        self.rate_limit_duracao = 300  # 5 minutos
        
        logger.info("✓ yfinance Client: rate limit control + cache (ULTRA conservador)")
    
    def _em_rate_limit(self) -> bool:
        """Verifica se está em rate limit"""
        if self.rate_limit_ate is None:
            return False
        
        if datetime.now() >= self.rate_limit_ate:
            self.rate_limit_ate = None
            logger.info("✓ yfinance liberado do rate limit")
            return False
        
        return True
    
    def _marcar_rate_limit(self):
        """Marca como em rate limit"""
        self.rate_limit_ate = datetime.now() + timedelta(seconds=self.rate_limit_duracao)
        logger.warning(f"⚠ yfinance em rate limit até {self.rate_limit_ate.strftime('%H:%M:%S')}")
    
    def _obter_do_cache(self, ticker: str) -> Optional[Dict]:
        """Obtém dados do cache se válidos"""
        if ticker not in self.cache:
            return None
        
        dados, timestamp = self.cache[ticker]
        
        if datetime.now() - timestamp < self.cache_duration:
            logger.debug(f"✓ {ticker}: Usando cache")
            return dados
        
        # Cache expirado
        del self.cache[ticker]
        return None
    
    def _salvar_no_cache(self, ticker: str, dados: Dict):
        """Salva dados no cache"""
        self.cache[ticker] = (dados, datetime.now())
    
    async def obter_dados(self, ticker: str) -> Optional[Dict]:
        """
        Obtém dados do yfinance com rate limit control
        
        Returns:
            Dict com dados ou None se falhar
        """
        
        # Verifica cache
        dados_cache = self._obter_do_cache(ticker)
        if dados_cache:
            return dados_cache
        
        # Verifica rate limit
        if self._em_rate_limit():
            tempo_restante = (self.rate_limit_ate - datetime.now()).seconds
            logger.debug(f"yfinance em rate limit, aguardando {tempo_restante}s...")
            await asyncio.sleep(min(tempo_restante, 30))  # Aguarda no máximo 30s
            
            if self._em_rate_limit():
                logger.warning(f"⚠ {ticker}: yfinance ainda em rate limit, pulando")
                return None
        
        # Delay entre requests
        if self.ultimo_request:
            tempo_desde_ultimo = (datetime.now() - self.ultimo_request).total_seconds()
            if tempo_desde_ultimo < self.delay_entre_requests:
                await asyncio.sleep(self.delay_entre_requests - tempo_desde_ultimo)
        
        # Retry com backoff exponencial
        for tentativa in range(self.max_retries):
            try:
                # Executa em thread separada (yfinance é síncrono)
                loop = asyncio.get_event_loop()
                ticker_yf = f"{ticker}.SA"
                stock = await loop.run_in_executor(None, yf.Ticker, ticker_yf)
                
                # Obtém dados
                info = stock.info
                financials = stock.quarterly_financials
                
                # Atualiza timestamp
                self.ultimo_request = datetime.now()
                
                # Prepara dados
                dados = {
                    "info": info,
                    "financials": financials
                }
                
                # Salva no cache
                self._salvar_no_cache(ticker, dados)
                
                return dados
            
            except Exception as e:
                error_str = str(e)
                
                # Detecta rate limit
                if "429" in error_str or "Too Many Requests" in error_str:
                    self._marcar_rate_limit()
                    logger.warning(f"⚠ {ticker}: yfinance rate limit detectado")
                    
                    if tentativa < self.max_retries - 1:
                        delay = self.retry_delay_base * (2 ** tentativa)
                        logger.debug(f"Retry {tentativa + 1}/{self.max_retries} em {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        return None
                else:
                    logger.debug(f"⚠ {ticker}: yfinance erro - {str(e)[:50]}")
                    return None
        
        return None


# Singleton
_yfinance_client: Optional[YFinanceClient] = None


def get_yfinance_client() -> YFinanceClient:
    """Retorna instância singleton"""
    global _yfinance_client
    
    if _yfinance_client is None:
        _yfinance_client = YFinanceClient()
    
    return _yfinance_client
