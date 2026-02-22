"""
Sistema de Análise Automática e Incremental

Módulo completo para análise inteligente de empresas com:
- Análise incremental (apenas empresas novas)
- Cache inteligente
- Validação rigorosa de resultados
- Auto-refresh automático
- Tratamento robusto de erros
"""

from .analise_service import AnaliseAutomaticaService, get_analise_automatica_service
from .cache_manager import CacheManager
from .validador import ValidadorResultados
from .scheduler import SchedulerAnalise, get_scheduler

__all__ = [
    'AnaliseAutomaticaService',
    'CacheManager',
    'ValidadorResultados',
    'SchedulerAnalise',
    'get_analise_automatica_service',
    'get_scheduler'
]
