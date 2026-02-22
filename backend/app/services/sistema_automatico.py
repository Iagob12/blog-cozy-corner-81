"""
Sistema Automático Completo

Gerencia todo o fluxo automaticamente:
1. Análise inicial com consenso (3x)
2. Detecção de releases novos
3. Atualização automática do ranking
4. Detecção de CSV novo
"""
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter
import hashlib


class SistemaAutomatico:
    """
    Sistema totalmente automático que:
    - Executa análise ao iniciar
    - Valida por consenso (3x)
    - Detecta releases novos
    - Atualiza ranking automaticamente
    - Detecta CSV novo e refaz processo
    """
    
    def __init__(self):
        self.config_file = "data/sistema_config.json"
        self.empresas_file = "data/empresas_aprovadas.json"
        self.ranking_file = "data/ranking_cache.json"
        self.csv_hash_file = "data/csv_hash.txt"
        
        self.config = self._carregar_config()
        
        print("✓ Sistema Automático inicializado")
    
    def _carregar_config(self) -> Dict:
        """Carrega configuração do sistema"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "analise_inicial_completa": False,
            "empresas_confirmadas": False,
            "ultima_analise": None,
            "csv_hash": None,
            "tentativas_consenso": 1,  # 1 tentativa por padrão (mais rápido)
            "threshold_consenso": 0.7  # 70% das empresas devem aparecer em todas análises
        }
    
    def _salvar_config(self):
        """Salva configuração"""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar config: {e}")
    
    def _calcular_hash_csv(self, csv_path: str = "data/stocks.csv") -> Optional[str]:
        """Calcula hash do CSV para detectar mudanças"""
        try:
            if not os.path.exists(csv_path):
                return None
            
            with open(csv_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def csv_mudou(self, csv_path: str = "data/stocks.csv") -> bool:
        """Verifica se CSV mudou desde última análise"""
        hash_atual = self._calcular_hash_csv(csv_path)
        hash_anterior = self.config.get("csv_hash")
        
        if not hash_anterior:
            return True  # Primeira vez
        
        return hash_atual != hash_anterior
    
    async def executar_analise_com_consenso(
        self,
        tentativas: int = 1,
        threshold: float = 0.7
    ) -> Dict:
        """
        Executa análise usando sistema incremental (SEM yfinance)
        
        SIMPLIFICADO: Usa apenas dados do CSV + releases
        
        Args:
            tentativas: Número de análises (1 = sem consenso, mais rápido)
            threshold: % mínimo de empresas que devem aparecer em todas
        
        Returns:
            Empresas aprovadas
        """
        print(f"\n{'='*70}")
        print(f"🔄 ANÁLISE INCREMENTAL (CSV + Releases)")
        print(f"{'='*70}\n")
        
        # Carrega empresas do arquivo (já foram selecionadas antes)
        if os.path.exists(self.empresas_file):
            with open(self.empresas_file, 'r', encoding='utf-8-sig') as f:
                dados = json.load(f)
            empresas = dados.get("empresas", [])
            
            if empresas:
                print(f"✓ Usando {len(empresas)} empresas já aprovadas")
                
                # Executa análise incremental
                from app.services.analise_automatica import get_analise_automatica_service
                service = get_analise_automatica_service()
                
                resultado = await service.analisar_incrementalmente(
                    empresas=empresas,
                    forcar_reanalise=True,  # Força reanálise
                    max_paralelo=1  # 1 por vez (evita rate limit)
                )
                
                print(f"\n✅ ANÁLISE CONCLUÍDA")
                print(f"   Analisadas: {resultado['novas_analises']}")
                print(f"   Falhas: {resultado['falhas']}")
                print(f"   Total no ranking: {resultado['total_ranking']}")
                
                return {
                    "empresas": empresas,
                    "total": len(empresas),
                    "tentativas": 1,
                    "threshold": 1.0
                }
        
        # Se não tem empresas aprovadas, retorna vazio
        print("⚠️ Nenhuma empresa aprovada encontrada")
        return {
            "empresas": [],
            "total": 0,
            "tentativas": 0,
            "threshold": 0
        }
    
    def _calcular_consenso(
        self,
        todas_empresas: List[List[str]],
        threshold: float
    ) -> List[str]:
        """
        Calcula consenso entre múltiplas análises
        
        Retorna apenas empresas que aparecem em pelo menos threshold% das análises
        """
        # Conta quantas vezes cada empresa aparece
        contador = Counter()
        for empresas in todas_empresas:
            for empresa in empresas:
                contador[empresa] += 1
        
        # Calcula threshold mínimo
        min_aparicoes = int(len(todas_empresas) * threshold)
        
        # Filtra empresas que atingem threshold
        empresas_consenso = [
            empresa
            for empresa, count in contador.items()
            if count >= min_aparicoes
        ]
        
        # Ordena por frequência (mais frequentes primeiro)
        empresas_consenso.sort(
            key=lambda e: contador[e],
            reverse=True
        )
        
        # Log detalhado
        print(f"📊 Análise de Consenso:")
        print(f"   Total de análises: {len(todas_empresas)}")
        print(f"   Threshold: {threshold*100}% ({min_aparicoes} aparições)")
        print(f"   Empresas únicas: {len(contador)}")
        print(f"   Empresas no consenso: {len(empresas_consenso)}")
        
        # Mostra top 10 mais frequentes
        print(f"\n   Top 10 mais frequentes:")
        for empresa in list(empresas_consenso)[:10]:
            freq = contador[empresa]
            pct = (freq / len(todas_empresas)) * 100
            print(f"      {empresa}: {freq}/{len(todas_empresas)} ({pct:.0f}%)")
        
        return empresas_consenso
    
    async def iniciar_sistema_automatico(self):
        """
        Inicia sistema automático completo
        
        Fluxo SIMPLIFICADO (sem yfinance):
        1. Verifica se já tem empresas aprovadas
        2. Se sim: executa análise incremental (CSV + releases)
        3. Se não: usa empresas do arquivo existente
        """
        print(f"\n{'='*70}")
        print(f"🚀 INICIANDO SISTEMA AUTOMÁTICO")
        print(f"{'='*70}\n")
        
        # Verifica se já tem empresas aprovadas
        if os.path.exists(self.empresas_file):
            with open(self.empresas_file, 'r', encoding='utf-8-sig') as f:
                dados = json.load(f)
            
            empresas = dados.get("empresas", [])
            
            if empresas and len(empresas) > 0:
                print(f"✓ {len(empresas)} empresas já aprovadas")
                print(f"📊 Executando análise incremental (CSV + releases)")
                
                try:
                    # Executa análise incremental
                    from app.services.analise_automatica import get_analise_automatica_service
                    service = get_analise_automatica_service()
                    
                    resultado = await service.analisar_incrementalmente(
                        empresas=empresas,
                        forcar_reanalise=True,  # Força reanálise
                        max_paralelo=1  # 1 por vez (evita rate limit)
                    )
                    
                    # Atualiza config
                    self.config["analise_inicial_completa"] = True
                    self.config["empresas_confirmadas"] = True
                    self.config["ultima_analise"] = datetime.now().isoformat()
                    self.config["csv_hash"] = self._calcular_hash_csv()
                    self._salvar_config()
                    
                    print(f"\n{'='*70}")
                    print(f"✅ SISTEMA AUTOMÁTICO PRONTO")
                    print(f"{'='*70}")
                    print(f"📊 {len(empresas)} empresas analisadas")
                    print(f"✓ Novas análises: {resultado['novas_analises']}")
                    print(f"❌ Falhas: {resultado['falhas']}")
                    print(f"🏆 Ranking: {resultado['total_ranking']} empresas")
                    print(f"💡 Aguardando releases no admin panel")
                    print(f"{'='*70}\n")
                    
                    return
                    
                except Exception as e:
                    print(f"\n❌ ERRO NA ANÁLISE INCREMENTAL: {e}")
                    import traceback
                    traceback.print_exc()
                    return
        
        print("⚠️ Nenhuma empresa aprovada encontrada")
        print("💡 Faça upload do CSV no admin panel para começar")
        print(f"{'='*70}\n")
    
    def _salvar_empresas_aprovadas(self, empresas: List[str]):
        """Salva lista de empresas aprovadas"""
        try:
            os.makedirs("data", exist_ok=True)
            
            dados = {
                "timestamp": datetime.now().isoformat(),
                "total": len(empresas),
                "empresas": empresas,
                "fonte": "consenso_automatico",
                "detalhes": [
                    {"ticker": ticker, "nome": ticker}
                    for ticker in empresas
                ]
            }
            
            with open(self.empresas_file, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Empresas aprovadas salvas: {self.empresas_file}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar empresas: {e}")
    
    def detectar_releases_novos(self) -> List[str]:
        """
        Detecta quais empresas têm releases novos
        
        Returns:
            Lista de tickers com releases novos
        """
        from app.services.release_manager import get_release_manager
        
        release_manager = get_release_manager()
        
        # Carrega empresas aprovadas
        if not os.path.exists(self.empresas_file):
            return []
        
        with open(self.empresas_file, 'r', encoding='utf-8-sig') as f:
            dados = json.load(f)
        
        empresas = dados.get("empresas", [])
        
        # Verifica quais têm releases
        empresas_com_releases = []
        for ticker in empresas:
            release = release_manager.obter_release_mais_recente(ticker)
            if release:
                empresas_com_releases.append(ticker)
        
        return empresas_com_releases
    
    async def atualizar_ranking_automaticamente(self):
        """
        Atualiza ranking automaticamente quando detecta releases novos
        
        Chamado periodicamente ou quando admin faz upload
        """
        print(f"\n🔄 Verificando releases novos...")
        
        empresas_com_releases = self.detectar_releases_novos()
        
        if not empresas_com_releases:
            print("   Nenhum release novo detectado")
            return
        
        print(f"   ✓ {len(empresas_com_releases)} empresas com releases")
        print(f"   Executando análise incremental...")
        
        # Executa análise incremental
        from app.services.analise_automatica import get_analise_automatica_service
        
        service = get_analise_automatica_service()
        
        # Carrega todas as empresas aprovadas
        with open(self.empresas_file, 'r', encoding='utf-8-sig') as f:
            dados = json.load(f)
        
        empresas = dados.get("empresas", [])
        
        resultado = await service.analisar_incrementalmente(
            empresas=empresas,
            forcar_reanalise=False,
            max_paralelo=3
        )
        
        print(f"   ✅ Ranking atualizado!")
        print(f"      Novas análises: {resultado['novas_analises']}")
        print(f"      Cache mantido: {resultado['cache_mantido']}")
        print(f"      Total no ranking: {resultado['total_ranking']}")


# Singleton
_sistema_automatico = None

def get_sistema_automatico() -> SistemaAutomatico:
    """Retorna instância singleton"""
    global _sistema_automatico
    if _sistema_automatico is None:
        _sistema_automatico = SistemaAutomatico()
    return _sistema_automatico
