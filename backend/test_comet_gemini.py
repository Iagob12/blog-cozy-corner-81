"""
Teste CometAPI com Gemini 3 Pro All
"""
import requests

API_KEY = "sk-vFa83qttcUit84rdkZp5Ptbidi1CfXrNs45yoiuurINuk6W9"

print("\n🧪 Testando CometAPI com Gemini 3 Pro All\n")

response = requests.post(
    "https://api.cometapi.com/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "gemini-3-pro-all",
        "messages": [
            {
                "role": "user",
                "content": "Responda em português: O que é o mercado de ações?"
            }
        ]
    }
)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"\n✅ SUCESSO!")
    print(f"\nResposta: {data['choices'][0]['message']['content']}")
    print(f"\nModelo: {data.get('model')}")
    print(f"Tokens usados: {data.get('usage', {})}")
else:
    print(f"\n❌ Erro: {response.status_code}")
    print(f"Detalhes: {response.text}")
