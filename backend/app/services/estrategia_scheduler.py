"""
Scheduler de Estratégia Dinâmica — Executa a cada 1h

Atualiza estratégias automaticamente em background
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json
import os


class EstrategiaScheduler:
    """
    Scheduler que executa atualização de estratégias periodicamente
    
    Features:
    - Executa a cada 1h (configurável)
    - Controle ON/OFF
    - Logs de execução
    - Tratamento de erros
    """
    
    def __init__(self, estrategia_service, precos_service):
        self.estrategia_service = estrategia_service
        self.precos_service = precos_service
        self.task: Optional[asyncio.Task] = None
        self.running = False
        
        self.logs_file = "data/estrategias/scheduler_logs.json"
        os.makedirs("data/estrategias", exist_ok=True)
        
        print("✓ Estratégia Scheduler inicializado")
    
    async def iniciar(self):
        """Inicia scheduler"""
        if self.running:
            print("⚠️  Scheduler já está rodando")
            return
        
        self.running = True
        self.estrategia_service.iniciar()
        
        # Inicia task em background
        self.task = asyncio.create_task(self._loop())
        
        print("✅ Scheduler iniciado")
        print(f"   Intervalo: {self.estrategia_service.config['intervalo_minutos']} minutos")
    
    async def parar(self):
        """Para scheduler"""
        if not self.running:
            print("⚠️  Scheduler já está parado")
            return
        
        self.running = False
        self.estrategia_service.parar()
        
        # Cancela task
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print("✅ Scheduler parado")
    
    async def _loop(self):
        """Loop principal do scheduler"""
        print("\n🔄 Scheduler em execução...")
        
        while self.running:
            try:
                # Aguarda intervalo
                intervalo = self.estrategia_service.config['intervalo_minutos']
                print(f"\n⏰ Próxima execução em {intervalo} minutos...")
                
                await asyncio.sleep(intervalo * 60)
                
                if not self.running:
                    break
                
                # Executa atualização
                await self._executar_atualizacao()
            
            except asyncio.CancelledError:
                print("\n⚠️  Scheduler cancelado")
                break
            
            except Exception as e:
                print(f"\n❌ Erro no scheduler: {e}")
                self._registrar_log("erro", str(e))
                
                # Aguarda 5 minutos antes de tentar novamente
                await asyncio.sleep(300)
    
    async def _executar_atualizacao(self):
        """Executa atualização de estratégias"""
        print(f"\n{'='*70}")
        print(f"SCHEDULER — ATUALIZAÇÃO AUTOMÁTICA")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        
        try:
            # Carrega empresas aprovadas
            empresas = self._carregar_empresas_aprovadas()
            
            if not empresas:
                print("⚠️  Nenhuma empresa aprovada")
                self._registrar_log("aviso", "Nenhuma empresa aprovada")
                return
            
            # Executa atualização
            resultado = await self.estrategia_service.atualizar_estrategias(
                empresas=empresas,
                precos_service=self.precos_service
            )
            
            if resultado.get('success'):
                self._registrar_log(
                    "sucesso",
                    f"{resultado['atualizadas']} estratégias atualizadas, {resultado['alertas']} alertas"
                )
            else:
                self._registrar_log("erro", resultado.get('erro', 'Erro desconhecido'))
        
        except Exception as e:
            print(f"❌ Erro: {e}")
            self._registrar_log("erro", str(e))
    
    def _carregar_empresas_aprovadas(self) -> list:
        """Carrega lista de empresas aprovadas"""
        empresas_file = "data/empresas_aprovadas.json"
        
        if not os.path.exists(empresas_file):
            return []
        
        try:
            with open(empresas_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                return data.get('empresas', [])
        except:
            return []
    
    def _registrar_log(self, tipo: str, mensagem: str):
        """Registra log de execução"""
        log = {
            "tipo": tipo,
            "mensagem": mensagem,
            "timestamp": datetime.now().isoformat()
        }
        
        # Carrega logs existentes
        logs = []
        if os.path.exists(self.logs_file):
            try:
                with open(self.logs_file, 'r', encoding='utf-8-sig') as f:
                    logs = json.load(f)
            except:
                pass
        
        # Adiciona novo log
        logs.append(log)
        
        # Mantém apenas últimos 100
        if len(logs) > 100:
            logs = logs[-100:]
        
        # Salva
        with open(self.logs_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    
    def obter_logs(self, limite: int = 20) -> list:
        """Retorna logs recentes"""
        if not os.path.exists(self.logs_file):
            return []
        
        try:
            with open(self.logs_file, 'r', encoding='utf-8-sig') as f:
                logs = json.load(f)
                return logs[-limite:]
        except:
            return []
    
    def obter_status(self) -> dict:
        """Retorna status do scheduler"""
        return {
            "running": self.running,
            "estrategia_status": self.estrategia_service.obter_status()
        }


# Singleton
_scheduler = None

def get_estrategia_scheduler(estrategia_service, precos_service) -> EstrategiaScheduler:
    """Retorna instância singleton"""
    global _scheduler
    if _scheduler is None:
        _scheduler = EstrategiaScheduler(estrategia_service, precos_service)
    return _scheduler
