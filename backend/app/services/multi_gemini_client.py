"""
Multi Gemini Client - Gerencia múltiplas chaves Gemini com especialização por tarefa
Cada chave é especializada em uma parte do fluxo para manter contexto correto
"""
import google.generativeai as genai
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)


class MultiGeminiClient:
    """
    Gerencia 6 chaves Gemini, cada uma especializada em uma tarefa:
    
    CHAVE 1: Prompt 1 - Radar de Oportunidades (Macro)
    CHAVE 2: Prompt 2 - Triagem Fundamentalista (Filtros)
    CHAVE 3: Prompt 3 - Análise Profunda (Releases + Dados)
    CHAVE 4: Prompt 6 - Anti-Manada (Validação)
    CHAVE 5: Web Research - Pesquisa Internet (Fallback)
    CHAVE 6: Backup Geral (Qualquer tarefa se outra falhar)
    """
    
    def __init__(self):
        # 6 chaves Gemini
        self.keys = [
            "AIzaSyCaRbjZF68oKkx4oNViPCUpumj8TG8csd4",  # CHAVE 1: Radar
            "AIzaSyDvoMOa5SSJXHK2BCP8AIq2Ki-IUdulmYI",  # CHAVE 2: Triagem
            "AIzaSyCt7m5eERleYZsKB9-3uPMhk1vNYi7cP2g",  # CHAVE 3: Análise Profunda
            "AIzaSyDNfZFJs7VHclKPDrvcYz-YxD7LejkdMe8",  # CHAVE 4: Anti-Manada
            "AIzaSyAzaSQMGKJz-6F3zv5RtSpYabKgVjmHzpw",  # CHAVE 5: Web Research
            "AIzaSyAvuxdXqCTVgtncI3h-vHQATbp1M9hKf7U",  # CHAVE 6: Backup
        ]
        
        # Inicializa modelos para cada chave
        self.models = []
        for i, key in enumerate(self.keys, 1):
            genai.configure(api_key=key)
            model = genai.GenerativeModel('gemini-2.5-flash')  # Mesmo modelo do gemini_client.py
            self.models.append(model)
            logger.info(f"[{datetime.now()}] [MULTI-GEMINI] Chave {i} inicializada")
        
        # Mapeamento de tarefas para chaves
        self.task_mapping = {
            "radar": 0,           # CHAVE 1
            "triagem": 1,         # CHAVE 2
            "analise_profunda": 2,  # CHAVE 3
            "anti_manada": 3,     # CHAVE 4
            "web_research": 4,    # CHAVE 5
            "backup": 5           # CHAVE 6
        }
        
        logger.info(f"[{datetime.now()}] [MULTI-GEMINI] Sistema com 6 chaves especializado inicializado")
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = False,  # Desabilitado por padrão
        task_type: str = "backup",
        usar_contexto: bool = False  # NOVO: controla se usa contexto
    ) -> Dict[str, Any]:
        """
        Executa prompt usando a chave especializada para a tarefa
        
        Args:
            prompt: Template do prompt
            context: Variáveis para substituir no prompt
            incluir_timestamp: Se deve adicionar data/hora
            task_type: Tipo de tarefa (radar, triagem, analise_profunda, anti_manada, web_research, backup)
            usar_contexto: Se deve usar context (padrão: False para consenso)
        
        Returns:
            Dict parseado da resposta JSON
        """
        
        # Adiciona timestamp ao context APENAS se usar_contexto=True
        if usar_contexto and incluir_timestamp:
            if context is None:
                context = {}
            context['data_hoje'] = datetime.now().strftime("%d/%m/%Y")
            context['hora_atual'] = datetime.now().strftime("%H:%M:%S")
        
        # Substitui variáveis no prompt APENAS se usar_contexto=True
        if usar_contexto and context:
            prompt_final = self._formatar_prompt(prompt, context)
        else:
            prompt_final = prompt
        
        # Seleciona chave especializada
        key_index = self.task_mapping.get(task_type, 5)  # Default: backup
        
        logger.info(
            f"[{datetime.now()}] [MULTI-GEMINI] Executando '{task_type}' "
            f"com CHAVE {key_index + 1} ({len(prompt_final)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt_final, key_index)
        
        # Parseia JSON
        resultado = self._parsear_json(response_text)
        
        logger.info(f"[{datetime.now()}] [MULTI-GEMINI] CHAVE {key_index + 1} respondeu com sucesso")
        
        return resultado
    
    async def executar_prompt_raw(
        self, 
        prompt: str,
        task_type: str = "backup"
    ) -> str:
        """
        Executa prompt e retorna texto bruto (sem parsing JSON)
        """
        
        # Seleciona chave especializada
        key_index = self.task_mapping.get(task_type, 5)
        
        logger.info(
            f"[{datetime.now()}] [MULTI-GEMINI] Executando RAW '{task_type}' "
            f"com CHAVE {key_index + 1} ({len(prompt)} chars)"
        )
        
        # Executa com retry
        response_text = await self._executar_com_retry(prompt, key_index)
        
        logger.info(f"[{datetime.now()}] [MULTI-GEMINI] CHAVE {key_index + 1} respondeu RAW ({len(response_text)} chars)")
        
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
        key_index: int,
        max_retries: int = 3,
        backoff_seconds: int = 2
    ) -> str:
        """Executa prompt com retry logic"""
        
        model = self.models[key_index]
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # Gemini API é síncrona, mas rodamos em executor para não bloquear
                loop = asyncio.get_event_loop()
                
                # Reconfigura API key antes de cada chamada
                genai.configure(api_key=self.keys[key_index])
                
                response = await loop.run_in_executor(
                    None,
                    lambda: model.generate_content(prompt)
                )
                
                return response.text
            
            except Exception as e:
                last_error = e
                logger.warning(
                    f"[{datetime.now()}] [MULTI-GEMINI] CHAVE {key_index + 1} "
                    f"Tentativa {attempt + 1}/{max_retries} falhou: {e}"
                )
                
                # Se falhou, tenta com chave backup
                if attempt == max_retries - 1 and key_index != 5:
                    logger.info(f"[{datetime.now()}] [MULTI-GEMINI] Tentando com CHAVE BACKUP (6)...")
                    try:
                        genai.configure(api_key=self.keys[5])
                        backup_model = self.models[5]
                        response = await loop.run_in_executor(
                            None,
                            lambda: backup_model.generate_content(prompt)
                        )
                        logger.info(f"[{datetime.now()}] [MULTI-GEMINI] ✓ CHAVE BACKUP respondeu")
                        return response.text
                    except Exception as backup_error:
                        logger.error(f"[{datetime.now()}] [MULTI-GEMINI] CHAVE BACKUP também falhou: {backup_error}")
                
                if attempt < max_retries - 1:
                    wait_time = backoff_seconds * (attempt + 1)
                    logger.info(f"[{datetime.now()}] [MULTI-GEMINI] Aguardando {wait_time}s antes de retry...")
                    await asyncio.sleep(wait_time)
        
        # Se todas as tentativas falharam
        logger.error(f"[{datetime.now()}] [MULTI-GEMINI] Todas as tentativas falharam")
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
            logger.error(f"[{datetime.now()}] [MULTI-GEMINI] Erro ao parsear JSON: {e}")
            logger.error(f"[{datetime.now()}] [MULTI-GEMINI] Texto recebido: {texto[:500]}...")
            
            # Fallback: retorna texto bruto
            return {
                "error": "Falha ao parsear JSON",
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    async def testar_conexao(self) -> Dict[str, bool]:
        """Testa conexão com todas as 6 chaves"""
        
        resultados = {}
        
        for i in range(6):
            try:
                logger.info(f"[{datetime.now()}] [MULTI-GEMINI] Testando CHAVE {i + 1}...")
                
                genai.configure(api_key=self.keys[i])
                model = self.models[i]
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: model.generate_content("Responda apenas: OK")
                )
                
                if "OK" in response.text.upper():
                    resultados[f"chave_{i + 1}"] = True
                    logger.info(f"[{datetime.now()}] [MULTI-GEMINI] ✓ CHAVE {i + 1} OK")
                else:
                    resultados[f"chave_{i + 1}"] = False
            
            except Exception as e:
                logger.error(f"[{datetime.now()}] [MULTI-GEMINI] ✗ CHAVE {i + 1} falhou: {e}")
                resultados[f"chave_{i + 1}"] = False
        
        return resultados


# Singleton instance
_multi_gemini_client: Optional[MultiGeminiClient] = None


def get_multi_gemini_client() -> MultiGeminiClient:
    """Retorna instância singleton do MultiGeminiClient"""
    global _multi_gemini_client
    
    if _multi_gemini_client is None:
        _multi_gemini_client = MultiGeminiClient()
    
    return _multi_gemini_client
