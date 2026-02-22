"""
ALPHA V4 OTIMIZADO - Sistema Profissional de Análise de Ações

🎯 FLUXO COMPLETO - 4 PASSOS (Metodologia Primo Rico)

PASSO 1 - ANÁLISE MACRO (Radar de Oportunidades)
  - Cenário atual: Selic, dólar, setores em aceleração
  - Megatendências e narrativa institucional
  - Cache de 24h para eficiência

PASSO 2 - TRIAGEM CSV (Perfil A e B)
  - Perfil A: Momentum Rápido (2 dias a 2 semanas)
    * ROE > 12%, P/L < 20
  - Perfil B: Consistência com Upside (até 3 meses)
    * ROE > 15%, P/L < 25
  - Elimina: P/L > 25, empresas ruins

PASSO 3 - ANÁLISE PROFUNDA COM RELEASE
  - Saúde financeira real
  - Qualidade da gestão
  - Catalisadores específicos (não genéricos!)
  - Riscos concretos
  - Valorização: caro/justo/barato
  - Nota de 0 a 10

PASSO 4 - RANKING FINAL
  - Apenas ações com nota >= 6
  - Ordenadas por nota (melhor para pior)
  - Estratégia operacional para cada

OBJETIVO: Valorização de preço. Meta: 5% ao mês. NÃO dividendos.
"""
import asyncio
from typing import Dict, List
from datetime import datetime
import pandas as pd
import os
import json

from app.services.multi_gemini_client import get_multi_gemini_client
from app.services.release_manager import get_release_manager
from app.services.precos_service import get_precos_service


