"""
Validators - Validação rigorosa de freshness de dados
CRÍTICO: Garante que todos os dados estão atualizados
"""
import os
from datetime import datetime, timedelta
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class DataFreshnessError(Exception):
    """Exceção para dados muito antigos"""
    pass


def validar_csv_freshness(csv_path: str, max_horas: int = 24) -> datetime:
    """
    Valida que CSV tem menos de X horas
    
    Args:
        csv_path: Caminho do arquivo CSV
        max_horas: Máximo de horas permitido (padrão: 24)
    
    Returns:
        datetime: Timestamp do arquivo
    
    Raises:
        DataFreshnessError: Se arquivo muito antigo ou não existe
    """
    
    if not os.path.exists(csv_path):
        raise DataFreshnessError(f"CSV não encontrado: {csv_path}")
    
    # Pega timestamp do arquivo
    file_timestamp = datetime.fromtimestamp(os.path.getmtime(csv_path))
    
    # Calcula idade
    idade = datetime.now() - file_timestamp
    horas_idade = idade.total_seconds() / 3600
    
    logger.info(
        f"[{datetime.now()}] [VALIDATOR] CSV: {horas_idade:.1f}h de idade "
        f"(máximo: {max_horas}h)"
    )
    
    # Valida
    if horas_idade > max_horas:
        raise DataFreshnessError(
            f"CSV muito antigo: {horas_idade:.1f}h (máximo: {max_horas}h). "
            f"Arquivo: {csv_path}"
        )
    
    logger.info(f"[{datetime.now()}] [VALIDATOR] ✓ CSV aprovado (freshness OK)")
    return file_timestamp


def validar_release_freshness(
    data_relatorio: datetime, 
    max_meses: int = 6
) -> bool:
    """
    Valida que Release tem menos de X meses
    
    Args:
        data_relatorio: Data do relatório trimestral
        max_meses: Máximo de meses permitido (padrão: 6)
    
    Returns:
        bool: True se válido
    
    Raises:
        DataFreshnessError: Se relatório muito antigo
    """
    
    # Calcula idade
    idade = datetime.now() - data_relatorio
    meses_idade = idade.days / 30
    
    logger.info(
        f"[{datetime.now()}] [VALIDATOR] Release: {meses_idade:.1f} meses de idade "
        f"(máximo: {max_meses} meses)"
    )
    
    # Valida
    if meses_idade > max_meses:
        raise DataFreshnessError(
            f"Release muito antigo: {meses_idade:.1f} meses (máximo: {max_meses} meses). "
            f"Data do relatório: {data_relatorio.strftime('%d/%m/%Y')}"
        )
    
    logger.info(f"[{datetime.now()}] [VALIDATOR] ✓ Release aprovado (freshness OK)")
    return True


def validar_preco_freshness(
    timestamp_preco: datetime, 
    max_horas: int = 24
) -> bool:
    """
    Valida que preço tem menos de X horas
    
    Args:
        timestamp_preco: Timestamp da consulta de preço
        max_horas: Máximo de horas permitido (padrão: 24)
    
    Returns:
        bool: True se válido
    
    Raises:
        DataFreshnessError: Se preço muito antigo
    """
    
    # Calcula idade
    idade = datetime.now() - timestamp_preco
    horas_idade = idade.total_seconds() / 3600
    
    logger.info(
        f"[{datetime.now()}] [VALIDATOR] Preço: {horas_idade:.1f}h de idade "
        f"(máximo: {max_horas}h)"
    )
    
    # Valida
    if horas_idade > max_horas:
        raise DataFreshnessError(
            f"Preço muito antigo: {horas_idade:.1f}h (máximo: {max_horas}h). "
            f"Timestamp: {timestamp_preco.strftime('%d/%m/%Y %H:%M:%S')}"
        )
    
    logger.info(f"[{datetime.now()}] [VALIDATOR] ✓ Preço aprovado (freshness OK)")
    return True


def validar_trimestre_release(trimestre: str, ano: int, minimo_trimestre: str = "Q1", minimo_ano: int = 2024) -> bool:
    """
    Valida que Release é de Q1 2024 ou mais recente
    
    ATUALIZADO: Aceita Q1 2024+ (qualquer trimestre de 2024)
    Motivo: Importante ter Release para análise, mesmo que seja Q1
    
    Args:
        trimestre: "Q1", "Q2", "Q3", "Q4"
        ano: Ano do relatório
        minimo_trimestre: Trimestre mínimo aceito (padrão: "Q1")
        minimo_ano: Ano mínimo aceito (padrão: 2024)
    
    Returns:
        bool: True se válido
    
    Raises:
        DataFreshnessError: Se trimestre muito antigo
    """
    
    # Converte trimestre para número
    trimestre_num = int(trimestre.replace("Q", ""))
    ref_trimestre = int(minimo_trimestre.replace("Q", ""))
    
    logger.info(
        f"[{datetime.now()}] [VALIDATOR] Trimestre: {trimestre} {ano} "
        f"(mínimo: {minimo_trimestre} {minimo_ano})"
    )
    
    # Valida
    if ano < minimo_ano:
        raise DataFreshnessError(
            f"Release muito antigo: {trimestre} {ano} (mínimo: {minimo_trimestre} {minimo_ano})"
        )
    
    if ano == minimo_ano and trimestre_num < ref_trimestre:
        raise DataFreshnessError(
            f"Release muito antigo: {trimestre} {ano} (mínimo: {minimo_trimestre} {minimo_ano})"
        )
    
    logger.info(f"[{datetime.now()}] [VALIDATOR] ✓ Trimestre aprovado")
    return True


