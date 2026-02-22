"""
Brapi.dev Service - Sistema de Rotação Inteligente de Tokens
API gratuita para preços de ações brasileiras com múltiplos tokens
https://brapi.dev/
"""
import aiohttp
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
import asyncio
import os
from collections import deque

logger = logging.getLogger(__name__)


class BrapiService:
    """
    Serviço para buscar preços usando Brapi.dev com rotação de tokens
    
    FEATURES:
    - Rotação automática entre 9 tokens
    - Cache de 5 minutos
    - Rate limit inteligente
    - Fallback automático se um token falhar
    """
    
    def __init__(self):
        self.base_url = "https://brapi.dev/api"
        
        # Carrega todos os tokens disponíveis
        self.tokens = []
        for i in range(1, 10):  # BRAPI_TOKEN_1 até BRAPI_TOKEN_9
            token = os.getenv(f"BRAPI_TOKEN_{i}", "")
            if token:
                self.tokens.append(token)
        
        # Fila de rotação (round-robin)
        self.token_queue = deque(range(len(self.tokens)))
        
        # Estatísticas por token
        self.token_stats = {i: {"uso": 0, "erros": 0, "ultimo_uso": None} for i in range(len(self.tokens))}
        
        # Rate limit por token
        self.rate_limit_ate = {i: None for i in range(len(self.tokens))}
        
        # Cache
        self._cache = {}
        self._cache_duration = timedelta(minutes=5)
        
        if self.tokens:
            logger.info(f"OK Brapi Service: {len(self.tokens)} tokens configurados")
            print(f"OK Brapi.dev Service inicializado ({len(self.tokens)} tokens)")
        else:
            logger.warning("AVISO Brapi Service: Nenhum token configurado")
            print("AVISO Brapi.dev Service inicializado SEM tokens")
    
    def _get_next_token_index(self) -> Optional[int]:
        """Retorna próximo token disponível (round-robin)"""
        if not self.tokens:
            return None
        
        # Tenta encontrar token disponível
        for _ in range(len(self.tokens)):
            token_idx = self.token_queue[0]
            self.token_queue.rotate(-1)  # Move para o fim da fila
            
            # Verifica se está em rate limit
            if self.rate_limit_ate[token_idx]:
                if datetime.now() < self.rate_limit_ate[token_idx]:
                    continue  # Pula este token
                else:
                    self.rate_limit_ate[token_idx] = None  # Libera
            
            return token_idx
        
        # Todos em rate limit, retorna o primeiro mesmo assim
        return self.token_queue[0]
    
    def _marcar_rate_limit(self, token_idx: int, duracao_segundos: int = 60):
        """Marca token como em rate limit"""
        self.rate_limit_ate[token_idx] = datetime.now() + timedelta(seconds=duracao_segundos)
        logger.warning(f"Token {token_idx + 1} em rate limit por {duracao_segundos}s")
    
    def _is_cache_valid(self, ticker: str) -> bool:
        """Verifica se cache é válido"""
        if ticker not in self._cache:
            return False
        
        _, cached_time = self._cache[ticker]
        idade = datetime.now() - cached_time
        return idade < self._cache_duration
    
    def _get_from_cache(self, ticker: str) -> Optional[Dict]:
        """Retorna dados do cache se válido"""
        if not self._is_cache_valid(ticker):
            return None
        
        cached_data, cached_time = self._cache[ticker]
        idade_segundos = (datetime.now() - cached_time).total_seconds()
        
        result = cached_data.copy()
        result["fonte"] = "cache"
        result["cache_idade_segundos"] = int(idade_segundos)
        
        return result
    
    async def get_quote(self, ticker: str) -> Optional[Dict]:
        """Busca cotação de uma ação com rotação de tokens"""
        
        # Verifica cache
        cached = self._get_from_cache(ticker)
        if cached:
            return cached
        
        # Tenta com múltiplos tokens se necessário
        for tentativa in range(min(3, len(self.tokens))):
            token_idx = self._get_next_token_index()
            if token_idx is None:
                logger.error("Nenhum token Brapi disponível")
                return None
            
            try:
                token = self.tokens[token_idx]
                url = f"{self.base_url}/quote/{ticker}?range=1d&interval=1d&fundamental=false&token={token}"
                
                timeout = aiohttp.ClientTimeout(total=10)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    
                    async with session.get(url, headers=headers) as response:
                        # Atualiza estatísticas
                        self.token_stats[token_idx]["uso"] += 1
                        self.token_stats[token_idx]["ultimo_uso"] = datetime.now()
                        
                        if response.status == 429:  # Rate limit
                            self._marcar_rate_limit(token_idx)
                            logger.warning(f"Token {token_idx + 1} em rate limit, tentando próximo...")
                            continue
                        
                        if response.status != 200:
                            self.token_stats[token_idx]["erros"] += 1
                            logger.warning(f"Token {token_idx + 1}: {ticker} Status {response.status}")
                            continue
                        
                        data = await response.json()
                        
                        if "results" not in data or len(data["results"]) == 0:
                            continue
                        
                        result = data["results"][0]
                        
                        quote_data = {
                            "ticker": ticker,
                            "regularMarketPrice": result.get("regularMarketPrice", 0),
                            "regularMarketChangePercent": result.get("regularMarketChangePercent", 0),
                            "regularMarketVolume": result.get("regularMarketVolume", 0),
                            "timestamp": datetime.now(),
                            "fonte": f"brapi_token_{token_idx + 1}"
                        }
                        
                        self._cache[ticker] = (quote_data, datetime.now())
                        
                        print(f"OK {ticker}: R$ {quote_data['regularMarketPrice']:.2f} (Brapi T{token_idx + 1})")
                        
                        return quote_data
            
            except Exception as e:
                self.token_stats[token_idx]["erros"] += 1
                logger.error(f"Token {token_idx + 1}: {ticker} Erro - {e}")
                continue
        
        logger.error(f"{ticker}: Falhou com todos os tokens")
        return None
    
    async def get_multiple_quotes(self, tickers: List[str]) -> Dict[str, Dict]:
        """Busca cotações de múltiplos tickers com rotação automática"""
        
        print(f"\n[BRAPI] Buscando preços de {len(tickers)} ações ({len(self.tokens)} tokens)...")
        
        quotes = {}
        cache_hits = 0
        api_calls = 0
        
        for ticker in tickers:
            if self._is_cache_valid(ticker):
                cached = self._get_from_cache(ticker)
                if cached:
                    quotes[ticker] = cached
                    cache_hits += 1
                    continue
            
            quote = await self.get_quote(ticker)
            if quote:
                quotes[ticker] = quote
                api_calls += 1
            
            # Delay menor com múltiplos tokens
            await asyncio.sleep(0.1)
        
        total = len(quotes)
        print(f"OK {total}/{len(tickers)} preços obtidos ({cache_hits} cache, {api_calls} API)")
        
        # Log de estatísticas
        self._log_stats()
        
        return quotes
    
    def _log_stats(self):
        """Log de estatísticas de uso dos tokens"""
        total_uso = sum(s["uso"] for s in self.token_stats.values())
        if total_uso > 0:
            logger.info(f"Brapi Stats: {total_uso} requisições distribuídas entre {len(self.tokens)} tokens")
    
    async def obter_precos_batch(self, tickers: List[str]) -> Dict[str, float]:
        """
        Busca preços de múltiplos tickers (alias para compatibilidade)
        Retorna dict {ticker: preco}
        """
        quotes = await self.get_multiple_quotes(tickers)
        
        # Converte para formato simples {ticker: preco}
        precos = {}
        for ticker, quote in quotes.items():
            if quote and 'regularMarketPrice' in quote:
                precos[ticker] = quote['regularMarketPrice']
        
        return precos
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas de uso dos tokens"""
        return {
            "total_tokens": len(self.tokens),
            "tokens_ativos": sum(1 for i, limite in self.rate_limit_ate.items() 
                                if limite is None or datetime.now() >= limite),
            "estatisticas": self.token_stats
        }

    
    async def get_quote_with_fundamentals(
        self, 
        ticker: str,
        modules: List[str] = None
    ) -> Optional[Dict]:
        """
        Busca cotação com dados fundamentalistas usando módulos da Brapi
        
        Args:
            ticker: Ticker da ação
            modules: Lista de módulos a incluir. Padrão: dados essenciais
        
        Módulos disponíveis:
        - summaryProfile: Perfil da empresa
        - defaultKeyStatistics: Estatísticas principais (P/L, ROE, etc)
        - financialData: Dados financeiros TTM
        - incomeStatementHistoryQuarterly: DRE trimestral
        - balanceSheetHistoryQuarterly: Balanço trimestral
        """
        if modules is None:
            # Módulos padrão: dados essenciais para análise
            modules = [
                "summaryProfile",
                "defaultKeyStatistics", 
                "financialData"
            ]
        
        # Tenta com múltiplos tokens se necessário
        for tentativa in range(min(3, len(self.tokens))):
            token_idx = self._get_next_token_index()
            if token_idx is None:
                logger.error("Nenhum token Brapi disponível")
                return None
            
            try:
                token = self.tokens[token_idx]
                modules_str = ",".join(modules)
                url = f"{self.base_url}/quote/{ticker}?modules={modules_str}&fundamental=true&token={token}"
                
                timeout = aiohttp.ClientTimeout(total=15)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    
                    async with session.get(url, headers=headers) as response:
                        # Atualiza estatísticas
                        self.token_stats[token_idx]["uso"] += 1
                        self.token_stats[token_idx]["ultimo_uso"] = datetime.now()
                        
                        if response.status == 429:  # Rate limit
                            self._marcar_rate_limit(token_idx)
                            logger.warning(f"Token {token_idx + 1} em rate limit, tentando próximo...")
                            continue
                        
                        if response.status != 200:
                            self.token_stats[token_idx]["erros"] += 1
                            logger.warning(f"Token {token_idx + 1}: {ticker} Status {response.status}")
                            continue
                        
                        data = await response.json()
                        
                        if "results" not in data or len(data["results"]) == 0:
                            continue
                        
                        result = data["results"][0]
                        
                        print(f"OK {ticker}: Dados fundamentalistas obtidos (Brapi T{token_idx + 1})")
                        
                        return result
            
            except Exception as e:
                self.token_stats[token_idx]["erros"] += 1
                logger.error(f"Token {token_idx + 1}: {ticker} Erro - {e}")
                continue
        
        logger.error(f"{ticker}: Falhou com todos os tokens (fundamentals)")
        return None
    
    async def get_multiple_quotes_with_fundamentals(
        self,
        tickers: List[str],
        modules: List[str] = None
    ) -> Dict[str, Dict]:
        """
        Busca cotações com dados fundamentalistas para múltiplos tickers
        
        Nota: Faz requisições individuais pois a API não suporta batch com módulos
        """
        print(f"\n[BRAPI] Buscando dados fundamentalistas de {len(tickers)} ações...")
        
        results = {}
        
        for ticker in tickers:
            data = await self.get_quote_with_fundamentals(ticker, modules)
            if data:
                results[ticker] = data
            
            # Delay menor com múltiplos tokens
            await asyncio.sleep(0.15)
        
        total = len(results)
        print(f"OK {total}/{len(tickers)} dados fundamentalistas obtidos")
        
        return results
