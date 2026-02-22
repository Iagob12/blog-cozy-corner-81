"""Testa Brapi COM token"""
import os
from dotenv import load_dotenv
import requests

# Carrega .env
load_dotenv()

token = os.getenv("BRAPI_TOKEN", "")
print(f"\n=== TESTE BRAPI COM TOKEN ===\n")
print(f"Token encontrado: {'Sim' if token else 'Não'}")
if token:
    print(f"Token: {token[:10]}...")

# Teste com token
ticker = "PETR4"
url = f"https://brapi.dev/api/quote/{ticker}?range=1d&interval=1d&fundamental=false"

if token:
    url += f"&token={token}"

print(f"\nURL: {url[:80]}...")

try:
    response = requests.get(url, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            preco = result.get("regularMarketPrice", 0)
            print(f"✓ {ticker}: R$ {preco:.2f}")
        else:
            print(f"✗ Sem dados na resposta")
    else:
        print(f"✗ Erro HTTP: {response.status_code}")
        print(f"Resposta: {response.text[:200]}")

except Exception as e:
    print(f"✗ Erro: {e}")
