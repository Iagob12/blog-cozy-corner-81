"""
Script para rodar análise manualmente
Gera novo ranking com prompts melhorados
"""
import asyncio
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.analise_automatica.analise_service import get_analise_automatica_service
from app.services.csv_manager import get_csv_manager

async def main():
    """Roda análise completa"""
    print("\n" + "="*70)
    print("🚀 ANÁLISE MANUAL - SISTEMA ALPHA V3")
    print("="*70 + "\n")
    
    # 1. Carrega empresas do CSV
    print("📊 Carregando empresas do CSV...")
    import pandas as pd
    
    csv_path = "data/stocks.csv"
    if not os.path.exists(csv_path):
        print(f"❌ Erro: CSV não encontrado em {csv_path}")
        return
    
    df = pd.read_csv(csv_path)
    
    if df is None or df.empty:
        print("❌ Erro: CSV vazio ou não encontrado")
        return
    
    # Pega apenas empresas com dados válidos
    df_valido = df[
        (df['roe'] > 0) &
        (df['pl'] > 0) &
        (df['pl'] < 50)  # Filtra P/L muito alto
    ]
    
    print(f"   Total no CSV: {len(df)}")
    print(f"   Com dados válidos: {len(df_valido)}")
    
    # Limita a 30 empresas para teste (evita rate limit)
    empresas = df_valido['ticker'].head(30).tolist()
    print(f"   Selecionadas para análise: {len(empresas)}")
    print(f"   Empresas: {', '.join(empresas[:10])}...")
    
    # 2. Roda análise incremental
    print(f"\n🤖 Iniciando análise...")
    print(f"   IMPORTANTE: Usando prompts MELHORADOS (foco em 5% ao mês)")
    print(f"   Rate limit: 1 empresa por vez, 5s entre cada")
    print()
    
    analise_service = get_analise_automatica_service()
    
    resultado = await analise_service.analisar_incrementalmente(
        empresas=empresas,
        forcar_reanalise=True,  # Força reanálise de todas
        max_paralelo=1  # 1 por vez para evitar rate limit
    )
    
    # 3. Mostra resultado
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
    
    # 4. Mostra top 10 do ranking
    ranking = analise_service.obter_ranking_atual()
    if ranking and ranking.ranking:
        print(f"\n🏆 TOP 10 RANKING:")
        print(f"{'='*70}")
        
        for i, stock in enumerate(ranking.ranking[:10], 1):
            print(f"{i:2d}. {stock.ticker:6s} - Score: {stock.efficiency_score:5.1f} - {stock.recomendacao_final:12s} - Upside: {stock.upside_potencial:5.1f}%")
        
        print(f"{'='*70}")
    
    print(f"\n✅ Ranking salvo em: backend/data/ranking_cache.json")
    print(f"✅ Frontend agora pode exibir os dados!")
    print()

if __name__ == "__main__":
    asyncio.run(main())
