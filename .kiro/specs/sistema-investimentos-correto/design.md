# Design Document - Sistema de Investimentos com IA

## Architecture Overview

O sistema segue uma arquitetura de 3 camadas com fluxo sequencial de prompts:

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                          │
│  - AlphaTerminal.tsx (UI)                                   │
│  - alphaApi.ts (API Client)                                 │
│  - Auto-refresh a cada 5 minutos                            │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│  - main.py (Endpoints)                                      │
│  - /api/v1/final/top-picks (endpoint principal)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              ALPHA SYSTEM V3 (Core Logic)                    │
│                                                              │
│  FLUXO SEQUENCIAL:                                          │
│  1. Prompt 1: Radar de Oportunidades                       │
│  2. Download CSV (validação < 24h)                         │
│  3. Prompt 2: Triagem Fundamentalista                      │
│  4. Download Releases (validação Q4 2025+)                 │
│  5. Prompt 3: Análise Profunda                             │
│  6. Prompt 6: Verificação Anti-Manada                      │
│  7. Busca Preços Atuais (timestamp)                        │
│  8. Retorna Ranking Final                                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  SERVIÇOS AUXILIARES                         │
│                                                              │
│  - investimentos_scraper.py (CSV diário)                   │
│  - release_downloader.py (PDFs trimestrais)                │
│  - brapi_service.py (Preços em tempo real)                 │
│  - gemini_client.py (Interface com Gemini AI)              │
└─────────────────────────────────────────────────────────────┘
```

## Component Design

### 1. Alpha System V3 (alpha_system_v3.py)

Componente principal que orquestra todo o fluxo de análise.

**Responsabilidades:**
- Executar os 6 prompts na sequência correta
- Validar freshness de todos os dados
- Coordenar serviços auxiliares
- Gerar logs detalhados com timestamps
- Retornar ranking final estruturado

**Métodos Principais:**

```python
class AlphaSystemV3:
    async def executar_analise_completa() -> Dict
        """Executa fluxo completo de 6 prompts"""
    
    async def _prompt_1_radar_oportunidades() -> Dict
        """Identifica setores quentes ANTES da manada"""
    
    async def _validar_csv_freshness(csv_path: str) -> bool
        """Valida que CSV tem < 24 horas"""
    
    async def _prompt_2_triagem_fundamentalista(csv_data, setores) -> List[str]
        """Filtra empresas com potencial de valorização"""
    
    async def _baixar_releases_recentes(tickers: List[str]) -> Dict
        """Baixa Releases Q4 2025+ de cada empresa"""
    
    async def _prompt_3_analise_profunda(releases: Dict) -> List[Dict]
        """Análise profunda com Releases"""
    
    async def _prompt_6_anti_manada(ticker: str) -> bool
        """Valida se não está comprando topo"""
    
    async def _buscar_precos_atuais(tickers: List[str]) -> Dict
        """Busca preços com timestamp"""
    
    def _gerar_log_completo() -> str
        """Gera log com todas as datas/fontes"""
```

**Fluxo de Dados:**

```
INPUT: Nenhum (sistema autônomo)
  ↓
PROMPT 1: Análise macro → setores_quentes[]
  ↓
CSV Download → validação < 24h → csv_data
  ↓
PROMPT 2: csv_data + setores_quentes → top_30_tickers[]
  ↓
Release Download → validação Q4 2025+ → releases{}
  ↓
PROMPT 3: releases + csv_data → top_15_analise[]
  ↓
PROMPT 6: Para cada ticker → aprovado/reprovado
  ↓
Preços Atuais → precos{} com timestamp
  ↓
OUTPUT: ranking_final[] com todas as informações
```

### 2. Gemini Client (gemini_client.py)

Interface unificada para comunicação com Gemini AI.

**Responsabilidades:**
- Gerenciar API key e configuração
- Executar prompts com retry logic
- Parsear respostas JSON
- Incluir data/hora em todos os prompts
- Logging de todas as chamadas

**Métodos:**

```python
class GeminiClient:
    def __init__(api_key: str)
    
    async def executar_prompt(prompt: str, context: Dict) -> Dict
        """Executa prompt e retorna JSON parseado"""
    
    def _adicionar_timestamp_prompt(prompt: str) -> str
        """Adiciona data/hora atual ao prompt"""
    
    def _parsear_resposta_json(response: str) -> Dict
        """Extrai JSON da resposta"""
    
    def _retry_on_error(func, max_retries=3)
        """Retry logic para falhas"""
