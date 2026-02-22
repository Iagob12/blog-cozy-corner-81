"""
Web Research Service - Busca informações da internet sobre empresas
Usado como fallback quando Release não é encontrado
"""
import asyncio
from typing import Dict, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup

from app.services.multi_groq_client import get_multi_groq_client


class WebResearchService:
    """
    Busca informações profundas sobre empresas na internet
    Usado quando Release de Resultados não está disponível
    Usa Multi Groq (6 chaves + contexto persistente)
    """
    
    def __init__(self):
        self.ai_client = get_multi_groq_client()
        print("✓ Web Research Service inicializado (Multi Groq - 6 chaves)")
    
    async def pesquisar_empresa_completo(self, ticker: str, nome_empresa: str) -> Dict:
        """
        Pesquisa COMPLETA sobre a empresa:
        - Notícias recentes (últimos 3 meses)
        - Análise de mercado
        - Eventos importantes
        - Contexto setorial
        - Performance recente
        
        Returns:
            Dict com todas as informações encontradas
        """
        
        print(f"\n🔍 [{ticker}] Pesquisando informações na internet...")
        print(f"   Empresa: {nome_empresa}")
        
        try:
            # Usa Gemini com Google Search para pesquisa profunda
            prompt = f"""
Você é um analista financeiro especializado em ações brasileiras.

TAREFA: Pesquise PROFUNDAMENTE sobre a empresa {nome_empresa} ({ticker}) e forneça uma análise COMPLETA e ATUALIZADA.

IMPORTANTE: Esta pesquisa substitui o Release de Resultados que não foi encontrado. Portanto, seja MUITO DETALHADO e ESPECÍFICO.

PESQUISE E ANALISE:

1. **RESULTADOS FINANCEIROS RECENTES** (últimos 3-6 meses):
   - Receita e lucro líquido
   - Margens operacionais
   - Crescimento vs trimestre anterior
   - Comparação com expectativas do mercado
   - Guidance da empresa (se houver)

2. **NOTÍCIAS E EVENTOS IMPORTANTES**:
   - Últimas notícias relevantes (últimos 3 meses)
   - Anúncios de novos projetos/contratos
   - Mudanças na gestão
   - Fusões, aquisições, parcerias
   - Problemas ou controvérsias

3. **CONTEXTO SETORIAL**:
   - Como está o setor da empresa?
   - Tendências macroeconômicas afetando o setor
   - Posição competitiva da empresa
   - Principais concorrentes e comparação

4. **PERFORMANCE DE MERCADO**:
   - Como a ação se comportou recentemente?
   - Houve algum movimento anormal de preço?
   - Volume de negociação
   - Sentimento geral do mercado sobre a ação

5. **CATALISADORES E RISCOS**:
   - Próximos eventos importantes (earnings, eventos corporativos)
   - Catalisadores positivos identificados
   - Riscos específicos da empresa
   - Fatores que podem impactar o preço

6. **ANÁLISE DE ANALISTAS**:
   - Recomendações recentes de casas de análise
   - Preço-alvo médio
   - Consenso do mercado

FORMATO DA RESPOSTA (JSON):
{{
    "ticker": "{ticker}",
    "nome": "{nome_empresa}",
    "data_pesquisa": "DD/MM/YYYY",
    
    "resumo_executivo": "Resumo de 2-3 parágrafos sobre a situação atual da empresa",
    
    "resultados_recentes": {{
        "receita_trimestre": "Valor ou 'Não disponível'",
        "lucro_liquido": "Valor ou 'Não disponível'",
        "crescimento": "% ou descrição",
        "destaques": ["ponto 1", "ponto 2", "ponto 3"]
    }},
    
    "noticias_importantes": [
        {{
            "data": "DD/MM/YYYY",
            "titulo": "Título da notícia",
            "resumo": "Resumo do impacto",
            "sentimento": "positivo/negativo/neutro"
        }}
    ],
    
    "contexto_setorial": {{
        "situacao_setor": "Descrição do setor",
        "tendencias": ["tendência 1", "tendência 2"],
        "posicao_competitiva": "Descrição da posição da empresa"
    }},
    
    "performance_mercado": {{
        "variacao_3m": "% ou descrição",
        "volume_medio": "Descrição",
        "sentimento_geral": "positivo/negativo/neutro",
        "analise": "Análise da performance"
    }},
    
    "catalisadores": [
        "Catalisador 1",
        "Catalisador 2",
        "Catalisador 3"
    ],
    
    "riscos": [
        "Risco 1",
        "Risco 2",
        "Risco 3"
    ],
    
    "consenso_analistas": {{
        "recomendacao_media": "Compra/Neutro/Venda",
        "preco_alvo_medio": "R$ X.XX ou 'Não disponível'",
        "numero_analistas": "X analistas ou 'Não disponível'"
    }},
    
    "conclusao": "Conclusão final sobre a empresa e perspectivas"
}}

IMPORTANTE:
- Use DADOS REAIS e ATUALIZADOS da internet
- Seja ESPECÍFICO com números e datas
- Cite FONTES quando possível
- Se não encontrar alguma informação, indique claramente
- Foque em informações dos ÚLTIMOS 3-6 MESES
- Esta análise será usada para decisão de investimento, seja PRECISO
"""
            
            print(f"   🤖 Consultando IA com pesquisa web (Multi Groq)...")
            
            # Executa pesquisa com IA (Multi Groq - rotação automática)
            resultado = await self.ai_client.executar_prompt_raw(
                prompt,
                task_type="web_research"
            )
            
            # Tenta extrair JSON da resposta
            import json
            import re
            
            # Procura por JSON na resposta
            json_match = re.search(r'\{.*\}', resultado, re.DOTALL)
            if json_match:
                dados = json.loads(json_match.group())
                
                print(f"   ✓ Pesquisa concluída!")
                print(f"   ✓ Notícias encontradas: {len(dados.get('noticias_importantes', []))}")
                print(f"   ✓ Catalisadores: {len(dados.get('catalisadores', []))}")
                
                return {
                    "success": True,
                    "ticker": ticker,
                    "nome": nome_empresa,
                    "dados": dados,
                    "texto_completo": self._formatar_para_prompt(dados),
                    "timestamp": datetime.now()
                }
            else:
                # Se não encontrou JSON, usa texto bruto
                print(f"   ⚠ JSON não encontrado, usando texto bruto")
                return {
                    "success": True,
                    "ticker": ticker,
                    "nome": nome_empresa,
                    "dados": None,
                    "texto_completo": resultado[:3000],  # Limita a 3000 chars
                    "timestamp": datetime.now()
                }
        
        except Exception as e:
            print(f"   ✗ Erro na pesquisa: {e}")
            return {
                "success": False,
                "ticker": ticker,
                "nome": nome_empresa,
                "error": str(e),
                "texto_completo": f"Não foi possível pesquisar informações sobre {nome_empresa} ({ticker})",
                "timestamp": datetime.now()
            }
    
    def _formatar_para_prompt(self, dados: Dict) -> str:
        """
        Formata dados da pesquisa para enviar ao Prompt 3
        """
        
        texto = f"""
=== PESQUISA WEB: {dados.get('nome', 'N/A')} ({dados.get('ticker', 'N/A')}) ===
Data da Pesquisa: {dados.get('data_pesquisa', 'N/A')}

RESUMO EXECUTIVO:
{dados.get('resumo_executivo', 'N/A')}

RESULTADOS RECENTES:
{self._formatar_resultados(dados.get('resultados_recentes', {}))}

NOTÍCIAS IMPORTANTES:
{self._formatar_noticias(dados.get('noticias_importantes', []))}

CONTEXTO SETORIAL:
{self._formatar_contexto(dados.get('contexto_setorial', {}))}

PERFORMANCE DE MERCADO:
{self._formatar_performance(dados.get('performance_mercado', {}))}

CATALISADORES:
{self._formatar_lista(dados.get('catalisadores', []))}

RISCOS:
{self._formatar_lista(dados.get('riscos', []))}

CONSENSO DE ANALISTAS:
{self._formatar_consenso(dados.get('consenso_analistas', {}))}

CONCLUSÃO:
{dados.get('conclusao', 'N/A')}
"""
        
        return texto
    
    def _formatar_resultados(self, resultados: Dict) -> str:
        if not resultados:
            return "Não disponível"
        
        texto = f"""
- Receita: {resultados.get('receita_trimestre', 'N/A')}
- Lucro Líquido: {resultados.get('lucro_liquido', 'N/A')}
- Crescimento: {resultados.get('crescimento', 'N/A')}
- Destaques: {', '.join(resultados.get('destaques', []))}
"""
        return texto
    
    def _formatar_noticias(self, noticias: list) -> str:
        if not noticias:
            return "Nenhuma notícia relevante encontrada"
        
        texto = ""
        for noticia in noticias[:5]:  # Limita a 5 notícias
            texto += f"""
• [{noticia.get('data', 'N/A')}] {noticia.get('titulo', 'N/A')}
  {noticia.get('resumo', 'N/A')}
  Sentimento: {noticia.get('sentimento', 'N/A')}
"""
        return texto
    
    def _formatar_contexto(self, contexto: Dict) -> str:
        if not contexto:
            return "Não disponível"
        
        texto = f"""
- Situação do Setor: {contexto.get('situacao_setor', 'N/A')}
- Tendências: {', '.join(contexto.get('tendencias', []))}
- Posição Competitiva: {contexto.get('posicao_competitiva', 'N/A')}
"""
        return texto
    
    def _formatar_performance(self, performance: Dict) -> str:
        if not performance:
            return "Não disponível"
        
        texto = f"""
- Variação 3 meses: {performance.get('variacao_3m', 'N/A')}
- Volume Médio: {performance.get('volume_medio', 'N/A')}
- Sentimento Geral: {performance.get('sentimento_geral', 'N/A')}
- Análise: {performance.get('analise', 'N/A')}
"""
        return texto
    
    def _formatar_lista(self, items: list) -> str:
        if not items:
            return "Nenhum identificado"
        
        return "\n".join([f"• {item}" for item in items])
    
    def _formatar_consenso(self, consenso: Dict) -> str:
        if not consenso:
            return "Não disponível"
        
        texto = f"""
- Recomendação Média: {consenso.get('recomendacao_media', 'N/A')}
- Preço-Alvo Médio: {consenso.get('preco_alvo_medio', 'N/A')}
- Número de Analistas: {consenso.get('numero_analistas', 'N/A')}
"""
        return texto
    
    async def pesquisar_multiplas_empresas(
        self, 
        empresas: list[Dict],
        batch_size: int = 6  # NOVO: 6 pesquisas por lote (uma por chave Groq)
    ) -> Dict[str, Dict]:
        """
        Pesquisa múltiplas empresas EM LOTES para evitar rate limit
        
        ESTRATÉGIA:
        - Processa 6 empresas por vez (uma por chave Groq)
        - Aguarda 2s entre lotes
        - Evita esgotar todas as chaves simultaneamente
        
        Args:
            empresas: Lista de dicts com 'ticker' e 'nome'
            batch_size: Quantas pesquisas simultâneas (padrão: 6)
        
        Returns:
            Dict[ticker, resultado_pesquisa]
        """
        
        total_empresas = len(empresas)
        total_lotes = (total_empresas + batch_size - 1) // batch_size
        
        print(f"\n🔍 Pesquisando {total_empresas} empresas em {total_lotes} lotes de {batch_size}...")
        print(f"   Estratégia: 1 empresa por chave Groq, aguarda entre lotes")
        
        pesquisas = {}
        
        # Processa em lotes
        for i in range(0, total_empresas, batch_size):
            batch = empresas[i:i+batch_size]
            lote_num = (i // batch_size) + 1
            
            print(f"\n📦 Lote {lote_num}/{total_lotes}: Pesquisando {len(batch)} empresas...")
            
            # Cria tasks para este lote
            tasks = []
            for empresa in batch:
                ticker = empresa.get('ticker', '')
                nome = empresa.get('nome', ticker)
                task = self.pesquisar_empresa_completo(ticker, nome)
                tasks.append(task)
            
            # Executa lote em paralelo
            resultados = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Processa resultados
            sucesso_lote = 0
            for j, resultado in enumerate(resultados):
                if isinstance(resultado, Exception):
                    ticker = batch[j].get('ticker', '')
                    print(f"   ✗ {ticker}: Erro - {resultado}")
                    continue
                
                if resultado.get('success'):
                    ticker = resultado['ticker']
                    pesquisas[ticker] = resultado
                    sucesso_lote += 1
            
            print(f"   ✓ Lote {lote_num}: {sucesso_lote}/{len(batch)} concluídas")
            
            # Aguarda entre lotes (exceto no último)
            # AUMENTADO: 5s ao invés de 2s para garantir zero rate limit
            if i + batch_size < total_empresas:
                tempo_espera = 5  # Era 2s, agora 5s (CONSERVADOR)
                print(f"   ⏳ Aguardando {tempo_espera}s antes do próximo lote...")
                await asyncio.sleep(tempo_espera)
        
        print(f"\n✓ TOTAL: {len(pesquisas)}/{total_empresas} pesquisas concluídas ({len(pesquisas)/total_empresas*100:.0f}%)\n")
        
        return pesquisas
