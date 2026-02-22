"""
Teste da CometAPI - Descobrir modelos disponíveis
"""
import requests
import json

API_KEY = "sk-vFa83qttcUit84rdkZp5Ptbidi1CfXrNs45yoiuurINuk6W9"

print("\n" + "="*60)
print("🧪 TESTANDO COMETAPI")
print("="*60)

# Testa diferentes endpoints possíveis
endpoints = [
    "https://api.cometapi.com/v1/models",
    "https://api.cometapi.com/models",
    "https://cometapi.com/v1/models",
    "https://api.comet.com/v1/models"
]

print("\n1️⃣ Tentando descobrir endpoint de modelos...\n")

for endpoint in endpoints:
    try:
        print(f"Testando: {endpoint}")
        response = requests.get(
            endpoint,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"✅ ENCONTRADO! Status: {response.status_code}")
            data = response.json()
            print(f"Resposta: {json.dumps(data, indent=2)[:500]}")
            break
        else:
            print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   Erro: {str(e)[:100]}")

print("\n2️⃣ Testando chat completions (formato OpenAI)...\n")

# Testa chat completions com modelos comuns
chat_endpoints = [
    "https://api.cometapi.com/v1/chat/completions",
    "https://api.cometapi.com/chat/completions",
    "https://cometapi.com/v1/chat/completions"
]

modelos_teste = [
    "gpt-4",
    "gpt-3.5-turbo",
    "gemini-pro",
    "gemini-flash",
    "claude-3-sonnet",
    "llama-3",
    "mistral"
]

for endpoint in chat_endpoints:
    print(f"\nTestando endpoint: {endpoint}")
    
    for modelo in modelos_teste:
        try:
            response = requests.post(
                endpoint,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": modelo,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Say hello"
                        }
                    ]
                },
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"✅ SUCESSO! Modelo: {modelo}")
                data = response.json()
                if "choices" in data:
                    print(f"   Resposta: {data['choices'][0]['message']['content'][:100]}")
                print(f"\n🎯 ENDPOINT FUNCIONANDO: {endpoint}")
                print(f"🎯 MODELO FUNCIONANDO: {modelo}")
                break
            elif response.status_code == 404:
                print(f"   {modelo}: 404 (endpoint não existe)")
                break
            elif response.status_code == 400:
                error_msg = response.text[:200]
                if "model" in error_msg.lower():
                    print(f"   {modelo}: Modelo não existe")
                else:
                    print(f"   {modelo}: 400 - {error_msg}")
            else:
                print(f"   {modelo}: Status {response.status_code}")
        
        except Exception as e:
            print(f"   {modelo}: Erro - {str(e)[:100]}")
    
    # Se encontrou endpoint funcionando, para
    if response.status_code in [200, 400]:
        break

print("\n" + "="*60)
