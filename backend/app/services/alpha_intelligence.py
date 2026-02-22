"""
Alpha Intelligence Service
Implementa os 6 prompts do sistema Alpha Terminal
"""
import google.generativeai as genai
import os
from typing import List, Dict
from datetime import datetime

class AlphaIntelligence:
    """Serviço de inteligência de mercado usando Gemini"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def prompt_1_radar_oportunidades(self) -> Dict:
        """PROMPT 1 — Radar de Oportunidades"""
        prompt = """Você é um analista especializado em identificar movimentos de valorização de preço antes da manada. 

Analise o cenário macroeconômico atual do Brasil (Fevereiro 2026) e responda em formato JSON:

{
  "setores_aceleracao": [
    {
      "setor": "nome do setor",
      "catalisador": "descrição do catalisador claro nos próximos 3-12 meses",
      "estagio_ciclo": "começo|meio|fim",
      "potencial_upside": "percentual estimado"
    }
  ],
  "movimentos_silenciosos": [
    {
      "ativo_tipo": "setor/commodity/moeda",
      "nome": "nome específico",
      "similaridade": "descrição de como é similar a Nvidia/Ouro/Bitcoin antes de explodir",
      "radar_varejo": "baixo|medio|alto"
    }
  ]
}

IMPORTANTE: 
- NÃO traga o que já virou manchete
- Foque em movimentos SILENCIOSOS
- Identifique o estágio do ciclo"""

        try:
            response = self.model.generate_content(prompt)
            import json
            return json.loads(self._clean_json_response(response.text))
        except Exception as e:
            return {"error": str(e), "setores_aceleracao": [], "movimentos_silenciosos": []}
    
    async def prompt_2_triagem_fundamentalista_v2(self, stocks_data: List[Dict], precos_reais: Dict[str, float]) -> List[Dict]:
        """
        PROMPT 2 REFORMULADO - Triagem Fundamentalista com Preços Reais
        Análise mais profunda considerando preço atual de mercado
        """
        # Enriquece dados com preços reais
        stocks_enriched = []
        for stock in stocks_data[:20]:
            ticker = stock.get("ticker")
            preco_real = precos_reais.get(ticker, 0)
            if preco_real > 0:
                stock["preco_atual_mercado"] = preco_real
                stock["pl_real"] = preco_real / (stock.get("lucro_por_acao", 1) or 1)
                stocks_enriched.append(stock)
        
        stocks_json = str(stocks_enriched)
        
        prompt = f"""Você é um analista quantitativo especializado em encontrar ações com potencial de 5% ao mês.

DATA ATUAL: {datetime.now().strftime('%d/%m/%Y')}

DADOS DAS AÇÕES (COM PREÇOS REAIS DE MERCADO):
{stocks_json}

MISSÃO:
Analise CRITICAMENTE cada ação e identifique as 10 MELHORES para valorização de preço nos próximos 90 dias.

CRITÉRIOS DE ANÁLISE:
1. **Eficiência Operacional**: ROE > 15% (quanto maior, melhor)
2. **Crescimento**: CAGR > 12% (crescimento consistente)
3. **Valuation**: P/L < 15 (não pagar caro)
4. **Preço Atual**: Considere se está em ponto de entrada favorável
5. **Momentum**: Evite ações que já subiram muito recentemente

RETORNE JSON:
{{
  "ranking": [
    {{
      "ticker": "TICKER",
      "score_valorizacao": 9.5,
      "preco_entrada_ideal": 45.50,
      "preco_teto_90d": 52.00,
      "upside_esperado_pct": 14.3,
      "catalisador_principal": "O que pode fazer o preço subir",
      "risco_principal": "Principal risco identificado",
      "confianca": "alta|media|baixa"
    }}
  ]
}}

IMPORTANTE:
- Use os PREÇOS REAIS fornecidos
- Seja CONSERVADOR nas estimativas
- Elimine ações com sinais de alerta
- Priorize empresas com fundamentos sólidos"""

        try:
            response = self.model.generate_content(prompt)
            import json
            result = json.loads(self._clean_json_response(response.text))
            return result.get("ranking", [])
        except Exception as e:
            print(f"Erro no Prompt 2: {e}")
            return []
    
    async def prompt_3_analise_comparativa(self, relatorios: List[Dict]) -> Dict:
        """PROMPT 3 — Análise Comparativa Profunda com Relatórios de RI"""
        relatorios_text = ""
        for rel in relatorios[:5]:  # Limita a 5 para não estourar token
            relatorios_text += f"\n\n=== {rel['ticker']} ===\n"
            relatorios_text += f"Trimestre: {rel.get('trimestre', 'N/A')}\n"
            relatorios_text += f"Resumo: {rel.get('resumo', 'Não disponível')}\n"
        
        prompt = f"""Você é um analista fundamentalista especializado em encontrar empresas com potencial de valorização de 5% ao mês.

