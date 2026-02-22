"""
Teste do que está disponível no plano FREE do HG Brasil
"""
import requests

API_KEY = "c1d73757"

def test_free_endpoints():
    """Testa endpoints disponíveis no plano free"""
    print("\n=== TESTE HG BRASIL - PLANO FREE ===\n")
    
    # Teste 1: Finance geral (sem ticker específico)
    print("1. Testando endpoint finance geral...")
    url = "https://api.hgbrasil.com/finance"
    params = {"key": API_KEY}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Campos disponíveis: {list(data.keys())}")
            
            # Verifica se tem dados de ações
            if "results" in data:
                results = data["results"]
                print(f"   Results keys: {list(results.keys())}")
                
                # Verifica stocks
                if "stocks" in results:
                    stocks = results["stocks"]
                    print(f"\n   ✓ Ações disponíveis:")
                    print(f"     Tipo: {type(stocks)}")
                    
                    if isinstance(stocks, dict):
                        # É um dicionário
                        for symbol, data in stocks.items():
                            print(f"     - {symbol}: {data}")
                    elif isinstance(stocks, list):
                        # É uma lista
                        for stock in stocks:
                            print(f"     - {stock}")
                
                # Verifica currencies
                if "currencies" in results:
                    currencies = results["currencies"]
                    print(f"\n   ✓ Moedas disponíveis:")
                    for curr_key, curr_data in currencies.items():
                        if isinstance(curr_data, dict):
                            print(f"     - {curr_key}: {curr_data.get('buy', 0):.2f}")
                
                # Verifica bitcoin
                if "bitcoin" in results:
                    bitcoin = results["bitcoin"]
                    print(f"\n   ✓ Bitcoin:")
                    for market, data in bitcoin.items():
                        if isinstance(data, dict):
                            print(f"     - {market}: R$ {data.get('last', 0):,.2f}")
        else:
            print(f"   ✗ Erro HTTP: {response.status_code}")
            print(f"   Resposta: {response.text[:500]}")
    
    except Exception as e:
        print(f"   ✗ Erro: {e}")

if __name__ == "__main__":
    test_free_endpoints()
