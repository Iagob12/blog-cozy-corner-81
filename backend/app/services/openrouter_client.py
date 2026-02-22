"""
OpenRouter Client - Interface para OpenRouter.ai
Suporta múltiplos modelos (gratuitos e pagos)
"""
import aiohttp
import os
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """
    Cliente para OpenRouter.ai
    
    MODELOS GRATUITOS RECOMENDADOS:
    - google/gemini-2.0-flash-exp:free (Melhor gratuito)
    - meta-llama/llama-3.2-3b-instruct:free
    - microsoft/phi-3-mini-128k-instruct:free
    - qwen/qwen-2-7b-instruct:free
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY não encontrada")
        
        self.base_url = "https://openrouter.ai/api/v1"
        
        # Modelo padrão (gratuito e muito bom)
        self.default_model = "google/gemini-2.0-flash-exp:free"
        
        logger.info(f"[{datetime.now()}] [OPENROUTER] Cliente inicializado (modelo: {self.default_model})")
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executa prompt no OpenRouter com retry logic
        
        Args:
            prompt: Template do prompt
            context: Variáveis para substituir no prompt
            incluir_timestamp: Se deve adicionar data/hora automaticamente
            model: Modelo específico (usa default se None)
        
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
        
        logger.info(f"[{datetime.now()}] [OPENROUTER] Executando prompt ({len(prompt_final)} chars)")
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt_final, model)
        
        # Parseia JSON
        resultado = self._parsear_json(response_text)
        
        logger.info(f"[{datetime.now()}] [OPENROUTER] Resposta recebida e parseada com sucesso")
        
        return resultado
    
    async def executar_prompt_raw(
        self, 
        prompt: str,
        model: Optional[str] = None
    ) -> str:
        """
        Executa prompt e retorna texto bruto (sem parsing JSON)
        Útil para pesquisas web e respostas em texto livre
        """
        
        logger.info(f"[{datetime.now()}] [OPENROUTER] Executando prompt RAW ({len(prompt)} chars)")
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt, model)
        
        logger.info(f"[{datetime.now()}] [OPENROUTER] Resposta RAW recebida ({len(response_text)} chars)")
        
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
        model: Optional[str] = None,
        max_retries: int = 3,
        backoff_seconds: int = 2
    ) -> str:
        """Executa prompt com retry logic"""
        
        model = model or self.default_model
        last_error = None
        
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://alpha-terminal.com",  # Opcional
                        "X-Title": "Alpha Terminal"  # Opcional
                    }
                    
                    payload = {
                        "model": model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    }
                    
                    async with session.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=aiohttp.ClientTimeout(total=60)
                    ) as response:
                        
                        if response.status == 200:
                            data = await response.json()
                            
                            # Extrai texto da resposta
                            if "choices" in data and len(data["choices"]) > 0:
                                content = data["choices"][0]["message"]["content"]
                                return content
                            else:
                                raise Exception("Resposta sem choices")
                        
                        else:
                            error_text = await response.text()
                            raise Exception(f"HTTP {response.status}: {error_text}")
            
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[{datetime.now()}] [OPENROUTER] Tentativa {attempt + 1}/{max_retries} falhou: {e}"
                )
                
                if attempt < max_retries - 1:
                    wait_time = backoff_seconds * (attempt + 1)
                    logger.info(f"[{datetime.now()}] [OPENROUTER] Aguardando {wait_time}s antes de retry...")
                    await asyncio.sleep(wait_time)
        
        # Se todas as tentativas falharam
        logger.error(f"[{datetime.now()}] [OPENROUTER] Todas as tentativas falharam")
        raise last_error
    
    def _parsear_json(self, response_text: str) -> Dict[str, Any]:
        """
        Parseia JSON da resposta
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
            logger.error(f"[{datetime.now()}] [OPENROUTER] Erro ao parsear JSON: {e}")
            logger.error(f"[{datetime.now()}] [OPENROUTER] Texto recebido: {texto[:500]}...")
            
            # Fallback: retorna texto bruto
            return {
                "error": "Falha ao parsear JSON",
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    async def testar_conexao(self) -> bool:
        """Testa conexão com OpenRouter"""
        
        try:
            logger.info(f"[{datetime.now()}] [OPENROUTER] Testando conexão...")
            
            prompt = "Responda apenas com JSON: {\"status\": \"ok\", \"mensagem\": \"OpenRouter funcionando\"}"
            resultado = await self.executar_prompt(prompt, incluir_timestamp=False)
            
            if resultado.get("status") == "ok":
                logger.info(f"[{datetime.now()}] [OPENROUTER] ✓ Conexão OK")
                return True
            else:
                logger.warning(f"[{datetime.now()}] [OPENROUTER] ⚠ Resposta inesperada: {resultado}")
                return False
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] [OPENROUTER] ✗ Erro na conexão: {e}")
            return False
    
    async def listar_modelos_disponiveis(self) -> list:
        """Lista modelos disponíveis no OpenRouter"""
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}"
                }
                
                async with session.get(
                    f"{self.base_url}/models",
                    headers=headers
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        return []
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] [OPENROUTER] Erro ao listar modelos: {e}")
            return []


# Singleton instance
_openrouter_client: Optional[OpenRouterClient] = None


def get_openrouter_client() -> OpenRouterClient:
    """Retorna instância singleton do OpenRouterClient"""
    global _openrouter_client
    
    if _openrouter_client is None:
        _openrouter_client = OpenRouterClient()
    
    return _openrouter_client
