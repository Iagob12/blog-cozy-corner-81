"""
SCRIPT PRINCIPAL — ALPHA SYSTEM V5 COMPLETO
Executa análise completa com metodologia avançada
"""
import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_system_v5_completo import get_alpha_system_v5


async def main():
    """Executa análise completa V5"""
    print("\n" + "="*80)
    print("ALPHA SYSTEM V5 — METODOLOGIA COMPLETA")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    print("CARACTERÍSTICAS:")
    print("- Gestão de contexto persistente entre etapas")
    print("- Perfis operacionais A/B separados")
    print("- Prompts profundos (metodologia avançada)")
    print("- Etapa 4: Estratégia operacional (entrada/saída/stop/R/R)")
    print("- Critérios rigorosos: Nota < 6 = descarte, R/R < 2.0 = não executar")
    print("\n" + "="*80 + "\n")
    
    # Configurações
    PERFIL = "A+B"  # "A" (momentum), "B" (position) ou "A+B" (ambos)
    LIMITE_EMPRESAS = 5  # REDUZIDO PARA 5 (rate limit Gemini: 5 req/min)
    FORCAR_NOVA_MACRO = False  # True para ignorar cache de 24h
    
    print(f"CONFIGURAÇÕES:")
    print(f"  Perfil: {PERFIL}")
    print(f"  Limite de empresas: {LIMITE_EMPRESAS}")
    print(f"  Forçar nova análise macro: {FORCAR_NOVA_MACRO}")
    print("\n" + "="*80 + "\n")
    
    try:
        # Cria instância do sistema
        alpha_v5 = get_alpha_system_v5()
        
        # Executa análise completa
        resultado = await alpha_v5.executar_analise_completa(
            perfil=PERFIL,
            limite_empresas=LIMITE_EMPRESAS,
            forcar_nova_macro=FORCAR_NOVA_MACRO
        )
        
        if resultado.get('success'):
            print("\n" + "="*80)
            print("✓ ANÁLISE CONCLUÍDA COM SUCESSO!")
            print("="*80 + "\n")
            
            # Mostra estatísticas
            print("ESTATÍSTICAS:")
            print(f"  Tempo total: {resultado['tempo_segundos']:.1f}s")
            print(f"  Empresas analisadas: {resultado['total_analisadas']}")
            print(f"  Empresas aprovadas (nota >= 6): {resultado['total_aprovadas']}")
            print(f"  Estratégias executáveis (R/R >= 2.0): {resultado['total_executaveis']}")
            
            # Top 5 estratégias
            if resultado.get('etapa_4_estrategia', {}).get('ranking'):
                print(f"\n  TOP 5 ESTRATÉGIAS:")
                for item in resultado['etapa_4_estrategia']['ranking'][:5]:
                    ticker = item['ticker']
                    rr = item['risco_retorno']
                    upside = item['upside_conservador']
                    convicao = item['convicao']
                    print(f"    {item['posicao']}. {ticker:6s} - R/R {rr:4.2f} - Upside {upside:5.1f}% - {convicao}")
            
            # Carteira sugerida
            if resultado.get('etapa_4_estrategia', {}).get('carteira'):
                carteira = resultado['etapa_4_estrategia']['carteira']
                print(f"\n  CARTEIRA SUGERIDA:")
                print(f"    Total alocado: {carteira.get('total_alocado_pct', 0):.1f}%")
                print(f"    Caixa reserva: {carteira.get('caixa_reserva_pct', 0):.1f}%")
                print(f"    Total posições: {carteira.get('total_posicoes', 0)}")
            
            print("\n" + "="*80)
            print("ARQUIVOS GERADOS:")
            print("  - data/resultados/alpha_v5_latest.json (resultado completo)")
            print("  - data/contexto/contexto_atual.json (contexto persistente)")
            print("  - data/contexto/contexto_atual.txt (contexto formatado)")
            print("="*80 + "\n")
            
            print("PRÓXIMOS PASSOS:")
            print("  1. Revisar estratégias em data/resultados/alpha_v5_latest.json")
            print("  2. Executar apenas operações com R/R >= 2.0")
            print("  3. Respeitar stops rigorosamente")
            print("  4. Revisar carteira mensalmente (Etapa 5)")
            print("\n" + "="*80 + "\n")
            
            return 0
        else:
            print("\n" + "="*80)
            print("✗ ERRO NA ANÁLISE")
            print("="*80)
            print(f"Erro: {resultado.get('erro', 'Desconhecido')}")
            return 1
    
    except Exception as e:
        print("\n" + "="*80)
        print("✗ ERRO CRÍTICO")
        print("="*80)
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
