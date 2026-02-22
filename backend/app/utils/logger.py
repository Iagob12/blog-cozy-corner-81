"""
Logger - Sistema de logging com timestamp e contexto
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "alpha_system", log_file: str = "logs/alpha_system.log") -> logging.Logger:
    """
    Configura logger com formato padrão e rotação
    
    Args:
        name: Nome do logger
        log_file: Caminho do arquivo de log
    
    Returns:
        Logger configurado
    """
    
    # Cria diretório de logs se não existir
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Cria logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Remove handlers existentes (evita duplicação)
    logger.handlers.clear()
    
    # Formato: [TIMESTAMP] [LEVEL] [CONTEXT] Message
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (com rotação)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def log_etapa(logger: logging.Logger, etapa: str, mensagem: str, nivel: str = "info"):
    """
    Log com contexto de etapa
    
    Args:
        logger: Logger instance
        etapa: Nome da etapa (ex: "PROMPT_1", "CSV", "RELEASE")
        mensagem: Mensagem do log
        nivel: "info", "warning", "error"
    """
    
    msg_formatada = f"[{etapa}] {mensagem}"
    
    if nivel == "info":
        logger.info(msg_formatada)
    elif nivel == "warning":
        logger.warning(msg_formatada)
    elif nivel == "error":
        logger.error(msg_formatada)


def log_ticker(logger: logging.Logger, ticker: str, mensagem: str, nivel: str = "info"):
    """
    Log com contexto de ticker
    
    Args:
        logger: Logger instance
        ticker: Ticker da ação
        mensagem: Mensagem do log
        nivel: "info", "warning", "error"
    """
    
    msg_formatada = f"[{ticker}] {mensagem}"
    
    if nivel == "info":
        logger.info(msg_formatada)
    elif nivel == "warning":
        logger.warning(msg_formatada)
    elif nivel == "error":
        logger.error(msg_formatada)


def log_separador(logger: logging.Logger, titulo: str = ""):
    """Log de separador visual"""
    
    if titulo:
        logger.info("=" * 60)
        logger.info(f"  {titulo}")
        logger.info("=" * 60)
    else:
        logger.info("=" * 60)


def log_inicio_analise(logger: logging.Logger):
    """Log de início de análise completa"""
    
    log_separador(logger, "ALPHA SYSTEM V3 - ANÁLISE COMPLETA")
    logger.info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    logger.info("")


def log_fim_analise(logger: logging.Logger, sucesso: bool, total_aprovadas: int = 0):
    """Log de fim de análise"""
    
    logger.info("")
    log_separador(logger)
    
    if sucesso:
        logger.info(f"✓ ANÁLISE CONCLUÍDA COM SUCESSO")
        logger.info(f"✓ Total de ações aprovadas: {total_aprovadas}")
    else:
        logger.error(f"✗ ANÁLISE FALHOU")
    
    logger.info(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    log_separador(logger)


# Logger global
_global_logger: logging.Logger = None


def get_logger() -> logging.Logger:
    """Retorna logger global (singleton)"""
    global _global_logger
    
    if _global_logger is None:
        _global_logger = setup_logger()
    
    return _global_logger
