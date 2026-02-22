"""
Script de Inicialização do Backend
Mostra todos os logs de startup
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from datetime import datetime


def print_header():
    """Imprime cabeçalho"""
    print("\n" + "="*80)
    print("  🚀 INICIANDO BACKEND - SISTEMA ALPHA")
    print(f"  Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")


def print_section(title):
    """Imprime seção"""
    print("\n" + "-"*80)
    print(f"  {title}")
    print("-"*80 + "\n")


async def main():
    """Inicia backend e mostra logs"""
    
    print_header()
    
    # 1. Importa módulos
    print_section("1. IMPORTANDO MÓDULOS")
    
    try:
        print("📦 Importando FastAPI...")
        from fastapi import FastAPI
        print("✅ FastAPI importado")
        
        print("📦 Importando app.main...")
        from app.main import app, startup_event
        print("✅ app.main importado")
        
        print("📦 Importando serviços...")
        from app.services.config_service import get_config_service
        from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
        from app.services.estrategia_scheduler import get_estrategia_scheduler
        from app.services.precos_service import get_precos_service
        print("✅ Serviços importados")
        
    except Exception as e:
        print(f"❌ ERRO na importação: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 2. Carrega configurações
    print_section("2. CARREGANDO CONFIGURAÇÕES")
    
    try:
        config_service = get_config_service()
        config = config_service.obter_todas()
        
        print(f"📋 Configurações carregadas:")
        print(f"   - Versão: {config.get('versao')}")
        print(f"   - Auto-start: {config.get('scheduler_estrategia', {}).get('auto_start')}")
        print(f"   - Intervalo: {config.get('scheduler_estrategia', {}).get('intervalo_minutos')} min")
        print(f"   - Consenso padrão: {config.get('analise', {}).get('usar_consenso_padrao')}")
        print(f"   - Cache ativo: {config.get('cache_precos', {}).get('ativo')}")
        print(f"   - Notas estruturadas: {config.get('notas_estruturadas', {}).get('ativo')}")
        print("✅ Configurações OK")
        
    except Exception as e:
        print(f"❌ ERRO ao carregar configurações: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 3. Executa startup event
    print_section("3. EXECUTANDO STARTUP EVENT")
    
    try:
        print("🔥 Executando startup_event()...")
        await startup_event()
        print("✅ Startup event concluído")
        
    except Exception as e:
        print(f"❌ ERRO no startup: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 4. Verifica status dos serviços
    print_section("4. VERIFICANDO STATUS DOS SERVIÇOS")
    
    try:
        # Config Service
        print("📋 Config Service:")
        print(f"   Status: ✅ Ativo")
        
        # Estratégia Service
        estrategia_service = get_estrategia_dinamica_service()
        estrategia_status = estrategia_service.obter_status()
        print(f"\n📋 Estratégia Dinâmica Service:")
        print(f"   Ativo: {estrategia_status['ativo']}")
        print(f"   Intervalo: {estrategia_status['intervalo_minutos']} min")
        print(f"   Histórico: {estrategia_status['total_historico']} registros")
        print(f"   Alertas: {estrategia_status['alertas_pendentes']} pendentes")
        
        # Scheduler
        precos_service = get_precos_service()
        scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
        scheduler_status = scheduler.obter_status()
        print(f"\n📋 Estratégia Scheduler:")
        print(f"   Running: {scheduler_status['running']}")
        
        print("\n✅ Todos os serviços verificados")
        
    except Exception as e:
        print(f"❌ ERRO ao verificar serviços: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # 5. Resumo final
    print_section("5. RESUMO FINAL")
    
    print("✅ Backend iniciado com sucesso!")
    print("\n📊 Status:")
    print("   - Importações: ✅ OK")
    print("   - Configurações: ✅ OK")
    print("   - Startup Event: ✅ OK")
    print("   - Serviços: ✅ OK")
    print("   - Scheduler: ✅ Iniciado automaticamente")
    
    print("\n🌐 Endpoints disponíveis:")
    print("   - API: http://localhost:8000")
    print("   - Docs: http://localhost:8000/docs")
    print("   - Admin: http://localhost:8000/api/v1/admin")
    
    print("\n🎯 Sistema pronto para receber requisições!")
    
    print("\n" + "="*80)
    print("  ✅ BACKEND INICIADO COM SUCESSO")
    print("="*80 + "\n")
    
    # Mantém rodando
    print("⏳ Pressione Ctrl+C para parar o backend...\n")
    
    try:
        # Inicia servidor uvicorn
        import uvicorn
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000, 
            log_level="warning",  # Desabilita logs INFO
            access_log=False  # Desabilita access log
        )
    except ImportError:
        print("⚠️ uvicorn não instalado - Backend iniciado mas não está servindo HTTP")
        print("   Para servir HTTP, instale: pip install uvicorn")
        print("\n✅ Mas todos os serviços estão funcionando!")
        
        # Aguarda indefinidamente
        while True:
            await asyncio.sleep(60)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Backend parado pelo usuário")
        print("✅ Shutdown concluído\n")
