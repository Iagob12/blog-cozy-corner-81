"""
Script para carregar ranking rapidamente e iniciar servidor
SEM rodar análise automática
"""
import json
import sys
from datetime import datetime

# Carrega ranking do arquivo
try:
    with open('data/ranking_cache.json', 'r', encoding='utf-8') as f:
        ranking_data = json.load(f)
    
    print(f"✓ Ranking carregado: {len(ranking_data['ranking'])} empresas")
    print(f"✓ Timestamp: {ranking_data['timestamp']}")
    print(f"\nTop 5:")
    for i, stock in enumerate(ranking_data['ranking'][:5], 1):
        print(f"  {i}. {stock['ticker']} - Score: {stock['efficiency_score']} - {stock['recomendacao_final']}")
    
    print(f"\n✅ Ranking pronto para servir!")
    print(f"🚀 Iniciando servidor...")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
