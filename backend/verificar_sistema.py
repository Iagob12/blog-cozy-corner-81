"""
Verificação Rápida do Sistema
Testa se todos os componentes estão funcionando
"""
import os
import json
from datetime import datetime

def verificar_arquivos():
    """Verifica se arquivos essenciais existem"""
    print("\n" + "="*80)
    print("VERIFICAÇÃO DE ARQUIVOS")
    print("="*80)
    
    arquivos = {
        "CSV de Empresas": "data/stocks.csv",
        "Ranking Cache": "data/ranking_cache.json",
        "Resultado V4": "data/alpha_v4_resultado.json",
        "Sistema V4 Otimizado": "app/services/alpha_v4_otimizado.py",
        "Script Integrado": "SISTEMA_FINAL_INTEGRADO.py",
        ".env": ".env"
    }
    
    todos_ok = True
    for nome, caminho in arquivos.items():
        existe = os.path.exists(caminho)
        status = "✓" if existe else "✗"
        print(f"{status} {nome}: {caminho}")
        if not existe:
            todos_ok = False
    
    return todos_ok

def verificar_ranking_cache():
    """Verifica conteúdo do ranking_cache.json"""
    print("\n" + "="*80)
    print("VERIFICAÇÃO DO RANKING CACHE")
    print("="*80)
    
    try:
        with open("data/ranking_cache.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"✓ Arquivo válido (JSON)")
        print(f"✓ Total de empresas: {data.get('total_aprovadas', 0)}")
        print(f"✓ Empresas no ranking: {len(data.get('ranking', []))}")
        print(f"✓ Timestamp: {data.get('timestamp', 'N/A')}")
        
        # Verifica idade do cache
        if data.get('timestamp'):
            timestamp = datetime.fromisoformat(data['timestamp'])
            idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
            print(f"✓ Idade do cache: {idade_horas:.1f} horas")
            
            if idade_horas > 24:
                print(f"⚠ Cache antigo (>24h) - Execute SISTEMA_FINAL_INTEGRADO.py")
        
        # Mostra Top 3
        if data.get('ranking'):
            print(f"\nTop 3:")
            for i, empresa in enumerate(data['ranking'][:3], 1):
                ticker = empresa.get('ticker', 'N/A')
                score = empresa.get('efficiency_score', 0)
                rec = empresa.get('recomendacao_final', 'N/A')
                print(f"  {i}. {ticker} - Score: {score:.1f} - {rec}")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro ao ler ranking_cache.json: {e}")
        return False

def verificar_env():
    """Verifica variáveis de ambiente"""
    print("\n" + "="*80)
    print("VERIFICAÇÃO DE VARIÁVEIS DE AMBIENTE")
    print("="*80)
    
    from dotenv import load_dotenv
    load_dotenv()
    
    # Nota: Groq keys estão hardcoded no multi_groq_client.py
    print("ℹ Groq Keys: Hardcoded no multi_groq_client.py (6 chaves)")
    
    vars_necessarias = {
        "BRAPI_TOKEN": "Brapi Token"
    }
    
    todos_ok = True
    for var, nome in vars_necessarias.items():
        valor = os.getenv(var)
        if valor:
            print(f"✓ {nome}: {valor[:10]}...")
        else:
            print(f"✗ {nome}: NÃO CONFIGURADO")
            todos_ok = False
    
    return todos_ok

def verificar_csv():
    """Verifica CSV de empresas"""
    print("\n" + "="*80)
    print("VERIFICAÇÃO DO CSV")
    print("="*80)
    
    try:
        import pandas as pd
        df = pd.read_csv("data/stocks.csv")
        
        print(f"✓ CSV válido")
        print(f"✓ Total de empresas: {len(df)}")
        print(f"✓ Colunas: {', '.join(df.columns.tolist())}")
        
        # Verifica colunas essenciais
        colunas_necessarias = ['ticker', 'roe', 'pl', 'cagr', 'setor']
        faltando = [col for col in colunas_necessarias if col not in df.columns]
        
        if faltando:
            print(f"⚠ Colunas faltando: {', '.join(faltando)}")
            return False
        
        print(f"✓ Todas as colunas necessárias presentes")
        
        # Mostra amostra
        print(f"\nAmostra (primeiras 3 empresas):")
        for _, row in df.head(3).iterrows():
            print(f"  {row['ticker']}: ROE={row['roe']:.2%}, P/L={row['pl']:.2f}")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro ao ler CSV: {e}")
        return False

def main():
    """Executa todas as verificações"""
    print("\n" + "="*80)
    print("VERIFICAÇÃO COMPLETA DO SISTEMA ALPHA V4")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80)
    
    resultados = {
        "Arquivos": verificar_arquivos(),
        "Ranking Cache": verificar_ranking_cache(),
        "Variáveis de Ambiente": verificar_env(),
        "CSV": verificar_csv()
    }
    
    print("\n" + "="*80)
    print("RESUMO")
    print("="*80)
    
    for nome, ok in resultados.items():
        status = "✓ OK" if ok else "✗ ERRO"
        print(f"{status} - {nome}")
    
    todos_ok = all(resultados.values())
    
    print("\n" + "="*80)
    if todos_ok:
        print("✓ SISTEMA 100% FUNCIONAL")
        print("\nPróximos passos:")
        print("1. Iniciar backend: python -m uvicorn app.main:app --reload --port 8000")
        print("2. Iniciar frontend: npm run dev")
        print("3. Acessar: http://localhost:8080")
    else:
        print("✗ SISTEMA COM PROBLEMAS")
        print("\nCorreções necessárias:")
        for nome, ok in resultados.items():
            if not ok:
                print(f"  - Corrigir: {nome}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
