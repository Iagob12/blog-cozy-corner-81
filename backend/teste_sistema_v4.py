"""
Teste Rápido do Sistema V4 - Verifica se pode executar
"""
import asyncio
import sys
from app.services.alpha_v4_otimizado import get_alpha_v4_otimizado

async def teste_rapido():
    """Testa componentes do sistema V4"""
    print("\n" + "="*80)
    print("TESTE RÁPIDO DO SISTEMA V4")
    print("="*80 + "\n")
    
    try:
        # 1. Instancia sistema
        print("1. Instanciando sistema V4...")
        alpha_v4 = get_alpha_v4_otimizado()
        print("   ✓ Sistema V4 instanciado")
        
        # 2. Testa filtro rápido
        print("\n2. Testando filtro rápido...")
        empresas = alpha_v4._filtro_rapido(5)
        print(f"   ✓ Filtro retornou {len(empresas)} empresas: {empresas}")
        
        # 3. Testa cache macro
        print("\n3. Testando cache macro...")
        contexto = await alpha_v4._analise_macro_cached()
        print(f"   ✓ Contexto macro: {contexto.get('resumo_executivo', 'N/A')[:80]}...")
        
        print("\n" + "="*80)
        print("✓ SISTEMA V4 FUNCIONANDO - PRONTO PARA EXECUTAR ANÁLISE COMPLETA")
        print("="*80 + "\n")
        
        print("Para executar análise completa:")
        print("  python SISTEMA_FINAL_INTEGRADO.py")
        
        return True
    
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "="*80)
        print("✗ SISTEMA V4 COM PROBLEMAS")
        print("="*80 + "\n")
        
        return False

if __name__ == "__main__":
    sucesso = asyncio.run(teste_rapido())
    sys.exit(0 if sucesso else 1)
