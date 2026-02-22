"""
Serviço de Dados Fundamentalistas - Sistema Híbrido
Combina múltiplas fontes para garantir dados de qualidade
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from app.services.multi_groq_client import get_multi_groq_client
from app.services.yfinance_client import get_yfinance_client


class DadosFundamentalistasService:
    """
    Sistema híbrido que combina:
    1. yfinance (dados financeiros históricos)
    2. Brapi (preços e indicadores B3)
    3. IA (análise de notícias e contexto)
    
    Objetivo: Substituir releases com dados equivalentes ou melhores
    """
    
    def __init__(self):
        self.ai_client = get_multi_groq_client()
        self.yfinance_client = get_yfinance_client()
        print("✓ Dados Fundamentalistas Service: Sistema Híbrido + yfinance otimizado")
    
    async def obter_dados_completos(self, ticker: str, nome_empresa: str) -> Dict:
        """
        Obtém dados fundamentalistas completos de múltiplas fontes
        
        OTIMIZADO: Reduz chamadas de IA para economizar rate limit
        
        FONTES:
        1. yfinance: Dados financeiros (receita, lucro, margens, dívida)
        2. IA: APENAS se yfinance não retornar dados suficientes
        
        Returns:
            Dict com todos os dados estruturados
        """
        
        print(f"📊 [{ticker}] Coletando dados...")
        
        dados = {
            "ticker": ticker,
            "nome": nome_empresa,
            "timestamp": datetime.now(),
            "fontes_usadas": []
        }
        
        # FONTE 1: CSV (dados básicos - SEMPRE disponível)
        # yfinance DESABILITADO devido a rate limit (429)
        # Sistema usa apenas dados do CSV por enquanto
        dados["financeiro"] = {
            "roe": None,  # Será preenchido do CSV
            "pl": None,   # Será preenchido do CSV
            "margem_liquida": None,
            "divida_patrimonio": None,
            "setor": "N/A"
        }
        dados["fontes_usadas"].append("csv_apenas")
        print(f"   ✓ Usando dados do CSV (yfinance desabilitado)")
        
        # Gera resumo estruturado
        dados["resumo_estruturado"] = self._gerar_resumo_estruturado(dados)
        
        return dados
    
    async def _obter_dados_yfinance(self, ticker: str) -> Optional[Dict]:
        """
        DESABILITADO: yfinance está bloqueado (429 Too Many Requests)
        
        Sistema agora usa apenas dados do CSV
        """
        print(f"      yfinance DESABILITADO (rate limit)")
        return None
    
    def _extrair_receita_trimestral(self, financials) -> List[Dict]:
        """Extrai receita dos últimos 4 trimestres"""
        try:
            if financials is None or financials.empty:
                return []
            
            receitas = []
            if 'Total Revenue' in financials.index:
                for col in financials.columns[:4]:  # Últimos 4 trimestres
                    valor = financials.loc['Total Revenue', col]
                    receitas.append({
                        "trimestre": col.strftime("%Y-Q%q") if hasattr(col, 'strftime') else str(col),
                        "valor": float(valor) if valor else 0
                    })
            
            return receitas
        except:
            return []
    
    def _extrair_lucro_trimestral(self, financials) -> List[Dict]:
        """Extrai lucro líquido dos últimos 4 trimestres"""
        try:
            if financials is None or financials.empty:
                return []
            
            lucros = []
            if 'Net Income' in financials.index:
                for col in financials.columns[:4]:
                    valor = financials.loc['Net Income', col]
                    lucros.append({
                        "trimestre": col.strftime("%Y-Q%q") if hasattr(col, 'strftime') else str(col),
                        "valor": float(valor) if valor else 0
                    })
            
            return lucros
        except:
            return []
    
    async def _obter_analise_ia(self, ticker: str, nome_empresa: str, dados_existentes: Dict) -> Optional[Dict]:
        """
        Usa IA para analisar contexto e notícias recentes
        
        FOCO:
        - Notícias dos últimos 3 meses
        - Contexto setorial
        - Catalisadores identificados
        - Riscos específicos
        """
        
        # Prepara contexto com dados já obtidos
        contexto_financeiro = ""
        if "financeiro" in dados_existentes:
            fin = dados_existentes["financeiro"]
            contexto_financeiro = f"""
