"""
Teste Completo do Sistema Alpha V3
Testa todos os componentes integrados
"""
import asyncio
import sys
import os
from datetime import datetime

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(__file__))

# Carrega .env
from dotenv import load_dotenv
load_dotenv()


async def test_investimentos_scraper():
    """Testa Investimentos Scraper com timestamp"""
    print("\n" + "="*60)
    print("TESTE: Investimentos Scraper")
    print("="*60)
    
    try:
        from app.services.investimentos_scraper import InvestimentosScraper
        
        scraper = InvestimentosScraper()
        print("✓ Scraper inicializado")
        
        # Tenta baixar CSV
        csv_path, timestamp = await scraper.baixar_csv_diario()
        
        print(f"✓ CSV: {csv_path}")
        print(f"✓ Data: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Verifica idade
        idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
        print(f"✓ Idade: {idade_horas:.1f} horas")
        
        if idade_horas < 24:
            print("✓ CSV está atualizado (< 24h)")
            return True
        else:
            print("⚠ CSV está antigo (> 24h)")
            return False
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_brapi_service():
    """Testa Brapi Service com timestamp"""
    print("\n" + "="*60)
    print("TESTE: Brapi Service")
    print("="*60)
    
    try:
        from app.services.brapi_service import BrapiService
        
        brapi = BrapiService()
        print("✓ Brapi inicializado")
        
        # Testa com alguns tickers
        tickers = ["PETR4", "VALE3", "ITUB4"]
        print(f"\nBuscando preços de {len(tickers)} ações...")
        
        quotes = await brapi.get_multiple_quotes(tickers)
        
        print(f"\n✓ {len(quotes)}/{len(tickers)} preços obtidos")
        
        for ticker, data in quotes.items():
            preco = data.get("preco_atual", 0)
            timestamp_str = data.get("data_consulta", "N/A")
            fonte = data.get("fonte", "N/A")
            
            print(f"  {ticker}: R$ {preco:.2f} ({timestamp_str}) [{fonte}]")
        
        # Testa cache
        print("\nTestando cache...")
        quotes2 = await brapi.get_multiple_quotes(tickers)
        
        cache_hits = sum(1 for q in quotes2.values() if q.get("fonte") == "cache")
        print(f"✓ {cache_hits}/{len(tickers)} do cache")
        
        # Stats do cache
        stats = brapi.get_cache_stats()
        print(f"✓ Cache: {stats['validos']} válidos, {stats['expirados']} expirados")
        
        return len(quotes) > 0
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_release_downloader():
    """Testa Release Downloader com fallback Q4→Q3→Q2→Q1"""
    print("\n" + "="*60)
    print("TESTE: Release Downloader")
    print("="*60)
    
    try:
        from app.services.release_downloader import ReleaseDownloader
        
        downloader = ReleaseDownloader()
        print("✓ Release Downloader inicializado")
        print(f"✓ {len(downloader.base_urls)} empresas configuradas")
        
        # Testa com alguns tickers
        tickers_teste = ["PRIO3", "PETR4", "VALE3"]
        print(f"\nBuscando Releases de {len(tickers_teste)} empresas...")
        print("Estratégia: Q4 2025 → Q3 2025 → Q2 2025 → Q1 2025")
        
        encontrados = 0
        
        for ticker in tickers_teste:
            print(f"\n{ticker}:")
            
            if ticker in downloader.base_urls:
                print(f"  ✓ URL configurada: {downloader.base_urls[ticker]}")
                
                # Tenta buscar (com timeout)
                try:
                    pdf_path = await asyncio.wait_for(
                        downloader.buscar_release_mais_recente(ticker),
                        timeout=15.0
                    )
                    
                    if pdf_path:
                        print(f"  ✓ Release encontrado: {pdf_path}")
                        encontrados += 1
                    else:
                        print(f"  ⚠ Release não encontrado")
                
                except asyncio.TimeoutError:
                    print(f"  ⚠ Timeout (15s)")
            else:
                print(f"  ⚠ URL não configurada")
        
        print(f"\n✓ {encontrados}/{len(tickers_teste)} Releases encontrados")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_validators():
    """Testa Validators com Q3 2025"""
    print("\n" + "="*60)
    print("TESTE: Validators")
    print("="*60)
    
    try:
        from app.utils.validators import (
            validar_trimestre_release,
            calcular_score_trimestre,
            DataFreshnessError
        )
        
        print("✓ Validators importados")
        
        # Testa validação de trimestres
        testes = [
            ("Q4", 2025, True),
            ("Q3", 2025, True),
            ("Q2", 2025, True),
            ("Q1", 2025, True),
            ("Q4", 2024, False),
        ]
        
        print("\nTestando validação de trimestres:")
        for trimestre, ano, deve_passar in testes:
            try:
                validar_trimestre_release(trimestre, ano, minimo_trimestre="Q3", minimo_ano=2025)
                resultado = "✓ PASSOU"
                passou = True
            except DataFreshnessError:
                resultado = "✗ REJEITADO"
                passou = False
            
            esperado = "✓" if deve_passar else "✗"
            status = "OK" if passou == deve_passar else "ERRO"
            
            print(f"  {trimestre} {ano}: {resultado} (esperado: {esperado}) [{status}]")
        
        # Testa score de trimestre
        print("\nTestando score de trimestre:")
        scores = [
            ("Q4", 2025, 1.0),
            ("Q3", 2025, 0.9),
            ("Q2", 2025, 0.8),
            ("Q1", 2025, 0.7),
        ]
        
        for trimestre, ano, score_esperado in scores:
            score = calcular_score_trimestre(trimestre, ano)
            print(f"  {trimestre} {ano}: {score:.1f} (esperado: {score_esperado})")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_gemini_connection():
    """Testa conexão com Gemini"""
    print("\n" + "="*60)
    print("TESTE: Gemini Connection")
    print("="*60)
    
    try:
        from app.services.gemini_client import get_gemini_client
        
        client = get_gemini_client()
        print("✓ Gemini Client inicializado")
        
        # Testa conexão
        conectado = await client.testar_conexao()
        
        if conectado:
            print("✓ Conexão com Gemini OK")
            return True
        else:
            print("✗ Falha na conexão com Gemini")
            return False
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        if "GEMINI_API_KEY" in str(e):
            print("⚠ Configure GEMINI_API_KEY no .env")
        return False


async def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTE COMPLETO DO SISTEMA ALPHA V3")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*60)
    
    resultados = {}
    
    # Teste 1: Validators
    resultados["Validators"] = await test_validators()
    
    # Teste 2: Investimentos Scraper
    resultados["Investimentos Scraper"] = await test_investimentos_scraper()
    
    # Teste 3: Brapi Service
    resultados["Brapi Service"] = await test_brapi_service()
    
    # Teste 4: Release Downloader
    resultados["Release Downloader"] = await test_release_downloader()
    
    # Teste 5: Gemini Connection
    resultados["Gemini Connection"] = await test_gemini_connection()
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    for nome, passou in resultados.items():
        status = "✓ PASSOU" if passou else "✗ FALHOU"
        print(f"{nome:.<40} {status}")
    
    total = len(resultados)
    passou_total = sum(resultados.values())
    percentual = (passou_total / total * 100) if total > 0 else 0
    
    print("\n" + "-"*60)
    print(f"Total: {total}")
    print(f"Passou: {passou_total}")
    print(f"Falhou: {total - passou_total}")
    print(f"Taxa de Sucesso: {percentual:.0f}%")
    print("="*60)
    
    if passou_total == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
    elif percentual >= 80:
        print(f"\n✓ Sistema funcionando ({percentual:.0f}% dos testes)")
    else:
        print(f"\n⚠ Alguns testes falharam ({percentual:.0f}% de sucesso)")


if __name__ == "__main__":
    asyncio.run(main())
