"""
Teste da API dadosdemercado.com.br
Explora endpoints disponíveis
"""
import requests

def test_api():
    """Testa API"""
    print("\n=== TESTE API DADOS DE MERCADO ===\n")
    
    # Teste 1: Documentação da API
    print("1. Acessando documentação da API...")
    try:
        response = requests.get("https://www.dadosdemercado.com.br/api/docs", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✓ Documentação acessível")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            
            # Salva HTML para análise
            with open('dadosdemercado_api_docs.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"   ✓ Documentação salva em dadosdemercado_api_docs.html")
    
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 2: Tenta endpoints comuns de APIs financeiras
    print("\n2. Testando endpoints comuns...")
    
    endpoints = [
        "/api/tickers",
        "/api/acoes",
        "/api/cotacoes",
        "/api/quotes",
        "/api/stocks",
        "/api/v1/tickers",
        "/api/v1/acoes",
        "/api/acoes/PETR4",
        "/api/tickers/PETR4",
        "/api/quotes/PETR4",
    ]
    
    for endpoint in endpoints:
        try:
            url = f"https://www.dadosdemercado.com.br{endpoint}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"   ✓ {endpoint}")
                
                # Tenta parsear JSON
                try:
                    data = response.json()
                    print(f"      JSON: {str(data)[:100]}...")
                except:
                    print(f"      HTML/Texto: {response.text[:100]}...")
            elif response.status_code == 404:
                print(f"   ✗ {endpoint} - 404")
            else:
                print(f"   ? {endpoint} - Status {response.status_code}")
        
        except Exception as e:
            print(f"   ✗ {endpoint} - Erro: {str(e)[:30]}")

if __name__ == "__main__":
    test_api()
