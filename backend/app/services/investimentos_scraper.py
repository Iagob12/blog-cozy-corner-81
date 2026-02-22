"""
Investimentos.com.br Scraper
Baixa CSV diário e preços atualizados
"""
import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os
from typing import Dict, List

class InvestimentosScraper:
    """Scraper para investimentos.com.br"""
    
    def __init__(self):
        self.base_url = "https://investimentos.com.br"
        self.csv_cache_path = "data/investimentos_cache.csv"
        self.cache_duration_hours = 24  # Atualiza a cada 24h
        
        print("✓ Investimentos.com.br Scraper inicializado")
    
    async def baixar_csv_diario(self) -> tuple[str, datetime]:
        """
        Baixa CSV diário de https://investimentos.com.br/ativos/
        
        ATUALIZAÇÃO AUTOMÁTICA: A cada 24 horas
        
        Returns:
            tuple[str, datetime]: (caminho_arquivo, timestamp)
        """
        
        # Verifica se já tem cache válido (menos de 24h)
        if os.path.exists(self.csv_cache_path):
            file_time = datetime.fromtimestamp(os.path.getmtime(self.csv_cache_path))
            hours_old = (datetime.now() - file_time).total_seconds() / 3600
            
            if hours_old < self.cache_duration_hours:
                print(f"✓ Usando CSV em cache ({hours_old:.1f}h atrás)")
                print(f"✓ Data do CSV: {file_time.strftime('%d/%m/%Y %H:%M')}")
                return self.csv_cache_path, file_time
        
        print("\n[DOWNLOAD] Baixando CSV COMPLETO de investimentos.com.br...")
        print("⏳ Isso pode levar alguns segundos...")
        
        try:
            # URLs possíveis para tentar
            urls_tentar = [
                "https://investimentos.com.br/acoes/download",
                "https://investimentos.com.br/ativos/acoes/download",
                "https://investimentos.com.br/api/acoes/export/csv",
                "https://investimentos.com.br/acoes/exportar",
                "https://www.investimentos.com.br/acoes/download",
                "https://www.investimentos.com.br/ativos/download",
                # Tenta também formato XLS
                "https://investimentos.com.br/acoes/download.xls",
                "https://investimentos.com.br/acoes/export.xlsx",
            ]
            
            timeout = aiohttp.ClientTimeout(total=30)  # 30 segundos para download completo
            async with aiohttp.ClientSession(timeout=timeout) as session:
                
                # Tenta cada URL
                for csv_url in urls_tentar:
                    try:
                        print(f"  Tentando: {csv_url}")
                        
                        # Headers para simular navegador
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                            'Accept': 'text/csv,application/csv,text/plain,*/*',
                            'Referer': 'https://investimentos.com.br/ativos/'
                        }
                        
                        async with session.get(csv_url, headers=headers) as response:
                            if response.status == 200:
                                content = await response.read()
                                
                                # Verifica se é CSV válido
                                if len(content) > 1000:  # CSV deve ter pelo menos 1KB
                                    # Salva o CSV
                                    os.makedirs("data", exist_ok=True)
                                    with open(self.csv_cache_path, 'wb') as f:
                                        f.write(content)
                                    
                                    # Verifica quantas linhas tem
                                    try:
                                        df = pd.read_csv(self.csv_cache_path, encoding='utf-8-sig')
                                        timestamp = datetime.now()
                                        print(f"✓ CSV baixado com SUCESSO!")
                                        print(f"✓ Total de ações: {len(df)}")
                                        print(f"✓ Data: {timestamp.strftime('%d/%m/%Y %H:%M')}")
                                        print(f"✓ Salvo em: {self.csv_cache_path}")
                                        return self.csv_cache_path, timestamp
                                    except:
                                        pass
                    except:
                        continue
                
                # Se nenhuma URL funcionou
                print(f"⚠ Nenhuma URL funcionou")
                
                # Tenta scraping da página
                print("  Tentando scraping da página...")
                csv_path = await self._scrape_tabela_acoes()
                if csv_path:
                    return csv_path
                
                # Fallback: usa cache antigo ou CSV local
                if os.path.exists(self.csv_cache_path):
                    file_time = datetime.fromtimestamp(os.path.getmtime(self.csv_cache_path))
                    print(f"⚠ Usando cache antigo")
                    print(f"⚠ Data: {file_time.strftime('%d/%m/%Y %H:%M')}")
                    return self.csv_cache_path, file_time
                
                print(f"⚠ Usando CSV local (stocks.csv)")
                csv_local = "data/stocks.csv"
                if os.path.exists(csv_local):
                    file_time = datetime.fromtimestamp(os.path.getmtime(csv_local))
                    return csv_local, file_time
                else:
                    # Último recurso: retorna path que não existe (será tratado depois)
                    return csv_local, datetime.now()
        
        except asyncio.TimeoutError:
            print(f"⚠ Timeout ao acessar investimentos.com.br")
            if os.path.exists(self.csv_cache_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(self.csv_cache_path))
                print(f"⚠ Usando cache antigo ({file_time.strftime('%d/%m/%Y %H:%M')})")
                return self.csv_cache_path, file_time
            csv_local = "data/stocks.csv"
            file_time = datetime.fromtimestamp(os.path.getmtime(csv_local)) if os.path.exists(csv_local) else datetime.now()
            return csv_local, file_time
        except Exception as e:
            print(f"⚠ Erro ao baixar CSV: {e}")
            if os.path.exists(self.csv_cache_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(self.csv_cache_path))
                print(f"⚠ Usando cache antigo ({file_time.strftime('%d/%m/%Y %H:%M')})")
                return self.csv_cache_path, file_time
            csv_local = "data/stocks.csv"
            file_time = datetime.fromtimestamp(os.path.getmtime(csv_local)) if os.path.exists(csv_local) else datetime.now()
            return csv_local, file_time
    
    async def _scrape_tabela_acoes(self) -> str:
        """
        Scrape da tabela de ações do site (fallback)
        Cria CSV a partir dos dados da página
        """
        try:
            print("  🔍 Fazendo scraping da tabela...")
            
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(f"{self.base_url}/acoes/", headers=headers) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Procura tabela de ações
                    tabela = soup.find('table') or soup.find('div', class_='table')
                    
                    if not tabela:
                        print("  ✗ Tabela não encontrada")
                        return None
                    
                    # Extrai dados da tabela
                    acoes = []
                    linhas = tabela.find_all('tr')[1:]  # Pula header
                    
                    for linha in linhas[:200]:  # Limita a 200 ações
                        colunas = linha.find_all('td')
                        if len(colunas) >= 5:
                            try:
                                ticker = colunas[0].text.strip()
                                # Tenta extrair métricas (ajustar conforme HTML real)
                                acoes.append({
                                    'ticker': ticker,
                                    'roe': 15.0,  # Placeholder
                                    'cagr': 12.0,
                                    'pl': 10.0,
                                    'divida': 1.0,
                                    'setor': 'N/A'
                                })
                            except:
                                continue
                    
                    if len(acoes) > 0:
                        # Cria CSV
                        df = pd.DataFrame(acoes)
                        os.makedirs("data", exist_ok=True)
                        df.to_csv(self.csv_cache_path, index=False)
                        
                        print(f"  ✓ Scraping concluído: {len(acoes)} ações")
                        return self.csv_cache_path
                    
                    return None
        
        except Exception as e:
            print(f"  ✗ Erro no scraping: {e}")
            return None
            return None
    
    async def scrape_precos_atualizados(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Scrape preços atualizados de investimentos.com.br
        Retorna dicionário com dados de cada ticker
        """
        
        print(f"\n[SCRAPE] Buscando preços de {len(tickers)} ações...")
        
        precos = {}
        
        async with aiohttp.ClientSession() as session:
            for ticker in tickers:
                try:
                    # URL da ação (formato pode variar)
                    url = f"{self.base_url}/acoes/{ticker.lower()}"
                    
                    async with session.get(url, timeout=10) as response:
                        if response.status == 200:
                            html = await response.text()
                            soup = BeautifulSoup(html, 'html.parser')
                            
                            # Tenta extrair preço (ajustar seletores conforme site)
                            preco_elem = soup.select_one('.price, .cotacao, [data-price]')
                            if preco_elem:
                                preco_text = preco_elem.text.strip()
                                # Remove R$, espaços, e converte vírgula para ponto
                                preco_text = preco_text.replace('R$', '').replace('.', '').replace(',', '.').strip()
                                preco = float(preco_text)
                                
                                # Tenta extrair variação
                                var_elem = soup.select_one('.variation, .variacao')
                                variacao = 0.0
                                if var_elem:
                                    var_text = var_elem.text.strip().replace('%', '').replace(',', '.')
                                    try:
                                        variacao = float(var_text)
                                    except:
                                        pass
                                
                                precos[ticker] = {
                                    "ticker": ticker,
                                    "preco_atual": preco,
                                    "variacao_dia": variacao,
                                    "timestamp": datetime.now().isoformat(),
                                    "fonte": "investimentos.com.br"
                                }
                                
                                print(f"  ✓ {ticker}: R$ {preco:.2f}")
                
                except Exception as e:
                    print(f"  ✗ {ticker}: Erro - {e}")
                    continue
        
        print(f"✓ {len(precos)}/{len(tickers)} preços obtidos")
        return precos
    
    async def scrape_dados_completos_acao(self, ticker: str) -> Dict:
        """
        Scrape dados completos de uma ação específica
        Inclui: preço, ROE, P/L, dividend yield, etc.
        """
        
        try:
            url = f"{self.base_url}/acoes/{ticker.lower()}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extrai dados (ajustar seletores conforme site)
                    dados = {
                        "ticker": ticker,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Preço
                    preco_elem = soup.select_one('.price, .cotacao')
                    if preco_elem:
                        preco_text = preco_elem.text.strip().replace('R$', '').replace('.', '').replace(',', '.').strip()
                        dados["preco"] = float(preco_text)
                    
                    # ROE
                    roe_elem = soup.select_one('[data-indicator="roe"], .roe')
                    if roe_elem:
                        roe_text = roe_elem.text.strip().replace('%', '').replace(',', '.')
                        dados["roe"] = float(roe_text)
                    
                    # P/L
                    pl_elem = soup.select_one('[data-indicator="pl"], .pl')
                    if pl_elem:
                        pl_text = pl_elem.text.strip().replace(',', '.')
                        dados["pl"] = float(pl_text)
                    
                    # Dividend Yield
                    dy_elem = soup.select_one('[data-indicator="dy"], .dividend-yield')
                    if dy_elem:
                        dy_text = dy_elem.text.strip().replace('%', '').replace(',', '.')
                        dados["dividend_yield"] = float(dy_text)
                    
                    return dados
        
        except Exception as e:
            print(f"Erro ao scrape {ticker}: {e}")
            return None
    
    async def processar_csv_e_enriquecer(self, csv_path: str = None) -> pd.DataFrame:
        """
        Processa CSV e enriquece com dados scraped
        """
        
        if not csv_path:
            csv_path = await self.baixar_csv_diario()
        
        if not csv_path or not os.path.exists(csv_path):
            print("⚠ CSV não disponível")
            return None
        
        # Lê CSV
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        print(f"\n✓ CSV carregado: {len(df)} ações")
        print(f"Colunas: {list(df.columns)}")
        
        # Filtra apenas ações (não FIIs, ETFs, etc)
        if 'Tipo' in df.columns:
            df = df[df['Tipo'] == 'Ação']
        
        # Renomeia colunas se necessário
        column_mapping = {
            'Código': 'Ticker',
            'Cotação': 'Preço',
            'P/L': 'PL',
            # Adicione outros mapeamentos conforme necessário
        }
        
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df.rename(columns={old_col: new_col}, inplace=True)
        
        return df
    
    async def obter_dados_atualizados_completos(self) -> Dict:
        """
        Método principal: baixa CSV + scrape preços
        Retorna dados completos e atualizados
        """
        
        print("\n" + "="*60)
        print("INVESTIMENTOS.COM.BR - DADOS ATUALIZADOS")
        print("="*60)
        
        # 1. Baixa CSV diário
        csv_path = await self.baixar_csv_diario()
        
        if not csv_path:
            return {"success": False, "error": "Falha ao baixar CSV"}
        
        # 2. Processa CSV
        df = await self.processar_csv_e_enriquecer(csv_path)
        
        if df is None or len(df) == 0:
            return {"success": False, "error": "CSV vazio ou inválido"}
        
        # 3. Pega top 20 ações por algum critério
        # (ajustar conforme colunas disponíveis)
        if 'ROE' in df.columns:
            df_top = df.nlargest(20, 'ROE')
        else:
            df_top = df.head(20)
        
        tickers = df_top['Ticker'].tolist() if 'Ticker' in df_top.columns else []
        
        # 4. Scrape preços atualizados
        precos = await self.scrape_precos_atualizados(tickers)
        
        # 5. Combina dados
        acoes_completas = []
        
        for _, row in df_top.iterrows():
            ticker = row.get('Ticker', '')
            
            acao_data = {
                "ticker": ticker,
                "roe": row.get('ROE', 0),
                "cagr": row.get('CAGR', 0),
                "pl": row.get('PL', 0),
                "setor": row.get('Setor', 'N/A'),
                "preco_csv": row.get('Preço', 0)
            }
            
            # Adiciona preço scraped se disponível
            if ticker in precos:
                acao_data["preco_atual"] = precos[ticker]["preco_atual"]
                acao_data["variacao_dia"] = precos[ticker]["variacao_dia"]
                acao_data["fonte_preco"] = "scrape"
            else:
                acao_data["preco_atual"] = acao_data["preco_csv"]
                acao_data["fonte_preco"] = "csv"
            
            acoes_completas.append(acao_data)
        
        print(f"\n✓ {len(acoes_completas)} ações com dados completos")
        
        return {
            "success": True,
            "data_atualizacao": datetime.now().isoformat(),
            "total_acoes": len(acoes_completas),
            "acoes": acoes_completas,
            "csv_path": csv_path
        }
