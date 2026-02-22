"""
Market Data Service
Busca dados reais usando Alpha Vantage API
"""
import aiohttp
from typing import Dict, List
from datetime import datetime, timedelta
import os

class MarketDataService:
    """Serviço para buscar dados de mercado usando Alpha Vantage"""
    
    def __init__(self):
        # Alpha Vantage API Keys (múltiplas para aumentar limite)
        self.api_keys = []
        
        # Carrega todas as 3 chaves disponíveis
        key1 = os.getenv("ALPHAVANTAGE_API_KEY")
        key2 = os.getenv("ALPHAVANTAGE_API_KEY_2")
        key3 = os.getenv("ALPHAVANTAGE_API_KEY_3")
        
        if key1 and key1 != "demo":
            self.api_keys.append(key1)
        if key2 and key2 != "demo":
            self.api_keys.append(key2)
        if key3 and key3 != "demo":
            self.api_keys.append(key3)
        
        if not self.api_keys:
            self.api_keys = ["demo"]
        
        self.current_key_index = 0
        self.base_url = "https://www.alphavantage.co/query"
        self._cache = {}
        self._cache_duration = timedelta(minutes=30)  # Cache mais longo (30 min)
        
        print(f"✓ Alpha Vantage: {len(self.api_keys)} chave(s) configurada(s)")
    
    def _get_next_api_key(self) -> str:
        """Retorna a próxima chave API (rotação)"""
        key = self.api_keys[self.current_key_index]
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key
    
    def _convert_ticker_to_alphavantage(self, ticker: str) -> str:
        """Converte ticker brasileiro para formato Alpha Vantage"""
        # Alpha Vantage usa formato: TICKER.SAO para B3
        if not ticker.endswith('.SAO'):
            # Remove números e adiciona .SAO
            base_ticker = ''.join([c for c in ticker if not c.isdigit()])
            return f"{base_ticker}.SAO"
        return ticker
    
    async def get_quote(self, ticker: str) -> Dict:
        """
        Busca cotação usando Alpha Vantage
        Endpoint: GLOBAL_QUOTE
        """
        # Verifica cache
        if ticker in self._cache:
            cached_data, cached_time = self._cache[ticker]
            if datetime.now() - cached_time < self._cache_duration:
                print(f"[CACHE] {ticker}: R$ {cached_data['preco_atual']:.2f}")
                cached_data["fonte"] = "cache"  # Marca como cache
                return cached_data
        
        try:
            av_ticker = self._convert_ticker_to_alphavantage(ticker)
            
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": av_ticker,
                "apikey": self._get_next_api_key()  # Usa rotação de chaves
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Alpha Vantage retorna em "Global Quote"
                        quote_data = data.get("Global Quote", {})
                        
                        if quote_data:
                            preco = float(quote_data.get("05. price", 0))
                            variacao = float(quote_data.get("10. change percent", "0").replace("%", ""))
                            volume = int(quote_data.get("06. volume", 0))
                            
                            if preco > 0:
                                result = {
                                    "ticker": ticker,
                                    "preco_atual": preco,
                                    "variacao_dia": variacao,
                                    "volume": volume,
                                    "timestamp": datetime.now().isoformat(),
                                    "fonte": "Alpha Vantage"
                                }
                                
                                # Salva no cache
                                self._cache[ticker] = (result, datetime.now())
                                print(f"✓ {ticker}: R$ {preco:.2f} (Alpha Vantage)")
                                return result
        except Exception as e:
            print(f"Alpha Vantage erro para {ticker}: {e}")
        
        return None
    
    async def get_multiple_quotes(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Busca cotações de múltiplos tickers com rotação de chaves
        Com 3 chaves: 15 requisições/minuto (5 por chave)
        OTIMIZADO: Usa cache agressivo e delay reduzido
        """
        num_keys = len(self.api_keys)
        max_requests = num_keys * 5  # 5 req/min por chave
        
        print(f"\n[ALPHA VANTAGE] Buscando preços reais de {len(tickers)} ações...")
        print(f"✓ {num_keys} chave(s) disponível(is) = {max_requests} req/min")
        
        quotes = {}
        requisicoes_feitas = 0
        
        # Processa todas as ações com rotação de chaves
        for i, ticker in enumerate(tickers, 1):
            quote = await self.get_quote(ticker)
            if quote:
                quotes[ticker] = quote
                # Só conta requisição se não veio do cache
                if quote.get("fonte") != "cache":
                    requisicoes_feitas += 1
            
            # Delay APENAS se não veio do cache e não é a última
            if i < len(tickers) and quote and quote.get("fonte") != "cache":
                # Delay reduzido: 3 segundos (mais rápido)
                delay = 3
                print(f"⏳ Aguardando {delay}s...")
                import asyncio
                await asyncio.sleep(delay)
        
        print(f"✓ {len(quotes)}/{len(tickers)} preços obtidos ({requisicoes_feitas} novas requisições)")
        return quotes
    
    async def get_intraday_data(self, ticker: str, interval: str = "5min") -> Dict:
        """
        Busca dados intraday para gráficos
        Intervalos: 1min, 5min, 15min, 30min, 60min
        """
        try:
            av_ticker = self._convert_ticker_to_alphavantage(ticker)
            
            params = {
                "function": "TIME_SERIES_INTRADAY",
                "symbol": av_ticker,
                "interval": interval,
                "apikey": self._get_next_api_key(),  # Usa rotação de chaves
                "outputsize": "compact"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        time_series_key = f"Time Series ({interval})"
                        time_series = data.get(time_series_key, {})
                        
                        if time_series:
                            # Converte para formato mais simples
                            prices = []
                            for timestamp, values in list(time_series.items())[:20]:
                                prices.append({
                                    "timestamp": timestamp,
                                    "open": float(values.get("1. open", 0)),
                                    "high": float(values.get("2. high", 0)),
                                    "low": float(values.get("3. low", 0)),
                                    "close": float(values.get("4. close", 0)),
                                    "volume": int(values.get("5. volume", 0))
                                })
                            
                            return {
                                "ticker": ticker,
                                "interval": interval,
                                "data": prices
                            }
        except Exception as e:
            print(f"Erro ao buscar intraday de {ticker}: {e}")
        
        return {}
    
    async def get_market_overview(self) -> Dict:
        """
        Visão geral do mercado
        Alpha Vantage não tem Ibovespa direto, usa dados simulados
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "ibovespa": {
                "pontos": 125000,
                "variacao_pct": 0.5
            },
            "dolar": {
                "cotacao": 5.15,
                "variacao_pct": -0.3
            },
            "fonte": "Simulado (Alpha Vantage não tem IBOV)"
        }
    
    async def calculate_momentum(self, ticker: str) -> Dict:
        """Calcula indicadores de momentum"""
        quote = await self.get_quote(ticker)
        
        if quote and quote.get("preco_atual", 0) > 0:
            variacao = quote.get("variacao_dia", 0)
            
            if variacao > 3:
                momentum = "FORTE_ALTA"
            elif variacao > 1:
                momentum = "ALTA"
            elif variacao > -1:
                momentum = "NEUTRO"
            elif variacao > -3:
                momentum = "BAIXA"
            else:
                momentum = "FORTE_BAIXA"
            
            return {
                "ticker": ticker,
                "momentum": momentum,
                "variacao_dia": variacao,
                "timestamp": datetime.now().isoformat()
            }
        
        return {"ticker": ticker, "momentum": "DESCONHECIDO", "variacao_dia": 0}
    
    async def validar_preco(self, ticker: str, preco: float) -> bool:
        """Valida se um preço é real e razoável"""
        if preco <= 0:
            return False
        if preco > 10000:
            return False
        return True
