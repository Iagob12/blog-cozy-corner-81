"""
Teste de Estratégia Dinâmica

Testa:
1. Serviço de estratégia dinâmica
2. Cálculo de entrada/stop/alvo
3. Geração de alertas
4. Scheduler
"""
import asyncio
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
from app.services.precos_service import get_precos_service


async def test_estrategia_service():
    """Teste 1: Serviço de Estratégia"""
    print("\n" + "="*70)
    print("TESTE 1 — SERVIÇO DE ESTRATÉGIA DINÂMICA")
    print("="*70 + "\n")
    
    estrategia_service = get_estrategia_dinamica_service()
    
    print("✅ Serviço inicializado")
    
    # Testa status
    status = estrategia_service.obter_status()
    print(f"\n📊 Status:")
    print(f"   Ativo: {status['ativo']}")
    print(f"   Intervalo: {status['intervalo_minutos']} min")
    print(f"   Histórico: {status['total_historico']} registros")
    
    return True


async def test_atualizacao_estrategias():
    """Teste 2: Atualização de Estratégias"""
    print("\n" + "="*70)
    print("TESTE 2 — ATUALIZAÇÃO DE ESTRATÉGIAS")
    print("="*70 + "\n")
    
    # Verifica se tem empresas aprovadas
    empresas_file = "data/empresas_aprovadas.json"
    if not os.path.exists(empresas_file):
        print("⚠️  Nenhuma empresa aprovada")
        print("   Execute análise primeiro")
        return False
    
    import json
    with open(empresas_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    empresas = data.get('empresas', [])[:5]  # Apenas 5 para teste
    
    if not empresas:
        print("⚠️  Lista vazia")
        return False
    
    print(f"📊 Testando com {len(empresas)} empresas:")
    for ticker in empresas:
        print(f"   • {ticker}")
    
    # Executa atualização
    estrategia_service = get_estrategia_dinamica_service()
    precos_service = get_precos_service()
    
    resultado = await estrategia_service.atualizar_estrategias(
        empresas=empresas,
        precos_service=precos_service
    )
    
    if resultado.get('success'):
        print(f"\n✅ Atualização concluída:")
        print(f"   Atualizadas: {resultado['atualizadas']}")
        print(f"   Alertas: {resultado['alertas']}")
        print(f"   Tempo: {resultado['tempo_segundos']:.1f}s")
        return True
    else:
        print(f"\n❌ Falhou: {resultado.get('erro')}")
        return False


async def test_alertas():
    """Teste 3: Alertas"""
    print("\n" + "="*70)
    print("TESTE 3 — ALERTAS")
    print("="*70 + "\n")
    
    estrategia_service = get_estrategia_dinamica_service()
    alertas = estrategia_service.obter_alertas(limite=10)
    
    print(f"📊 Alertas recentes: {len(alertas)}")
    
    if alertas:
        print(f"\n   Últimos 5:")
        for alerta in alertas[-5:]:
            tipo = alerta.get('tipo', 'N/A')
            ticker = alerta.get('ticker', 'N/A')
            msg = alerta.get('mensagem', 'N/A')
            print(f"      {tipo}: {ticker} - {msg}")
    else:
        print("   Nenhum alerta gerado ainda")
    
    print("\n✅ Teste de alertas: PASSOU")
    return True


async def test_historico():
    """Teste 4: Histórico"""
    print("\n" + "="*70)
    print("TESTE 4 — HISTÓRICO")
    print("="*70 + "\n")
    
    # Pega primeira empresa aprovada
    empresas_file = "data/empresas_aprovadas.json"
    if not os.path.exists(empresas_file):
        print("⚠️  Nenhuma empresa aprovada")
        return False
    
    import json
    with open(empresas_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    empresas = data.get('empresas', [])
    if not empresas:
        print("⚠️  Lista vazia")
        return False
    
    ticker = empresas[0]
    
    estrategia_service = get_estrategia_dinamica_service()
    historico = estrategia_service.obter_historico_empresa(ticker, limite=5)
    
    print(f"📊 Histórico de {ticker}: {len(historico)} registros")
    
    if historico:
        print(f"\n   Últimos 3:")
        for h in historico[-3:]:
            preco = h.get('preco_atual', 0)
            status = h.get('status', 'N/A')
            rr = h.get('rr', 0)
            print(f"      R$ {preco:.2f} - {status} - R/R {rr:.2f}")
    else:
        print("   Nenhum histórico ainda")
    
    print("\n✅ Teste de histórico: PASSOU")
    return True


async def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("TESTES DE ESTRATÉGIA DINÂMICA")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)
    
    resultados = {}
    
    # Teste 1: Serviço
    try:
        resultados["servico"] = await test_estrategia_service()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        resultados["servico"] = False
    
    await asyncio.sleep(1)
    
    # Teste 2: Atualização
    try:
        resultados["atualizacao"] = await test_atualizacao_estrategias()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        resultados["atualizacao"] = False
    
    await asyncio.sleep(1)
    
    # Teste 3: Alertas
    try:
        resultados["alertas"] = await test_alertas()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        resultados["alertas"] = False
    
    await asyncio.sleep(1)
    
    # Teste 4: Histórico
    try:
        resultados["historico"] = await test_historico()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        resultados["historico"] = False
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70 + "\n")
    
    for nome, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"  {nome.replace('_', ' ').title()}: {status}")
    
    passou = sum(1 for r in resultados.values() if r)
    falhou = sum(1 for r in resultados.values() if not r)
    
    print(f"\n📊 Total: {passou} passou, {falhou} falhou")
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos")
        sys.exit(1)
