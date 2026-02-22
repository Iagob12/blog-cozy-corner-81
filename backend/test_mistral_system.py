"""
Teste completo do sistema com Mistral AI
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services.mistral_client import get_mistral_client


async def testar_mistral():
    """Testa Mistral AI"""
    
    print("\n" + "="*60)
    print("🧪 TESTE: Mistral AI")
    print("="*60)
    
    try:
        # Inicializa cliente
        client = get_mistral_client()
        
        # Teste 1: Conexão básica
        print("\n1️⃣ Testando conexão básica...")
        sucesso = await client.testar_conexao()
        
        if sucesso:
            print("   ✅ Conexão OK!")
        else:
            print("   ❌ Conexão falhou")
            return
        
        # Teste 2: Prompt simples
        print("\n2️⃣ Testando prompt simples...")
        resultado = await client.executar_prompt_raw(
            "Responda em português em uma frase: O que é o mercado de ações?",
            task_type="teste"
        )
        print(f"   ✅ Resposta: {resultado[:150]}...")
        
        # Teste 3: Prompt com JSON
        print("\n3️⃣ Testando prompt com JSON...")
        prompt_json = """
Analise a ação PETR4 e retorne APENAS um JSON válido com:
{
    "ticker": "PETR4",
    "setor": "Petróleo e Gás",
    "recomendacao": "COMPRA ou VENDA ou NEUTRO",
    "justificativa": "Breve justificativa"
}
"""
        resultado_json = await client.executar_prompt(
            prompt_json,
            task_type="teste"
        )
        print(f"   ✅ JSON parseado:")
        print(f"      Ticker: {resultado_json.get('ticker')}")
        print(f"      Setor: {resultado_json.get('setor')}")
        print(f"      Recomendação: {resultado_json.get('recomendacao')}")
        
        print("\n" + "="*60)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("="*60)
        print("\n🎯 Sistema pronto para usar Mistral AI!")
        print("   Execute: python -m uvicorn app.main:app --reload --port 8000")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(testar_mistral())
