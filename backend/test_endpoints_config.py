"""
Teste dos Endpoints de Configuração
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from fastapi.testclient import TestClient
from app.main import app


def print_section(title):
    """Imprime seção formatada"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def test_config_endpoints():
    """Testa endpoints de configuração"""
    print_section("TESTE: Endpoints de Configuração")
    
    client = TestClient(app)
    
    # 1. Login para obter token
    print("📋 1. Fazendo login...")
    response = client.post("/api/v1/admin/login", json={"password": "a1e2i3o4u5"})
    
    if response.status_code != 200:
        print(f"❌ Erro no login: {response.status_code}")
        print(response.json())
        return False
    
    token = response.json()["token"]
    print(f"✅ Login bem-sucedido")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Obter todas as configurações
    print("\n📋 2. Obtendo todas as configurações...")
    response = client.get("/api/v1/admin/config", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    config = response.json()["config"]
    print(f"✅ {len(config)} seções carregadas")
    print(f"   Seções: {', '.join(config.keys())}")
    
    # 3. Obter seção específica
    print("\n📋 3. Obtendo seção 'scheduler_estrategia'...")
    response = client.get("/api/v1/admin/config/scheduler_estrategia", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    scheduler_config = response.json()["config"]
    print(f"✅ Configuração obtida:")
    print(f"   Auto-start: {scheduler_config['auto_start']}")
    print(f"   Intervalo: {scheduler_config['intervalo_minutos']} minutos")
    
    # 4. Atualizar configuração específica
    print("\n📋 4. Atualizando configuração específica...")
    response = client.put(
        "/api/v1/admin/config",
        headers=headers,
        json={"chave": "scheduler_estrategia.intervalo_minutos", "valor": 45}
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    print(f"✅ Configuração atualizada: {response.json()['novo_valor']} minutos")
    
    # 5. Verificar se mudança foi aplicada
    print("\n📋 5. Verificando mudança...")
    response = client.get("/api/v1/admin/config/scheduler_estrategia", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        return False
    
    novo_intervalo = response.json()["config"]["intervalo_minutos"]
    if novo_intervalo == 45:
        print(f"✅ Mudança aplicada corretamente: {novo_intervalo} minutos")
    else:
        print(f"❌ Mudança não aplicada: {novo_intervalo} minutos")
        return False
    
    # 6. Atualizar seção completa
    print("\n📋 6. Atualizando seção completa...")
    response = client.put(
        "/api/v1/admin/config/scheduler_estrategia",
        headers=headers,
        json={"valores": {"intervalo_minutos": 60, "auto_start": True}}
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    print(f"✅ Seção atualizada")
    
    # 7. Resetar configurações
    print("\n📋 7. Resetando configurações para padrão...")
    response = client.post("/api/v1/admin/config/resetar", headers=headers)
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    print(f"✅ Configurações resetadas")
    
    print("\n✅ Todos os endpoints de configuração funcionando!")
    return True


def test_consenso_endpoint():
    """Testa endpoint de análise com consenso"""
    print_section("TESTE: Endpoint de Análise com Consenso")
    
    client = TestClient(app)
    
    # Login
    print("📋 1. Fazendo login...")
    response = client.post("/api/v1/admin/login", json={"password": "a1e2i3o4u5"})
    
    if response.status_code != 200:
        print(f"❌ Erro no login: {response.status_code}")
        return False
    
    token = response.json()["token"]
    print(f"✅ Login bem-sucedido")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Testa endpoint com consenso
    print("\n📋 2. Testando endpoint /iniciar-analise com usar_consenso=True...")
    response = client.post(
        "/api/v1/admin/iniciar-analise?usar_consenso=true",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    result = response.json()
    print(f"✅ Endpoint respondeu:")
    print(f"   Mensagem: {result['mensagem']}")
    print(f"   Tempo estimado: {result['tempo_estimado']}")
    print(f"   Detalhes: {result['detalhes']}")
    
    # Testa endpoint sem consenso
    print("\n📋 3. Testando endpoint /iniciar-analise com usar_consenso=False...")
    response = client.post(
        "/api/v1/admin/iniciar-analise?usar_consenso=false",
        headers=headers
    )
    
    if response.status_code != 200:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return False
    
    result = response.json()
    print(f"✅ Endpoint respondeu:")
    print(f"   Mensagem: {result['mensagem']}")
    print(f"   Tempo estimado: {result['tempo_estimado']}")
    
    print("\n✅ Endpoint de análise com consenso funcionando!")
    return True


def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("  TESTE DOS ENDPOINTS DE CONFIGURAÇÃO")
    print("="*70)
    
    resultados = []
    
    # Executa testes
    resultados.append(test_config_endpoints())
    resultados.append(test_consenso_endpoint())
    
    # Resumo
    print_section("RESUMO DOS TESTES")
    
    total = len(resultados)
    passou = sum(resultados)
    falhou = total - passou
    
    print(f"Total de testes: {total}")
    print(f"✅ Passou: {passou}")
    print(f"❌ Falhou: {falhou}")
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Endpoints funcionando corretamente")
    else:
        print(f"\n⚠️ {falhou} teste(s) falharam")
        print("❌ Verificar erros acima")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
