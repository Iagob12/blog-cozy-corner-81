"""
Gerenciador de Cache Inteligente

Responsável por:
- Armazenar análises de empresas
- Verificar validade do cache
- Detectar mudanças (novos releases, dados atualizados)
- Persistir dados em disco
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class CacheManager:
    """
    Gerenciador de cache para análises de empresas
    
    Estrutura do cache:
    {
        "versao": "1.0",
        "timestamp_criacao": "2026-02-20T15:00:00",
        "timestamp_atualizacao": "2026-02-20T16:00:00",
        "analises": {
            "PRIO3": {
                "ticker": "PRIO3",
                "analise": {...},
                "timestamp": "2026-02-20T15:30:00",
                "tem_release": true,
                "release_hash": "abc123",
                "dados_hash": "def456"
            }
        },
        "metadados": {
            "total_analises": 30,
            "com_release": 25,
            "sem_release": 5
        }
    }
    """
    
    def __init__(self, cache_dir: str = "data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.cache_file = self.cache_dir / "analises_cache.json"
        self.ranking_file = self.cache_dir / "ranking_atual.json"
        self.historico_file = self.cache_dir / "historico_analises.json"
        
        self.cache = self._carregar_cache()
        self.historico = self._carregar_historico()
    
    def _carregar_cache(self) -> Dict:
        """Carrega cache do disco"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8-sig') as f:
                    cache = json.load(f)
                    print(f"✓ Cache carregado: {cache.get('metadados', {}).get('total_analises', 0)} análises")
                    return cache
            except Exception as e:
                print(f"⚠️ Erro ao carregar cache: {e}")
        
        return self._criar_cache_vazio()
    
    def _criar_cache_vazio(self) -> Dict:
        """Cria estrutura de cache vazia"""
        return {
            "versao": "1.0",
            "timestamp_criacao": datetime.now().isoformat(),
            "timestamp_atualizacao": None,
            "analises": {},
            "metadados": {
                "total_analises": 0,
                "com_release": 0,
                "sem_release": 0
            }
        }
    
    def _carregar_historico(self) -> List[Dict]:
        """Carrega histórico de análises"""
        if self.historico_file.exists():
            try:
                with open(self.historico_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def salvar_cache(self):
        """Salva cache no disco"""
        try:
            self.cache["timestamp_atualizacao"] = datetime.now().isoformat()
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Cache salvo: {self.cache['metadados']['total_analises']} análises")
        except Exception as e:
            print(f"❌ Erro ao salvar cache: {e}")
    
    def adicionar_analise(
        self, 
        ticker: str, 
        analise: Dict,
        tem_release: bool = False,
        release_hash: Optional[str] = None,
        dados_hash: Optional[str] = None
    ):
        """
        Adiciona ou atualiza análise no cache
        
        Args:
            ticker: Código da ação
            analise: Dados da análise
            tem_release: Se tem release disponível
            release_hash: Hash do release (para detectar mudanças)
            dados_hash: Hash dos dados fundamentalistas
        """
        self.cache["analises"][ticker] = {
            "ticker": ticker,
            "analise": analise,
            "timestamp": datetime.now().isoformat(),
            "tem_release": tem_release,
            "release_hash": release_hash,
            "dados_hash": dados_hash
        }
        
        # Atualiza metadados
        self._atualizar_metadados()
    
    def obter_analise(self, ticker: str) -> Optional[Dict]:
        """Retorna análise do cache"""
        return self.cache["analises"].get(ticker)
    
    def precisa_reanalisar(
        self, 
        ticker: str,
        tem_release_novo: bool = False,
        release_hash_novo: Optional[str] = None,
        dados_hash_novo: Optional[str] = None,
        max_idade_horas: int = 24
    ) -> bool:
        """
        Verifica se empresa precisa ser reanalisada
        
        Motivos para reanalisar:
        1. Não tem cache
        2. Cache muito antigo (> max_idade_horas)
        3. Release novo disponível
        4. Dados fundamentalistas mudaram
        
        Returns:
            True se precisa reanalisar
        """
        cache_ticker = self.obter_analise(ticker)
        
        # Sem cache - precisa analisar
        if not cache_ticker:
            return True
        
        # Verifica idade do cache
        try:
            timestamp = datetime.fromisoformat(cache_ticker["timestamp"])
            idade = datetime.now() - timestamp
            
            if idade > timedelta(hours=max_idade_horas):
                print(f"🔄 {ticker}: Cache antigo ({idade.total_seconds() / 3600:.1f}h)")
                return True
        except:
            return True
        
        # Verifica se tem release novo
        if tem_release_novo and not cache_ticker.get("tem_release"):
            print(f"🔄 {ticker}: Release novo detectado")
            return True
        
        # Verifica se release mudou
        if release_hash_novo and cache_ticker.get("release_hash") != release_hash_novo:
            print(f"🔄 {ticker}: Release atualizado")
            return True
        
        # Verifica se dados mudaram
        if dados_hash_novo and cache_ticker.get("dados_hash") != dados_hash_novo:
            print(f"🔄 {ticker}: Dados fundamentalistas atualizados")
            return True
        
        return False
    
    def _atualizar_metadados(self):
        """Atualiza metadados do cache"""
        total = len(self.cache["analises"])
        com_release = sum(1 for a in self.cache["analises"].values() if a.get("tem_release"))
        sem_release = total - com_release
        
        self.cache["metadados"] = {
            "total_analises": total,
            "com_release": com_release,
            "sem_release": sem_release
        }
    
    def gerar_ranking(self) -> List[Dict]:
        """
        Gera ranking ordenado por score
        
        Returns:
            Lista de análises ordenadas
        """
        analises = []
        
        for ticker, cache_item in self.cache["analises"].items():
            analise = cache_item.get("analise", {})
            if analise:
                analises.append({
                    **analise,
                    "ticker": ticker,
                    "timestamp_analise": cache_item.get("timestamp"),
                    "tem_release": cache_item.get("tem_release", False)
                })
        
        # Ordena por score (decrescente)
        analises.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        # Adiciona rank
        for i, analise in enumerate(analises, 1):
            analise["rank"] = i
        
        return analises
    
    def salvar_ranking(self, ranking: List[Dict]):
        """Salva ranking atual"""
        try:
            dados_ranking = {
                "versao": "1.0",
                "timestamp": datetime.now().isoformat(),
                "total": len(ranking),
                "ranking": ranking,
                "metadados": {
                    "com_release": sum(1 for r in ranking if r.get("tem_release")),
                    "sem_release": sum(1 for r in ranking if not r.get("tem_release")),
                    "score_medio": sum(r.get("score", 0) for r in ranking) / len(ranking) if ranking else 0
                }
            }
            
            with open(self.ranking_file, 'w', encoding='utf-8') as f:
                json.dump(dados_ranking, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Ranking salvo: {len(ranking)} empresas")
        except Exception as e:
            print(f"❌ Erro ao salvar ranking: {e}")
    
    def obter_ranking_atual(self) -> Optional[Dict]:
        """Retorna ranking atual salvo"""
        if self.ranking_file.exists():
            try:
                with open(self.ranking_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except:
                return None
        return None
    
    def adicionar_ao_historico(self, evento: Dict):
        """Adiciona evento ao histórico"""
        self.historico.append({
            **evento,
            "timestamp": datetime.now().isoformat()
        })
        
        # Mantém apenas últimos 100 eventos
        self.historico = self.historico[-100:]
        
        try:
            with open(self.historico_file, 'w', encoding='utf-8') as f:
                json.dump(self.historico, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar histórico: {e}")
    
    def limpar_cache(self):
        """Limpa todo o cache"""
        self.cache = self._criar_cache_vazio()
        self.salvar_cache()
        print("✓ Cache limpo")
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do cache"""
        return {
            "total_analises": self.cache["metadados"]["total_analises"],
            "com_release": self.cache["metadados"]["com_release"],
            "sem_release": self.cache["metadados"]["sem_release"],
            "timestamp_criacao": self.cache.get("timestamp_criacao"),
            "timestamp_atualizacao": self.cache.get("timestamp_atualizacao"),
            "total_historico": len(self.historico)
        }
