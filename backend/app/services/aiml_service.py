"""
AIML API Service - Multi-Model AI Platform
Usa Gemini 2.0 Flash Thinking + Claude 3.5 Sonnet
"""
import aiohttp
import os
from typing import Dict, List, Optional
from datetime import datetime

class AIMLService:
    """Serviço para usar múltiplas IAs via AIML API"""
    
    def __init__(self):
        self.api_key = os.getenv("AIML_API_KEY")
        self.base_url = "https://api.aimlapi.com/v1"
        
        # Modelos disponíveis na AIML API
        self.models = {
            "gemini_pro": "google/gemini-2.5-pro",  # Gemini 2.5 Pro (melhor)
            "gemini_flash": "google/gemini-2.5-flash",  # Gemini 2.5 Flash (rápido)
            "claude_sonnet": "anthropic/claude-sonnet-4-6",  # Claude Sonnet 4.6
            "deepseek_reasoner": "deepseek/deepseek-reasoner",  # DeepSeek R1 (raciocínio)
            "qwen_max": "alibaba/qwen-max",  # Qwen Max (alternativa)
        }
        
        print(f"✓ AIML API configurada com {len(self.models)} modelos")
    
    async def _call_model(
        self, 
        model: str, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000
    ) -> Dict:
        """Chama um modelo específico via AIML API"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Monta mensagens
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        
                        return {
                            "success": True,
                            "content": content,
                            "model": model,
                            "tokens": data.get("usage", {})
                        }
                    else:
                        error_text = await response.text()
                        print(f"Erro AIML API ({response.status}): {error_text}")
                        return {"success": False, "error": error_text}
        
        except Exception as e:
            print(f"Erro ao chamar AIML API: {e}")
            return {"success": False, "error": str(e)}
    
    async def gemini_thinking_analise_mercado(
        self, 
        acoes_candidatas: List[Dict],
        contexto_macro: Dict
    ) -> Dict:
        """
        FASE 1: Gemini 2.5 Pro
        Análise profunda do mercado e seleção das melhores ações
        """
        
        system_prompt = """Você é um analista quantitativo elite especializado em ações brasileiras.
Sua missão: analisar o contexto macroeconômico e selecionar as 15 MELHORES ações para investimento.

FILOSOFIA DE INVESTIMENTO:
- Meta: 5% ao mês através de valorização (não dividendos)
- ROE > 15% (eficiência operacional)
- CAGR > 12% (crescimento consistente)
- P/L < 15 (preço justo)

ANÁLISE REQUERIDA:
1. Contexto macro atual (juros, inflação, câmbio)
2. Setores em aceleração
3. Empresas com fundamentos sólidos
4. Momento de entrada (não comprar no topo)
5. Catalisadores de curto prazo

FORMATO DE RESPOSTA (JSON):
{
    "analise_macro": "análise do cenário atual",
    "setores_favoritos": ["setor1", "setor2"],
    "top_15_acoes": [
        {
            "ticker": "PRIO3",
            "score": 9.5,
            "razao": "por que essa ação",
            "catalisadores": ["cat1", "cat2"],
            "risco": "baixo/médio/alto"
        }
    ],
    "alertas": ["alerta1", "alerta2"]
}"""

        # Prepara dados das ações
        acoes_texto = "\n".join([
            f"- {a['ticker']}: ROE={a['roe']}%, CAGR={a['cagr']}%, P/L={a['pl']}, Setor={a['setor']}"
            for a in acoes_candidatas
        ])
        
        prompt = f"""ANÁLISE DE MERCADO - {datetime.now().strftime('%d/%m/%Y')}

CONTEXTO MACROECONÔMICO:
{contexto_macro}

AÇÕES CANDIDATAS ({len(acoes_candidatas)} empresas):
{acoes_texto}

TAREFA:
Use seu raciocínio profundo para:
1. Analisar o cenário macro atual
2. Identificar setores com melhor momento
3. Selecionar as 15 MELHORES ações
4. Justificar cada escolha
5. Alertar sobre riscos

