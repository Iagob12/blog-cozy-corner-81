"""
CometAPI Gemini Client - Usa Gemini 3 Pro via CometAPI
606 modelos disponíveis incluindo Gemini 3 Pro All
"""
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)


class CometGeminiClient:
    """
    Cliente para usar Gemini 3 Pro All via CometAPI
    
    Vantagens:
    - 606 modelos disponíveis
    - Gemini 3 Pro All (modelo mais completo)
    - Suporta OpenAI API format
    - Preços competitivos
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cometapi.com/v1/chat/completions"
        self.model = "gemini-3-pro-all"  # Gemini 3 Pro All!
        
        logger.info(f"[{datetime.now()}] [COMETAPI] Cliente inicializado com Gemini 3 Pro All")
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True,
        task_type: str = "backup"
    ) -> Dict[str, Any]:
        """
        Executa prompt usando CometAPI
        
        Args:
            prompt: Template do prompt
            context: Variáveis para substituir no prompt
            incluir_timestamp: Se deve adicionar data/hora
            task_type: Tipo de tarefa (para logging)
        
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
        
        logger.info(
            f"[{datetime.now()}] [COMETAPI] Executando '{task_type}' "
            f"({len(prompt_final)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt_final)
        
        # Parseia JSON
        resultado = self._parsear_json(response_text)
        
        logger.info(f"[{datetime.now()}] [COMETAPI] Resposta recebida com sucesso")
        
        return resultado
    
    async def executar_prompt_raw(
        self, 
        prompt: str,
        task_type: str = "backup"
    ) -> str:
        """
        Executa prompt e retorna texto bruto (sem parsing JSON)
        """
        
        logger.info(
            f"[{datetime.now()}] [COMETAPI] Executando RAW '{task_type}' "
            f"({len(prompt)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt)
        
        logger.info(f"[{datetime.now()}] [COMETAPI] Resposta RAW recebida ({len(response_text)} chars)")
        
        return response_text
    
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
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        self.base_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ]
                        }
                    )
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    # Extrai texto da resposta
                    if "choices" in data and len(data["choices"]) > 0:
                        return data["choices"][0]["message"]["content"]
                    else:
                        raise Exception("Resposta sem conteúdo")
            
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[{datetime.now()}] [COMETAPI] "
                    f"Tentativa {attempt + 1}/{max_retries} falhou: {e}"
                )
                
                if attempt < max_retries - 1:
                    wait_time = backoff_seconds * (attempt + 1)
                    logger.info(f"[{datetime.now()}] [COMETAPI] Aguardando {wait_time}s antes de retry...")
                    await asyncio.sleep(wait_time)
        
        # Se todas as tentativas falharam
        logger.error(f"[{datetime.now()}] [COMETAPI] Todas as tentativas falharam")
        raise last_error
    
    def _parsear_json(self, response_text: str) -> Dict[str, Any]:
        """Parseia JSON da resposta"""
        
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
            logger.error(f"[{datetime.now()}] [COMETAPI] Erro ao parsear JSON: {e}")
            logger.error(f"[{datetime.now()}] [COMETAPI] Texto recebido: {texto[:500]}...")
            
            # Fallback: retorna texto bruto
            return {
                "error": "Falha ao parsear JSON",
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    async def testar_conexao(self) -> bool:
        """Testa conexão com CometAPI"""
        
        try:
            logger.info(f"[{datetime.now()}] [COMETAPI] Testando conexão...")
            
            response = await self._executar_com_retry("Responda apenas: OK")
            
            if "OK" in response.upper():
                logger.info(f"[{datetime.now()}] [COMETAPI] ✓ Conexão OK")
                return True
            else:
                return False
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] [COMETAPI] ✗ Teste falhou: {e}")
            return False


# Singleton instance
_comet_client: Optional[CometGeminiClient] = None


def get_comet_gemini_client(api_key: str = None) -> CometGeminiClient:
    """Retorna instância singleton do CometGeminiClient"""
    global _comet_client
    
    if _comet_client is None:
        if api_key is None:
            import os
            api_key = os.getenv("COMETAPI_KEY")
        
        if not api_key:
            raise ValueError("COMETAPI_KEY não configurada")
        
        _comet_client = CometGeminiClient(api_key)
    
    return _comet_client
