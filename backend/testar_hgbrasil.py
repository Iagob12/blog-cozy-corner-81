"""
Teste rápido do HG Brasil
"""
import asyncio
from app.services.hgbrasil_service import get_hgbrasil_service

async def main():
    print("="*70)
    print("  TESTANDO HG BRASIL")
    print("="*70)
    print()
    
    hg = get_hgbrasil_service()
    
    # Testa algumas ações
    tickers = ["PETR4", "VALE3", "ITUB4", "BBDC4", "ABEV3"]
    
    print(f"Testando {len(tickers)} ações...")
    print()
    
    for ticker in tickers:
        quote = await hg.get_quote(ticker)
        if quote:
            preco = quote.get("regularMarketPrice", 0)
            print(f"✓ {ticker}: R$ {preco:.2f}")
        else:
            print(f"✗ {ticker}: Falhou")
    
    print()
    print("="*70)

if __name__ == "__main__":
    asyncio.run(main())
