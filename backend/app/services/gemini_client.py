"""
Gemini Client - Interface unificada para comunicação com Gemini AI
Inclui timestamp automático, retry logic e parsing robusto de JSON
"""
import google.generativeai as genai
import os
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    """Cliente unificado para Gemini AI com retry e timestamp automático"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada")
        
        genai.configure(api_key=self.api_key)
        # Usa gemini-2.5-flash (modelo mais recente disponível)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        logger.info(f"[{datetime.now()}] [GEMINI] Cliente inicializado (modelo: gemini-2.5-flash)")
    
    async def executar_prompt_raw(self, prompt: str) -> str:
        """
        Executa prompt e retorna texto bruto (sem parsing JSON)
        Útil para pesquisas web e respostas em texto livre
        """
        
        logger.info(f"[{datetime.now()}] [GEMINI] Executando prompt RAW ({len(prompt)} chars)")
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt)
        
        logger.info(f"[{datetime.now()}] [GEMINI] Resposta RAW recebida ({len(response_text)} chars)")
        
        return response_text
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True
    ) -> Dict[str, Any]:
        """
        Executa prompt no Gemini com retry logic
        
        Args:
            prompt: Template do prompt
            context: Variáveis para substituir no prompt
            incluir_timestamp: Se deve adicionar data/hora automaticamente
        
        Returns:
            Dict parseado da resposta JSON
        """
        
        # Adiciona timestamp ao context
        if incluir_timestamp:
            if context is None:
                context = {}
            context['data_hoje'] = datetime.now().strftime("%d/%m/%Y")
            context['hora_atual'] = datetime.now().strftime("%H:%M:%S")
        
        # Substitui variáveis no prompt
        prompt_final = self._formatar_prompt(prompt, context or {})
        
        logger.info(f"[{datetime.now()}] [GEMINI] Executando prompt ({len(prompt_final)} chars)")
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt_final)
        
        # Parseia JSON
        resultado = self._parsear_json(response_text)
        
        logger.info(f"[{datetime.now()}] [GEMINI] Resposta recebida e parseada com sucesso")
        
        return resultado
    
    def _formatar_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        """Substitui variáveis no prompt"""
        
        prompt_formatado = prompt
        
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            
            # Converte valor para string se necessário
            if isinstance(value, (list, dict)):
                value_str = json.dumps(value, ensure_ascii=False, indent=2)
            else:
                value_str = str(value)
            
            prompt_formatado = prompt_formatado.replace(placeholder, value_str)
        
        return prompt_formatado
    
    async def _executar_com_retry(
        self, 
        prompt: str, 
        max_retries: int = 3,
        backoff_seconds: int = 2
    ) -> str:
        """Executa prompt com retry logic"""
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Gemini API é síncrona, mas rodamos em executor para não bloquear
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: self.model.generate_content(prompt)
                )
                
                return response.text
            
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[{datetime.now()}] [GEMINI] Tentativa {attempt + 1}/{max_retries} falhou: {e}"
                )
                
                if attempt < max_retries - 1:
                    wait_time = backoff_seconds * (attempt + 1)
                    logger.info(f"[{datetime.now()}] [GEMINI] Aguardando {wait_time}s antes de retry...")
                    await asyncio.sleep(wait_time)
        
        # Se todas as tentativas falharam
        logger.error(f"[{datetime.now()}] [GEMINI] Todas as tentativas falharam")
        raise last_error
    
    def _parsear_json(self, response_text: str) -> Dict[str, Any]:
        """
        Parseia JSON da resposta do Gemini
        Trata múltiplos formatos possíveis
        """
        
        # Remove markdown code blocks se existirem
        texto = response_text.strip()
        
        # Padrão 1: ```json ... ```
        if "```json" in texto:
            match = re.search(r'```json\s*(.*?)\s*```', texto, re.DOTALL)
            if match:
                texto = match.group(1)
        
        # Padrão 2: ``` ... ```
        elif "```" in texto:
            match = re.search(r'```\s*(.*?)\s*```', texto, re.DOTALL)
            if match:
                texto = match.group(1)
        
        # Padrão 3: Procura por { ... } no texto
        else:
            match = re.search(r'\{.*\}', texto, re.DOTALL)
            if match:
                texto = match.group(0)
        
        # Tenta parsear
        try:
            resultado = json.loads(texto)
            return resultado
        
        except json.JSONDecodeError as e:
            logger.error(f"[{datetime.now()}] [GEMINI] Erro ao parsear JSON: {e}")
            logger.error(f"[{datetime.now()}] [GEMINI] Texto recebido: {texto[:500]}...")
            
            # Fallback: retorna texto bruto
            return {
                "error": "Falha ao parsear JSON",
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    async def testar_conexao(self) -> bool:
        """Testa conexão com Gemini"""
        
        try:
            logger.info(f"[{datetime.now()}] [GEMINI] Testando conexão...")
            
            prompt = "Responda apenas com JSON: {\"status\": \"ok\", \"mensagem\": \"Gemini funcionando\"}"
            resultado = await self.executar_prompt(prompt, incluir_timestamp=False)
            
            if resultado.get("status") == "ok":
                logger.info(f"[{datetime.now()}] [GEMINI] ✓ Conexão OK")
                return True
            else:
                logger.warning(f"[{datetime.now()}] [GEMINI] ⚠ Resposta inesperada: {resultado}")
                return False
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] [GEMINI] ✗ Erro na conexão: {e}")
            return False


# Singleton instance
_gemini_client: Optional[GeminiClient] = None


def get_gemini_client() -> GeminiClient:
    """Retorna instância singleton do GeminiClient"""
    global _gemini_client
    
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    
    return _gemini_client
