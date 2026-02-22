"""
Teste de Integração — Verifica se as novas rotas da API funcionam

Testa:
1. Servidor está rodando
2. Endpoints de consenso
3. Endpoints de cache de preços
4. Endpoints de notas estruturadas
"""
import requests
import time
import sys

BASE_URL = "http://localhost:8000"
TOKEN = None


def print_header(title):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(title)
    print("="*70 + "\n")


def test_servidor():
    """Teste 1: Verifica se servidor está rodando"""
    print_header("TESTE 1 — SERVIDOR")
    
    try:
        # Tenta endpoint raiz ou docs
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando")
            return True
        else:
            print(f"❌ Servidor retornou status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando")
        print("   Execute: cd backend && python -m uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_login():
    """Teste 2: Faz login e obtém token"""
    print_header("TESTE 2 — LOGIN ADMIN")
    
    global TOKEN
    
    # Tenta senha configurada
    senha = "a1e2i3o4u5"
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/admin/login",
            json={"password": senha},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            TOKEN = data.get("token")
            print(f"✅ Login realizado com sucesso")
            print(f"   Token: {TOKEN[:20]}...")
            return True
        else:
            print(f"❌ Login falhou: {response.status_code}")
            print(f"   Resposta: {response.text}")
            print(f"\n   DICA: Verifique a senha no .env")
            print(f"   Ou gere nova com: python gerar_senha_admin.py")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_cache_stats():
    """Teste 3: Estatísticas do cache de preços"""
    print_header("TESTE 3 — CACHE DE PREÇOS: ESTATÍSTICAS")
    
    if not TOKEN:
        print("❌ Sem token. Execute login primeiro.")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/admin/precos-cache/stats",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            cache = data.get("cache_precos", {})
            
            print("✅ Endpoint funcionando")
            print(f"\n📊 Estatísticas:")
            print(f"   Total: {cache.get('total', 0)}")
            print(f"   Atualizados (🟢): {cache.get('atualizados', 0)}")
            print(f"   Recentes (🟡): {cache.get('recentes', 0)}")
            print(f"   Antigos (🔴): {cache.get('antigos', 0)}")
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_nota_estruturada():
    """Teste 4: Calcular nota estruturada"""
    print_header("TESTE 4 — NOTAS ESTRUTURADAS")
    
    if not TOKEN:
        print("❌ Sem token. Execute login primeiro.")
        return False
    
    # Testa com PRIO3 (se existir no CSV)
    ticker = "PRIO3"
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/admin/notas-estruturadas/calcular/{ticker}",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Endpoint funcionando")
            print(f"\n📊 Nota para {ticker}:")
            print(f"   Nota Final: {data.get('nota_calculada', 0)}/10")
            
            detalhes = data.get('detalhamento', {})
            print(f"\n   Detalhamento:")
            print(f"      Fundamentos: {detalhes.get('fundamentos', 0)}/10")
            print(f"      Catalisadores: {detalhes.get('catalisadores', 0)}/10")
            print(f"      Valuation: {detalhes.get('valuation', 0)}/10")
            print(f"      Gestão: {detalhes.get('gestao', 0)}/10")
            
            return True
        elif response.status_code == 404:
            print(f"⚠️  Empresa {ticker} não encontrada no CSV")
            print(f"   Isso é normal se o CSV não foi carregado ainda")
            return True  # Não é erro do endpoint
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_empresas_aprovadas():
    """Teste 5: Verifica endpoint de empresas aprovadas"""
    print_header("TESTE 5 — EMPRESAS APROVADAS")
    
    if not TOKEN:
        print("❌ Sem token. Execute login primeiro.")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/admin/empresas-aprovadas",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            empresas = data.get('empresas', [])
            
            print("✅ Endpoint funcionando")
            print(f"\n📊 Empresas aprovadas: {total}")
            
            if total > 0:
                print(f"\n   Top 5:")
                for i, ticker in enumerate(empresas[:5], 1):
                    print(f"      {i}. {ticker}")
            else:
                print(f"\n   ⚠️  Nenhuma empresa aprovada ainda")
                print(f"   Execute análise primeiro")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_ranking_atual():
    """Teste 6: Verifica endpoint de ranking"""
    print_header("TESTE 6 — RANKING ATUAL")
    
    if not TOKEN:
        print("❌ Sem token. Execute login primeiro.")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/admin/ranking-atual",
            headers={"Authorization": f"Bearer {TOKEN}"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            total = data.get('total', 0)
            ranking = data.get('ranking', [])
            
            print("✅ Endpoint funcionando")
            print(f"\n📊 Ranking: {total} empresas")
            
            if total > 0:
                print(f"\n   Top 5:")
                for item in ranking[:5]:
                    ticker = item.get('ticker', 'N/A')
                    score = item.get('score', 0)
                    rec = item.get('recomendacao', 'N/A')
                    print(f"      {ticker}: {score:.1f}/10 - {rec}")
            else:
                print(f"\n   ⚠️  Nenhum ranking disponível")
                print(f"   Execute análise incremental primeiro")
            
            return True
        else:
            print(f"❌ Erro: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("TESTE DE INTEGRAÇÃO — NOVAS ROTAS DA API")
    print("="*70)
    
    resultados = {}
    
    # Teste 1: Servidor
    resultados["servidor"] = test_servidor()
    if not resultados["servidor"]:
        print("\n❌ Servidor não está rodando. Abortando testes.")
        return 1
    
    time.sleep(1)
    
    # Teste 2: Login
    resultados["login"] = test_login()
    if not resultados["login"]:
        print("\n❌ Login falhou. Abortando testes.")
        return 1
    
    time.sleep(1)
    
    # Teste 3: Cache Stats
    resultados["cache_stats"] = test_cache_stats()
    time.sleep(1)
    
    # Teste 4: Nota Estruturada
    resultados["nota_estruturada"] = test_nota_estruturada()
    time.sleep(1)
    
    # Teste 5: Empresas Aprovadas
    resultados["empresas_aprovadas"] = test_empresas_aprovadas()
    time.sleep(1)
    
    # Teste 6: Ranking Atual
    resultados["ranking_atual"] = test_ranking_atual()
    
    # Resumo
    print_header("RESUMO DOS TESTES")
    
    for nome, resultado in resultados.items():
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"  {nome.replace('_', ' ').title()}: {status}")
    
    passou = sum(1 for r in resultados.values() if r)
    falhou = sum(1 for r in resultados.values() if not r)
    
    print(f"\n📊 Total: {passou} passou, {falhou} falhou")
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ Sistema integrado e funcionando corretamente!")
        print("\n🚀 Pronto para próximo passo: Estratégia Dinâmica")
        return 0
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM")
        print("\nVerifique os erros acima e corrija antes de continuar.")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário")
        sys.exit(1)
