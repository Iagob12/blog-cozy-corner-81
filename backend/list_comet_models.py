"""
Lista todos os modelos disponíveis na CometAPI
"""
import requests
import json

API_KEY = "sk-vFa83qttcUit84rdkZp5Ptbidi1CfXrNs45yoiuurINuk6W9"

print("\n🔍 Listando modelos CometAPI...\n")

response = requests.get(
    "https://api.cometapi.com/v1/models",
    headers={
        "Authorization": f"Bearer {API_KEY}"
    }
)

if response.status_code == 200:
    data = response.json()
    models = data.get('data', [])
    
    print(f"Total de modelos: {len(models)}\n")
    print("="*80)
    
    # Filtra modelos Gemini
    gemini_models = [m for m in models if 'gemini' in m.get('id', '').lower()]
    
    if gemini_models:
        print("\n🎯 MODELOS GEMINI:\n")
        for model in gemini_models:
            print(f"ID: {model.get('id')}")
            print(f"Owner: {model.get('owned_by')}")
            print(f"Endpoint: {model.get('supported_endpoint_types')}")
            print("-" * 80)
    
    # Filtra modelos GPT
    gpt_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
    
    if gpt_models:
        print("\n🤖 MODELOS GPT:\n")
        for model in gpt_models[:10]:  # Primeiros 10
            print(f"ID: {model.get('id')}")
            print(f"Owner: {model.get('owned_by')}")
            print("-" * 80)
    
    # Filtra modelos Claude
    claude_models = [m for m in models if 'claude' in m.get('id', '').lower()]
    
    if claude_models:
        print("\n🧠 MODELOS CLAUDE:\n")
        for model in claude_models:
            print(f"ID: {model.get('id')}")
            print(f"Owner: {model.get('owned_by')}")
            print("-" * 80)
    
    # Outros modelos interessantes
    print("\n📋 TODOS OS MODELOS DISPONÍVEIS:\n")
    for model in models:
        model_id = model.get('id', '')
        owner = model.get('owned_by', '')
        print(f"{model_id:50} | {owner}")
    
else:
    print(f"Erro: {response.status_code}")
    print(response.text)
