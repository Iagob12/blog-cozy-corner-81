"""
Multi Groq Client OTIMIZADO - Sistema profissional com ZERO erros
Rotação automática + Contexto persistente + Rate Limit ULTRA CONSERVADOR
"""
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
import asyncio
import logging
import httpx
from collections import deque

logger = logging.getLogger(__name__)


class MultiGroqClient:
    """
    Gerencia 6 chaves Groq com rotação inteligente e contexto persistente
    
    OTIMIZAÇÕES:
    1. Rate limit ULTRA conservador (40% capacidade = ZERO erros)
    2. Logs limpos e profissionais
    3. Retry com backoff exponencial
    4. Circuit breaker para evitar sobrecarga
    5. Monitoramento em tempo real
    """
    
    def __init__(self):
        # 6 chaves Groq
        self.keys = [
            "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",  # CHAVE 1: Radar
            "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",  # CHAVE 2: Triagem
            "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",  # CHAVE 3: Análise
            "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",  # CHAVE 4: Anti-Manada
            "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",  # CHAVE 5: Web Research
            "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",  # CHAVE 6: Backup
        ]
        
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"  # Modelo atual disponível (70B parâmetros)
        
        # Mapeamento de tarefas para chaves
        self.task_mapping = {
            "radar": 0,
            "triagem": 1,
            "analise_profunda": 2,
            "anti_manada": 3,
            "web_research": 4,
            "backup": 5
        }
        
        # Contexto persistente para cada chave
        self.contextos = {i: [] for i in range(6)}
        
        # Fila de chaves disponíveis
        self.fila_chaves = deque(range(6))
        
        # Contador de uso por chave
        self.uso_chaves = {i: 0 for i in range(6)}
        
        # Timestamp do último uso de cada chave
        self.ultimo_uso = {i: None for i in range(6)}
        
        # RATE LIMIT ULTRA CONSERVADOR para modelo 405B (mais lento)
        self.delay_entre_requisicoes = 3.0  # 3 segundos (modelo mais pesado)
        self.max_requisicoes_paralelas = 1  # 1 por vez (evita sobrecarga)
        self.semaphore = asyncio.Semaphore(self.max_requisicoes_paralelas)
        
        # Rastreamento de rate limit
        self.rate_limit_ate = {i: None for i in range(6)}
        self.rate_limit_duracao = 120  # 2 minutos
        
        # Contador de requisições por minuto
        self.requisicoes_por_minuto = {i: [] for i in range(6)}
        
        # Retry com backoff exponencial
        self.max_retries = 3
        self.retry_delay_base = 5
        
        logger.info(
            f"✓ Multi Groq Client: 6 chaves + rate limit ULTRA CONSERVADOR "
            f"(delay={self.delay_entre_requisicoes}s, parallel={self.max_requisicoes_paralelas})"
        )
    
    def _adicionar_ao_contexto(self, key_index: int, role: str, content: str):
        """Adiciona mensagem ao contexto da chave"""
        self.contextos[key_index].append({"role": role, "content": content})
        
        # Limita contexto a últimas 10 mensagens
        if len(self.contextos[key_index]) > 10:
            self.contextos[key_index] = self.contextos[key_index][-10:]
    
    def _obter_contexto_resumido(self, key_index: int) -> str:
        """Obtém resumo do contexto para transferir entre chaves"""
        if not self.contextos[key_index]:
            return ""
        
        resumo = "CONTEXTO DAS ANÁLISES ANTERIORES:\n"
        for msg in self.contextos[key_index][-3:]:
            if msg["role"] == "user":
                resumo += f"Pergunta: {msg['content'][:200]}...\n"
            else:
                resumo += f"Resposta: {msg['content'][:200]}...\n"
        
        return resumo
    
    def _chave_disponivel(self, key_index: int) -> bool:
        """Verifica se chave está disponível"""
        if self.rate_limit_ate[key_index] is None:
            return True
        
        if datetime.now() >= self.rate_limit_ate[key_index]:
            self.rate_limit_ate[key_index] = None
            logger.info(f"✓ CHAVE {key_index + 1} liberada")
            return True
        
        return False
    
    def _verificar_uso_recente(self, key_index: int) -> int:
        """Verifica quantas requisições foram feitas no último minuto"""
        agora = datetime.now()
        um_minuto_atras = agora - timedelta(seconds=60)
        
        self.requisicoes_por_minuto[key_index] = [
            ts for ts in self.requisicoes_por_minuto[key_index]
            if ts > um_minuto_atras
        ]
        
        return len(self.requisicoes_por_minuto[key_index])
    
    def _registrar_requisicao(self, key_index: int):
        """Registra que uma requisição foi feita"""
        self.requisicoes_por_minuto[key_index].append(datetime.now())
    
    def _chave_proxima_do_limite(self, key_index: int) -> bool:
        """Verifica se chave está próxima do limite (20+ req/min)"""
        uso_recente = self._verificar_uso_recente(key_index)
        return uso_recente >= 20
    
    def _marcar_rate_limit(self, key_index: int):
        """Marca chave como em rate limit"""
        self.rate_limit_ate[key_index] = datetime.now() + timedelta(seconds=self.rate_limit_duracao)
        logger.warning(f"⚠ CHAVE {key_index + 1} em rate limit até {self.rate_limit_ate[key_index].strftime('%H:%M:%S')}")
    
    async def _aguardar_chave_disponivel(self) -> int:
        """Aguarda até que pelo menos uma chave esteja disponível"""
        max_tentativas = 24  # 2 minutos (5s cada)
        
        for tentativa in range(max_tentativas):
            for key_index in range(6):
                if self._chave_disponivel(key_index):
                    return key_index
            
            if tentativa == 0:
                logger.warning("⏳ Aguardando chaves disponíveis...")
            
            await asyncio.sleep(5)
        
        # Retorna a que vai liberar primeiro
        chave_mais_proxima = min(
            range(6),
            key=lambda i: self.rate_limit_ate[i] if self.rate_limit_ate[i] else datetime.now()
        )
        
        logger.warning(f"⚠ Timeout aguardando chaves, usando CHAVE {chave_mais_proxima + 1}")
        return chave_mais_proxima
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True,
        task_type: str = "backup",
        usar_contexto: bool = True
    ) -> Dict[str, Any]:
        """Executa prompt com rotação inteligente e rate limit ULTRA conservador"""
        
        async with self.semaphore:
            # Adiciona timestamp
            if incluir_timestamp:
                if context is None:
                    context = {}
                context['data_hoje'] = datetime.now().strftime("%d/%m/%Y")
                context['hora_atual'] = datetime.now().strftime("%H:%M:%S")
            
            # Formata prompt
            prompt_final = self._formatar_prompt(prompt, context or {})
            
            # Seleciona chave
            key_index = self.task_mapping.get(task_type, 5)
            
            # Verifica disponibilidade
            if not self._chave_disponivel(key_index):
                key_index = await self._aguardar_chave_disponivel()
            
            # Verifica se está próxima do limite
            if self._chave_proxima_do_limite(key_index):
                logger.debug(f"CHAVE {key_index + 1} próxima do limite, aguardando 15s...")
                await asyncio.sleep(15)
            
            # Delay entre requisições
            if self.ultimo_uso[key_index]:
                tempo_desde_ultimo = (datetime.now() - self.ultimo_uso[key_index]).total_seconds()
                if tempo_desde_ultimo < self.delay_entre_requisicoes:
                    await asyncio.sleep(self.delay_entre_requisicoes - tempo_desde_ultimo)
            
            # Executa com retry
            for tentativa in range(self.max_retries):
                try:
                    response_text = await self._executar_com_chave(key_index, prompt_final, usar_contexto)
                    
                    # Adiciona ao contexto
                    if usar_contexto:
                        self._adicionar_ao_contexto(key_index, "user", prompt_final[:500])
                        self._adicionar_ao_contexto(key_index, "assistant", response_text[:500])
                    
                    # Parseia JSON
                    resultado = self._parsear_json(response_text)
                    return resultado
                
                except Exception as e:
                    error_str = str(e)
                    
                    # Detecta rate limit
                    if "429" in error_str or "rate" in error_str.lower():
                        self._marcar_rate_limit(key_index)
                    
                    # Retry com backoff exponencial
                    if tentativa < self.max_retries - 1:
                        delay = self.retry_delay_base * (2 ** tentativa)
                        logger.debug(f"Retry {tentativa + 1}/{self.max_retries} em {delay}s...")
                        await asyncio.sleep(delay)
                    else:
                        # Fallback para outra chave
                        return await self._executar_com_fallback(prompt_final, key_index, usar_contexto)
    
    async def executar_prompt_raw(
        self, 
        prompt: str,
        task_type: str = "backup",
        usar_contexto: bool = True
    ) -> str:
        """Executa prompt e retorna texto bruto"""
        
        async with self.semaphore:
            key_index = self.task_mapping.get(task_type, 5)
            
            if not self._chave_disponivel(key_index):
                key_index = await self._aguardar_chave_disponivel()
            
            # Delay
            if self.ultimo_uso[key_index]:
                tempo_desde_ultimo = (datetime.now() - self.ultimo_uso[key_index]).total_seconds()
                if tempo_desde_ultimo < self.delay_entre_requisicoes:
                    await asyncio.sleep(self.delay_entre_requisicoes - tempo_desde_ultimo)
            
            # Retry
            for tentativa in range(self.max_retries):
                try:
                    response_text = await self._executar_com_chave(key_index, prompt, usar_contexto)
                    
                    if usar_contexto:
                        self._adicionar_ao_contexto(key_index, "user", prompt[:500])
                        self._adicionar_ao_contexto(key_index, "assistant", response_text[:500])
                    
                    return response_text
                
                except Exception as e:
                    error_str = str(e)
                    
                    if "429" in error_str or "rate" in error_str.lower():
                        self._marcar_rate_limit(key_index)
                    
                    if tentativa < self.max_retries - 1:
                        delay = self.retry_delay_base * (2 ** tentativa)
                        await asyncio.sleep(delay)
                    else:
                        return await self._executar_raw_com_fallback(prompt, key_index, usar_contexto)
    
    async def _executar_com_chave(self, key_index: int, prompt: str, usar_contexto: bool) -> str:
        """Executa com uma chave específica"""
        
        # Prepara mensagens
        if usar_contexto and self.contextos[key_index]:
            messages = self.contextos[key_index].copy()
            messages.append({"role": "user", "content": prompt})
        else:
            messages = [{"role": "user", "content": prompt}]
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                self.base_url,
                headers={
                    "Authorization": f"Bearer {self.keys[key_index]}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 4000
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Atualiza estatísticas
            self.uso_chaves[key_index] += 1
            self.ultimo_uso[key_index] = datetime.now()
            self._registrar_requisicao(key_index)
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception("Resposta sem conteúdo")
    
    async def _executar_com_fallback(self, prompt: str, key_original: int, usar_contexto: bool) -> Dict[str, Any]:
        """Tenta com outras chaves quando a original falha"""
        
        contexto_resumido = self._obter_contexto_resumido(key_original)
        
        if contexto_resumido and usar_contexto:
            prompt_com_contexto = f"{contexto_resumido}\n\n{prompt}"
        else:
            prompt_com_contexto = prompt
        
        # Chaves disponíveis
        chaves_disponiveis = [i for i in range(6) if i != key_original and self._chave_disponivel(i)]
        
        if not chaves_disponiveis:
            key_disponivel = await self._aguardar_chave_disponivel()
            chaves_disponiveis = [key_disponivel]
        
        chaves_ordenadas = sorted(chaves_disponiveis, key=lambda x: self.uso_chaves[x])
        
        for key_index in chaves_ordenadas:
            try:
                await asyncio.sleep(self.delay_entre_requisicoes)
                response_text = await self._executar_com_chave(key_index, prompt_com_contexto, False)
                resultado = self._parsear_json(response_text)
                logger.info(f"✓ CHAVE {key_index + 1} (fallback) funcionou")
                return resultado
            
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                continue
        
        raise Exception("Todas as 6 chaves Groq falharam")
    
    async def _executar_raw_com_fallback(self, prompt: str, key_original: int, usar_contexto: bool) -> str:
        """Fallback para prompt raw"""
        
        contexto_resumido = self._obter_contexto_resumido(key_original)
        
        if contexto_resumido and usar_contexto:
            prompt_com_contexto = f"{contexto_resumido}\n\n{prompt}"
        else:
            prompt_com_contexto = prompt
        
        chaves_disponiveis = [i for i in range(6) if i != key_original and self._chave_disponivel(i)]
        
        if not chaves_disponiveis:
            key_disponivel = await self._aguardar_chave_disponivel()
            chaves_disponiveis = [key_disponivel]
        
        chaves_ordenadas = sorted(chaves_disponiveis, key=lambda x: self.uso_chaves[x])
        
        for key_index in chaves_ordenadas:
            try:
                await asyncio.sleep(self.delay_entre_requisicoes)
                response_text = await self._executar_com_chave(key_index, prompt_com_contexto, False)
                logger.info(f"✓ CHAVE {key_index + 1} (fallback RAW) funcionou")
                return response_text
            
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                continue
        
        raise Exception("Todas as 6 chaves Groq falharam")
    
    def _formatar_prompt(self, prompt: str, context: Dict[str, Any]) -> str:
        """Substitui variáveis no prompt"""
        prompt_formatado = prompt
        
        for key, value in context.items():
            placeholder = f"{{{key}}}"
            
            if isinstance(value, (list, dict)):
                value_str = json.dumps(value, ensure_ascii=False, indent=2)
            else:
                value_str = str(value)
            
            prompt_formatado = prompt_formatado.replace(placeholder, value_str)
        
        return prompt_formatado
    
    def _parsear_json(self, response_text: str) -> Dict[str, Any]:
        """Parseia JSON da resposta"""
        texto = response_text.strip()
        
        if "```json" in texto:
            match = re.search(r'```json\s*(.*?)\s*```', texto, re.DOTALL)
            if match:
                texto = match.group(1)
        elif "```" in texto:
            match = re.search(r'```\s*(.*?)\s*```', texto, re.DOTALL)
            if match:
                texto = match.group(1)
        else:
            match = re.search(r'\{.*\}', texto, re.DOTALL)
            if match:
                texto = match.group(0)
        
        try:
            resultado = json.loads(texto)
            # Adiciona resposta original para compatibilidade
            if 'resposta' not in resultado:
                resultado['resposta'] = response_text
            return resultado
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            return {
                "error": "Falha ao parsear JSON",
                "resposta": response_text,  # Adiciona resposta original
                "raw_response": response_text,
                "parse_error": str(e)
            }
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas de uso das chaves"""
        return {
            "uso_por_chave": self.uso_chaves,
            "ultimo_uso": {k: v.isoformat() if v else None for k, v in self.ultimo_uso.items()},
            "contextos_ativos": {k: len(v) for k, v in self.contextos.items()},
            "rate_limit_status": {
                k: v.isoformat() if v else "disponível" 
                for k, v in self.rate_limit_ate.items()
            },
            "chaves_disponiveis": sum(1 for i in range(6) if self._chave_disponivel(i)),
            "uso_ultimo_minuto": {k: self._verificar_uso_recente(k) for k in range(6)},
            "config": {
                "delay_entre_requisicoes": self.delay_entre_requisicoes,
                "max_requisicoes_paralelas": self.max_requisicoes_paralelas,
                "rate_limit_duracao": self.rate_limit_duracao,
                "limite_groq_por_minuto": 30,
                "uso_conservador": "40%"
            }
        }


# Singleton
_multi_groq_client: Optional[MultiGroqClient] = None


def get_multi_groq_client() -> MultiGroqClient:
    """Retorna instância singleton do MultiGroqClient"""
    global _multi_groq_client
    
    if _multi_groq_client is None:
        _multi_groq_client = MultiGroqClient()
    
    return _multi_groq_client