```

### 3. Investimentos Scraper V2 (investimentos_scraper_v2.py)

Scraper melhorado com validação de freshness.

**Melhorias:**
- Validação rigorosa de data do CSV
- Rejeita CSV com > 24 horas
- Timestamp em todos os dados
- Fallback para múltiplas fontes
- Cache inteligente

**Métodos:**

```python
class InvestimentosScraperV2:
    async def baixar_csv_validado() -> Tuple[str, datetime]
        """Baixa CSV e retorna com timestamp"""
    
    def _validar_freshness(csv_path: str) -> bool
        """Valida que CSV tem < 24 horas"""
    
    async def _tentar_multiplas_fontes() -> str
        """Tenta múltiplas URLs"""
    
    def _adicionar_timestamp_csv(df: DataFrame) -> DataFrame
        """Adiciona coluna com timestamp"""
```

### 4. Release Downloader V2 (release_downloader_v2.py)

Downloader melhorado com validação de trimestre.

**Melhorias:**
- Validação de data do relatório (Q4 2025+)
- Extração de data do PDF
- Rejeita relatórios antigos
- Suporte para mais sites de RI
- OCR como fallback

**Métodos:**

```python
class ReleaseDownloaderV2:
    async def buscar_release_validado(ticker: str) -> Tuple[str, str, datetime]
        """Retorna: (pdf_path, trimestre, data)"""
    
    def _extrair_data_relatorio(pdf_path: str) -> datetime
        """Extrai data do relatório do PDF"""
    
    def _validar_trimestre(data: datetime) -> bool
        """Valida que é Q4 2025 ou mais recente"""
    
    async def _buscar_em_multiplos_sites(ticker: str) -> str
        """Tenta múltiplos sites de RI"""
    
    async def _ocr_fallback(pdf_path: str) -> str
        """OCR se extração falhar"""
```

### 5. Brapi Service (brapi_service.py)

Serviço de preços em tempo real (já implementado, apenas melhorias).

**Melhorias:**
- Adicionar timestamp em cada preço
- Validar que preço é de hoje
- Fallback para Alpha Vantage
- Cache de 5 minutos

## Data Models

### StockData
```python
@dataclass
class StockData:
    ticker: str
    nome: str
    setor: str
    roe: float
    cagr: float
    pl: float
    divida_ebitda: float
    margem_liquida: float
    data_csv: datetime  # NOVO: timestamp do CSV
```

### ReleaseData
```python
@dataclass
class ReleaseData:
    ticker: str
    trimestre: str  # "Q4 2025"
    data_relatorio: datetime  # NOVO: data do relatório
    pdf_path: str
    texto_completo: str
    metricas: Dict[str, Any]
```

### PriceData
```python
@dataclass
class PriceData:
    ticker: str
    preco_atual: float
    timestamp: datetime  # NOVO: hora da consulta
    fonte: str  # "brapi" ou "alphavantage"
    variacao_dia: float
```

### AnaliseCompleta
```python
@dataclass
class AnaliseCompleta:
    rank: int
    ticker: str
    nome: str
    setor: str
    
    # Preços
    preco_atual: float
    preco_entrada: float
    preco_teto: float
    upside_percent: float
    
    # Timestamps
    data_csv: datetime
    data_relatorio: datetime
    data_preco: datetime
    
    # Análise
    recomendacao: str  # "COMPRA FORTE", "COMPRA", "MONITORAR"
    confianca: str  # "ALTA", "MÉDIA", "BAIXA"
    tempo_estimado_dias: int
    
    # Detalhes
    catalisadores: List[str]
    riscos: List[str]
    analise_release: str
    anti_manada_status: str  # "APROVADO", "REPROVADO"
    
    # Fundamentos
    roe: float
    cagr: float
    pl: float
