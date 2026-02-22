"""
Teste da API dadosdemercado.com.br
Verifica quais dados estão disponíveis
"""
import requests
from bs4 import BeautifulSoup

def test_dadosdemercado():
    """Testa acesso ao site e verifica dados disponíveis"""
    print("\n=== TESTE DADOS DE MERCADO ===\n")
    
    # Teste 1: Página principal
    print("1. Testando acesso ao site...")
    try:
        response = requests.get("https://www.dadosdemercado.com.br", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✓ Site acessível")
            
            # Verifica se tem API ou dados estruturados
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Procura por links de API ou dados
            links = soup.find_all('a', href=True)
            api_links = [link['href'] for link in links if 'api' in link['href'].lower()]
            
            if api_links:
                print(f"\n   Links de API encontrados:")
                for link in api_links[:5]:
                    print(f"     - {link}")
        else:
            print(f"   ✗ Erro HTTP: {response.status_code}")
    
    except Exception as e:
        print(f"   ✗ Erro: {e}")
    
    # Teste 2: Tenta acessar dados de ações específicas
    print("\n2. Testando acesso a dados de ações...")
    tickers = ["PETR4", "VALE3", "ITUB4"]
    
    for ticker in tickers:
        try:
            # Tenta diferentes URLs possíveis
            urls = [
                f"https://www.dadosdemercado.com.br/acoes/{ticker}",
                f"https://www.dadosdemercado.com.br/bolsa/{ticker}",
                f"https://www.dadosdemercado.com.br/api/acoes/{ticker}",
            ]
            
            for url in urls:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✓ {ticker}: {url} - Acessível")
                    
                    # Verifica se tem dados JSON
                    try:
                        data = response.json()
                        print(f"      Dados JSON disponíveis: {list(data.keys())[:5]}")
                    except:
                        print(f"      HTML (não é JSON)")
                    break
            else:
                print(f"   ✗ {ticker}: Nenhuma URL funcionou")
        
        except Exception as e:
            print(f"   ✗ {ticker}: Erro - {str(e)[:50]}")

if __name__ == "__main__":
    test_dadosdemercado()
