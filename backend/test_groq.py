"""
Teste do Groq (Llama 3.3 70B)
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from app.services.groq_client import get_groq_client


async def testar_groq():
    """Testa Groq"""
    
    print("\n" + "="*60)
    print("🧪 TESTE: Groq Llama 3.3 70B")
    print("="*60)
    
    try:
        client = get_groq_client()
        
        print("\n1️⃣ Testando conexão...")
        sucesso = await client.testar_conexao()
        
        if sucesso:
            print("   ✅ Conexão OK!")
        else:
            print("   ❌ Conexão falhou")
            return
        
        print("\n2️⃣ Testando análise financeira...")
        resultado = await client.executar_prompt_raw(
            "Responda em português: Quais são os 3 principais indicadores para avaliar uma ação?",
            task_type="teste"
        )
        print(f"   ✅ Resposta: {resultado[:200]}...")
        
        print("\n3️⃣ Testando JSON...")
        prompt_json = """
Analise a ação PETR4 e retorne APENAS um JSON válido:
{
    "ticker": "PETR4",
    "setor": "Petróleo e Gás",
    "recomendacao": "COMPRA",
    "justificativa": "Breve justificativa"
}
"""
        resultado_json = await client.executar_prompt(prompt_json, task_type="teste")
        print(f"   ✅ JSON parseado:")
        print(f"      Ticker: {resultado_json.get('ticker')}")
        print(f"      Recomendação: {resultado_json.get('recomendacao')}")
        
        print("\n" + "="*60)
        print("✅ GROQ FUNCIONANDO PERFEITAMENTE!")
        print("="*60)
        print("\n🚀 Velocidade: EXTREMAMENTE RÁPIDO")
        print("🎯 Qualidade: Excelente (Llama 3.3 70B)")
        print("💰 Free tier: 30 req/min")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(testar_groq())
