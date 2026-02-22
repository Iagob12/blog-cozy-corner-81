"""
SCRIPT — ETAPA 5: REVISÃO DE CARTEIRA
Revisa carteira ativa sem apego
"""
import asyncio
import sys
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.revisao_carteira import get_revisao_carteira
from app.services.context_manager import get_context_manager
from app.services.multi_groq_client import get_multi_groq_client


async def main():
    """Executa revisão de carteira"""
    print("\n" + "="*80)
    print("ETAPA 5 — REVISÃO DE CARTEIRA")
    print(f"Iniciado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("="*80 + "\n")
    
    # Carrega carteira atual
    carteira_file = "data/carteira_atual.json"
    
    if not os.path.exists(carteira_file):
        print("ERRO: Arquivo data/carteira_atual.json não encontrado!")
        print("\nCrie o arquivo com o seguinte formato:")
        print("""
{
  "posicoes": [
    {
      "ticker": "PRIO3",
      "preco_medio": 45.50,
      "preco_atual": 48.20,
      "resultado_pct": 5.9,
      "pct_carteira": 15.0,
      "data_entrada": "2026-01-15",
      "tese_original": "Empresa de petróleo com bons fundamentos..."
    }
  ]
}
        """)
        return 1
    
    try:
        # Carrega carteira
        with open(carteira_file, 'r', encoding='utf-8') as f:
            carteira_data = json.load(f)
        
        carteira_atual = carteira_data.get('posicoes', [])
        
        if not carteira_atual:
            print("ERRO: Nenhuma posição encontrada na carteira!")
            return 1
        
        print(f"CARTEIRA ATUAL: {len(carteira_atual)} posições")
        for pos in carteira_atual:
            ticker = pos.get('ticker', 'N/A')
            resultado = pos.get('resultado_pct', 0)
            pct = pos.get('pct_carteira', 0)
            print(f"  - {ticker}: {resultado:+.1f}% ({pct:.1f}% da carteira)")
        
        print("\n" + "="*80 + "\n")
        
        # Carrega contexto macro atual
        context_manager = get_context_manager()
        contexto_macro = context_manager.obter_macro()
        
        if not contexto_macro:
            print("AVISO: Contexto macro não encontrado. Execute análise V5 primeiro.")
            contexto_texto = "[Contexto macro não disponível]"
        else:
            contexto_texto = context_manager.obter_contexto_texto()
        
        # Carrega novas oportunidades (se houver)
        novas_oportunidades = None
        resultado_v5_file = "data/resultados/alpha_v5_latest.json"
        
        if os.path.exists(resultado_v5_file):
            with open(resultado_v5_file, 'r', encoding='utf-8') as f:
                resultado_v5 = json.load(f)
                novas_oportunidades = resultado_v5.get('empresas_aprovadas', [])
                
                if novas_oportunidades:
                    print(f"NOVAS OPORTUNIDADES: {len(novas_oportunidades)} empresas aprovadas")
                    for oport in novas_oportunidades[:5]:
                        ticker = oport.get('ticker', 'N/A')
                        nota = oport.get('nota', 0)
                        upside = oport.get('upside', 0)
                        print(f"  - {ticker}: Nota {nota:.1f}/10, Upside {upside:.1f}%")
                    print()
        
        print("="*80 + "\n")
        
        # Executa revisão
        groq_client = get_multi_groq_client()
        revisao_service = get_revisao_carteira(groq_client)
        
        print("Executando revisão...")
        resultado = await revisao_service.revisar_carteira(
            carteira_atual=carteira_atual,
            contexto_macro_atual=contexto_texto,
            novas_oportunidades=novas_oportunidades
        )
        
        # Salva resultado
        os.makedirs("data/revisoes", exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        arquivo = f"data/revisoes/revisao_{timestamp}.json"
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
        
        # Também salva como "latest"
        with open("data/revisoes/revisao_latest.json", 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
        
        # Atualiza contexto
        context_manager.atualizar_etapa_5_revisao(resultado)
        
        # Mostra relatório
        print("\n" + "="*80)
        print("RESULTADO DA REVISÃO")
        print("="*80 + "\n")
        
        relatorio = revisao_service.gerar_relatorio_revisao(resultado)
        print(relatorio)
        
        print("\n" + "="*80)
        print("ARQUIVOS GERADOS:")
        print(f"  - {arquivo}")
        print("  - data/revisoes/revisao_latest.json")
        print("="*80 + "\n")
        
        return 0
    
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
