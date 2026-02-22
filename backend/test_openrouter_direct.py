"""
Teste direto da API OpenRouter
"""
import requests
import json

API_KEY = "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"
URL = "https://openrouter.ai/api/v1/chat/completions"

# Testa Gemini 3 Flash
modelos = [
    "google/gemini-3-flash-preview"
]

for modelo in modelos:
    print(f"\n{'='*60}")
    print(f"Testando modelo: {modelo}")
    print(f"{'='*60}")
    
    response = requests.post(
        URL,
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
        }
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ SUCESSO!")
        print(f"Resposta: {data['choices'][0]['message']['content'][:100]}")
        print(f"\n🎯 MODELO FUNCIONANDO: {modelo}")
        break
    else:
        print(f"❌ Erro: {response.text[:200]}")

