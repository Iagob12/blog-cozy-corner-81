"""
Testa APIs alternativas que podem ter Gemini gratuito
"""
import requests
import json

print("\n" + "="*80)
print("🔍 BUSCANDO APIs COM GEMINI GRATUITO")
print("="*80)

# Lista de APIs para testar
apis_teste = [
    {
        "nome": "AI/ML API (aimlapi.com)",
        "url": "https://api.aimlapi.com/v1/chat/completions",
        "key": "3d1ad51f660b4adfadfb6bead232d998",
        "modelo": "gemini-2.0-flash-exp"
    },
    {
        "nome": "AI/ML API - Gemini Pro",
        "url": "https://api.aimlapi.com/v1/chat/completions",
        "key": "3d1ad51f660b4adfadfb6bead232d998",
        "modelo": "gemini-pro"
    },
    {
        "nome": "AI/ML API - Gemini 1.5 Flash",
        "url": "https://api.aimlapi.com/v1/chat/completions",
        "key": "3d1ad51f660b4adfadfb6bead232d998",
        "modelo": "gemini-1.5-flash"
    },
    {
        "nome": "Mistral AI",
        "url": "https://api.mistral.ai/v1/chat/completions",
        "key": "YlD9P2x2rRKbZiagsVYS3THWPU7BMHUd",
        "modelo": "mistral-small-latest"
    },
    {
        "nome": "Together AI - Gemini",
        "url": "https://api.together.xyz/v1/chat/completions",
        "key": "test",
        "modelo": "google/gemini-pro"
    },
    {
        "nome": "Groq - Llama 3",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "key": "test",
        "modelo": "llama3-8b-8192"
    },
]

modelos_funcionando = []

for api in apis_teste:
    print(f"\n📝 Testando: {api['nome']}")
    print(f"   Modelo: {api['modelo']}")
    
    try:
        response = requests.post(
            api['url'],
            headers={
                "Authorization": f"Bearer {api['key']}",
                "Content-Type": "application/json"
            },
            json={
                "model": api['modelo'],
                "messages": [
                    {
                        "role": "user",
                        "content": "Say hello in one word"
                    }
                ],
                "max_tokens": 50
            },
            timeout=15
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                resposta = data["choices"][0]["message"]["content"]
                print(f"   ✅ FUNCIONOU!")
                print(f"   Resposta: {resposta}")
                
                usage = data.get("usage", {})
                print(f"   Tokens: {usage}")
                
                modelos_funcionando.append({
                    "nome": api['nome'],
                    "url": api['url'],
                    "modelo": api['modelo'],
                    "key": api['key']
                })
            else:
                print(f"   ⚠️  Resposta sem choices")
        
        elif response.status_code == 401:
            print(f"   ❌ Não autorizado (chave inválida)")
        
        elif response.status_code == 403:
            error_data = response.json()
            print(f"   ❌ 403: {error_data.get('error', {}).get('message', 'Sem permissão')[:100]}")
        
        elif response.status_code == 429:
            print(f"   ⚠️  Rate limit atingido")
        
        else:
            try:
                error_data = response.json()
                print(f"   ❌ Erro: {error_data}")
            except:
                print(f"   ❌ Erro: {response.text[:200]}")
    
    except requests.exceptions.Timeout:
        print(f"   ⏱️  Timeout")
    except Exception as e:
        print(f"   ❌ Erro: {str(e)[:100]}")

print("\n" + "="*80)
print("📊 RESUMO")
print("="*80)

if modelos_funcionando:
    print(f"\n✅ {len(modelos_funcionando)} API(s) funcionando:\n")
    for item in modelos_funcionando:
        print(f"\n🎯 {item['nome']}")
        print(f"   URL: {item['url']}")
        print(f"   Modelo: {item['modelo']}")
        print(f"   Key: {item['key'][:20]}...")
        print("-" * 80)
    
    print(f"\n💡 RECOMENDAÇÃO: Use '{modelos_funcionando[0]['nome']}'")
    print(f"   Modelo: {modelos_funcionando[0]['modelo']}")
else:
    print("\n⚠️  Nenhuma API gratuita com Gemini encontrada")
    print("\n💡 ALTERNATIVAS:")
    print("   1. Adicionar créditos no OpenRouter ($5)")
    print("   2. Adicionar créditos no CometAPI ($10)")
    print("   3. Usar as 6 chaves Gemini diretas (aguardar 24h)")
    print("   4. Usar modelos alternativos (Llama, Mistral)")

print("\n" + "="*80)
