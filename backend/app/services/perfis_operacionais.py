"""
PERFIS OPERACIONAIS A/B
Define critérios específicos para cada tipo de operação
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass
import pandas as pd


@dataclass
class CriteriosPerfil:
    """Critérios de um perfil operacional"""
    nome: str
    descricao: str
    horizonte: str
    roe_min: float
    pl_max: float
    roic_min: float
    divida_ebitda_max: float
    margem_ebitda_min: float = None
    margem_liquida_min: float = None
    cagr_receita_min: float = None
    cagr_lucro_min: float = None
    liquidez_corrente_min: float = 0.7


class PerfisOperacionais:
    """
    Gerencia os perfis operacionais A e B
    
    PERFIL A — MOMENTUM RÁPIDO (2 a 15 dias):
    - ROE > 12%
    - P/L < 15
    - ROIC > 10%
    - Dívida/EBITDA < 3,0
    - Margem EBITDA > 10%
    - Setor com catalisador no macro
    
    PERFIL B — POSIÇÃO CONSISTENTE (1 a 3 meses):
    - ROE > 15%
    - CAGR Receita > 8%
    - CAGR Lucro > 10%
    - Dívida/EBITDA < 2,5
    - Margem Líquida > 8%
    - Setor com vento a favor
    """
    
    PERFIL_A = CriteriosPerfil(
        nome="A",
        descricao="MOMENTUM RÁPIDO",
        horizonte="2 a 15 dias",
        roe_min=10.0,  # Reduzido de 12% para 10%
        pl_max=20.0,   # Aumentado de 15 para 20
        roic_min=8.0,  # Reduzido de 10% para 8%
        divida_ebitda_max=3.5,  # Aumentado de 3.0 para 3.5
        margem_ebitda_min=8.0,  # Reduzido de 10% para 8%
        liquidez_corrente_min=0.7
    )
    
    PERFIL_B = CriteriosPerfil(
        nome="B",
        descricao="POSIÇÃO CONSISTENTE",
        horizonte="1 a 3 meses",
        roe_min=12.0,  # Reduzido de 15% para 12%
        pl_max=25.0,  # Mais flexível que A
        roic_min=10.0,  # Reduzido de 12% para 10%
        divida_ebitda_max=3.0,  # Aumentado de 2.5 para 3.0
        margem_liquida_min=6.0,  # Reduzido de 8% para 6%
        cagr_receita_min=5.0,  # Reduzido de 8% para 5%
        cagr_lucro_min=8.0,  # Reduzido de 10% para 8%
        liquidez_corrente_min=0.7
    )
    
    @staticmethod
    def criterios_eliminacao_imediata() -> Dict:
        """
        Critérios de eliminação imediata (sem análise)
        
        ELIMINAÇÃO IMEDIATA:
        - Dívida/EBITDA > 4,0
        - ROE negativo
        - CAGR Receita negativo
        - Setor "a evitar" no macro
        - Liquidez Corrente < 0,7
        """
        return {
            "divida_ebitda_max": 4.0,
            "roe_min": 0.0,
            "cagr_receita_min": 0.0,
            "liquidez_corrente_min": 0.7
        }
    
    @staticmethod
    def aplicar_eliminacao_imediata(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
        """
        Aplica critérios de eliminação imediata
        
        Returns:
            (df_filtrado, motivos_descarte)
        """
        # Normaliza nomes de colunas
        df = df.copy()
        column_mapping = {
            'Dívida Líq. / EBITDA': 'divida_ebitda',
            'Dívida Líq./EBITDA': 'divida_ebitda',
            'Liquidez Corrente': 'liquidez_corrente',
            'CAGR de Receita': 'cagr_receita',
            'Margem Líquida': 'margem_liquida',
            'Margem EBITDA': 'margem_ebitda',
            'Margem Bruta': 'margem_bruta',
            'CAGR de Lucro': 'cagr_lucro'
        }
        
        # Renomeia colunas se necessário
        for old_name, new_name in column_mapping.items():
            if old_name in df.columns and new_name not in df.columns:
                df[new_name] = df[old_name]
        
        # Se não tem cagr_receita mas tem cagr, usa cagr
        if 'cagr_receita' not in df.columns and 'cagr' in df.columns:
            df['cagr_receita'] = df['cagr']
        
        criterios = PerfisOperacionais.criterios_eliminacao_imediata()
        motivos = []
        
        total_inicial = len(df)
        
        # Dívida/EBITDA > 4,0
        if 'divida_ebitda' in df.columns:
            antes = len(df)
            df = df[df['divida_ebitda'] <= criterios['divida_ebitda_max']]
            if len(df) < antes:
                motivos.append(f"Dívida/EBITDA > {criterios['divida_ebitda_max']}: {antes - len(df)} empresas")
        
        # ROE negativo
        if 'roe' in df.columns:
            antes = len(df)
            df = df[df['roe'] > criterios['roe_min']]
            if len(df) < antes:
                motivos.append(f"ROE negativo: {antes - len(df)} empresas")
        
        # CAGR Receita negativo
        if 'cagr_receita' in df.columns:
            antes = len(df)
            df = df[df['cagr_receita'] >= criterios['cagr_receita_min']]
            if len(df) < antes:
                motivos.append(f"CAGR Receita negativo: {antes - len(df)} empresas")
        
        # Liquidez Corrente < 0,7
        if 'liquidez_corrente' in df.columns:
            antes = len(df)
            df = df[df['liquidez_corrente'] >= criterios['liquidez_corrente_min']]
            if len(df) < antes:
                motivos.append(f"Liquidez Corrente < {criterios['liquidez_corrente_min']}: {antes - len(df)} empresas")
        
        total_eliminadas = total_inicial - len(df)
        if total_eliminadas > 0:
            motivos.insert(0, f"TOTAL ELIMINADAS: {total_eliminadas}/{total_inicial} empresas")
        
        return df, motivos
    
    @staticmethod
    def filtrar_por_perfil(df: pd.DataFrame, perfil: str) -> pd.DataFrame:
        """
        Filtra empresas por perfil (A ou B)
        
        Args:
            df: DataFrame com dados das empresas
            perfil: "A", "B" ou "A+B"
        
        Returns:
            DataFrame filtrado
        """
        if perfil == "A":
            return PerfisOperacionais._filtrar_perfil_a(df)
        elif perfil == "B":
            return PerfisOperacionais._filtrar_perfil_b(df)
        elif perfil == "A+B":
            df_a = PerfisOperacionais._filtrar_perfil_a(df)
            df_b = PerfisOperacionais._filtrar_perfil_b(df)
            # Combina e remove duplicatas
            return pd.concat([df_a, df_b]).drop_duplicates(subset=['ticker'])
        else:
            raise ValueError(f"Perfil inválido: {perfil}. Use 'A', 'B' ou 'A+B'")
    
    @staticmethod
    def _filtrar_perfil_a(df: pd.DataFrame) -> pd.DataFrame:
        """Filtra empresas do Perfil A (Momentum Rápido)"""
        # Normaliza nomes de colunas
        df = df.copy()
        if 'Margem EBITDA' in df.columns and 'margem_ebitda' not in df.columns:
            df['margem_ebitda'] = df['Margem EBITDA']
        if 'Dívida Líq. / EBITDA' in df.columns and 'divida_ebitda' not in df.columns:
            df['divida_ebitda'] = df['Dívida Líq. / EBITDA']
        if 'ROIC' in df.columns and 'roic' not in df.columns:
            df['roic'] = df['ROIC']
        
        criterios = PerfisOperacionais.PERFIL_A
        
        # Valores estão em decimal (0.2864 = 28.64%), então dividimos critérios por 100
        roe_min = criterios.roe_min / 100
        roic_min = criterios.roic_min / 100
        margem_ebitda_min = criterios.margem_ebitda_min / 100
        
        df_filtrado = df[
            (df['roe'] > roe_min) &
            (df['pl'] > 0) &
            (df['pl'] < criterios.pl_max) &
            (df['roic'] > roic_min) &
            (df['divida_ebitda'] < criterios.divida_ebitda_max) &
            (df['margem_ebitda'] > margem_ebitda_min)
        ].copy()
        
        df_filtrado['perfil'] = 'A'
        return df_filtrado
    
    @staticmethod
    def _filtrar_perfil_b(df: pd.DataFrame) -> pd.DataFrame:
        """Filtra empresas do Perfil B (Posição Consistente)"""
        # Normaliza nomes de colunas
        df = df.copy()
        if 'Margem Líquida' in df.columns and 'margem_liquida' not in df.columns:
            df['margem_liquida'] = df['Margem Líquida']
        if 'Dívida Líq. / EBITDA' in df.columns and 'divida_ebitda' not in df.columns:
            df['divida_ebitda'] = df['Dívida Líq. / EBITDA']
        if 'ROIC' in df.columns and 'roic' not in df.columns:
            df['roic'] = df['ROIC']
        if 'cagr' in df.columns and 'cagr_receita' not in df.columns:
            df['cagr_receita'] = df['cagr']
        
        criterios = PerfisOperacionais.PERFIL_B
        
        # Valores estão em decimal (0.2864 = 28.64%), então dividimos critérios por 100
        roe_min = criterios.roe_min / 100
        roic_min = criterios.roic_min / 100
        margem_liquida_min = criterios.margem_liquida_min / 100
        cagr_receita_min = criterios.cagr_receita_min / 100
        
        df_filtrado = df[
            (df['roe'] > roe_min) &
            (df['pl'] > 0) &
            (df['pl'] < criterios.pl_max) &
            (df['roic'] > roic_min) &
            (df['divida_ebitda'] < criterios.divida_ebitda_max) &
            (df['margem_liquida'] > margem_liquida_min) &
            (df['cagr_receita'] > cagr_receita_min)
        ].copy()
        
        df_filtrado['perfil'] = 'B'
        return df_filtrado
    
    @staticmethod
    def identificar_perfil(row: pd.Series) -> str:
        """
        Identifica qual perfil uma empresa se encaixa
        
        Returns:
            "A", "B", "A+B" ou "NENHUM"
        """
        # Normaliza nomes de colunas
        if 'Margem EBITDA' in row.index and 'margem_ebitda' not in row.index:
            row['margem_ebitda'] = row['Margem EBITDA']
        if 'Margem Líquida' in row.index and 'margem_liquida' not in row.index:
            row['margem_liquida'] = row['Margem Líquida']
        if 'Dívida Líq. / EBITDA' in row.index and 'divida_ebitda' not in row.index:
            row['divida_ebitda'] = row['Dívida Líq. / EBITDA']
        if 'ROIC' in row.index and 'roic' not in row.index:
            row['roic'] = row['ROIC']
        if 'cagr' in row.index and 'cagr_receita' not in row.index:
            row['cagr_receita'] = row['cagr']
        
        # Valores já estão em decimal (0.2864 = 28.64%), então comparamos diretamente
        roe = row['roe']
        roic = row['roic']
        margem_ebitda = row['margem_ebitda']
        margem_liquida = row['margem_liquida']
        cagr = row['cagr_receita']
        
        # Verifica Perfil A (critérios em decimal)
        perfil_a = (
            roe > PerfisOperacionais.PERFIL_A.roe_min / 100 and
            row['pl'] > 0 and
            row['pl'] < PerfisOperacionais.PERFIL_A.pl_max and
            roic > PerfisOperacionais.PERFIL_A.roic_min / 100 and
            row['divida_ebitda'] < PerfisOperacionais.PERFIL_A.divida_ebitda_max and
            margem_ebitda > PerfisOperacionais.PERFIL_A.margem_ebitda_min / 100
        )
        
        # Verifica Perfil B (critérios em decimal)
        perfil_b = (
            roe > PerfisOperacionais.PERFIL_B.roe_min / 100 and
            row['pl'] > 0 and
            row['pl'] < PerfisOperacionais.PERFIL_B.pl_max and
            roic > PerfisOperacionais.PERFIL_B.roic_min / 100 and
            row['divida_ebitda'] < PerfisOperacionais.PERFIL_B.divida_ebitda_max and
            margem_liquida > PerfisOperacionais.PERFIL_B.margem_liquida_min / 100 and
            cagr > PerfisOperacionais.PERFIL_B.cagr_receita_min / 100
        )
        
        if perfil_a and perfil_b:
            return "A+B"
        elif perfil_a:
            return "A"
        elif perfil_b:
            return "B"
        else:
            return "NENHUM"
    
    @staticmethod
    def obter_descricao_perfil(perfil: str) -> str:
        """Retorna descrição do perfil"""
        if perfil == "A":
            return f"{PerfisOperacionais.PERFIL_A.descricao} ({PerfisOperacionais.PERFIL_A.horizonte})"
        elif perfil == "B":
            return f"{PerfisOperacionais.PERFIL_B.descricao} ({PerfisOperacionais.PERFIL_B.horizonte})"
        elif perfil == "A+B":
            return "AMBOS OS PERFIS (flexível)"
        else:
            return "Nenhum perfil identificado"
    
    @staticmethod
    def obter_criterios_perfil(perfil: str) -> Dict:
        """Retorna critérios do perfil em formato dict"""
        if perfil == "A":
            c = PerfisOperacionais.PERFIL_A
            return {
                "nome": c.nome,
                "descricao": c.descricao,
                "horizonte": c.horizonte,
                "roe_min": c.roe_min,
                "pl_max": c.pl_max,
                "roic_min": c.roic_min,
                "divida_ebitda_max": c.divida_ebitda_max,
                "margem_ebitda_min": c.margem_ebitda_min
            }
        elif perfil == "B":
            c = PerfisOperacionais.PERFIL_B
            return {
                "nome": c.nome,
                "descricao": c.descricao,
                "horizonte": c.horizonte,
                "roe_min": c.roe_min,
                "pl_max": c.pl_max,
                "roic_min": c.roic_min,
                "divida_ebitda_max": c.divida_ebitda_max,
                "margem_liquida_min": c.margem_liquida_min,
                "cagr_receita_min": c.cagr_receita_min,
                "cagr_lucro_min": c.cagr_lucro_min
            }
        else:
            return {}
