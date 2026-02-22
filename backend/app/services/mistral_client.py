"""
Mistral AI Client - Cliente para usar Mistral AI
Modelo: mistral-small-latest (funcionando!)
"""
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging
import httpx

logger = logging.getLogger(__name__)


class MistralClient:
    """
    Cliente para usar Mistral AI
    
    Vantagens:
    - Funcionando agora (testado!)
    - Boa qualidade para análise
    - Formato OpenAI compatível
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mistral.ai/v1/chat/completions"
        self.model = "mistral-small-latest"
        
        logger.info(f"[{datetime.now()}] [MISTRAL] Cliente inicializado com Mistral Small")
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True,
        task_type: str = "backup"
    ) -> Dict[str, Any]:
        """
        Executa prompt usando Mistral AI
        
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
            f"[{datetime.now()}] [MISTRAL] Executando '{task_type}' "
            f"({len(prompt_final)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt_final)
        
        # Parseia JSON
        resultado = self._parsear_json(response_text)
        
        logger.info(f"[{datetime.now()}] [MISTRAL] Resposta recebida com sucesso")
        
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
            f"[{datetime.now()}] [MISTRAL] Executando RAW '{task_type}' "
            f"({len(prompt)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt)
        
        logger.info(f"[{datetime.now()}] [MISTRAL] Resposta RAW recebida ({len(response_text)} chars)")
        
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
                    f"[{datetime.now()}] [MISTRAL] "
                    f"Tentativa {attempt + 1}/{max_retries} falhou: {e}"
                )
                
                if attempt < max_retries - 1:
                    wait_time = backoff_seconds * (attempt + 1)
                    logger.info(f"[{datetime.now()}] [MISTRAL] Aguardando {wait_time}s antes de retry...")
                    await asyncio.sleep(wait_time)
        
        # Se todas as tentativas falharam
        logger.error(f"[{datetime.now()}] [MISTRAL] Todas as tentativas falharam")
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
            logger.error(f"[{datetime.now()}] [MISTRAL] Erro ao parsear JSON: {e}")
            logger.error(f"[{datetime.now()}] [MISTRAL] Texto recebido: {texto[:500]}...")
            
            # Fallback: retorna texto bruto
            return {
                "error": "Falha ao parsear JSON",
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    async def testar_conexao(self) -> bool:
        """Testa conexão com Mistral AI"""
        
        try:
            logger.info(f"[{datetime.now()}] [MISTRAL] Testando conexão...")
            
            response = await self._executar_com_retry("Responda apenas: OK")
            
            if "OK" in response.upper():
                logger.info(f"[{datetime.now()}] [MISTRAL] ✓ Conexão OK")
                return True
            else:
                return False
        
        except Exception as e:
            logger.error(f"[{datetime.now()}] [MISTRAL] ✗ Teste falhou: {e}")
            return False


# Singleton instance
_mistral_client: Optional[MistralClient] = None


def get_mistral_client(api_key: str = None) -> MistralClient:
    """Retorna instância singleton do MistralClient"""
    global _mistral_client
    
    if _mistral_client is None:
        if api_key is None:
            import os
            api_key = os.getenv("MISTRAL_API_KEY")
        
        if not api_key:
            raise ValueError("MISTRAL_API_KEY não configurada")
        
        _mistral_client = MistralClient(api_key)
    
    return _mistral_client
