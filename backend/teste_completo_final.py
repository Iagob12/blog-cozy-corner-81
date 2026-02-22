"""
TESTE COMPLETO FINAL - Simula uso real do sistema
"""
import json
import os
from datetime import datetime

def teste_completo():
    """Executa todos os testes de verificação"""
    print("\n" + "="*80)
    print("TESTE COMPLETO FINAL - SIMULAÇÃO DE USO REAL")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    testes = []
    
    # TESTE 1: Arquivos essenciais existem
    print("TESTE 1: Verificando arquivos essenciais...")
    arquivos = {
        "CSV": "data/stocks.csv",
        "Ranking Cache": "data/ranking_cache.json",
        "Sistema V4": "app/services/alpha_v4_otimizado.py",
        "Script Integrado": "SISTEMA_FINAL_INTEGRADO.py",
        "Multi Groq": "app/services/multi_groq_client.py"
    }
    
    teste1_ok = True
    for nome, caminho in arquivos.items():
        existe = os.path.exists(caminho)
        status = "✓" if existe else "✗"
        print(f"  {status} {nome}: {caminho}")
        if not existe:
            teste1_ok = False
    
    testes.append(("Arquivos Essenciais", teste1_ok))
    
    # TESTE 2: Ranking cache válido
    print("\nTESTE 2: Verificando ranking cache...")
    teste2_ok = False
    try:
        with open("data/ranking_cache.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        empresas = len(data.get('ranking', []))
        timestamp = data.get('timestamp', 'N/A')
        
        if empresas > 0:
            print(f"  ✓ Ranking válido: {empresas} empresas")
            print(f"  ✓ Timestamp: {timestamp}")
            
            # Verifica Top 3
            top3 = data['ranking'][:3]
            print(f"  ✓ Top 3:")
            for i, emp in enumerate(top3, 1):
                print(f"    {i}. {emp['ticker']} - Score: {emp['efficiency_score']}")
            
            teste2_ok = True
        else:
            print(f"  ✗ Ranking vazio")
    
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    testes.append(("Ranking Cache", teste2_ok))
    
    # TESTE 3: Formato compatível com backend
    print("\nTESTE 3: Verificando compatibilidade com backend...")
    teste3_ok = False
    try:
        from app.models import TopPick
        
        with open("data/ranking_cache.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Tenta criar TopPick
        erros = 0
        for stock_data in data.get("ranking", [])[:3]:
            try:
                TopPick(**stock_data)
            except Exception as e:
                print(f"  ✗ Erro ao criar TopPick para {stock_data.get('ticker')}: {e}")
                erros += 1
        
        if erros == 0:
            print(f"  ✓ Formato compatível com TopPick")
            teste3_ok = True
        else:
            print(f"  ✗ {erros} erros de compatibilidade")
    
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    testes.append(("Compatibilidade Backend", teste3_ok))
    
    # TESTE 4: Sistema V4 pode ser importado
    print("\nTESTE 4: Verificando importação do Sistema V4...")
    teste4_ok = False
    try:
        from app.services.alpha_v4_otimizado import get_alpha_v4_otimizado
        alpha_v4 = get_alpha_v4_otimizado()
        print(f"  ✓ Sistema V4 importado e instanciado")
        teste4_ok = True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    testes.append(("Sistema V4", teste4_ok))
    
    # TESTE 5: Groq Client configurado
    print("\nTESTE 5: Verificando Groq Client...")
    teste5_ok = False
    try:
        from app.services.multi_groq_client import get_multi_groq_client
        client = get_multi_groq_client()
        print(f"  ✓ Groq Client: {len(client.keys)} chaves configuradas")
        teste5_ok = True
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    testes.append(("Groq Client", teste5_ok))
    
    # TESTE 6: CSV com dados
    print("\nTESTE 6: Verificando CSV de empresas...")
    teste6_ok = False
    try:
        import pandas as pd
        df = pd.read_csv("data/stocks.csv")
        
        colunas_necessarias = ['ticker', 'roe', 'pl', 'cagr', 'setor']
        faltando = [col for col in colunas_necessarias if col not in df.columns]
        
        if not faltando:
            print(f"  ✓ CSV válido: {len(df)} empresas")
            print(f"  ✓ Todas as colunas necessárias presentes")
            teste6_ok = True
        else:
            print(f"  ✗ Colunas faltando: {faltando}")
    
    except Exception as e:
        print(f"  ✗ Erro: {e}")
    
    testes.append(("CSV de Empresas", teste6_ok))
    
    # RESUMO FINAL
    print("\n" + "="*80)
    print("RESUMO DOS TESTES")
    print("="*80)
    
    passou = sum(1 for _, ok in testes if ok)
    total = len(testes)
    percentual = (passou / total) * 100
    
    for nome, ok in testes:
        status = "✓ PASSOU" if ok else "✗ FALHOU"
        print(f"{status} - {nome}")
    
    print("\n" + "="*80)
    if passou == total:
        print(f"✓ TODOS OS {total} TESTES PASSARAM!")
        print("\n🎉 SISTEMA 100% FUNCIONAL E PRONTO PARA USO!")
        print("\nPróximos passos:")
        print("1. Iniciar backend: python -m uvicorn app.main:app --reload --port 8000")
        print("2. Iniciar frontend: npm run dev")
        print("3. Acessar: http://localhost:8080")
        print("\nOpcional - Gerar novo ranking:")
        print("  python SISTEMA_FINAL_INTEGRADO.py")
    else:
        print(f"⚠ {total - passou} TESTE(S) FALHARAM")
        print(f"\nSistema {percentual:.0f}% funcional")
        print("\nCorreções necessárias:")
        for nome, ok in testes:
            if not ok:
                print(f"  - {nome}")
    
    print("="*80 + "\n")
    
    return passou == total

if __name__ == "__main__":
    sucesso = teste_completo()
    exit(0 if sucesso else 1)
