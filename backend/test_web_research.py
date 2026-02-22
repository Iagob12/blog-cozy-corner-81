"""
Teste do Web Research Service
"""
import asyncio
from app.services.web_research_service import WebResearchService


async def main():
    print("\n" + "="*60)
    print("TESTE: WEB RESEARCH SERVICE")
    print("="*60 + "\n")
    
    service = WebResearchService()
    
    # Testa pesquisa de uma empresa
    print("Testando pesquisa: PETR4 (Petrobras)")
    
    resultado = await service.pesquisar_empresa_completo(
        ticker="PETR4",
        nome_empresa="Petrobras"
    )
    
    if resultado.get('success'):
        print("\n✓ Pesquisa concluída com sucesso!")
        print(f"\nTexto formatado ({len(resultado['texto_completo'])} chars):")
        print("-" * 60)
        print(resultado['texto_completo'][:1000])
        print("...")
        print("-" * 60)
    else:
        print(f"\n✗ Erro: {resultado.get('error')}")
    
    print("\n" + "="*60)
    print("TESTE CONCLUÍDO")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
