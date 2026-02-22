"""
Gerenciador de CSV - Upload e validação
"""
import os
import shutil
from datetime import datetime
from typing import Optional, Dict, Any
import pandas as pd
import logging
import math

logger = logging.getLogger(__name__)


def sanitize_float(value: Any) -> Any:
    """
    Sanitiza valores float para garantir que são JSON compliant
    Converte NaN, Infinity para None ou 0
    """
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return 0
    return value


def sanitize_dict(data: Dict) -> Dict:
    """
    Sanitiza todos os valores float em um dicionário recursivamente
    """
    result = {}
    for key, value in data.items():
        if isinstance(value, dict):
            result[key] = sanitize_dict(value)
        elif isinstance(value, list):
            result[key] = [sanitize_float(v) if not isinstance(v, dict) else sanitize_dict(v) for v in value]
        else:
            result[key] = sanitize_float(value)
    return result


class CSVManager:
    """
    Gerencia upload e validação de CSV de ações
    
    Features:
    - Upload de CSV atualizado
    - Validação de colunas obrigatórias
    - Backup automático do CSV anterior
    - Logs de atualizações
    """
    
    def __init__(self):
        self.csv_path = "data/stocks.csv"
        self.backup_dir = "data/backups"
        self.log_file = "data/csv_updates.log"
        
        # Cria diretórios se não existirem
        os.makedirs("data", exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Colunas obrigatórias no CSV
        self.colunas_obrigatorias = [
            "ticker",  # ou "Ticker"
            "roe",     # ou "ROE"
            "pl"       # ou "PL"
        ]
        
        # Colunas opcionais (bom ter, mas não obrigatório)
        self.colunas_opcionais = [
            "cagr",    # ou "CAGR" ou "crescimento"
            "setor",   # ou "Setor"
            "nome"     # ou "Nome"
        ]
        
        logger.info("✓ CSV Manager inicializado")
    
    def validar_csv(self, file_path: str) -> Dict:
        """
        Valida se o CSV tem as colunas necessárias
        
        Returns:
            Dict com status e mensagem
        """
        try:
            # Lê CSV com encoding correto para UTF-8 BOM
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            
            # Normaliza nomes das colunas (lowercase)
            colunas_lower = {col.lower(): col for col in df.columns}
            
            # Mapeamento de colunas aceitas (mais flexível)
            mapeamento_colunas = {
                'ticker': ['ticker', 'código', 'codigo', 'ação', 'acao', 'papel'],
                'roe': ['roe', 'return on equity', 'retorno sobre patrimônio', 'retorno sobre patrimonio'],
                'pl': ['pl', 'p/l', 'preço/lucro', 'preco/lucro', 'price/earnings', 'p/e']
            }
            
            # Colunas opcionais
            mapeamento_opcionais = {
                'cagr': ['cagr', 'crescimento', 'cresc. receitas 5 anos', 'cresc receitas', 'crescimento receita'],
                'setor': ['setor', 'sector', 'segmento'],
                'nome': ['nome', 'name', 'empresa', 'razão social', 'razao social']
            }
            
            # Verifica colunas obrigatórias
            colunas_encontradas = {}
            colunas_faltando = []
            
            for col_obrigatoria, variacoes in mapeamento_colunas.items():
                encontrada = False
                for variacao in variacoes:
                    if variacao in colunas_lower:
                        colunas_encontradas[col_obrigatoria] = colunas_lower[variacao]
                        encontrada = True
                        break
                
                if not encontrada:
                    colunas_faltando.append(col_obrigatoria)
            
            # Verifica colunas opcionais (não obrigatórias)
            for col_opcional, variacoes in mapeamento_opcionais.items():
                for variacao in variacoes:
                    if variacao in colunas_lower:
                        colunas_encontradas[col_opcional] = colunas_lower[variacao]
                        break
            
            if colunas_faltando:
                return {
                    "valido": False,
                    "erro": f"Colunas faltando: {', '.join(colunas_faltando)}",
                    "colunas_encontradas": list(df.columns),
                    "colunas_obrigatorias": list(mapeamento_colunas.keys()),
                    "sugestao": "Verifique se o CSV tem as colunas obrigatórias: ticker, ROE, P/L"
                }
            
            # Verifica se tem dados
            if len(df) == 0:
                return {
                    "valido": False,
                    "erro": "CSV vazio (sem dados)",
                    "total_linhas": 0
                }
            
            # Verifica se tem pelo menos 30 ações (reduzido de 50)
            if len(df) < 30:
                return {
                    "valido": False,
                    "erro": f"CSV com poucas ações ({len(df)}). Mínimo: 30",
                    "total_linhas": len(df)
                }
            
            # Normaliza nomes das colunas no DataFrame
            rename_map = {}
            for col_padrao, col_original in colunas_encontradas.items():
                if col_original != col_padrao:
                    rename_map[col_original] = col_padrao
            
            if rename_map:
                df.rename(columns=rename_map, inplace=True)
                # Salva CSV normalizado
                df.to_csv(file_path, index=False)
            
            # Se não tem CAGR, adiciona coluna com valor padrão (0)
            if 'cagr' not in df.columns:
                df['cagr'] = 0
                df.to_csv(file_path, index=False)
            
            # Validação OK
            return {
                "valido": True,
                "total_acoes": len(df),
                "colunas": list(df.columns),
                "colunas_normalizadas": list(colunas_encontradas.keys()),
                "colunas_adicionadas": ['cagr'] if 'cagr' not in colunas_encontradas else [],
                "amostra": df.head(5).to_dict('records')
            }
        
        except Exception as e:
            return {
                "valido": False,
                "erro": f"Erro ao ler CSV: {str(e)}"
            }
    
    def fazer_backup(self) -> Optional[str]:
        """
        Faz backup do CSV atual antes de substituir
        
        Returns:
            Path do backup ou None se não havia CSV
        """
        if not os.path.exists(self.csv_path):
            return None
        
        try:
            # Nome do backup com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"stocks_{timestamp}.csv")
            
            # Copia arquivo
            shutil.copy2(self.csv_path, backup_path)
            
            logger.info(f"✓ Backup criado: {backup_path}")
            return backup_path
        
        except Exception as e:
            logger.error(f"Erro ao criar backup: {e}")
            return None
    
    def atualizar_csv(self, novo_csv_path: str, usuario: str = "admin") -> Dict:
        """
        Atualiza o CSV principal com validação e backup
        
        Args:
            novo_csv_path: Path do novo CSV
            usuario: Usuário que fez o upload
        
        Returns:
            Dict com resultado da operação
        """
        try:
            # 1. Valida novo CSV
            validacao = self.validar_csv(novo_csv_path)
            
            if not validacao["valido"]:
                return {
                    "sucesso": False,
                    "erro": validacao["erro"],
                    "detalhes": validacao
                }
            
            # 2. Faz backup do CSV atual
            backup_path = self.fazer_backup()
            
            # 3. Substitui CSV
            shutil.copy2(novo_csv_path, self.csv_path)
            
            # 4. Registra no log
            self._registrar_atualizacao(usuario, validacao["total_acoes"], backup_path)
            
            # 5. Limpa backups antigos (mantém últimos 10)
            self._limpar_backups_antigos()
            
            logger.info(f"✓ CSV atualizado: {validacao['total_acoes']} ações")
            
            return {
                "sucesso": True,
                "total_acoes": validacao["total_acoes"],
                "backup": backup_path,
                "timestamp": datetime.now().isoformat(),
                "usuario": usuario
            }
        
        except Exception as e:
            logger.error(f"Erro ao atualizar CSV: {e}")
            return {
                "sucesso": False,
                "erro": f"Erro ao atualizar: {str(e)}"
            }
    
    def _registrar_atualizacao(self, usuario: str, total_acoes: int, backup_path: Optional[str]):
        """Registra atualização no log"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"[{timestamp}] Usuário: {usuario} | Ações: {total_acoes} | Backup: {backup_path or 'N/A'}\n"
            
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        
        except Exception as e:
            logger.error(f"Erro ao registrar log: {e}")
    
    def _limpar_backups_antigos(self, manter: int = 10):
        """Mantém apenas os últimos N backups"""
        try:
            backups = sorted(
                [f for f in os.listdir(self.backup_dir) if f.startswith("stocks_")],
                reverse=True
            )
            
            # Remove backups antigos
            for backup in backups[manter:]:
                backup_path = os.path.join(self.backup_dir, backup)
                os.remove(backup_path)
                logger.debug(f"Backup antigo removido: {backup}")
        
        except Exception as e:
            logger.error(f"Erro ao limpar backups: {e}")
    
    def obter_info_csv_atual(self) -> Dict:
        """
        Retorna informações sobre o CSV atual
        
        Returns:
            Dict com informações do CSV
        """
        if not os.path.exists(self.csv_path):
            return {
                "existe": False,
                "erro": "CSV não encontrado"
            }
        
        try:
            # Informações do arquivo
            stat = os.stat(self.csv_path)
            ultima_modificacao = datetime.fromtimestamp(stat.st_mtime)
            tamanho_kb = stat.st_size / 1024
            
            # Lê CSV
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            # Idade do CSV
            idade = datetime.now() - ultima_modificacao
            idade_horas = idade.total_seconds() / 3600
            
            # Garante que não é NaN ou infinito
            if not math.isfinite(idade_horas):
                idade_horas = 0
            idade_horas = max(0, round(idade_horas, 1))
            
            result = {
                "existe": True,
                "total_acoes": len(df),
                "colunas": list(df.columns),
                "ultima_modificacao": ultima_modificacao.strftime("%d/%m/%Y %H:%M:%S"),
                "idade_horas": idade_horas,
                "tamanho_kb": round(tamanho_kb, 2),
                "atualizado": idade_horas < 24,  # Considera atualizado se < 24h
                "amostra": df.head(3).to_dict('records')
            }
            
            # Sanitiza todos os valores float
            return sanitize_dict(result)
        
        except Exception as e:
            return {
                "existe": True,
                "erro": f"Erro ao ler CSV: {str(e)}"
            }
    
    def obter_historico_atualizacoes(self, limite: int = 10) -> list:
        """
        Retorna histórico de atualizações
        
        Returns:
            Lista com últimas atualizações
        """
        if not os.path.exists(self.log_file):
            return []
        
        try:
            with open(self.log_file, "r", encoding="utf-8-sig") as f:
                linhas = f.readlines()
            
            # Retorna últimas N linhas
            return [linha.strip() for linha in linhas[-limite:]]
        
        except Exception as e:
            logger.error(f"Erro ao ler histórico: {e}")
            return []


# Singleton
_csv_manager: Optional[CSVManager] = None


def get_csv_manager() -> CSVManager:
    """Retorna instância singleton"""
    global _csv_manager
    
    if _csv_manager is None:
        _csv_manager = CSVManager()
    
    return _csv_manager
