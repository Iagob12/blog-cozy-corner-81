"""
Teste de leitura do CSV com UTF-8 BOM
"""
import pandas as pd

print("🧪 Testando leitura do CSV...")

try:
    # Tenta ler sem encoding especial (deve falhar se tiver BOM)
    print("\n1. Tentando ler SEM encoding especial...")
    df = pd.read_csv("data/stocks.csv")
    print(f"   ✅ Sucesso! {len(df)} linhas")
except Exception as e:
    print(f"   ❌ Erro: {e}")

try:
    # Tenta ler COM encoding utf-8-sig (deve funcionar)
    print("\n2. Tentando ler COM encoding='utf-8-sig'...")
    df = pd.read_csv("data/stocks.csv", encoding='utf-8-sig')
    print(f"   ✅ Sucesso! {len(df)} linhas")
    print(f"   Colunas: {list(df.columns)[:5]}")
    print(f"   Primeira linha: {df.iloc[0]['ticker']}")
except Exception as e:
    print(f"   ❌ Erro: {e}")

print("\n✅ Teste concluído!")
