"""
TESTE RÁPIDO — ALPHA SYSTEM V5
Valida que todos os módulos estão funcionando
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("\n" + "="*80)
    print("TESTE 1: IMPORTS")
    print("="*80 + "\n")
    
    try:
        from app.services.context_manager import get_context_manager
        print("✓ ContextManager importado")
        
        from app.services.perfis_operacionais import PerfisOperacionais
        print("✓ PerfisOperacionais importado")
        
        from app.services.estrategia_operacional import get_estrategia_operacional
        print("✓ EstrategiaOperacional importado")
        
        from app.services.revisao_carteira import get_revisao_carteira
        print("✓ RevisaoCarteira importado")
        
        from app.services.alpha_system_v5_completo import get_alpha_system_v5
        print("✓ AlphaSystemV5Completo importado")
        
        print("\n✅ TODOS OS IMPORTS OK\n")
        return True
    
    except Exception as e:
        print(f"\n❌ ERRO NO IMPORT: {e}\n")
        return False


def test_context_manager():
    """Testa ContextManager"""
    print("="*80)
    print("TESTE 2: CONTEXT MANAGER")
    print("="*80 + "\n")
    
    try:
        from app.services.context_manager import get_context_manager
        
        context = get_context_manager()
        print("✓ ContextManager instanciado")
        
        # Inicia novo contexto
        context.iniciar_novo_contexto()
        print("✓ Novo contexto iniciado")
        
        # Atualiza macro
        context.atualizar_etapa_1_macro({
            "cenario_macro": {"resumo": "Teste"},
            "megatendencias": []
        })
        print("✓ Etapa 1 atualizada")
        
        # Obtém contexto texto
        texto = context.obter_contexto_texto()
        assert "[===== CONTEXTO DO DIA =====]" in texto
        print("✓ Contexto texto gerado")
        
        # Obtém contexto JSON
        json_ctx = context.obter_contexto_json()
        assert "data" in json_ctx
        print("✓ Contexto JSON obtido")
        
        print("\n✅ CONTEXT MANAGER OK\n")
        return True
    
    except Exception as e:
        print(f"\n❌ ERRO NO CONTEXT MANAGER: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_perfis_operacionais():
    """Testa PerfisOperacionais"""
    print("="*80)
    print("TESTE 3: PERFIS OPERACIONAIS")
    print("="*80 + "\n")
    
    try:
        from app.services.perfis_operacionais import PerfisOperacionais
        import pandas as pd
        
        # Cria DataFrame de teste
        df = pd.DataFrame({
            'ticker': ['TEST3', 'TEST4'],
            'roe': [0.20, 0.10],
            'pl': [12.0, 18.0],
            'roic': [0.15, 0.08],
            'divida_ebitda': [2.0, 5.0],
            'margem_ebitda': [0.15, 0.05],
            'margem_liquida': [0.10, 0.03],
            'cagr': [0.12, -0.05],
            'liquidez_corrente': [1.5, 0.5]
        })
        print("✓ DataFrame de teste criado")
        
        # Testa eliminação imediata
        df_filtrado, motivos = PerfisOperacionais.aplicar_eliminacao_imediata(df)
        assert len(df_filtrado) < len(df)
        print(f"✓ Eliminação imediata: {len(df)} -> {len(df_filtrado)} empresas")
        
        # Testa identificação de perfil
        perfil = PerfisOperacionais.identificar_perfil(df.iloc[0])
        print(f"✓ Perfil identificado: {perfil}")
        
        # Testa descrição
        desc = PerfisOperacionais.obter_descricao_perfil("A")
        assert "MOMENTUM" in desc
        print(f"✓ Descrição Perfil A: {desc}")
        
        print("\n✅ PERFIS OPERACIONAIS OK\n")
        return True
    
    except Exception as e:
        print(f"\n❌ ERRO NOS PERFIS: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """Testa estrutura de arquivos"""
    print("="*80)
    print("TESTE 4: ESTRUTURA DE ARQUIVOS")
    print("="*80 + "\n")
    
    arquivos_necessarios = [
        "app/services/context_manager.py",
        "app/services/perfis_operacionais.py",
        "app/services/estrategia_operacional.py",
        "app/services/revisao_carteira.py",
        "app/services/alpha_system_v5_completo.py",
        "rodar_alpha_v5_completo.py",
        "rodar_revisao_carteira.py",
        "SISTEMA_V5_DOCUMENTACAO_COMPLETA.md",
        "COMECE_AQUI_V5.md"
    ]
    
    todos_ok = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✓ {arquivo}")
        else:
            print(f"❌ {arquivo} NÃO ENCONTRADO")
            todos_ok = False
    
    if todos_ok:
        print("\n✅ ESTRUTURA DE ARQUIVOS OK\n")
    else:
        print("\n⚠️ ALGUNS ARQUIVOS FALTANDO\n")
    
    return todos_ok


def test_data_directories():
    """Testa diretórios de dados"""
    print("="*80)
    print("TESTE 5: DIRETÓRIOS DE DADOS")
    print("="*80 + "\n")
    
    diretorios = [
        "data",
        "data/cache",
        "data/contexto",
        "data/resultados",
        "data/revisoes"
    ]
    
    for diretorio in diretorios:
        os.makedirs(diretorio, exist_ok=True)
        if os.path.exists(diretorio):
            print(f"✓ {diretorio}/")
        else:
            print(f"❌ {diretorio}/ NÃO CRIADO")
    
    print("\n✅ DIRETÓRIOS OK\n")
    return True


def main():
    """Executa todos os testes"""
    print("\n" + "="*80)
    print("TESTE COMPLETO — ALPHA SYSTEM V5")
    print("="*80 + "\n")
    
    resultados = []
    
    # Teste 1: Imports
    resultados.append(("Imports", test_imports()))
    
    # Teste 2: ContextManager
    resultados.append(("ContextManager", test_context_manager()))
    
    # Teste 3: PerfisOperacionais
    resultados.append(("PerfisOperacionais", test_perfis_operacionais()))
    
    # Teste 4: Estrutura de arquivos
    resultados.append(("Estrutura de Arquivos", test_file_structure()))
    
    # Teste 5: Diretórios
    resultados.append(("Diretórios", test_data_directories()))
    
    # Resumo
    print("="*80)
    print("RESUMO DOS TESTES")
    print("="*80 + "\n")
    
    total = len(resultados)
    passou = sum(1 for _, ok in resultados if ok)
    
    for nome, ok in resultados:
        status = "✅ PASSOU" if ok else "❌ FALHOU"
        print(f"{nome:30s} {status}")
    
    print("\n" + "="*80)
    print(f"RESULTADO FINAL: {passou}/{total} testes passaram")
    print("="*80 + "\n")
    
    if passou == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\nSistema V5 está pronto para uso!")
        print("\nPróximos passos:")
        print("  1. Execute: python rodar_alpha_v5_completo.py")
        print("  2. Veja: COMECE_AQUI_V5.md")
        print("\n" + "="*80 + "\n")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("\nVerifique os erros acima e corrija antes de usar o sistema.")
        print("\n" + "="*80 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
