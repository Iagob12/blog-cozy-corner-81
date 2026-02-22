"""
Teste do Fluxo Completo do Alpha Terminal
"""
import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.portfolio_orchestrator import PortfolioOrchestrator

async def main():
    print("=" * 80)
    print("🚀 ALPHA TERMINAL - TESTE DO FLUXO COMPLETO")
    print("=" * 80)
    print(f"\nInício: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    
    # Verifica API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  AVISO: GEMINI_API_KEY não configurada!")
        print("   Configure no arquivo .env para usar análise de IA\n")
        print("   Obtendo chave: https://makersuite.google.com/app/apikey\n")
        return
    
    orchestrator = PortfolioOrchestrator()
    
    try:
        # Executa o fluxo completo
        resultado = await orchestrator.executar_fluxo_completo()
        
        # Exibe resumo
        print("\n" + "=" * 80)
        print("📊 RESUMO DO RESULTADO")
        print("=" * 80)
        
        if "carteira_final" in resultado:
            print(f"\n✨ CARTEIRA FINAL ({len(resultado['carteira_final'])} ações):\n")
            
            for pos in resultado["carteira_final"]:
                print(f"  {pos['posicao']}. {pos['ticker']}")
                print(f"     Ação: {pos['acao']}")
                print(f"     Preço: R$ {pos.get('preco_atual', 0):.2f}")
                print(f"     Veredito: {pos.get('anti_manada', {}).get('veredito', 'N/A')}")
                print(f"     {pos['justificativa'][:100]}...")
                print()
        
        # Estatísticas
        print("\n📈 ESTATÍSTICAS:")
        etapas = resultado.get("etapas", {})
        print(f"  • Ações analisadas: {etapas.get('dados_coletados', 0)}")
        print(f"  • Top 15 selecionadas: {len(etapas.get('top_15', []))}")
        print(f"  • PDFs processados: {etapas.get('relatorios_processados', 0)}")
        print(f"  • Carteira final: {len(resultado.get('carteira_final', []))}")
        
        # Gera relatório HTML
        print("\n📄 Gerando relatório HTML...")
        html_path = orchestrator.gerar_relatorio_html(resultado)
        print(f"   ✓ Relatório salvo em: {html_path}")
        
        print("\n" + "=" * 80)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        print(f"\nFim: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
