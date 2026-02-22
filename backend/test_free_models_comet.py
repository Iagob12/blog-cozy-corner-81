"""
Testa modelos GRATUITOS ou com trial na CometAPI
"""
import requests

API_KEY = "sk-vFa83qttcUit84rdkZp5Ptbidi1CfXrNs45yoiuurINuk6W9"

# Modelos que podem ter trial/free tier
modelos_teste = [
    # Modelos menores/mais baratos
    "qwen2.5-7b-instruct",
    "qwen2-7b-instruct",
    "qwen-turbo",
    "glm-4-flash",
    "deepseek-chat",
    "deepseek-v3",
    "minimax-hailuo-02",
    "hunyuan-lite",
    "hunyuan-turbo",
    # Modelos custom/cometapi
    "cometapi-3-5-sonnet",
    "cometapi-haiku-4-5-20251001",
]

print("\n" + "="*80)
print("🧪 TESTANDO MODELOS ALTERNATIVOS NA COMETAPI")
print("="*80)

modelos_funcionando = []

for modelo in modelos_teste:
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
                        "content": "Responda em português: O que é investimento?"
                    }
                ]
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            resposta = data['choices'][0]['message']['content']
            print(f"   ✅ FUNCIONOU!")
            print(f"   Resposta: {resposta[:100]}...")
            
            # Verifica tokens/custo
            usage = data.get('usage', {})
            print(f"   Tokens: {usage}")
            
            modelos_funcionando.append({
                "modelo": modelo,
                "resposta": resposta[:200]
            })
        
        elif response.status_code == 403:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', '')
            
            if 'quota' in error_msg.lower():
                print(f"   ⚠️  Precisa créditos")
            else:
                print(f"   ❌ 403: {error_msg[:80]}")
        
        elif response.status_code == 400:
            print(f"   ❌ Modelo inválido")
        
        elif response.status_code == 503:
            print(f"   ⏸️  Indisponível")
        
        else:
            print(f"   ❌ Status {response.status_code}")
    
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:80]}")

print("\n" + "="*80)
print("📊 RESUMO")
print("="*80)

if modelos_funcionando:
    print(f"\n✅ {len(modelos_funcionando)} modelo(s) funcionando:\n")
    for item in modelos_funcionando:
        print(f"\n🎯 MODELO: {item['modelo']}")
        print(f"   Resposta: {item['resposta']}")
        print("-" * 80)
    
    print(f"\n💡 RECOMENDAÇÃO: Use '{modelos_funcionando[0]['modelo']}'")
else:
    print("\n⚠️  Nenhum modelo gratuito encontrado")
    print("   CometAPI requer créditos para todos os modelos testados")

print("\n" + "="*80)
