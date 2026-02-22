from typing import Dict
from app.models import MacroContext

class MacroLayer:
    """Camada 2: Análise Macro"""
    
    def __init__(self):
        self.sector_sensitivity = {
            "Financeiro": {"juros": 1.5, "inflacao": -0.3},
            "Construção": {"juros": -1.8, "inflacao": -0.5},
            "Varejo": {"juros": -1.2, "inflacao": -1.5},
            "Tecnologia": {"juros": -0.8, "inflacao": 0.2},
            "Energia": {"juros": 0.3, "inflacao": 1.2},
            "Saúde": {"juros": -0.2, "inflacao": 0.5},
            "Industrial": {"juros": -0.6, "inflacao": 0.8},
            "Consumo": {"juros": -1.0, "inflacao": -1.3}
        }
    
    async def fetch_macro_data(self) -> Dict:
        """Busca dados macroeconômicos"""
        return {
            "selic": 10.75,
            "ipca": 4.5
        }
    
    def calculate_sector_weights(self, juros: float, inflacao: float) -> Dict[str, float]:
        """Calcula o peso de cada setor baseado no cenário macro"""
        juros_neutro = 9.0
        inflacao_neutra = 4.5
        
        delta_juros = (juros - juros_neutro) / juros_neutro
        delta_inflacao = (inflacao - inflacao_neutra) / inflacao_neutra
        
        weights = {}
        for sector, sensitivity in self.sector_sensitivity.items():
            weight = 1.0 + (sensitivity["juros"] * delta_juros * 0.1) + \
                           (sensitivity["inflacao"] * delta_inflacao * 0.1)
            weight = max(0.5, min(1.5, weight))
            weights[sector] = round(weight, 2)
        
        return weights
    
    def identify_favored_sectors(self, weights: Dict[str, float]) -> tuple:
        """Identifica setores favorecidos e desfavorecidos"""
        sorted_sectors = sorted(weights.items(), key=lambda x: x[1], reverse=True)
        
        favorecidos = [s[0] for s in sorted_sectors[:3] if s[1] > 1.0]
        desfavorecidos = [s[0] for s in sorted_sectors[-3:] if s[1] < 1.0]
        
        return favorecidos, desfavorecidos
    
    async def process(self) -> MacroContext:
        """Pipeline completo da Camada 2"""
        macro_data = await self.fetch_macro_data()
        
        juros = macro_data["selic"]
        inflacao = macro_data["ipca"]
        
        weights = self.calculate_sector_weights(juros, inflacao)
        favorecidos, desfavorecidos = self.identify_favored_sectors(weights)
        
        return MacroContext(
            juros_selic=juros,
            inflacao_ipca=inflacao,
            setor_favorecido=favorecidos,
            setor_desfavorecido=desfavorecidos,
            peso_ajuste=weights
        )
