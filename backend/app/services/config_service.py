"""
Serviço de Configuração Persistente
Gerencia configurações do sistema em arquivo JSON
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime


class ConfigService:
    """Gerencia configurações persistentes do sistema"""
    
    def __init__(self, config_file: str = "data/config/sistema.json"):
        self.config_file = config_file
        self._config: Optional[Dict[str, Any]] = None
        self._carregar_config()
    
    def _carregar_config(self):
        """Carrega configuração do arquivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                    self._config = json.load(f)
                print(f"✓ Configuração carregada de {self.config_file}")
            else:
                print(f"⚠️ Arquivo de configuração não encontrado: {self.config_file}")
                self._config = self._config_padrao()
                self._salvar_config()
        except Exception as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            self._config = self._config_padrao()
    
    def _config_padrao(self) -> Dict[str, Any]:
        """Retorna configuração padrão"""
        return {
            "versao": "1.0.0",
            "ultima_atualizacao": datetime.now().isoformat(),
            "scheduler_estrategia": {
                "ativo": True,
                "intervalo_minutos": 60,
                "auto_start": True
            },
            "analise": {
                "usar_consenso_padrao": True,
                "num_execucoes_consenso": 5,
                "min_aparicoes_consenso": 3
            },
            "cache_precos": {
                "ativo": True,
                "tempo_expiracao_horas": 24,
                "usar_fallback": True
            },
            "notas_estruturadas": {
                "ativo": True,
                "divergencia_maxima": 2.0,
                "pesos": {
                    "fundamentos": 0.30,
                    "catalisadores": 0.30,
                    "valuation": 0.20,
                    "gestao": 0.20
                }
            },
            "alertas": {
                "ativo": True,
                "tipos": ["OPORTUNIDADE", "STOP", "ALVO", "AGUARDAR"]
            }
        }
    
    def _salvar_config(self):
        """Salva configuração no arquivo"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # Atualiza timestamp
            if self._config:
                self._config["ultima_atualizacao"] = datetime.now().isoformat()
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Configuração salva em {self.config_file}")
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
    
    def obter(self, chave: str, padrao: Any = None) -> Any:
        """
        Obtém valor de configuração
        
        Args:
            chave: Chave no formato "secao.campo" (ex: "scheduler_estrategia.ativo")
            padrao: Valor padrão se não encontrado
        
        Returns:
            Valor da configuração ou padrão
        """
        if not self._config:
            return padrao
        
        partes = chave.split('.')
        valor = self._config
        
        for parte in partes:
            if isinstance(valor, dict) and parte in valor:
                valor = valor[parte]
            else:
                return padrao
        
        return valor
    
    def definir(self, chave: str, valor: Any):
        """
        Define valor de configuração
        
        Args:
            chave: Chave no formato "secao.campo"
            valor: Novo valor
        """
        if not self._config:
            self._config = self._config_padrao()
        
        partes = chave.split('.')
        config_atual = self._config
        
        # Navega até o penúltimo nível
        for parte in partes[:-1]:
            if parte not in config_atual:
                config_atual[parte] = {}
            config_atual = config_atual[parte]
        
        # Define valor
        config_atual[partes[-1]] = valor
        
        # Salva
        self._salvar_config()
    
    def obter_secao(self, secao: str) -> Dict[str, Any]:
        """
        Obtém seção completa de configuração
        
        Args:
            secao: Nome da seção (ex: "scheduler_estrategia")
        
        Returns:
            Dicionário com configurações da seção
        """
        if not self._config or secao not in self._config:
            return {}
        
        return self._config[secao]
    
    def atualizar_secao(self, secao: str, valores: Dict[str, Any]):
        """
        Atualiza seção completa
        
        Args:
            secao: Nome da seção
            valores: Novos valores
        """
        if not self._config:
            self._config = self._config_padrao()
        
        if secao not in self._config:
            self._config[secao] = {}
        
        self._config[secao].update(valores)
        self._salvar_config()
    
    def obter_todas(self) -> Dict[str, Any]:
        """Retorna todas as configurações"""
        return self._config or {}
    
    def resetar(self):
        """Reseta configurações para padrão"""
        self._config = self._config_padrao()
        self._salvar_config()
        print("✓ Configurações resetadas para padrão")


# Singleton
_config_service = None

def get_config_service() -> ConfigService:
    """Retorna instância singleton do serviço de configuração"""
    global _config_service
    if _config_service is None:
        _config_service = ConfigService()
    return _config_service
