"""
TESTE DO ALPHA V4 COM GEMINI
Testa o sistema com controle de rate limit
"""
import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Carrega .env
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_v4_otimizado import AlphaV4Otimizado


async def testar_sistema():
    """Testa o sistema Alpha V4 com Gemini"""
    print("\n" + "="*80)
    print("TESTE ALPHA V4 COM GEMINI API")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    print("CONFIGURACAO:")
    print("  - API: Gemini 2.5 Flash")
    print("  - Rate Limit: 5 req/min por chave")
    print("  - Total: 6 chaves = 30 req/min")
    print("  - Delay: 2s entre requisicoes")
    print("  - Empresas: TODAS que passarem no filtro")
    print("\n" + "="*80 + "\n")
    
    try:
        # Cria instancia
        sistema = AlphaV4Otimizado()
        
        # Executa analise (sem limite)
        print("Iniciando analise completa...\n")
        resultado = await sistema.executar_analise_rapida()
        
        if resultado.get('success'):
            print("\n" + "="*80)
            print("TESTE CONCLUIDO COM SUCESSO!")
            print("="*80 + "\n")
            
            # Mostra estatisticas
            print("ESTATISTICAS:")
            print(f"  Tempo total: {resultado.get('tempo_segundos', 0):.1f}s")
            print(f"  Empresas analisadas: {resultado.get('total_analisadas', 0)}")
            print(f"  Empresas aprovadas: {resultado.get('total_aprovadas', 0)}")
            
            # Mostra ranking
            ranking = resultado.get('ranking', [])
            if ranking:
                print(f"\nTOP 5 RANKING:")
                for i, empresa in enumerate(ranking[:5], 1):
                    ticker = empresa.get('ticker', 'N/A')
                    nota = empresa.get('nota', 0)
                    rec = empresa.get('recomendacao', 'N/A')
                    upside = empresa.get('upside', 0)
                    print(f"  {i}. {ticker} - Nota {nota:.1f}/10 - {rec} - Upside {upside:.1f}%")
            
            print("\n" + "="*80 + "\n")
            return 0
        else:
            print("\n" + "="*80)
            print("ERRO NO TESTE")
            print("="*80)
            print(f"Erro: {resultado.get('error', 'Erro desconhecido')}")
            print("\n" + "="*80 + "\n")
            return 1
    
    except KeyboardInterrupt:
        print("\n\n[INTERROMPIDO] Teste cancelado pelo usuario")
        return 130
    
    except Exception as e:
        print("\n" + "="*80)
        print("ERRO CRITICO")
        print("="*80)
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "="*80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(testar_sistema())
    sys.exit(exit_code)
