"""
Teste do Serviço de Dados Fundamentalistas
"""
import asyncio
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.dados_fundamentalistas_service import get_dados_fundamentalistas_service


async def test_uma_empresa():
    """Testa coleta de dados de uma empresa"""
    
    print("\n" + "="*60)
    print("TESTE 1: Uma Empresa (PRIO3)")
    print("="*60)
    
    service = get_dados_fundamentalistas_service()
    
    dados = await service.obter_dados_completos("PRIO3", "PRIO")
    
    print("\n" + "="*60)
    print("DADOS OBTIDOS:")
    print("="*60)
    print(f"\nFontes usadas: {dados.get('fontes_usadas', [])}")
    print(f"\nResumo Estruturado:\n{dados.get('resumo_estruturado', '')}")
    
    # Verifica dados financeiros
    if "financeiro" in dados:
        fin = dados["financeiro"]
        print("\n" + "-"*60)
        print("DADOS FINANCEIROS:")
        print("-"*60)
        print(f"ROE: {fin.get('roe', 'N/A')}%")
        print(f"Margem Líquida: {fin.get('margem_liquida', 'N/A')}%")
        print(f"P/L: {fin.get('pl', 'N/A')}")
        print(f"Setor: {fin.get('setor', 'N/A')}")
    
    # Verifica análise de IA
    if "analise_ia" in dados:
        ia = dados["analise_ia"]
        print("\n" + "-"*60)
        print("ANÁLISE DE IA:")
        print("-"*60)
        
        if ia.get("catalisadores"):
            print(f"\nCatalisadores: {len(ia['catalisadores'])}")
            for cat in ia["catalisadores"][:2]:
                print(f"  - {cat.get('descricao', '')}")
        
        if ia.get("riscos"):
            print(f"\nRiscos: {len(ia['riscos'])}")
            for risco in ia["riscos"][:2]:
                print(f"  - {risco.get('descricao', '')}")


async def test_multiplas_empresas():
    """Testa coleta de dados de múltiplas empresas"""
    
    print("\n\n" + "="*60)
    print("TESTE 2: Múltiplas Empresas (3 empresas)")
    print("="*60)
    
    service = get_dados_fundamentalistas_service()
    
    empresas = [
        {"ticker": "PRIO3", "nome": "PRIO"},
        {"ticker": "VALE3", "nome": "VALE"},
        {"ticker": "PETR4", "nome": "PETROBRAS"}
    ]
    
    dados_multiplas = await service.obter_dados_multiplas_empresas(
        empresas, 
        batch_size=3
    )
    
    print("\n" + "="*60)
    print("RESULTADOS:")
    print("="*60)
    print(f"\nDados obtidos: {len(dados_multiplas)}/3 empresas")
    
    for ticker, dados in dados_multiplas.items():
        fontes = dados.get('fontes_usadas', [])
        print(f"\n{ticker}:")
        print(f"  - Fontes: {', '.join(fontes)}")
        print(f"  - Resumo: {len(dados.get('resumo_estruturado', ''))} caracteres")


async def main():
    """Executa todos os testes"""
    
    print("\n" + "="*60)
    print("TESTE DO SERVIÇO DE DADOS FUNDAMENTALISTAS")
    print("="*60)
    
    try:
        # Teste 1: Uma empresa
        await test_uma_empresa()
        
        # Teste 2: Múltiplas empresas
        await test_multiplas_empresas()
        
        print("\n\n" + "="*60)
        print("✅ TODOS OS TESTES CONCLUÍDOS")
        print("="*60)
    
    except Exception as e:
        print(f"\n\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
