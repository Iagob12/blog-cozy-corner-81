"""
TESTE DO SISTEMA - Alpha V4 Otimizado
Executa análise completa e mostra resultados
"""
import asyncio
import sys
import os

# Adiciona path do backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_v4_otimizado import get_alpha_v4_otimizado


async def testar_sistema():
    """Testa sistema completo"""
    print("\n" + "="*80)
    print("TESTE DO SISTEMA - ALPHA V4 OTIMIZADO")
    print("="*80 + "\n")
    
    try:
        # Instancia sistema
        print("📦 Carregando sistema...")
        alpha_v4 = get_alpha_v4_otimizado()
        print("✓ Sistema carregado\n")
        
        # Executa análise (sem limite = TODAS as empresas)
        print("🚀 Iniciando análise completa...")
        print("⚠️  Analisando TODAS as empresas que passarem no filtro\n")
        
        resultado = await alpha_v4.executar_analise_rapida(limite_empresas=None)
        
        if not resultado['success']:
            print(f"\n❌ ERRO: {resultado.get('error')}")
            return
        
        # Mostra resultados
        print("\n" + "="*80)
        print("RESULTADOS DA ANÁLISE")
        print("="*80 + "\n")
        
        ranking = resultado['ranking']
        total = resultado['total']
        tempo = resultado['tempo_segundos']
        
        print(f"✅ Análise concluída em {tempo:.1f}s")
        print(f"📊 Total de empresas aprovadas: {total}\n")
        
        if total == 0:
            print("⚠️  Nenhuma empresa aprovada (nota < 6)")
            return
        
        # Top 10
        print("🏆 TOP 10 EMPRESAS:\n")
        for i, empresa in enumerate(ranking[:10], 1):
            ticker = empresa.get('ticker', 'N/A')
            nota = empresa.get('nota', 0)
            recomendacao = empresa.get('recomendacao', 'N/A')
            preco_atual = empresa.get('preco_atual', 0)
            preco_teto = empresa.get('preco_teto', 0)
            upside = empresa.get('upside', 0)
            
            print(f"{i:2d}. {ticker:8s} | Nota: {nota:.1f}/10 | {recomendacao:15s}")
            print(f"    Preço: R$ {preco_atual:7.2f} → R$ {preco_teto:7.2f} (Upside: {upside:5.1f}%)")
            
            tese = empresa.get('tese_resumida', '')
            if tese:
                # Limita tese a 100 caracteres
                tese_curta = tese[:100] + "..." if len(tese) > 100 else tese
                print(f"    Tese: {tese_curta}")
            print()
        
        # Estatísticas
        print("\n" + "="*80)
        print("ESTATÍSTICAS")
        print("="*80 + "\n")
        
        notas = [e.get('nota', 0) for e in ranking]
        nota_media = sum(notas) / len(notas) if notas else 0
        nota_max = max(notas) if notas else 0
        nota_min = min(notas) if notas else 0
        
        print(f"Nota média: {nota_media:.2f}/10")
        print(f"Nota máxima: {nota_max:.2f}/10")
        print(f"Nota mínima: {nota_min:.2f}/10")
        
        # Distribuição por recomendação
        recomendacoes = {}
        for e in ranking:
            rec = e.get('recomendacao', 'N/A')
            recomendacoes[rec] = recomendacoes.get(rec, 0) + 1
        
        print("\nDistribuição por recomendação:")
        for rec, count in sorted(recomendacoes.items(), key=lambda x: x[1], reverse=True):
            print(f"  {rec:15s}: {count:3d} empresas")
        
        print("\n" + "="*80)
        print("✅ TESTE CONCLUÍDO COM SUCESSO")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(testar_sistema())
