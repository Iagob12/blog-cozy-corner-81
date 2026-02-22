"""
Unified AI Client - Cliente unificado que usa OpenRouter (preferencial) ou Gemini (fallback)
"""
import os
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class UnifiedAIClient:
    """
    Cliente unificado que tenta:
    1. OpenRouter (gratuito, sem limites rígidos)
    2. Gemini (fallback se OpenRouter falhar)
    """
    
    def __init__(self):
        self.openrouter = None
        self.gemini = None
        
        # Tenta inicializar OpenRouter
        try:
            if os.getenv("OPENROUTER_API_KEY"):
                from app.services.openrouter_client import get_openrouter_client
                self.openrouter = get_openrouter_client()
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ OpenRouter disponível")
        except Exception as e:
            logger.warning(f"[{datetime.now()}] [UNIFIED] OpenRouter não disponível: {e}")
        
        # Tenta inicializar Gemini
        try:
            if os.getenv("GEMINI_API_KEY"):
                from app.services.gemini_client import get_gemini_client
                self.gemini = get_gemini_client()
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ Gemini disponível")
        except Exception as e:
            logger.warning(f"[{datetime.now()}] [UNIFIED] Gemini não disponível: {e}")
        
        if not self.openrouter and not self.gemini:
            raise ValueError("Nenhuma API de IA disponível! Configure OPENROUTER_API_KEY ou GEMINI_API_KEY")
        
        logger.info(f"[{datetime.now()}] [UNIFIED] Cliente unificado inicializado")
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True
    ) -> Dict[str, Any]:
        """
        Executa prompt tentando OpenRouter primeiro, depois Gemini
        """
        
        # Tenta OpenRouter primeiro (preferencial)
        if self.openrouter:
            try:
                logger.info(f"[{datetime.now()}] [UNIFIED] Tentando OpenRouter...")
                resultado = await self.openrouter.executar_prompt(
                    prompt, context, incluir_timestamp
                )
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ OpenRouter respondeu")
                return resultado
            
            except Exception as e:
                logger.warning(f"[{datetime.now()}] [UNIFIED] OpenRouter falhou: {e}")
        
        # Fallback para Gemini
        if self.gemini:
            try:
                logger.info(f"[{datetime.now()}] [UNIFIED] Tentando Gemini (fallback)...")
                resultado = await self.gemini.executar_prompt(
                    prompt, context, incluir_timestamp
                )
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ Gemini respondeu")
                return resultado
            
            except Exception as e:
                logger.error(f"[{datetime.now()}] [UNIFIED] Gemini também falhou: {e}")
                raise
        
        raise Exception("Todas as APIs de IA falharam")
    
    async def executar_prompt_raw(self, prompt: str) -> str:
        """
        Executa prompt RAW tentando OpenRouter primeiro, depois Gemini
        """
        
        # Tenta OpenRouter primeiro
        if self.openrouter:
            try:
                logger.info(f"[{datetime.now()}] [UNIFIED] Tentando OpenRouter RAW...")
                resultado = await self.openrouter.executar_prompt_raw(prompt)
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ OpenRouter respondeu")
                return resultado
            
            except Exception as e:
                logger.warning(f"[{datetime.now()}] [UNIFIED] OpenRouter falhou: {e}")
        
        # Fallback para Gemini
        if self.gemini:
            try:
                logger.info(f"[{datetime.now()}] [UNIFIED] Tentando Gemini RAW (fallback)...")
                resultado = await self.gemini.executar_prompt_raw(prompt)
                logger.info(f"[{datetime.now()}] [UNIFIED] ✓ Gemini respondeu")
                return resultado
            
            except Exception as e:
                logger.error(f"[{datetime.now()}] [UNIFIED] Gemini também falhou: {e}")
                raise
        
        raise Exception("Todas as APIs de IA falharam")
    
    async def testar_conexao(self) -> Dict[str, bool]:
        """Testa conexão com todas as APIs disponíveis"""
        
        resultados = {
            "openrouter": False,
            "gemini": False
        }
        
        if self.openrouter:
            try:
                resultados["openrouter"] = await self.openrouter.testar_conexao()
            except:
                pass
        
        if self.gemini:
            try:
                resultados["gemini"] = await self.gemini.testar_conexao()
            except:
                pass
        
        return resultados


# Singleton instance
_unified_client: Optional[UnifiedAIClient] = None


def get_unified_ai_client() -> UnifiedAIClient:
    """Retorna instância singleton do UnifiedAIClient"""
    global _unified_client
    
    if _unified_client is None:
        _unified_client = UnifiedAIClient()
    
    return _unified_client
