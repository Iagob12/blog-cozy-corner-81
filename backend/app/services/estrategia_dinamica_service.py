"""
Serviço de Estratégia Dinâmica — Atualização automática a cada 1h

Recalcula entrada/stop/alvo com preços atuais
Gera alertas automáticos
Mantém histórico de mudanças
"""
import asyncio
import json
import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import math


class EstrategiaDinamicaService:
    """
    Atualiza estratégias automaticamente baseado em preços atuais
    
    Features:
    - Recalcula entrada/stop/alvo a cada 1h
    - Gera alertas (entrada, stop, alvo)
    - Mantém histórico de mudanças
    - Atualiza ranking dinamicamente
    """
    
    def __init__(self):
        self.estrategias_dir = "data/estrategias"
        self.historico_file = os.path.join(self.estrategias_dir, "historico.json")
        self.alertas_file = os.path.join(self.estrategias_dir, "alertas.json")
        self.config_file = os.path.join(self.estrategias_dir, "config.json")
        
        os.makedirs(self.estrategias_dir, exist_ok=True)
        
        self.config = self._carregar_config()
        self.historico = self._carregar_historico()
        self.alertas = []
        
        print("✓ Estratégia Dinâmica Service inicializado")
    
    def _carregar_config(self) -> Dict:
        """Carrega configuração"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except:
                pass
        
        # Config padrão
        return {
            "ativo": False,
            "intervalo_minutos": 60,
            "ultima_execucao": None,
            "proxima_execucao": None
        }
    
    def _salvar_config(self):
        """Salva configuração"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def _carregar_historico(self) -> List[Dict]:
        """Carrega histórico"""
        if os.path.exists(self.historico_file):
            try:
                with open(self.historico_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except:
                pass
        return []
    
    def _salvar_historico(self):
        """Salva histórico"""
        # Mantém apenas últimos 1000 registros
        if len(self.historico) > 1000:
            self.historico = self.historico[-1000:]
        
        with open(self.historico_file, 'w', encoding='utf-8') as f:
            json.dump(self.historico, f, indent=2, ensure_ascii=False)
    
    def _salvar_alertas(self):
        """Salva alertas"""
        with open(self.alertas_file, 'w', encoding='utf-8') as f:
            json.dump(self.alertas, f, indent=2, ensure_ascii=False)
    
    async def atualizar_estrategias(
        self,
        empresas: List[str],
        precos_service
    ) -> Dict:
        """
        Atualiza estratégias de todas as empresas
        
        Args:
            empresas: Lista de tickers
            precos_service: Serviço de preços
        
        Returns:
            Resultado com estatísticas e alertas
        """
        print(f"\n{'='*70}")
        print(f"ATUALIZAÇÃO DE ESTRATÉGIAS")
        print(f"{'='*70}")
        print(f"📊 Empresas: {len(empresas)}")
        print(f"⏰ Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        self.alertas = []  # Limpa alertas anteriores
        
        # 1. Busca preços atuais
        print("💰 Buscando preços atuais...")
        precos = await self._buscar_precos(empresas, precos_service)
        print(f"   ✓ {len(precos)} preços obtidos")
        
        # 2. Carrega ranking atual
        ranking = self._carregar_ranking()
        if not ranking:
            print("⚠️  Nenhum ranking disponível")
            return {
                "success": False,
                "erro": "Nenhum ranking disponível"
            }
        
        # 3. Atualiza cada empresa
        print(f"\n🔄 Atualizando estratégias...")
        atualizadas = 0
        
        for item in ranking:
            ticker = item.get('ticker')
            if ticker not in precos:
                continue
            
            preco_atual = precos[ticker]
            resultado = self._atualizar_estrategia_empresa(
                ticker,
                preco_atual,
                item
            )
            
            if resultado:
                atualizadas += 1
        
        # 4. Salva dados
        self._salvar_historico()
        self._salvar_alertas()
        
        # 5. Atualiza config
        self.config['ultima_execucao'] = datetime.now().isoformat()
        self.config['proxima_execucao'] = (
            datetime.now() + timedelta(minutes=self.config['intervalo_minutos'])
        ).isoformat()
        self._salvar_config()
        
        tempo = (datetime.now() - inicio).total_seconds()
        
        print(f"\n{'='*70}")
        print(f"✅ ATUALIZAÇÃO CONCLUÍDA")
        print(f"{'='*70}")
        print(f"✓ Estratégias atualizadas: {atualizadas}")
        print(f"🔔 Alertas gerados: {len(self.alertas)}")
        print(f"⏱️  Tempo: {tempo:.1f}s")
        print(f"{'='*70}\n")
        
        return {
            "success": True,
            "atualizadas": atualizadas,
            "alertas": len(self.alertas),
            "tempo_segundos": tempo
        }

    
    async def _buscar_precos(
        self,
        tickers: List[str],
        precos_service
    ) -> Dict[str, float]:
        """Busca preços atuais"""
        try:
            quotes = await precos_service.get_multiple_quotes(tickers)
            
            precos = {}
            for ticker, quote in quotes.items():
                preco = quote.get("regularMarketPrice", 0)
                if preco > 0:
                    precos[ticker] = preco
            
            return precos
        except Exception as e:
            print(f"⚠️ Erro ao buscar preços: {e}")
            return {}
    
    def _carregar_ranking(self) -> Optional[List[Dict]]:
        """Carrega ranking atual"""
        ranking_file = "data/cache/ranking_atual.json"
        
        if not os.path.exists(ranking_file):
            return None
        
        try:
            with open(ranking_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
                return data.get('ranking', [])
        except:
            return None
    
    def _atualizar_estrategia_empresa(
        self,
        ticker: str,
        preco_atual: float,
        dados_ranking: Dict
    ) -> bool:
        """
        Atualiza estratégia de uma empresa
        
        Calcula:
        - Entrada ideal
        - Stop loss
        - Alvo conservador e otimista
        - R/R (Risk/Reward)
        - Status (pode entrar, aguardar, stop atingido)
        """
        try:
            # Dados do ranking
            score = dados_ranking.get('score', 0)
            upside = dados_ranking.get('upside', 0)
            preco_teto = dados_ranking.get('preco_teto', 0)
            
            # Calcula entrada (5% abaixo do preço atual)
            entrada = preco_atual * 0.95
            
            # Calcula stop (10% abaixo da entrada)
            stop = entrada * 0.90
            
            # Calcula alvos baseado no upside
            alvo_conservador = preco_atual * (1 + (upside / 100) * 0.7)
            alvo_otimista = preco_teto if preco_teto > 0 else preco_atual * (1 + (upside / 100))
            
            # Calcula R/R
            risco = entrada - stop
            retorno = alvo_conservador - entrada
            rr = retorno / risco if risco > 0 else 0
            
            # Define status
            status = self._calcular_status(preco_atual, entrada, stop, alvo_otimista)
            
            # Verifica se houve mudança significativa
            mudanca = self._verificar_mudanca(ticker, status, preco_atual)
            
            # Gera alerta se necessário
            if mudanca:
                self._gerar_alerta(ticker, status, preco_atual, entrada, stop, alvo_conservador, rr)
            
            # Adiciona ao histórico
            self.historico.append({
                "ticker": ticker,
                "timestamp": datetime.now().isoformat(),
                "preco_atual": round(preco_atual, 2),
                "entrada": round(entrada, 2),
                "stop": round(stop, 2),
                "alvo_conservador": round(alvo_conservador, 2),
                "alvo_otimista": round(alvo_otimista, 2),
                "rr": round(rr, 2),
                "status": status,
                "score": score
            })
            
            return True
        
        except Exception as e:
            print(f"⚠️ Erro ao atualizar {ticker}: {e}")
            return False
    
    def _calcular_status(
        self,
        preco_atual: float,
        entrada: float,
        stop: float,
        alvo: float
    ) -> str:
        """Calcula status da operação"""
        
        # Stop atingido
        if preco_atual <= stop:
            return "STOP_ATINGIDO"
        
        # Alvo atingido
        if preco_atual >= alvo:
            return "ALVO_ATINGIDO"
        
        # Pode entrar (preço <= entrada)
        if preco_atual <= entrada:
            return "PODE_ENTRAR"
        
        # Aguardar correção (preço > entrada + 5%)
        if preco_atual > entrada * 1.05:
            return "AGUARDAR_CORRECAO"
        
        # Próximo da entrada
        return "PROXIMO_ENTRADA"
    
    def _verificar_mudanca(
        self,
        ticker: str,
        status_novo: str,
        preco_atual: float
    ) -> bool:
        """Verifica se houve mudança significativa"""
        
        # Busca último registro no histórico
        ultimos = [h for h in self.historico if h['ticker'] == ticker]
        
        if not ultimos:
            return True  # Primeira vez
        
        ultimo = ultimos[-1]
        status_anterior = ultimo.get('status')
        preco_anterior = ultimo.get('preco_atual', 0)
        
        # Mudança de status
        if status_novo != status_anterior:
            return True
        
        # Mudança de preço > 3%
        if preco_anterior > 0:
            variacao = abs((preco_atual - preco_anterior) / preco_anterior)
            if variacao > 0.03:
                return True
        
        return False
    
    def _gerar_alerta(
        self,
        ticker: str,
        status: str,
        preco: float,
        entrada: float,
        stop: float,
        alvo: float,
        rr: float
    ):
        """Gera alerta"""
        
        # Define tipo e mensagem
        if status == "PODE_ENTRAR":
            tipo = "OPORTUNIDADE"
            mensagem = f"{ticker} atingiu preço de entrada: R$ {preco:.2f}"
            prioridade = "ALTA"
        
        elif status == "STOP_ATINGIDO":
            tipo = "STOP"
            mensagem = f"{ticker} atingiu stop loss: R$ {preco:.2f}"
            prioridade = "CRITICA"
        
        elif status == "ALVO_ATINGIDO":
            tipo = "ALVO"
            mensagem = f"{ticker} atingiu alvo: R$ {preco:.2f}"
            prioridade = "ALTA"
        
        elif status == "AGUARDAR_CORRECAO":
            tipo = "AGUARDAR"
            mensagem = f"{ticker} acima da entrada, aguardar correção"
            prioridade = "BAIXA"
        
        else:
            return  # Não gera alerta
        
        alerta = {
            "ticker": ticker,
            "tipo": tipo,
            "mensagem": mensagem,
            "prioridade": prioridade,
            "timestamp": datetime.now().isoformat(),
            "dados": {
                "preco_atual": round(preco, 2),
                "entrada": round(entrada, 2),
                "stop": round(stop, 2),
                "alvo": round(alvo, 2),
                "rr": round(rr, 2)
            }
        }
        
        self.alertas.append(alerta)
        print(f"   🔔 {tipo}: {mensagem}")
    
    def obter_alertas(self, limite: int = 50) -> List[Dict]:
        """Retorna alertas recentes"""
        if os.path.exists(self.alertas_file):
            try:
                with open(self.alertas_file, 'r', encoding='utf-8-sig') as f:
                    alertas = json.load(f)
                    return alertas[-limite:]
            except:
                pass
        return []
    
    def obter_historico_empresa(
        self,
        ticker: str,
        limite: int = 100
    ) -> List[Dict]:
        """Retorna histórico de uma empresa"""
        historico_empresa = [
            h for h in self.historico
            if h['ticker'] == ticker
        ]
        return historico_empresa[-limite:]
    
    def obter_status(self) -> Dict:
        """Retorna status do serviço"""
        return {
            "ativo": self.config.get('ativo', False),
            "intervalo_minutos": self.config.get('intervalo_minutos', 60),
            "ultima_execucao": self.config.get('ultima_execucao'),
            "proxima_execucao": self.config.get('proxima_execucao'),
            "total_historico": len(self.historico),
            "alertas_pendentes": len(self.obter_alertas())
        }
    
    def iniciar(self):
        """Inicia serviço"""
        self.config['ativo'] = True
        self._salvar_config()
        print("✓ Estratégia Dinâmica iniciada")
    
    def parar(self):
        """Para serviço"""
        self.config['ativo'] = False
        self._salvar_config()
        print("✓ Estratégia Dinâmica parada")


# Singleton
_estrategia_service = None

def get_estrategia_dinamica_service() -> EstrategiaDinamicaService:
    """Retorna instância singleton"""
    global _estrategia_service
    if _estrategia_service is None:
        _estrategia_service = EstrategiaDinamicaService()
    return _estrategia_service
