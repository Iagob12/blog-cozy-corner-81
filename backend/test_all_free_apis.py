"""
Testa TODAS as APIs gratuitas possíveis
"""
import requests
import json

print("\n" + "="*80)
print("🔍 TESTANDO TODAS AS APIs GRATUITAS CONHECIDAS")
print("="*80)

# Lista completa de APIs para testar
apis_teste = [
    # Groq (Llama 3 - muito rápido e gratuito)
    {
        "nome": "Groq - Llama 3.3 70B",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "modelo": "llama-3.3-70b-versatile",
        "precisa_key": True,
        "signup": "https://console.groq.com"
    },
    {
        "nome": "Groq - Llama 3.1 8B",
        "url": "https://api.groq.com/openai/v1/chat/completions",
        "modelo": "llama-3.1-8b-instant",
        "precisa_key": True,
        "signup": "https://console.groq.com"
    },
    # Together AI
    {
        "nome": "Together AI - Llama 3.3 70B",
        "url": "https://api.together.xyz/v1/chat/completions",
        "modelo": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "precisa_key": True,
        "signup": "https://api.together.xyz"
    },
    # Hugging Face
    {
        "nome": "Hugging Face - Mistral 7B",
        "url": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
        "modelo": "mistralai/Mistral-7B-Instruct-v0.2",
        "precisa_key": True,
        "signup": "https://huggingface.co/settings/tokens",
        "formato": "hf"
    },
    # Perplexity
    {
        "nome": "Perplexity - Llama 3.1 Sonar",
        "url": "https://api.perplexity.ai/chat/completions",
        "modelo": "llama-3.1-sonar-small-128k-online",
        "precisa_key": True,
        "signup": "https://www.perplexity.ai/settings/api"
    },
    # Fireworks AI
    {
        "nome": "Fireworks AI - Llama 3.3 70B",
        "url": "https://api.fireworks.ai/inference/v1/chat/completions",
        "modelo": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "precisa_key": True,
        "signup": "https://fireworks.ai"
    },
    # Replicate
    {
        "nome": "Replicate - Llama 3.1 70B",
        "url": "https://api.replicate.com/v1/predictions",
        "modelo": "meta/llama-3.1-70b-instruct",
        "precisa_key": True,
        "signup": "https://replicate.com",
        "formato": "replicate"
    },
    # DeepInfra
    {
        "nome": "DeepInfra - Llama 3.3 70B",
        "url": "https://api.deepinfra.com/v1/openai/chat/completions",
        "modelo": "meta-llama/Llama-3.3-70B-Instruct",
        "precisa_key": True,
        "signup": "https://deepinfra.com"
    },
    # Anyscale
    {
        "nome": "Anyscale - Llama 3.1 70B",
        "url": "https://api.endpoints.anyscale.com/v1/chat/completions",
        "modelo": "meta-llama/Llama-3.1-70B-Instruct",
        "precisa_key": True,
        "signup": "https://www.anyscale.com"
    },
    # Cerebras
    {
        "nome": "Cerebras - Llama 3.3 70B",
        "url": "https://api.cerebras.ai/v1/chat/completions",
        "modelo": "llama3.3-70b",
        "precisa_key": True,
        "signup": "https://cloud.cerebras.ai"
    },
    # Novita AI
    {
        "nome": "Novita AI - Llama 3.1 70B",
        "url": "https://api.novita.ai/v3/openai/chat/completions",
        "modelo": "meta-llama/llama-3.1-70b-instruct",
        "precisa_key": True,
        "signup": "https://novita.ai"
    },
    # Lepton AI
    {
        "nome": "Lepton AI - Llama 3.1 70B",
        "url": "https://llama3-1-70b.lepton.run/api/v1/chat/completions",
        "modelo": "llama3-1-70b",
        "precisa_key": False,
        "signup": None
    },
]

print(f"\n📋 Total de APIs para testar: {len(apis_teste)}\n")

apis_gratuitas = []
apis_precisam_signup = []

for api in apis_teste:
    print(f"\n{'='*80}")
    print(f"📝 {api['nome']}")
    print(f"   URL: {api['url']}")
    print(f"   Modelo: {api['modelo']}")
    
    if not api['precisa_key']:
        print(f"   🆓 Não precisa chave!")
        
        try:
            # Testa sem chave
            response = requests.post(
                api['url'],
                headers={"Content-Type": "application/json"},
                json={
                    "model": api['modelo'],
                    "messages": [{"role": "user", "content": "Say hi"}],
                    "max_tokens": 10
                },
                timeout=15
            )
            
            if response.status_code == 200:
                print(f"   ✅ FUNCIONOU SEM CHAVE!")
                apis_gratuitas.append(api)
            else:
                print(f"   ❌ Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Erro: {str(e)[:80]}")
    else:
        print(f"   🔑 Precisa criar conta em: {api['signup']}")
        apis_precisam_signup.append(api)

print("\n" + "="*80)
print("📊 RESUMO FINAL")
print("="*80)

if apis_gratuitas:
    print(f"\n✅ {len(apis_gratuitas)} API(s) GRATUITA(S) SEM PRECISAR CHAVE:\n")
    for api in apis_gratuitas:
        print(f"🎯 {api['nome']}")
        print(f"   URL: {api['url']}")
        print(f"   Modelo: {api['modelo']}")
        print(f"   📝 Não precisa signup!")
        print()
else:
    print("\n⚠️  Nenhuma API totalmente gratuita (sem chave) encontrada")

if apis_precisam_signup:
    print(f"\n📋 {len(apis_precisam_signup)} API(s) COM FREE TIER (precisa signup):\n")
    
    print("🔥 RECOMENDAÇÕES (melhores free tiers):\n")
    
    recomendacoes = [
        ("Groq", "Muito rápido, 30 req/min grátis", "https://console.groq.com"),
        ("Together AI", "$25 créditos grátis", "https://api.together.xyz"),
        ("DeepInfra", "$5 créditos grátis", "https://deepinfra.com"),
        ("Cerebras", "Muito rápido, free tier generoso", "https://cloud.cerebras.ai"),
        ("Fireworks AI", "$1 crédito grátis", "https://fireworks.ai"),
    ]
    
    for nome, beneficio, url in recomendacoes:
        print(f"   • {nome}")
        print(f"     {beneficio}")
        print(f"     Signup: {url}")
        print()

print("\n💡 PRÓXIMO PASSO:")
print("   1. Escolha uma API da lista acima")
print("   2. Crie conta (leva 2 minutos)")
print("   3. Copie a chave API")
print("   4. Configure no sistema")
print("\n" + "="*80)
