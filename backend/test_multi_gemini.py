"""
Teste do Multi Gemini Client - Verifica todas as 6 chaves
"""
import asyncio
from app.services.multi_gemini_client import get_multi_gemini_client


async def main():
    print("\n" + "="*60)
    print("TESTE: MULTI GEMINI CLIENT (6 CHAVES)")
    print("="*60 + "\n")
    
    client = get_multi_gemini_client()
    
    print("Testando conexão com todas as 6 chaves...\n")
    
    resultados = await client.testar_conexao()
    
    print("\n" + "="*60)
    print("RESULTADOS:")
    print("="*60)
    
    total = len(resultados)
    funcionando = sum(1 for v in resultados.values() if v)
    
    for chave, status in resultados.items():
        emoji = "✓" if status else "✗"
        print(f"{emoji} {chave.upper()}: {'OK' if status else 'FALHOU'}")
    
    print("\n" + "="*60)
    print(f"Total: {funcionando}/{total} chaves funcionando")
    print("="*60 + "\n")
    
    if funcionando >= 4:
        print("✅ Sistema pronto para uso!")
    elif funcionando >= 2:
        print("⚠️  Sistema funcional mas com algumas chaves com problema")
    else:
        print("❌ Muitas chaves com problema - verifique as API keys")


if __name__ == "__main__":
    asyncio.run(main())
