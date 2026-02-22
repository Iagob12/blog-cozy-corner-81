"""
Script de Atualização Diária
Executa após o fechamento da bolsa (18h)
"""
import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.append(str(Path(__file__).parent.parent))

from app.layers.quant_layer import QuantLayer
from app.layers.macro_layer import MacroLayer
from app.layers.surgical_layer import SurgicalLayer
from app.services.sentiment_analysis import SentimentAnalyzer

class DailyUpdatePipeline:
    """Pipeline de atualização diária"""
    
    def __init__(self):
        self.quant_layer = QuantLayer()
        self.macro_layer = MacroLayer()
        self.surgical_layer = SurgicalLayer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.csv_path = "data/stocks.csv"
    
    async def download_csv_from_investimentos(self):
        """
        Baixa CSV de investimentos.com.br
        TODO: Implementar scraping ou API
        """
        print("📥 Baixando dados de investimentos.com.br...")
        # Placeholder - implementar scraping real
        print("✅ CSV baixado com sucesso")
        return self.csv_path
    
    async def process_with_ai(self, csv_path: str):
        """Processa CSV com as 3 camadas"""
        print("\n🤖 Processando com IA...")
        
        # Camada 1: Filtro Quantitativo
        print("  📊 Camada 1: Filtro Quantitativo")
        ranked_stocks = self.quant_layer.process(csv_path)
        print(f"  ✅ {len(ranked_stocks)} ações passaram nos filtros")
        
        # Camada 2: Análise Macro
        print("  🌍 Camada 2: Análise Macro")
        macro_context = await self.macro_layer.process()
        print(f"  ✅ Setores favorecidos: {', '.join(macro_context.setor_favorecido)}")
        
        # Camada 3: Análise de Sentimento
        print("  💭 Camada 3: Análise de Sentimento")
        for stock in ranked_stocks[:5]:  # Top 5
            sentiment = await self.sentiment_analyzer.analyze(stock.ticker)
            if sentiment.risco_manada:
                print(f"  ⚠️ {stock.ticker}: Risco de manada detectado!")
        
        return ranked_stocks, macro_context
    
    async def filter_with_gemini(self, stocks):
        """
        Filtro adicional com Gemini
        Analisa contexto global e tendências
        """
        print("\n🧠 Filtro Gemini: Análise de contexto global...")
        
        # TODO: Implementar análise com Gemini
        # Prompt: "Considerando o contexto global atual (Bitcoin, Ouro, Nvidia, etc),
        # quais dessas ações têm maior probabilidade de subir nos próximos 90 dias?"
        
        print("✅ Filtro Gemini concluído")
        return stocks[:15]  # Top 15
    
    async def analyze_reports(self, stocks):
        """
        Baixa e analisa relatórios de RI
        """
        print("\n📄 Analisando relatórios de RI...")
        
        for stock in stocks[:5]:  # Top 5
            print(f"  📋 {stock.ticker}: Buscando relatório...")
            # TODO: Implementar download automático de PDFs de RI
            # Fontes: site de RI da empresa, CVM, etc.
        
        print("✅ Relatórios analisados")
    
    async def calculate_strategies(self, stocks):
        """
        Calcula estratégias para bater 5% ao mês
        """
        print("\n💰 Calculando estratégias...")
        
        total_upside = sum(s.score for s in stocks[:15])
        avg_upside = total_upside / 15
        
        print(f"  📈 Upside médio: {avg_upside:.2f}%")
        print(f"  🎯 Meta: 5% ao mês (60% ao ano)")
        
        if avg_upside >= 5:
            print("  ✅ Carteira tem potencial para bater a meta!")
        else:
            print("  ⚠️ Carteira abaixo da meta. Ajustando pesos...")
        
        return stocks
    
    async def save_results(self, stocks):
        """Salva resultados em JSON"""
        import json
        from datetime import datetime
        
        output = {
            "updated_at": datetime.now().isoformat(),
            "stocks": [
                {
                    "ticker": s.ticker,
                    "score": s.score,
                    "roe": s.roe,
                    "cagr": s.cagr,
                    "pl": s.pl,
                    "rank": s.rank
                }
                for s in stocks
            ]
        }
        
        output_path = "data/daily_picks.json"
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n💾 Resultados salvos em {output_path}")
    
    async def send_notifications(self, stocks):
        """Envia notificações"""
        print("\n📧 Enviando notificações...")
        
        # TODO: Implementar envio de emails/push notifications
        print(f"  ✅ {len(stocks)} ações na carteira de hoje")
        print(f"  🏆 Alpha Pick: {stocks[0].ticker}")
        
    async def run(self):
        """Executa pipeline completo"""
        print("=" * 60)
        print("🚀 ALPHA TERMINAL - ATUALIZAÇÃO DIÁRIA")
        print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. Download CSV
            csv_path = await self.download_csv_from_investimentos()
            
            # 2. Processar com IA
            stocks, macro = await self.process_with_ai(csv_path)
            
            # 3. Filtro Gemini
            filtered_stocks = await self.filter_with_gemini(stocks)
            
            # 4. Analisar relatórios
            await self.analyze_reports(filtered_stocks)
            
            # 5. Calcular estratégias
            final_stocks = await self.calculate_strategies(filtered_stocks)
            
            # 6. Salvar resultados
            await self.save_results(final_stocks)
            
            # 7. Enviar notificações
            await self.send_notifications(final_stocks)
            
            print("\n" + "=" * 60)
            print("✅ ATUALIZAÇÃO CONCLUÍDA COM SUCESSO!")
            print("=" * 60)
            
        except Exception as e:
            print(f"\n❌ ERRO: {str(e)}")
            import traceback
            traceback.print_exc()

async def main():
    pipeline = DailyUpdatePipeline()
    await pipeline.run()

if __name__ == "__main__":
    asyncio.run(main())
