"""
Rotas Admin - Upload de CSV e gerenciamento
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Header, Depends, Body
from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime
import tempfile
import os
import json
import asyncio

from app.services.csv_manager import get_csv_manager
from app.services.auth_service import get_auth_service
from app.services.release_manager import get_release_manager

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

csv_manager = get_csv_manager()
auth_service = get_auth_service()
release_manager = get_release_manager()


class LoginRequest(BaseModel):
    password: str


def verificar_token(authorization: Optional[str] = Header(None)):
    """Dependency para verificar token de autenticação"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    # Remove "Bearer " do token
    token = authorization.replace("Bearer ", "")
    
    if not auth_service.validar_token(token):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    
    return token


@router.post("/login")
async def admin_login(request: LoginRequest):
    """
    Login do admin
    
    Args:
        request: Objeto com a senha
    
    Returns:
        Token de autenticação
    """
    resultado = auth_service.login(request.password)
    
    if not resultado:
        raise HTTPException(status_code=401, detail="Senha incorreta")
    
    return resultado


@router.post("/logout")
async def admin_logout(token: str = Depends(verificar_token)):
    """Logout do admin"""
    auth_service.logout(token)
    return {"mensagem": "Logout realizado com sucesso"}


@router.get("/csv/info")
async def obter_info_csv(token: str = Depends(verificar_token)):
    """
    Retorna informações sobre o CSV atual
    
    Requer autenticação admin
    """
    info = csv_manager.obter_info_csv_atual()
    historico = csv_manager.obter_historico_atualizacoes(limite=5)
    
    return {
        "csv_atual": info,
        "historico_recente": historico
    }


@router.post("/csv/upload")
async def upload_csv(
    file: UploadFile = File(...),
    token: str = Depends(verificar_token)
):
    """
    Upload de novo CSV
    
    Requer autenticação admin
    
    O CSV deve conter as colunas:
    - ticker (ou Ticker)
    - roe (ou ROE)
    - cagr (ou CAGR)
    - pl (ou PL)
    
    Mínimo: 50 ações
    
    AUTOMÁTICO: Se CSV mudou, refaz análise completa
    """
    # Verifica se é CSV
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos CSV são aceitos"
        )
    
    try:
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Atualiza CSV
        resultado = csv_manager.atualizar_csv(tmp_path, usuario="admin")
        
        # Remove arquivo temporário
        os.unlink(tmp_path)
        
        if not resultado["sucesso"]:
            raise HTTPException(
                status_code=400,
                detail=resultado.get("erro", "Erro ao atualizar CSV")
            )
        
        # AUTOMÁTICO: Verifica se CSV mudou e refaz análise
        asyncio.create_task(_verificar_csv_e_reanalisar())
        
        return {
            "mensagem": "CSV atualizado com sucesso",
            "detalhes": resultado,
            "auto_update": "Verificando se deve refazer análise..."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar upload: {str(e)}"
        )


async def _verificar_csv_e_reanalisar():
    """
    Verifica se CSV mudou e refaz análise completa
    """
    try:
        from app.services.sistema_automatico import get_sistema_automatico
        
        sistema = get_sistema_automatico()
        
        # Verifica se CSV mudou
        if sistema.csv_mudou():
            print("\n📝 CSV NOVO DETECTADO - Refazendo análise completa")
            await sistema.iniciar_sistema_automatico()
        else:
            print("\n✓ CSV não mudou - Mantendo análise atual")
        
    except Exception as e:
        print(f"⚠️ Erro na verificação de CSV: {e}")


