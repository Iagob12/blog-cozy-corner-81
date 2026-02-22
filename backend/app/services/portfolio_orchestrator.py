"""
Portfolio Orchestrator
Orquestra todo o fluxo de análise e montagem de carteira
"""
import asyncio
from typing import List, Dict
import pandas as pd
from datetime import datetime
import os

from app.services.data_collector import DataCollector
from app.services.alpha_intelligence import AlphaIntelligence
from app.services.market_data import MarketDataService
from app.layers.surgical_layer import SurgicalLayer

class PortfolioOrchestrator:
    """
    Orquestra o fluxo completo:
    1. Prompt 1: Identifica setores em ascensão
    2. Coleta dados de ações (CSV)
    3. Prompt 2: Filtra 15 melhores
    4. Busca relatórios de resultados
    5. Prompt 3: Análise profunda e carteira final
    """
    
    def __init__(self):
        self.collector = DataCollector()
        self.ai = AlphaIntelligence()
        self.market = MarketDataService()
        self.surgical = SurgicalLayer()
    
    async def executar_fluxo_completo(self) -> Dict:
        """
        Executa o fluxo completo de análise
        """
        resultado = {
            "timestamp": datetime.now().isoformat(),
            "etapas": {}
        }
        
        print("🚀 Iniciando Alpha Terminal - Fluxo Completo\n")
        
        # ETAPA 1: Radar de Oportunidades (Prompt 1)
        print("📡 ETAPA 1: Radar de Oportunidades...")
        radar = await self.ai.prompt_1_radar_oportunidades()
        resultado["etapas"]["radar"] = radar
        
        setores_quentes = [s["setor"] for s in radar.get("setores_aceleracao", [])]
        print(f"   ✓ Setores identificados: {', '.join(setores_quentes[:3])}")
        
        # ETAPA 2: Coleta de Dados
        print("\n📊 ETAPA 2: Coletando dados de ações...")
        
        # Tenta baixar CSV do investimentos.com.br
        csv_path = await self.collector.download_investimentos_csv()
        
        if csv_path and os.path.exists(csv_path):
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
            print(f"   ✓ CSV baixado: {len(df)} ações")
        else:
            # Fallback: scraping
            print("   ⚠ CSV não disponível, fazendo scraping...")
            df = await self.collector.scrape_investimentos_data()
            
            if df.empty:
                # Fallback final: Fundamentus
                print("   ⚠ Tentando Fundamentus...")
                df = await self.collector.enriquecer_dados_com_fundamentus(pd.DataFrame())
        
        if df.empty:
            return {"erro": "Não foi possível coletar dados de ações"}
        
        resultado["etapas"]["dados_coletados"] = len(df)
        
        # ETAPA 3: Filtro Fundamentalista (Prompt 2)
        print(f"\n🔍 ETAPA 3: Aplicando filtros fundamentalistas...")
        
        # Prepara dados para o Prompt 2
        stocks_data = []
        for _, row in df.iterrows():
            try:
                stocks_data.append({
                    "ticker": row.get('Ticker', ''),
                    "pl": float(row.get('P/L', 0)),
                    "roe": float(row.get('ROE', 0)),
                    "cagr": float(row.get('CAGR', 0)) if 'CAGR' in row else 15.0,
                    "setor": row.get('Setor', 'Desconhecido'),
                    "preco": float(row.get('Preço', 0))
                })
            except:
                continue
        
        # Aplica Prompt 2
        top_15 = await self.ai.prompt_2_triagem_fundamentalista(stocks_data)
        top_15 = top_15[:15]  # Garante apenas 15
        
        print(f"   ✓ Top 15 selecionadas")
        for i, stock in enumerate(top_15[:5], 1):
            print(f"      {i}. {stock['ticker']} - Score: {stock.get('score_valorizacao', 0)}")
        
        resultado["etapas"]["top_15"] = top_15
        
        # ETAPA 4: Busca de Relatórios
        print(f"\n📄 ETAPA 4: Buscando relatórios de resultados...")
        
        tickers_top15 = [s['ticker'] for s in top_15]
        relatorios_info = await self.collector.coletar_relatorios_batch(tickers_top15)
        
        print(f"   ✓ {len(relatorios_info)} relatórios encontrados")
        
        # Download dos PDFs
        relatorios_completos = []
        for info in relatorios_info:
            print(f"   📥 Baixando {info['ticker']}...")
            pdf_path = await self.collector.download_pdf(
                info['url'], 
                info['ticker']
            )
            
            if pdf_path:
                # Extrai texto do PDF
                try:
                    analise = await self.surgical.process(pdf_path, info['ticker'])
                    relatorios_completos.append({
                        "ticker": info['ticker'],
                        "conteudo": analise.tese_qualitativa,
                        "catalisadores": [c.descricao for c in analise.catalisadores],
                        "score": analise.score_qualitativo,
                        "pdf_path": pdf_path
                    })
                except Exception as e:
                    print(f"      ⚠ Erro ao processar PDF: {e}")
        
        print(f"   ✓ {len(relatorios_completos)} PDFs processados")
        resultado["etapas"]["relatorios_processados"] = len(relatorios_completos)
        
        # ETAPA 5: Análise Comparativa (Prompt 3)
        print(f"\n🎯 ETAPA 5: Análise comparativa profunda...")
        
        if relatorios_completos:
            analise_final = await self.ai.prompt_3_analise_comparativa(relatorios_completos)
            resultado["etapas"]["analise_comparativa"] = analise_final
            
            # Extrai carteira final
            carteira_final = analise_final.get("ranking_final", [])[:5]
            
            print(f"\n✨ CARTEIRA FINAL:")
            for pos in carteira_final:
                print(f"   {pos['posicao']}. {pos['ticker']} - {pos['acao']}")
                print(f"      {pos['justificativa'][:100]}...")
            
            resultado["carteira_final"] = carteira_final
        
        # ETAPA 6: Enriquece com dados de mercado
        print(f"\n💰 ETAPA 6: Buscando preços em tempo real...")
        
        if "carteira_final" in resultado:
            tickers_carteira = [p['ticker'] for p in resultado["carteira_final"]]
            quotes = await self.market.get_multiple_quotes(tickers_carteira)
            
            # Adiciona preços à carteira
            for posicao in resultado["carteira_final"]:
                ticker = posicao['ticker']
                if ticker in quotes:
                    posicao['preco_atual'] = quotes[ticker]['preco_atual']
                    posicao['variacao_dia'] = quotes[ticker]['variacao_dia']
            
            print(f"   ✓ Preços atualizados")
        
        # ETAPA 7: Verificação Anti-Manada
        print(f"\n🛡️ ETAPA 7: Verificação anti-manada...")
        
        if "carteira_final" in resultado:
            for posicao in resultado["carteira_final"]:
                ticker = posicao['ticker']
                verificacao = await self.ai.prompt_6_verificacao_anti_manada(ticker)
                posicao['anti_manada'] = verificacao
                
                veredito = verificacao.get('veredito', 'DESCONHECIDO')
                print(f"   {ticker}: {veredito}")
        
        print(f"\n✅ FLUXO COMPLETO CONCLUÍDO!\n")
        
        return resultado
    
    async def atualizar_precos_carteira(self, tickers: List[str]) -> Dict[str, Dict]:
        """
        Atualiza preços em tempo real de uma carteira
        """
        return await self.market.get_multiple_quotes(tickers)
    
    async def analise_rapida_ticker(self, ticker: str) -> Dict:
        """
        Análise rápida de um ticker específico
        """
        resultado = {}
        
        # Preço atual
        quote = await self.market.get_quote(ticker)
        resultado['quote'] = quote
        
        # Momentum
        momentum = await self.market.calculate_momentum(ticker)
        resultado['momentum'] = momentum
        
        # Swing trade
        if quote.get('preco_atual', 0) > 0:
            swing = await self.ai.prompt_4_swing_trade(ticker, quote['preco_atual'])
            resultado['swing_trade'] = swing
        
        # Anti-manada
        anti_manada = await self.ai.prompt_6_verificacao_anti_manada(ticker)
        resultado['anti_manada'] = anti_manada
        
        return resultado
    
    def gerar_relatorio_html(self, resultado: Dict, output_path: str = "data/relatorio.html"):
        """
        Gera relatório HTML do resultado
        """
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Alpha Terminal - Relatório</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2563eb; }}
                h2 {{ color: #1e40af; margin-top: 30px; }}
                .carteira {{ background: #f0f9ff; padding: 20px; border-radius: 8px; }}
                .acao {{ margin: 15px 0; padding: 15px; background: white; border-left: 4px solid #2563eb; }}
                .score {{ color: #16a34a; font-weight: bold; }}
                .alerta {{ color: #dc2626; }}
            </style>
        </head>
        <body>
            <h1>🎯 Alpha Terminal - Relatório de Análise</h1>
            <p><strong>Data:</strong> {resultado.get('timestamp', '')}</p>
            
            <h2>📊 Carteira Recomendada</h2>
            <div class="carteira">
        """
        
        for pos in resultado.get('carteira_final', []):
            html += f"""
                <div class="acao">
                    <h3>{pos['posicao']}. {pos['ticker']}</h3>
                    <p><strong>Ação:</strong> {pos['acao']}</p>
                    <p>{pos['justificativa']}</p>
                    <p><strong>Preço:</strong> R$ {pos.get('preco_atual', 0):.2f}</p>
                    <p><strong>Veredito Anti-Manada:</strong> {pos.get('anti_manada', {}).get('veredito', 'N/A')}</p>
                </div>
            """
        
        html += """
            </div>
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return output_path
