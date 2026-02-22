"""
Script de teste para verificar as chaves da Alpha Vantage
"""
import os
from dotenv import load_dotenv
from app.services.market_data import MarketDataService

# Carrega variáveis de ambiente
load_dotenv()

print("=" * 60)
print("TESTE DE CONFIGURAÇÃO - ALPHA VANTAGE")
print("=" * 60)

# Verifica variáveis de ambiente
print("\n1. VARIÁVEIS DE AMBIENTE:")
key1 = os.getenv("ALPHAVANTAGE_API_KEY")
key2 = os.getenv("ALPHAVANTAGE_API_KEY_2")
key3 = os.getenv("ALPHAVANTAGE_API_KEY_3")

print(f"   ALPHAVANTAGE_API_KEY: {key1[:10]}... ✓" if key1 else "   ALPHAVANTAGE_API_KEY: NOT SET ✗")
print(f"   ALPHAVANTAGE_API_KEY_2: {key2[:10]}... ✓" if key2 else "   ALPHAVANTAGE_API_KEY_2: NOT SET ✗")
print(f"   ALPHAVANTAGE_API_KEY_3: {key3[:10]}... ✓" if key3 else "   ALPHAVANTAGE_API_KEY_3: NOT SET ✗")

# Inicializa serviço
print("\n2. INICIALIZANDO MARKET DATA SERVICE:")
service = MarketDataService()

print(f"\n3. RESUMO:")
print(f"   Total de chaves carregadas: {len(service.api_keys)}")
print(f"   Limite de requisições/min: {len(service.api_keys) * 5}")
print(f"   Máximo de ações por consulta: {len(service.api_keys) * 5}")
print(f"   Delay entre requisições: {60 / (len(service.api_keys) * 5):.1f}s")

if len(service.api_keys) == 3:
    print("\n✓ SISTEMA CONFIGURADO CORRETAMENTE!")
    print("✓ Pronto para buscar 15 ações com preços reais")
else:
    print(f"\n✗ ATENÇÃO: Apenas {len(service.api_keys)} chave(s) carregada(s)")
    print("✗ Esperado: 3 chaves")

print("\n" + "=" * 60)
