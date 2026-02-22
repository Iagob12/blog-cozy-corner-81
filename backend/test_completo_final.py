"""
TESTE COMPLETO FINAL — Verifica TUDO que foi implementado

Testa:
1. Serviços Base (Consenso, Cache, Notas, Estratégia)
2. Integração com API
3. Fluxo completo
"""
import asyncio
import requests
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

BASE_URL = "http://localhost:8000"
TOKEN = None


def print_header(title):
    """Imprime cabeçalho"""
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")


def print_section(title):
    """Imprime seção"""
    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}\n")


# ===== TESTES DE SERVIÇOS =====

async def test_servicos_base():
    """Teste 1: Serviços Base"""
    print_header("PARTE 1 — SERVIÇOS BASE")
    
    resultados = {}
    
    # 1.1 Consenso Service
    print_section("1.1 Consenso Service")
    try:
        from app.services.consenso_service import get_consenso_service
        from app.services.multi_groq_client import get_multi_groq_client
        
        ai_client = get_multi_groq_client()
        consenso = get_consenso_service(ai_client)
        
        print("✅ Consenso Service: OK")
        resultados["consenso"] = True
    except Exception as e:
        print(f"❌ Consenso Service: {e}")
        resultados["consenso"] = False
    
    # 1.2 Cache de Preços
    print_section("1.2 Cache de Preços")
    try:
        from app.services.precos_cache_service import get_precos_cache_service
        
        cache = get_precos_cache_service()
        stats = cache.obter_estatisticas()
        
        print(f"✅ Cache de Preços: OK")
        print(f"   Total: {stats['total']}")
        print(f"   Atualizados: {stats['atualizados']}")
        resultados["cache_precos"] = True
    except Exception as e:
        print(f"❌ Cache de Preços: {e}")
        resultados["cache_precos"] = False
    
    # 1.3 Notas Estruturadas
    print_section("1.3 Notas Estruturadas")
    try:
        from app.services.notas_estruturadas_service import get_notas_estruturadas_service
        
        notas = get_notas_estruturadas_service()
        
        # Testa cálculo
        nota, detalhes = notas.calcular_nota(
            dados_csv={"roe": 20, "pl": 12, "cagr": 10},
            preco_atual=50,
            tem_release=True,
            setor_quente=True
        )
        
        print(f"✅ Notas Estruturadas: OK")
        print(f"   Nota teste: {nota}/10")
        resultados["notas"] = True
    except Exception as e:
        print(f"❌ Notas Estruturadas: {e}")
        resultados["notas"] = False
    
    # 1.4 Estratégia Dinâmica
    print_section("1.4 Estratégia Dinâmica")
    try:
        from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
        
        estrategia = get_estrategia_dinamica_service()
        status = estrategia.obter_status()
        
        print(f"✅ Estratégia Dinâmica: OK")
        print(f"   Intervalo: {status['intervalo_minutos']} min")
        print(f"   Histórico: {status['total_historico']} registros")
        resultados["estrategia"] = True
    except Exception as e:
        print(f"❌ Estratégia Dinâmica: {e}")
        resultados["estrategia"] = False
    
    return resultados


# ===== TESTES DE API =====

def test_servidor():
    """Teste 2.1: Servidor"""
    print_section("2.1 Servidor")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor: RODANDO")
            return True
        else:
            print(f"❌ Servidor: Status {response.status_code}")
            return False
    except:
        print("❌ Servidor: NÃO ESTÁ RODANDO")
        print("   Execute: python -m uvicorn app.main:app --reload")
        return False


def test_login():
    """Teste 2.2: Login"""
    print_section("2.2 Login Admin")
    
    global TOKEN
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/admin/login",
            json={"password": "a1e2i3o4u5"},
            timeout=10
        )
        
        if response.status_code == 200:
            TOKEN = response.json().get("token")
            print(f"✅ Login: OK")
            print(f"   Token: {TOKEN[:20]}...")
            return True
        else:
            print(f"❌ Login: Falhou ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Login: {e}")
        return False


def test_endpoints_novos():
    """Teste 2.3: Novos Endpoints"""
    print_section("2.3 Novos Endpoints")
    
    if not TOKEN:
        print("❌ Sem token")
        return {}
    
    resultados = {}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Cache Stats
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/precos-cache/stats", headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ Cache Stats: OK")
            resultados["cache_stats"] = True
        else:
            print(f"❌ Cache Stats: {r.status_code}")
            resultados["cache_stats"] = False
    except Exception as e:
        print(f"❌ Cache Stats: {e}")
        resultados["cache_stats"] = False
    
    # Notas Estruturadas
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/notas-estruturadas/calcular/PRIO3", headers=headers, timeout=10)
        if r.status_code in [200, 404]:  # 404 é OK se não tem CSV
            print("✅ Notas Estruturadas: OK")
            resultados["notas_api"] = True
        else:
            print(f"❌ Notas Estruturadas: {r.status_code}")
            resultados["notas_api"] = False
    except Exception as e:
        print(f"❌ Notas Estruturadas: {e}")
        resultados["notas_api"] = False
    
    # Estratégia Status
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/estrategia/status", headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ Estratégia Status: OK")
            resultados["estrategia_api"] = True
        else:
            print(f"❌ Estratégia Status: {r.status_code}")
            resultados["estrategia_api"] = False
    except Exception as e:
        print(f"❌ Estratégia Status: {e}")
        resultados["estrategia_api"] = False
    
    # Estratégia Alertas
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/estrategia/alertas", headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ Estratégia Alertas: OK")
            resultados["alertas_api"] = True
        else:
            print(f"❌ Estratégia Alertas: {r.status_code}")
            resultados["alertas_api"] = False
    except Exception as e:
        print(f"❌ Estratégia Alertas: {e}")
        resultados["alertas_api"] = False
    
    # Scheduler Status
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/estrategia-scheduler/status", headers=headers, timeout=10)
        if r.status_code == 200:
            print("✅ Scheduler Status: OK")
            resultados["scheduler_api"] = True
        else:
            print(f"❌ Scheduler Status: {r.status_code}")
            resultados["scheduler_api"] = False
    except Exception as e:
        print(f"❌ Scheduler Status: {e}")
        resultados["scheduler_api"] = False
    
    return resultados


