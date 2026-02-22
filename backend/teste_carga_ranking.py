"""
Teste de Carga do Ranking - Simula o que o backend faz ao iniciar
"""
import json
import os
from datetime import datetime
from app.models import TopPick

def teste_carregar_ranking():
    """Testa se o ranking pode ser carregado corretamente"""
    print("\n" + "="*80)
    print("TESTE DE CARGA DO RANKING")
    print("="*80 + "\n")
    
    RANKING_FILE = "data/ranking_cache.json"
    
    try:
        # 1. Verifica se arquivo existe
        if not os.path.exists(RANKING_FILE):
            print(f"✗ ERRO: Arquivo não encontrado: {RANKING_FILE}")
            return False
        
        print(f"✓ Arquivo encontrado: {RANKING_FILE}")
        
        # 2. Carrega JSON
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        print(f"✓ JSON carregado com sucesso")
        print(f"  - Total aprovadas: {dados.get('total_aprovadas', 0)}")
        print(f"  - Empresas no ranking: {len(dados.get('ranking', []))}")
        print(f"  - Timestamp: {dados.get('timestamp', 'N/A')}")
        
        # 3. Tenta criar objetos TopPick
        ranking_objects = []
        erros = []
        
        for i, stock_data in enumerate(dados.get("ranking", []), 1):
            try:
                top_pick = TopPick(**stock_data)
                ranking_objects.append(top_pick)
                print(f"✓ [{i}] {stock_data['ticker']} - TopPick criado")
            except Exception as e:
                erros.append(f"✗ [{i}] {stock_data.get('ticker', 'N/A')}: {str(e)}")
        
        if erros:
            print(f"\n⚠ ERROS ENCONTRADOS:")
            for erro in erros:
                print(f"  {erro}")
            return False
        
        print(f"\n✓ Todos os {len(ranking_objects)} objetos TopPick criados com sucesso")
        
        # 4. Testa get_top_n
        class RankingSimples:
            def __init__(self, ranking, total):
                self.ranking = ranking
                self.total_aprovadas = total
            
            def get_top_n(self, n: int):
                return self.ranking[:n]
        
        ranking_final = RankingSimples(
            ranking=ranking_objects,
            total=dados.get("total_aprovadas", len(ranking_objects))
        )
        
        top_5 = ranking_final.get_top_n(5)
        print(f"\n✓ get_top_n(5) funcionou:")
        for i, stock in enumerate(top_5, 1):
            print(f"  {i}. {stock.ticker} - Score: {stock.efficiency_score} - {stock.recomendacao_final}")
        
        # 5. Verifica idade do cache
        timestamp_str = dados.get("timestamp")
        if timestamp_str:
            timestamp = datetime.fromisoformat(timestamp_str)
            idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
            print(f"\n✓ Idade do cache: {idade_horas:.1f} horas")
            
            if idade_horas > 24:
                print(f"⚠ Cache antigo (>24h) - Recomendado executar nova análise")
            else:
                print(f"✓ Cache recente (<24h)")
        
        print("\n" + "="*80)
        print("✓ TESTE PASSOU - RANKING PODE SER CARREGADO CORRETAMENTE")
        print("="*80 + "\n")
        
        return True
    
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        print("\n" + "="*80)
        print("✗ TESTE FALHOU")
        print("="*80 + "\n")
        
        return False

if __name__ == "__main__":
    sucesso = teste_carregar_ranking()
    exit(0 if sucesso else 1)
