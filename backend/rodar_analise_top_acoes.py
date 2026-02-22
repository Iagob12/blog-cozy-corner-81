"""
Script para rodar análise com as ações MAIS POPULARES
Usa tickers que têm maior chance de funcionar no Brapi
"""
import asyncio
import sys
import os
from dotenv import load_dotenv

# Carrega .env ANTES de importar serviços
load_dotenv()

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.analise_automatica.analise_service import get_analise_automatica_service

async def main():
    """Roda análise com ações populares"""
    print("\n" + "="*70)
    print("🚀 ANÁLISE MANUAL - AÇÕES POPULARES")
    print("="*70 + "\n")
    
    # Lista de ações MAIS POPULARES do Ibovespa
    # Estas têm maior chance de funcionar no Brapi free tier
    empresas_populares = [
        "PETR4",  # Petrobras
        "VALE3",  # Vale
        "ITUB4",  # Itaú
        "BBDC4",  # Bradesco
        "ABEV3",  # Ambev
        "BBAS3",  # Banco do Brasil
        "WEGE3",  # WEG
        "RENT3",  # Localiza
        "SUZB3",  # Suzano
        "RAIL3",  # Rumo
        "JBSS3",  # JBS
        "EMBR3",  # Embraer
        "GGBR4",  # Gerdau
        "CSNA3",  # CSN
        "USIM5",  # Usiminas
        "CSAN3",  # Cosan
        "RADL3",  # Raia Drogasil
        "PRIO3",  # Prio
        "CPLE6",  # Copel
        "ELET3",  # Eletrobras
    ]
    
    print(f"📊 Empresas selecionadas: {len(empresas_populares)}")
    print(f"   {', '.join(empresas_populares)}")
    
    # Roda análise incremental
    print(f"\n🤖 Iniciando análise...")
    print(f"   IMPORTANTE: Usando prompts MELHORADOS (foco em 5% ao mês)")
    print(f"   Rate limit: 1 empresa por vez, 5s entre cada")
    print()
    
    analise_service = get_analise_automatica_service()
    
    resultado = await analise_service.analisar_incrementalmente(
        empresas=empresas_populares,
        forcar_reanalise=True,  # Força reanálise de todas
        max_paralelo=1  # 1 por vez para evitar rate limit
    )
    
    # Mostra resultado
    print(f"\n{'='*70}")
    print(f"✅ ANÁLISE CONCLUÍDA")
    print(f"{'='*70}")
    print(f"✓ Novas análises: {resultado['novas_analises']}")
    print(f"💾 Cache mantido: {resultado['cache_mantido']}")
    print(f"❌ Falhas: {resultado['falhas']}")
    print(f"🏆 Ranking: {resultado['total_ranking']} empresas")
    print(f"⏱️  Tempo: {resultado['tempo_segundos']:.1f}s")
    
    if resultado['falhas'] > 0:
        print(f"\n⚠️ Detalhes das falhas:")
        for falha in resultado.get('detalhes_falhas', [])[:5]:
            print(f"   - {falha.get('ticker')}: {falha.get('erro')[:50]}")
    
    # Mostra top 10 do ranking
    ranking_dict = analise_service.obter_ranking_atual()
    if ranking_dict and 'ranking' in ranking_dict:
        ranking_list = ranking_dict['ranking']
        print(f"\n🏆 TOP 10 RANKING:")
        print(f"{'='*70}")
        
        for i, stock in enumerate(ranking_list[:10], 1):
            ticker = stock.get('ticker', 'N/A')
            score = stock.get('score', 0)
            recomendacao = stock.get('recomendacao', 'N/A')
            upside = stock.get('upside', 0)
            print(f"{i:2d}. {ticker:6s} - Score: {score:5.1f} - {recomendacao:12s} - Upside: {upside:5.1f}%")
        
        print(f"{'='*70}")
    
    print(f"\n✅ Ranking salvo em: backend/data/ranking_cache.json")
    print(f"✅ Frontend agora pode exibir os dados!")
    print()

if __name__ == "__main__":
    asyncio.run(main())
