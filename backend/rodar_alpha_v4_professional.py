"""
Script para rodar Alpha System V4 Professional
Sistema completo em 5 passos com prompts de nível institucional
"""
import asyncio
import sys
import os
import json
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

# Adiciona ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_system_v4_professional import get_alpha_system_v4

async def main():
    """Executa análise completa V4"""
    print("\n" + "="*80)
    print("ALPHA SYSTEM V4 - PROFESSIONAL GRADE")
    print("Sistema de Análise em 5 Passos")
    print("="*80 + "\n")
    
    # Inicializa sistema
    alpha_v4 = get_alpha_system_v4()
    
    # Executa análise completa
    resultado = await alpha_v4.executar_analise_completa_v4()
    
    # Salva resultado completo
    output_file = "data/alpha_v4_resultado_completo.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ Resultado completo salvo em: {output_file}")
    
    # Mostra resumo
    print(f"\n{'='*80}")
    print(f"RESUMO EXECUTIVO")
    print(f"{'='*80}")
    
    print(f"\nCONTEXTO GLOBAL:")
    print(f"   {resultado['contexto_global'].get('resumo_executivo', 'N/A')}")
    
    print(f"\nEMPRESAS FILTRADAS: {len(resultado['empresas_filtradas'])}")
    print(f"   {', '.join(resultado['empresas_filtradas'][:10])}...")
    
    print(f"\nANALISES PROFUNDAS: {len(resultado['analises_profundas'])}")
    
    print(f"\nTOP 5 RANKING:")
    for empresa in resultado['ranking'][:5]:
        ticker = empresa.get('ticker', 'N/A')
        score = empresa.get('score', 0)
        recomendacao = empresa.get('recomendacao', 'N/A')
        upside = empresa.get('upside_potencial', 0)
        tese = empresa.get('tese_investimento', 'N/A')[:80]
        print(f"\n   {empresa['rank']}. {ticker} - Score: {score:.1f}/10 - {recomendacao}")
        print(f"      Upside: {upside:.1f}%")
        print(f"      Tese: {tese}...")
    
    print(f"\nESTRATEGIAS CRIADAS: {len(resultado['estrategias'])}")
    
    if resultado['estrategias']:
        print(f"\nESTRATEGIA #1 ({resultado['estrategias'][0]['ticker']}):")
        estrategia = resultado['estrategias'][0]['estrategia']
        print(f"   {estrategia.get('resumo_estrategia', 'N/A')}")
    
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(main())
