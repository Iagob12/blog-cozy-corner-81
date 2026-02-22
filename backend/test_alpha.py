"""
Script de teste do Alpha Terminal
"""
import asyncio
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_intelligence import AlphaIntelligence
from app.services.market_data import MarketDataService

async def test_radar():
    print("=" * 60)
    print("TESTE 1: RADAR DE OPORTUNIDADES")
    print("=" * 60)
    
    ai = AlphaIntelligence()
    result = await ai.prompt_1_radar_oportunidades()
    
    print("\n📊 Setores em Aceleração:")
    for setor in result.get("setores_aceleracao", []):
        print(f"\n  • {setor['setor']} ({setor['estagio_ciclo']})")
        print(f"    Catalisador: {setor['catalisador']}")
        print(f"    Upside: {setor['potencial_upside']}")
    
    print("\n🔍 Movimentos Silenciosos:")
    for mov in result.get("movimentos_silenciosos", []):
        print(f"\n  • {mov['nome']} (Radar: {mov['radar_varejo']})")
        print(f"    {mov['similaridade']}")

async def test_market_data():
    print("\n" + "=" * 60)
    print("TESTE 2: DADOS DE MERCADO")
    print("=" * 60)
    
    market = MarketDataService()
    
    # Testa cotação
    print("\n📈 Cotação PRIO3:")
    quote = await market.get_quote("PRIO3")
    print(f"  Preço: R$ {quote.get('preco_atual', 0):.2f}")
    print(f"  Variação: {quote.get('variacao_dia', 0):.2f}%")
    
    # Testa overview
    print("\n🌎 Visão Geral do Mercado:")
    overview = await market.get_market_overview()
    if overview.get("ibovespa"):
        print(f"  Ibovespa: {overview['ibovespa'].get('pontos', 0):,.0f} pts")
        print(f"  Variação: {overview['ibovespa'].get('variacao_pct', 0):.2f}%")
    if overview.get("dolar"):
        print(f"  Dólar: R$ {overview['dolar'].get('cotacao', 0):.2f}")

async def test_swing_trade():
    print("\n" + "=" * 60)
    print("TESTE 3: ANÁLISE SWING TRADE")
    print("=" * 60)
    
    ai = AlphaIntelligence()
    market = MarketDataService()
    
    ticker = "PRIO3"
    quote = await market.get_quote(ticker)
    preco = quote.get("preco_atual", 50.0)
    
    print(f"\n🎯 Analisando {ticker} (R$ {preco:.2f})...")
    result = await ai.prompt_4_swing_trade(ticker, preco)
    
    print(f"\n  Recomendação: {result.get('recomendacao')}")
    print(f"  Justificativa: {result.get('justificativa')}")
    print(f"\n  Stop Loss: R$ {result.get('stop_loss', 0):.2f}")
    print(f"  Alvo: R$ {result.get('alvo', 0):.2f}")
    print(f"  Risco/Retorno: {result.get('relacao_risco_retorno', 0):.1f}:1")

async def test_anti_manada():
    print("\n" + "=" * 60)
    print("TESTE 4: VERIFICAÇÃO ANTI-MANADA")
    print("=" * 60)
    
    ai = AlphaIntelligence()
    ticker = "PRIO3"
    
    print(f"\n🔍 Verificando {ticker}...")
    result = await ai.prompt_6_verificacao_anti_manada(ticker)
    
    print(f"\n  Exposição Mídia: {result.get('exposicao_midia')}")
    print(f"  Fundamento vs Narrativa: {result.get('fundamento_vs_narrativa')}")
    print(f"  Posicionamento Institucional: {result.get('posicionamento_institucional')}")
    print(f"\n  ⚡ VEREDITO: {result.get('veredito')}")
    print(f"  {result.get('justificativa')}")

async def main():
    print("\n🚀 ALPHA TERMINAL - TESTE DO SISTEMA\n")
    
    # Verifica API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  AVISO: GEMINI_API_KEY não configurada!")
        print("   Configure no arquivo .env para usar análise de IA\n")
    
    try:
        # Testa dados de mercado (não precisa de API key)
        await test_market_data()
        
        # Testes que precisam de Gemini API
        if os.getenv("GEMINI_API_KEY"):
            await test_radar()
            await test_swing_trade()
            await test_anti_manada()
        else:
            print("\n⏭️  Pulando testes de IA (configure GEMINI_API_KEY)")
        
        print("\n" + "=" * 60)
        print("✅ TESTES CONCLUÍDOS")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
