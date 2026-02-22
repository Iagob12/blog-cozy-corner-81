import requests
import json

# Testa login
url = "http://localhost:8000/api/v1/admin/login"
payload = {"password": "a1e2i3o4u5"}

print("🔐 Testando login admin...")
print(f"URL: {url}")
print(f"Senha: {payload['password']}")

try:
    response = requests.post(url, json=payload)
    print(f"\n📊 Status: {response.status_code}")
    print(f"📄 Resposta: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ LOGIN OK!")
        print(f"Token: {data.get('token', 'N/A')[:20]}...")
    else:
        print(f"\n❌ LOGIN FALHOU!")
        
except Exception as e:
    print(f"\n❌ ERRO: {e}")
