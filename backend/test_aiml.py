"""
Script de teste para AIML API
Testa Gemini 2.0 Flash Thinking + Claude 3.5 Sonnet
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.aiml_service import AIMLService

load_dotenv()

async def test_aiml():
    print("=" * 60)
    print("TESTE AIML API - MULTI-IA")
    print("=" * 60)
    
    # Verifica API Key
    api_key = os.getenv("AIML_API_KEY")
    if not api_key:
        print("✗ AIML_API_KEY não configurada!")
        return
    
    print(f"\n✓ API Key: {api_key[:10]}...")
    
    # Inicializa serviço
    service = AIMLService()
    
    # Teste 1: Gemini Thinking - Análise de Mercado
    print("\n" + "-" * 60)
    print("TESTE 1: Gemini 2.0 Flash Thinking")
    print("-" * 60)
    
    acoes_teste = [
        {"ticker": "PRIO3", "roe": 35.2, "cagr": 18.5, "pl": 8.5, "setor": "Energia", "score": 9.2},
        {"ticker": "VULC3", "roe": 50.1, "cagr": 15.3, "pl": 6.2, "setor": "Consumo", "score": 9.5},
        {"ticker": "WEGE3", "roe": 22.3, "cagr": 18.5, "pl": 28.5, "setor": "Industrial", "score": 7.8},
    ]
    
    contexto = {
        "data": "19/02/2026",
        "setores": {"Energia": 1.2, "Consumo": 1.1, "Industrial": 1.0},
        "tendencias": ["Juros em queda", "Commodities em alta"]
    }
    
    result1 = await service.gemini_thinking_analise_mercado(
        acoes_candidatas=acoes_teste,
        contexto_macro=contexto
    )
    
    if result1["success"]:
        print("\n✓ Gemini Thinking - SUCESSO")
        print(f"Tokens usados: {result1['tokens']}")
        print("\nResposta (primeiros 500 chars):")
        print(result1["content"][:500] + "...")
    else:
        print(f"\n✗ Gemini Thinking - FALHOU: {result1.get('error')}")
    
    # Teste 2: Claude Sonnet - Análise de Ação
    print("\n" + "-" * 60)
    print("TESTE 2: Claude 3.5 Sonnet")
    print("-" * 60)
    
    result2 = await service.claude_analise_profunda_acao(
        ticker="PRIO3",
        dados_fundamentalistas={
            "roe": 35.2,
            "cagr": 18.5,
            "pl": 8.5,
            "divida": 1.2,
            "setor": "Energia"
        },
        preco_atual=48.50,
        relatorio_trimestral="Q4 2025: Receita cresceu 15%, lucro líquido aumentou 20%, margens em expansão."
    )
    
    if result2["success"]:
        print("\n✓ Claude Sonnet - SUCESSO")
        print(f"Tokens usados: {result2['tokens']}")
        print("\nResposta (primeiros 500 chars):")
        print(result2["content"][:500] + "...")
    else:
        print(f"\n✗ Claude Sonnet - FALHOU: {result2.get('error')}")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Gemini Thinking: {'✓ OK' if result1['success'] else '✗ FALHOU'}")
    print(f"Claude Sonnet: {'✓ OK' if result2['success'] else '✗ FALHOU'}")
    
    if result1["success"] and result2["success"]:
        print("\n🎉 SISTEMA MULTI-IA FUNCIONANDO!")
    else:
        print("\n⚠ Alguns testes falharam. Verifique a API key e conexão.")

if __name__ == "__main__":
    asyncio.run(test_aiml())
