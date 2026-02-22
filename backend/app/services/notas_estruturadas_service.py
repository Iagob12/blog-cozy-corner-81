"""
Serviço de Notas Estruturadas — Calcula notas baseado em critérios objetivos

Valida notas da IA e força reanálise se divergir muito
"""
from typing import Dict, Tuple


class NotasEstruturadasService:
    """
    Calcula notas baseado em critérios objetivos
    
    Fórmula:
    NOTA = (Fundamentos × 0.3) + (Catalisadores × 0.3) + 
           (Valuation × 0.2) + (Gestão × 0.2)
    """
    
    def __init__(self):
        print("✓ Notas Estruturadas Service inicializado")
    
    def calcular_nota(
        self,
        dados_csv: Dict,
        preco_atual: float,
        tem_release: bool,
        setor_quente: bool
    ) -> Tuple[float, Dict]:
        """
        Calcula nota baseado em critérios objetivos
        
        Returns:
            (nota_final, detalhamento)
        """
        # 1. FUNDAMENTOS (0-10)
        nota_fundamentos = self._calcular_fundamentos(dados_csv)
        
        # 2. CATALISADORES (0-10)
        nota_catalisadores = self._calcular_catalisadores(
            tem_release, 
            setor_quente
        )
        
        # 3. VALUATION (0-10)
        nota_valuation = self._calcular_valuation(dados_csv, preco_atual)
        
        # 4. GESTÃO (0-10) — Simplificado
        nota_gestao = self._calcular_gestao(dados_csv)
        
        # NOTA FINAL
        nota_final = (
            nota_fundamentos * 0.3 +
            nota_catalisadores * 0.3 +
            nota_valuation * 0.2 +
            nota_gestao * 0.2
        )
        
        detalhamento = {
            "fundamentos": round(nota_fundamentos, 2),
            "catalisadores": round(nota_catalisadores, 2),
            "valuation": round(nota_valuation, 2),
            "gestao": round(nota_gestao, 2),
            "nota_final": round(nota_final, 2)
        }
        
        return round(nota_final, 2), detalhamento

    
    def _calcular_fundamentos(self, dados_csv: Dict) -> float:
        """Calcula nota de fundamentos (0-10)"""
        nota = 0.0
        
        roe = dados_csv.get("roe", 0)
        pl = dados_csv.get("pl", 0)
        cagr = dados_csv.get("cagr", 0)
        
        # ROE (max 4 pontos)
        if roe > 20:
            nota += 4
        elif roe > 15:
            nota += 3
        elif roe > 12:
            nota += 2
        elif roe > 8:
            nota += 1
        
        # P/L (max 3 pontos)
        if 5 <= pl <= 15:
            nota += 3
        elif 15 < pl <= 20:
            nota += 2
        elif 3 < pl < 5:
            nota += 1
        
        # CAGR (max 3 pontos)
        if cagr > 15:
            nota += 3
        elif cagr > 10:
            nota += 2
        elif cagr > 5:
            nota += 1
        
        return min(nota, 10.0)
    
    def _calcular_catalisadores(
        self,
        tem_release: bool,
        setor_quente: bool
    ) -> float:
        """Calcula nota de catalisadores (0-10)"""
        nota = 5.0  # Base
        
        if tem_release:
            nota += 3
        
        if setor_quente:
            nota += 2
        
        return min(nota, 10.0)
    
    def _calcular_valuation(self, dados_csv: Dict, preco_atual: float) -> float:
        """Calcula nota de valuation (0-10)"""
        nota = 0.0
        
        pl = dados_csv.get("pl", 0)
        
        # P/L (max 7 pontos)
        if pl < 10:
            nota += 5
        elif pl < 15:
            nota += 4
        elif pl < 20:
            nota += 3
        elif pl < 25:
            nota += 2
        
        # Upside estimado (simplificado - max 3 pontos)
        # Assume upside baseado em P/L
        if pl < 12:
            nota += 3  # Potencial alto
        elif pl < 18:
            nota += 2  # Potencial médio
        else:
            nota += 1  # Potencial baixo
        
        return min(nota, 10.0)
    
    def _calcular_gestao(self, dados_csv: Dict) -> float:
        """Calcula nota de gestão (0-10) — Simplificado"""
        # Baseado em crescimento consistente
        cagr = dados_csv.get("cagr", 0)
        roe = dados_csv.get("roe", 0)
        
        nota = 5.0  # Base
        
        if cagr > 10:
            nota += 2
        elif cagr > 5:
            nota += 1
        
        if roe > 15:
            nota += 2
        elif roe > 10:
            nota += 1
        
        return min(nota, 10.0)
    
    def validar_nota_ia(
        self,
        nota_ia: float,
        nota_calculada: float,
        max_divergencia: float = 1.5
    ) -> Tuple[bool, str]:
        """
        Valida se nota da IA está coerente
        
        Args:
            nota_ia: Nota dada pela IA
            nota_calculada: Nota calculada pelos critérios
            max_divergencia: Divergência máxima aceitável
        
        Returns:
            (valido, mensagem)
        """
        divergencia = abs(nota_ia - nota_calculada)
        
        if divergencia <= max_divergencia:
            return True, f"OK (divergência: {divergencia:.2f})"
        else:
            return False, f"Divergência alta: {divergencia:.2f} (IA: {nota_ia}, Calc: {nota_calculada})"


# Singleton
_notas_service = None

def get_notas_estruturadas_service() -> NotasEstruturadasService:
    """Retorna instância singleton"""
    global _notas_service
    if _notas_service is None:
        _notas_service = NotasEstruturadasService()
    return _notas_service
