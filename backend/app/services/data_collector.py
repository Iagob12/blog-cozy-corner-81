"""
Data Collector Service
Coleta dados de múltiplas fontes para análise
"""
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import pandas as pd
from datetime import datetime
import os
import re

class DataCollector:
    """Coleta dados de ações de múltiplas fontes"""
    
    def __init__(self):
        self.investimentos_url = "https://investimentos.com.br/ativos/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def download_investimentos_csv(self, output_path: str = "data/acoes_brasil.csv") -> str:
        """
        Baixa o CSV de ações do investimentos.com.br
        """
        try:
            # URL do CSV exportado (pode precisar ajustar)
            csv_url = "https://investimentos.com.br/acoes/ranking"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(csv_url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Salva o CSV
                        os.makedirs(os.path.dirname(output_path), exist_ok=True)
                        with open(output_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        return output_path
        except Exception as e:
            print(f"Erro ao baixar CSV: {e}")
        
        return None
    
    async def scrape_investimentos_data(self) -> pd.DataFrame:
        """
        Faz scraping da página de ações do investimentos.com.br
        Alternativa caso o CSV não esteja disponível
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.investimentos_url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extrai dados da tabela
                        acoes = []
                        
                        # Procura por tabelas de ações
                        tables = soup.find_all('table')
                        for table in tables:
                            rows = table.find_all('tr')
                            for row in rows[1:]:  # Pula header
                                cols = row.find_all('td')
                                if len(cols) >= 5:
                                    try:
                                        acao = {
                                            'Ticker': cols[0].text.strip(),
                                            'Preço': self._parse_number(cols[1].text),
                                            'P/L': self._parse_number(cols[2].text),
                                            'ROE': self._parse_number(cols[3].text),
                                            'DY': self._parse_number(cols[4].text)
                                        }
                                        acoes.append(acao)
                                    except:
                                        continue
                        
                        if acoes:
                            return pd.DataFrame(acoes)
        
        except Exception as e:
            print(f"Erro no scraping: {e}")
        
        return pd.DataFrame()
    
    async def buscar_relatorio_ri(self, ticker: str) -> Optional[Dict]:
        """
        Busca o relatório de resultados mais recente de uma empresa
        """
        # URLs de RI das principais empresas
        ri_urls = {
            "PRIO3": "https://ri.prioenergia.com.br/",
            "VULC3": "https://ri.vulcabras.com.br/",
            "GMAT3": "https://ri.grupomateus.com.br/",
            "CURY3": "https://ri.cury.com.br/",
            "POMO3": "https://ri.marcopolo.com.br/",
            "PETR4": "https://ri.petrobras.com.br/",
            "VALE3": "https://ri.vale.com/",
            "ITUB4": "https://www.itau.com.br/relacoes-com-investidores/",
            "BBDC4": "https://ri.bradesco.com.br/",
            "ABEV3": "https://ri.ambev.com.br/",
            "WEGE3": "https://ri.weg.net/",
            "RENT3": "https://ri.localiza.com/",
            "SUZB3": "https://ri.suzano.com.br/",
            "RAIL3": "https://ri.rumo.com.br/",
            "RADL3": "https://ri.rd.com.br/"
        }
        
        base_ticker = ticker.replace('.SA', '')
        url = ri_urls.get(base_ticker)
        
        if not url:
            # Tenta construir URL padrão
            empresa = base_ticker.replace('3', '').replace('4', '').lower()
            url = f"https://ri.{empresa}.com.br/"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=15) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Procura por links de PDF de resultados
                        pdf_links = []
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            text = link.text.lower()
                            
                            # Identifica PDFs de resultados
                            if ('.pdf' in href.lower() and 
                                any(keyword in text for keyword in 
                                    ['resultado', 'trimestre', '4t', '3t', '2t', '1t', 
                                     'earnings', 'release', 'demonstra'])):
                                
                                # Converte para URL absoluta
                                if not href.startswith('http'):
                                    from urllib.parse import urljoin
                                    href = urljoin(url, href)
                                
                                pdf_links.append({
                                    'url': href,
                                    'titulo': link.text.strip(),
                                    'ticker': ticker
                                })
                        
                        # Retorna o mais recente (primeiro da lista geralmente)
                        if pdf_links:
                            return pdf_links[0]
        
        except Exception as e:
            print(f"Erro ao buscar RI de {ticker}: {e}")
        
        return None
    
    async def download_pdf(self, url: str, ticker: str, output_dir: str = "data/pdfs") -> Optional[str]:
        """
        Baixa um PDF de relatório
        """
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            filename = f"{ticker}_{datetime.now().strftime('%Y%m%d')}.pdf"
            filepath = os.path.join(output_dir, filename)
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=60) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        
                        return filepath
        
        except Exception as e:
            print(f"Erro ao baixar PDF de {ticker}: {e}")
        
        return None
    
    async def coletar_relatorios_batch(self, tickers: List[str]) -> List[Dict]:
        """
        Coleta relatórios de múltiplas empresas em paralelo
        """
        tasks = [self.buscar_relatorio_ri(ticker) for ticker in tickers]
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        relatorios = []
        for ticker, resultado in zip(tickers, resultados):
            if isinstance(resultado, dict) and resultado:
                relatorios.append(resultado)
        
        return relatorios
    
    def _parse_number(self, text: str) -> float:
        """
        Converte texto em número
        """
        try:
            # Remove caracteres não numéricos exceto . , -
            text = re.sub(r'[^\d.,-]', '', text)
            # Substitui vírgula por ponto
            text = text.replace(',', '.')
            return float(text)
        except:
            return 0.0
    
    async def enriquecer_dados_com_fundamentus(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Enriquece dados com informações do Fundamentus
        """
        try:
            url = "https://www.fundamentus.com.br/resultado.php"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=30) as response:
                    if response.status == 200:
                        html = await response.text()
                        
                        # Usa pandas para ler a tabela HTML
                        import io
                        tables = pd.read_html(io.StringIO(html))
                        
                        if tables:
                            fundamentus_df = tables[0]
                            
                            # Merge com dados existentes
                            if 'Papel' in fundamentus_df.columns:
                                fundamentus_df = fundamentus_df.rename(columns={'Papel': 'Ticker'})
                                df = df.merge(fundamentus_df, on='Ticker', how='left')
                            
                            return df
        
        except Exception as e:
            print(f"Erro ao buscar Fundamentus: {e}")
        
        return df