DADOS FINANCEIROS DISPONÍVEIS:
- ROE: {fin.get('roe', 'N/A')}%
- Margem Líquida: {fin.get('margem_liquida', 'N/A')}%
- P/L: {fin.get('pl', 'N/A')}
- Dívida/Patrimônio: {fin.get('divida_patrimonio', 'N/A')}
- Setor: {fin.get('setor', 'N/A')}
"""
        
        prompt = f"""
Você é um analista fundamentalista especializado em ações brasileiras.

EMPRESA: {nome_empresa} ({ticker})
{contexto_financeiro}

TAREFA: Analise esta empresa e forneça informações ATUALIZADAS e ESPECÍFICAS.

IMPORTANTE: Seja ESPECÍFICO e FACTUAL. Não use informações genéricas.

Analise:

1. **NOTÍCIAS RECENTES** (últimos 3 meses):
   - Principais eventos corporativos
   - Anúncios importantes
   - Mudanças na gestão
   - Novos contratos/projetos

2. **CONTEXTO SETORIAL**:
   - Como está o setor desta empresa?
   - Tendências macroeconômicas afetando o setor
   - Posição competitiva da empresa

3. **CATALISADORES** (próximos 6-12 meses):
   - O que pode fazer a ação subir?
   - Eventos futuros importantes
   - Expansões, novos produtos, etc.

4. **RISCOS ESPECÍFICOS**:
   - Riscos reais desta empresa (não genéricos)
   - O que pode derrubar o preço?

5. **QUALIDADE DA GESTÃO**:
   - Histórico de execução
   - Transparência com acionistas
   - Alocação de capital

