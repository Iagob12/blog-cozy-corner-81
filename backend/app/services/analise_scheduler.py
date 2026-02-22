"""
Scheduler de Análise Automática
Roda análises automaticamente em intervalos configurados
"""
import asyncio
from datetime import datetime, time
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AnaliseScheduler:
    """
    Scheduler de análises automáticas
    
    Funcionalidades:
    - Análise completa diária (todo dia às 8h)
    - Atualização de preços/estratégias a cada 1h
    - Execução manual sob demanda
    """
    
    def __init__(self):
        self.ativo = False
        self.task_horaria: Optional[asyncio.Task] = None
        self.task_diaria: Optional[asyncio.Task] = None
        self.intervalo_horas = 1  # Atualiza a cada 1h
        self.hora_analise_diaria = time(8, 0)  # 8h da manhã
        self.logs = []
        
        logger.info("✓ Análise Scheduler inicializado")
    
    async def iniciar(self):
        """Inicia scheduler"""
        if self.ativo:
            logger.warning("⚠️ Scheduler já está ativo")
            return
        
        self.ativo = True
        
        # Task de atualização horária
        self.task_horaria = asyncio.create_task(self._loop_atualizacao_horaria())
        
        # Task de análise diária
        self.task_diaria = asyncio.create_task(self._loop_analise_diaria())
        
        self._add_log("Scheduler iniciado")
        logger.info("✅ Scheduler iniciado")
        logger.info(f"   - Atualização: a cada {self.intervalo_horas}h")
        logger.info(f"   - Análise diária: {self.hora_analise_diaria.strftime('%H:%M')}")
    
    async def parar(self):
        """Para scheduler"""
        if not self.ativo:
            return
        
        self.ativo = False
        
        if self.task_horaria:
            self.task_horaria.cancel()
            try:
                await self.task_horaria
            except asyncio.CancelledError:
                pass
        
        if self.task_diaria:
            self.task_diaria.cancel()
            try:
                await self.task_diaria
            except asyncio.CancelledError:
                pass
        
        self._add_log("Scheduler parado")
        logger.info("🛑 Scheduler parado")
    
    async def _loop_atualizacao_horaria(self):
        """Loop de atualização a cada 1h"""
        while self.ativo:
            try:
                # Aguarda intervalo
                await asyncio.sleep(self.intervalo_horas * 3600)
                
                if not self.ativo:
                    break
                
                logger.info("\n🔄 Executando atualização horária...")
                self._add_log("Iniciando atualização horária")
                
                # Atualiza preços e estratégias
                await self._atualizar_precos_e_estrategias()
                
                self._add_log("Atualização horária concluída")
                logger.info("✅ Atualização horária concluída")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na atualização horária: {e}")
                self._add_log(f"Erro na atualização horária: {e}")
                await asyncio.sleep(300)  # Aguarda 5min antes de tentar novamente
    
    async def _loop_analise_diaria(self):
        """Loop de análise completa diária"""
        while self.ativo:
            try:
                # Calcula tempo até próxima execução
                agora = datetime.now()
                proxima_execucao = datetime.combine(
                    agora.date(),
                    self.hora_analise_diaria
                )
                
                # Se já passou da hora hoje, agenda para amanhã
                if agora.time() > self.hora_analise_diaria:
                    from datetime import timedelta
                    proxima_execucao += timedelta(days=1)
                
                segundos_ate_execucao = (proxima_execucao - agora).total_seconds()
                
                logger.info(f"⏰ Próxima análise diária em {segundos_ate_execucao/3600:.1f}h ({proxima_execucao.strftime('%d/%m %H:%M')})")
                
                # Aguarda até a hora
                await asyncio.sleep(segundos_ate_execucao)
                
                if not self.ativo:
                    break
                
                logger.info("\n📊 Executando análise diária completa...")
                self._add_log("Iniciando análise diária completa")
                
                # Executa análise completa
                await self._executar_analise_completa()
                
                self._add_log("Análise diária concluída")
                logger.info("✅ Análise diária concluída")
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Erro na análise diária: {e}")
                self._add_log(f"Erro na análise diária: {e}")
                await asyncio.sleep(3600)  # Aguarda 1h antes de tentar novamente
    
    async def _atualizar_precos_e_estrategias(self):
        """Atualiza preços e recalcula estratégias"""
        try:
            from app.services.analise_com_release_service import get_analise_com_release_service
            from app.services.precos_service import get_precos_service
            import json
            import os
            
            analise_service = get_analise_com_release_service()
            precos_service = get_precos_service()
            
            # Lê ranking atual
            ranking_file = "data/cache/ranking_atual.json"
            if not os.path.exists(ranking_file):
                logger.warning("⚠️ Ranking não encontrado")
                return
            
            with open(ranking_file, 'r', encoding='utf-8-sig') as f:
                ranking_data = json.load(f)
            
            ranking = ranking_data.get('ranking', [])
            
            if not ranking:
                logger.warning("⚠️ Ranking vazio")
                return
            
            logger.info(f"🔄 Atualizando {len(ranking)} empresas...")
            
            # Atualiza cada empresa
            atualizadas = 0
            for item in ranking:
                ticker = item.get('ticker')
                if not ticker:
                    continue
                
                try:
                    # Busca novo preço
                    quote = await precos_service.get_quote(ticker)
                    preco_novo = quote.get('regularMarketPrice', 0) if quote else 0
                    
                    if not preco_novo or preco_novo <= 0:
                        continue
                    
                    preco_antigo = item.get('preco_atual', 0)
                    
                    # Atualiza apenas se mudou
                    if abs(preco_novo - preco_antigo) > 0.01:
                        item['preco_atual'] = preco_novo
                        
                        # Recalcula upside
                        preco_teto = item.get('preco_teto', preco_novo)
                        item['upside'] = ((preco_teto - preco_novo) / preco_novo * 100) if preco_novo > 0 else 0
                        
                        # Recalcula estratégia
                        estrategia = await analise_service._calcular_estrategia(
                            ticker=ticker,
                            preco_atual=preco_novo,
                            preco_teto=preco_teto,
                            nota=item.get('nota', 5.0)
                        )
                        
                        item['preco_entrada'] = estrategia['entrada']
                        item['preco_stop'] = estrategia['stop']
                        item['preco_alvo'] = estrategia['alvo']
                        item['risco_retorno'] = estrategia['risco_retorno']
                        
                        atualizadas += 1
                        logger.info(f"  ✓ {ticker}: R$ {preco_antigo:.2f} → R$ {preco_novo:.2f}")
                    
                    await asyncio.sleep(0.5)  # Evita rate limit
                    
                except Exception as e:
                    logger.error(f"  ❌ {ticker}: {e}")
                    continue
            
            # Salva ranking atualizado
            ranking_data['timestamp'] = datetime.now().isoformat()
            ranking_data['metadados']['ultima_atualizacao_precos'] = datetime.now().isoformat()
            
            with open(ranking_file, 'w', encoding='utf-8') as f:
                json.dump(ranking_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ {atualizadas} empresas atualizadas")
            
        except Exception as e:
            logger.error(f"❌ Erro ao atualizar preços: {e}")
            raise
    
    async def _executar_analise_completa(self):
        """Executa análise completa (reanalisa tudo)"""
        try:
            from app.services.analise_com_release_service import get_analise_com_release_service
            
            analise_service = get_analise_com_release_service()
            
            # Executa análise completa
            resultado = await analise_service.analisar_todas_com_releases(
                forcar_reanalise=True
            )
            
            if resultado.get('sucesso'):
                logger.info(f"✅ Análise completa: {resultado.get('total_analisadas')} empresas")
            else:
                logger.error(f"❌ Falha na análise: {resultado.get('mensagem')}")
            
        except Exception as e:
            logger.error(f"❌ Erro na análise completa: {e}")
            raise
    
    async def executar_agora(self, tipo: str = "completa"):
        """
        Executa análise manualmente
        
        Args:
            tipo: "completa" ou "atualizacao"
        """
        if tipo == "completa":
            logger.info("🚀 Executando análise completa manual...")
            await self._executar_analise_completa()
        else:
            logger.info("🚀 Executando atualização manual...")
            await self._atualizar_precos_e_estrategias()
    
    def obter_status(self) -> dict:
        """Retorna status do scheduler"""
        return {
            "ativo": self.ativo,
            "intervalo_horas": self.intervalo_horas,
            "hora_analise_diaria": self.hora_analise_diaria.strftime("%H:%M"),
            "proxima_atualizacao": "Em execução" if self.ativo else "Parado",
            "proxima_analise_diaria": "Em execução" if self.ativo else "Parado"
        }
    
    def obter_logs(self, limite: int = 10) -> list:
        """Retorna últimos logs"""
        return self.logs[-limite:]
    
    def _add_log(self, mensagem: str):
        """Adiciona log"""
        self.logs.append({
            "timestamp": datetime.now().isoformat(),
            "mensagem": mensagem
        })
        
        # Mantém apenas últimos 100 logs
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]


# Singleton
_analise_scheduler: Optional[AnaliseScheduler] = None


def get_analise_scheduler() -> AnaliseScheduler:
    """Retorna instância singleton"""
    global _analise_scheduler
    
    if _analise_scheduler is None:
        _analise_scheduler = AnaliseScheduler()
    
    return _analise_scheduler