class AlphaV4Otimizado:
    """Versão otimizada do Alpha V4 para produção com GEMINI API"""
    
    def __init__(self):
        self.gemini_client = get_multi_gemini_client()
        self.release_manager = get_release_manager()
        self.precos_service = get_precos_service()
        self.cache_precos_file = "data/cache/precos_cache.json"
    
    async def executar_analise_rapida(self, limite_empresas: int = None) -> Dict:
        """
        FLUXO COMPLETO - 4 PASSOS
        
        PASSO 1: Análise Macro (Radar de Oportunidades)
        PASSO 2: Triagem CSV (Perfil A e B) - TODAS as empresas que passarem
        PASSO 3: Análise Profunda com Release
        PASSO 4: Ranking Final (nota >= 6)
        
        Args:
            limite_empresas: IGNORADO - analisa TODAS as empresas que passarem no filtro
        
        Returns:
            Ranking com empresas aprovadas
        """
        print(f"\n{'='*80}")
        print(f"FLUXO COMPLETO - ANALISE DE ACOES COM GROQ")
        print(f"Analisando TODAS as empresas que passarem no filtro")
        print(f"{'='*80}\n")
        
        inicio = datetime.now()
        
        try:
            # PASSO 1: Análise Macro (cache de 24h)
            print("PASSO 1: Análise Macro (Radar de Oportunidades)")
            contexto = await self._analise_macro_cached()
            print(f"OK Contexto macro obtido\n")
            
            # PASSO 2: Filtro Rápido (Perfil A e B) - TODAS
            print("PASSO 2: Triagem CSV (Perfil A e B)")
            empresas = self._filtro_rapido(None)  # None = TODAS
            print(f"OK {len(empresas)} empresas selecionadas\n")
            
            # PASSO 3: Busca Preços
            print("Buscando precos reais...")
            precos = await self._buscar_precos(empresas)
            print(f"OK {len(precos)} precos obtidos\n")
            
            # PASSO 3: Análise Individual com Release
            print("PASSO 3: Análise Profunda com Release")
            analises = await self._analisar_empresas(empresas, precos, contexto)
            print(f"OK {len(analises)} analises concluidas\n")
            
            # PASSO 4: Ranking Final
            print("PASSO 4: Ranking Final (nota >= 6)")
            ranking = self._gerar_ranking(analises)
            print(f"OK {len(ranking)} empresas aprovadas\n")
            
            tempo = (datetime.now() - inicio).total_seconds()
            
            print(f"{'='*80}")
            print(f"✅ ANÁLISE CONCLUÍDA EM {tempo:.1f}s")
            print(f"Total aprovadas: {len(ranking)}/{len(empresas)}")
            print(f"{'='*80}\n")
            
            return {
                "success": True,
                "ranking": ranking,
                "total": len(ranking),
                "tempo_segundos": tempo,
                "contexto_global": contexto
            }
        
        except Exception as e:
            print(f"\nERRO: {e}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "ranking": []
            }
    
    async def _analise_macro_cached(self) -> Dict:
        """
        PASSO 1 - PROMPT MACRO (Radar de Oportunidades)
        Análise macro com cache de 24h
        """
        cache_file = "data/cache/macro_context.json"
        
        # Verifica cache (válido por 24h)
        if os.path.exists(cache_file):
            import json
            with open(cache_file, 'r', encoding='utf-8-sig') as f:
                cache = json.load(f)
            
            cache_time = datetime.fromisoformat(cache.get('timestamp', '2000-01-01'))
            if (datetime.now() - cache_time).total_seconds() < 86400:
                print("[PASSO 1] Usando cache macro (valido por 24h)")
                return cache.get('contexto', {})
        
        # Análise nova
        print("[PASSO 1] Executando analise macro...")
        
        data_hoje = datetime.now().strftime('%d/%m/%Y')
        
        # PROMPT EXATO DO USUÁRIO
        prompt = f"""Você é um analista sênior de investimentos focado em valorização de preço no mercado brasileiro (B3).
Data de hoje: {data_hoje}

Responda em JSON com o seguinte formato:
{{
  "cenario_macro": {{
    "resumo": "Resumo do cenário atual em 3-4 linhas",
    "taxa_selic": "valor atual e tendência",
    "dolar": "patamar atual e impacto nas ações",
    "setores_acelerando": ["setor1", "setor2", "setor3"],
    "setores_evitar": ["setor1", "setor2"],
    "catalisadores_proximas_semanas": ["evento1", "evento2"],
    "narrativa_institucional": "O que fundos e instituições estão comprando agora que o varejo ainda não percebeu",
    "alertas": ["alerta1", "alerta2"]
  }},
  "megatendencias": [
    {{
      "nome": "nome da tendência",
      "setores_beneficiados": ["setor"],
      "timing": "curto/médio/longo prazo",
      "estagio_ciclo": "começo/meio/fim"
    }}
  ]
}}"""
        
        try:
            contexto = await self.gemini_client.executar_prompt(
                prompt=prompt,
                task_type="radar"
            )
            
            # Adiciona resumo executivo para uso posterior
            if 'cenario_macro' in contexto:
                contexto['resumo_executivo'] = contexto['cenario_macro'].get('resumo', 'N/A')
            
            # Salva cache
            os.makedirs("data/cache", exist_ok=True)
            import json
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "contexto": contexto
                }, f, ensure_ascii=False, indent=2)
            
            print(f"[PASSO 1] OK Analise macro concluida e salva em cache")
            return contexto
        except Exception as e:
            print(f"[PASSO 1] ERRO: {e}")
            return {"resumo_executivo": "Analise macro nao disponivel", "cenario_macro": {}}
    
    def _filtro_rapido(self, limite: int) -> List[str]:
        """
        PASSO 2 - TRIAGEM DO CSV
        Filtra ações com Perfil A (Momentum) ou Perfil B (Consistência)
        RETORNA TODAS AS EMPRESAS QUE PASSAREM NO FILTRO (sem limite)
        """
        csv_path = "data/stocks.csv"
        if not os.path.exists(csv_path):
            return []
        
        print("[PASSO 2] Filtrando ações com Perfil A ou B...")
        
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        # PERFIL A - Momentum Rápido (2 dias a 2 semanas)
        # - ROE > 12%
        # - P/L abaixo da média do setor
        perfil_a = df[
            (df['roe'] > 0.12) &
            (df['pl'] > 0) &
            (df['pl'] < 20)
        ].copy()
        
        # PERFIL B - Consistência com Upside (até 3 meses)
        # - ROE > 15%
        # - P/L razoável
        perfil_b = df[
            (df['roe'] > 0.15) &
            (df['pl'] > 0) &
            (df['pl'] < 25)
        ].copy()
        
        # CRITÉRIOS DE ELIMINAÇÃO
        # - P/L > 25 sem justificativa
        # - Empresas ruins
        
        # Combina perfis (remove duplicatas)
        df_filtrado = pd.concat([perfil_a, perfil_b]).drop_duplicates(subset=['ticker'])
        
        # Ordena por ROE (prioriza qualidade)
        df_filtrado = df_filtrado.sort_values('roe', ascending=False)
        
        # RETORNA TODAS (sem limite)
        tickers = df_filtrado['ticker'].tolist()
        print(f"[PASSO 2] OK {len(tickers)} acoes selecionadas (Perfil A ou B) - TODAS")
        
        return tickers
    
    def _carregar_cache_precos(self) -> Dict:
        """Carrega cache de preços do arquivo"""
        if not os.path.exists(self.cache_precos_file):
            return {}
        
        try:
            with open(self.cache_precos_file, 'r', encoding='utf-8-sig') as f:
                cache = json.load(f)
            return cache.get('precos', {})
        except:
            return {}
    
    def _salvar_cache_precos(self, precos: Dict):
        """Salva preços no cache"""
        try:
            os.makedirs("data/cache", exist_ok=True)
            
            # Carrega cache existente
            cache_atual = self._carregar_cache_precos()
            
            # Atualiza com novos preços
            for ticker, dados in precos.items():
                if dados and dados.get('regularMarketPrice', 0) > 0:
                    cache_atual[ticker] = {
                        'preco': dados.get('regularMarketPrice'),
                        'timestamp': datetime.now().isoformat(),
                        'fonte': dados.get('fonte', 'api')
                    }
            
            # Salva
            with open(self.cache_precos_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'precos': cache_atual,
                    'ultima_atualizacao': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
            
            print(f"[CACHE] {len(cache_atual)} preços salvos")
        except Exception as e:
            print(f"[CACHE] Erro ao salvar: {e}")
    
    async def _buscar_precos(self, tickers: List[str]) -> Dict:
        """
        Busca preços com fallback para cache
        
        1. Tenta buscar da API
        2. Se falhar (401), usa cache
        3. Salva novos preços no cache
        """
        print(f"[PRECOS] Buscando {len(tickers)} precos...")
        
        # Carrega cache
        cache = self._carregar_cache_precos()
        
        try:
            # Tenta API
            precos_api = await self.precos_service.get_multiple_quotes(tickers)
            
            if precos_api and len(precos_api) > 0:
                print(f"[PRECOS] {len(precos_api)} obtidos da API")
                
                # Salva no cache
                self._salvar_cache_precos(precos_api)
                
                return precos_api
            else:
                # API não retornou nada, usa cache
                print(f"[PRECOS] API vazia, usando cache")
                return self._usar_cache(tickers, cache)
        
        except Exception as e:
            # Erro na API, usa cache
            print(f"[PRECOS] Erro na API ({str(e)[:50]}), usando cache")
            return self._usar_cache(tickers, cache)
    
    def _usar_cache(self, tickers: List[str], cache: Dict) -> Dict:
        """Usa preços do cache"""
        precos_cache = {}
        
        for ticker in tickers:
            if ticker in cache:
                dados_cache = cache[ticker]
                precos_cache[ticker] = {
                    'regularMarketPrice': dados_cache['preco'],
                    'fonte': 'cache',
                    'timestamp_cache': dados_cache['timestamp']
                }
        
        print(f"[CACHE] {len(precos_cache)} preços recuperados do cache")
        
        # Se cache também está vazio, retorna vazio
        if not precos_cache:
            print(f"[CACHE] Cache vazio para esses tickers")
        
        return precos_cache
    
    async def _analisar_empresas(self, tickers: List[str], precos: Dict, contexto: Dict) -> List[Dict]:
        """
        Analisa empresas em paralelo com controle de rate limit
        
        GEMINI FREE TIER: 5 req/min por chave
        Com 6 chaves: 30 req/min total
        Estratégia: 1 req a cada 2 segundos = 30 req/min
        """
        print(f"[ANALISE] Analisando {len(tickers)} empresas...")
        print(f"[RATE LIMIT] Gemini: 5 req/min por chave, delay de 2s entre requisições")
        
        df = pd.read_csv("data/stocks.csv", encoding='utf-8-sig')
        analises = []
        
        # Processa sequencialmente com delay (evita rate limit)
        for i, ticker in enumerate(tickers, 1):
            preco = precos.get(ticker, {}).get('regularMarketPrice', 0)
            if preco > 0:
                print(f"[{i}/{len(tickers)}] Analisando {ticker}...")
                
                try:
                    resultado = await self._analisar_empresa(ticker, preco, df, contexto)
                    if isinstance(resultado, dict):
                        analises.append(resultado)
                        print(f"  OK {ticker}: Nota {resultado.get('nota', 0):.1f}/10")
                except Exception as e:
                    print(f"  ERRO {ticker}: {str(e)[:80]}")
                
                # Delay de 2s entre requisições (30 req/min)
                if i < len(tickers):
                    await asyncio.sleep(2)
        
        print(f"[ANALISE] {len(analises)} concluidas")
        return analises
    
    async def _analisar_empresa(self, ticker: str, preco: float, df: pd.DataFrame, contexto: Dict) -> Dict:
        """
        PASSO 3 - ANÁLISE PROFUNDA COM RELEASE
        Analisa uma empresa usando release de resultados
        """
        try:
            # Dados do CSV
            row = df[df['ticker'] == ticker]
            if row.empty:
                return None
            
            row = row.iloc[0]
            roe = row['roe'] * 100 if row['roe'] < 1 else row['roe']
            pl = row['pl']
            setor = row.get('setor', 'N/A')
            
            # Release
            release = self.release_manager.obter_release_mais_recente(ticker)
            release_texto = ""
            if release:
                release_texto = f"\n\n[LANÇAMENTO ABAIXO]\n{release.get('conteudo', '')[:3000]}\n[FIM DO LANÇAMENTO]"
            
            # Contexto macro resumido
            contexto_resumo = contexto.get('resumo_executivo', 'N/A')
            if not contexto_resumo or contexto_resumo == 'N/A':
                cenario = contexto.get('cenario_macro', {})
                contexto_resumo = cenario.get('resumo', 'Cenário macro não disponível')
            
            # PROMPT EXATO DO USUÁRIO - PASSO 3
            prompt = f"""[CONTEXTO MACRO E TRIAGEM]
Cenário macro: {contexto_resumo}
Empresa selecionada na triagem: {ticker}
Preço atual na bolsa: R$ {preco:.2f}
ROE: {roe:.1f}% | P/L: {pl:.2f}
Setor: {setor}
[FIM DO CONTEXTO]

Analisar o lançamento de resultados abaixo da empresa {ticker}.

Avalie os seguintes pontos:

1. SAÚDE FINANCEIRA REAL
   - Geração de caixa operacional, tendência de margens, endividamento real

2. QUALIDADE DA GESTÃO
   - O que o release mostra sobre execução, alocação de capital e transparência

3. CATALISADORES DE VALORIZAÇÃO
   - O que pode fazer essa ação subir nos próximos 6 a 18 meses? Seja específico.

4. RISCOS CONCRETOS
   - Não os genéricos. Os riscos que realmente podem derrubar o preço DESSA empresa.

5. VALORIZAÇÃO
   - Com base nos fundamentos e no preço atual de R$ {preco:.2f}, a ação tá cara, justa ou barata?

6. NOTA DE RECOMENDAÇÃO (0 a 10)
   - Se a empresa for claramente ruim para o objetivo de valorização de preço, retorne nota 0 e explique por quê descartar.
{release_texto if release else "\n[RELEASE NÃO DISPONÍVEL - Analise apenas com os dados fornecidos]"}

Retorne JSON:
{{
  "ticker": "{ticker}",
  "preco_atual": {preco:.2f},
  "nota": 7.5,
  "recomendacao": "COMPRA FORTE|COMPRA|MONITORAR|DESCARTAR",
  "saude_financeira": "análise detalhada",
  "qualidade_gestao": "análise detalhada",
  "catalisadores": ["catalisador específico 1", "catalisador específico 2"],
  "riscos_reais": ["risco concreto 1", "risco concreto 2"],
  "valorizacao": "cara|justa|barata — justificativa detalhada",
  "tese_resumida": "Por que comprar ou não comprar essa ação agora em 4-5 linhas"
}}"""
            
            resposta = await self.gemini_client.executar_prompt(
                prompt=prompt,
                task_type="analise_profunda"
            )
            
            # Adiciona dados complementares
            resposta['preco_atual'] = preco
            resposta['roe'] = roe
            resposta['pl'] = pl
            resposta['setor'] = setor
            
            # Converte nota para score (compatibilidade)
            if 'nota' in resposta:
                resposta['score'] = resposta['nota']
            
            # Calcula preço teto e upside
            nota = resposta.get('nota', 5)
            if nota >= 8:
                multiplicador = 1.30  # +30%
            elif nota >= 6:
                multiplicador = 1.20  # +20%
            elif nota >= 4:
                multiplicador = 1.10  # +10%
            else:
                multiplicador = 1.05  # +5%
            
            resposta['preco_teto'] = preco * multiplicador
            resposta['upside'] = (multiplicador - 1) * 100
            
            return resposta
        
        except Exception as e:
            print(f"[PASSO 3] {ticker}: Erro - {str(e)[:100]}")
            return None
    
    def _gerar_ranking(self, analises: List[Dict]) -> List[Dict]:
        """
        PASSO 4 - RANKING FINAL
        Gera ranking ordenado por nota/score
        """
        # Remove None
        analises = [a for a in analises if a]
        
        # Filtra apenas ações com nota >= 6 (aprovadas)
        analises_aprovadas = [a for a in analises if a.get('nota', 0) >= 6 or a.get('score', 0) >= 6]
        
        print(f"[PASSO 4] {len(analises_aprovadas)}/{len(analises)} ações aprovadas (nota >= 6)")
        
        # Ordena por nota/score
        analises_aprovadas.sort(key=lambda x: x.get('nota', x.get('score', 0)), reverse=True)
        
        # Adiciona rank
        for i, analise in enumerate(analises_aprovadas, 1):
            analise['rank'] = i
        
        return analises_aprovadas


# Singleton
_alpha_v4_otimizado = None

def get_alpha_v4_otimizado():
    """Retorna instância singleton"""
    global _alpha_v4_otimizado
    if _alpha_v4_otimizado is None:
        _alpha_v4_otimizado = AlphaV4Otimizado()
    return _alpha_v4_otimizado