RELATÓRIOS DE RESULTADOS:
{relatorios_text}

ANÁLISE REQUERIDA:
1. Compare as empresas lado a lado
2. Identifique qual tem maior potencial de VALORIZAÇÃO DE PREÇO
3. Foque em: crescimento de receita, margem operacional, geração de caixa, guidance

Retorne JSON:
{{
  "ranking_final": [
    {{
      "ticker": "TICKER",
      "score_final": 9.5,
      "por_que_venceu": "explicação objetiva do diferencial",
      "catalisador_trimestre": "o que pode fazer o preço subir nos próximos 90 dias",
      "risco_principal": "principal risco identificado",
      "preco_justo_estimado": 50.00
    }}
  ],
  "eliminadas": [
    {{
      "ticker": "TICKER",
      "motivo_eliminacao": "razão clara"
    }}
  ]
}}

IMPORTANTE: Seja CRÍTICO. Elimine empresas com sinais de alerta."""

        try:
            response = self.model.generate_content(prompt)
            import json
            return json.loads(self._clean_json_response(response.text))
        except Exception as e:
            return {"error": str(e), "ranking_final": [], "eliminadas": []}
    
    async def buscar_relatorios_ri(self, ticker: str) -> Dict:
        """Busca relatórios de RI da empresa (simulado por enquanto)"""
        # TODO: Implementar scraping real dos sites de RI
        # Por enquanto, retorna estrutura simulada
        return {
            "ticker": ticker,
            "trimestre": "3T 2025",
            "resumo": f"Relatório de resultados {ticker} - 3T 2025. Aguardando implementação de scraping.",
            "url": f"https://ri.{ticker.lower()}.com.br/resultados",
            "data_divulgacao": "2025-11-15"
        }
    
    async def prompt_6_verificacao_anti_manada_v2(self, ticker: str, preco_atual: float, variacao_30d: float = 0) -> Dict:
        """
        PROMPT 6 REFORMULADO - Verificação Anti-Manada com Dados Reais
        Análise mais precisa considerando preço e momentum
        """
        prompt = f"""Você é um especialista em psicologia de mercado e timing de entrada.

AÇÃO: {ticker}
PREÇO ATUAL: R$ {preco_atual:.2f}
VARIAÇÃO 30 DIAS: {variacao_30d:+.2f}%
DATA: {datetime.now().strftime('%d/%m/%Y')}

MISSÃO:
Determine se AGORA é um bom momento para entrar em {ticker} ou se devemos AGUARDAR.

ANÁLISE REQUERIDA:
1. **Exposição na Mídia**: Está sendo muito comentado? (baixa/media/alta)
2. **Momentum Recente**: Subiu muito nos últimos 30 dias? (se > 20%, ALERTA)
3. **Fundamento vs Narrativa**: O preço reflete fundamentos ou apenas hype?
4. **Timing**: Estamos comprando no topo ou em ponto de entrada?

RETORNE JSON:
{{
  "exposicao_midia": "baixa|media|alta",
  "momentum_status": "saudavel|aquecido|sobrecomprado",
  "fundamento_vs_narrativa": "fundamento_solido|narrativa_predomina|equilibrado",
  "veredito": "ENTRAR_AGORA|ESPERAR_CORRECAO|JANELA_FECHOU",
  "justificativa": "Explicação clara e direta",
  "preco_entrada_ideal": 45.50,
  "confianca_analise": "alta|media|baixa"
}}

