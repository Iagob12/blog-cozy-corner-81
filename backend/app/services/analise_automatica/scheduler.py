"""
Scheduler para Análises Automáticas

Executa análises em background periodicamente
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json
import os

from .analise_service import get_analise_automatica_service


class SchedulerAnalise:
    """
    Scheduler para executar análises automaticamente
    
    Features:
    - Executa análises em intervalos configuráveis
    - Controle de ON/OFF
    - Logs de execução
    - Tratamento de erros
    """
    
    def __init__(self, intervalo_minutos: int = 60):
        self.intervalo_minutos = intervalo_minutos
        self.ativo = False
        self.task: Optional[asyncio.Task] = None
        self.config_file = "data/scheduler_config.json"
        self.log_file = "data/scheduler_log.json"
        
        # Carrega configuração
        self.config = self._carregar_config()
        
        print(f"✓ Scheduler inicializado (intervalo: {intervalo_minutos}min)")
    
    def _carregar_config(self) -> dict:
        """Carrega configuração do scheduler"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "ativo": False,
            "intervalo_minutos": self.intervalo_minutos,
            "ultima_execucao": None,
            "proxima_execucao": None
        }
    
    def _salvar_config(self):
        """Salva configuração"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erro ao salvar config: {e}")
    
    def _adicionar_log(self, evento: dict):
        """Adiciona evento ao log"""
        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
            
            logs.append({
                **evento,
                "timestamp": datetime.now().isoformat()
            })
            
            # Mantém apenas últimos 50 logs
            logs = logs[-50:]
            
            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=2)
        except Exception as e:
            print(f"⚠️ Erro ao salvar log: {e}")
    
    async def iniciar(self):
        """Inicia scheduler"""
        if self.ativo:
            print("⚠️ Scheduler já está ativo")
            return
        
        self.ativo = True
        self.config["ativo"] = True
        self._salvar_config()
        
        print(f"✅ Scheduler iniciado (intervalo: {self.intervalo_minutos}min)")
        
        self.task = asyncio.create_task(self._loop_analise())
        
        self._adicionar_log({
            "tipo": "scheduler_iniciado",
            "intervalo_minutos": self.intervalo_minutos
        })
    
    async def parar(self):
        """Para scheduler"""
        if not self.ativo:
            print("⚠️ Scheduler já está parado")
            return
        
        self.ativo = False
        self.config["ativo"] = False
        self._salvar_config()
        
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        
        print("✅ Scheduler parado")
        
        self._adicionar_log({
            "tipo": "scheduler_parado"
        })
    
    async def _loop_analise(self):
        """Loop principal do scheduler"""
        while self.ativo:
            try:
                # Calcula próxima execução
                proxima = datetime.now() + timedelta(minutes=self.intervalo_minutos)
                self.config["proxima_execucao"] = proxima.isoformat()
                self._salvar_config()
                
                print(f"\n{'='*70}")
                print(f"🕐 SCHEDULER - Próxima execução: {proxima.strftime('%H:%M:%S')}")
                print(f"{'='*70}\n")
                
                # Aguarda intervalo
                await asyncio.sleep(self.intervalo_minutos * 60)
                
                if not self.ativo:
                    break
                
                # Executa análise
                await self._executar_analise()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Erro no scheduler: {e}")
                self._adicionar_log({
                    "tipo": "erro_scheduler",
                    "erro": str(e)
                })
                
                # Aguarda 5 minutos antes de tentar novamente
                await asyncio.sleep(300)
    
    async def _executar_analise(self):
        """Executa análise incremental"""
        print(f"\n{'='*70}")
        print(f"🤖 SCHEDULER - Executando análise automática")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        
        try:
            # Carrega empresas aprovadas
            empresas_file = "data/empresas_aprovadas.json"
            if not os.path.exists(empresas_file):
                print("⚠️ Nenhuma empresa aprovada. Pulando análise.")
                return
            
            with open(empresas_file, 'r') as f:
                data = json.load(f)
            
            empresas = data.get("empresas", [])
            
            if not empresas:
                print("⚠️ Lista de empresas vazia. Pulando análise.")
                return
            
            # Executa análise
            service = get_analise_automatica_service()
            resultado = await service.analisar_incrementalmente(
                empresas=empresas,
                forcar_reanalise=False,
                max_paralelo=3
            )
            
            tempo = (datetime.now() - inicio).total_seconds()
            
            # Atualiza config
            self.config["ultima_execucao"] = datetime.now().isoformat()
            self._salvar_config()
            
            # Log
            self._adicionar_log({
                "tipo": "analise_executada",
                "resultado": resultado,
                "tempo_segundos": tempo
            })
            
            print(f"\n✅ Análise automática concluída em {tempo:.1f}s")
            
        except Exception as e:
            print(f"❌ Erro na análise: {e}")
            import traceback
            traceback.print_exc()
            
            self._adicionar_log({
                "tipo": "erro_analise",
                "erro": str(e)
            })
    
    def obter_status(self) -> dict:
        """Retorna status do scheduler"""
        return {
            "ativo": self.ativo,
            "intervalo_minutos": self.intervalo_minutos,
            "ultima_execucao": self.config.get("ultima_execucao"),
            "proxima_execucao": self.config.get("proxima_execucao")
        }
    
    def obter_logs(self, limite: int = 10) -> list:
        """Retorna últimos logs"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    logs = json.load(f)
                return logs[-limite:]
            except:
                return []
        return []


# Singleton
_scheduler = None

def get_scheduler() -> SchedulerAnalise:
    """Retorna instância singleton"""
    global _scheduler
    if _scheduler is None:
        _scheduler = SchedulerAnalise(intervalo_minutos=60)
    return _scheduler
