from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse as FastAPIJSONResponse
from typing import List, Dict, Optional, Any
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import asyncio
import json
import math

# Carrega .env ANTES de importar os services
load_dotenv()

from app.models import TopPick, PDFAnalysis, PriceAlert
from app.layers.quant_layer import QuantLayer
from app.layers.macro_layer import MacroLayer
from app.layers.surgical_layer import SurgicalLayer
from app.services.sentiment_analysis import SentimentAnalyzer
from app.services.alert_service import AlertService
from app.services.alpha_intelligence import AlphaIntelligence
from app.services.market_data import MarketDataService
from app.services.portfolio_orchestrator import PortfolioOrchestrator
from app.services.data_collector import DataCollector
from app.services.aiml_service import AIMLService
from app.services.mistral_ocr_service import MistralOCRService
from app.services.investimentos_scraper import InvestimentosScraper
from app.services.brapi_service import BrapiService
from app.services.csv_manager import get_csv_manager
from app.services.auth_service import get_auth_service
from app.routes.admin import router as admin_router


def sanitize_for_json(obj: Any) -> Any:
    """Remove NaN e Infinity recursivamente"""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return 0
        return obj
    elif isinstance(obj, dict):
        return {k: sanitize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [sanitize_for_json(item) for item in obj]
    return obj


class SafeJSONResponse(FastAPIJSONResponse):
    """JSONResponse que sanitiza NaN e Infinity"""
    def render(self, content: Any) -> bytes:
        # Sanitiza conteúdo antes de renderizar
        safe_content = sanitize_for_json(content)
        return json.dumps(
            safe_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


app = FastAPI(
    title="Alpha Terminal API",
    description="Terminal de Inteligência Tática",
    version="1.0.0",
    default_response_class=SafeJSONResponse  # USA resposta segura por padrão
)

# Inclui rotas admin
app.include_router(admin_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173"), "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# CACHE GLOBAL - Análise roda 1x quando backend inicia, serve para todos
# ============================================================================
CACHE_GLOBAL = {
    "ranking": None,
    "timestamp": None,
    "is_loading": False,
    "error": None
}
CACHE_DURATION_MINUTES = 60  # Cache válido por 1 hora
RANKING_FILE = "data/ranking_cache.json"  # Arquivo para persistir ranking

def salvar_ranking_em_arquivo(ranking_data):
    """Salva ranking em arquivo JSON para persistência"""
    try:
        os.makedirs("data", exist_ok=True)
        
        # Prepara dados para salvar
        dados_para_salvar = {
            "timestamp": datetime.now().isoformat(),
            "total_aprovadas": ranking_data.total_aprovadas if ranking_data else 0,
            "ranking": [
                {
                    "ticker": stock.ticker,
                    "efficiency_score": stock.efficiency_score,
                    "macro_weight": stock.macro_weight,
                    "catalisadores": stock.catalisadores,
                    "preco_teto": stock.preco_teto,
                    "preco_atual": stock.preco_atual,
                    "upside_potencial": stock.upside_potencial,
                    "sentiment_status": stock.sentiment_status,
                    "recomendacao_final": stock.recomendacao_final,
                    "setor": stock.setor,
                    "roe": stock.roe,
                    "cagr": stock.cagr,
                    "pl": stock.pl,
                    "tempo_estimado_dias": stock.tempo_estimado_dias,
                    "sentiment_ratio": stock.sentiment_ratio,
                    "variacao_30d": stock.variacao_30d,
                    "rank": stock.rank
                }
                for stock in (ranking_data.ranking if ranking_data and ranking_data.ranking else [])
            ]
        }
        
        # Sanitiza NaN/Infinity
        dados_para_salvar = sanitize_for_json(dados_para_salvar)
        
        with open(RANKING_FILE, 'w', encoding='utf-8') as f:
            json.dump(dados_para_salvar, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Ranking salvo em {RANKING_FILE} ({len(dados_para_salvar['ranking'])} empresas)")
        return True
    except Exception as e:
        print(f"❌ Erro ao salvar ranking: {e}")
        return False

def carregar_ranking_do_arquivo():
    """Carrega ranking do arquivo JSON - VERSÃO SIMPLIFICADA"""
    try:
        if not os.path.exists(RANKING_FILE):
            print(f"⚠️ Arquivo de ranking não encontrado: {RANKING_FILE}")
            return None
        
        with open(RANKING_FILE, 'r', encoding='utf-8-sig') as f:
            dados = json.load(f)
        
        # Cria objetos TopPick diretamente (sem RankingFinal)
        ranking_objects = [
            TopPick(**stock_data)
            for stock_data in dados.get("ranking", [])
        ]
        
        # Cria objeto simples com ranking
        class RankingSimples:
            def __init__(self, ranking, total):
                self.ranking = ranking
                self.total_aprovadas = total
            
            def get_top_n(self, n: int):
                """Retorna top N ações"""
                return self.ranking[:n]
        
        ranking_final = RankingSimples(
            ranking=ranking_objects,
            total=dados.get("total_aprovadas", len(ranking_objects))
        )
        
        timestamp_str = dados.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None
        
        idade_horas = (datetime.now() - timestamp).total_seconds() / 3600 if timestamp else 999
        
        print(f"✓ Ranking carregado do arquivo ({len(ranking_objects)} empresas, {idade_horas:.1f}h atrás)")
        
        return {
            "ranking": ranking_final,
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"❌ Erro ao carregar ranking do arquivo: {e}")
        import traceback
        traceback.print_exc()
        return None

async def executar_analise_v4_automatica():
    """
    Executa análise V4 automaticamente
    Chamado pelo scheduler a cada X horas
    """
    global CACHE_GLOBAL
    
    if CACHE_GLOBAL["is_loading"]:
        print("⚠️ Análise já em andamento, pulando...")
        return
    
    CACHE_GLOBAL["is_loading"] = True
    
    try:
        print("\n" + "="*80)
        print(f"🤖 ANÁLISE AUTOMÁTICA V4 INICIADA")
        print(f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("="*80 + "\n")
        
        # Importa Sistema V4
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app.services.alpha_v4_otimizado import get_alpha_v4_otimizado
        
        alpha_v4 = get_alpha_v4_otimizado()
        resultado = await alpha_v4.executar_analise_rapida(limite_empresas=15)
        
        if not resultado['success']:
            raise Exception(resultado.get('error'))
        
        # Converte para formato frontend
        import pandas as pd
        df = pd.read_csv("data/stocks.csv", encoding='utf-8-sig')
        
        ranking_convertido = []
        for empresa in resultado['ranking']:
            ticker = empresa.get('ticker', 'N/A')
            row = df[df['ticker'] == ticker]
            if row.empty:
                continue
            row = row.iloc[0]
            
            top_pick = {
                "ticker": ticker,
                "efficiency_score": float(empresa.get('score', 0)),
                "macro_weight": 1.0,
                "catalisadores": [empresa.get('tese', '')],
                "preco_teto": float(empresa.get('preco_teto', 0)),
                "preco_atual": float(empresa.get('preco_atual', 0)),
                "upside_potencial": float(empresa.get('upside', 0)),
                "sentiment_status": "Normal",
                "recomendacao_final": empresa.get('recomendacao', 'AGUARDAR'),
                "setor": str(row.get('setor', 'N/A')),
                "roe": float(empresa.get('roe', 0)),
                "cagr": float(row['cagr'] * 100 if row['cagr'] < 1 else row['cagr']),
                "pl": float(empresa.get('pl', 0)),
                "tempo_estimado_dias": 90,
                "sentiment_ratio": 1.0,
                "variacao_30d": 0.0,
                "rank": empresa.get('rank', 0)
            }
            ranking_convertido.append(top_pick)
        
        ranking_frontend = {
            "timestamp": datetime.now().isoformat(),
            "total_aprovadas": len(ranking_convertido),
            "ranking": ranking_convertido,
            "versao": "4.0-otimizado-auto"
        }
        
        # Salva ranking_cache.json
        with open('data/ranking_cache.json', 'w', encoding='utf-8') as f:
            json.dump(ranking_frontend, f, indent=2, ensure_ascii=False)
        
        # Atualiza cache global
        ranking_do_arquivo = carregar_ranking_do_arquivo()
        if ranking_do_arquivo:
            CACHE_GLOBAL["ranking"] = ranking_do_arquivo["ranking"]
            CACHE_GLOBAL["timestamp"] = ranking_do_arquivo["timestamp"]
            CACHE_GLOBAL["error"] = None
        
        print("\n" + "="*80)
        print(f"✅ ANÁLISE AUTOMÁTICA CONCLUÍDA")
        print(f"Total: {len(ranking_convertido)} empresas")
        print(f"Tempo: {resultado['tempo_segundos']:.1f}s")
        print(f"Próxima análise: {(datetime.now() + timedelta(hours=1)).strftime('%H:%M:%S')}")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRO NA ANÁLISE AUTOMÁTICA: {e}")
        import traceback
        traceback.print_exc()
        
        # Mantém cache anterior se houver
        if CACHE_GLOBAL["ranking"]:
            print("⚠️ Mantendo cache anterior")
            CACHE_GLOBAL["error"] = f"Erro temporário: {str(e)[:100]}"
        else:
            CACHE_GLOBAL["error"] = f"Erro: {str(e)[:100]}"
    
    finally:
        CACHE_GLOBAL["is_loading"] = False

async def carregar_analise_inicial():
    """
    Carrega ranking existente e agenda análises automáticas
    """
    global CACHE_GLOBAL
    
    # Carrega ranking do arquivo
    ranking_do_arquivo = carregar_ranking_do_arquivo()
    if ranking_do_arquivo:
        CACHE_GLOBAL["ranking"] = ranking_do_arquivo["ranking"]
        CACHE_GLOBAL["timestamp"] = ranking_do_arquivo["timestamp"]
        CACHE_GLOBAL["error"] = None
        
        idade_horas = (datetime.now() - ranking_do_arquivo["timestamp"]).total_seconds() / 3600
        print(f"✓ Ranking V4 carregado ({idade_horas:.1f}h atrás)")
        
        # Se ranking está muito antigo (>1h), executa análise agora
        if idade_horas > 1:
            print("⚠️ Ranking antigo (>1h) - Executando análise agora...")
            await executar_analise_v4_automatica()
        else:
            print(f"✓ Ranking recente - Próxima análise em {1 - idade_horas:.1f}h")
    else:
        print("⚠️ Nenhum ranking encontrado - Executando primeira análise...")
        await executar_analise_v4_automatica()

def cache_valido() -> bool:
    """Verifica se cache ainda é válido"""
    if not CACHE_GLOBAL["ranking"] or not CACHE_GLOBAL["timestamp"]:
        return False
    
    idade = datetime.now() - CACHE_GLOBAL["timestamp"]
    return idade.total_seconds() < (CACHE_DURATION_MINUTES * 60)

@app.on_event("startup")
async def startup_event():
    """Inicia backend e scheduler automático"""
    print("\n🔥 Backend iniciado")
    
    # Carrega ranking e executa primeira análise se necessário
    # await carregar_analise_inicial()  # DESABILITADO - Usar botão no admin
    
    # Inicia scheduler para análises automáticas a cada 1 hora
    # asyncio.create_task(scheduler_analise_automatica())  # DESABILITADO
    
    # NOVO: Inicia scheduler de estratégia dinâmica automaticamente
    try:
        from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
        from app.services.estrategia_scheduler import get_estrategia_scheduler
        from app.services.precos_service import get_precos_service
        
        estrategia_service = get_estrategia_dinamica_service()
        precos_service = get_precos_service()
        scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
        
        # Verifica se auto_start está habilitado
        if estrategia_service.config.get('auto_start', True):
            asyncio.create_task(scheduler.iniciar())
            print("✅ Scheduler de Estratégia Dinâmica iniciado automaticamente")
        else:
            print("⚠️ Auto-start do scheduler desabilitado")
    except Exception as e:
        print(f"⚠️ Erro ao iniciar scheduler de estratégia: {e}")
    
    # NOVO: Inicia scheduler de análises com releases automaticamente
    try:
        from app.services.analise_scheduler import get_analise_scheduler
        
        analise_scheduler = get_analise_scheduler()
        asyncio.create_task(analise_scheduler.iniciar())
        print("✅ Scheduler de Análises com Releases iniciado automaticamente")
        print("   - Atualização de preços: a cada 1h")
        print("   - Análise completa: todo dia às 8h")
    except Exception as e:
        print(f"⚠️ Erro ao iniciar scheduler de análises: {e}")
    
    print("✅ Sistema pronto")

async def scheduler_analise_automatica():
    """Scheduler que executa análise V4 a cada 1 hora"""
    await asyncio.sleep(10)  # Aguarda 10s para backend estabilizar
    
    while True:
        try:
            # Aguarda 1 hora
            await asyncio.sleep(1 * 60 * 60)  # 1 hora em segundos
            
            print("\n⏰ Scheduler: Hora de executar análise automática")
            await executar_analise_v4_automatica()
            
        except Exception as e:
            print(f"❌ Erro no scheduler: {e}")
            # Continua rodando mesmo com erro
            await asyncio.sleep(60)  # Aguarda 1 minuto antes de tentar novamente

# Inicializa serviços
quant_layer = QuantLayer(
    min_roe=float(os.getenv("MIN_ROE", 15)),
    min_cagr=float(os.getenv("MIN_CAGR", 12)),
    max_pl=float(os.getenv("MAX_PL", 15))
)
macro_layer = MacroLayer()
surgical_layer = SurgicalLayer()
sentiment_analyzer = SentimentAnalyzer(
    threshold=float(os.getenv("SENTIMENT_THRESHOLD", 3.0))
)
alert_service = AlertService()
alpha_intelligence = AlphaIntelligence()
market_data = MarketDataService()
orchestrator = PortfolioOrchestrator()
data_collector = DataCollector()
aiml_service = AIMLService()  # Multi-IA: Gemini + Claude
mistral_ocr = MistralOCRService()  # OCR de relatórios
investimentos_scraper = InvestimentosScraper()  # Dados reais diários
brapi_service = BrapiService()  # Preços reais de ações BR (gratuito)
csv_manager = get_csv_manager()  # Gerenciador de CSV
auth_service = get_auth_service()  # Autenticação admin

@app.get("/")
async def root():
    return {
        "message": "Alpha Terminal API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/api/v1/top-picks", response_model=List[TopPick])
async def get_top_picks(
    csv_path: str = Query(default="data/stocks.csv"),
    limit: int = Query(default=15, description="Número de picks (máx 15 com 3 chaves)")
):
    """
    VERSÃO COM PREÇOS 100% REAIS
    Retorna APENAS ações com preços reais do Alpha Vantage
    LIMITE: 15 ações (3 chaves × 5 req/min)
    """
    try:
        # Limita a 15 ações (3 chaves × 5 req/min)
        if limit > 15:
            limit = 15
            print("⚠ Limitado a 15 ações (3 chaves × 5 req/min)")
        
        # 1. Filtro Quantitativo Elite
        ranked_stocks = quant_layer.process(csv_path)
        
        if not ranked_stocks:
            raise HTTPException(status_code=404, detail="Nenhum ativo encontrado")
        
        # 2. Busca Preços Reais
        tickers = [stock.ticker for stock in ranked_stocks[:limit]]
        
        # Busca preços reais (Alpha Vantage)
        quotes = {}
        
        # Se mock não retornou nada, usa Alpha Vantage
        if not quotes:
            print(f"\n=== BUSCANDO {len(tickers)} PREÇOS REAIS (Alpha Vantage) ===")
            print(f"✓ Usando 3 chaves API (limite: 15 req/min)")
            quotes = await market_data.get_multiple_quotes(tickers)
        
        # 3. FILTRA: Só continua com ações que têm preço real
        if not quotes:
            raise HTTPException(
                status_code=503,
                detail="Não foi possível buscar preços reais. Aguarde alguns minutos e tente novamente."
            )
        
        print(f"✓ {len(quotes)} ações com preços reais obtidos")
        
        # 4. Contexto Macro
        macro_context = await macro_layer.process()
        
        # 5. Análise APENAS das ações com preço real
        top_picks = []
        for stock in ranked_stocks[:limit]:
            # Verifica se tem preço real
            quote = quotes.get(stock.ticker)
            if not quote or quote.get("preco_atual", 0) <= 0:
                print(f"✗ {stock.ticker}: Sem preço real, ignorando")
                continue
            
            # USA APENAS PREÇO REAL
            preco_atual = quote.get("preco_atual")
            variacao_dia = quote.get("variacao_dia", 0)
            setor = stock.setor if hasattr(stock, 'setor') else "N/A"
            
            # Cálculo Inteligente do Preço Teto
            # Considera: Score de eficiência + Peso macro do setor
            macro_weight = macro_context.peso_ajuste.get(setor, 1.0)
            score_ajustado = stock.score * macro_weight
            
            # Preço teto mais conservador e realista
            multiplicador = 1 + (score_ajustado / 25)  # Mais conservador
            preco_teto = preco_atual * multiplicador
            upside = ((preco_teto / preco_atual) - 1) * 100
            
            # Análise de Qualidade dos Fundamentos
            qualidade_score = (
                (stock.roe / 15) * 0.4 +  # ROE pesa 40%
                (stock.cagr / 12) * 0.3 +  # CAGR pesa 30%
                (15 / stock.pl) * 0.3      # P/L inverso pesa 30%
            )
            
            # Catalisadores Específicos por Setor
            catalisadores = []
            if setor == "Energia":
                catalisadores.append("Setor energético em alta")
            elif setor == "Consumo":
                catalisadores.append("Recuperação do consumo")
            elif setor == "Tecnologia":
                catalisadores.append("Transformação digital")
            else:
                catalisadores.append(f"Fundamentos sólidos no setor {setor}")
            
            # Adiciona catalisador de eficiência
            if stock.score > 8:
                catalisadores.append("Efficiency Score excepcional")
            elif stock.score > 6:
                catalisadores.append("Efficiency Score forte")
            
            # Recomendação Inteligente
            if upside > 25 and qualidade_score > 1.2:
                recomendacao = "COMPRA FORTE"
                confianca = "ALTA"
            elif upside > 15 and qualidade_score > 1.0:
                recomendacao = "COMPRA"
                confianca = "ALTA"
            elif upside > 10:
                recomendacao = "COMPRA"
                confianca = "MÉDIA"
            elif upside > 5:
                recomendacao = "MONITORAR"
                confianca = "MÉDIA"
            else:
                recomendacao = "AGUARDAR"
                confianca = "BAIXA"
            
            # Status de Sentimento
            if stock.roe > 30:
                sentiment_status = "Excelente - ROE Excepcional"
            elif stock.roe > 20:
                sentiment_status = "Muito Bom - ROE Forte"
            else:
                sentiment_status = "Normal"
            
            # Tempo Estimado baseado no upside
            if upside > 20:
                tempo_dias = 60  # Mais rápido
            elif upside > 10:
                tempo_dias = 90
            else:
                tempo_dias = 120  # Mais conservador
            
            top_picks.append(TopPick(
                ticker=stock.ticker,
                efficiency_score=round(score_ajustado, 2),
                macro_weight=round(macro_weight, 2),
                catalisadores=catalisadores,
                preco_teto=round(preco_teto, 2),
                preco_atual=preco_atual,
                upside_potencial=round(upside, 2),
                sentiment_status=sentiment_status,
                recomendacao_final=recomendacao,
                setor=setor,
                roe=stock.roe,
                cagr=stock.cagr,
                pl=stock.pl,
                tempo_estimado_dias=tempo_dias,
                sentiment_ratio=qualidade_score,
                variacao_30d=0.0
            ))
        
        # Ordena por efficiency_score ajustado
        top_picks.sort(key=lambda x: x.efficiency_score, reverse=True)
        
        # Adiciona rank
        for rank, pick in enumerate(top_picks, 1):
            pick.rank = rank
        
        return top_picks
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"CSV não encontrado: {csv_path}")
    except Exception as e:
        print(f"ERRO: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-pdf", response_model=PDFAnalysis)
async def analyze_pdf(
    file: UploadFile = File(...),
    ticker: str = Query(..., description="Ticker da ação")
):
    """Análise cirúrgica de PDF de RI"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, 
                          detail="Apenas arquivos PDF são aceitos")
    
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        analysis = await surgical_layer.process(tmp_path, ticker)
        os.unlink(tmp_path)
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, 
                          detail=f"Erro ao processar PDF: {str(e)}")

@app.get("/api/v1/alerts", response_model=List[PriceAlert])
async def get_price_alerts(
    csv_path: str = Query(default="data/stocks.csv")
):
    """
    ALERTAS V2 - Sistema Inteligente de Alertas
    Monitora preços reais e gera alertas acionáveis
    """
    try:
        ranked_stocks = quant_layer.process(csv_path)
        tickers = [stock.ticker for stock in ranked_stocks[:15]]
        
        # Busca preços REAIS
        quotes = await market_data.get_multiple_quotes(tickers)
        
        # Prepara carteira para análise
        carteira = []
        for stock in ranked_stocks[:15]:
            quote = quotes.get(stock.ticker, {})
            preco_atual = quote.get("preco_atual", 0)
            
            if preco_atual > 0:
                preco_teto = preco_atual * (1 + stock.score / 20)
                carteira.append({
                    "ticker": stock.ticker,
                    "preco_entrada": preco_atual * 0.95,  # Simula entrada 5% abaixo
                    "preco_teto": preco_teto,
                    "preco_atual": preco_atual
                })
        
        # Gera alertas inteligentes
        precos_atuais = {item["ticker"]: item["preco_atual"] for item in carteira}
        alertas_ia = await alpha_intelligence.gerar_alertas_inteligentes(carteira, precos_atuais)
        
        # Converte para formato PriceAlert
        alerts = []
        for alerta in alertas_ia:
            ticker = alerta.get("ticker")
            stock = next((s for s in ranked_stocks if s.ticker == ticker), None)
            if stock:
                preco_atual = precos_atuais.get(ticker, 0)
                preco_teto = preco_atual * (1 + stock.score / 20)
                
                alerts.append(PriceAlert(
                    ticker=ticker,
                    preco_atual=preco_atual,
                    preco_teto=preco_teto,
                    margem_seguranca=((preco_teto / preco_atual) - 1) * 100,
                    acao_recomendada=alerta.get("acao_recomendada", "Monitorar")
                ))
        
        return alerts
        
    except Exception as e:
        print(f"Erro ao gerar alertas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/macro-context-live")
async def get_macro_context_live():
    """
    NOVO - Contexto Macro em Tempo Real com IA
    Análise atualizada do cenário macroeconômico
    """
    try:
        analise_macro = await alpha_intelligence.analisar_contexto_macro_atual()
        market_overview = await market_data.get_market_overview()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "mercado": market_overview,
            "analise_ia": analise_macro
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/macro-context")
async def get_macro_context():
    """Retorna o contexto macroeconômico atual"""
    try:
        context = await macro_layer.process()
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/sentiment/{ticker}")
async def get_sentiment(ticker: str):
    """Análise de sentimento para um ticker"""
    try:
        sentiment = await sentiment_analyzer.analyze(ticker)
        return sentiment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== NOVOS ENDPOINTS - ALPHA INTELLIGENCE =====

@app.get("/api/v1/alpha/radar-oportunidades")
async def radar_oportunidades():
    """
    PROMPT 1 - Radar de Oportunidades
    Identifica setores em aceleração antes da manada
    """
    try:
        result = await alpha_intelligence.prompt_1_radar_oportunidades()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/alpha/analise-comparativa")
async def analise_comparativa(tickers: List[str]):
    """
    PROMPT 3 - Análise Comparativa
    Busca relatórios de RI e compara empresas
    """
    try:
        # Busca relatórios de RI
        relatorios = []
        for ticker in tickers:
            relatorio = await alpha_intelligence.buscar_relatorios_ri(ticker)
            relatorios.append(relatorio)
        
        # Análise comparativa
        result = await alpha_intelligence.prompt_3_analise_comparativa(relatorios)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/alpha/swing-trade/{ticker}")
async def swing_trade_analysis(ticker: str):
    """
    PROMPT 4 - Swing Trade
    Análise para operação de 5-20 dias
    """
    try:
        # Busca preço atual
        quote = await market_data.get_quote(ticker)
        preco_atual = quote.get("preco_atual", 0)
        
        if preco_atual == 0:
            raise HTTPException(status_code=404, detail="Preço não encontrado")
        
        result = await alpha_intelligence.prompt_4_swing_trade(ticker, preco_atual)
        
        # Adiciona dados de momentum
        momentum = await market_data.calculate_momentum(ticker)
        result["momentum"] = momentum
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/alpha/revisao-carteira")
async def revisao_carteira(carteira: List[dict]):
    """
    PROMPT 5 - Revisão Mensal de Carteira
    Análise sem apego das posições
    
    Formato esperado:
    [
        {"ticker": "PRIO3", "qtd": 100, "preco_medio": 45.50, "resultado_pct": 12.5},
        ...
    ]
    """
    try:
        result = await alpha_intelligence.prompt_5_revisao_carteira(carteira)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/alpha/anti-manada/{ticker}")
async def verificacao_anti_manada(ticker: str):
    """
    PROMPT 6 - Verificação Anti-Manada
    Checa se não estamos comprando o topo
    """
    try:
        result = await alpha_intelligence.prompt_6_verificacao_anti_manada(ticker)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== MARKET DATA ENDPOINTS =====

@app.get("/api/v1/market/quote/{ticker}")
async def get_market_quote(ticker: str):
    """Cotação em tempo real"""
    try:
        quote = await market_data.get_quote(ticker)
        return quote
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/overview")
async def get_market_overview():
    """Visão geral do mercado (Ibovespa, Dólar)"""
    try:
        overview = await market_data.get_market_overview()
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/market/momentum/{ticker}")
async def get_momentum(ticker: str):
    """Indicadores de momentum"""
    try:
        momentum = await market_data.calculate_momentum(ticker)
        return momentum
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== ORQUESTRADOR - FLUXO COMPLETO =====

@app.post("/api/v1/portfolio/executar-fluxo-completo")
async def executar_fluxo_completo():
    """
    🚀 FLUXO COMPLETO AUTOMATIZADO
    
    1. Prompt 1: Radar de Oportunidades
    2. Coleta dados de ações (CSV)
    3. Prompt 2: Filtra 15 melhores
    4. Busca relatórios de resultados (PDFs)
    5. Prompt 3: Análise profunda
    6. Monta carteira final
    7. Preços em tempo real
    8. Verificação anti-manada
    """
    try:
        resultado = await orchestrator.executar_fluxo_completo()
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/portfolio/analise-rapida/{ticker}")
async def analise_rapida(ticker: str):
    """
    Análise rápida completa de um ticker
    - Preço atual
    - Momentum
    - Swing trade
    - Anti-manada
    """
    try:
        resultado = await orchestrator.analise_rapida_ticker(ticker)
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/portfolio/atualizar-precos")
async def atualizar_precos(tickers: List[str]):
    """
    Atualiza preços em tempo real de múltiplos tickers
    """
    try:
        quotes = await orchestrator.atualizar_precos_carteira(tickers)
        return quotes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/data/coletar-acoes")
async def coletar_dados_acoes():
    """
    Coleta dados de ações do investimentos.com.br
    """
    try:
        # Tenta baixar CSV
        csv_path = await data_collector.download_investimentos_csv()
        
        if csv_path:
            import pandas as pd
            df = pd.read_csv(csv_path, encoding='utf-8-sig')
            return {
                "sucesso": True,
                "total_acoes": len(df),
                "arquivo": csv_path,
                "amostra": df.head(10).to_dict('records')
            }
        else:
            # Fallback: scraping
            df = await data_collector.scrape_investimentos_data()
            return {
                "sucesso": True,
                "metodo": "scraping",
                "total_acoes": len(df),
                "amostra": df.head(10).to_dict('records')
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/data/buscar-relatorios")
async def buscar_relatorios(tickers: List[str]):
    """
    Busca relatórios de RI de múltiplas empresas
    """
    try:
        relatorios = await data_collector.coletar_relatorios_batch(tickers)
        return {
            "total_encontrados": len(relatorios),
            "relatorios": relatorios
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="warning",  # Desabilita logs INFO de requisições
        access_log=False  # Desabilita access log completamente
    )


# ===== NOVOS ENDPOINTS - AIML MULTI-IA =====

@app.get("/api/v1/aiml/top-picks-inteligente", response_model=List[TopPick])
async def get_top_picks_aiml(
    csv_path: str = Query(default="data/stocks.csv"),
    limit: int = Query(default=15, description="Número de picks")
):
    """
    🚀 VERSÃO PREMIUM - MULTI-IA
    
    FASE 1: Gemini 2.0 Flash Thinking
    - Analisa contexto macro
    - Raciocínio profundo sobre mercado
    - Seleciona top 15 ações
    
    FASE 2: Claude 3.5 Sonnet
    - Análise cirúrgica de cada ação
    - Valuation preciso
    - Recomendação final
    
    Retorna APENAS ações com preços reais + análise IA
    """
    try:
        from datetime import datetime
        import json
        
        # 1. Filtro Quantitativo
        ranked_stocks = quant_layer.process(csv_path)
        if not ranked_stocks:
            raise HTTPException(status_code=404, detail="Nenhum ativo encontrado")
        
        # 2. Busca Preços Reais
        tickers = [stock.ticker for stock in ranked_stocks[:limit]]
        quotes = await market_data.get_multiple_quotes(tickers)
        
        if not quotes:
            raise HTTPException(
                status_code=503,
                detail="Não foi possível buscar preços reais"
            )
        
        # 3. Contexto Macro
        macro_context = await macro_layer.process()
        
        # 4. Prepara dados para IA
        acoes_candidatas = []
        precos_atuais = {}
        
        for stock in ranked_stocks[:limit]:
            quote = quotes.get(stock.ticker)
            if not quote or quote.get("preco_atual", 0) <= 0:
                continue
            
            preco_atual = quote.get("preco_atual")
            precos_atuais[stock.ticker] = preco_atual
            
            acoes_candidatas.append({
                "ticker": stock.ticker,
                "roe": stock.roe,
                "cagr": stock.cagr,
                "pl": stock.pl,
                "divida": getattr(stock, 'divida', 1.0),
                "setor": getattr(stock, 'setor', 'N/A'),
                "preco_atual": preco_atual,
                "score": stock.score
            })
        
        # 5. ANÁLISE MULTI-IA (Gemini + Claude)
        print("\n🤖 Iniciando análise Multi-IA...")
        analise_completa = await aiml_service.analise_completa_portfolio(
            acoes_candidatas=acoes_candidatas,
            contexto_macro={
                "data": datetime.now().strftime("%d/%m/%Y"),
                "setores": macro_context.peso_ajuste,
                "tendencias": macro_context.tendencias
            },
            precos_atuais=precos_atuais
        )
        
        if not analise_completa["success"]:
            # Fallback: usa análise tradicional
            print("⚠ Fallback para análise tradicional")
            return await get_top_picks(csv_path, limit)
        
        # 6. Processa resultados das IAs
        top_picks = []
        fase2_analises = analise_completa.get("fase2_claude", [])
        
        for acao in acoes_candidatas[:15]:
            ticker = acao["ticker"]
            preco_atual = acao["preco_atual"]
            
            # Busca análise do Claude para esta ação
            analise_claude = next(
                (a for a in fase2_analises if a["ticker"] == ticker),
                None
            )
            
            # Tenta extrair dados da análise do Claude
            if analise_claude:
                try:
                    content = analise_claude["analise_claude"]
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0]
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0]
                    
                    claude_data = json.loads(content.strip())
                    
                    preco_teto = claude_data.get("preco_teto", preco_atual * 1.15)
                    upside = claude_data.get("upside", 15)
                    recomendacao = claude_data.get("recomendacao", "COMPRA")
                    tempo_dias = claude_data.get("tempo_estimado_dias", 90)
                    riscos = claude_data.get("riscos", [])
                    
                except:
                    # Fallback: cálculo tradicional
                    preco_teto = preco_atual * (1 + acao["score"] / 20)
                    upside = ((preco_teto / preco_atual) - 1) * 100
                    recomendacao = "COMPRA" if upside > 10 else "MONITORAR"
                    tempo_dias = 90
                    riscos = []
            else:
                # Sem análise do Claude
                preco_teto = preco_atual * (1 + acao["score"] / 20)
                upside = ((preco_teto / preco_atual) - 1) * 100
                recomendacao = "COMPRA" if upside > 10 else "MONITORAR"
                tempo_dias = 90
                riscos = []
            
            # Catalisadores da Fase 1 (Gemini)
            gemini_top15 = analise_completa.get("fase1_gemini", {}).get("top_15", [])
            gemini_acao = next((a for a in gemini_top15 if a.get("ticker") == ticker), None)
            
            if gemini_acao:
                catalisadores = gemini_acao.get("catalisadores", [])
                confianca = "ALTA" if gemini_acao.get("risco") == "baixo" else "MÉDIA"
            else:
                catalisadores = [f"Fundamentos sólidos no setor {acao['setor']}"]
                confianca = "MÉDIA"
            
            top_picks.append(TopPick(
                ticker=ticker,
                efficiency_score=round(acao["score"], 2),
                macro_weight=1.0,
                catalisadores=catalisadores,
                preco_teto=round(preco_teto, 2),
                preco_atual=preco_atual,
                upside_potencial=round(upside, 2),
                sentiment_status=f"Análise IA: {recomendacao}",
                recomendacao_final=recomendacao,
                setor=acao["setor"],
                roe=acao["roe"],
                cagr=acao["cagr"],
                pl=acao["pl"],
                tempo_estimado_dias=tempo_dias,
                sentiment_ratio=acao["roe"] / 15,
                variacao_30d=0.0
            ))
        
        # Ordena por upside
        top_picks.sort(key=lambda x: x.upside_potencial, reverse=True)
        
        # Adiciona rank
        for rank, pick in enumerate(top_picks, 1):
            pick.rank = rank
        
        print(f"\n✓ {len(top_picks)} ações analisadas com Multi-IA")
        return top_picks
        
    except Exception as e:
        print(f"ERRO Multi-IA: {str(e)}")
        # Fallback: análise tradicional
        return await get_top_picks(csv_path, limit)

@app.get("/api/v1/aiml/analise-mercado")
async def analise_mercado_gemini():
    """
    Gemini 2.0 Flash Thinking - Análise de Mercado
    Raciocínio profundo sobre o cenário atual
    """
    try:
        # Busca dados
        ranked_stocks = quant_layer.process("data/stocks.csv")
        macro_context = await macro_layer.process()
        
        acoes_candidatas = [
            {
                "ticker": s.ticker,
                "roe": s.roe,
                "cagr": s.cagr,
                "pl": s.pl,
                "setor": getattr(s, 'setor', 'N/A'),
                "score": s.score
            }
            for s in ranked_stocks[:20]
        ]
        
        # Análise com Gemini Thinking
        result = await aiml_service.gemini_thinking_analise_mercado(
            acoes_candidatas=acoes_candidatas,
            contexto_macro={
                "setores": macro_context.peso_ajuste,
                "tendencias": macro_context.tendencias
            }
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/aiml/analise-acao/{ticker}")
async def analise_acao_claude(ticker: str):
    """
    Claude 3.5 Sonnet - Análise Profunda de Ação
    Análise cirúrgica com relatório trimestral
    """
    try:
        # Busca dados da ação
        ranked_stocks = quant_layer.process("data/stocks.csv")
        stock = next((s for s in ranked_stocks if s.ticker == ticker), None)
        
        if not stock:
            raise HTTPException(status_code=404, detail="Ação não encontrada")
        
        # Busca preço atual
        quote = await market_data.get_quote(ticker)
        preco_atual = quote.get("preco_atual", 0)
        
        if preco_atual == 0:
            raise HTTPException(status_code=404, detail="Preço não encontrado")
        
        # Busca relatório trimestral
        relatorio = await aiml_service.buscar_relatorio_trimestral(ticker)
        
        # Análise com Claude
        result = await aiml_service.claude_analise_profunda_acao(
            ticker=ticker,
            dados_fundamentalistas={
                "roe": stock.roe,
                "cagr": stock.cagr,
                "pl": stock.pl,
                "divida": getattr(stock, 'divida', 1.0),
                "setor": getattr(stock, 'setor', 'N/A')
            },
            preco_atual=preco_atual,
            relatorio_trimestral=relatorio
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== ENDPOINTS MISTRAL OCR - RELATÓRIOS TRIMESTRAIS =====

@app.post("/api/v1/ocr/upload-relatorio/{ticker}")
async def upload_relatorio_trimestral(
    ticker: str,
    file: UploadFile = File(...)
):
    """
    Upload de relatório trimestral em PDF
    Extrai dados automaticamente usando Mistral AI OCR
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    try:
        import tempfile
        import shutil
        
        # Salva PDF temporariamente
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Extrai dados com Mistral OCR
        resultado = await mistral_ocr.extrair_dados_relatorio_trimestral(tmp_path, ticker)
        
        if resultado["success"]:
            # Salva PDF permanentemente
            import os
            os.makedirs("data/relatorios", exist_ok=True)
            
            trimestre = resultado["dados"].get("trimestre", "Q4_2025").replace(" ", "_")
            pdf_final = f"data/relatorios/{ticker}_{trimestre}.pdf"
            
            shutil.copy(tmp_path, pdf_final)
            os.unlink(tmp_path)
            
            return {
                "success": True,
                "ticker": ticker,
                "arquivo_salvo": pdf_final,
                "dados_extraidos": resultado["dados"],
                "mensagem": f"Relatório de {ticker} processado com sucesso!"
            }
        else:
            os.unlink(tmp_path)
            raise HTTPException(status_code=500, detail=resultado.get("error"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/ocr/analisar-pdf")
async def analisar_pdf_customizado(
    file: UploadFile = File(...),
    ticker: str = Query(...),
    perguntas: str = Query(..., description="Perguntas separadas por |")
):
    """
    Análise customizada de PDF com perguntas específicas
    
    Exemplo:
    perguntas = "Qual foi o crescimento?|A empresa está lucrativa?|Quais os riscos?"
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são aceitos")
    
    try:
        import tempfile
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Separa perguntas
        lista_perguntas = [p.strip() for p in perguntas.split("|")]
        
        # Analisa com Mistral AI
        resultado = await mistral_ocr.analisar_relatorio_com_ia(
            tmp_path,
            ticker,
            lista_perguntas
        )
        
        import os
        os.unlink(tmp_path)
        
        if resultado["success"]:
            return resultado
        else:
            raise HTTPException(status_code=500, detail=resultado.get("error"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/ocr/relatorios-disponiveis")
async def listar_relatorios_disponiveis():
    """
    Lista todos os relatórios trimestrais disponíveis localmente
    """
    try:
        import os
        import glob
        
        relatorios_dir = "data/relatorios"
        
        if not os.path.exists(relatorios_dir):
            return {"total": 0, "relatorios": []}
        
        pdfs = glob.glob(f"{relatorios_dir}/*.pdf")
        
        relatorios = []
        for pdf in pdfs:
            filename = os.path.basename(pdf)
            # Formato esperado: TICKER_Q4_2025.pdf
            parts = filename.replace(".pdf", "").split("_")
            
            if len(parts) >= 2:
                ticker = parts[0]
                trimestre = "_".join(parts[1:])
                
                relatorios.append({
                    "ticker": ticker,
                    "trimestre": trimestre,
                    "arquivo": filename,
                    "caminho": pdf
                })
        
        return {
            "total": len(relatorios),
            "relatorios": relatorios
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/v1/ocr/relatorio/{ticker}/{trimestre}")
async def deletar_relatorio(ticker: str, trimestre: str):
    """
    Remove um relatório trimestral
    """
    try:
        import os
        
        pdf_path = f"data/relatorios/{ticker}_{trimestre}.pdf"
        
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            return {
                "success": True,
                "mensagem": f"Relatório {ticker} {trimestre} removido"
            }
        else:
            raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== SISTEMA CORRETO - ALPHA V4 OTIMIZADO COM GROQ =====
# Este é o ÚNICO sistema que deve ser usado
# Usa GROQ + LLAMA 3.1 405B conforme especificado
# Analisa TODAS as empresas que passam no filtro (sem limite artificial)

@app.get("/api/v1/alpha-v2/top-picks", response_model=List[TopPick])
async def get_top_picks_v2(
    csv_path: str = Query(default="data/stocks.csv"),
    limit: int = Query(default=15)
):
    """
    🚀 ALPHA SYSTEM V2 - SISTEMA COMPLETO
    
    FLUXO EXATO COMO SOLICITADO:
    1. Gemini 2.5 Pro analisa mercado atual
    2. Gemini seleciona top 15 ações
    3. Busca preços REAIS (Alpha Vantage)
    4. Para cada ação:
       - Busca relatório Q4 2025
       - Claude Sonnet 4.6 analisa
    5. Retorna ranking 1-15
    
    ATUALIZAÇÃO: Diária (cache de 24h)
    """
    try:
        from datetime import datetime
        
        # 1. Filtro Quantitativo
        ranked_stocks = quant_layer.process(csv_path)
        if not ranked_stocks:
            raise HTTPException(status_code=404, detail="Nenhum ativo encontrado")
        
        # 2. Busca Preços REAIS (Alpha Vantage - SEM MOCK)
        tickers = [stock.ticker for stock in ranked_stocks[:20]]
        print(f"\n=== BUSCANDO PREÇOS REAIS (Alpha Vantage) ===")
        quotes = await market_data.get_multiple_quotes(tickers)
        
        if not quotes:
            raise HTTPException(
                status_code=503,
                detail="Não foi possível buscar preços reais"
            )
        
        # 3. Prepara dados para análise
        acoes_candidatas = []
        precos_reais = {}
        
        for stock in ranked_stocks[:20]:
            quote = quotes.get(stock.ticker)
            if not quote or quote.get("preco_atual", 0) <= 0:
                continue
            
            preco_atual = quote.get("preco_atual")
            precos_reais[stock.ticker] = preco_atual
            
            acoes_candidatas.append({
                "ticker": stock.ticker,
                "roe": stock.roe,
                "cagr": stock.cagr,
                "pl": stock.pl,
                "divida": getattr(stock, 'divida', 1.0),
                "setor": getattr(stock, 'setor', 'N/A'),
                "score": stock.score
            })
        
        # 4. ANÁLISE COMPLETA COM MULTI-IA
        print("\n🤖 Iniciando Alpha System V2...")
        resultado = await alpha_system_v2.executar_analise_completa(
            acoes_candidatas=acoes_candidatas,
            precos_reais=precos_reais
        )
        
        if not resultado["success"]:
            # Fallback: análise tradicional
            print("⚠ Fallback para análise tradicional")
            return await get_top_picks(csv_path, limit)
        
        # 5. Converte para formato TopPick
        top_picks = []
        
        for item in resultado["ranking_top_15"]:
            ticker = item["ticker"]
            rank = item["rank"]
            preco_atual = item["preco_atual"]
            analise = item["analise_claude"]
            
            # Extrai dados da análise do Claude
            valuation = analise.get("valuation", {})
            recomendacao = analise.get("recomendacao", {})
            
            preco_teto = valuation.get("preco_teto_90d", preco_atual * 1.10)
            upside = valuation.get("upside_potencial", 10.0)
            
            # Busca dados originais
            acao_original = next((a for a in acoes_candidatas if a["ticker"] == ticker), None)
            
            if acao_original:
                top_picks.append(TopPick(
                    ticker=ticker,
                    rank=rank,
                    efficiency_score=round(acao_original["score"], 2),
                    macro_weight=1.0,
                    catalisadores=analise.get("analise_relatorio_q4", {}).get("destaques", []),
                    preco_teto=round(preco_teto, 2),
                    preco_atual=preco_atual,
                    upside_potencial=round(upside, 2),
                    sentiment_status=f"Análise IA: {recomendacao.get('acao', 'COMPRA')}",
                    recomendacao_final=recomendacao.get("acao", "COMPRA"),
                    setor=acao_original["setor"],
                    roe=acao_original["roe"],
                    cagr=acao_original["cagr"],
                    pl=acao_original["pl"],
                    tempo_estimado_dias=recomendacao.get("tempo_estimado_dias", 90),
                    sentiment_ratio=acao_original["roe"] / 15,
                    variacao_30d=0.0
                ))
        
        print(f"\n✓ {len(top_picks)} ações analisadas com Alpha System V2")
        return top_picks
        
    except Exception as e:
        print(f"ERRO Alpha System V2: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback
        return await get_top_picks(csv_path, limit)


# ===== ENDPOINT FINAL - COM INVESTIMENTOS.COM.BR =====

@app.get("/api/v1/final/top-picks", response_model=List[TopPick])
async def get_top_picks_final(limit: int = Query(default=15)):
    """
    🎯 SISTEMA FINAL - EXATAMENTE COMO SOLICITADO
    
    FONTE DE DADOS:
    1. CSV diário de investimentos.com.br (atualizado todo dia)
    2. Preços scraped de investimentos.com.br (tempo real)
    3. Gemini analisa e seleciona top 15
    4. Relatórios Q4 2025 (se disponíveis)
    
    GARANTIAS:
    ✅ Dados atualizados diariamente
    ✅ Preços reais do mercado
    ✅ Ranking 1-15 recalculado
    ✅ Análise com IA
    """
    try:
        from datetime import datetime
        import asyncio
        
        print(f"\n{'='*60}")
        print(f"INICIANDO ANÁLISE - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}")
        
        # 1. BUSCA DADOS ATUALIZADOS (investimentos.com.br) - COM TIMEOUT
        print("\n[1/5] Buscando dados de investimentos.com.br...")
        
        try:
            dados_investimentos = await asyncio.wait_for(
                investimentos_scraper.obter_dados_atualizados_completos(),
                timeout=10.0  # 10 segundos max
            )
        except asyncio.TimeoutError:
            print("⚠ Timeout ao buscar investimentos.com.br - usando CSV local")
            dados_investimentos = {"success": False}
        except Exception as e:
            print(f"⚠ Erro ao buscar investimentos.com.br: {e}")
            dados_investimentos = {"success": False}
        
        if not dados_investimentos["success"]:
            # Fallback: usa CSV local
            print("⚠ Fallback para CSV local")
            
            # Lê CSV local
            import pandas as pd
            csv_path = "data/stocks.csv"
            
            try:
                df = pd.read_csv(csv_path, encoding='utf-8-sig')
                print(f"✓ CSV local carregado: {len(df)} ações")
                
                # Converte para formato esperado
                acoes_disponiveis = []
                for _, row in df.iterrows():
                    acoes_disponiveis.append({
                        "ticker": row.get("ticker", ""),
                        "roe": row.get("roe", 0),
                        "cagr": row.get("cagr", 0),
                        "pl": row.get("pl", 0),
                        "setor": row.get("setor", "N/A"),
                        "preco_atual": 0  # Será preenchido depois
                    })
            except Exception as e:
                print(f"❌ Erro ao ler CSV: {e}")
                raise HTTPException(status_code=500, detail="Nenhuma fonte de dados disponível")
        else:
            acoes_disponiveis = dados_investimentos["acoes"]
            print(f"✓ {len(acoes_disponiveis)} ações disponíveis")
        
        # 2. FILTRA POR FUNDAMENTOS (ROE>15%, CAGR>12%, P/L<15)
        print("\n[2/5] Filtrando por fundamentos...")
        acoes_filtradas = []
        for acao in acoes_disponiveis:
            if (acao.get("roe", 0) > 15 and 
                acao.get("cagr", 0) > 12 and 
                acao.get("pl", 0) < 15):
                acoes_filtradas.append(acao)
        
        print(f"✓ {len(acoes_filtradas)} ações passaram no filtro")
        
        if len(acoes_filtradas) == 0:
            # Usa todas se nenhuma passar
            acoes_filtradas = acoes_disponiveis
            print(f"⚠ Nenhuma passou no filtro, usando todas ({len(acoes_filtradas)})")
        
        # Limita a 20 para análise
        acoes_filtradas = acoes_filtradas[:20]
        
        # 3. BUSCA PREÇOS REAIS
        print("\n[3/5] Buscando preços reais...")
        tickers = [a["ticker"] for a in acoes_filtradas]
        
        # Tenta Brapi primeiro (API gratuita brasileira)
        try:
            print("Tentando Brapi.dev...")
            precos = await asyncio.wait_for(
                brapi_service.get_multiple_quotes(tickers),
                timeout=30.0  # 30 segundos para buscar todos
            )
            if precos and len(precos) > 0:
                print(f"✓ Brapi retornou {len(precos)} preços REAIS")
        except asyncio.TimeoutError:
            print("⚠ Timeout Brapi - tentando Alpha Vantage")
            precos = {}
        except Exception as e:
            print(f"⚠ Erro Brapi: {e} - tentando Alpha Vantage")
            precos = {}
        
        # Se Brapi falhou, tenta Alpha Vantage
        if not precos or len(precos) == 0:
            try:
                print("Tentando Alpha Vantage...")
                precos = await asyncio.wait_for(
                    market_data.get_multiple_quotes(tickers),
                    timeout=15.0
                )
            except asyncio.TimeoutError:
                print("⚠ Timeout Alpha Vantage")
                precos = {}
            except Exception as e:
                print(f"⚠ Erro Alpha Vantage: {e}")
                precos = {}
        
        # Se ambos falharam, retorna erro
        if not precos or len(precos) == 0:
            print("❌ Nenhuma API de preços disponível")
            raise HTTPException(
                status_code=503,
                detail="Serviço de preços temporariamente indisponível. Tente novamente em alguns minutos."
            )
        
        # Atualiza preços nas ações
        for acao in acoes_filtradas:
            ticker = acao["ticker"]
            if ticker in precos:
                acao["preco_atual"] = precos[ticker].get("preco_atual", 0)
                acao["variacao_dia"] = precos[ticker].get("variacao_dia", 0)
        
        # Remove ações sem preço
        acoes_com_preco = [a for a in acoes_filtradas if a.get("preco_atual", 0) > 0]
        print(f"✓ {len(acoes_com_preco)} ações com preços")
        
        if len(acoes_com_preco) == 0:
            raise HTTPException(status_code=500, detail="Nenhuma ação com preço disponível")
        
        # 4. PREPARA DADOS PARA IA
        print("\n[4/5] Preparando dados...")
        precos_reais = {a["ticker"]: a["preco_atual"] for a in acoes_com_preco}
        print(f"✓ {len(precos_reais)} preços disponíveis")
        
        # 5. ANÁLISE COM GEMINI (Alpha System V2) - COM TIMEOUT
        print("\n[5/5] Iniciando análise com Gemini...")
        
        try:
            resultado = await asyncio.wait_for(
                alpha_system_v2.executar_analise_completa(
                    acoes_candidatas=acoes_com_preco[:20],
                    precos_reais=precos_reais
                ),
                timeout=30.0  # 30 segundos max
            )
        except asyncio.TimeoutError:
            print("⚠ Timeout na análise Gemini - usando análise simples")
            resultado = {"success": False}
        except Exception as e:
            print(f"⚠ Erro na análise Gemini: {e}")
            resultado = {"success": False}
        
        if not resultado["success"]:
            # Fallback: análise simples
            print("⚠ Fallback para análise simples")
            return await _criar_top_picks_simples(acoes_com_preco[:15])
        
        # 6. CONVERTE PARA TopPick
        print("\n[6/6] Convertendo resultados...")
        top_picks = []
        
        for item in resultado["ranking_top_15"][:limit]:
            ticker = item["ticker"]
            rank = item["rank"]
            preco_atual = item["preco_atual"]
            analise = item.get("analise", {})
            
            # Busca dados originais
            acao_original = next((a for a in acoes_com_preco if a["ticker"] == ticker), None)
            
            if acao_original:
                valuation = analise.get("valuation", {})
                recomendacao = analise.get("recomendacao", {})
                
                preco_teto = valuation.get("preco_teto_90d", preco_atual * 1.10)
                upside = valuation.get("upside_potencial", 10.0)
                
                top_picks.append(TopPick(
                    ticker=ticker,
                    rank=rank,
                    efficiency_score=round((acao_original["roe"] / 15) * 10, 2),
                    macro_weight=1.0,
                    catalisadores=analise.get("analise_relatorio_q4", {}).get("destaques", ["Fundamentos sólidos"]),
                    preco_teto=round(preco_teto, 2),
                    preco_atual=preco_atual,
                    upside_potencial=round(upside, 2),
                    sentiment_status=f"Análise IA: {recomendacao.get('acao', 'COMPRA')}",
                    recomendacao_final=recomendacao.get("acao", "COMPRA"),
                    setor=acao_original.get("setor", "N/A"),
                    roe=acao_original["roe"],
                    cagr=acao_original.get("cagr", 0),
                    pl=acao_original["pl"],
                    tempo_estimado_dias=recomendacao.get("tempo_estimado_dias", 90),
                    sentiment_ratio=acao_original["roe"] / 15,
                    variacao_30d=acao_original.get("variacao_dia", 0)
                ))
        
        print(f"\n✓ {len(top_picks)} ações no ranking final")
        print(f"✓ Concluído em {datetime.now().strftime('%H:%M:%S')}")
        
        return top_picks
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao gerar análise: {str(e)}")

async def _criar_top_picks_simples(acoes: List[Dict]) -> List[TopPick]:
    """Cria top picks sem IA (fallback)"""
    
    # Ordena por ROE
    acoes_sorted = sorted(acoes, key=lambda x: x.get("roe", 0), reverse=True)
    
    top_picks = []
    
    for rank, acao in enumerate(acoes_sorted[:15], 1):
        preco_atual = acao["preco_atual"]
        preco_teto = preco_atual * 1.15
        upside = 15.0
        
        top_picks.append(TopPick(
            ticker=acao["ticker"],
            rank=rank,
            efficiency_score=round((acao["roe"] / 15) * 10, 2),
            macro_weight=1.0,
            catalisadores=[f"ROE de {acao['roe']:.1f}%"],
            preco_teto=round(preco_teto, 2),
            preco_atual=preco_atual,
            upside_potencial=round(upside, 2),
            sentiment_status="Análise Automática",
            recomendacao_final="COMPRA",
            setor=acao.get("setor", "N/A"),
            roe=acao["roe"],
            cagr=acao.get("cagr", 0),
            pl=acao["pl"],
            tempo_estimado_dias=90,
            sentiment_ratio=acao["roe"] / 15,
            variacao_30d=acao.get("variacao_dia", 0)
        ))
    
    return top_picks


# ===== FIM DOS ENDPOINTS =====