```

## Prompt Templates

### Prompt 1: Radar de Oportunidades
```python
PROMPT_1_TEMPLATE = """
Você é um analista especializado em identificar movimentos de valorização de preço antes da manada.

DATA DE HOJE: {data_hoje}
HORA ATUAL: {hora_atual}

Analise o cenário macroeconômico atual e responda:

1) Quais setores estão em fase inicial de aceleração com catalisador claro nos próximos 3-12 meses? 
   Não me traga o que já virou manchete.

2) Existe algum movimento se formando agora parecido com o que aconteceu com Nvidia, Ouro ou Bitcoin 
   antes de explodirem — algo que ainda não está no radar do investidor comum?

3) Quais países, moedas ou commodities estão sinalizando mudança de ciclo?

4) Tem alguma narrativa sendo construída no mercado institucional que o varejo ainda não percebeu?

Para cada ponto, me diga em que estágio do ciclo está — começo, meio ou fim. 
Quero entrar no começo, não comprar o topo.

Retorne JSON:
{{
  "data_analise": "{data_hoje}",
  "setores_quentes": [
    {{
      "setor": "Nome do Setor",
      "estagio_ciclo": "começo|meio|fim",
      "catalisador": "Descrição do catalisador",
      "tempo_estimado_meses": 6
    }}
  ],
  "movimentos_formando": ["Descrição"],
  "narrativas_institucionais": ["Descrição"]
}}
"""
```

### Prompt 2: Triagem Fundamentalista
```python
PROMPT_2_TEMPLATE = """
Analise a planilha de ações anexada e filtre as empresas com maior potencial de valorização de preço.

DATA DO CSV: {data_csv}
DATA DE HOJE: {data_hoje}
SETORES IDENTIFICADOS NO PROMPT 1: {setores_quentes}

IMPORTANTE: Ignore empresas cujo principal atrativo seja dividendo.

Critérios obrigatórios:
- P/L abaixo de 15
- ROE acima de 15%
- CAGR de receita acima de 12% nos últimos 3 anos
- Dívida Líquida/EBITDA abaixo de 2,5
- Margem líquida crescente ou estável nos últimos 3 trimestres

Critérios de desempate — valorize empresas com:
- Histórico de recompra de ações
- Expansão de mercado endereçável
- Setor com vento a favor no cenário atual (considere os setores identificados anteriormente)

Retorne uma tabela ranqueada do maior para o menor potencial de valorização de preço. 
Para cada empresa, adicione uma linha de 'por que ela aparece aqui' — o que nos dados chama atenção.

CSV ANEXADO:
{csv_data}

Retorne JSON:
{{
  "data_analise": "{data_hoje}",
  "data_csv_usado": "{data_csv}",
  "empresas_selecionadas": [
    {{
      "ticker": "PRIO3",
      "motivo": "ROE 25% + setor energia em alta",
      "score": 9.5
    }}
  ]
}}
"""
```

### Prompt 3: Análise Profunda
```python
PROMPT_3_TEMPLATE = """
Você vai receber relatórios administrativos, demonstrações financeiras ou qualquer documentação de múltiplas empresas.

DATA DE HOJE: {data_hoje}
DATA DOS RELATÓRIOS: {data_relatorios}

Analise cada uma individualmente e depois compare todas entre si.

Para cada empresa avalie:

1) Saúde financeira real — endividamento, geração de caixa, margem e tendência dos últimos trimestres.

2) Qualidade da gestão — o que os relatórios mostram sobre execução, alocação de capital e transparência com o acionista?

3) Catalisadores de valorização de preço — o que pode fazer essa ação subir nos próximos 6 a 18 meses? 
   Seja específico: contrato, expansão, ciclo setorial, melhora de margem.

4) Riscos reais e concretos — não os genéricos de qualquer relatório, os que realmente podem derrubar 
   o preço dessa empresa específica.

5) Preço: com base nos fundamentos, a ação está cara, justa ou barata agora? 
   IMPORTANTE: Compare com o preço ATUAL de mercado (DATA: {data_hoje}, PREÇOS: {precos_atuais}).

Após analisar todas individualmente, faça uma comparação final e me entregue um ranking das 15 melhores 
para o meu objetivo, que é: valorização de preço, não dividendos. Quero comprar bem, esperar o movimento e vender com lucro.

Me diga qual entrar primeiro, qual monitorar e qual descartar — com justificativa real para cada decisão.

RELATÓRIOS DAS EMPRESAS:
{releases_data}

Retorne JSON:
{{
  "data_analise": "{data_hoje}",
  "ranking_top_15": [
    {{
      "rank": 1,
      "ticker": "PRIO3",
      "recomendacao": "COMPRA FORTE",
      "confianca": "ALTA",
      "preco_entrada": 45.00,
      "preco_teto_90d": 52.00,
      "upside_percent": 15.5,
      "tempo_estimado_dias": 90,
      "catalisadores": ["Novo contrato", "Expansão"],
      "riscos": ["Regulação"],
      "analise_release": "Crescimento de receita...",
      "saude_financeira": "Excelente",
      "qualidade_gestao": "Alta"
    }}
  ]
}}
"""
```

### Prompt 6: Anti-Manada
```python
PROMPT_6_TEMPLATE = """
Você é um analista especializado em identificar topos de mercado e evitar comprar na euforia.

DATA DE HOJE: {data_hoje}
TICKER ANALISADO: {ticker}
PREÇO ATUAL: R$ {preco_atual}
RECOMENDAÇÃO ANTERIOR: {recomendacao}

Analise se este ativo está em um momento de:
1. COMEÇO de movimento (janela aberta para entrada)
2. MEIO de movimento (ainda dá para entrar com cautela)
3. FIM de movimento (janela fechada, manada já entrou)

Critérios para avaliar:

1) Cobertura de mídia: O ativo virou pauta comum em portais financeiros, YouTube, redes sociais?

2) Movimento de preço: Subiu muito rápido recentemente? Está em máxima histórica sem correção?

3) Fundamento vs Euforia: O movimento é sustentado por fundamentos reais ou por FOMO?

4) Posicionamento institucional: Institucionais estão comprando ou vendendo?

5) Histórico: Compare com situações similares no passado. Como terminou?

IMPORTANTE: Seja HONESTO. Se a janela fechou, diga claramente. Melhor perder uma oportunidade 
do que comprar o topo.

Retorne JSON:
{{
  "data_analise": "{data_hoje}",
  "ticker": "{ticker}",
  "status": "APROVADO|REPROVADO",
  "estagio_movimento": "COMEÇO|MEIO|FIM",
  "cobertura_midia": "BAIXA|MÉDIA|ALTA",
  "fundamento_vs_euforia": "FUNDAMENTO|MISTO|EUFORIA",
  "conclusao": "ENTRAR AGORA|ESPERAR CORREÇÃO|JANELA FECHOU",
  "justificativa": "Explicação detalhada"
}}
"""
```

## Error Handling

### Validação de Freshness
```python
class DataFreshnessError(Exception):
    """Dados muito antigos"""
    pass

