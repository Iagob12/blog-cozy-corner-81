"""
AnÃ¡lise Completa com Releases
Analisa empresas que tÃªm releases, uma por vez, calculando nota e estratÃ©gia
"""
import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class AnaliseComReleaseService:
    """
    ServiÃ§o de anÃ¡lise completa com releases
    
    Fluxo:
    1. Pega empresas com releases
    2. Para cada empresa (SEQUENCIAL):
       - Busca preÃ§o atual
       - LÃª release (PDF)
       - Envia para IA: release + preÃ§o + dados CSV
       - IA retorna: nota, anÃ¡lise, recomendaÃ§Ã£o
       - Calcula estratÃ©gia (entrada/stop/alvo)
       - Salva no ranking
    3. Ordena ranking por nota
    4. Salva ranking_atual.json
    """
    
    def __init__(self):
        self.ranking_file = "data/cache/ranking_atual.json"
        self.csv_path = "data/stocks.csv"
        
        logger.info("âœ“ AnÃ¡lise com Release Service inicializado")
    
    async def analisar_todas_com_releases(
        self,
        forcar_reanalise: bool = False
    ) -> Dict:
        """
        Analisa todas as empresas que tÃªm releases
        
        Args:
            forcar_reanalise: Se True, reanalisa mesmo que jÃ¡ tenha anÃ¡lise recente
        
        Returns:
            Dict com resultado da anÃ¡lise
        """
        from app.services.release_manager import get_release_manager
        from app.services.brapi_service import BrapiService
        
        release_manager = get_release_manager()
        brapi_service = BrapiService()
        
        # 1. Pega empresas com releases
        empresas_com_release = release_manager.listar_empresas_com_releases()
        
        if not empresas_com_release:
            logger.warning("âš ï¸ Nenhuma empresa com release")
            return {
                "sucesso": False,
                "mensagem": "Nenhuma empresa com release disponÃ­vel"
            }
        
        logger.info(f"ðŸ“Š Analisando {len(empresas_com_release)} empresas com releases")
        
        if forcar_reanalise:
            logger.info(f"âš¡ MODO: ReanÃ¡lise forÃ§ada - TODAS as empresas serÃ£o reanalisadas")
        else:
            logger.info(f"ðŸ’¾ MODO: AnÃ¡lise incremental - Apenas empresas novas ou atualizadas")
        
        # 2. Carrega CSV
        if not os.path.exists(self.csv_path):
            logger.error("âŒ CSV nÃ£o encontrado")
            return {
                "sucesso": False,
                "mensagem": "CSV nÃ£o encontrado"
            }
        
        df_csv = pd.read_csv(self.csv_path, encoding='utf-8-sig')
        df_csv['ticker'] = df_csv['ticker'].str.upper()
        
        # 3. Carrega ranking anterior (fallback em caso de erro)
        ranking_anterior = {}
        if os.path.exists(self.ranking_file):
            try:
                with open(self.ranking_file, 'r', encoding='utf-8-sig') as f:
                    data_anterior = json.load(f)
                    for item in data_anterior.get('ranking', []):
                        ticker = item.get('ticker')
                        if ticker:
                            # Normaliza item (garante que tem 'nota')
                            if 'nota' not in item and 'score' in item:
                                item['nota'] = item['score']
                            elif 'nota' not in item:
                                item['nota'] = 5.0
                            
                            ranking_anterior[ticker] = item
                logger.info(f"ðŸ’¾ Carregado ranking anterior com {len(ranking_anterior)} empresas")
            except Exception as e:
                logger.warning(f"âš ï¸ NÃ£o foi possÃ­vel carregar ranking anterior: {e}")
        
        # 4. Analisa cada empresa SEQUENCIALMENTE
        ranking = []
        total_analisadas = 0
        total_erros = 0
        total_fallback = 0
        
        for ticker in empresas_com_release:
            try:
                logger.info(f"\nðŸ” Analisando {ticker}...")
                
                # Busca dados do CSV
                linha_csv = df_csv[df_csv['ticker'] == ticker]
                if linha_csv.empty:
                    logger.warning(f"âš ï¸ {ticker} nÃ£o encontrado no CSV")
                    # Tenta usar resultado anterior
                    if ticker in ranking_anterior:
                        logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                        ranking.append(ranking_anterior[ticker])
                        total_fallback += 1
                    continue
                
                dados_csv = linha_csv.iloc[0].to_dict()
                
                # Busca preÃ§o atual E dados fundamentalistas da Brapi
                logger.info(f"  ðŸ“ˆ Buscando dados fundamentalistas de {ticker}...")
                dados_brapi = await brapi_service.get_quote_with_fundamentals(
                    ticker,
                    modules=["summaryProfile", "defaultKeyStatistics", "financialData"]
                )
                
                if not dados_brapi:
                    logger.warning(f"âš ï¸ {ticker}: Dados da Brapi nÃ£o disponÃ­veis")
                    # Tenta usar resultado anterior
                    if ticker in ranking_anterior:
                        logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                        ranking.append(ranking_anterior[ticker])
                        total_fallback += 1
                    continue
                
                preco_atual = dados_brapi.get('regularMarketPrice', 0)
                
                if not preco_atual or preco_atual <= 0:
                    logger.warning(f"âš ï¸ {ticker}: PreÃ§o nÃ£o disponÃ­vel")
                    # Tenta usar resultado anterior
                    if ticker in ranking_anterior:
                        logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                        ranking.append(ranking_anterior[ticker])
                        total_fallback += 1
                    continue
                
                # Busca release
                release = release_manager.obter_release_mais_recente(ticker)
                if not release:
                    logger.warning(f"âš ï¸ {ticker}: Release nÃ£o encontrado")
                    # Tenta usar resultado anterior
                    if ticker in ranking_anterior:
                        logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                        ranking.append(ranking_anterior[ticker])
                        total_fallback += 1
                    continue
                
                # Analisa com IA (agora com dados fundamentalistas completos)
                resultado_analise = await self._analisar_empresa_com_ia(
                    ticker=ticker,
                    dados_csv=dados_csv,
                    dados_brapi=dados_brapi,
                    preco_atual=preco_atual,
                    release_path=release['path']
                )
                
                if not resultado_analise:
                    logger.error(f"âŒ {ticker}: Falha na anÃ¡lise")
                    total_erros += 1
                    # Tenta usar resultado anterior
                    if ticker in ranking_anterior:
                        logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                        ranking.append(ranking_anterior[ticker])
                        total_fallback += 1
                    continue
                
                # Calcula estratÃ©gia
                estrategia = await self._calcular_estrategia(
                    ticker=ticker,
                    preco_atual=preco_atual,
                    preco_teto=resultado_analise.get('preco_teto', preco_atual * 1.05),
                    nota=resultado_analise.get('nota', 5.0)
                )
                
                # Monta item do ranking
                item_ranking = {
                    "ticker": ticker,
                    "rank": 0,  # SerÃ¡ calculado depois
                    "nota": resultado_analise.get('nota', 5.0),
                    "recomendacao": resultado_analise.get('recomendacao', 'AGUARDAR'),
                    "preco_atual": preco_atual,
                    "preco_teto": resultado_analise.get('preco_teto', preco_atual * 1.05),
                    "upside": resultado_analise.get('upside', 5.0),
                    "score": resultado_analise.get('nota', 5.0),
                    "catalisadores": resultado_analise.get('catalisadores', []),
                    "riscos": resultado_analise.get('riscos', []),
                    "resumo": resultado_analise.get('resumo', ''),
                    "timestamp_analise": datetime.now().isoformat(),
                    "tem_release": True,
                    # EstratÃ©gia
                    "preco_entrada": estrategia.get('entrada', preco_atual),
                    "preco_stop": estrategia.get('stop', preco_atual * 0.95),
                    "preco_alvo": estrategia.get('alvo', preco_atual * 1.05),
                    "risco_retorno": estrategia.get('risco_retorno', 1.0),
                    # Dados CSV
                    "roe": float(dados_csv.get('roe', 0) or 0),
                    "pl": float(dados_csv.get('pl', 0) or 0),
                    "cagr": float(dados_csv.get('cagr', 0) or 0),
                    "setor": dados_csv.get('setor', None)
                }
                
                ranking.append(item_ranking)
                total_analisadas += 1
                
                logger.info(f"âœ… {ticker}: Nota {item_ranking['nota']:.1f} | {item_ranking['recomendacao']}")
                
                # Aguarda 2s entre anÃ¡lises (evita rate limit)
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"âŒ Erro ao analisar {ticker}: {e}")
                total_erros += 1
                # Tenta usar resultado anterior
                if ticker in ranking_anterior:
                    logger.info(f"  ðŸ’¾ Usando resultado anterior do cache")
                    ranking.append(ranking_anterior[ticker])
                    total_fallback += 1
                continue
        
        # 4. Normaliza dados do ranking (garante compatibilidade com cache antigo)
        for item in ranking:
            # Garante que 'nota' existe (pode vir como 'score' do cache antigo)
            if 'nota' not in item and 'score' in item:
                item['nota'] = item['score']
            elif 'nota' not in item:
                item['nota'] = 5.0  # Valor padrÃ£o
            
            # Garante que 'score' existe (para compatibilidade com frontend)
            if 'score' not in item:
                item['score'] = item['nota']
        
        # 5. Ordena ranking por nota (maior primeiro)
        ranking.sort(key=lambda x: x.get('nota', 0), reverse=True)
        
        # 5. Atualiza ranks
        for i, item in enumerate(ranking):
            item['rank'] = i + 1
        
        # 6. Salva ranking
        ranking_data = {
            "versao": "5.0-com-releases",
            "timestamp": datetime.now().isoformat(),
            "total": len(ranking),
            "ranking": ranking,
            "metadados": {
                "total_analisadas": total_analisadas,
                "total_erros": total_erros,
                "total_fallback": total_fallback,
                "com_release": len(ranking),
                "sem_release": 0
            }
        }
        
        os.makedirs(os.path.dirname(self.ranking_file), exist_ok=True)
        with open(self.ranking_file, 'w', encoding='utf-8') as f:
            json.dump(ranking_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"\nâœ… AnÃ¡lise concluÃ­da:")
        logger.info(f"   - Analisadas: {total_analisadas}")
        logger.info(f"   - Erros: {total_erros}")
        logger.info(f"   - Fallback (cache): {total_fallback}")
        logger.info(f"   - Ranking salvo: {self.ranking_file}")
        
        return {
            "sucesso": True,
            "total_analisadas": total_analisadas,
            "total_erros": total_erros,
            "total_fallback": total_fallback,
            "ranking_file": self.ranking_file
        }
    
    async def _analisar_empresa_com_ia(
        self,
        ticker: str,
        dados_csv: Dict,
        dados_brapi: Dict,
        preco_atual: float,
        release_path: str
    ) -> Optional[Dict]:
        """
        Envia release + dados para IA calcular nota
        
        Args:
            dados_brapi: Dados completos da Brapi (cotaÃ§Ã£o + fundamentalistas)
        
        Returns:
            Dict com nota, recomendaÃ§Ã£o, anÃ¡lise
        """
        try:
            from app.services.multi_groq_client import get_multi_groq_client
            
            # 1. Por enquanto, usa placeholder para release (OCR Ã© lento)
            # TODO: Implementar OCR quando sistema estiver estÃ¡vel
            texto_release = f"Release de resultados da empresa {ticker}. Dados financeiros disponÃ­veis no CSV."
            
            logger.info(f"  ðŸ“„ {ticker}: Usando placeholder para release (OCR desabilitado temporariamente)")
            
            # 2. Monta prompt para IA (agora com dados fundamentalistas)
            prompt = self._montar_prompt_analise(
                ticker=ticker,
                dados_csv=dados_csv,
                dados_brapi=dados_brapi,
                preco_atual=preco_atual,
                texto_release=texto_release[:8000]  # Limita tamanho
            )
            
            # 3. Envia para IA
            ai_client = get_multi_groq_client()
            resposta_dict = await ai_client.executar_prompt(
                prompt=prompt,
                task_type="analise_profunda",
                usar_contexto=False
            )
            
            # Extrai texto da resposta
            if isinstance(resposta_dict, dict):
                resposta = resposta_dict.get('resposta', '')
                if not resposta:
                    # Tenta outras chaves do dict
                    resposta = resposta_dict.get('texto', '') or resposta_dict.get('content', '') or str(resposta_dict)
            else:
                resposta = str(resposta_dict)
            
            logger.info(f"  ðŸ¤– {ticker}: Resposta IA ({len(resposta)} chars)")
            
            if not resposta or len(resposta) < 50:
                logger.error(f"âŒ {ticker}: IA nÃ£o respondeu adequadamente (resposta muito curta)")
                logger.debug(f"Resposta recebida: {resposta_dict}")
                return None
            
            # 4. Parse da resposta
            resultado = self._parse_resposta_ia(resposta, preco_atual)
            
            return resultado
            
        except Exception as e:
            logger.error(f"âŒ Erro na anÃ¡lise com IA de {ticker}: {e}")
            return None
    
    def _montar_prompt_analise(
        self,
        ticker: str,
        dados_csv: Dict,
        dados_brapi: Dict,
        preco_atual: float,
        texto_release: str
    ) -> str:
        """
        Monta prompt MELHORADO focado em VALORIZAÃ‡ÃƒO DE 5% AO MÃŠS
        
        Baseado no prompt que funcionou bem: anÃ¡lise profunda com foco em
        catalisadores reais de valorizaÃ§Ã£o, nÃ£o apenas fundamentos genÃ©ricos
        """
        
        roe = dados_csv.get('roe', 0) or 0
        pl = dados_csv.get('pl', 0) or 0
        cagr = dados_csv.get('cagr', 0) or 0
        setor = dados_csv.get('setor', 'N/A')
        
        # Extrai dados fundamentalistas da Brapi
        financial_data = dados_brapi.get('financialData', {})
        key_stats = dados_brapi.get('defaultKeyStatistics', {})
        summary = dados_brapi.get('summaryProfile', {})
        
        # Dados adicionais (com proteÃ§Ã£o contra None)
        market_cap = dados_brapi.get('marketCap') or 0
        ebitda = financial_data.get('ebitda') or 0
        debt_to_equity = financial_data.get('debtToEquity') or 0
        roe_brapi = financial_data.get('returnOnEquity') or 0
        roa = financial_data.get('returnOnAssets') or 0
        margem_liquida = financial_data.get('profitMargins') or 0
        margem_ebitda = financial_data.get('ebitdaMargins') or 0
        receita_total = financial_data.get('totalRevenue') or 0
        divida_total = financial_data.get('totalDebt') or 0
        caixa_total = financial_data.get('totalCash') or 0
        fluxo_caixa_livre = financial_data.get('freeCashflow') or 0
        price_to_book = key_stats.get('priceToBook') or 0
        ev_ebitda = key_stats.get('enterpriseToEbitda') or 0
        industry = summary.get('industry') or 'N/A'
        
        # FormataÃ§Ã£o segura
        market_cap_bi = market_cap / 1_000_000_000 if market_cap else 0
        ebitda_mi = ebitda / 1_000_000 if ebitda else 0
        receita_bi = receita_total / 1_000_000_000 if receita_total else 0
        fcf_mi = fluxo_caixa_livre / 1_000_000 if fluxo_caixa_livre else 0
        caixa_mi = caixa_total / 1_000_000 if caixa_total else 0
        
        prompt = f"""Analista: identifique ações 5%/mês.

{ticker}|{setor}|R${preco_atual:.2f} ROE:{roe_brapi*100:.1f}% P/L:{pl:.1f} Margem:{margem_liquida*100:.1f}% Div:{debt_to_equity:.1f}%

RELEASE:{texto_release[:2500]}

CATALISADORES(40pts)-Sem concretos máx 6.0:
✅Concreto:contrato(cliente,valor),expansão física,produto(nome,data),mercado(país,quando)
❌Vago:"expansão","melhoria","novos produtos"

MOMENTUM(25pts):Setor aquecido?Gatilho iminente?Preço entrada?
SAÚDE(20pts):Margens↑?Caixa ok?Dívida ok?
GESTÃO(10pts)|PREÇO(5pts)

NOTAS:
9-10:3+concretos+timing perfeito(50%+)
7.5-8.9:2+concretos+bom(30-50%)
6-7.4:1-2concretos(20-30%)
4-5.9:vagos(10-20%)
0-3.9:sem

JSON:{{"nota":8.5,"recomendacao":"COMPRA FORTE","preco_teto":65.0,"upside":18.0,"catalisadores":["Específico 1(o quê,quando,quanto)","2","3"],"riscos":["Concreto 1","2","3"],"resumo":"2 linhas"}}"""
        
        return prompt
    
    def _parse_resposta_ia(self, resposta: str, preco_atual: float) -> Dict:
        """Parse da resposta da IA"""
        try:
            # Tenta extrair JSON
            import re
            json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
            if json_match:
                dados = json.loads(json_match.group())
                return dados
            
            # Fallback: valores padrÃ£o
            return {
                "nota": 5.0,
                "recomendacao": "AGUARDAR",
                "preco_teto": preco_atual * 1.05,
                "upside": 5.0,
                "catalisadores": [],
                "riscos": [],
                "resumo": "AnÃ¡lise nÃ£o disponÃ­vel"
            }
            
        except Exception as e:
            logger.error(f"Erro ao fazer parse da resposta: {e}")
            return {
                "nota": 5.0,
                "recomendacao": "AGUARDAR",
                "preco_teto": preco_atual * 1.05,
                "upside": 5.0,
                "catalisadores": [],
                "riscos": [],
                "resumo": "Erro ao processar anÃ¡lise"
            }
    
    async def _calcular_estrategia(
        self,
        ticker: str,
        preco_atual: float,
        preco_teto: float,
        nota: float
    ) -> Dict:
        """Calcula estratÃ©gia de entrada/stop/alvo"""
        
        # Entrada: 2% abaixo do preÃ§o atual
        entrada = preco_atual * 0.98
        
        # Stop: baseado na nota (quanto menor a nota, stop mais apertado)
        if nota >= 8:
            stop = entrada * 0.92  # 8% de stop
        elif nota >= 6:
            stop = entrada * 0.95  # 5% de stop
        else:
            stop = entrada * 0.97  # 3% de stop
        
        # Alvo: preÃ§o teto
        alvo = preco_teto
        
        # Risco/Retorno
        risco = entrada - stop
        retorno = alvo - entrada
        risco_retorno = retorno / risco if risco > 0 else 0
        
        return {
            "entrada": round(entrada, 2),
            "stop": round(stop, 2),
            "alvo": round(alvo, 2),
            "risco_retorno": round(risco_retorno, 2)
        }


# Singleton
_analise_com_release_service: Optional[AnaliseComReleaseService] = None


def get_analise_com_release_service() -> AnaliseComReleaseService:
    """Retorna instÃ¢ncia singleton"""
    global _analise_com_release_service
    
    if _analise_com_release_service is None:
        _analise_com_release_service = AnaliseComReleaseService()
    
    return _analise_com_release_service
