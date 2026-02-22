"""
ETAPA 4 — ESTRATÉGIA OPERACIONAL
Monta estratégia completa de entrada/saída/stop para empresas aprovadas
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime


class EstrategiaOperacional:
    """
    Cria estratégias operacionais completas para empresas aprovadas (nota ≥ 6)
    
    Para cada ação, define:
    1. ENTRADA: pode entrar agora ou aguardar? Preço ideal e gatilhos
    2. ALVOS: conservador e otimista (R$) + critério de saída antecipada
    3. STOP: preço exato e justificativa
    4. R/R: Risk/Reward ratio (mínimo 2.0 para executar)
    5. TEMPO: horizonte estimado + aceleradores/freios
    6. ALOCAÇÃO: % do portfólio + convicção
    7. ANTI-MANADA: análise de sentimento e fundamento
    """
    
    def __init__(self, groq_client):
        self.groq_client = groq_client
    
    async def criar_estrategias(
        self,
        empresas_aprovadas: List[Dict],
        contexto_completo: str,
        precos_atuais: Dict[str, float]
    ) -> Dict:
        """
        Cria estratégias para todas as empresas aprovadas
        
        Args:
            empresas_aprovadas: Lista de empresas com nota ≥ 6
            contexto_completo: Contexto das etapas 1, 2 e 3
            precos_atuais: Dicionário {ticker: preco}
        
        Returns:
            {
                "estrategias": [...],
                "ranking": [...],
                "carteira": {...},
                "total_aprovadas": int,
                "total_executaveis": int (R/R >= 2.0)
            }
        """
        print(f"\n[ETAPA 4] Criando estratégias para {len(empresas_aprovadas)} empresas...")
        
        # Monta prompt
        prompt = self._montar_prompt_estrategia(
            empresas_aprovadas,
            contexto_completo,
            precos_atuais
        )
        
        try:
            # Executa prompt
            resultado = await self.groq_client.executar_prompt(
                prompt=prompt,
                task_type="estrategia_operacional",
                usar_contexto=False  # Contexto já está no prompt
            )
            
            # Valida e processa estratégias
            estrategias_validadas = self._validar_estrategias(resultado.get('estrategias', []))
            
            # Filtra apenas executáveis (R/R >= 2.0)
            estrategias_executaveis = [
                e for e in estrategias_validadas
                if e.get('risco_retorno', 0) >= 2.0
            ]
            
            # Cria ranking
            ranking = self._criar_ranking_estrategias(estrategias_executaveis)
            
            # Calcula alocação de carteira
            carteira = self._calcular_carteira(estrategias_executaveis)
            
            return {
                "estrategias": estrategias_validadas,
                "estrategias_executaveis": estrategias_executaveis,
                "ranking": ranking,
                "carteira": carteira,
                "total_aprovadas": len(empresas_aprovadas),
                "total_executaveis": len(estrategias_executaveis),
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            print(f"[ETAPA 4] Erro ao criar estratégias: {e}")
            return {
                "estrategias": [],
                "estrategias_executaveis": [],
                "ranking": [],
                "carteira": {},
                "total_aprovadas": len(empresas_aprovadas),
                "total_executaveis": 0,
                "erro": str(e)
            }
    
    def _montar_prompt_estrategia(
        self,
        empresas: List[Dict],
        contexto: str,
        precos: Dict[str, float]
    ) -> str:
        """Monta prompt da Etapa 4"""
        
        # Lista de empresas aprovadas
        empresas_texto = []
        for emp in empresas:
            ticker = emp.get('ticker', 'N/A')
            nota = emp.get('nota', 0)
            preco = precos.get(ticker, emp.get('preco_atual', 0))
            perfil = emp.get('perfil', 'N/A')
            
            empresas_texto.append(
                f"- {ticker} | Nota {nota:.1f}/10 | Preço ATUAL: R${preco:.2f} | Perfil: {perfil}"
            )
        
        empresas_str = "\n".join(empresas_texto)
        
        prompt = f"""{contexto}

