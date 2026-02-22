"""
CONTEXT MANAGER - Gestão de Contexto Persistente
Resolve o problema de perda de contexto entre sessões do Groq
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class ContextManager:
    """
    Gerencia o bloco de contexto manual que persiste entre etapas.
    
    Template do Contexto:
    [===== CONTEXTO DO DIA =====]
    DATA: DD/MM/AAAA
    MACRO: Selic XX%, Dólar R$XX, Setores quentes: [X,Y], Evitar: [Z]
    AÇÕES SELECIONADAS (Etapa 2):
    - TICK1 | R$XX | ROE XX% | P/L XX | Perfil A/B | Motivo: [resumo]
    RELEASES ANALISADOS (Etapa 3):
    - TICK1: Nota X/10 | COMPRA/MONITORAR | Tese: [resumo]
    ESTRATÉGIAS MONTADAS (Etapa 4):
    - TICK1: Entry R$XX | Alvo R$XX | Stop R$XX | R/R X.X
    [===== FIM DO CONTEXTO =====]
    """
    
    def __init__(self, contexto_dir: str = "data/contexto"):
        self.contexto_dir = Path(contexto_dir)
        self.contexto_dir.mkdir(parents=True, exist_ok=True)
        
        self.contexto_file = self.contexto_dir / "contexto_atual.json"
        self.contexto_texto_file = self.contexto_dir / "contexto_atual.txt"
        self.historico_file = self.contexto_dir / "historico_contextos.json"
        
        self.contexto_atual = self._carregar_contexto()
    
    def _carregar_contexto(self) -> Dict:
        """Carrega contexto atual do disco"""
        if self.contexto_file.exists():
            try:
                with open(self.contexto_file, 'r', encoding='utf-8-sig') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[ContextManager] Erro ao carregar contexto: {e}")
        
        # Contexto vazio inicial
        return {
            "data": datetime.now().strftime('%d/%m/%Y'),
            "timestamp": datetime.now().isoformat(),
            "etapa_1_macro": None,
            "etapa_2_triagem": None,
            "etapa_3_releases": [],
            "etapa_4_estrategias": [],
            "etapa_5_revisao": None
        }
    
    def _salvar_contexto(self):
        """Salva contexto atual no disco (JSON + TXT)"""
        try:
            # Salva JSON
            with open(self.contexto_file, 'w', encoding='utf-8') as f:
                json.dump(self.contexto_atual, f, indent=2, ensure_ascii=False)
            
            # Salva TXT formatado
            texto = self._gerar_texto_contexto()
            with open(self.contexto_texto_file, 'w', encoding='utf-8') as f:
                f.write(texto)
            
            # Adiciona ao histórico
            self._adicionar_historico()
            
        except Exception as e:
            print(f"[ContextManager] Erro ao salvar contexto: {e}")
    
    def _gerar_texto_contexto(self) -> str:
        """Gera texto formatado do contexto para colar nos prompts"""
        linhas = ["[===== CONTEXTO DO DIA =====]"]
        linhas.append(f"DATA: {self.contexto_atual['data']}")
        
        # ETAPA 1 - MACRO
        if self.contexto_atual.get('etapa_1_macro'):
            macro = self.contexto_atual['etapa_1_macro']
            cenario = macro.get('cenario_macro', {})
            
            selic = cenario.get('taxa_selic', 'N/A')
            dolar = cenario.get('dolar', 'N/A')
            setores_quentes = ', '.join(cenario.get('setores_acelerando', []))
            setores_evitar = ', '.join(cenario.get('setores_evitar', []))
            
            linhas.append(f"MACRO: Selic {selic}, Dólar {dolar}")
            linhas.append(f"Setores quentes: [{setores_quentes}]")
            linhas.append(f"Evitar: [{setores_evitar}]")
            
            if cenario.get('narrativa_institucional'):
                linhas.append(f"Narrativa Institucional: {cenario['narrativa_institucional'][:150]}...")
        
        # ETAPA 2 - TRIAGEM
        if self.contexto_atual.get('etapa_2_triagem'):
            linhas.append("\nAÇÕES SELECIONADAS (Etapa 2):")
            triagem = self.contexto_atual['etapa_2_triagem']
            
            for acao in triagem.get('acoes_selecionadas', [])[:10]:  # Max 10 para não ficar muito grande
                ticker = acao.get('ticker', 'N/A')
                preco = acao.get('preco_atual', 0)
                roe = acao.get('roe', 0)
                pl = acao.get('pl', 0)
                perfil = acao.get('perfil', 'N/A')
                motivo = acao.get('motivo_selecao', 'N/A')[:80]
                
                linhas.append(f"- {ticker} | R${preco:.2f} | ROE {roe:.1f}% | P/L {pl:.2f} | Perfil {perfil} | {motivo}")
        
        # ETAPA 3 - RELEASES
        if self.contexto_atual.get('etapa_3_releases'):
            linhas.append("\nRELEASES ANALISADOS (Etapa 3):")
            
            for release in self.contexto_atual['etapa_3_releases'][:10]:  # Max 10
                ticker = release.get('ticker', 'N/A')
                nota = release.get('nota', 0)
                rec = release.get('recomendacao', 'N/A')
                tese = release.get('tese_resumida', 'N/A')[:100]
                
                linhas.append(f"- {ticker}: Nota {nota:.1f}/10 | {rec} | {tese}")
        
        # ETAPA 4 - ESTRATÉGIAS
        if self.contexto_atual.get('etapa_4_estrategias'):
            linhas.append("\nESTRATÉGIAS MONTADAS (Etapa 4):")
            
            for estrategia in self.contexto_atual['etapa_4_estrategias'][:10]:
                ticker = estrategia.get('ticker', 'N/A')
                entrada = estrategia.get('entrada', {}).get('preco_ideal', 0)
                alvo = estrategia.get('alvos', {}).get('conservador', 0)
                stop = estrategia.get('stop', {}).get('preco', 0)
                rr = estrategia.get('risco_retorno', 0)
                
                linhas.append(f"- {ticker}: Entry R${entrada:.2f} | Alvo R${alvo:.2f} | Stop R${stop:.2f} | R/R {rr:.2f}")
        
        linhas.append("[===== FIM DO CONTEXTO =====]")
        
        return "\n".join(linhas)
    
    def _adicionar_historico(self):
        """Adiciona contexto atual ao histórico"""
        try:
            historico = []
            if self.historico_file.exists():
                with open(self.historico_file, 'r', encoding='utf-8-sig') as f:
                    historico = json.load(f)
            
            # Calcula totais com segurança
            triagem = self.contexto_atual.get('etapa_2_triagem') or {}
            acoes = triagem.get('acoes_selecionadas') or []
            releases = self.contexto_atual.get('etapa_3_releases') or []
            estrategias = self.contexto_atual.get('etapa_4_estrategias') or []
            
            # Adiciona contexto atual
            historico.append({
                "timestamp": datetime.now().isoformat(),
                "data": self.contexto_atual['data'],
                "resumo": {
                    "total_acoes_triagem": len(acoes),
                    "total_releases": len(releases),
                    "total_estrategias": len(estrategias)
                }
            })
            
            # Mantém apenas últimos 30 dias
            historico = historico[-30:]
            
            with open(self.historico_file, 'w', encoding='utf-8') as f:
                json.dump(historico, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            print(f"[ContextManager] Erro ao adicionar histórico: {e}")
    
    # ========== MÉTODOS PÚBLICOS ==========
    
    def iniciar_novo_contexto(self) -> Dict:
        """Inicia um novo contexto (nova análise do dia)"""
        self.contexto_atual = {
            "data": datetime.now().strftime('%d/%m/%Y'),
            "timestamp": datetime.now().isoformat(),
            "etapa_1_macro": None,
            "etapa_2_triagem": None,
            "etapa_3_releases": [],
            "etapa_4_estrategias": [],
            "etapa_5_revisao": None
        }
        self._salvar_contexto()
        return self.contexto_atual
    
    def atualizar_etapa_1_macro(self, resultado_macro: Dict):
        """Atualiza contexto com resultado da Etapa 1 (Macro)"""
        self.contexto_atual['etapa_1_macro'] = resultado_macro
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def atualizar_etapa_2_triagem(self, resultado_triagem: Dict):
        """Atualiza contexto com resultado da Etapa 2 (Triagem)"""
        self.contexto_atual['etapa_2_triagem'] = resultado_triagem
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def adicionar_etapa_3_release(self, resultado_release: Dict):
        """Adiciona análise de release da Etapa 3"""
        if 'etapa_3_releases' not in self.contexto_atual:
            self.contexto_atual['etapa_3_releases'] = []
        
        self.contexto_atual['etapa_3_releases'].append(resultado_release)
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def atualizar_etapa_3_releases(self, resultados_releases: List[Dict]):
        """Atualiza contexto com todos os releases da Etapa 3"""
        self.contexto_atual['etapa_3_releases'] = resultados_releases
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def adicionar_etapa_4_estrategia(self, estrategia: Dict):
        """Adiciona estratégia da Etapa 4"""
        if 'etapa_4_estrategias' not in self.contexto_atual:
            self.contexto_atual['etapa_4_estrategias'] = []
        
        self.contexto_atual['etapa_4_estrategias'].append(estrategia)
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def atualizar_etapa_4_estrategias(self, estrategias: List[Dict]):
        """Atualiza contexto com todas as estratégias da Etapa 4"""
        self.contexto_atual['etapa_4_estrategias'] = estrategias
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def atualizar_etapa_5_revisao(self, resultado_revisao: Dict):
        """Atualiza contexto com resultado da Etapa 5 (Revisão)"""
        self.contexto_atual['etapa_5_revisao'] = resultado_revisao
        self.contexto_atual['timestamp'] = datetime.now().isoformat()
        self._salvar_contexto()
    
    def obter_contexto_texto(self) -> str:
        """Retorna contexto formatado em texto para colar nos prompts"""
        return self._gerar_texto_contexto()
    
    def obter_contexto_json(self) -> Dict:
        """Retorna contexto completo em JSON"""
        return self.contexto_atual.copy()
    
    def obter_macro(self) -> Optional[Dict]:
        """Retorna apenas o contexto macro (Etapa 1)"""
        return self.contexto_atual.get('etapa_1_macro')
    
    def obter_triagem(self) -> Optional[Dict]:
        """Retorna apenas a triagem (Etapa 2)"""
        return self.contexto_atual.get('etapa_2_triagem')
    
    def obter_releases(self) -> List[Dict]:
        """Retorna todas as análises de releases (Etapa 3)"""
        return self.contexto_atual.get('etapa_3_releases', [])
    
    def obter_estrategias(self) -> List[Dict]:
        """Retorna todas as estratégias (Etapa 4)"""
        return self.contexto_atual.get('etapa_4_estrategias', [])
    
    def obter_revisao(self) -> Optional[Dict]:
        """Retorna a revisão de carteira (Etapa 5)"""
        return self.contexto_atual.get('etapa_5_revisao')
    
    def limpar_contexto(self):
        """Limpa contexto atual (útil para testes)"""
        self.iniciar_novo_contexto()
    
    def obter_historico(self, limite: int = 30) -> List[Dict]:
        """Retorna histórico de contextos"""
        try:
            if self.historico_file.exists():
                with open(self.historico_file, 'r', encoding='utf-8-sig') as f:
                    historico = json.load(f)
                    return historico[-limite:]
            return []
        except Exception as e:
            print(f"[ContextManager] Erro ao obter histórico: {e}")
            return []


# Singleton global
_context_manager_instance = None

def get_context_manager() -> ContextManager:
    """Retorna instância singleton do ContextManager"""
    global _context_manager_instance
    if _context_manager_instance is None:
        _context_manager_instance = ContextManager()
    return _context_manager_instance
