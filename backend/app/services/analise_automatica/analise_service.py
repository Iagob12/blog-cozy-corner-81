"""
Serviço Principal de Análise Automática

Orquestra todo o processo de análise incremental
"""
import asyncio
import hashlib
import os
from typing import Dict, List, Optional
from datetime import datetime

from .cache_manager import CacheManager
from .validador import ValidadorResultados
from app.services.multi_groq_client import get_multi_groq_client
from app.services.release_manager import get_release_manager
from app.services.precos_service import get_precos_service
from app.services.dados_fundamentalistas_service import get_dados_fundamentalistas_service


class AnaliseAutomaticaService:
    """
    Serviço de análise automática e incremental
    
    Features:
    - Analisa apenas empresas que precisam
    - Cache inteligente
    - Validação rigorosa
    - Tratamento robusto de erros
    - Logs detalhados
    """
    
    def __init__(self):
        self.cache_manager = CacheManager()
        self.validador = ValidadorResultados()
        self.ai_client = get_multi_groq_client()
        self.release_manager = get_release_manager()
        self.precos_service = get_precos_service()  # Serviço unificado (Brapi + HG Brasil)
        self.dados_service = get_dados_fundamentalistas_service()
        
        print("✓ Análise Automática Service inicializado")
    
    async def analisar_incrementalmente(
        self,
        empresas: List[str],
        forcar_reanalise: bool = False,
        max_paralelo: int = 3
    ) -> Dict:
        """
        Analisa empresas incrementalmente
        
        Args:
            empresas: Lista de tickers
            forcar_reanalise: Se True, ignora cache
            max_paralelo: Máximo de análises paralelas
        
        Returns:
            Resultado com estatísticas
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISE INCREMENTAL AUTOMÁTICA")
        print(f"{'='*70}")
        print(f"📊 Total de empresas: {len(empresas)}")
        print(f"🔄 Forçar reanálise: {'Sim' if forcar_reanalise else 'Não'}")
        print(f"⚡ Análises paralelas: {max_paralelo}")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        
        # 1. Identifica empresas que precisam análise
        empresas_para_analisar = await self._identificar_empresas_para_analisar(
            empresas, 
            forcar_reanalise
        )
        
        empresas_com_cache = len(empresas) - len(empresas_para_analisar)
        
        print(f"\n📋 RESUMO:")
        print(f"   Para analisar: {len(empresas_para_analisar)}")
        print(f"   Com cache válido: {empresas_com_cache}")
        
        if len(empresas_para_analisar) == 0:
            print(f"\n✅ Todas as empresas já têm cache válido!")
            ranking = self.cache_manager.gerar_ranking()
            self.cache_manager.salvar_ranking(ranking)
            
            return {
                "success": True,
                "novas_analises": 0,
                "cache_mantido": empresas_com_cache,
                "falhas": 0,
                "total_ranking": len(ranking),
                "tempo_segundos": 0
            }
        
        # 2. Busca preços (batch)
        print(f"\n💰 Buscando preços...")
        precos = await self._buscar_precos_batch(empresas_para_analisar)
        print(f"   ✓ {len(precos)} preços obtidos")
        
        # 3. Analisa empresas (com controle de paralelismo)
        print(f"\n🤖 Analisando empresas...")
        resultados = await self._analisar_empresas_batch(
            empresas_para_analisar,
            precos,
            max_paralelo=1  # REDUZIDO: 1 por vez para evitar rate limit do yfinance
        )
        
        # 4. Gera ranking atualizado
        print(f"\n🏆 Gerando ranking...")
        ranking = self.cache_manager.gerar_ranking()
        self.cache_manager.salvar_ranking(ranking)
        
        # 5. Salva cache
        self.cache_manager.salvar_cache()
        
        # 6. Adiciona ao histórico
        self.cache_manager.adicionar_ao_historico({
            "tipo": "analise_incremental",
            "empresas_analisadas": len(resultados["sucesso"]),
            "empresas_falhadas": len(resultados["falhas"]),
            "tempo_segundos": (datetime.now() - inicio).total_seconds()
        })
        
        tempo_total = (datetime.now() - inicio).total_seconds()
        
        print(f"\n{'='*70}")
        print(f"✅ ANÁLISE CONCLUÍDA")
        print(f"{'='*70}")
        print(f"✓ Novas análises: {len(resultados['sucesso'])}")
        print(f"💾 Cache mantido: {empresas_com_cache}")
        print(f"❌ Falhas: {len(resultados['falhas'])}")
        print(f"🏆 Ranking: {len(ranking)} empresas")
        print(f"⏱️  Tempo total: {tempo_total:.1f}s")
        print(f"{'='*70}\n")
        
        return {
            "success": True,
            "novas_analises": len(resultados["sucesso"]),
            "cache_mantido": empresas_com_cache,
            "falhas": len(resultados["falhas"]),
            "detalhes_falhas": resultados["falhas"],
            "total_ranking": len(ranking),
            "tempo_segundos": tempo_total
        }
    
    async def _identificar_empresas_para_analisar(
        self,
        empresas: List[str],
        forcar: bool
    ) -> List[str]:
        """Identifica quais empresas precisam ser analisadas"""
        empresas_para_analisar = []
        
        for ticker in empresas:
            if forcar:
                empresas_para_analisar.append(ticker)
                continue
            
            # Verifica se tem release
            release = self.release_manager.obter_release_mais_recente(ticker)
            tem_release = release is not None
            release_hash = self._calcular_hash_release(release) if release else None
            
            # Verifica se precisa reanalisar
            if self.cache_manager.precisa_reanalisar(
                ticker,
                tem_release_novo=tem_release,
                release_hash_novo=release_hash,
                max_idade_horas=24
            ):
                empresas_para_analisar.append(ticker)
        
        return empresas_para_analisar
    
    async def _buscar_precos_batch(self, tickers: List[str]) -> Dict[str, float]:
        """Busca preços de múltiplas ações usando cache + API"""
        from app.services.precos_cache_service import get_precos_cache_service
        
        cache_service = get_precos_cache_service()
        precos = {}
        
        # 1. Tenta buscar do cache primeiro
        print("   💾 Verificando cache...")
        precos_cache = cache_service.obter_precos_batch(tickers, max_idade_minutos=120)
        
        for ticker, dados in precos_cache.items():
            precos[ticker] = dados['preco']
            indicador = dados['indicador']
            idade = dados['idade_minutos']
            print(f"      {ticker}: R$ {dados['preco']:.2f} {indicador} (cache {idade}min)")
        
        # 2. Busca da API apenas os que não estão no cache
        tickers_faltando = [t for t in tickers if t not in precos]
        
        if tickers_faltando:
            print(f"   🌐 Buscando {len(tickers_faltando)} preços da API...")
            try:
                quotes = await self.precos_service.get_multiple_quotes(tickers_faltando)
                
                precos_novos = {}
                for ticker, quote in quotes.items():
                    preco = quote.get("regularMarketPrice", 0)
                    if preco > 0:
                        precos[ticker] = preco
                        precos_novos[ticker] = preco
                        print(f"      {ticker}: R$ {preco:.2f} 🟢 (API)")
                
                # Atualiza cache
                if precos_novos:
                    cache_service.atualizar_precos_batch(precos_novos, fonte="brapi")
                    print(f"   💾 Cache atualizado com {len(precos_novos)} preços")
            
            except Exception as e:
                print(f"   ⚠️ Erro ao buscar da API: {e}")
                print(f"   ℹ️ Usando apenas preços do cache")
        
        return precos
    
    async def _analisar_empresas_batch(
        self,
        tickers: List[str],
        precos: Dict[str, float],
        max_paralelo: int
    ) -> Dict:
        """
        Analisa múltiplas empresas com controle de paralelismo
        
        Returns:
            {"sucesso": [...], "falhas": [...]}
        """
        sucesso = []
        falhas = []
        
        # Divide em batches
        for i in range(0, len(tickers), max_paralelo):
            batch = tickers[i:i + max_paralelo]
            
            # Analisa batch em paralelo
            tasks = [
                self._analisar_empresa(ticker, precos.get(ticker, 0))
                for ticker in batch
            ]
            
            resultados = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Processa resultados
            for ticker, resultado in zip(batch, resultados):
                if isinstance(resultado, Exception):
                    print(f"❌ {ticker}: {str(resultado)[:50]}")
                    falhas.append({"ticker": ticker, "erro": str(resultado)})
                elif resultado:
                    sucesso.append(ticker)
                else:
                    falhas.append({"ticker": ticker, "erro": "Análise retornou None"})
            
            # Delay entre batches (aumentado para evitar rate limit)
            if i + max_paralelo < len(tickers):
                await asyncio.sleep(5)  # 5 segundos entre empresas
        
        return {"sucesso": sucesso, "falhas": falhas}
    
    async def _analisar_empresa(self, ticker: str, preco_atual: float) -> bool:
        """
        Analisa uma empresa individual
        
        Returns:
            True se sucesso, False se falha
        """
        try:
            print(f"🔍 {ticker}: Iniciando análise...")
            
            # Valida preço
            if preco_atual <= 0:
                print(f"⚠️ {ticker}: Sem preço disponível")
                return False
            
            # 1. Busca dados do CSV
            print(f"   📊 Buscando dados do CSV...")
            dados_csv = self._obter_dados_csv(ticker)
            
            if not dados_csv:
                print(f"⚠️ {ticker}: Não encontrado no CSV")
                return False
            
            # 2. Busca release
            release = self.release_manager.obter_release_mais_recente(ticker)
            tem_release = release is not None
            
            # 3. Monta prompt simplificado (apenas CSV + release)
            prompt = self._montar_prompt_simplificado(ticker, dados_csv, preco_atual, release)
            
            # 4. Chama IA
            print(f"   🤖 Consultando IA...")
            try:
                resposta = await self.ai_client.executar_prompt(
                    prompt=prompt,
                    task_type="analise_fundamentalista"
                )
                
                if not resposta:
                    print(f"❌ {ticker}: IA retornou None")
                    return False
                
                # A resposta pode vir diretamente como JSON ou dentro de {"resposta": ...}
                if isinstance(resposta, dict):
                    # Se já é um dict com os campos esperados, usa direto
                    if "ticker" in resposta or "recomendacao" in resposta:
                        analise = resposta
                    # Se está dentro de {"resposta": ...}, extrai
                    elif "resposta" in resposta:
                        analise = resposta.get("resposta")
                        if isinstance(analise, str):
                            # Se resposta é string, tenta parsear
                            analise = self.validador.extrair_json_da_resposta(analise)
                    else:
                        print(f"❌ {ticker}: Resposta em formato inesperado: {list(resposta.keys())}")
                        return False
                else:
                    print(f"❌ {ticker}: Resposta não é dict: {type(resposta)}")
                    return False
                    
            except Exception as e:
                print(f"❌ {ticker}: Erro ao chamar IA - {str(e)[:100]}")
                return False
            
            if not analise:
                print(f"❌ {ticker}: Não foi possível extrair análise")
                return False
            
            # Garante ticker correto
            analise["ticker"] = ticker
            
            # Valida estrutura
            valido, erros = self.validador.validar(analise, ticker, preco_atual)
            
            if not valido:
                print(f"❌ {ticker}: Validação falhou:")
                for erro in erros[:3]:
                    print(f"      - {erro}")
                return False
            
            # Valida nota com cálculo estruturado
            print(f"   🔍 Validando nota...")
            from app.services.notas_estruturadas_service import get_notas_estruturadas_service
            
            notas_service = get_notas_estruturadas_service()
            nota_calculada, detalhes = notas_service.calcular_nota(
                dados_csv=dados_csv,
                preco_atual=preco_atual,
                tem_release=tem_release,
                setor_quente=False  # Simplificado por enquanto
            )
            
            nota_ia = analise.get('score', 0)
            valido_nota, msg_nota = notas_service.validar_nota_ia(nota_ia, nota_calculada, max_divergencia=2.0)
            
            if not valido_nota:
                print(f"   ⚠️ {msg_nota}")
                print(f"      Nota IA: {nota_ia:.1f} | Calculada: {nota_calculada:.1f}")
                # Não rejeita, apenas avisa
            else:
                print(f"   ✓ Nota validada: {msg_nota}")
            
            # 6. Salva no cache
            release_hash = self._calcular_hash_release(release) if release else None
            dados_hash = self._calcular_hash_dados_csv(dados_csv)
            
            self.cache_manager.adicionar_analise(
                ticker=ticker,
                analise=analise,
                tem_release=tem_release,
                release_hash=release_hash,
                dados_hash=dados_hash
            )
            
            print(f"✅ {ticker}: Análise concluída (Score: {analise.get('score', 0):.1f})")
            return True
            
        except Exception as e:
            print(f"❌ {ticker}: Erro - {str(e)[:50]}")
            return False
    
    def _obter_dados_csv(self, ticker: str) -> Optional[Dict]:
        """Obtém dados do CSV para um ticker específico"""
        try:
            import pandas as pd
            csv_path = "data/stocks.csv"
            
            if not os.path.exists(csv_path):
                return None
            
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
            
            # Busca ticker (case insensitive)
            linha = df[df['ticker'].str.upper() == ticker.upper()]
            
            if linha.empty:
                return None
            
            # Extrai dados
            dados = linha.iloc[0].to_dict()
            
            return {
                "ticker": ticker,
                "roe": dados.get("roe", 0),
                "pl": dados.get("pl", 0),
                "cagr": dados.get("cagr", 0),
                "setor": dados.get("setor", "N/A"),
                "nome": dados.get("nome", ticker)
            }
        
        except Exception as e:
            print(f"      Erro ao ler CSV: {e}")
            return None
    
    def _montar_prompt_simplificado(
        self,
        ticker: str,
        dados_csv: Dict,
        preco: float,
        release: Optional[Dict]
    ) -> str:
        """Monta prompt MELHORADO baseado no Primo Rico - FOCO EM 5% AO MÊS"""
        
        prompt = f"""Você é um analista fundamentalista sênior com 20 anos de experiência, especializado em identificar ações com potencial de valorização de 5% ao mês.

