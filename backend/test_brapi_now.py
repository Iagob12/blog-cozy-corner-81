"""
Teste Brapi AGORA - verifica se está funcionando
"""
import asyncio
from app.services.brapi_service import BrapiService

async def test_brapi():
    """Testa Brapi com alguns tickers"""
    print("\n=== TESTE BRAPI ===\n")
    
    brapi = BrapiService()
    
    # Teste 1: Um ticker
    print("1. Testando um ticker (PETR4)...")
    try:
        quote = await brapi.get_quote("PETR4")
        if quote:
            print(f"   ✓ PETR4: R$ {quote.get('regularMarketPrice', 0):.2f}")
        else:
            print(f"   ✗ PETR4: Sem dados")
    except Exception as e:
        print(f"   ✗ PETR4: Erro - {e}")
    
    # Teste 2: Múltiplos tickers
    print("\n2. Testando múltiplos tickers...")
    tickers = ["PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3"]
    
    try:
        quotes = await brapi.get_multiple_quotes(tickers)
        print(f"   Total obtidos: {len(quotes)}/{len(tickers)}")
        
        for ticker in tickers:
            quote = quotes.get(ticker)
            if quote:
                preco = quote.get("regularMarketPrice", 0)
                print(f"   ✓ {ticker}: R$ {preco:.2f}")
            else:
                print(f"   ✗ {ticker}: Sem dados")
    except Exception as e:
        print(f"   ✗ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_brapi())
