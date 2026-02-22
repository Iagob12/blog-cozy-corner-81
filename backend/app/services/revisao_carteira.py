"""
ETAPA 5 — REVISÃO MENSAL
Revisa carteira ativa sem apego, focando nas melhores oportunidades de agora
"""
from typing import Dict, List, Optional
from datetime import datetime


class RevisaoCarteira:
    """
    Revisa posições da carteira ativa
    
    Para cada posição:
    - A tese original ainda vale?
    - O upside ainda existe?
    - Há algo melhor para esse capital agora?
    
    Critério único: a carteira deve ter as melhores oportunidades de AGORA,
    não defender o que foi comprado.
    """
    
    def __init__(self, groq_client):
        self.groq_client = groq_client
    
    async def revisar_carteira(
        self,
        carteira_atual: List[Dict],
        contexto_macro_atual: str,
        novas_oportunidades: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Revisa carteira ativa
        
        Args:
            carteira_atual: Lista de posições atuais
                [
                    {
                        "ticker": "PRIO3",
                        "preco_medio": 45.50,
                        "preco_atual": 48.20,
                        "resultado_pct": 5.9,
                        "pct_carteira": 15.0,
                        "data_entrada": "2026-01-15",
                        "tese_original": "..."
                    }
                ]
            contexto_macro_atual: Contexto macro mais recente
            novas_oportunidades: Novas empresas analisadas (opcional)
        
        Returns:
            {
                "analise_posicoes": [...],
                "parecer_geral": {...},
                "acoes_recomendadas": {...}
            }
        """
        print(f"\n[ETAPA 5] Revisando carteira com {len(carteira_atual)} posições...")
        
        # Monta prompt
        prompt = self._montar_prompt_revisao(
            carteira_atual,
            contexto_macro_atual,
            novas_oportunidades
        )
        
        try:
            # Executa prompt
            resultado = await self.groq_client.executar_prompt(
                prompt=prompt,
                task_type="revisao_carteira",
                usar_contexto=False  # Contexto já está no prompt
            )
            
            # Processa resultado
            analise_posicoes = resultado.get('analise_posicoes', [])
            parecer_geral = resultado.get('parecer_geral', {})
            
            # Gera ações recomendadas
            acoes_recomendadas = self._gerar_acoes_recomendadas(analise_posicoes)
            
            return {
                "analise_posicoes": analise_posicoes,
                "parecer_geral": parecer_geral,
                "acoes_recomendadas": acoes_recomendadas,
                "total_posicoes": len(carteira_atual),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"[ETAPA 5] Erro ao revisar carteira: {e}")
            return {
                "analise_posicoes": [],
                "parecer_geral": {},
                "acoes_recomendadas": {},
                "erro": str(e)
            }
    
    def _montar_prompt_revisao(
        self,
        carteira: List[Dict],
        contexto: str,
        novas_oportunidades: Optional[List[Dict]]
    ) -> str:
        """Monta prompt da Etapa 5"""
        
        # Lista de posições atuais
        posicoes_texto = []
        for pos in carteira:
            ticker = pos.get('ticker', 'N/A')
            pm = pos.get('preco_medio', 0)
            pa = pos.get('preco_atual', 0)
            resultado = pos.get('resultado_pct', 0)
            pct = pos.get('pct_carteira', 0)
            
            posicoes_texto.append(
                f"- {ticker} | PM: R${pm:.2f} | Atual: R${pa:.2f} | "
                f"Resultado: {resultado:+.1f}% | % carteira: {pct:.1f}%"
            )
        
        posicoes_str = "\n".join(posicoes_texto)
        
        # Novas oportunidades (se houver)
        novas_str = ""
        if novas_oportunidades:
            novas_texto = []
            for oport in novas_oportunidades[:5]:  # Max 5
                ticker = oport.get('ticker', 'N/A')
                nota = oport.get('nota', 0)
                upside = oport.get('upside', 0)
                novas_texto.append(f"- {ticker}: Nota {nota:.1f}/10, Upside {upside:.1f}%")
            
            novas_str = "\n\nNOVAS OPORTUNIDADES IDENTIFICADAS:\n" + "\n".join(novas_texto)
        
        prompt = f"""{contexto}

Você é analista de carteiras na B3. Revise as posições abaixo sem apego.
Critério único: a carteira deve ter as melhores oportunidades de agora, não defender o que foi comprado.

CARTEIRA ATUAL:
{posicoes_str}
{novas_str}

Para cada posição: a tese original ainda vale? O upside ainda existe? Há algo melhor para esse capital agora?

IMPORTANTE:
- Seja honesto e sem apego emocional
- Se a tese não vale mais, recomende VENDER (mesmo com lucro)
- Se há oportunidade melhor, recomende REDUZIR e realocar
- Considere o cenário macro atual
- Foque em maximizar retorno futuro, não justificar decisões passadas

Responda SOMENTE com JSON válido:
{{
  "analise_posicoes": [
    {{
      "ticker": "",
      "resultado_pct": 0.0,
      "tese_valida": true,
      "upside_restante": "alto/médio/baixo/nenhum",
      "acao": "MANTER / AUMENTAR / REDUZIR PARCIAL / VENDER TUDO",
      "justificativa": "2-3 linhas diretas sobre por que tomar essa ação",
      "prioridade": "alta/média/baixa"
    }}
  ],
  "parecer_geral": {{
    "cortar": ["TICK1", "TICK2"],
    "manter": ["TICK3", "TICK4"],
    "aumentar": ["TICK5"],
    "oportunidade_faltando": "existe algo melhor para esse capital? Qual?",
    "saude_carteira": "resumo honesto em 3-4 linhas sobre a saúde da carteira",
    "risco_atual": "baixo/médio/alto",
    "diversificacao": "adequada/concentrada/dispersa"
  }}
}}"""
        
        return prompt
    
    def _gerar_acoes_recomendadas(self, analise_posicoes: List[Dict]) -> Dict:
        """Gera resumo de ações recomendadas"""
        acoes = {
            "vender_tudo": [],
            "reduzir_parcial": [],
            "manter": [],
            "aumentar": [],
            "total_acoes": 0
        }
        
        for pos in analise_posicoes:
            ticker = pos.get('ticker', 'N/A')
            acao = pos.get('acao', 'MANTER').upper()
            prioridade = pos.get('prioridade', 'média')
            
            if 'VENDER TUDO' in acao:
                acoes['vender_tudo'].append({
                    "ticker": ticker,
                    "prioridade": prioridade,
                    "motivo": pos.get('justificativa', 'N/A')[:100]
                })
                acoes['total_acoes'] += 1
            
            elif 'REDUZIR' in acao:
                acoes['reduzir_parcial'].append({
                    "ticker": ticker,
                    "prioridade": prioridade,
                    "motivo": pos.get('justificativa', 'N/A')[:100]
                })
                acoes['total_acoes'] += 1
            
            elif 'AUMENTAR' in acao:
                acoes['aumentar'].append({
                    "ticker": ticker,
                    "prioridade": prioridade,
                    "motivo": pos.get('justificativa', 'N/A')[:100]
                })
                acoes['total_acoes'] += 1
            
            else:  # MANTER
                acoes['manter'].append({
                    "ticker": ticker,
                    "upside_restante": pos.get('upside_restante', 'N/A')
                })
        
        return acoes
    
    def gerar_relatorio_revisao(self, resultado_revisao: Dict) -> str:
        """Gera relatório texto da revisão"""
        linhas = ["=" * 80]
        linhas.append("RELATÓRIO DE REVISÃO DE CARTEIRA")
        linhas.append("=" * 80)
        linhas.append("")
        
        # Parecer geral
        parecer = resultado_revisao.get('parecer_geral', {})
        linhas.append("PARECER GERAL:")
        linhas.append(f"  Saúde da Carteira: {parecer.get('saude_carteira', 'N/A')}")
        linhas.append(f"  Risco Atual: {parecer.get('risco_atual', 'N/A').upper()}")
        linhas.append(f"  Diversificação: {parecer.get('diversificacao', 'N/A').upper()}")
        linhas.append("")
        
        # Ações recomendadas
        acoes = resultado_revisao.get('acoes_recomendadas', {})
        
        if acoes.get('vender_tudo'):
            linhas.append("🔴 VENDER TUDO:")
            for item in acoes['vender_tudo']:
                linhas.append(f"  - {item['ticker']} (Prioridade: {item['prioridade']})")
                linhas.append(f"    {item['motivo']}")
            linhas.append("")
        
        if acoes.get('reduzir_parcial'):
            linhas.append("🟡 REDUZIR PARCIAL:")
            for item in acoes['reduzir_parcial']:
                linhas.append(f"  - {item['ticker']} (Prioridade: {item['prioridade']})")
                linhas.append(f"    {item['motivo']}")
            linhas.append("")
        
        if acoes.get('aumentar'):
            linhas.append("🟢 AUMENTAR POSIÇÃO:")
            for item in acoes['aumentar']:
                linhas.append(f"  - {item['ticker']} (Prioridade: {item['prioridade']})")
                linhas.append(f"    {item['motivo']}")
            linhas.append("")
        
        if acoes.get('manter'):
            linhas.append("✅ MANTER:")
            for item in acoes['manter']:
                linhas.append(f"  - {item['ticker']} (Upside restante: {item['upside_restante']})")
            linhas.append("")
        
        # Oportunidades
        if parecer.get('oportunidade_faltando'):
            linhas.append("💡 OPORTUNIDADES:")
            linhas.append(f"  {parecer['oportunidade_faltando']}")
            linhas.append("")
        
        linhas.append("=" * 80)
        
        return "\n".join(linhas)


def get_revisao_carteira(groq_client):
    """Factory function"""
    return RevisaoCarteira(groq_client)
