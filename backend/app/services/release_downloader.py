"""
Release de Resultados Downloader
Busca e baixa PDFs de Release de Resultados das empresas
"""
import aiohttp
from bs4 import BeautifulSoup
import os
from datetime import datetime
from typing import Optional, Dict
import re

class ReleaseDownloader:
    """Baixa Release de Resultados das empresas"""
    
    def __init__(self):
        self.base_urls = {
            # URLs de RI das principais empresas brasileiras
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
            
            # Adicione mais conforme necessário
        }
        
        self.cache_dir = "data/releases"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        print("✓ Release Downloader inicializado")
    
    async def buscar_release_mais_recente(self, ticker: str, trimestres_aceitos: list = None) -> Optional[str]:
        """
        Busca o Release de Resultados mais recente
        
        ESTRATÉGIA ATUALIZADA:
        1. Tenta Q3 2025 (mais recente disponível)
        2. Se não encontrar, tenta Q2 2025
        3. Se não encontrar, tenta Q1 2025
        4. Se não encontrar, tenta Q4 2024
        5. Se não encontrar, tenta Q3 2024
        
        Args:
            ticker: Ticker da ação
            trimestres_aceitos: Lista de trimestres aceitos (ex: ["Q3 2025", "Q2 2025"])
        
        Returns:
            Caminho do PDF ou None
        """
        
        if trimestres_aceitos is None:
            # Ordem de preferência: Q3 2025 → Q2 2025 → Q1 2025 → Q4 2024 → Q3 2024
            # IMPORTANTE: Q3 2025 já deve estar disponível (estamos em fevereiro 2026)
            trimestres_aceitos = [
                # 2025 (mais recente)
                "Q3 2025", "3T 2025", "3T25", "3º trimestre 2025", "terceiro trimestre 2025",
                "Q2 2025", "2T 2025", "2T25", "2º trimestre 2025", "segundo trimestre 2025",
                "Q1 2025", "1T 2025", "1T25", "1º trimestre 2025", "primeiro trimestre 2025",
                # 2024 (fallback)
                "Q4 2024", "4T 2024", "4T24", "4º trimestre 2024", "quarto trimestre 2024",
                "Q3 2024", "3T 2024", "3T24", "3º trimestre 2024", "terceiro trimestre 2024",
            ]
        
        # Verifica se já tem em cache
        cached = self._verificar_cache(ticker)
        if cached:
            print(f"  ✓ {ticker}: Release em cache")
            return cached
        
        # Tenta baixar
        print(f"  🔍 {ticker}: Buscando Release (Q3 2025 → Q2 2025 → Q1 2025 → Q4 2024)...")
        
        # Estratégia 1: Site de RI específico
        if ticker in self.base_urls:
            pdf_path = await self._baixar_de_ri(ticker, trimestres_aceitos)
            if pdf_path:
                return pdf_path
        
        # Estratégia 2: Google Search (simulado)
        pdf_path = await self._buscar_via_google(ticker, trimestres_aceitos)
        if pdf_path:
            return pdf_path
        
        print(f"  ⚠ {ticker}: Release não encontrado (tentou Q3 2025 → Q4 2024)")
        return None
    
    def _verificar_cache(self, ticker: str) -> Optional[str]:
        """Verifica se já tem PDF em cache (últimos 90 dias)"""
        
        import glob
        pattern = f"{self.cache_dir}/{ticker}_*.pdf"
        files = glob.glob(pattern)
        
        if files:
            # Pega o mais recente
            latest = max(files, key=os.path.getmtime)
            
            # Verifica se tem menos de 90 dias
            file_time = datetime.fromtimestamp(os.path.getmtime(latest))
            days_old = (datetime.now() - file_time).days
            
            if days_old < 90:
                return latest
        
        return None
    
    async def _baixar_de_ri(self, ticker: str, trimestres_aceitos: list) -> Optional[str]:
        """
        Baixa PDF do site de RI da empresa
        Tenta múltiplos trimestres em ordem de preferência
        """
        
        base_url = self.base_urls.get(ticker)
        if not base_url:
            return None
        
        try:
            async with aiohttp.ClientSession() as session:
                # Acessa página de resultados
                urls_tentar = [
                    f"{base_url}/resultados",
                    f"{base_url}/central-de-resultados",
                    f"{base_url}/releases",
                    f"{base_url}/comunicados"
                ]
                
                for url in urls_tentar:
                    try:
                        async with session.get(url, timeout=10) as response:
                            if response.status == 200:
                                html = await response.text()
                                soup = BeautifulSoup(html, 'html.parser')
                                
                                # Procura links de PDF
                                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.I))
                                
                                # Filtra por trimestres aceitos (ordem de preferência)
                                for trimestre in trimestres_aceitos:
                                    trimestre_lower = trimestre.lower()
                                    
                                    for link in pdf_links:
                                        href = link.get('href', '')
                                        text = link.text.lower()
                                        
                                        # Verifica se contém o trimestre
                                        if trimestre_lower in text or trimestre_lower in href.lower():
                                            # Verifica se é resultado/release
                                            if any(kw in text or kw in href.lower() for kw in ['resultado', 'release', 'earnings']):
                                                # Encontrou! Baixa o PDF
                                                pdf_url = href if href.startswith('http') else f"{base_url}{href}"
                                                
                                                print(f"    ✓ Encontrado: {trimestre}")
                                                pdf_path = await self._download_pdf(session, pdf_url, ticker, trimestre)
                                                if pdf_path:
                                                    return pdf_path
                    except:
                        continue
        
        except Exception as e:
            print(f"    Erro ao buscar no RI: {e}")
        
        return None
    
    async def _buscar_via_google(self, ticker: str, trimestres_aceitos: list) -> Optional[str]:
        """
        Busca via Google (simulado - retorna placeholder)
        
        TODO: Implementar Google Custom Search API
        Exemplo de query: "{ticker} release resultados Q3 2025 filetype:pdf"
        """
        
        # Em produção, você pode usar Google Custom Search API
        # Por enquanto, retorna None
        return None
    
    async def _download_pdf(self, session: aiohttp.ClientSession, url: str, ticker: str, trimestre: str = "") -> Optional[str]:
        """
        Baixa um PDF
        
        Args:
            session: Sessão aiohttp
            url: URL do PDF
            ticker: Ticker da ação
            trimestre: Trimestre do relatório (ex: "Q3 2025")
        """
        
        try:
            async with session.get(url, timeout=30) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # Salva com trimestre no nome
                    if trimestre:
                        trimestre_clean = trimestre.replace(" ", "_")
                        filename = f"{ticker}_{trimestre_clean}.pdf"
                    else:
                        timestamp = datetime.now().strftime("%Y%m%d")
                        filename = f"{ticker}_{timestamp}.pdf"
                    
                    filepath = os.path.join(self.cache_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(content)
                    
                    print(f"    ✓ PDF baixado: {filename}")
                    return filepath
        
        except Exception as e:
            print(f"    Erro ao baixar PDF: {e}")
        
        return None
    
    async def extrair_texto_pdf(self, pdf_path: str) -> str:
        """Extrai texto do PDF usando PyPDF2"""
        
        try:
            from PyPDF2 import PdfReader
            
            reader = PdfReader(pdf_path)
            texto = ""
            
            # Extrai primeiras 10 páginas (suficiente para análise)
            for page in reader.pages[:10]:
                texto += page.extract_text() + "\n"
            
            return texto
        
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
            return ""
    
    async def extrair_trimestre_do_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        Extrai trimestre e data do PDF usando regex
        
        Procura por padrões como:
        - "Q3 2025", "3T 2025", "3T25"
        - "Terceiro Trimestre de 2025"
        - "Resultados do 3º Trimestre"
        
        Returns:
            Dict com: trimestre, ano, data_publicacao, confianca
        """
        
        try:
            texto = await self.extrair_texto_pdf(pdf_path)
            
            if not texto:
                return {
                    "trimestre": "Q3",
                    "ano": 2025,
                    "data_publicacao": None,
                    "confianca": "BAIXA",
                    "metodo": "fallback"
                }
            
            # Padrões de regex para trimestre
            import re
            
            # Padrão 1: Q3 2025, 3T 2025, 3T25
            pattern1 = r'(?:Q|q)?([1-4])[TtºQq]\s*(?:de\s*)?(\d{4}|\d{2})'
            match1 = re.search(pattern1, texto[:2000])  # Primeiras 2000 chars
            
            if match1:
                trimestre_num = int(match1.group(1))
                ano_str = match1.group(2)
                ano = int(ano_str) if len(ano_str) == 4 else 2000 + int(ano_str)
                
                return {
                    "trimestre": f"Q{trimestre_num}",
                    "ano": ano,
                    "data_publicacao": None,
                    "confianca": "ALTA",
                    "metodo": "regex_pattern1"
                }
            
            # Padrão 2: Terceiro Trimestre de 2025
            trimestres_texto = {
                "primeiro": 1, "1º": 1, "1°": 1,
                "segundo": 2, "2º": 2, "2°": 2,
                "terceiro": 3, "3º": 3, "3°": 3,
                "quarto": 4, "4º": 4, "4°": 4
            }
            
            for texto_trim, num in trimestres_texto.items():
                pattern2 = rf'{texto_trim}\s+trimestre\s+(?:de\s+)?(\d{{4}})'
                match2 = re.search(pattern2, texto[:2000], re.IGNORECASE)
                
                if match2:
                    ano = int(match2.group(1))
                    return {
                        "trimestre": f"Q{num}",
                        "ano": ano,
                        "data_publicacao": None,
                        "confianca": "ALTA",
                        "metodo": "regex_pattern2"
                    }
            
            # Padrão 3: Data de publicação (dd/mm/yyyy)
            pattern_data = r'(\d{2})[/-](\d{2})[/-](\d{4})'
            match_data = re.search(pattern_data, texto[:1000])
            
            if match_data:
                dia = int(match_data.group(1))
                mes = int(match_data.group(2))
                ano = int(match_data.group(3))
                
                # Infere trimestre baseado no mês
                if mes <= 3:
                    trimestre = "Q1"
                elif mes <= 6:
                    trimestre = "Q2"
                elif mes <= 9:
                    trimestre = "Q3"
                else:
                    trimestre = "Q4"
                
                from datetime import datetime
                data_pub = datetime(ano, mes, dia)
                
                return {
                    "trimestre": trimestre,
                    "ano": ano,
                    "data_publicacao": data_pub.strftime("%d/%m/%Y"),
                    "confianca": "MÉDIA",
                    "metodo": "inferido_da_data"
                }
            
            # Fallback: assume Q3 2025
            print(f"    ⚠ Não conseguiu extrair trimestre do PDF, assumindo Q3 2025")
            return {
                "trimestre": "Q3",
                "ano": 2025,
                "data_publicacao": None,
                "confianca": "BAIXA",
                "metodo": "fallback"
            }
        
        except Exception as e:
            print(f"    Erro ao extrair trimestre: {e}")
            return {
                "trimestre": "Q3",
                "ano": 2025,
                "data_publicacao": None,
                "confianca": "BAIXA",
                "metodo": "erro"
            }
        """Prepara resumo do Release para análise"""
        
        texto = await self.extrair_texto_pdf(pdf_path)
        
        if not texto:
            return {
                "ticker": ticker,
                "disponivel": False,
                "resumo": "Release não disponível"
            }
        
        # Extrai informações chave (regex simples)
        receita = self._extrair_valor(texto, r'receita.*?(\d+[.,]\d+)', 'milhões')
        lucro = self._extrair_valor(texto, r'lucro.*?(\d+[.,]\d+)', 'milhões')
        ebitda = self._extrair_valor(texto, r'ebitda.*?(\d+[.,]\d+)', 'milhões')
        
        return {
            "ticker": ticker,
            "disponivel": True,
            "pdf_path": pdf_path,
            "texto_completo": texto[:5000],  # Primeiros 5000 chars
            "trimestre": info_trimestre["trimestre"],
            "ano": info_trimestre["ano"],
            "data_publicacao": info_trimestre.get("data_publicacao"),
            "confianca_trimestre": info_trimestre["confianca"],
            "metricas": {
                "receita": receita,
                "lucro": lucro,
                "ebitda": ebitda
            }
        }
    
    def _extrair_valor(self, texto: str, pattern: str, unidade: str) -> str:
        """Extrai valor usando regex"""
        
        import re
        match = re.search(pattern, texto.lower())
        if match:
            return f"{match.group(1)} {unidade}"
        return "N/A"
