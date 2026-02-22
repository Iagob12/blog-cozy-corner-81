"""
Teste simples das chaves Groq
"""
import asyncio
import httpx


async def testar_chave(key, index):
    """Testa uma chave Groq"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers={
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "user", "content": "Responda apenas: OK"}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 10
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                resposta = data["choices"][0]["message"]["content"]
                print(f"✓ CHAVE {index + 1}: OK - Resposta: {resposta}")
                return True
            else:
                print(f"✗ CHAVE {index + 1}: ERRO {response.status_code} - {response.text[:100]}")
                return False
    
    except Exception as e:
        print(f"✗ CHAVE {index + 1}: EXCEÇÃO - {str(e)[:100]}")
        return False


async def main():
    """Testa todas as chaves"""
    keys = [
        "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",
        "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",
        "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",
        "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",
        "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",
        "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",
    ]
    
    print("\n" + "="*60)
    print("TESTANDO CHAVES GROQ")
    print("="*60 + "\n")
    
    resultados = []
    for i, key in enumerate(keys):
        resultado = await testar_chave(key, i)
        resultados.append(resultado)
        await asyncio.sleep(2)  # Delay entre testes
    
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    print(f"Chaves funcionando: {sum(resultados)}/6")
    print(f"Chaves com erro: {6 - sum(resultados)}/6")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
