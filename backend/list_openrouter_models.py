"""
Lista modelos disponíveis no OpenRouter
"""
import requests

API_KEY = "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"

response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

if response.status_code == 200:
    models = response.json()
    
    print("\n🔍 Modelos Gemini disponíveis no OpenRouter:\n")
    
    gemini_models = [m for m in models.get('data', []) if 'gemini' in m.get('id', '').lower()]
    
    for model in gemini_models:
        model_id = model.get('id', '')
        name = model.get('name', '')
        pricing = model.get('pricing', {})
        prompt_price = pricing.get('prompt', 'N/A')
        
        print(f"ID: {model_id}")
        print(f"Nome: {name}")
        print(f"Preço: {prompt_price}")
        print("-" * 60)
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
