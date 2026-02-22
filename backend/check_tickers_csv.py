"""Verifica quais tickers populares estão no CSV"""
import pandas as pd

df = pd.read_csv('data/stocks.csv')

populares = [
    'PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'ABEV3',
    'BBAS3', 'WEGE3', 'RENT3', 'SUZB3', 'RAIL3',
    'JBSS3', 'EMBR3', 'GGBR4', 'CSNA3', 'USIM5'
]

print("\n=== TICKERS POPULARES NO CSV ===\n")

encontrados = []
for ticker in populares:
    if ticker in df['ticker'].values:
        row = df[df['ticker'] == ticker].iloc[0]
        encontrados.append(ticker)
        print(f"✓ {ticker:6s} - ROE: {row.roe*100:5.1f}% | P/L: {row.pl:6.2f} | CAGR: {row.cagr*100:5.1f}%")
    else:
        print(f"✗ {ticker:6s} - NÃO ENCONTRADO")

print(f"\nTotal encontrados: {len(encontrados)}/{len(populares)}")
print(f"Tickers: {', '.join(encontrados)}")
