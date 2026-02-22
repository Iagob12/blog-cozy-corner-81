"""
SISTEMA COMPLETO AUTOMÁTICO - ALPHA V4 PROFESSIONAL

Executa análise completa em 5 passos e atualiza o ranking automaticamente
Pode ser rodado manualmente ou agendado para rodar periodicamente
"""
import asyncio
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

# Adiciona ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_system_v4_professional import get_alpha_system_v4

async def executar_sistema_completo():
    """
    Executa sistema completo:
    1. Análise de Tendências Globais
    2. Filtro Inteligente de Empresas
    3. Análise Profunda Individual (com release se disponível)
    4. Ranking por Score
    5. Estratégia de Operação
    """
    print("\n" + "="*80)
    print("SISTEMA COMPLETO AUTOMATICO - ALPHA V4 PROFESSIONAL")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    try:
        # Inicializa sistema V4
        alpha_v4 = get_alpha_system_v4()
        
        # Executa análise completa em 5 passos
        print("Executando análise completa em 5 passos...")
        resultado = await alpha_v4.executar_analise_completa_v4()
        
        # Salva resultado completo
        output_file = "data/alpha_v4_resultado_completo.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\nResultado completo salvo em: {output_file}")
        
        # Converte para formato do ranking_cache.json (para o frontend)
        print("\nConvertendo para formato do frontend...")
        ranking_frontend = converter_para_frontend(resultado)
        
        # Salva ranking para o frontend
        ranking_file = "data/ranking_cache.json"
        with open(ranking_file, 'w', encoding='utf-8') as f:
            json.dump(ranking_frontend, f, indent=2, ensure_ascii=False)
        
        print(f"Ranking salvo em: {ranking_file}")
        
        # Mostra resumo
        mostrar_resumo(resultado)
        
        print("\n" + "="*80)
        print("SISTEMA EXECUTADO COM SUCESSO!")
        print(f"Finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*80 + "\n")
        
        return True
    
    except Exception as e:
        print(f"\nERRO ao executar sistema: {e}")
        import traceback
        traceback.print_exc()
        return False

def converter_para_frontend(resultado: dict) -> dict:
    """
    Converte resultado V4 para formato esperado pelo frontend
    """
    import pandas as pd
    
    # Carrega CSV para dados adicionais
    df = pd.read_csv("data/stocks.csv")
    
    ranking_convertido = []
    
    for empresa in resultado['ranking'][:20]:  # Top 20
        ticker = empresa.get('ticker', 'N/A')
        
        # Busca dados do CSV
        row = df[df['ticker'] == ticker]
        if row.empty:
            continue
        
        row = row.iloc[0]
        
        # Busca estratégia (se disponível)
        estrategia = None
        for est in resultado.get('estrategias', []):
            if est['ticker'] == ticker:
                estrategia = est['estrategia']
                break
        
        # Cria objeto TopPick
        top_pick = {
            "ticker": ticker,
            "efficiency_score": float(empresa.get('score', 0)),
            "macro_weight": 1.0,
            "catalisadores": [cat.get('descricao', '') for cat in empresa.get('catalisadores', [])],
            "preco_teto": float(empresa.get('preco_teto', 0)),
            "preco_atual": float(empresa.get('preco_atual', 0)),
            "upside_potencial": float(empresa.get('upside_potencial', 0)),
            "sentiment_status": "Normal",
            "recomendacao_final": empresa.get('recomendacao', 'AGUARDAR'),
            "setor": str(row.get('setor', 'N/A')),
            "roe": float(row['roe'] * 100 if row['roe'] < 1 else row['roe']),
            "cagr": float(row['cagr'] * 100 if row['cagr'] < 1 else row['cagr']),
            "pl": float(row['pl']),
            "tempo_estimado_dias": 90,
            "sentiment_ratio": 1.0,
            "variacao_30d": 0.0,
            "rank": empresa.get('rank', 0),
            # Campos extras do V4
            "tese_investimento": empresa.get('tese_investimento', ''),
            "horizonte_recomendado": empresa.get('horizonte_recomendado', '6-12 meses'),
            "estrategia": estrategia  # Estratégia completa
        }
        
        ranking_convertido.append(top_pick)
    
    return {
        "timestamp": datetime.now().isoformat(),
        "total_aprovadas": len(ranking_convertido),
        "ranking": ranking_convertido,
        "contexto_global": resultado.get('contexto_global', {}),
        "versao": "4.0-professional"
    }

def mostrar_resumo(resultado: dict):
    """Mostra resumo executivo"""
    print("\n" + "="*80)
    print("RESUMO EXECUTIVO")
    print("="*80)
    
    # Contexto Global
    print("\nCONTEXTO GLOBAL:")
    contexto = resultado.get('contexto_global', {})
    print(f"   {contexto.get('resumo_executivo', 'N/A')}")
    
    # Megatendências
    megatendencias = contexto.get('megatendencias', [])
    if megatendencias:
        print("\nMEGATENDENCIAS IDENTIFICADAS:")
        for i, mega in enumerate(megatendencias[:3], 1):
            print(f"   {i}. {mega.get('nome', 'N/A')}")
    
    # Empresas Filtradas
    print(f"\nEMPRESAS FILTRADAS: {len(resultado.get('empresas_filtradas', []))}")
    
    # Análises Profundas
    print(f"ANALISES PROFUNDAS: {len(resultado.get('analises_profundas', []))}")
    
    # Top 5
    print("\nTOP 5 RANKING:")
    for empresa in resultado.get('ranking', [])[:5]:
        ticker = empresa.get('ticker', 'N/A')
        score = empresa.get('score', 0)
        recomendacao = empresa.get('recomendacao', 'N/A')
        upside = empresa.get('upside_potencial', 0)
        tese = empresa.get('tese_investimento', 'N/A')[:80]
        
        print(f"\n   {empresa.get('rank', 0)}. {ticker} - Score: {score:.1f}/10 - {recomendacao}")
        print(f"      Upside: {upside:.1f}%")
        print(f"      Tese: {tese}...")
    
    # Estratégias
    print(f"\nESTRATEGIAS CRIADAS: {len(resultado.get('estrategias', []))}")

if __name__ == "__main__":
    # Executa sistema
    sucesso = asyncio.run(executar_sistema_completo())
    
    # Exit code
    sys.exit(0 if sucesso else 1)