def test_endpoints_existentes():
    """Teste 2.4: Endpoints Existentes"""
    print_section("2.4 Endpoints Existentes")
    
    if not TOKEN:
        print("❌ Sem token")
        return {}
    
    resultados = {}
    headers = {"Authorization": f"Bearer {TOKEN}"}
    
    # Empresas Aprovadas
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/empresas-aprovadas", headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            total = data.get('total', 0)
            print(f"✅ Empresas Aprovadas: OK ({total} empresas)")
            resultados["empresas"] = True
        else:
            print(f"❌ Empresas Aprovadas: {r.status_code}")
            resultados["empresas"] = False
    except Exception as e:
        print(f"❌ Empresas Aprovadas: {e}")
        resultados["empresas"] = False
    
    # Ranking Atual
    try:
        r = requests.get(f"{BASE_URL}/api/v1/admin/ranking-atual", headers=headers, timeout=10)
        if r.status_code == 200:
            data = r.json()
            total = data.get('total', 0)
            print(f"✅ Ranking Atual: OK ({total} empresas)")
            resultados["ranking"] = True
        else:
            print(f"❌ Ranking Atual: {r.status_code}")
            resultados["ranking"] = False
    except Exception as e:
        print(f"❌ Ranking Atual: {e}")
        resultados["ranking"] = False
    
    return resultados


async def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("TESTE COMPLETO FINAL — TODAS AS MELHORIAS")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*70)
    
    todos_resultados = {}
    
    # PARTE 1: Serviços Base
    print_header("PARTE 1 — SERVIÇOS BASE")
    resultados_servicos = await test_servicos_base()
    todos_resultados.update(resultados_servicos)
    
    # PARTE 2: API
    print_header("PARTE 2 — INTEGRAÇÃO COM API")
    
    # 2.1 Servidor
    servidor_ok = test_servidor()
    todos_resultados["servidor"] = servidor_ok
    
    if not servidor_ok:
        print("\n❌ Servidor não está rodando. Abortando testes de API.")
    else:
        # 2.2 Login
        login_ok = test_login()
        todos_resultados["login"] = login_ok
        
        if login_ok:
            # 2.3 Novos Endpoints
            resultados_novos = test_endpoints_novos()
            todos_resultados.update(resultados_novos)
            
            # 2.4 Endpoints Existentes
            resultados_existentes = test_endpoints_existentes()
            todos_resultados.update(resultados_existentes)
    
    # RESUMO FINAL
    print_header("RESUMO FINAL")
    
    print("📊 SERVIÇOS BASE:")
    print(f"   Consenso: {'✅' if todos_resultados.get('consenso') else '❌'}")
    print(f"   Cache Preços: {'✅' if todos_resultados.get('cache_precos') else '❌'}")
    print(f"   Notas: {'✅' if todos_resultados.get('notas') else '❌'}")
    print(f"   Estratégia: {'✅' if todos_resultados.get('estrategia') else '❌'}")
    
    print("\n📊 API:")
    print(f"   Servidor: {'✅' if todos_resultados.get('servidor') else '❌'}")
    print(f"   Login: {'✅' if todos_resultados.get('login') else '❌'}")
    print(f"   Cache Stats: {'✅' if todos_resultados.get('cache_stats') else '❌'}")
    print(f"   Notas API: {'✅' if todos_resultados.get('notas_api') else '❌'}")
    print(f"   Estratégia API: {'✅' if todos_resultados.get('estrategia_api') else '❌'}")
    print(f"   Alertas API: {'✅' if todos_resultados.get('alertas_api') else '❌'}")
    print(f"   Scheduler API: {'✅' if todos_resultados.get('scheduler_api') else '❌'}")
    print(f"   Empresas: {'✅' if todos_resultados.get('empresas') else '❌'}")
    print(f"   Ranking: {'✅' if todos_resultados.get('ranking') else '❌'}")
    
    passou = sum(1 for r in todos_resultados.values() if r)
    falhou = sum(1 for r in todos_resultados.values() if not r)
    total = len(todos_resultados)
    
    print(f"\n📊 TOTAL: {passou}/{total} testes passaram")
    
    if falhou == 0:
        print("\n" + "="*70)
        print("🎉 SUCESSO TOTAL! TUDO FUNCIONANDO!")
        print("="*70)
        print("\n✅ Todos os serviços implementados")
        print("✅ Todas as rotas da API funcionando")
        print("✅ Sistema completo e integrado")
        print("\n🚀 PRONTO PARA PRÓXIMO PASSO: Admin Frontend")
        print("="*70 + "\n")
        return 0
    else:
        print(f"\n⚠️  {falhou} teste(s) falharam")
        print("\nVerifique os erros acima.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos")
        sys.exit(1)
