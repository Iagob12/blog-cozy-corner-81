"""
Teste REAL da API HG Brasil
Testa endpoint correto e formato de resposta
"""
import requests
import asyncio

API_KEY = "c1d73757"

def test_hgbrasil_sync():
    """Teste síncrono para debug"""
    print("\n=== TESTE HG BRASIL API ===\n")
    
    # Teste 1: Endpoint de cotações múltiplas
    print("1. Testando endpoint de cotações...")
    url = "https://api.hgbrasil.com/finance/stock_price"
    
    # Testa com um ticker
    ticker = "PETR4"
    params = {
        "key": API_KEY,
        "symbol": ticker
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Resposta: {data}")
            
            # Verifica estrutura
            if "results" in data:
                if ticker in data["results"]:
                    result = data["results"][ticker]
                    print(f"\n   ✓ {ticker}:")
                    print(f"     - Preço: R$ {result.get('price', 0):.2f}")
                    print(f"     - Variação: {result.get('change_percent', 0):.2f}%")
                    print(f"     - Volume: {result.get('volume', 0):,}")
                else:
                    print(f"   ✗ Ticker {ticker} não encontrado na resposta")
            else:
                print(f"   ✗ Resposta sem campo 'results'")
        else:
            print(f"   ✗ Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
    
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 2: Múltiplos tickers
    print("\n2. Testando múltiplos tickers...")
    tickers = ["PETR4", "VALE3", "ITUB4"]
    
    for ticker in tickers:
        params = {
            "key": API_KEY,
            "symbol": ticker
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "results" in data and ticker in data["results"]:
                    result = data["results"][ticker]
                    preco = result.get("price", 0)
                    print(f"   ✓ {ticker}: R$ {preco:.2f}")
                else:
                    print(f"   ✗ {ticker}: Sem dados")
            else:
                print(f"   ✗ {ticker}: HTTP {response.status_code}")
        
        except Exception as e:
            print(f"   ✗ {ticker}: {e}")

if __name__ == "__main__":
    test_hgbrasil_sync()