Pense como um gestor de fundos que precisa entregar 5% ao mês.
Seja criterioso e evite armadilhas (ações no topo, setores em queda, etc.)."""

        print("\n[FASE 1] Gemini 2.5 Pro - Análise de Mercado...")
        result = await self._call_model(
            model=self.models["gemini_pro"],
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.3,  # Mais conservador
            max_tokens=4000
        )
        
        if result["success"]:
            print(f"✓ Análise concluída ({result['tokens'].get('total_tokens', 0)} tokens)")
        
        return result
    
    async def claude_analise_profunda_acao(
        self,
        ticker: str,
        dados_fundamentalistas: Dict,
        preco_atual: float,
        relatorio_trimestral: Optional[str] = None
    ) -> Dict:
        """
        FASE 2: Claude Sonnet 4.6
        Análise profunda de uma ação específica
        Inclui análise do relatório trimestral mais recente
        """
        
        system_prompt = """Você é um analista fundamentalista especializado em análise de balanços.
Sua missão: fazer análise CIRÚRGICA de uma ação específica.

ANÁLISE REQUERIDA:
1. Fundamentos (ROE, CAGR, P/L, Dívida)
2. Relatório trimestral (receita, lucro, margens)
3. Qualidade dos resultados
4. Preço justo (valuation)
5. Recomendação final

FORMATO DE RESPOSTA (JSON):
{
    "ticker": "PRIO3",
    "analise_fundamentalista": {
        "qualidade_roe": "análise do ROE",
        "crescimento": "análise do CAGR",
        "valuation": "análise do P/L",
        "endividamento": "análise da dívida"
    },
    "analise_trimestral": {
        "receita": "crescimento/queda",
        "lucro": "qualidade do lucro",
        "margens": "evolução das margens",
        "destaques": ["ponto1", "ponto2"]
    },
    "preco_justo": 45.50,
    "preco_teto": 52.00,
    "upside": 15.5,
    "recomendacao": "COMPRA FORTE/COMPRA/MONITORAR/EVITAR",
    "confianca": "ALTA/MÉDIA/BAIXA",
    "tempo_estimado_dias": 90,
    "riscos": ["risco1", "risco2"]
}"""

        # Monta prompt com dados
        prompt = f"""ANÁLISE PROFUNDA - {ticker}

DADOS FUNDAMENTALISTAS:
- ROE: {dados_fundamentalistas.get('roe')}%
- CAGR: {dados_fundamentalistas.get('cagr')}%
- P/L: {dados_fundamentalistas.get('pl')}
- Dívida/Patrimônio: {dados_fundamentalistas.get('divida')}
- Setor: {dados_fundamentalistas.get('setor')}
- Preço Atual: R$ {preco_atual:.2f}

RELATÓRIO TRIMESTRAL (Q4 2025 - Mais Recente):
{relatorio_trimestral if relatorio_trimestral else "Não disponível - use apenas fundamentos"}

TAREFA:
Faça uma análise CIRÚRGICA desta ação:
1. Os fundamentos são realmente sólidos?
2. O relatório trimestral confirma a qualidade?
3. O preço atual está justo?
4. Qual o preço teto realista?
5. Vale a pena comprar AGORA?

