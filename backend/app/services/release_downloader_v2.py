"""
Release Downloader V2 - Versão melhorada com busca mais agressiva
Busca Q3 2025 (mais recente disponível)
"""
import aiohttp
from bs4 import BeautifulSoup
import os
from datetime import datetime
from typing import Optional, Dict, List
import re


class ReleaseDownloaderV2:
    """
    Versão melhorada do Release Downloader
    
    MELHORIAS:
    - Busca Q3 2025 primeiro (mais recente)
    - Mais variações de URLs
    - Busca mais flexível (case-insensitive, variações)
    - Procura em data-href, data-url, etc
    """
    
    def __init__(self):
        # URLs de RI das principais empresas
        self.base_urls = {
            # Energia
            "PRIO3": "https://ri.prioenergia.com.br",
            "PETR3": "https://ri.petrobras.com.br",
            "PETR4": "https://ri.petrobras.com.br",
            "ELET3": "https://ri.eletrobras.com",
            "ELET6": "https://ri.eletrobras.com",
            "CPLE6": "https://ri.cpfl.com.br",
            "ENGI11": "https://ri.engie.com.br",
            
            # Mineração
            "VALE3": "https://ri.vale.com",
            
            # Bancos
            "ITUB3": "https://www.itau.com.br/relacoes-com-investidores",
            "ITUB4": "https://www.itau.com.br/relacoes-com-investidores",
            "BBDC3": "https://ri.bradesco.com.br",
            "BBDC4": "https://ri.bradesco.com.br",
            "BBAS3": "https://ri.bb.com.br",
            "SANB11": "https://ri.santander.com.br",
            
            # Industrial
            "WEGE3": "https://ri.weg.net",
            "EMBR3": "https://ri.embraer.com.br",
            
            # Varejo
            "RENT3": "https://ri.locamerica.com.br",
            "MGLU3": "https://ri.magazineluiza.com.br",
            "LREN3": "https://ri.lojasrenner.com.br",
            "ARZZ3": "https://ri.arezzo.com.br",
            "PETZ3": "https://ri.petz.com.br",
            
            # Saúde
            "RADL3": "https://ri.rd.com.br",
            "HAPV3": "https://ri.hapvida.com.br",
            "FLRY3": "https://ri.fleury.com.br",
            
            # Papel e Celulose
            "SUZB3": "https://ri.suzano.com.br",
            
            # Alimentos e Bebidas
            "ABEV3": "https://ri.ambev.com.br",
            "JBSS3": "https://ri.jbs.com.br",
            "BRFS3": "https://ri.brf-global.com",
            
            # Telecomunicações
            "VIVT3": "https://ri.telefonica.com.br",
            "TIMS3": "https://ri.tim.com.br",
            
            # Construção
            "CYRE3": "https://ri.cyrela.com.br",
            "MRVE3": "https://ri.mrv.com.br",
            
            # Logística
            "RAIL3": "https://ri.rumo.com.br",
            
            # Siderurgia
            "GGBR4": "https://ri.gerdau.com.br",
            "CSNA3": "https://ri.csn.com.br",
            
            # Educação
            "COGN3": "https://ri.cogna.com.br",
            "YDUQ3": "https://ri.yduqs.com.br",
        }
        
        self.cache_dir = "data/releases"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        print("✓ Release Downloader V2 inicializado (busca Q3 2025)")
    
    async def buscar_release_mais_recente(self, ticker: str) -> Optional[Dict]:
        """
        Busca Release mais recente (Q3 2025 → Q2 2025 → Q1 2025 → Q4 2024)
        
        Returns:
            Dict com informações do release ou None
        """
        
        # Ordem de preferência
        trimestres = [
            ("Q3", 2025), ("Q2", 2025), ("Q1", 2025),
            ("Q4", 2024), ("Q3", 2024)
        ]
        
        print(f"  🔍 {ticker}: Buscando Release (Q3 2025 → Q4 2024)...")
        
        if ticker not in self.base_urls:
            print(f"    ⚠ {ticker}: URL de RI não configurada")
            return None
        
        base_url = self.base_urls[ticker]
        
        # Tenta cada trimestre
        for trimestre, ano in trimestres:
            release = await self._buscar_trimestre_especifico(ticker, base_url, trimestre, ano)
            if release:
                return release
        
        print(f"    ⚠ {ticker}: Nenhum release encontrado")
        return None
    
    async def _buscar_trimestre_especifico(
        self, 
        ticker: str, 
        base_url: str, 
        trimestre: str, 
        ano: int
    ) -> Optional[Dict]:
        """
        Busca um trimestre específico
        """
        
        # Gera variações do trimestre
        variacoes = self._gerar_variacoes(trimestre, ano)
        
        try:
            async with aiohttp.ClientSession() as session:
                # URLs para tentar
                urls_tentar = [
                    f"{base_url}/resultados",
                    f"{base_url}/central-de-resultados",
                    f"{base_url}/releases",
                    f"{base_url}/comunicados",
                    f"{base_url}/resultados-trimestrais",
                    f"{base_url}/relatorios",
                    f"{base_url}/relatorios-financeiros",
                    f"{base_url}/investidores/resultados",
                    f"{base_url}/pt/resultados",
                    f"{base_url}/pt-br/resultados",
                    base_url,  # Página principal
                ]
                
                for url in urls_tentar:
                    try:
                        async with session.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                            if response.status != 200:
                                continue
                            
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Procura PDFs
                            pdf_links = []
                            pdf_links += soup.find_all('a', href=re.compile(r'\.pdf', re.I))
                            pdf_links += soup.find_all('a', attrs={'data-href': re.compile(r'\.pdf', re.I)})
                            pdf_links += soup.find_all('a', attrs={'data-url': re.compile(r'\.pdf', re.I)})
                            
                            # Verifica cada link
                            for link in pdf_links:
                                href = link.get('href', '') or link.get('data-href', '') or link.get('data-url', '')
                                text = link.text.lower()
                                title = link.get('title', '').lower()
                                
                                texto_completo = f"{text} {href.lower()} {title}"
                                
                                # Verifica se contém alguma variação do trimestre
                                if any(var in texto_completo for var in variacoes):
                                    # Verifica se é release/resultado
                                    keywords = ['resultado', 'release', 'earnings', 'trimestre', 'trimestral', 'iti', 'itr']
                                    if any(kw in texto_completo for kw in keywords):
                                        print(f"    ✓ {ticker}: Encontrado {trimestre} {ano} em {url}")
                                        
                                        # Monta URL completa
                                        pdf_url = href if href.startswith('http') else f"{base_url}{href}"
                                        
                                        return {
                                            "ticker": ticker,
                                            "trimestre": trimestre,
                                            "ano": ano,
                                            "url": pdf_url,
                                            "fonte": url,
                                            "tipo": "release",
                                            "data_relatorio": datetime(ano, self._trimestre_para_mes(trimestre), 1),
                                            "resumo": f"Release {trimestre} {ano} encontrado em {url}"
                                        }
                    
                    except Exception as e:
                        continue
        
        except Exception as e:
            pass
        
        return None
    
    def _gerar_variacoes(self, trimestre: str, ano: int) -> List[str]:
        """
        Gera variações de busca para um trimestre
        
        Ex: Q3 2025 -> ["q3", "3t", "3º", "terceiro", "2025", "3t25", "3t2025", etc]
        """
        num = trimestre.replace("Q", "")
        ano_str = str(ano)
        ano_curto = ano_str[-2:]
        
        variacoes = [
            # Formatos básicos
            f"q{num}",
            f"{num}t",
            f"{num}º",
            f"{num}°",
            ano_str,
            ano_curto,
            # Combinações
            f"q{num}{ano_str}",
            f"q{num}{ano_curto}",
            f"{num}t{ano_str}",
            f"{num}t{ano_curto}",
            f"{num}t {ano_str}",
            f"q{num} {ano_str}",
            # Por extenso
            self._numero_para_extenso(num),
            f"{self._numero_para_extenso(num)} trimestre",
            f"{self._numero_para_extenso(num)} trimestre {ano_str}",
        ]
        
        return [v.lower() for v in variacoes]
    
    def _numero_para_extenso(self, num: str) -> str:
        """Converte número para extenso"""
        extenso = {
            "1": "primeiro",
            "2": "segundo",
            "3": "terceiro",
            "4": "quarto"
        }
        return extenso.get(num, num)
    
    def _trimestre_para_mes(self, trimestre: str) -> int:
        """Converte trimestre para mês final"""
        meses = {"Q1": 3, "Q2": 6, "Q3": 9, "Q4": 12}
        return meses.get(trimestre, 12)


# Singleton
_release_downloader_v2: Optional[ReleaseDownloaderV2] = None


def get_release_downloader_v2() -> ReleaseDownloaderV2:
    """Retorna instância singleton"""
    global _release_downloader_v2
    
    if _release_downloader_v2 is None:
        _release_downloader_v2 = ReleaseDownloaderV2()
    
    return _release_downloader_v2
