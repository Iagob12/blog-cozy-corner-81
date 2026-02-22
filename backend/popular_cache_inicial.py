"""
Script para popular cache inicial com dados simulados
Útil para testes rápidos sem esperar API
"""
import asyncio
from datetime import datetime
from app.services.market_data import MarketDataService

async def popular_cache():
    print("=" * 60)
    print("POPULANDO CACHE INICIAL")
    print("=" * 60)
    
    service = MarketDataService()
    
    # Dados simulados baseados em preços reais aproximados
    dados_simulados = {
        "PRIO3": 48.50,
        "VULC3": 12.30,
        "GMAT3": 8.90,
        "CURY3": 15.20,
        "POMO3": 3.45,
        "WEGE3": 45.80,
        "RENT3": 65.30,
        "RAIL3": 18.90,
        "RADL3": 28.70,
        "SUZB3": 52.30,
        "PETR4": 37.19,
        "VALE3": 62.45,
        "ITUB4": 28.90,
        "BBDC4": 14.50,
        "ABEV3": 11.80,
    }
    
    print(f"\nAdicionando {len(dados_simulados)} ações ao cache...")
    
    for ticker, preco in dados_simulados.items():
        cache_data = {
            "ticker": ticker,
            "preco_atual": preco,
            "variacao_dia": 0.5,  # Simulado
            "volume": 1000000,
            "timestamp": datetime.now().isoformat(),
            "fonte": "Cache Inicial (Simulado)"
        }
        
        service._cache[ticker] = (cache_data, datetime.now())
        print(f"✓ {ticker}: R$ {preco:.2f}")
    
    print(f"\n✓ Cache populado com {len(service._cache)} ações")
    print("✓ Válido por 30 minutos")
    print("\nAgora o sistema vai responder instantaneamente!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(popular_cache())
