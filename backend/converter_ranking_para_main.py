"""
Converte ranking do cache_manager para formato do main.py
"""
import json
import pandas as pd

# Lê ranking do cache
with open('data/cache/ranking_atual.json', 'r', encoding='utf-8') as f:
    cache_ranking = json.load(f)

# Lê CSV para pegar dados adicionais
df = pd.read_csv('data/stocks.csv')

# Converte para formato TopPick
ranking_convertido = []

for item in cache_ranking['ranking']:
    ticker = item['ticker']
    
    # Busca dados do CSV
    row = df[df['ticker'] == ticker]
    if row.empty:
        print(f"⚠️ {ticker} não encontrado no CSV, pulando...")
        continue
    
    row = row.iloc[0]
    
    # Cria objeto TopPick
    top_pick = {
        "ticker": ticker,
        "efficiency_score": float(item.get('score', 0)),
        "macro_weight": 1.0,  # Padrão
        "catalisadores": item.get('catalisadores', []),
        "preco_teto": float(item.get('preco_teto', 0)),
        "preco_atual": float(item.get('preco_teto', 0) / (1 + item.get('upside', 0) / 100)) if item.get('upside', 0) != 0 else 0.0,
        "upside_potencial": float(item.get('upside', 0)),
        "sentiment_status": "Normal",
        "recomendacao_final": item.get('recomendacao', 'AGUARDAR'),
        "setor": str(row.get('setor', 'N/A')),
        "roe": float(row['roe'] * 100 if row['roe'] < 1 else row['roe']),  # Converte para %
        "cagr": float(row['cagr'] * 100 if row['cagr'] < 1 else row['cagr']),  # Converte para %
        "pl": float(row['pl']),
        "tempo_estimado_dias": 90,  # Padrão
        "sentiment_ratio": 1.0,  # Padrão
        "variacao_30d": 0.0,  # Padrão
        "rank": int(item.get('rank', 0))
    }
    
    ranking_convertido.append(top_pick)

# Salva no formato esperado pelo main.py
dados_para_salvar = {
    "timestamp": cache_ranking['timestamp'],
    "total_aprovadas": len(ranking_convertido),
    "ranking": ranking_convertido
}

with open('data/ranking_cache.json', 'w', encoding='utf-8') as f:
    json.dump(dados_para_salvar, f, indent=2, ensure_ascii=False)

print(f"\n✅ Ranking convertido e salvo!")
print(f"   Total: {len(ranking_convertido)} empresas")
print(f"   Arquivo: data/ranking_cache.json")
print(f"\n🏆 TOP 5:")
for i, stock in enumerate(ranking_convertido[:5], 1):
    print(f"   {i}. {stock['ticker']:6s} - Score: {stock['efficiency_score']:5.1f} - {stock['recomendacao_final']:12s}")