@router.post("/csv/validar")
async def validar_csv(
    file: UploadFile = File(...),
    token: str = Depends(verificar_token)
):
    """
    Valida CSV sem fazer upload
    
    Útil para verificar se o CSV está correto antes de fazer upload
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos CSV são aceitos"
        )
    
    try:
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Valida CSV
        validacao = csv_manager.validar_csv(tmp_path)
        
        # Remove arquivo temporário
        os.unlink(tmp_path)
        
        return validacao
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao validar CSV: {str(e)}"
        )


@router.get("/csv/historico")
async def obter_historico(
    limite: int = 20,
    token: str = Depends(verificar_token)
):
    """
    Retorna histórico de atualizações do CSV
    """
    historico = csv_manager.obter_historico_atualizacoes(limite=limite)
    
    return {
        "total": len(historico),
        "historico": historico
    }


@router.get("/status")
async def status_admin(token: str = Depends(verificar_token)):
    """
    Status geral do sistema admin
    """
    info_csv = csv_manager.obter_info_csv_atual()
    
    return {
        "autenticado": True,
        "csv": {
            "existe": info_csv.get("existe", False),
            "total_acoes": info_csv.get("total_acoes", 0),
            "idade_horas": info_csv.get("idade_horas", 0),
            "atualizado": info_csv.get("atualizado", False)
        }
    }


@router.post("/iniciar-analise")
async def iniciar_analise(
    usar_consenso: bool = True,
    token: str = Depends(verificar_token)
):
    """
    Inicia análise completa do Alpha System V3
    
    Args:
        usar_consenso: Se True, usa consenso (5x análise macro + triagem). Padrão: True
    
    Requer autenticação admin
    
    Executa em background e retorna imediatamente
    """
    import asyncio
    from app.main import carregar_analise_inicial
    
    # Inicia análise em background
    if usar_consenso:
        # Usa análise com consenso (Groq com 6 chaves)
        async def executar_com_consenso():
            try:
                from app.services.consenso_service import get_consenso_service
                from app.services.multi_groq_client import get_multi_groq_client
                
                print(f"\n{'='*70}")
                print(f"🚀 SISTEMA DE CONSENSO - GROQ (6 CHAVES)")
                print(f"{'='*70}")
                print(f"📌 Passo 1: Análise Macro (1x) - GROQ")
                print(f"📌 Passo 2: Triagem CSV (3x consenso) - GROQ")
                print(f"📌 Rotação: 6 chaves Groq com delays inteligentes")
                print(f"📌 Retry infinito: NÃO desiste até conseguir")
                print(f"{'='*70}\n")
                
                # Usa Groq com 6 chaves e rotação inteligente
                ai_client = get_multi_groq_client()
                consenso_service = get_consenso_service(ai_client)
                
                # Passo 1: Análise Macro (1x com Groq)
                contexto_macro = await consenso_service.executar_passo1_consenso(num_execucoes=1)
                
                if not contexto_macro:
                    print("❌ Falha no Passo 1 (não deveria acontecer com retry infinito)")
                    return
                
                # DELAY entre Passo 1 e Passo 2 (aguarda chaves se recuperarem)
                print("\n⏳ Aguardando 60s para chaves Groq se recuperarem...")
                await asyncio.sleep(60)
                
                # Passo 2: Triagem CSV (3x com consenso usando Groq)
                csv_path = "data/stocks.csv"
                
                if not os.path.exists(csv_path):
                    print("❌ CSV não encontrado")
                    return
                
                empresas_aprovadas = await consenso_service.executar_passo2_consenso(
                    csv_path=csv_path,
                    contexto_macro=contexto_macro,
                    num_execucoes=3
                )
                
                if not empresas_aprovadas:
                    print("❌ Nenhuma empresa aprovada (não deveria acontecer)")
                    return
                
                # Salva empresas aprovadas
                empresas_file = "data/empresas_aprovadas.json"
                with open(empresas_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "total": len(empresas_aprovadas),
                        "empresas": empresas_aprovadas,
                        "timestamp": datetime.now().isoformat(),
                        "metodo": "consenso_groq",
                        "num_execucoes_passo1": 1,
                        "num_execucoes_passo2": 3,
                        "min_aparicoes": 2
                    }, f, indent=2, ensure_ascii=False)
                
                print(f"\n{'='*70}")
                print(f"✅ CONSENSO CONCLUÍDO")
                print(f"{'='*70}")
                print(f"📊 Total: {len(empresas_aprovadas)} empresas aprovadas")
                print(f"📄 Arquivo: {empresas_file}")
                print(f"🎯 Próximo passo: Análise com releases (Groq)")
                print(f"{'='*70}\n")
                
            except Exception as e:
                print(f"❌ Erro no consenso: {e}")
                import traceback
                traceback.print_exc()
        
        asyncio.create_task(executar_com_consenso())
        
        return {
            "mensagem": "Análise com CONSENSO iniciada (GROQ - 6 chaves)",
            "tempo_estimado": "Variável (retry infinito com rotação de chaves)",
            "detalhes": "Passo 1 (1x) + Passo 2 (3x consenso) usando Groq. Rotação entre 6 chaves."
        }
    else:
        # Análise normal (1x)
        asyncio.create_task(carregar_analise_inicial())
        
        return {
            "mensagem": "Análise iniciada com sucesso",
            "tempo_estimado": "3-5 minutos",
            "detalhes": "Sistema Híbrido (yfinance + IA) com ZERO erros de rate limit"
        }


@router.post("/analise-incremental")
async def analise_incremental(
    forcar_reanalise: bool = False,
    token: str = Depends(verificar_token)
):
    """
    Análise incremental - Analisa TODAS as empresas que têm releases
    
    Args:
        forcar_reanalise: Se True, reanalisa todas (ignora cache)
    
    Executa em background e retorna imediatamente
    """
    import asyncio
    from app.services.analise_automatica import get_analise_automatica_service
    from app.services.release_manager import get_release_manager
    
    async def executar_analise():
        try:
            # Busca TODAS as empresas que têm releases
            release_manager = get_release_manager()
            empresas_com_release = release_manager.listar_empresas_com_releases()
            
            if not empresas_com_release:
                print("❌ Nenhuma empresa com release disponível")
                return
            
            print(f"📊 Encontradas {len(empresas_com_release)} empresas com releases")
            print(f"   Empresas: {', '.join(empresas_com_release[:10])}{'...' if len(empresas_com_release) > 10 else ''}")
            
            # Executa análise incremental
            service = get_analise_automatica_service()
            resultado = await service.analisar_incrementalmente(
                empresas=empresas_com_release,
                forcar_reanalise=forcar_reanalise,
                max_paralelo=3
            )
            
            print(f"✅ Análise incremental concluída: {resultado}")
            
        except Exception as e:
            print(f"❌ Erro na análise incremental: {e}")
            import traceback
            traceback.print_exc()
    
    # Inicia em background
    asyncio.create_task(executar_analise())
    
    return {
        "mensagem": "Análise incremental iniciada",
        "tempo_estimado": "5-15 minutos (depende do número de empresas com releases)",
        "detalhes": "Analisa TODAS as empresas que têm releases. Cache inteligente."
    }


@router.get("/ranking-atual")
async def obter_ranking_atual(token: str = Depends(verificar_token)):
    """
    Retorna ranking atual ATUALIZADO e ENRIQUECIDO
    
    Lê do ranking_atual.json e enriquece com dados do CSV
    """
    return await _obter_ranking_atual_interno()


@router.get("/ranking-publico")
async def obter_ranking_publico():
    """
    Retorna ranking atual SEM autenticação (para frontend público)
    
    Mesmo conteúdo do /ranking-atual mas sem necessidade de token
    """
    return await _obter_ranking_atual_interno()


async def _obter_ranking_atual_interno():
    """
    Retorna ranking atual ATUALIZADO e ENRIQUECIDO
    
    Lê do ranking_atual.json e enriquece com dados do CSV
    """
    import json
    import os
    import pandas as pd
    
    # Lê do ranking_atual.json (mais recente)
    ranking_file = "data/cache/ranking_atual.json"
    
    if not os.path.exists(ranking_file):
        return {
            "total_aprovadas": 0,
            "ranking": [],
            "timestamp": None,
            "versao": "4.0",
            "mensagem": "Nenhum ranking disponível. Execute análise primeiro."
        }
    
    try:
        with open(ranking_file, 'r', encoding='utf-8-sig') as f:
            ranking_data = json.load(f)
        
        # Carrega CSV para enriquecer dados
        csv_path = "data/stocks.csv"
        df_csv = None
        if os.path.exists(csv_path):
            df_csv = pd.read_csv(csv_path, encoding='utf-8-sig')
            # Normaliza ticker
            df_csv['ticker'] = df_csv['ticker'].str.upper()
        
        # Enriquece cada item do ranking
        ranking_enriquecido = []
        for item in ranking_data.get("ranking", []):
            ticker = item.get("ticker", "")
            
            # Pega preço atual do ranking (já foi buscado na análise)
            preco_atual = item.get("preco_atual", 0)
            
            # Dados do CSV
            roe = 0
            pl = 0
            cagr = 0
            setor = None
            
            if df_csv is not None and ticker:
                linha = df_csv[df_csv['ticker'] == ticker]
                if not linha.empty:
                    roe = float(linha.iloc[0].get('roe', 0) or 0)
                    pl = float(linha.iloc[0].get('pl', 0) or 0)
                    cagr = float(linha.iloc[0].get('cagr', 0) or 0)
                    setor = linha.iloc[0].get('setor', None)
            
            # Se não tem no CSV, pega do item
            if roe == 0:
                roe = item.get("roe", 0)
            if pl == 0:
                pl = item.get("pl", 0)
            if cagr == 0:
                cagr = item.get("cagr", 0)
            if setor is None:
                setor = item.get("setor", None)
            
            # Monta item enriquecido
            item_enriquecido = {
                "ticker": ticker,
                "rank": item.get("rank", 0),
                "efficiency_score": item.get("score", item.get("nota", 0)),
                "macro_weight": 1.0,
                "catalisadores": item.get("catalisadores", []),
                "preco_teto": item.get("preco_teto", 0),
                "preco_atual": preco_atual,  # Preço do ranking
                "upside_potencial": item.get("upside", 0),
                "sentiment_status": "NEUTRO",
                "recomendacao_final": item.get("recomendacao", "AGUARDAR"),
                "setor": setor,
                "roe": roe,
                "cagr": cagr,
                "pl": pl,
                "tempo_estimado_dias": 30,
                "sentiment_ratio": 0.5,
                "variacao_30d": 0,
                # Adiciona dados extras para a tela de detalhes
                "preco_entrada": item.get("preco_entrada", preco_atual),
                "preco_stop": item.get("preco_stop", preco_atual * 0.95),
                "preco_alvo": item.get("preco_alvo", preco_atual * 1.05),
                "risco_retorno": item.get("risco_retorno", 1.0),
                "riscos": item.get("riscos", []),
                "resumo": item.get("resumo", "")
            }
            
            ranking_enriquecido.append(item_enriquecido)
        
        # Retorna no formato esperado pelo frontend
        return {
            "timestamp": ranking_data.get("timestamp"),
            "total_aprovadas": ranking_data.get("total", 0),
            "ranking": ranking_enriquecido,
            "versao": ranking_data.get("versao", "4.0"),
            "metadados": ranking_data.get("metadados", {})
        }
    
    except Exception as e:
        print(f"❌ Erro ao ler ranking: {e}")
        import traceback
        traceback.print_exc()
        return {
            "total_aprovadas": 0,
            "ranking": [],
            "timestamp": None,
            "versao": "4.0",
            "mensagem": f"Erro ao carregar ranking: {str(e)}"
        }


@router.get("/estatisticas-analise")
async def obter_estatisticas_analise(token: str = Depends(verificar_token)):
    """
    Retorna estatísticas do sistema de análise
    
    Inclui:
    - Total de análises em cache
    - Empresas com/sem release
    - Estatísticas de validação
    - Histórico
    """
    from app.services.analise_automatica import get_analise_automatica_service
    
    service = get_analise_automatica_service()
    stats = service.obter_estatisticas()
    
    return stats


@router.post("/scheduler/iniciar")
async def iniciar_scheduler(token: str = Depends(verificar_token)):
    """
    Inicia scheduler de análises automáticas
    
    Executa análises incrementais automaticamente a cada hora
    """
    from app.services.analise_automatica import get_scheduler
    
    scheduler = get_scheduler()
    await scheduler.iniciar()
    
    return {
        "mensagem": "Scheduler iniciado",
        "status": scheduler.obter_status()
    }


@router.post("/scheduler/parar")
async def parar_scheduler(token: str = Depends(verificar_token)):
    """Para scheduler de análises automáticas"""
    from app.services.analise_automatica import get_scheduler
    
    scheduler = get_scheduler()
    await scheduler.parar()
    
    return {
        "mensagem": "Scheduler parado",
        "status": scheduler.obter_status()
    }


@router.get("/scheduler/status")
async def status_scheduler(token: str = Depends(verificar_token)):
    """Retorna status do scheduler"""
    from app.services.analise_automatica import get_scheduler
    
    scheduler = get_scheduler()
    status = scheduler.obter_status()
    logs = scheduler.obter_logs(limite=5)
    
    return {
        "status": status,
        "ultimos_logs": logs
    }


# ===== ROTAS DE RELEASES =====

class ReleaseUploadRequest(BaseModel):
    ticker: str
    trimestre: str  # Q1, Q2, Q3, Q4
    ano: int


@router.post("/releases/upload")
async def upload_release(
    file: UploadFile = File(...),
    ticker: str = Body(...),
    trimestre: str = Body(...),
    ano: int = Body(...),
    token: str = Depends(verificar_token)
):
    """
    Upload de release de resultados (PDF)
    
    Args:
        file: Arquivo PDF do release
        ticker: Código da ação (ex: PRIO3)
        trimestre: Q1, Q2, Q3 ou Q4
        ano: Ano do release (ex: 2025)
    
    AUTOMÁTICO: Após upload, verifica se deve atualizar ranking
    """
    # Valida PDF
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são aceitos"
        )
    
    try:
        # Salva arquivo temporário
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        # Adiciona release
        resultado = release_manager.adicionar_release(
            ticker=ticker.upper(),
            file_path=tmp_path,
            trimestre=trimestre.upper(),
            ano=ano,
            usuario="admin"
        )
        
        # Remove arquivo temporário
        os.unlink(tmp_path)
        
        if not resultado["sucesso"]:
            raise HTTPException(
                status_code=400,
                detail=resultado.get("erro", "Erro ao adicionar release")
            )
        
        # AUTOMÁTICO: Verifica se deve atualizar ranking
        asyncio.create_task(_verificar_e_atualizar_ranking())
        
        return {
            "mensagem": f"Release de {ticker} {trimestre} {ano} adicionado com sucesso",
            "detalhes": resultado,
            "auto_update": "Verificando se deve atualizar ranking..."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar upload: {str(e)}"
        )


async def _verificar_e_atualizar_ranking():
    """
    Verifica se deve atualizar ranking automaticamente
    
    Atualiza se:
    - Há releases novos
    - Última atualização foi há mais de 5 minutos
    """
    try:
        from app.services.sistema_automatico import get_sistema_automatico
        
        sistema = get_sistema_automatico()
        
        # Aguarda 5 segundos (para admin fazer mais uploads se necessário)
        await asyncio.sleep(5)
        
        # Atualiza ranking
        await sistema.atualizar_ranking_automaticamente()
        
    except Exception as e:
        print(f"⚠️ Erro na atualização automática: {e}")


@router.get("/releases/pendentes")
async def obter_releases_pendentes(
    tickers: str,  # Lista separada por vírgula
    token: str = Depends(verificar_token)
):
    """
    Verifica quais empresas precisam de releases
    
    Args:
        tickers: Lista de tickers separados por vírgula (ex: PRIO3,VALE3,PETR4)
    """
    try:
        lista_tickers = [t.strip().upper() for t in tickers.split(',')]
        resultado = release_manager.verificar_releases_pendentes(lista_tickers)
        
        return resultado
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar releases: {str(e)}"
        )


@router.get("/releases/empresa/{ticker}")
async def obter_releases_empresa(
    ticker: str,
    token: str = Depends(verificar_token)
):
    """Obtém todos os releases de uma empresa"""
    try:
        releases = release_manager.obter_todos_releases(ticker.upper())
        
        return {
            "ticker": ticker.upper(),
            "total": len(releases),
            "releases": releases
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar releases: {str(e)}"
        )


@router.get("/releases/estatisticas")
async def obter_estatisticas_releases(token: str = Depends(verificar_token)):
    """Retorna estatísticas gerais dos releases"""
    try:
        stats = release_manager.obter_estatisticas()
        return stats
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter estatísticas: {str(e)}"
        )


@router.delete("/releases/{ticker}/{trimestre}/{ano}")
async def remover_release(
    ticker: str,
    trimestre: str,
    ano: int,
    token: str = Depends(verificar_token)
):
    """Remove um release específico"""
    try:
        resultado = release_manager.remover_release(
            ticker.upper(),
            trimestre.upper(),
            ano
        )
        
        if not resultado["sucesso"]:
            raise HTTPException(
                status_code=404,
                detail=resultado.get("erro", "Release não encontrado")
            )
        
        return {
            "mensagem": f"Release de {ticker} {trimestre} {ano} removido com sucesso"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao remover release: {str(e)}"
        )


@router.get("/releases/listar")
async def listar_todas_empresas_com_releases(token: str = Depends(verificar_token)):
    """Lista todas as empresas que têm releases"""
    try:
        empresas = release_manager.listar_empresas_com_releases()
        
        # Pega release mais recente de cada empresa
        detalhes = []
        for ticker in empresas:
            release = release_manager.obter_release_mais_recente(ticker)
            if release:
                detalhes.append({
                    "ticker": ticker,
                    "release_mais_recente": {
                        "trimestre": release['trimestre'],
                        "ano": release['ano'],
                        "data_upload": release['data_upload']
                    }
                })
        
        return {
            "total": len(empresas),
            "empresas": detalhes
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao listar empresas: {str(e)}"
        )


@router.get("/empresas-aprovadas")
async def obter_empresas_aprovadas(token: str = Depends(verificar_token)):
    """
    Retorna empresas aprovadas ATUALIZADAS do ranking atual
    
    Lê do ranking_atual.json (dados mais recentes)
    Fallback para empresas_aprovadas.json se não existir
    """
    import json
    import os
    from datetime import datetime
    import math
    
    # PRIORIDADE 1: Ranking atual (mais recente)
    ranking_file = "data/cache/ranking_atual.json"
    if os.path.exists(ranking_file):
        try:
            with open(ranking_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            # Extrai tickers do ranking
            empresas = [item['ticker'] for item in data.get('ranking', [])]
            timestamp_str = data.get('timestamp')
            
            if empresas:
                # Calcula idade
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                        idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
                        if not math.isfinite(idade_horas):
                            idade_horas = 0
                    except:
                        idade_horas = 0
                else:
                    idade_horas = 0
                
                idade_horas = max(0, round(idade_horas, 1))
                
                return {
                    "total": len(empresas),
                    "empresas": empresas,
                    "timestamp": timestamp_str,
                    "idade_horas": idade_horas,
                    "fonte": "ranking_atual",
                    "mensagem": f"Dados do ranking atual ({idade_horas:.1f}h atrás)" if idade_horas > 1 else "Dados atualizados"
                }
        except Exception as e:
            print(f"⚠️ Erro ao ler ranking_atual: {e}")
    
    # FALLBACK: empresas_aprovadas.json (antigo)
    empresas_file = "data/empresas_aprovadas.json"
    if not os.path.exists(empresas_file):
        return {
            "total": 0,
            "empresas": [],
            "fonte": "nenhuma",
            "mensagem": "Nenhuma análise executada ainda. Execute 'Iniciar Análise' primeiro.",
            "timestamp": None,
            "idade_horas": 0
        }
    
    try:
        with open(empresas_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Calcula idade dos dados
        timestamp_str = data.get("timestamp")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
                
                if not math.isfinite(idade_horas):
                    idade_horas = 0
            except:
                idade_horas = 0
        else:
            idade_horas = 0
        
        idade_horas = max(0, round(idade_horas, 1))
        
        return {
            "total": data.get("total", 0),
            "empresas": data.get("empresas", []),
            "timestamp": timestamp_str,
            "idade_horas": idade_horas,
            "fonte": "empresas_aprovadas_antigo",
            "detalhes": data.get("detalhes", []),
            "mensagem": f"⚠️ Dados antigos ({idade_horas:.1f}h atrás). Execute nova análise."
        }
    
    except Exception as e:
        return {
            "total": 0,
            "empresas": [],
            "fonte": "erro",
            "mensagem": f"Erro ao ler empresas: {str(e)}",
            "timestamp": None,
            "idade_horas": 0
        }


@router.get("/releases-pendentes")
async def obter_releases_pendentes(token: str = Depends(verificar_token)):
    """
    Retorna lista de empresas aguardando releases
    
    Lê do arquivo data/releases_pendentes/lista_pendentes.json
    """
    import json
    import os
    from datetime import datetime
    import math
    
    pendentes_file = "data/releases_pendentes/lista_pendentes.json"
    
    # Se não existe, retorna vazio
    if not os.path.exists(pendentes_file):
        return {
            "total": 0,
            "empresas": [],
            "timestamp": None,
            "idade_horas": 0,
            "mensagem": "Nenhuma empresa pendente"
        }
    
    try:
        with open(pendentes_file, 'r', encoding='utf-8-sig') as f:
            data = json.load(f)
        
        # Calcula idade dos dados
        timestamp_str = data.get("timestamp")
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
                idade_horas = (datetime.now() - timestamp).total_seconds() / 3600
                
                if not math.isfinite(idade_horas):
                    idade_horas = 0
            except:
                idade_horas = 0
        else:
            idade_horas = 0
        
        idade_horas = max(0, round(idade_horas, 1))
        
        return {
            "total": data.get("total", 0),
            "empresas": data.get("empresas", []),
            "timestamp": timestamp_str,
            "idade_horas": idade_horas,
            "instrucoes": data.get("instrucoes", ""),
            "mensagem": f"Lista atualizada há {idade_horas:.1f}h"
        }
    
    except Exception as e:
        return {
            "total": 0,
            "empresas": [],
            "timestamp": None,
            "idade_horas": 0,
            "mensagem": f"Erro ao ler pendentes: {str(e)}"
        }



# ===== ROTAS DE CONSENSO (NOVAS MELHORIAS) =====

@router.post("/analise-consenso")
async def analise_com_consenso(
    num_execucoes: int = 5,
    min_aparicoes: int = 3,
    token: str = Depends(verificar_token)
):
    """
    Análise completa com CONSENSO (Passo 1 + Passo 2)
    
    Executa múltiplas vezes e consolida resultados:
    - Passo 1 (Macro): 5x → Consolida setores
    - Passo 2 (Triagem): 5x → Empresas que aparecem 3+ vezes
    
    Args:
        num_execucoes: Quantas vezes executar (padrão: 5)
        min_aparicoes: Mínimo de aparições para aprovar (padrão: 3)
    
    Executa em background
    """
    async def executar_consenso():
        try:
            from app.services.consenso_service import get_consenso_service
            from app.services.multi_groq_client import get_multi_groq_client
            
            ai_client = get_multi_groq_client()
            consenso_service = get_consenso_service(ai_client)
            
            # Passo 1: Análise Macro com consenso
            print("\n🔄 Executando Passo 1 com consenso...")
            contexto_macro = await consenso_service.executar_passo1_consenso(
                num_execucoes=num_execucoes,
                min_aparicoes=min_aparicoes
            )
            
            if not contexto_macro:
                print("❌ Falha no Passo 1")
                return
            
            # Passo 2: Triagem CSV com consenso
            print("\n🔄 Executando Passo 2 com consenso...")
            csv_path = "data/stocks.csv"
            
            if not os.path.exists(csv_path):
                print("❌ CSV não encontrado")
                return
            
            empresas_aprovadas = await consenso_service.executar_passo2_consenso(
                csv_path=csv_path,
                contexto_macro=contexto_macro,
                num_execucoes=num_execucoes,
                min_aparicoes=min_aparicoes
            )
            
            if not empresas_aprovadas:
                print("❌ Nenhuma empresa aprovada")
                return
            
            # Salva empresas aprovadas
            empresas_file = "data/empresas_aprovadas.json"
            with open(empresas_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "total": len(empresas_aprovadas),
                    "empresas": empresas_aprovadas,
                    "timestamp": datetime.now().isoformat(),
                    "metodo": "consenso",
                    "num_execucoes": num_execucoes,
                    "min_aparicoes": min_aparicoes
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n✅ Análise com consenso concluída: {len(empresas_aprovadas)} empresas")
            
        except Exception as e:
            print(f"❌ Erro na análise com consenso: {e}")
            import traceback
            traceback.print_exc()
    
    # Inicia em background
    asyncio.create_task(executar_consenso())
    
    return {
        "mensagem": "Análise com consenso iniciada",
        "tempo_estimado": "5-10 minutos",
        "detalhes": f"Executando {num_execucoes}x cada passo. Empresas precisam aparecer {min_aparicoes}+ vezes."
    }


@router.get("/precos-cache/stats")
async def obter_stats_cache_precos(token: str = Depends(verificar_token)):
    """
    Retorna estatísticas do cache de preços
    
    Mostra:
    - Total de preços em cache
    - Atualizados (< 30min) 🟢
    - Recentes (30min-2h) 🟡
    - Antigos (> 2h) 🔴
    """
    from app.services.precos_cache_service import get_precos_cache_service
    
    cache_service = get_precos_cache_service()
    stats = cache_service.obter_estatisticas()
    
    return {
        "cache_precos": stats,
        "legenda": {
            "atualizados": "< 30 minutos (🟢)",
            "recentes": "30min - 2h (🟡)",
            "antigos": "> 2 horas (🔴)"
        }
    }


@router.post("/precos-cache/limpar")
async def limpar_cache_precos(
    max_dias: int = 7,
    token: str = Depends(verificar_token)
):
    """
    Remove preços antigos do cache
    
    Args:
        max_dias: Remove preços com mais de X dias (padrão: 7)
    """
    from app.services.precos_cache_service import get_precos_cache_service
    
    cache_service = get_precos_cache_service()
    cache_service.limpar_cache_antigo(max_dias=max_dias)
    
    stats = cache_service.obter_estatisticas()
    
    return {
        "mensagem": f"Cache limpo (preços > {max_dias} dias removidos)",
        "cache_atual": stats
    }


@router.get("/notas-estruturadas/calcular/{ticker}")
async def calcular_nota_estruturada(
    ticker: str,
    token: str = Depends(verificar_token)
):
    """
    Calcula nota estruturada para uma empresa
    
    Baseado em critérios objetivos:
    - Fundamentos (30%)
    - Catalisadores (30%)
    - Valuation (20%)
    - Gestão (20%)
    """
    from app.services.notas_estruturadas_service import get_notas_estruturadas_service
    import pandas as pd
    
    # Busca dados do CSV
    csv_path = "data/stocks.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV não encontrado")
    
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    linha = df[df['ticker'].str.upper() == ticker.upper()]
    
    if linha.empty:
        raise HTTPException(status_code=404, detail=f"Empresa {ticker} não encontrada no CSV")
    
    dados = linha.iloc[0].to_dict()
    
    # Calcula nota
    notas_service = get_notas_estruturadas_service()
    nota, detalhes = notas_service.calcular_nota(
        dados_csv={
            "ticker": ticker,
            "roe": dados.get("roe", 0),
            "pl": dados.get("pl", 0),
            "cagr": dados.get("cagr", 0)
        },
        preco_atual=0,  # Não usado no cálculo
        tem_release=False,  # Simplificado
        setor_quente=False  # Simplificado
    )
    
    return {
        "ticker": ticker.upper(),
        "nota_calculada": nota,
        "detalhamento": detalhes,
        "dados_usados": {
            "roe": dados.get("roe", 0),
            "pl": dados.get("pl", 0),
            "cagr": dados.get("cagr", 0)
        }
    }



# ===== ROTAS DE ESTRATÉGIA DINÂMICA (NOVAS) =====

@router.post("/estrategia/atualizar")
async def atualizar_estrategias_manual(token: str = Depends(verificar_token)):
    """
    Atualiza estratégias manualmente (sem aguardar scheduler)
    
    Recalcula entrada/stop/alvo com preços atuais
    Gera alertas automáticos
    """
    async def executar():
        try:
            from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
            from app.services.precos_service import get_precos_service
            
            estrategia_service = get_estrategia_dinamica_service()
            precos_service = get_precos_service()
            
            # Carrega empresas
            empresas_file = "data/empresas_aprovadas.json"
            if not os.path.exists(empresas_file):
                print("❌ Nenhuma empresa aprovada")
                return
            
            with open(empresas_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
            
            empresas = data.get('empresas', [])
            
            # Atualiza
            resultado = await estrategia_service.atualizar_estrategias(
                empresas=empresas,
                precos_service=precos_service
            )
            
            print(f"✅ Atualização manual concluída: {resultado}")
        
        except Exception as e:
            print(f"❌ Erro: {e}")
            import traceback
            traceback.print_exc()
    
    # Executa em background
    asyncio.create_task(executar())
    
    return {
        "mensagem": "Atualização de estratégias iniciada",
        "tempo_estimado": "30-60 segundos"
    }


@router.get("/estrategia/alertas")
async def obter_alertas_estrategia(
    limite: int = 50,
    token: str = Depends(verificar_token)
):
    """
    Retorna alertas recentes
    
    Tipos de alertas:
    - OPORTUNIDADE: Preço atingiu entrada
    - STOP: Stop loss atingido
    - ALVO: Alvo atingido
    - AGUARDAR: Aguardar correção
    """
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    
    estrategia_service = get_estrategia_dinamica_service()
    alertas = estrategia_service.obter_alertas(limite=limite)
    
    return {
        "total": len(alertas),
        "alertas": alertas
    }


@router.get("/estrategia/historico/{ticker}")
async def obter_historico_estrategia(
    ticker: str,
    limite: int = 100,
    token: str = Depends(verificar_token)
):
    """
    Retorna histórico de estratégia de uma empresa
    
    Mostra evolução de:
    - Preço
    - Entrada
    - Stop
    - Alvo
    - R/R
    - Status
    """
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    
    estrategia_service = get_estrategia_dinamica_service()
    historico = estrategia_service.obter_historico_empresa(ticker.upper(), limite=limite)
    
    return {
        "ticker": ticker.upper(),
        "total": len(historico),
        "historico": historico
    }


@router.get("/estrategia/status")
async def obter_status_estrategia(token: str = Depends(verificar_token)):
    """Retorna status do serviço de estratégia dinâmica"""
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    
    estrategia_service = get_estrategia_dinamica_service()
    status = estrategia_service.obter_status()
    
    return status


@router.post("/estrategia-scheduler/iniciar")
async def iniciar_scheduler_estrategia(token: str = Depends(verificar_token)):
    """
    Inicia scheduler de estratégia dinâmica
    
    Executa atualização automática a cada 1h
    """
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    from app.services.estrategia_scheduler import get_estrategia_scheduler
    from app.services.precos_service import get_precos_service
    
    estrategia_service = get_estrategia_dinamica_service()
    precos_service = get_precos_service()
    scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
    
    await scheduler.iniciar()
    
    return {
        "mensagem": "Scheduler de estratégia iniciado",
        "status": scheduler.obter_status()
    }


@router.post("/estrategia-scheduler/parar")
async def parar_scheduler_estrategia(token: str = Depends(verificar_token)):
    """Para scheduler de estratégia dinâmica"""
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    from app.services.estrategia_scheduler import get_estrategia_scheduler
    from app.services.precos_service import get_precos_service
    
    estrategia_service = get_estrategia_dinamica_service()
    precos_service = get_precos_service()
    scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
    
    await scheduler.parar()
    
    return {
        "mensagem": "Scheduler de estratégia parado",
        "status": scheduler.obter_status()
    }


@router.get("/estrategia-scheduler/status")
async def status_scheduler_estrategia(token: str = Depends(verificar_token)):
    """Retorna status do scheduler"""
    from app.services.estrategia_dinamica_service import get_estrategia_dinamica_service
    from app.services.estrategia_scheduler import get_estrategia_scheduler
    from app.services.precos_service import get_precos_service
    
    estrategia_service = get_estrategia_dinamica_service()
    precos_service = get_precos_service()
    scheduler = get_estrategia_scheduler(estrategia_service, precos_service)
    
    status = scheduler.obter_status()
    logs = scheduler.obter_logs(limite=10)
    
    return {
        "status": status,
        "ultimos_logs": logs
    }


# ===== ROTAS DE CONFIGURAÇÃO (NOVAS) =====

@router.get("/config")
async def obter_configuracoes(token: str = Depends(verificar_token)):
    """
    Retorna todas as configurações do sistema
    
    Returns:
        Dicionário com todas as configurações
    """
    from app.services.config_service import get_config_service
    
    config_service = get_config_service()
    config = config_service.obter_todas()
    
    return {
        "success": True,
        "config": config
    }


@router.get("/config/{secao}")
async def obter_secao_config(
    secao: str,
    token: str = Depends(verificar_token)
):
    """
    Retorna configurações de uma seção específica
    
    Args:
        secao: Nome da seção (scheduler_estrategia, analise, cache_precos, etc)
    
    Returns:
        Configurações da seção
    """
    from app.services.config_service import get_config_service
    
    config_service = get_config_service()
    config_secao = config_service.obter_secao(secao)
    
    if not config_secao:
        raise HTTPException(status_code=404, detail=f"Seção '{secao}' não encontrada")
    
    return {
        "success": True,
        "secao": secao,
        "config": config_secao
    }


class ConfigUpdateRequest(BaseModel):
    chave: str
    valor: Any


@router.put("/config")
async def atualizar_configuracao(
    request: ConfigUpdateRequest,
    token: str = Depends(verificar_token)
):
    """
    Atualiza uma configuração específica
    
    Args:
        chave: Chave no formato "secao.campo" (ex: "scheduler_estrategia.intervalo_minutos")
        valor: Novo valor
    
    Returns:
        Confirmação da atualização
    """
    from app.services.config_service import get_config_service
    
    config_service = get_config_service()
    config_service.definir(request.chave, request.valor)
    
    return {
        "success": True,
        "mensagem": f"Configuração '{request.chave}' atualizada",
        "novo_valor": request.valor
    }


class ConfigSecaoUpdateRequest(BaseModel):
    valores: dict


@router.put("/config/{secao}")
async def atualizar_secao_config(
    secao: str,
    request: ConfigSecaoUpdateRequest,
    token: str = Depends(verificar_token)
):
    """
    Atualiza seção completa de configuração
    
    Args:
        secao: Nome da seção
        valores: Novos valores para a seção
    
    Returns:
        Confirmação da atualização
    """
    from app.services.config_service import get_config_service
    
    config_service = get_config_service()
    config_service.atualizar_secao(secao, request.valores)
    
    return {
        "success": True,
        "mensagem": f"Seção '{secao}' atualizada",
        "valores": request.valores
    }


@router.post("/config/resetar")
async def resetar_configuracoes(token: str = Depends(verificar_token)):
    """
    Reseta todas as configurações para valores padrão
    
    Returns:
        Confirmação do reset
    """
    from app.services.config_service import get_config_service
    
    config_service = get_config_service()
    config_service.resetar()
    
    return {
        "success": True,
        "mensagem": "Configurações resetadas para padrão",
        "config": config_service.obter_todas()
    }


# ===== ROTAS DE ANÁLISE COM RELEASES (NOVO SISTEMA) =====

@router.post("/analise-com-releases/executar")
async def executar_analise_com_releases(
    forcar_reanalise: bool = True,  # SEMPRE força reanálise por padrão
    token: str = Depends(verificar_token)
):
    """
    Executa análise completa de TODAS as empresas COM releases
    
    IMPORTANTE: Por padrão, SEMPRE reanalisa todas as empresas (forcar_reanalise=True)
    para garantir que o ranking seja recalculado com notas atualizadas.
    
    Fluxo:
    1. Pega TODAS as empresas com releases
    2. Para cada empresa (SEQUENCIAL):
       - Busca preço atual + dados fundamentalistas (Brapi)
       - Lê release (PDF)
       - Envia para IA: release + preço + dados fundamentalistas completos
       - IA retorna: nota focada em VALORIZAÇÃO 5% ao mês
       - Calcula estratégia (entrada/stop/alvo)
    3. Ordena ranking por nota (maior primeiro)
    4. Salva ranking_atual.json
    
    Args:
        forcar_reanalise: Se True (padrão), reanalisa TODAS as empresas ignorando cache
    
    Executa em background
    """
    async def executar():
        try:
            from app.services.analise_com_release_service import get_analise_com_release_service
            
            print(f"\n{'='*70}")
            print(f"🔄 ANÁLISE COMPLETA COM RELEASES")
            print(f"{'='*70}")
            print(f"⚡ Forçar reanálise: {'SIM' if forcar_reanalise else 'NÃO'}")
            print(f"📊 Todas as empresas com releases serão analisadas")
            print(f"🎯 Foco: Valorização de 5% ao mês")
            print(f"{'='*70}\n")
            
            analise_service = get_analise_com_release_service()
            
            resultado = await analise_service.analisar_todas_com_releases(
                forcar_reanalise=forcar_reanalise
            )
            
            if resultado.get('sucesso'):
                print(f"\n{'='*70}")
                print(f"✅ ANÁLISE CONCLUÍDA COM SUCESSO")
                print(f"{'='*70}")
                print(f"📊 Empresas analisadas: {resultado.get('total_analisadas')}")
                print(f"❌ Erros: {resultado.get('total_erros', 0)}")
                print(f"🏆 Ranking atualizado: {resultado.get('ranking_file')}")
                print(f"{'='*70}\n")
            else:
                print(f"\n❌ Falha na análise: {resultado.get('mensagem')}")
            
        except Exception as e:
            print(f"\n❌ Erro na análise com releases: {e}")
            import traceback
            traceback.print_exc()
    
    # Executa em background
    asyncio.create_task(executar())
    
    return {
        "mensagem": "Análise completa com releases iniciada",
        "tempo_estimado": "10-20 minutos (depende do número de empresas)",
        "detalhes": "Analisa apenas empresas COM releases. Uma por vez (sequencial)."
    }


@router.post("/analise-scheduler/iniciar")
async def iniciar_analise_scheduler(token: str = Depends(verificar_token)):
    """
    Inicia scheduler de análises automáticas
    
    Funcionalidades:
    - Análise completa diária (todo dia às 8h)
    - Atualização de preços/estratégias a cada 1h
    """
    from app.services.analise_scheduler import get_analise_scheduler
    
    scheduler = get_analise_scheduler()
    await scheduler.iniciar()
    
    return {
        "mensagem": "Scheduler de análises iniciado",
        "status": scheduler.obter_status()
    }


@router.post("/analise-scheduler/parar")
async def parar_analise_scheduler(token: str = Depends(verificar_token)):
    """Para scheduler de análises automáticas"""
    from app.services.analise_scheduler import get_analise_scheduler
    
    scheduler = get_analise_scheduler()
    await scheduler.parar()
    
    return {
        "mensagem": "Scheduler de análises parado",
        "status": scheduler.obter_status()
    }


@router.get("/analise-scheduler/status")
async def status_analise_scheduler(token: str = Depends(verificar_token)):
    """Retorna status do scheduler de análises"""
    from app.services.analise_scheduler import get_analise_scheduler
    
    scheduler = get_analise_scheduler()
    status = scheduler.obter_status()
    logs = scheduler.obter_logs(limite=10)
    
    return {
        "status": status,
        "ultimos_logs": logs
    }


@router.post("/analise-scheduler/executar-agora")
async def executar_analise_agora(
    tipo: str = "completa",
    token: str = Depends(verificar_token)
):
    """
    Executa análise manualmente (sem aguardar scheduler)
    
    Args:
        tipo: "completa" (reanalisa tudo) ou "atualizacao" (só atualiza preços)
    """
    async def executar():
        try:
            from app.services.analise_scheduler import get_analise_scheduler
            
            scheduler = get_analise_scheduler()
            await scheduler.executar_agora(tipo=tipo)
            
            print(f"✅ Análise manual concluída ({tipo})")
            
        except Exception as e:
            print(f"❌ Erro na análise manual: {e}")
            import traceback
            traceback.print_exc()
    
    # Executa em background
    asyncio.create_task(executar())
    
    return {
        "mensagem": f"Análise manual iniciada ({tipo})",
        "tempo_estimado": "5-15 minutos" if tipo == "completa" else "1-3 minutos"
    }