EMPRESA: {ticker} - {dados_csv.get('nome', ticker)}
SETOR: {dados_csv.get('setor', 'N/A')}

DADOS FUNDAMENTALISTAS:
- ROE: {dados_csv.get('roe', 0):.2f}%
- P/L: {dados_csv.get('pl', 0):.2f}
- CAGR (Crescimento): {dados_csv.get('cagr', 0):.2f}%
- Setor: {dados_csv.get('setor', 'N/A')}

PREÇO ATUAL: R$ {preco:.2f}
"""
        
        if release:
            prompt += f"""
RELEASE DE RESULTADOS DISPONÍVEL:
- Trimestre: {release.get('trimestre')} {release.get('ano')}
- Arquivo: {release.get('filename')}

✅ IMPORTANTE: Considere os dados do release na análise. Se resultados foram positivos (crescimento de receita/lucro), AUMENTE o score. Se negativos, DIMINUA o score.
"""
        else:
            prompt += "\n⚠️ NOTA: Sem release disponível. Análise baseada apenas em dados históricos do CSV.\n"
        
        prompt += """
TAREFA: Analise profundamente esta empresa considerando:

1. **POTENCIAL DE VALORIZAÇÃO DE 5% AO MÊS** (CRÍTICO)
   - Esta ação tem fundamentos para valorizar 5%+ nos próximos 30 dias?
   - Existem catalisadores de curto prazo?
   - O preço está atrativo (P/L baixo)?

