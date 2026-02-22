"""
JSON Sanitizer - Remove NaN e Infinity de respostas JSON
"""
import math
from typing import Any, Dict, List


def sanitize_value(value: Any) -> Any:
    """
    Sanitiza um valor individual
    Converte NaN/Infinity para None ou 0
    """
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return 0
    return value


def sanitize_json(data: Any) -> Any:
    """
    Sanitiza recursivamente qualquer estrutura de dados
    Remove NaN e Infinity de dicts, lists, etc
    """
    if isinstance(data, dict):
        return {key: sanitize_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_json(item) for item in data]
    elif isinstance(data, tuple):
        return tuple(sanitize_json(item) for item in data)
    else:
        return sanitize_value(data)
