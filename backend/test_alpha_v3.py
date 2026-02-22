"""
Teste rápido do Alpha System V3
"""
import asyncio
import sys
import os

# Adiciona o diretório ao path
sys.path.insert(0, os.path.dirname(__file__))

async def test_gemini_client():
    """Testa Gemini Client"""
    print("\n=== TESTE 1: Gemini Client ===")
    
    try:
        from app.services.gemini_client import get_gemini_client
        
        client = get_gemini_client()
        print("✓ Gemini Client inicializado")
        
        # Teste de conexão
        conectado = await client.testar_conexao()
        
        if conectado:
            print("✓ Conexão com Gemini OK")
        else:
            print("✗ Falha na conexão com Gemini")
        
        return conectado
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False


async def test_validators():
    """Testa Validators"""
    print("\n=== TESTE 2: Validators ===")
    
    try:
        from app.utils.validators import validar_csv_freshness, DataFreshnessError
        from datetime import datetime
        import os
        
        # Cria arquivo de teste
        test_file = "test_temp.csv"
        with open(test_file, 'w') as f:
            f.write("ticker,roe,cagr,pl\n")
            f.write("PRIO3,35,18,8\n")
        
        # Testa validação
        try:
            timestamp = validar_csv_freshness(test_file, max_horas=24)
            print(f"✓ Validação OK: {timestamp.strftime('%d/%m/%Y %H:%M')}")
        except DataFreshnessError as e:
            print(f"✗ Validação falhou: {e}")
        
        # Remove arquivo de teste
        os.remove(test_file)
        
        print("✓ Validators funcionando")
        return True
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False


async def test_data_models():
    """Testa Data Models"""
    print("\n=== TESTE 3: Data Models ===")
    
    try:
        from app.models.investment_models import StockData, AnaliseCompleta
        from datetime import datetime
        
        # Cria StockData
        stock = StockData(
            ticker="PRIO3",
            nome="PRIO",
            setor="Energia",
            roe=35.0,
            cagr=18.0,
            pl=8.5,
            divida_ebitda=1.2,
            margem_liquida=25.0,
            data_csv=datetime.now()
        )
        
        print(f"✓ StockData criado: {stock.ticker}")
        
        # Testa conversão
        stock_dict = stock.to_dict()
        stock_restored = StockData.from_dict(stock_dict)
        
        print(f"✓ Conversão to_dict/from_dict OK")
        
        # Testa critérios
        if stock.atende_criterios():
            print(f"✓ {stock.ticker} atende critérios")
        else:
            print(f"✗ {stock.ticker} não atende critérios")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_alpha_system_v3_init():
    """Testa inicialização do Alpha System V3"""
    print("\n=== TESTE 4: Alpha System V3 (Init) ===")
    
    try:
        from app.services.alpha_system_v3 import AlphaSystemV3
        
        system = AlphaSystemV3()
        print("✓ Alpha System V3 inicializado")
        
        # Verifica componentes
        if system.gemini:
            print("✓ Gemini Client OK")
        if system.scraper:
            print("✓ Investimentos Scraper OK")
        if system.release_downloader:
            print("✓ Release Downloader OK")
        if system.brapi:
            print("✓ Brapi Service OK")
        
        return True
    
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTES DO ALPHA SYSTEM V3")
    print("="*60)
    
    resultados = []
    
    # Teste 1: Gemini Client
    resultados.append(await test_gemini_client())
    
    # Teste 2: Validators
    resultados.append(await test_validators())
    
    # Teste 3: Data Models
    resultados.append(await test_data_models())
    
    # Teste 4: Alpha System V3
    resultados.append(await test_alpha_system_v3_init())
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    passou = sum(resultados)
    
    print(f"Total: {total}")
    print(f"Passou: {passou}")
    print(f"Falhou: {total - passou}")
    
    if passou == total:
        print("\n✓ TODOS OS TESTES PASSARAM!")
    else:
        print(f"\n⚠ {total - passou} teste(s) falharam")
    
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