2. **QUALIDADE FUNDAMENTALISTA**
   - ROE > 12%? (Excelente se sim)
   - P/L entre 5-15? (Ideal)
   - Crescimento consistente? (CAGR > 10%)
   - Margem saudável?

3. **VANTAGENS COMPETITIVAS**
   - Empresa tem moat (barreira de entrada)?
   - Marca forte no setor?
   - Poder de precificação?

4. **PERSPECTIVAS DO SETOR**
   - Setor em crescimento?
   - Tendências favoráveis?
   - Regulação positiva?

5. **RISCOS ESPECÍFICOS**
   - Quais os principais riscos?
   - Endividamento alto?
   - Concorrência acirrada?

CRITÉRIOS DE SCORE:
- Score 9-10: COMPRA FORTE - Potencial de 5%+ ao mês, fundamentos excelentes
- Score 7-8: COMPRA - Bons fundamentos, potencial de 3-5% ao mês
- Score 5-6: MANTER - Fundamentos OK, potencial de 1-3% ao mês
- Score 3-4: VENDA - Fundamentos fracos, risco de queda
- Score 0-2: VENDA FORTE - Fundamentos ruins, alto risco

Retorne APENAS este JSON (sem markdown, sem explicações):
{
  "ticker": "XXXX3",
  "recomendacao": "COMPRA FORTE|COMPRA|MANTER|VENDA|AGUARDAR",
  "preco_teto": 50.00,
  "upside": 25.5,
  "score": 8.5,
  "riscos": ["Risco 1", "Risco 2", "Risco 3"],
  "catalisadores": ["Catalisador 1", "Catalisador 2"],
  "resumo": "Análise em 1-2 frases focando no potencial de valorização"
}

