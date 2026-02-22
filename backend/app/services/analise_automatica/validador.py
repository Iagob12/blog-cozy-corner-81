"""
Validador de Resultados da IA

Garante que as análises da IA são consistentes e confiáveis
"""
from typing import Dict, List, Optional, Tuple
import re


class ValidadorResultados:
    """
    Valida resultados da IA para garantir qualidade
    
    Validações:
    1. Estrutura do JSON
    2. Campos obrigatórios
    3. Tipos de dados
    4. Ranges de valores
    5. Coerência lógica
    """
    
    CAMPOS_OBRIGATORIOS = [
        "ticker", "recomendacao", "preco_teto", 
        "upside", "score", "riscos", "catalisadores"
    ]
    
    RECOMENDACOES_VALIDAS = [
        "COMPRA FORTE", "COMPRA", "MANTER", "VENDA", "AGUARDAR"
    ]
    
    def __init__(self):
        self.erros_comuns = []
    
    def validar(self, analise: Dict, ticker: str, preco_atual: float) -> Tuple[bool, List[str]]:
        """
        Valida análise completa
        
        Args:
            analise: Dicionário com análise da IA
            ticker: Código da ação
            preco_atual: Preço atual da ação
        
        Returns:
            (valido, lista_de_erros)
        """
        erros = []
        
        # 1. Valida estrutura
        erros.extend(self._validar_estrutura(analise, ticker))
        
        # 2. Valida campos obrigatórios
        erros.extend(self._validar_campos_obrigatorios(analise, ticker))
        
        # 3. Valida tipos de dados
        erros.extend(self._validar_tipos(analise, ticker))
        
        # 4. Valida ranges
        erros.extend(self._validar_ranges(analise, ticker, preco_atual))
        
        # 5. Valida coerência
        erros.extend(self._validar_coerencia(analise, ticker))
        
        valido = len(erros) == 0
        
        if not valido:
            self.erros_comuns.extend(erros)
        
        return valido, erros
    
    def _validar_estrutura(self, analise: Dict, ticker: str) -> List[str]:
        """Valida se é um dicionário válido"""
        erros = []
        
        if not isinstance(analise, dict):
            erros.append(f"{ticker}: Análise não é um dicionário")
            return erros
        
        if len(analise) == 0:
            erros.append(f"{ticker}: Análise vazia")
        
        return erros
    
    def _validar_campos_obrigatorios(self, analise: Dict, ticker: str) -> List[str]:
        """Valida presença de campos obrigatórios"""
        erros = []
        
        for campo in self.CAMPOS_OBRIGATORIOS:
            if campo not in analise:
                erros.append(f"{ticker}: Campo '{campo}' ausente")
        
        return erros
    
    def _validar_tipos(self, analise: Dict, ticker: str) -> List[str]:
        """Valida tipos de dados"""
        erros = []
        
        # Numéricos
        campos_numericos = {
            "preco_teto": (int, float),
            "upside": (int, float),
            "score": (int, float)
        }
        
        for campo, tipos in campos_numericos.items():
            if campo in analise:
                if not isinstance(analise[campo], tipos):
                    erros.append(f"{ticker}: '{campo}' deve ser numérico")
        
        # Strings
        if "recomendacao" in analise:
            if not isinstance(analise["recomendacao"], str):
                erros.append(f"{ticker}: 'recomendacao' deve ser string")
        
        # Listas
        campos_lista = ["riscos", "catalisadores"]
        for campo in campos_lista:
            if campo in analise:
                if not isinstance(analise[campo], list):
                    erros.append(f"{ticker}: '{campo}' deve ser lista")
        
        return erros
    
    def _validar_ranges(self, analise: Dict, ticker: str, preco_atual: float) -> List[str]:
        """Valida ranges de valores"""
        erros = []
        
        # Preço teto
        if "preco_teto" in analise:
            preco_teto = analise["preco_teto"]
            
            if preco_teto <= 0:
                erros.append(f"{ticker}: Preço teto deve ser positivo")
            
            if preco_atual > 0:
                # Preço teto não pode ser muito diferente do atual
                ratio = preco_teto / preco_atual
                if ratio < 0.5 or ratio > 3.0:
                    erros.append(f"{ticker}: Preço teto muito distante do atual (ratio: {ratio:.2f})")
        
        # Upside
        if "upside" in analise:
            upside = analise["upside"]
            
            if upside < -90 or upside > 500:
                erros.append(f"{ticker}: Upside fora do range (-90% a 500%): {upside}%")
        
        # Score
        if "score" in analise:
            score = analise["score"]
            
            if score < 0 or score > 10:
                erros.append(f"{ticker}: Score fora do range (0-10): {score}")
        
        # Recomendação
        if "recomendacao" in analise:
            rec = analise["recomendacao"].upper()
            
            if rec not in self.RECOMENDACOES_VALIDAS:
                erros.append(f"{ticker}: Recomendação inválida: '{rec}'")
        
        return erros
    
    def _validar_coerencia(self, analise: Dict, ticker: str) -> List[str]:
        """Valida coerência lógica entre campos"""
        erros = []
        
        recomendacao = analise.get("recomendacao", "").upper()
        upside = analise.get("upside", 0)
        score = analise.get("score", 0)
        
        # COMPRA FORTE deve ter upside alto
        if recomendacao == "COMPRA FORTE":
            if upside < 15:
                erros.append(f"{ticker}: COMPRA FORTE com upside baixo ({upside}%)")
            if score < 7:
                erros.append(f"{ticker}: COMPRA FORTE com score baixo ({score})")
        
        # VENDA não deve ter upside positivo alto
        if recomendacao == "VENDA":
            if upside > 10:
                erros.append(f"{ticker}: VENDA com upside positivo ({upside}%)")
        
        # Score alto deve ter upside razoável
        if score >= 8 and upside < 10:
            erros.append(f"{ticker}: Score alto ({score}) mas upside baixo ({upside}%)")
        
        # Score baixo não deve ter COMPRA FORTE
        if score < 5 and recomendacao == "COMPRA FORTE":
            erros.append(f"{ticker}: Score baixo ({score}) com COMPRA FORTE")
        
        # Riscos e catalisadores não devem estar vazios
        if len(analise.get("riscos", [])) == 0:
            erros.append(f"{ticker}: Lista de riscos vazia")
        
        if len(analise.get("catalisadores", [])) == 0:
            erros.append(f"{ticker}: Lista de catalisadores vazia")
        
        return erros
    
    def extrair_json_da_resposta(self, resposta: str) -> Optional[Dict]:
        """
        Extrai JSON da resposta da IA
        
        Trata casos comuns:
        - JSON dentro de markdown (```json)
        - JSON com texto antes/depois
        - JSON malformado
        """
        import json
        
        # Remove markdown
        if "```json" in resposta:
            resposta = resposta.split("```json")[1].split("```")[0]
        elif "```" in resposta:
            resposta = resposta.split("```")[1].split("```")[0]
        
        # Tenta encontrar JSON com regex
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, resposta, re.DOTALL)
        
        if matches:
            # Tenta parsear cada match
            for match in matches:
                try:
                    return json.loads(match)
                except:
                    continue
        
        # Tenta parsear direto
        try:
            return json.loads(resposta.strip())
        except:
            return None
    
    def obter_estatisticas_erros(self) -> Dict:
        """Retorna estatísticas dos erros mais comuns"""
        if not self.erros_comuns:
            return {"total_erros": 0, "erros_por_tipo": {}}
        
        erros_por_tipo = {}
        for erro in self.erros_comuns:
            # Extrai tipo do erro (parte após o ticker)
            if ":" in erro:
                tipo = erro.split(":", 1)[1].strip().split()[0]
                erros_por_tipo[tipo] = erros_por_tipo.get(tipo, 0) + 1
        
        return {
            "total_erros": len(self.erros_comuns),
            "erros_por_tipo": erros_por_tipo
        }
