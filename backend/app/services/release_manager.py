"""
Release Manager - Gerenciamento de Releases de Resultados
Armazena e gerencia releases de empresas para análise
"""
import os
import shutil
from datetime import datetime
from typing import Optional, Dict, List
import logging
import json

logger = logging.getLogger(__name__)


class ReleaseManager:
    """
    Gerencia releases de resultados das empresas
    
    Features:
    - Upload de releases (PDFs)
    - Armazenamento organizado por ticker
    - Metadados (trimestre, ano, data upload)
    - Busca de releases disponíveis
    - Validação de freshness
    """
    
    def __init__(self):
        self.releases_dir = "data/releases"
        self.metadata_file = "data/releases_metadata.json"
        
        # Cria diretórios
        os.makedirs(self.releases_dir, exist_ok=True)
        
        # Carrega metadados
        self.metadata = self._load_metadata()
        
        logger.info("✓ Release Manager inicializado")
    
    def _load_metadata(self) -> Dict:
        """Carrega metadados dos releases"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Erro ao carregar metadados: {e}")
                return {}
        return {}
    
    def _save_metadata(self):
        """Salva metadados dos releases"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {e}")
    
    def adicionar_release(
        self,
        ticker: str,
        file_path: str,
        trimestre: str,
        ano: int,
        usuario: str = "admin"
    ) -> Dict:
        """
        Adiciona release de uma empresa
        
        Args:
            ticker: Código da ação (ex: PRIO3)
            file_path: Path do arquivo PDF
            trimestre: Q1, Q2, Q3 ou Q4
            ano: Ano do release (ex: 2025)
            usuario: Usuário que fez upload
        
        Returns:
            Dict com resultado da operação
        """
        try:
            # Valida arquivo
            if not os.path.exists(file_path):
                return {
                    "sucesso": False,
                    "erro": "Arquivo não encontrado"
                }
            
            if not file_path.lower().endswith('.pdf'):
                return {
                    "sucesso": False,
                    "erro": "Apenas arquivos PDF são aceitos"
                }
            
            # Valida trimestre
            if trimestre not in ['Q1', 'Q2', 'Q3', 'Q4']:
                return {
                    "sucesso": False,
                    "erro": "Trimestre inválido (use Q1, Q2, Q3 ou Q4)"
                }
            
            # Nome do arquivo: TICKER_Q4_2025.pdf
            filename = f"{ticker}_{trimestre}_{ano}.pdf"
            dest_path = os.path.join(self.releases_dir, filename)
            
            # Copia arquivo
            shutil.copy2(file_path, dest_path)
            
            # Atualiza metadados
            if ticker not in self.metadata:
                self.metadata[ticker] = []
            
            # Remove release antigo do mesmo trimestre/ano (se existir)
            self.metadata[ticker] = [
                r for r in self.metadata[ticker]
                if not (r['trimestre'] == trimestre and r['ano'] == ano)
            ]
            
            # Adiciona novo release
            self.metadata[ticker].append({
                "trimestre": trimestre,
                "ano": ano,
                "filename": filename,
                "path": dest_path,
                "data_upload": datetime.now().isoformat(),
                "usuario": usuario,
                "tamanho_kb": os.path.getsize(dest_path) / 1024
            })
            
            # Ordena por ano/trimestre (mais recente primeiro)
            self.metadata[ticker].sort(
                key=lambda x: (x['ano'], x['trimestre']),
                reverse=True
            )
            
            self._save_metadata()
            
            logger.info(f"✓ Release adicionado: {ticker} {trimestre} {ano}")
            
            return {
                "sucesso": True,
                "ticker": ticker,
                "trimestre": trimestre,
                "ano": ano,
                "filename": filename,
                "path": dest_path
            }
        
        except Exception as e:
            logger.error(f"Erro ao adicionar release: {e}")
            return {
                "sucesso": False,
                "erro": str(e)
            }
    
    def obter_release_mais_recente(self, ticker: str) -> Optional[Dict]:
        """
        Obtém o release mais recente de uma empresa
        
        Returns:
            Dict com informações do release ou None
        """
        if ticker not in self.metadata or not self.metadata[ticker]:
            return None
        
        # Já está ordenado (mais recente primeiro)
        release = self.metadata[ticker][0]
        
        # Verifica se arquivo existe
        if not os.path.exists(release['path']):
            logger.warning(f"Release não encontrado: {release['path']}")
            return None
        
        return release
    
    def obter_todos_releases(self, ticker: str) -> List[Dict]:
        """Obtém todos os releases de uma empresa"""
        if ticker not in self.metadata:
            return []
        
        # Filtra apenas releases que existem
        releases_validos = []
        for release in self.metadata[ticker]:
            if os.path.exists(release['path']):
                releases_validos.append(release)
        
        return releases_validos
    
    def listar_empresas_com_releases(self) -> List[str]:
        """Lista todas as empresas que têm releases"""
        empresas = []
        for ticker in self.metadata:
            if self.obter_release_mais_recente(ticker):
                empresas.append(ticker)
        
        return sorted(empresas)
    
    def verificar_releases_pendentes(self, tickers: List[str]) -> Dict:
        """
        Verifica quais empresas precisam de releases
        
        Args:
            tickers: Lista de tickers para verificar
        
        Returns:
            Dict com empresas que têm/não têm releases
        """
        com_release = []
        sem_release = []
        
        for ticker in tickers:
            release = self.obter_release_mais_recente(ticker)
            if release:
                com_release.append({
                    "ticker": ticker,
                    "trimestre": release['trimestre'],
                    "ano": release['ano'],
                    "data_upload": release['data_upload']
                })
            else:
                sem_release.append(ticker)
        
        return {
            "total": len(tickers),
            "com_release": com_release,
            "sem_release": sem_release,
            "percentual_completo": (len(com_release) / len(tickers) * 100) if tickers else 0
        }
    
    def remover_release(self, ticker: str, trimestre: str, ano: int) -> Dict:
        """Remove um release específico"""
        try:
            if ticker not in self.metadata:
                return {
                    "sucesso": False,
                    "erro": "Empresa não encontrada"
                }
            
            # Encontra release
            release = None
            for r in self.metadata[ticker]:
                if r['trimestre'] == trimestre and r['ano'] == ano:
                    release = r
                    break
            
            if not release:
                return {
                    "sucesso": False,
                    "erro": "Release não encontrado"
                }
            
            # Remove arquivo
            if os.path.exists(release['path']):
                os.remove(release['path'])
            
            # Remove dos metadados
            self.metadata[ticker] = [
                r for r in self.metadata[ticker]
                if not (r['trimestre'] == trimestre and r['ano'] == ano)
            ]
            
            # Remove ticker se não tem mais releases
            if not self.metadata[ticker]:
                del self.metadata[ticker]
            
            self._save_metadata()
            
            logger.info(f"✓ Release removido: {ticker} {trimestre} {ano}")
            
            return {
                "sucesso": True,
                "ticker": ticker,
                "trimestre": trimestre,
                "ano": ano
            }
        
        except Exception as e:
            logger.error(f"Erro ao remover release: {e}")
            return {
                "sucesso": False,
                "erro": str(e)
            }
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas gerais dos releases"""
        total_empresas = len(self.metadata)
        total_releases = sum(len(releases) for releases in self.metadata.values())
        
        # Releases por trimestre
        por_trimestre = {"Q1": 0, "Q2": 0, "Q3": 0, "Q4": 0}
        por_ano = {}
        
        for releases in self.metadata.values():
            for release in releases:
                por_trimestre[release['trimestre']] += 1
                ano = release['ano']
                por_ano[ano] = por_ano.get(ano, 0) + 1
        
        return {
            "total_empresas": total_empresas,
            "total_releases": total_releases,
            "por_trimestre": por_trimestre,
            "por_ano": por_ano,
            "empresas": self.listar_empresas_com_releases()
        }


# Singleton
_release_manager: Optional[ReleaseManager] = None


def get_release_manager() -> ReleaseManager:
    """Retorna instância singleton"""
    global _release_manager
    
    if _release_manager is None:
        _release_manager = ReleaseManager()
    
    return _release_manager
