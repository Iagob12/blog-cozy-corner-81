"""
Script para rodar nova análise com prompts melhorados
"""
import asyncio
import json
from datetime import datetime

async def main():
    print("="*70)
    print("  RODANDO NOVA ANÁLISE COM PROMPTS MELHORADOS")
    print("="*70)
    print()
    
    # Carrega empresas aprovadas
    with open('data/empresas_aprovadas.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    empresas = dados.get("empresas", [])
    print(f"✓ {len(empresas)} empresas para analisar")
    print()
    
    # Executa análise incremental
    from app.services.analise_automatica import get_analise_automatica_service
    
    service = get_analise_automatica_service()
    
    resultado = await service.analisar_incrementalmente(
        empresas=empresas,
        forcar_reanalise=True,  # Força reanálise com novos prompts
        max_paralelo=1  # 1 por vez
    )
    
    print()
    print("="*70)
    print("  ANÁLISE CONCLUÍDA!")
    print("="*70)
    print(f"✓ Analisadas: {resultado['novas_analises']}")
    print(f"❌ Falhas: {resultado['falhas']}")
    print(f"🏆 Ranking: {resultado['total_ranking']} empresas")
    print()
    
    # Converte ranking para formato TopPick
    print("Convertendo ranking...")
    import subprocess
    subprocess.run(["python", "converter_ranking.py"], check=True)
    
    print()
    print("✅ PRONTO! Ranking atualizado com prompts melhorados!")
    print("🚀 Reinicie o backend para carregar novo ranking")

if __name__ == "__main__":
    asyncio.run(main())
