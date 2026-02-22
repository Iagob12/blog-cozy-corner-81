"""
Teste das Melhorias - Fase 1
Valida todas as integrações implementadas
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime


def print_section(title):
    """Imprime seção formatada"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


async def test_config_service():
    """Testa serviço de configuração"""
    print_section("1. TESTE: Serviço de Configuração")
    
    try:
        from app.services.config_service import get_config_service
        
        config_service = get_config_service()
        
        # Testa obter todas as configurações
        print("📋 Obtendo todas as configurações...")
        config = config_service.obter_todas()
        print(f"✅ {len(config)} seções carregadas")
        
        # Testa obter seção específica
        print("\n📋 Obtendo seção 'scheduler_estrategia'...")
        scheduler_config = config_service.obter_secao('scheduler_estrategia')
        print(f"✅ Configuração: {scheduler_config}")
        
        # Testa obter valor específico
        print("\n📋 Obtendo valor 'scheduler_estrategia.auto_start'...")
        auto_start = config_service.obter('scheduler_estrategia.auto_start', False)
        print(f"✅ Auto-start: {auto_start}")
        
        # Testa definir valor
        print("\n📋 Definindo valor de teste...")
        config_service.definir('teste.valor', 123)
        valor_teste = config_service.obter('teste.valor')
        print(f"✅ Valor definido e recuperado: {valor_teste}")
        
        print("\n✅ Serviço de configuração funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_auto_start_config():
    """Testa se auto-start está configurado"""
    print_section("2. TESTE: Configuração de Auto-Start")
    
    try:
        from app.services.config_service import get_config_service
        
        config_service = get_config_service()
        
        # Verifica configuração de auto-start
        auto_start = config_service.obter('scheduler_estrategia.auto_start', False)
        intervalo = config_service.obter('scheduler_estrategia.intervalo_minutos', 60)
        
        print(f"📋 Auto-start: {auto_start}")
        print(f"📋 Intervalo: {intervalo} minutos")
        
        if auto_start:
            print("\n✅ Auto-start HABILITADO - Scheduler iniciará automaticamente")
        else:
            print("\n⚠️ Auto-start DESABILITADO - Scheduler precisa ser iniciado manualmente")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_consenso_config():
    """Testa configuração de consenso"""
    print_section("3. TESTE: Configuração de Consenso")
    
    try:
        from app.services.config_service import get_config_service
        
        config_service = get_config_service()
        
        # Verifica configuração de consenso
        usar_consenso = config_service.obter('analise.usar_consenso_padrao', True)
        num_execucoes = config_service.obter('analise.num_execucoes_consenso', 5)
        min_aparicoes = config_service.obter('analise.min_aparicoes_consenso', 3)
        
        print(f"📋 Usar consenso por padrão: {usar_consenso}")
        print(f"📋 Número de execuções: {num_execucoes}")
        print(f"📋 Mínimo de aparições: {min_aparicoes}")
        
        if usar_consenso:
            print(f"\n✅ Consenso HABILITADO - Análises executarão {num_execucoes}x")
        else:
            print("\n⚠️ Consenso DESABILITADO - Análises executarão 1x")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cache_config():
    """Testa configuração de cache"""
    print_section("4. TESTE: Configuração de Cache de Preços")
    
    try:
        from app.services.config_service import get_config_service
        
        config_service = get_config_service()
        
        # Verifica configuração de cache
        cache_ativo = config_service.obter('cache_precos.ativo', True)
        tempo_expiracao = config_service.obter('cache_precos.tempo_expiracao_horas', 24)
        usar_fallback = config_service.obter('cache_precos.usar_fallback', True)
        
        print(f"📋 Cache ativo: {cache_ativo}")
        print(f"📋 Tempo de expiração: {tempo_expiracao} horas")
        print(f"📋 Usar fallback: {usar_fallback}")
        
        if cache_ativo:
            print("\n✅ Cache HABILITADO - Preços serão armazenados")
        else:
            print("\n⚠️ Cache DESABILITADO - Sempre buscará da API")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_notas_config():
    """Testa configuração de notas estruturadas"""
    print_section("5. TESTE: Configuração de Notas Estruturadas")
    
    try:
        from app.services.config_service import get_config_service
        
        config_service = get_config_service()
        
        # Verifica configuração de notas
        notas_ativo = config_service.obter('notas_estruturadas.ativo', True)
        divergencia_max = config_service.obter('notas_estruturadas.divergencia_maxima', 2.0)
        pesos = config_service.obter_secao('notas_estruturadas').get('pesos', {})
        
        print(f"📋 Notas estruturadas ativas: {notas_ativo}")
        print(f"📋 Divergência máxima: {divergencia_max}")
        print(f"📋 Pesos:")
        for categoria, peso in pesos.items():
            print(f"   - {categoria}: {peso*100}%")
        
        if notas_ativo:
            print("\n✅ Notas estruturadas HABILITADAS - Validação ativa")
        else:
            print("\n⚠️ Notas estruturadas DESABILITADAS - Sem validação")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_services_integration():
    """Testa integração dos serviços"""
    print_section("6. TESTE: Integração de Serviços")
    
    try:
        # Testa importação de todos os serviços
        print("📋 Importando serviços...")
        
        from app.services.config_service import get_config_service
        from app.services.precos_cache_service import get_precos_cache_service
        from app.services.notas_estruturadas_service import get_notas_estruturadas_service
        from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
        from app.services.estrategia_scheduler import get_estrategia_scheduler
        from app.services.precos_service import get_precos_service
        
        print("✅ Todos os serviços importados com sucesso")
        
        # Testa inicialização
        print("\n📋 Inicializando serviços...")
        
        config_service = get_config_service()
        cache_service = get_precos_cache_service()
        notas_service = get_notas_estruturadas_service()
        estrategia_service = get_estrategia_dinamica_service()
        precos_service = get_precos_service()
        scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
        
        print("✅ Todos os serviços inicializados com sucesso")
        
        # Testa status dos serviços
        print("\n📋 Verificando status dos serviços...")
        
        cache_stats = cache_service.obter_estatisticas()
        print(f"   Cache: {cache_stats['total']} preços em cache")
        
        estrategia_status = estrategia_service.obter_status()
        print(f"   Estratégia: {estrategia_status['total_historico']} registros no histórico")
        
        scheduler_status = scheduler.obter_status()
        print(f"   Scheduler: {'Ativo' if scheduler_status['running'] else 'Inativo'}")
        
        print("\n✅ Todos os serviços funcionando corretamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_main_startup():
    """Testa se startup_event está configurado corretamente"""
    print_section("7. TESTE: Configuração de Startup")
    
    try:
        print("📋 Verificando código de startup...")
        
        # Lê arquivo main.py
        with open('app/main.py', 'r', encoding='utf-8') as f:
            main_content = f.read()
        
        # Verifica se auto-start está implementado
        checks = {
            "Importa estrategia_dinamica_service": "from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service" in main_content,
            "Importa estrategia_scheduler": "from app.services.estrategia_scheduler import get_estrategia_scheduler" in main_content,
            "Importa precos_service": "from app.services.precos_service import get_precos_service" in main_content,
            "Verifica auto_start": "auto_start" in main_content,
            "Inicia scheduler": "asyncio.create_task(scheduler.iniciar())" in main_content
        }
        
        for check, resultado in checks.items():
            status = "✅" if resultado else "❌"
            print(f"{status} {check}")
        
        if all(checks.values()):
            print("\n✅ Startup configurado corretamente - Auto-start implementado!")
            return True
        else:
            print("\n⚠️ Alguns checks falharam - Verificar implementação")
            return False
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Executa todos os testes"""
    print("\n" + "="*70)
    print("  TESTE DAS MELHORIAS - FASE 1")
    print("  Validação de Integrações Implementadas")
    print("="*70)
    
    resultados = []
    
    # Executa testes
    resultados.append(await test_config_service())
    resultados.append(await test_auto_start_config())
    resultados.append(await test_consenso_config())
    resultados.append(await test_cache_config())
    resultados.append(await test_notas_config())
    resultados.append(await test_services_integration())
    resultados.append(await test_main_startup())
    
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
        print("✅ Sistema pronto para produção")
    else:
        print(f"\n⚠️ {falhou} teste(s) falharam")
        print("❌ Verificar erros acima")
    
    print("\n" + "="*70)


if __name__ == "__main__":
    asyncio.run(main())
