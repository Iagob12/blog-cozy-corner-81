"""
SCRIPT PRINCIPAL — ALPHA SYSTEM V5 ROBUSTO
Sistema completo com validacao rigorosa e processamento incremental
"""
import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_system_v5_robusto import get_alpha_system_v5_robusto


async def main():
    """Executa analise completa robusta"""
    print("\n" + "="*80)
    print("ALPHA SYSTEM V5 ROBUSTO — SISTEMA COMPLETO")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    print("CARACTERISTICAS:")
    print("- Validacao rigorosa entre etapas (para se falhar)")
    print("- Analisa TODAS as empresas que passaram no filtro")
    print("- Sistema de fila para releases faltantes")
    print("- Processamento incremental (empresas com release avancam)")
    print("- Ranking dinamico atualizado em tempo real")
    print("\n" + "="*80 + "\n")
    
    # Configuracoes
    PERFIL = "A+B"  # "A" (momentum), "B" (position) ou "A+B" (ambos)
    FORCAR_NOVA_MACRO = False  # True para ignorar cache de 24h
    
    print(f"CONFIGURACOES:")
    print(f"  Perfil: {PERFIL}")
    print(f"  Forcar nova analise macro: {FORCAR_NOVA_MACRO}")
    print(f"  Limite de empresas: TODAS que passarem no filtro")
    print("\n" + "="*80 + "\n")
    
    try:
        # Cria instancia do sistema
        alpha_v5 = get_alpha_system_v5_robusto()
        
        # Executa analise completa
        resultado = await alpha_v5.executar_analise_completa(
            perfil=PERFIL,
            forcar_nova_macro=FORCAR_NOVA_MACRO
        )
        
        if resultado.get('success'):
            print("\n" + "="*80)
            print("ANALISE CONCLUIDA COM SUCESSO!")
            print("="*80 + "\n")
            
            return 0
        else:
            print("\n" + "="*80)
            print("ERRO NA ANALISE")
            print("="*80)
            print(f"Etapa que falhou: {resultado.get('etapa_falhou', 'desconhecida')}")
            print(f"Erro: {resultado.get('erro', 'Erro desconhecido')}")
            print("\n" + "="*80 + "\n")
            
            return 1
    
    except KeyboardInterrupt:
        print("\n\n[INTERROMPIDO] Analise cancelada pelo usuario")
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
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