def calcular_score_trimestre(trimestre: str, ano: int) -> float:
    """
    Calcula score de qualidade do trimestre (mais recente = maior score)
    
    Q4 2024 = 1.0
    Q3 2024 = 0.9
    Q2 2024 = 0.8
    Q1 2024 = 0.7
    Q4 2023 = 0.6
    etc.
    
    Args:
        trimestre: "Q1", "Q2", "Q3", "Q4"
        ano: Ano do relatório
    
    Returns:
        float: Score de 0.0 a 1.0
    """
    
    trimestre_num = int(trimestre.replace("Q", ""))
    
    # Referência: Q4 2024
    ref_ano = 2024
    ref_trimestre = 4
    
    # Calcula diferença em trimestres
    diff_anos = ref_ano - ano
    diff_trimestres = ref_trimestre - trimestre_num
    diff_total = (diff_anos * 4) + diff_trimestres
    
    # Score: 1.0 para Q4 2024, -0.1 para cada trimestre anterior
    score = 1.0 - (diff_total * 0.1)
    
    # Limita entre 0.0 e 1.0
    return max(0.0, min(1.0, score))


def validar_todos_dados(
    csv_timestamp: datetime,
    release_timestamp: datetime,
    preco_timestamp: datetime
) -> Dict[str, bool]:
    """
    Valida todos os dados de uma vez
    
    Returns:
        Dict com status de cada validação
    """
    
    logger.info(f"[{datetime.now()}] [VALIDATOR] Validando todos os dados...")
    
    resultados = {
        "csv_valido": False,
        "release_valido": False,
        "preco_valido": False,
        "todos_validos": False
    }
    
    try:
        # Valida CSV (simula validação com timestamp)
        idade_csv = (datetime.now() - csv_timestamp).total_seconds() / 3600
        if idade_csv <= 24:
            resultados["csv_valido"] = True
        else:
            raise DataFreshnessError(f"CSV muito antigo: {idade_csv:.1f}h")
        
        # Valida Release
        validar_release_freshness(release_timestamp)
        resultados["release_valido"] = True
        
        # Valida Preço
        validar_preco_freshness(preco_timestamp)
        resultados["preco_valido"] = True
        
        # Todos válidos
        resultados["todos_validos"] = True
        logger.info(f"[{datetime.now()}] [VALIDATOR] ✓ TODOS OS DADOS VÁLIDOS")
        
    except DataFreshnessError as e:
        logger.error(f"[{datetime.now()}] [VALIDATOR] ✗ Validação falhou: {e}")
        raise
    
    return resultados


def gerar_relatorio_freshness(
    csv_timestamp: datetime,
    release_timestamp: datetime,
    preco_timestamp: datetime
) -> str:
    """
    Gera relatório legível sobre freshness dos dados
    """
    
    agora = datetime.now()
    
    csv_idade = (agora - csv_timestamp).total_seconds() / 3600
    release_idade = (agora - release_timestamp).days
    preco_idade = (agora - preco_timestamp).total_seconds() / 3600
    
    relatorio = f"""
╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE FRESHNESS DOS DADOS                   ║
╠══════════════════════════════════════════════════════════════╣
║ Data/Hora da Análise: {agora.strftime('%d/%m/%Y %H:%M:%S')}            ║
║                                                              ║
║ CSV:                                                         ║
║   • Data: {csv_timestamp.strftime('%d/%m/%Y %H:%M:%S')}                      ║
║   • Idade: {csv_idade:.1f} horas                                    ║
║   • Status: {'✓ OK' if csv_idade <= 24 else '✗ ANTIGO'}                                      ║
║                                                              ║
║ Release de Resultados:                                       ║
║   • Data: {release_timestamp.strftime('%d/%m/%Y')}                              ║
║   • Idade: {release_idade} dias                                     ║
║   • Status: {'✓ OK' if release_idade <= 180 else '✗ ANTIGO'}                                      ║
║                                                              ║
║ Preços:                                                      ║
║   • Data: {preco_timestamp.strftime('%d/%m/%Y %H:%M:%S')}                      ║
║   • Idade: {preco_idade:.1f} horas                                    ║
║   • Status: {'✓ OK' if preco_idade <= 24 else '✗ ANTIGO'}                                      ║
╚══════════════════════════════════════════════════════════════╝
"""
    
    return relatorio