IMPORTANTE:
- Score de 0 a 10 (quanto maior, melhor)
- Upside em % (pode ser negativo se ação está cara)
- Mínimo 2 riscos e 2 catalisadores
- Recomendação coerente com score:
  * Score >= 8: COMPRA FORTE
  * Score 6-7: COMPRA
  * Score 4-5: MANTER
  * Score 2-3: VENDA
  * Score < 2: AGUARDAR
- Seja RIGOROSO: apenas ações REALMENTE boas devem ter score alto
"""
        return prompt
    
    def _calcular_hash_dados_csv(self, dados_csv: Dict) -> str:
        """Calcula hash dos dados do CSV"""
        import json
        
        # Usa apenas campos relevantes
        campos_relevantes = {
            "roe": dados_csv.get("roe"),
            "pl": dados_csv.get("pl"),
            "cagr": dados_csv.get("cagr")
        }
        
        identificador = json.dumps(campos_relevantes, sort_keys=True)
        return hashlib.md5(identificador.encode()).hexdigest()
    
    def _calcular_hash_release(self, release: Optional[Dict]) -> Optional[str]:
        """Calcula hash do release para detectar mudanças"""
        if not release:
            return None
        
        # Usa filename + data_upload como identificador
        identificador = f"{release.get('filename')}_{release.get('data_upload')}"
        return hashlib.md5(identificador.encode()).hexdigest()
    
    def _calcular_hash_dados(self, dados: Dict) -> str:
        """Calcula hash dos dados fundamentalistas"""
        import json
        
        # Usa apenas campos relevantes
        campos_relevantes = {
            "roe": dados.get("financeiro", {}).get("roe"),
            "pl": dados.get("financeiro", {}).get("pl"),
            "margem": dados.get("financeiro", {}).get("margem_liquida")
        }
        
        identificador = json.dumps(campos_relevantes, sort_keys=True)
        return hashlib.md5(identificador.encode()).hexdigest()
    
    def obter_ranking_atual(self) -> Optional[Dict]:
        """Retorna ranking atual"""
        return self.cache_manager.obter_ranking_atual()
    
    def obter_estatisticas(self) -> Dict:
        """Retorna estatísticas do sistema"""
        stats_cache = self.cache_manager.obter_estatisticas()
        stats_validador = self.validador.obter_estatisticas_erros()
        
        return {
            **stats_cache,
            "validacao": stats_validador
        }


# Singleton
_analise_service = None

def get_analise_automatica_service() -> AnaliseAutomaticaService:
    """Retorna instância singleton"""
    global _analise_service
    if _analise_service is None:
        _analise_service = AnaliseAutomaticaService()
    return _analise_service
