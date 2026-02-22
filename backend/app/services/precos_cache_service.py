"""
Serviço de Cache de Preços — Fallback inteligente quando Brapi falha

Mantém cache de preços com timestamp e usa preços recentes
quando API está offline
"""
import json
import os
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta


class PrecosCacheService:
    """
    Cache inteligente de preços com fallback
    
    Features:
    - Salva preços com timestamp
    - Fallback automático quando API falha
    - Indicadores de idade (🟢🟡🔴)
    - Atualização automática quando API volta
    """
    
    def __init__(self):
        self.cache_dir = "data/cache"
        self.cache_file = os.path.join(self.cache_dir, "precos_cache.json")
        os.makedirs(self.cache_dir, exist_ok=True)
        self.cache = self._carregar_cache()
        print("✓ Preços Cache Service inicializado")
    
    def _carregar_cache(self) -> Dict:
        """Carrega cache do disco"""
        if not os.path.exists(self.cache_file):
            return {}
        
        try:
            with open(self.cache_file, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except:
            return {}
    
    def _salvar_cache(self):
        """Salva cache no disco"""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2, ensure_ascii=False)
    
    def atualizar_preco(
        self,
        ticker: str,
        preco: float,
        fonte: str = "brapi"
    ):
        """
        Atualiza preço no cache
        
        Args:
            ticker: Código da ação
            preco: Preço atual
            fonte: Fonte do preço (brapi, hgbrasil, etc)
        """
        self.cache[ticker] = {
            "preco": preco,
            "timestamp": datetime.now().isoformat(),
            "fonte": fonte
        }
        self._salvar_cache()
    
    def atualizar_precos_batch(
        self,
        precos: Dict[str, float],
        fonte: str = "brapi"
    ):
        """
        Atualiza múltiplos preços de uma vez
        
        Args:
            precos: Dict {ticker: preco}
            fonte: Fonte dos preços
        """
        timestamp = datetime.now().isoformat()
        
        for ticker, preco in precos.items():
            self.cache[ticker] = {
                "preco": preco,
                "timestamp": timestamp,
                "fonte": fonte
            }
        
        self._salvar_cache()
        print(f"💾 {len(precos)} preços atualizados no cache")
    
    def obter_preco(
        self,
        ticker: str,
        max_idade_minutos: int = 120
    ) -> Optional[Tuple[float, str, int]]:
        """
        Obtém preço do cache
        
        Args:
            ticker: Código da ação
            max_idade_minutos: Idade máxima aceitável (padrão: 2h)
        
        Returns:
            (preco, indicador, idade_minutos) ou None
            Indicador: 🟢 (< 30min), 🟡 (30min-2h), 🔴 (> 2h)
        """
        if ticker not in self.cache:
            return None
        
        dados = self.cache[ticker]
        preco = dados["preco"]
        timestamp_str = dados["timestamp"]
        
        # Calcula idade
        timestamp = datetime.fromisoformat(timestamp_str)
        idade = datetime.now() - timestamp
        idade_minutos = int(idade.total_seconds() / 60)
        
        # Define indicador
        if idade_minutos < 30:
            indicador = "🟢"  # Atualizado
        elif idade_minutos < 120:
            indicador = "🟡"  # Recente
        else:
            indicador = "🔴"  # Antigo
        
        # Verifica se está muito antigo
        if idade_minutos > max_idade_minutos:
            return None
        
        return (preco, indicador, idade_minutos)
    
    def obter_precos_batch(
        self,
        tickers: list[str],
        max_idade_minutos: int = 120
    ) -> Dict[str, Dict]:
        """
        Obtém múltiplos preços do cache
        
        Returns:
            Dict {ticker: {preco, indicador, idade_minutos}}
        """
        resultado = {}
        
        for ticker in tickers:
            dados = self.obter_preco(ticker, max_idade_minutos)
            if dados:
                preco, indicador, idade = dados
                resultado[ticker] = {
                    "preco": preco,
                    "indicador": indicador,
                    "idade_minutos": idade
                }
        
        return resultado
    
    def limpar_cache_antigo(self, max_dias: int = 7):
        """
        Remove preços muito antigos do cache
        
        Args:
            max_dias: Idade máxima em dias (padrão: 7)
        """
        limite = datetime.now() - timedelta(days=max_dias)
        removidos = 0
        
        tickers_remover = []
        for ticker, dados in self.cache.items():
            timestamp = datetime.fromisoformat(dados["timestamp"])
            if timestamp < limite:
                tickers_remover.append(ticker)
        
        for ticker in tickers_remover:
            del self.cache[ticker]
            removidos += 1
        
        if removidos > 0:
            self._salvar_cache()
            print(f"🧹 {removidos} preços antigos removidos do cache")
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do cache"""
        if not self.cache:
            return {
                "total": 0,
                "atualizados": 0,
                "recentes": 0,
                "antigos": 0
            }
        
        atualizados = 0  # < 30min
        recentes = 0     # 30min-2h
        antigos = 0      # > 2h
        
        for ticker, dados in self.cache.items():
            try:
                # Verifica se tem timestamp
                if "timestamp" not in dados:
                    antigos += 1
                    continue
                
                timestamp = datetime.fromisoformat(dados["timestamp"])
                idade = datetime.now() - timestamp
                idade_minutos = int(idade.total_seconds() / 60)
                
                if idade_minutos < 30:
                    atualizados += 1
                elif idade_minutos < 120:
                    recentes += 1
                else:
                    antigos += 1
            except Exception as e:
                # Se der erro, conta como antigo
                antigos += 1
        
        return {
            "total": len(self.cache),
            "atualizados": atualizados,
            "recentes": recentes,
            "antigos": antigos
        }


# Singleton
_precos_cache_service = None

def get_precos_cache_service() -> PrecosCacheService:
    """Retorna instância singleton"""
    global _precos_cache_service
    if _precos_cache_service is None:
        _precos_cache_service = PrecosCacheService()
    return _precos_cache_service
