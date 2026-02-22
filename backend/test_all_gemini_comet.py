"""
Testa todos os modelos Gemini da CometAPI
"""
import requests

API_KEY = "sk-vFa83qttcUit84rdkZp5Ptbidi1CfXrNs45yoiuurINuk6W9"

# Lista de modelos Gemini para testar
modelos = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-thinking",
    "gemini-2.0-flash-thinking-exp",
    "gemini-2.0-pro-exp",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite",
    "gemini-2.5-pro",
    "gemini-3-flash",
    "gemini-3-flash-preview",
    "gemini-3-pro-preview",
    "gemini-3-pro-all",
    "gemini-3.1-pro-preview"
]

print("\n" + "="*80)
print("🧪 TESTANDO MODELOS GEMINI NA COMETAPI")
print("="*80)

modelos_funcionando = []

for modelo in modelos:
    print(f"\n📝 Testando: {modelo}")
    
    try:
        response = requests.post(
            "https://api.cometapi.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": modelo,
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello in one word"
                    }
                ]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            resposta = data['choices'][0]['message']['content']
            print(f"   ✅ FUNCIONOU!")
            print(f"   Resposta: {resposta[:50]}")
            
            # Verifica tokens/custo
            usage = data.get('usage', {})
            print(f"   Tokens: {usage}")
            
            modelos_funcionando.append(modelo)
        
        elif response.status_code == 403:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', '')
            
            if 'quota' in error_msg.lower():
                print(f"   ⚠️  Precisa créditos (quota)")
            else:
                print(f"   ❌ 403: {error_msg[:100]}")
        
        elif response.status_code == 400:
            error_data = response.json()
            print(f"   ❌ Modelo inválido ou erro: {error_data.get('error', {}).get('message', '')[:100]}")
        
        elif response.status_code == 503:
            print(f"   ⏸️  Serviço indisponível (503)")
        
        else:
            print(f"   ❌ Status {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}")

print("\n" + "="*80)
print("📊 RESUMO")
print("="*80)

if modelos_funcionando:
    print(f"\n✅ {len(modelos_funcionando)} modelo(s) funcionando SEM precisar créditos:\n")
    for modelo in modelos_funcionando:
        print(f"   • {modelo}")
    print(f"\n🎯 RECOMENDAÇÃO: Use '{modelos_funcionando[0]}'")
else:
    print("\n⚠️  Nenhum modelo funcionou sem créditos")
    print("   Todos os modelos Gemini na CometAPI requerem créditos na conta")

print("\n" + "="*80)