def validar_freshness_csv(csv_path: str, max_hours: int = 24):
    file_time = datetime.fromtimestamp(os.path.getmtime(csv_path))
    hours_old = (datetime.now() - file_time).total_seconds() / 3600
    
    if hours_old > max_hours:
        raise DataFreshnessError(
            f"CSV muito antigo: {hours_old:.1f}h (máximo: {max_hours}h)"
        )
```

### Retry Logic
```python
async def retry_with_backoff(func, max_retries=3, backoff_seconds=2):
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(backoff_seconds * (attempt + 1))
```

### Fallbacks
```python
# CSV: investimentos.com.br → cache → stocks.csv local
# Preços: brapi → alphavantage → último conhecido
# Release: site RI → Google → análise sem Release
```

## Logging Strategy

Todos os logs devem incluir timestamp e contexto:

```python
import logging
from datetime import datetime

logger = logging.getLogger("alpha_system")

# Formato: [TIMESTAMP] [ETAPA] Mensagem
logger.info(f"[{datetime.now()}] [PROMPT_1] Iniciando análise macro")
logger.info(f"[{datetime.now()}] [CSV] Baixado: {len(df)} ações (data: {csv_date})")
logger.info(f"[{datetime.now()}] [RELEASE] {ticker}: Q4 2025 encontrado")
logger.info(f"[{datetime.now()}] [PRECOS] {ticker}: R$ {preco} (fonte: brapi)")
logger.warning(f"[{datetime.now()}] [ANTI_MANADA] {ticker}: REPROVADO - janela fechou")
```

## Performance Considerations

- CSV download: cache de 24h (evita downloads desnecessários)
- Releases: cache de 90 dias (relatórios não mudam)
- Preços: cache de 5 minutos (balance entre freshness e performance)
- Gemini calls: batch quando possível (reduz latência)
- Async/await: todas as operações I/O são assíncronas

## Security

- API keys em .env (nunca no código)
- Validação de inputs (evita injection)
- Rate limiting (respeita limites das APIs)
- Sanitização de dados scraped (evita XSS)

## Testing Strategy

- Unit tests: cada componente isolado
- Integration tests: fluxo completo end-to-end
- Mock data: para testes sem APIs reais
- Validation tests: freshness, formato JSON, etc.

---

**Próximo passo:** Implementar tasks.md com checklist detalhado