Retorne APENAS JSON:
{{
    "noticias_recentes": [
        {{"data": "2025-11", "evento": "...", "impacto": "positivo/negativo/neutro"}}
    ],
    "contexto_setorial": {{
        "situacao": "...",
        "tendencias": ["..."],
        "posicao_competitiva": "..."
    }},
    "catalisadores": [
        {{"descricao": "...", "prazo": "curto/médio/longo", "probabilidade": "alta/média/baixa"}}
    ],
    "riscos": [
        {{"descricao": "...", "severidade": "alta/média/baixa"}}
    ],
    "qualidade_gestao": {{
        "nota": "alta/média/baixa",
        "justificativa": "..."
    }},
    "resumo_executivo": "Resumo de 2-3 parágrafos sobre a situação atual da empresa"
}}
"""
        
        try:
            resultado = await self.ai_client.executar_prompt_raw(
                prompt,
                task_type="web_research"
            )
            
            # Tenta parsear JSON
            import json
            import re
            
            json_match = re.search(r'\{.*\}', resultado, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            
            return {"resumo_executivo": resultado[:1000]}
        
        except Exception as e:
            print(f"      Erro IA: {e}")
            return None
    
    def _gerar_resumo_estruturado(self, dados: Dict) -> str:
        """
        Gera resumo estruturado para enviar ao Prompt 3
        
        Formato similar a um release de resultados
        """
        
        ticker = dados.get("ticker", "")
        nome = dados.get("nome", "")
        
        resumo = f"=== {ticker} - {nome} ===\n\n"
        
        # Dados Financeiros
        if "financeiro" in dados:
            fin = dados["financeiro"]
            resumo += "DADOS FINANCEIROS:\n"
            
            if fin.get("receita_trimestral"):
                resumo += f"- Receita (últimos trimestres): "
                for r in fin["receita_trimestral"][:2]:
                    resumo += f"{r['trimestre']}: R$ {r['valor']/1e9:.2f}B, "
                resumo += "\n"
            
            if fin.get("lucro_liquido_trimestral"):
                resumo += f"- Lucro Líquido (últimos trimestres): "
                for l in fin["lucro_liquido_trimestral"][:2]:
                    resumo += f"{l['trimestre']}: R$ {l['valor']/1e9:.2f}B, "
                resumo += "\n"
            
            if fin.get("margem_liquida"):
                resumo += f"- Margem Líquida: {fin['margem_liquida']:.1f}%\n"
            
            if fin.get("roe"):
                resumo += f"- ROE: {fin['roe']:.1f}%\n"
            
            if fin.get("divida_patrimonio"):
                resumo += f"- Dívida/Patrimônio: {fin['divida_patrimonio']:.2f}\n"
            
            resumo += "\n"
        
        # Análise de IA
        if "analise_ia" in dados:
            ia = dados["analise_ia"]
            
            if ia.get("resumo_executivo"):
                resumo += f"CONTEXTO ATUAL:\n{ia['resumo_executivo']}\n\n"
            
            if ia.get("catalisadores"):
                resumo += "CATALISADORES:\n"
                for cat in ia["catalisadores"][:3]:
                    resumo += f"- {cat.get('descricao', '')} ({cat.get('prazo', '')} prazo)\n"
                resumo += "\n"
            
            if ia.get("riscos"):
                resumo += "RISCOS:\n"
                for risco in ia["riscos"][:3]:
                    resumo += f"- {risco.get('descricao', '')} (severidade: {risco.get('severidade', '')})\n"
                resumo += "\n"
            
            if ia.get("qualidade_gestao"):
                gestao = ia["qualidade_gestao"]
                resumo += f"QUALIDADE DA GESTÃO: {gestao.get('nota', 'N/A').upper()}\n"
                resumo += f"{gestao.get('justificativa', '')}\n\n"
        
        # Fontes
        resumo += f"FONTES: {', '.join(dados.get('fontes_usadas', []))}\n"
        resumo += f"DATA: {dados.get('timestamp', datetime.now()).strftime('%d/%m/%Y %H:%M')}\n"
        
        return resumo
    
    async def obter_dados_multiplas_empresas(
        self,
        empresas: List[Dict],
        batch_size: int = 2  # ULTRA REDUZIDO: 2 por lote (ZERO erros)
    ) -> Dict[str, Dict]:
        """
        Obtém dados de múltiplas empresas em lotes
        
        ULTRA OTIMIZADO:
        - batch_size=2 (apenas 2 empresas por vez)
        - Delay de 8s entre lotes (evita sobrecarga)
        - Processa sequencialmente dentro do lote (não paralelo)
        """
        
        print(f"\n📊 Coletando dados fundamentalistas de {len(empresas)} empresas...")
        print(f"   Estratégia: {batch_size} empresas por lote + 8s delay (ZERO erros)")
        
        dados_empresas = {}
        
        # Processa em lotes
        for i in range(0, len(empresas), batch_size):
            batch = empresas[i:i+batch_size]
            lote_num = (i // batch_size) + 1
            total_lotes = (len(empresas) + batch_size - 1) // batch_size
            
            print(f"\n📦 Lote {lote_num}/{total_lotes}: {len(batch)} empresas")
            
            # MUDANÇA: Processa SEQUENCIALMENTE (não paralelo)
            for empresa in batch:
                ticker = empresa.get('ticker', '')
                nome = empresa.get('nome', ticker)
                
                try:
                    resultado = await self.obter_dados_completos(ticker, nome)
                    
                    if resultado:
                        dados_empresas[ticker] = resultado
                    
                    # Delay entre empresas do mesmo lote
                    await asyncio.sleep(3)
                
                except Exception as e:
                    print(f"   ✗ {ticker}: Erro - {str(e)[:50]}")
            
            # Aguarda entre lotes (aumentado para 8s)
            if i + batch_size < len(empresas):
                print(f"   ⏳ Aguardando 8s antes do próximo lote...")
                await asyncio.sleep(8)
        
        print(f"\n✓ Dados obtidos: {len(dados_empresas)}/{len(empresas)} empresas\n")
        
        return dados_empresas


# Singleton
_dados_fundamentalistas_service: Optional[DadosFundamentalistasService] = None


def get_dados_fundamentalistas_service() -> DadosFundamentalistasService:
    """Retorna instância singleton"""
    global _dados_fundamentalistas_service
    
    if _dados_fundamentalistas_service is None:
        _dados_fundamentalistas_service = DadosFundamentalistasService()
    
    return _dados_fundamentalistas_service
