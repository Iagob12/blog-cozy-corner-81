"""
PROCESSADOR DE RELEASES PENDENTES
Processa empresas que estavam aguardando release quando o admin enviar
"""
import asyncio
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.alpha_system_v5_robusto import AlphaSystemV5Robusto


async def processar_pendentes():
    """Processa empresas que estavam aguardando release"""
    print("\n" + "="*80)
    print("PROCESSADOR DE RELEASES PENDENTES")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Carrega lista de pendentes
    pendentes_file = "data/releases_pendentes/lista_pendentes.json"
    
    if not os.path.exists(pendentes_file):
        print("[ERRO] Nenhuma lista de pendentes encontrada")
        print(f"Arquivo esperado: {pendentes_file}")
        return 1
    
    with open(pendentes_file, 'r', encoding='utf-8') as f:
        dados_pendentes = json.load(f)
    
    empresas_pendentes = dados_pendentes.get('empresas', [])
    
    if not empresas_pendentes:
        print("[INFO] Nenhuma empresa pendente")
        return 0
    
    print(f"[INFO] {len(empresas_pendentes)} empresas pendentes encontradas\n")
    
    # Cria instancia do sistema
    sistema = AlphaSystemV5Robusto()
    
    # Verifica quais agora tem release
    com_release_novo = []
    ainda_pendentes = []
    
    for empresa in empresas_pendentes:
        ticker = empresa['ticker']
        release = sistema.release_manager.obter_release_mais_recente(ticker)
        
        if release and release.get('conteudo'):
            com_release_novo.append(empresa)
            print(f"  OK {ticker}: Release disponivel agora")
        else:
            ainda_pendentes.append(empresa)
            print(f"  PENDENTE {ticker}: Ainda sem release")
    
    print(f"\n[RESUMO]")
    print(f"  - Com release novo: {len(com_release_novo)}")
    print(f"  - Ainda pendentes: {len(ainda_pendentes)}")
    
    if not com_release_novo:
        print("\n[INFO] Nenhuma empresa nova para processar")
        return 0
    
    # Processa empresas com release novo
    print(f"\n[PROCESSAMENTO] Analisando {len(com_release_novo)} empresas...")
    
    analisadas = []
    aprovadas = []
    
    for empresa in com_release_novo:
        print(f"\n  Analisando {empresa['ticker']}...")
        
        try:
            analise = await sistema._analisar_empresa_profunda(empresa)
            
            if analise:
                analisadas.append(analise)
                sistema._atualizar_ranking_dinamico(analise)
                
                if analise.get('nota', 0) >= 6.0:
                    aprovadas.append(analise)
                    print(f"    APROVADA: Nota {analise['nota']:.1f}/10")
                else:
                    print(f"    DESCARTADA: Nota {analise['nota']:.1f}/10")
            else:
                print(f"    ERRO: Falha na analise")
        
        except Exception as e:
            print(f"    ERRO: {e}")
    
    # Atualiza lista de pendentes
    if ainda_pendentes:
        with open(pendentes_file, 'w', encoding='utf-8') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total": len(ainda_pendentes),
                "empresas": ainda_pendentes,
                "instrucoes": "Admin deve fazer upload dos releases dessas empresas."
            }, f, ensure_ascii=False, indent=2)
    else:
        # Remove arquivo se nao ha mais pendentes
        os.remove(pendentes_file)
        print("\n[INFO] Todas as empresas foram processadas!")
    
    # Mostra resumo
    print("\n" + "="*80)
    print("RESUMO FINAL")
    print("="*80)
    print(f"\nEmpresas processadas: {len(analisadas)}")
    print(f"Empresas aprovadas: {len(aprovadas)}")
    print(f"Empresas ainda pendentes: {len(ainda_pendentes)}")
    
    if aprovadas:
        print(f"\nAPROVADAS:")
        for emp in aprovadas:
            print(f"  - {emp['ticker']}: Nota {emp['nota']:.1f}/10 - {emp['recomendacao']}")
    
    print("\n" + "="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(processar_pendentes())
    sys.exit(exit_code)