REGRAS:
- Se variação 30d > 25%: Provavelmente "ESPERAR_CORRECAO"
- Se exposição mídia = alta: Cuidado com "JANELA_FECHOU"
- Seja CONSERVADOR: melhor perder oportunidade que entrar no topo"""

        try:
            response = self.model.generate_content(prompt)
            import json
            return json.loads(self._clean_json_response(response.text))
        except Exception as e:
            print(f"Erro no Prompt 6: {e}")
            return {
                "veredito": "ERRO",
                "justificativa": f"Erro na análise: {str(e)}",
                "confianca_analise": "baixa"
            }
    
    async def gerar_alertas_inteligentes(self, carteira: List[Dict], precos_atuais: Dict[str, float]) -> List[Dict]:
        """
        NOVO - Sistema de Alertas Inteligentes
        Monitora carteira e gera alertas acionáveis
        """
        alertas = []
        
        for posicao in carteira:
            ticker = posicao.get("ticker")
            preco_entrada = posicao.get("preco_entrada", 0)
            preco_teto = posicao.get("preco_teto", 0)
            preco_atual = precos_atuais.get(ticker, 0)
            
            if preco_atual == 0:
                continue
            
            # Calcula métricas
            variacao_pct = ((preco_atual / preco_entrada) - 1) * 100 if preco_entrada > 0 else 0
            distancia_teto = ((preco_teto / preco_atual) - 1) * 100 if preco_atual > 0 else 0
            
            # ALERTA 1: Atingiu preço teto (realizar lucros)
            if preco_atual >= preco_teto * 0.95:
                alertas.append({
                    "tipo": "REALIZAR_LUCROS",
                    "ticker": ticker,
                    "prioridade": "ALTA",
                    "mensagem": f"{ticker} atingiu {(preco_atual/preco_teto)*100:.1f}% do preço teto",
                    "acao_recomendada": f"Vender {ticker} a R$ {preco_atual:.2f}",
                    "ganho_potencial": f"+{variacao_pct:.1f}%"
                })
            
            # ALERTA 2: Oportunidade de compra (abaixo do preço ideal)
            elif preco_atual <= preco_entrada * 0.90:
                alertas.append({
                    "tipo": "OPORTUNIDADE_COMPRA",
                    "ticker": ticker,
                    "prioridade": "MEDIA",
                    "mensagem": f"{ticker} caiu {abs(variacao_pct):.1f}% - oportunidade de média",
                    "acao_recomendada": f"Considerar compra adicional a R$ {preco_atual:.2f}",
                    "upside_potencial": f"+{distancia_teto:.1f}%"
                })
            
            # ALERTA 3: Stop loss (queda significativa)
            elif variacao_pct <= -15:
                alertas.append({
                    "tipo": "STOP_LOSS",
                    "ticker": ticker,
                    "prioridade": "URGENTE",
                    "mensagem": f"{ticker} caiu {abs(variacao_pct):.1f}% - revisar tese",
                    "acao_recomendada": f"Avaliar saída ou aguardar recuperação",
                    "perda_atual": f"{variacao_pct:.1f}%"
                })
        
        return alertas
    
    async def analisar_contexto_macro_atual(self) -> Dict:
        """
        NOVO - Análise de Contexto Macro em Tempo Real
        Identifica mudanças que podem afetar a carteira
        """
        prompt = f"""Você é um analista macroeconômico especializado no mercado brasileiro.

DATA: {datetime.now().strftime('%d/%m/%Y')}

MISSÃO:
Analise o contexto macroeconômico ATUAL do Brasil e identifique fatores que podem impactar investimentos em ações.

RETORNE JSON:
{{
  "cenario_geral": "favoravel|neutro|desfavoravel",
  "fatores_positivos": ["fator 1", "fator 2"],
  "fatores_negativos": ["fator 1", "fator 2"],
  "setores_favorecidos": ["setor 1", "setor 2"],
  "setores_desfavorecidos": ["setor 1", "setor 2"],
  "recomendacao_posicionamento": "agressivo|moderado|defensivo",
  "alertas_importantes": [
    {{
      "tipo": "JUROS|INFLACAO|CAMBIO|POLITICA",
      "descricao": "Descrição do alerta",
      "impacto": "alto|medio|baixo"
    }}
  ]
}}

Seja OBJETIVO e ATUAL."""

        try:
            response = self.model.generate_content(prompt)
            import json
            return json.loads(self._clean_json_response(response.text))
        except Exception as e:
            print(f"Erro na análise macro: {e}")
            return {
                "cenario_geral": "neutro",
                "fatores_positivos": [],
                "fatores_negativos": [],
                "alertas_importantes": []
            }
        """Remove markdown do JSON"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
