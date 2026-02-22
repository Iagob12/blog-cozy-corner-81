"""
Multi Groq Client - Sistema inteligente com 6 chaves Groq
Rotação automática + Contexto persistente + Especialização por tarefa
+ CONTROLE DE RATE LIMIT (delay entre requisições + limite de paralelismo)
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
    
    FEATURES:
    1. Rotação automática quando uma chave atinge rate limit
    2. Contexto persistente: cada chave "lembra" das conversas anteriores
    3. Especialização: cada chave focada em uma tarefa
    4. Fallback inteligente: se uma falha, tenta outra com contexto
    5. CONTROLE DE RATE LIMIT: delay entre requisições + limite de paralelismo
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
        self.model = "llama-3.3-70b-versatile"
        
        # Mapeamento de tarefas para chaves
        self.task_mapping = {
            "radar": 0,
            "triagem": 1,
            "analise_profunda": 2,
            "anti_manada": 3,
            "web_research": 4,
            "backup": 5
        }
        
        # Contexto persistente para cada chave (histórico de conversas)
        self.contextos = {i: [] for i in range(6)}
        
        # Fila de chaves disponíveis (para rotação)
        self.fila_chaves = deque(range(6))
        
        # Contador de uso por chave
        self.uso_chaves = {i: 0 for i in range(6)}
        
        # Timestamp do último uso de cada chave
        self.ultimo_uso = {i: None for i in range(6)}
        
        # CONTROLE DE RATE LIMIT - ULTRA CONSERVADOR (ZERO ERROS)
        # Groq: 30 req/min por chave = 180 req/min total (6 chaves)
        # Para ZERO falhas: usar apenas 40% da capacidade = 72 req/min
        # Delay: 60s / 72 = 0.83s → arredondado para 2s (ULTRA seguro)
        self.delay_entre_requisicoes = 2.0  # 2 segundos entre requisições (ULTRA CONSERVADOR)
        self.max_requisicoes_paralelas = 2  # Máximo 2 simultâneas (reduzido de 3)
        self.semaphore = asyncio.Semaphore(self.max_requisicoes_paralelas)
        
        # Rastreamento de rate limit por chave
        self.rate_limit_ate = {i: None for i in range(6)}  # Timestamp até quando está em rate limit
        self.rate_limit_duracao = 120  # Aguarda 120 segundos após rate limit (aumentado de 90s)
        
        # Contador de requisições por minuto (para monitoramento)
        self.requisicoes_por_minuto = {i: [] for i in range(6)}  # Lista de timestamps
        
        # Retry com backoff exponencial
        self.max_retries = 3
        self.retry_delay_base = 5  # 5 segundos base
        
        logger.info(
            f"✓ Multi Groq Client: 6 chaves + contexto + rate limit ULTRA CONSERVADOR "
            f"(delay={self.delay_entre_requisicoes}s, max_parallel={self.max_requisicoes_paralelas}, "
            f"capacidade=40% para ZERO erros)"
        )
    
    def _adicionar_ao_contexto(self, key_index: int, role: str, content: str):
        """Adiciona mensagem ao contexto da chave"""
        self.contextos[key_index].append({
            "role": role,
            "content": content
        })
        
        # Limita contexto a últimas 10 mensagens (para não estourar tokens)
        if len(self.contextos[key_index]) > 10:
            self.contextos[key_index] = self.contextos[key_index][-10:]
    
    def _obter_contexto_resumido(self, key_index: int) -> str:
        """Obtém resumo do contexto para transferir entre chaves"""
        if not self.contextos[key_index]:
            return ""
        
        resumo = "CONTEXTO DAS ANÁLISES ANTERIORES:\n"
        for msg in self.contextos[key_index][-3:]:  # Últimas 3 mensagens
            if msg["role"] == "user":
                resumo += f"Pergunta: {msg['content'][:200]}...\n"
            else:
                resumo += f"Resposta: {msg['content'][:200]}...\n"
        
        return resumo
    
    def _chave_disponivel(self, key_index: int) -> bool:
        """Verifica se chave está disponível (não em rate limit)"""
        if self.rate_limit_ate[key_index] is None:
            return True
        
        # Verifica se já passou o tempo de rate limit
        if datetime.now() >= self.rate_limit_ate[key_index]:
            self.rate_limit_ate[key_index] = None
            logger.info(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} liberada do rate limit")
            return True
        
        return False
    
    def _verificar_uso_recente(self, key_index: int) -> int:
        """
        Verifica quantas requisições foram feitas no último minuto
        
        Returns:
            Número de requisições no último minuto
        """
        agora = datetime.now()
        um_minuto_atras = agora - timedelta(seconds=60)
        
        # Remove requisições antigas (mais de 1 minuto)
        self.requisicoes_por_minuto[key_index] = [
            ts for ts in self.requisicoes_por_minuto[key_index]
            if ts > um_minuto_atras
        ]
        
        return len(self.requisicoes_por_minuto[key_index])
    
    def _registrar_requisicao(self, key_index: int):
        """Registra que uma requisição foi feita"""
        self.requisicoes_por_minuto[key_index].append(datetime.now())
    
    def _chave_proxima_do_limite(self, key_index: int) -> bool:
        """
        Verifica se chave está próxima do limite (20+ requisições no último minuto)
        
        Groq: 30 req/min
        Alerta: 20 req/min (67% da capacidade) - MAIS CONSERVADOR
        """
        uso_recente = self._verificar_uso_recente(key_index)
        return uso_recente >= 20  # Reduzido de 25 para 20
    
    def _marcar_rate_limit(self, key_index: int):
        """Marca chave como em rate limit"""
        self.rate_limit_ate[key_index] = datetime.now() + timedelta(seconds=self.rate_limit_duracao)
        logger.warning(
            f"⚠ CHAVE {key_index + 1} em rate limit até {self.rate_limit_ate[key_index].strftime('%H:%M:%S')}"
        )
    
    async def _aguardar_chave_disponivel(self) -> int:
        """Aguarda até que pelo menos uma chave esteja disponível"""
        max_tentativas = 12  # 12 tentativas = 1 minuto (5s cada)
        
        for tentativa in range(max_tentativas):
            # Verifica se alguma chave está disponível
            for key_index in range(6):
                if self._chave_disponivel(key_index):
                    return key_index
            
            # Nenhuma chave disponível, aguarda 5 segundos
            tempo_espera = 5
            logger.warning(
                f"[{datetime.now()}] [MULTI-GROQ] Todas as chaves em rate limit. "
                f"Aguardando {tempo_espera}s... (tentativa {tentativa + 1}/{max_tentativas})"
            )
            await asyncio.sleep(tempo_espera)
        
        # Se chegou aqui, todas as chaves ainda estão em rate limit
        # Retorna a que vai liberar primeiro
        chave_mais_proxima = min(
            range(6),
            key=lambda i: self.rate_limit_ate[i] if self.rate_limit_ate[i] else datetime.now()
        )
        
        logger.warning(
            f"[{datetime.now()}] [MULTI-GROQ] Timeout aguardando chaves. "
            f"Usando CHAVE {chave_mais_proxima + 1} (pode falhar)"
        )
        
        return chave_mais_proxima
    
    async def executar_prompt(
        self, 
        prompt: str, 
        context: Optional[Dict[str, Any]] = None,
        incluir_timestamp: bool = True,
        task_type: str = "backup",
        usar_contexto: bool = True
    ) -> Dict[str, Any]:
        """
        Executa prompt com rotação inteligente e contexto persistente
        + CONTROLE DE RATE LIMIT (delay + semáforo)
        
        Args:
            prompt: Template do prompt
            context: Variáveis para substituir no prompt
            incluir_timestamp: Se deve adicionar data/hora
            task_type: Tipo de tarefa (radar, triagem, etc)
            usar_contexto: Se deve usar contexto persistente
        
        Returns:
            Dict parseado da resposta JSON
        """
        
        # CONTROLE DE PARALELISMO: aguarda semáforo
        async with self.semaphore:
            # Adiciona timestamp ao context
            if incluir_timestamp:
                if context is None:
                    context = {}
                context['data_hoje'] = datetime.now().strftime("%d/%m/%Y")
                context['hora_atual'] = datetime.now().strftime("%H:%M:%S")
            
            # Substitui variáveis no prompt
            prompt_final = self._formatar_prompt(prompt, context or {})
            
            # Seleciona chave especializada
            key_index = self.task_mapping.get(task_type, 5)
            
            # Verifica se chave está disponível, senão aguarda
            if not self._chave_disponivel(key_index):
                logger.warning(
                    f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} em rate limit, "
                    f"aguardando chave disponível..."
                )
                key_index = await self._aguardar_chave_disponivel()
            
            # NOVO: Verifica se está próxima do limite
            if self._chave_proxima_do_limite(key_index):
                logger.warning(
                    f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} próxima do limite "
                    f"({self._verificar_uso_recente(key_index)}/30 req/min), "
                    f"aguardando 10s para segurança..."
                )
                await asyncio.sleep(10)  # Aguarda 10s para dar tempo de resetar
            
            logger.info(
                f"[{datetime.now()}] [MULTI-GROQ] Executando '{task_type}' "
                f"com CHAVE {key_index + 1} ({len(prompt_final)} chars) "
                f"[uso: {self._verificar_uso_recente(key_index)}/30 req/min]"
            )
            
            # DELAY ENTRE REQUISIÇÕES
            if self.ultimo_uso[key_index]:
                tempo_desde_ultimo = (datetime.now() - self.ultimo_uso[key_index]).total_seconds()
                if tempo_desde_ultimo < self.delay_entre_requisicoes:
                    delay = self.delay_entre_requisicoes - tempo_desde_ultimo
                    logger.debug(f"[{datetime.now()}] [MULTI-GROQ] Aguardando {delay:.2f}s (rate limit control)")
                    await asyncio.sleep(delay)
            
            # Tenta executar com a chave especializada
            try:
                response_text = await self._executar_com_chave(
                    key_index, prompt_final, usar_contexto
                )
                
                # Adiciona ao contexto
                if usar_contexto:
                    self._adicionar_ao_contexto(key_index, "user", prompt_final[:500])
                    self._adicionar_ao_contexto(key_index, "assistant", response_text[:500])
                
                # Parseia JSON
                resultado = self._parsear_json(response_text)
                
                logger.info(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} respondeu com sucesso")
                
                return resultado
            
            except Exception as e:
                error_str = str(e)
                
                # Detecta rate limit (429)
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                    logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} atingiu rate limit: {e}")
                else:
                    logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} falhou: {e}")
                
                # FALLBACK: Tenta com outra chave + transfere contexto
                return await self._executar_com_fallback(
                    prompt_final, key_index, usar_contexto
                )
    
    async def executar_prompt_raw(
        self, 
        prompt: str,
        task_type: str = "backup",
        usar_contexto: bool = True
    ) -> str:
        """
        Executa prompt e retorna texto bruto (sem parsing JSON)
        + CONTROLE DE RATE LIMIT
        """
        
        # CONTROLE DE PARALELISMO
        async with self.semaphore:
            key_index = self.task_mapping.get(task_type, 5)
            
            # Verifica disponibilidade
            if not self._chave_disponivel(key_index):
                logger.warning(
                    f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} em rate limit (RAW), "
                    f"aguardando..."
                )
                key_index = await self._aguardar_chave_disponivel()
            
            logger.info(
                f"[{datetime.now()}] [MULTI-GROQ] Executando RAW '{task_type}' "
                f"com CHAVE {key_index + 1}"
            )
            
            # DELAY
            if self.ultimo_uso[key_index]:
                tempo_desde_ultimo = (datetime.now() - self.ultimo_uso[key_index]).total_seconds()
                if tempo_desde_ultimo < self.delay_entre_requisicoes:
                    delay = self.delay_entre_requisicoes - tempo_desde_ultimo
                    await asyncio.sleep(delay)
            
            try:
                response_text = await self._executar_com_chave(
                    key_index, prompt, usar_contexto
                )
                
                if usar_contexto:
                    self._adicionar_ao_contexto(key_index, "user", prompt[:500])
                    self._adicionar_ao_contexto(key_index, "assistant", response_text[:500])
                
                return response_text
            
            except Exception as e:
                error_str = str(e)
                
                # Detecta rate limit
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                    logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} atingiu rate limit (RAW): {e}")
                else:
                    logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} falhou (RAW): {e}")
                
                # FALLBACK
                return await self._executar_raw_com_fallback(
                    prompt, key_index, usar_contexto
                )
    
    async def _executar_com_chave(
        self,
        key_index: int,
        prompt: str,
        usar_contexto: bool
    ) -> str:
        """Executa com uma chave específica"""
        
        # Prepara mensagens (com ou sem contexto)
        if usar_contexto and self.contextos[key_index]:
            # Usa contexto + nova mensagem
            messages = self.contextos[key_index].copy()
            messages.append({"role": "user", "content": prompt})
        else:
            # Apenas nova mensagem
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
            
            # NOVO: Registra requisição para monitoramento
            self._registrar_requisicao(key_index)
            
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            else:
                raise Exception("Resposta sem conteúdo")
    
    async def _executar_com_fallback(
        self,
        prompt: str,
        key_original: int,
        usar_contexto: bool
    ) -> Dict[str, Any]:
        """Tenta com outras chaves quando a original falha"""
        
        # Obtém contexto da chave original
        contexto_resumido = self._obter_contexto_resumido(key_original)
        
        # Adiciona contexto ao prompt se existir
        if contexto_resumido and usar_contexto:
            prompt_com_contexto = f"{contexto_resumido}\n\n{prompt}"
        else:
            prompt_com_contexto = prompt
        
        # Tenta com outras chaves DISPONÍVEIS (em ordem de menos uso)
        chaves_disponiveis = [
            i for i in range(6) 
            if i != key_original and self._chave_disponivel(i)
        ]
        
        # Se não há chaves disponíveis, aguarda
        if not chaves_disponiveis:
            logger.warning(
                f"[{datetime.now()}] [MULTI-GROQ] Nenhuma chave disponível para fallback, aguardando..."
            )
            key_disponivel = await self._aguardar_chave_disponivel()
            chaves_disponiveis = [key_disponivel]
        
        # Ordena por menos uso
        chaves_ordenadas = sorted(chaves_disponiveis, key=lambda x: self.uso_chaves[x])
        
        for key_index in chaves_ordenadas:
            try:
                logger.info(f"[{datetime.now()}] [MULTI-GROQ] Tentando CHAVE {key_index + 1} (fallback)")
                
                # DELAY antes de fallback
                await asyncio.sleep(self.delay_entre_requisicoes)
                
                response_text = await self._executar_com_chave(
                    key_index, prompt_com_contexto, False  # Não usa contexto no fallback
                )
                
                resultado = self._parsear_json(response_text)
                
                logger.info(f"[{datetime.now()}] [MULTI-GROQ] ✓ CHAVE {key_index + 1} (fallback) funcionou!")
                
                return resultado
            
            except Exception as e:
                error_str = str(e)
                
                # Marca rate limit se necessário
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                
                logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} (fallback) falhou: {e}")
                continue
        
        # Se todas falharam
        raise Exception("Todas as 6 chaves Groq falharam")
    
    async def _executar_raw_com_fallback(
        self,
        prompt: str,
        key_original: int,
        usar_contexto: bool
    ) -> str:
        """Fallback para prompt raw"""
        
        contexto_resumido = self._obter_contexto_resumido(key_original)
        
        if contexto_resumido and usar_contexto:
            prompt_com_contexto = f"{contexto_resumido}\n\n{prompt}"
        else:
            prompt_com_contexto = prompt
        
        # Chaves disponíveis
        chaves_disponiveis = [
            i for i in range(6) 
            if i != key_original and self._chave_disponivel(i)
        ]
        
        if not chaves_disponiveis:
            logger.warning(
                f"[{datetime.now()}] [MULTI-GROQ] Nenhuma chave disponível para fallback RAW, aguardando..."
            )
            key_disponivel = await self._aguardar_chave_disponivel()
            chaves_disponiveis = [key_disponivel]
        
        chaves_ordenadas = sorted(chaves_disponiveis, key=lambda x: self.uso_chaves[x])
        
        for key_index in chaves_ordenadas:
            try:
                logger.info(f"[{datetime.now()}] [MULTI-GROQ] Tentando CHAVE {key_index + 1} (fallback RAW)")
                
                # DELAY
                await asyncio.sleep(self.delay_entre_requisicoes)
                
                response_text = await self._executar_com_chave(
                    key_index, prompt_com_contexto, False
                )
                
                logger.info(f"[{datetime.now()}] [MULTI-GROQ] ✓ CHAVE {key_index + 1} (fallback RAW) funcionou!")
                
                return response_text
            
            except Exception as e:
                error_str = str(e)
                
                if "429" in error_str or "rate" in error_str.lower():
                    self._marcar_rate_limit(key_index)
                
                logger.warning(f"[{datetime.now()}] [MULTI-GROQ] CHAVE {key_index + 1} (fallback RAW) falhou: {e}")
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
            return resultado
        except json.JSONDecodeError as e:
            logger.error(f"[{datetime.now()}] [MULTI-GROQ] Erro ao parsear JSON: {e}")
            return {
                "error": "Falha ao parsear JSON",
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
            "uso_ultimo_minuto": {k: self._verificar_uso_recente(k) for k in range(6)},  # NOVO
            "config": {
                "delay_entre_requisicoes": self.delay_entre_requisicoes,
                "max_requisicoes_paralelas": self.max_requisicoes_paralelas,
                "rate_limit_duracao": self.rate_limit_duracao,
                "limite_groq_por_minuto": 30,  # NOVO
                "uso_conservador": "60%"  # NOVO
            }
        }


# Singleton instance
_multi_groq_client: Optional[MultiGroqClient] = None


def get_multi_groq_client() -> MultiGroqClient:
    """Retorna instância singleton do MultiGroqClient"""
    global _multi_groq_client
    
    if _multi_groq_client is None:
        _multi_groq_client = MultiGroqClient()
    
    return _multi_groq_client