Seja rigoroso. Prefira dizer "EVITAR" do que recomendar uma ação duvidosa."""

        print(f"\n[FASE 2] Claude Sonnet 4.6 - Análise de {ticker}...")
        result = await self._call_model(
            model=self.models["claude_sonnet"],
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.2,  # Muito conservador
            max_tokens=3000
        )
        
        if result["success"]:
            print(f"✓ Análise de {ticker} concluída")
        
        return result
    
    async def analise_completa_portfolio(
        self,
        acoes_candidatas: List[Dict],
        contexto_macro: Dict,
        precos_atuais: Dict[str, float],
        relatorios: Dict[str, str] = None
    ) -> Dict:
        """
        FLUXO COMPLETO: Gemini 2.5 Pro + Claude Sonnet 4.6
        
        1. Gemini analisa mercado e seleciona top 15
        2. Claude analisa cada uma das 15 em profundidade
        3. Retorna portfolio final com análises completas
        """
        
        print("\n" + "="*60)
        print("ANÁLISE MULTI-IA - AIML API")
        print("="*60)
        
        # FASE 1: Gemini Thinking - Seleção
        fase1 = await self.gemini_thinking_analise_mercado(
            acoes_candidatas=acoes_candidatas,
            contexto_macro=contexto_macro
        )
        
        if not fase1["success"]:
            return {"success": False, "error": "Falha na Fase 1"}
        
        # Extrai top 15 da análise do Gemini
        import json
        try:
            # Tenta extrair JSON da resposta
            content = fase1["content"]
            # Remove markdown se houver
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            analise_gemini = json.loads(content.strip())
            top_15_tickers = [a["ticker"] for a in analise_gemini.get("top_15_acoes", [])]
        except:
            # Fallback: usa as primeiras 15
            print("⚠ Não foi possível parsear JSON, usando fallback")
            top_15_tickers = [a["ticker"] for a in acoes_candidatas[:15]]
            analise_gemini = {"analise_macro": fase1["content"]}
        
        print(f"\n✓ Fase 1 concluída: {len(top_15_tickers)} ações selecionadas")
        
        # FASE 2: Claude Sonnet - Análise Profunda
        analises_detalhadas = []
        
        for ticker in top_15_tickers[:15]:  # Garante máximo 15
            # Busca dados da ação
            acao_data = next((a for a in acoes_candidatas if a["ticker"] == ticker), None)
            if not acao_data:
                continue
            
            preco_atual = precos_atuais.get(ticker, 0)
            if preco_atual == 0:
                continue
            
            relatorio = relatorios.get(ticker) if relatorios else None
            
            # Análise profunda com Claude
            fase2 = await self.claude_analise_profunda_acao(
                ticker=ticker,
                dados_fundamentalistas=acao_data,
                preco_atual=preco_atual,
                relatorio_trimestral=relatorio
            )
            
            if fase2["success"]:
                analises_detalhadas.append({
                    "ticker": ticker,
                    "analise_claude": fase2["content"],
                    "tokens_usados": fase2["tokens"]
                })
            
            # Delay para não sobrecarregar API
            import asyncio
            await asyncio.sleep(1)
        
        print(f"\n✓ Fase 2 concluída: {len(analises_detalhadas)} análises detalhadas")
        
        return {
            "success": True,
            "fase1_gemini": {
                "analise_macro": analise_gemini.get("analise_macro"),
                "setores_favoritos": analise_gemini.get("setores_favoritos", []),
                "top_15": analise_gemini.get("top_15_acoes", []),
                "alertas": analise_gemini.get("alertas", [])
            },
            "fase2_claude": analises_detalhadas,
            "timestamp": datetime.now().isoformat()
        }
    
    async def buscar_relatorio_trimestral(self, ticker: str) -> Optional[str]:
        """
        Busca relatório trimestral mais recente (Q4 2025)
        
        Estratégias:
        1. Verifica se existe PDF local em data/relatorios/{ticker}_Q4_2025.pdf
        2. Se não existir, retorna placeholder
        
        TODO: Implementar download automático de sites de RI
        """
        import os
        
        # Verifica se existe PDF local
        pdf_path = f"data/relatorios/{ticker}_Q4_2025.pdf"
        
        if os.path.exists(pdf_path):
            # Usa Mistral OCR para extrair dados
            from app.services.mistral_ocr_service import MistralOCRService
            
            mistral_ocr = MistralOCRService()
            resultado = await mistral_ocr.extrair_dados_relatorio_trimestral(pdf_path, ticker)
            
            if resultado["success"]:
                dados = resultado["dados"]
                
                # Formata dados para texto legível
                texto = f"""RELATÓRIO TRIMESTRAL {dados.get('trimestre', 'Q4 2025')} - {ticker}

DADOS FINANCEIROS:
- Receita Líquida: R$ {dados.get('receita_liquida', 0):.1f}M
- Lucro Líquido: R$ {dados.get('lucro_liquido', 0):.1f}M
- EBITDA: R$ {dados.get('ebitda', 0):.1f}M
- Margem Líquida: {dados.get('margem_liquida', 0):.1f}%
- Margem EBITDA: {dados.get('margem_ebitda', 0):.1f}%

CRESCIMENTO:
- Receita YoY: {dados.get('crescimento_receita_yoy', 0):.1f}%
- Lucro YoY: {dados.get('crescimento_lucro_yoy', 0):.1f}%

DESTAQUES:
{chr(10).join(['- ' + d for d in dados.get('destaques', [])])}

RISCOS:
{chr(10).join(['- ' + r for r in dados.get('riscos', [])])}

GUIDANCE: {dados.get('guidance', 'Não informado')}

Fonte: Mistral AI OCR"""
                
                return texto
        
        # Fallback: placeholder
        return f"Relatório Q4 2025 de {ticker} não disponível localmente. Use apenas fundamentos para análise."
