"""
SISTEMA FINAL INTEGRADO
Executa análise V4 otimizada e atualiza frontend automaticamente
"""
import asyncio
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_v4_otimizado import get_alpha_v4_otimizado

async def executar_sistema_completo():
    """Executa sistema completo e atualiza frontend"""
    print("\n" + "="*80)
    print("SISTEMA FINAL INTEGRADO - ALPHA V4 OTIMIZADO")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    try:
        # 1. Executa análise V4 otimizada
        print("PASSO 1: Executando analise V4 otimizada...")
        alpha_v4 = get_alpha_v4_otimizado()
        resultado = await alpha_v4.executar_analise_rapida(limite_empresas=15)
        
        if not resultado['success']:
            print(f"ERRO: {resultado.get('error')}")
            return False
        
        # 2. Converte para formato frontend
        print("\nPASSO 2: Convertendo para formato frontend...")
        ranking_frontend = converter_para_frontend(resultado)
        
        # 3. Salva ranking_cache.json
        print("\nPASSO 3: Salvando ranking_cache.json...")
        with open('data/ranking_cache.json', 'w', encoding='utf-8') as f:
            json.dump(ranking_frontend, f, indent=2, ensure_ascii=False)
        
        print("OK ranking_cache.json atualizado")
        
        # 4. Salva resultado completo
        print("\nPASSO 4: Salvando resultado completo...")
        with open('data/alpha_v4_resultado.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
        
        print("OK alpha_v4_resultado.json salvo")
        
        # 5. Mostra resumo
        print("\n" + "="*80)
        print("RESUMO EXECUTIVO")
        print("="*80)
        
        print(f"\nContexto Global:")
        print(f"  {resultado['contexto_global'].get('resumo_executivo', 'N/A')[:100]}...")
        
        print(f"\nEmpresas Analisadas: {resultado['total']}")
        print(f"Tempo Total: {resultado['tempo_segundos']:.1f}s")
        
        print(f"\nTOP 5 RANKING:")
        for empresa in resultado['ranking'][:5]:
            ticker = empresa.get('ticker', 'N/A')
            score = empresa.get('score', 0)
            rec = empresa.get('recomendacao', 'N/A')
            upside = empresa.get('upside', 0)
            print(f"  {empresa.get('rank', 0)}. {ticker:6s} - Score: {score:4.1f} - {rec:8s} - Upside: {upside:5.1f}%")
        
        print("\n" + "="*80)
        print("SISTEMA EXECUTADO COM SUCESSO!")
        print(f"Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*80 + "\n")
        
        print("PROXIMOS PASSOS:")
        print("1. Acesse http://localhost:8080 para ver o ranking")
        print("2. O frontend deve carregar automaticamente")
        print("3. Se nao carregar, reinicie o frontend (npm run dev)")
        
        return True
    
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        return False

def converter_para_frontend(resultado: dict) -> dict:
    """Converte resultado V4 para formato frontend"""
    df = pd.read_csv("data/stocks.csv")
    
    ranking_convertido = []
    
    for empresa in resultado['ranking']:
        ticker = empresa.get('ticker', 'N/A')
        
        # Busca dados do CSV
        row = df[df['ticker'] == ticker]
        if row.empty:
            continue
        
        row = row.iloc[0]
        
        # Cria objeto TopPick
        top_pick = {
            "ticker": ticker,
            "efficiency_score": float(empresa.get('score', 0)),
            "macro_weight": 1.0,
            "catalisadores": [empresa.get('tese', '')],
            "preco_teto": float(empresa.get('preco_teto', 0)),
            "preco_atual": float(empresa.get('preco_atual', 0)),
            "upside_potencial": float(empresa.get('upside', 0)),
            "sentiment_status": "Normal",
            "recomendacao_final": empresa.get('recomendacao', 'AGUARDAR'),
            "setor": str(row.get('setor', 'N/A')),
            "roe": float(empresa.get('roe', 0)),
            "cagr": float(row['cagr'] * 100 if row['cagr'] < 1 else row['cagr']),
            "pl": float(empresa.get('pl', 0)),
            "tempo_estimado_dias": 90,
            "sentiment_ratio": 1.0,
            "variacao_30d": 0.0,
            "rank": empresa.get('rank', 0)
        }
        
        ranking_convertido.append(top_pick)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_aprovadas": len(ranking_convertido),
        "ranking": ranking_convertido,
        "versao": "4.0-otimizado"
    }

if __name__ == "__main__":
    sucesso = asyncio.run(executar_sistema_completo())
    sys.exit(0 if sucesso else 1)
