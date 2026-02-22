"""
Script para converter ranking do sistema incremental para formato TopPick
"""
import json
from datetime import datetime

# Lê ranking do sistema incremental
with open('data/cache/ranking_atual.json', 'r', encoding='utf-8') as f:
    ranking_incremental = json.load(f)

# Lê CSV para pegar dados adicionais (ROE, P/L, CAGR, setor)
import pandas as pd
df_csv = pd.read_csv('data/stocks.csv')

# Busca preços do Brapi
import requests
tickers = [stock["ticker"] for stock in ranking_incremental["ranking"]]
precos = {}
try:
    response = requests.get(f"https://brapi.dev/api/quote/{','.join(tickers)}?token=YOUR_TOKEN")
    if response.status_code == 200:
        data = response.json()
        for result in data.get("results", []):
            precos[result["symbol"]] = result.get("regularMarketPrice", 0)
except:
    pass

# Converte para formato TopPick
ranking_convertido = {
    "timestamp": ranking_incremental["timestamp"],
    "total_aprovadas": ranking_incremental["total"],
    "ranking": []
}

for stock in ranking_incremental["ranking"]:
    ticker = stock["ticker"]
    
    # Busca dados do CSV
    linha_csv = df_csv[df_csv['ticker'] == ticker]
    roe = float(linha_csv['roe'].values[0]) if not linha_csv.empty and 'roe' in linha_csv.columns else 0
    pl = float(linha_csv['pl'].values[0]) if not linha_csv.empty and 'pl' in linha_csv.columns else 0
    cagr = float(linha_csv['cagr'].values[0]) if not linha_csv.empty and 'cagr' in linha_csv.columns else 0
    setor = str(linha_csv['setor'].values[0]) if not linha_csv.empty and 'setor' in linha_csv.columns else "N/A"
    
    # Mapeia campos
    top_pick = {
        "ticker": ticker,
        "efficiency_score": stock["score"],  # score -> efficiency_score
        "macro_weight": 1.0,  # Valor padrão
        "catalisadores": stock["catalisadores"],
        "preco_teto": stock["preco_teto"],
        "preco_atual": precos.get(ticker, None),
        "upside_potencial": stock["upside"],
        "sentiment_status": "neutro",  # Valor padrão
        "recomendacao_final": stock["recomendacao"],
        "setor": setor,
        "roe": roe,
        "cagr": cagr,
        "pl": pl,
        "tempo_estimado_dias": 90,  # Valor padrão
        "sentiment_ratio": 1.0,  # Valor padrão
        "variacao_30d": 0,  # Valor padrão
        "rank": stock.get("rank", 0)
    }
    
    ranking_convertido["ranking"].append(top_pick)

# Salva no formato correto
with open('data/ranking_cache.json', 'w', encoding='utf-8') as f:
    json.dump(ranking_convertido, f, indent=2, ensure_ascii=False)

print(f"✓ Ranking convertido: {len(ranking_convertido['ranking'])} empresas")
print(f"✓ Salvo em: data/ranking_cache.json")