Você é estrategista de operações de curto e médio prazo na B3. Meta: 5% ao mês.

APROVADAS com preços ATUAIS:
{empresas_str}

Para cada ação, monte:
1. ENTRADA: pode entrar agora ou aguardar? Se aguardar, qual preço e qual gatilho?
2. ALVOS: alvo conservador e otimista (R$) | critério de saída antecipada
3. STOP: preço exato e justificativa do nível
4. R/R: calcule (Alvo - Entrada) / (Entrada - Stop). Se < 2,0, descarte ou ajuste.
5. TEMPO: dias/semanas estimados | o que pode acelerar ou atrasar a tese
6. ALOCAÇÃO: % do portfólio sugerido | convicção: Alta/Média/Baixa
7. ANTI-MANADA: já é manchete? Sustentado por fundamento ou euforia? Institucionais ainda comprando?

IMPORTANTE:
- Apenas estratégias com R/R >= 2.0 devem ser executadas
- Se R/R < 2.0, ajuste os alvos/stop ou descarte a operação
- Seja realista nos alvos (não exagere)
- Stop deve proteger o capital (máximo -8% por operação)

Responda SOMENTE com JSON válido:
{{
  "estrategias": [
    {{
      "ticker": "",
      "tipo_operacao": "Swing Trade / Position Trade",
      "preco_atual": 0.00,
      "entrada": {{
        "pode_entrar_agora": true,
        "preco_ideal": 0.00,
        "gatilho": "descrição do gatilho se não puder entrar agora"
      }},
      "alvos": {{
        "conservador": 0.00,
        "otimista": 0.00,
        "upside_conservador_pct": 0.0,
        "saida_antecipada": "critério para sair antes do alvo"
      }},
      "stop": {{
        "preco": 0.00,
        "perda_pct": 0.0,
        "justificativa": "por que esse nível de stop"
      }},
      "risco_retorno": 0.0,
      "tempo_estimado": "X dias/semanas",
      "alocacao_pct": 0.0,
      "convicao": "Alta/Média/Baixa",
      "anti_manada": {{
        "ja_e_manchete": false,
        "sustentado_por_fundamento": true,
        "conclusao": "análise de sentimento vs fundamento"
      }}
    }}
  ],
  "ranking": [
    {{
      "posicao": 1,
      "ticker": "",
      "justificativa": "2 linhas — por que é a melhor entrada agora"
    }}
  ],
  "carteira": {{
    "total_alocado_pct": 0.0,
    "caixa_reserva_pct": 0.0,
    "observacao": "comentário sobre a carteira sugerida"
  }}
}}"""
        
        return prompt
    
    def _validar_estrategias(self, estrategias: List[Dict]) -> List[Dict]:
        """Valida e corrige estratégias"""
        validadas = []
        
        for estrategia in estrategias:
            try:
                # Valida campos obrigatórios
                if not estrategia.get('ticker'):
                    continue
                
                # Calcula R/R se não estiver presente
                if 'risco_retorno' not in estrategia or estrategia['risco_retorno'] == 0:
                    entrada = estrategia.get('entrada', {}).get('preco_ideal', 0)
                    alvo = estrategia.get('alvos', {}).get('conservador', 0)
                    stop = estrategia.get('stop', {}).get('preco', 0)
                    
                    if entrada > 0 and alvo > entrada and stop < entrada:
                        rr = (alvo - entrada) / (entrada - stop)
                        estrategia['risco_retorno'] = round(rr, 2)
                
                # Calcula upside conservador se não estiver presente
                if 'alvos' in estrategia:
                    entrada = estrategia.get('entrada', {}).get('preco_ideal', 0)
                    alvo_conservador = estrategia['alvos'].get('conservador', 0)
                    
                    if entrada > 0 and alvo_conservador > 0:
                        upside = ((alvo_conservador - entrada) / entrada) * 100
                        estrategia['alvos']['upside_conservador_pct'] = round(upside, 1)
                
                # Calcula perda % do stop se não estiver presente
                if 'stop' in estrategia:
                    entrada = estrategia.get('entrada', {}).get('preco_ideal', 0)
                    stop = estrategia['stop'].get('preco', 0)
                    
                    if entrada > 0 and stop > 0:
                        perda = ((stop - entrada) / entrada) * 100
                        estrategia['stop']['perda_pct'] = round(perda, 1)
                
                # Adiciona flag de executável
                estrategia['executavel'] = estrategia.get('risco_retorno', 0) >= 2.0
                
                validadas.append(estrategia)
            
            except Exception as e:
                print(f"[ETAPA 4] Erro ao validar estratégia {estrategia.get('ticker', 'N/A')}: {e}")
                continue
        
        return validadas
    
    def _criar_ranking_estrategias(self, estrategias: List[Dict]) -> List[Dict]:
        """Cria ranking de estratégias por atratividade"""
        # Ordena por: convicção > R/R > upside
        def score_estrategia(e):
            convicao_score = {"Alta": 3, "Média": 2, "Baixa": 1}.get(e.get('convicao', 'Baixa'), 1)
            rr = e.get('risco_retorno', 0)
            upside = e.get('alvos', {}).get('upside_conservador_pct', 0)
            
            return (convicao_score * 100) + (rr * 10) + upside
        
        estrategias_ordenadas = sorted(estrategias, key=score_estrategia, reverse=True)
        
        ranking = []
        for i, estrategia in enumerate(estrategias_ordenadas, 1):
            ranking.append({
                "posicao": i,
                "ticker": estrategia.get('ticker'),
                "risco_retorno": estrategia.get('risco_retorno', 0),
                "upside_conservador": estrategia.get('alvos', {}).get('upside_conservador_pct', 0),
                "convicao": estrategia.get('convicao', 'Baixa'),
                "justificativa": self._gerar_justificativa_ranking(estrategia)
            })
        
        return ranking
    
    def _gerar_justificativa_ranking(self, estrategia: Dict) -> str:
        """Gera justificativa para posição no ranking"""
        ticker = estrategia.get('ticker', 'N/A')
        rr = estrategia.get('risco_retorno', 0)
        upside = estrategia.get('alvos', {}).get('upside_conservador_pct', 0)
        convicao = estrategia.get('convicao', 'Baixa')
        
        return f"{ticker}: R/R {rr:.2f}, upside {upside:.1f}%, convicção {convicao}"
    
    def _calcular_carteira(self, estrategias: List[Dict]) -> Dict:
        """Calcula alocação sugerida da carteira"""
        if not estrategias:
            return {
                "total_alocado_pct": 0.0,
                "caixa_reserva_pct": 100.0,
                "observacao": "Nenhuma estratégia executável (R/R < 2.0)"
            }
        
        # Soma alocações sugeridas
        total_alocado = sum(e.get('alocacao_pct', 0) for e in estrategias)
        
        # Ajusta se ultrapassar 100%
        if total_alocado > 80:  # Máximo 80% alocado, 20% caixa
            fator_ajuste = 80 / total_alocado
            for estrategia in estrategias:
                estrategia['alocacao_pct'] = round(estrategia.get('alocacao_pct', 0) * fator_ajuste, 1)
            total_alocado = 80
        
        caixa_reserva = 100 - total_alocado
        
        return {
            "total_alocado_pct": round(total_alocado, 1),
            "caixa_reserva_pct": round(caixa_reserva, 1),
            "total_posicoes": len(estrategias),
            "observacao": f"Carteira com {len(estrategias)} posições, {caixa_reserva:.1f}% em caixa para oportunidades"
        }


def get_estrategia_operacional(groq_client):
    """Factory function"""
    return EstrategiaOperacional(groq_client)
