# Guia de Implementação - Alpha Terminal

## 🎯 Visão Geral

Este guia detalha como implementar completamente o Alpha Terminal, desde o setup inicial até a automação diária.

---

## 📋 Checklist de Implementação

### Fase 1: Setup Básico ✅
- [x] Backend FastAPI estruturado
- [x] Camadas de processamento (Quant, Macro, Surgical)
- [x] Serviços (Alertas, Sentiment)
- [x] API REST com endpoints
- [x] Front-end React com TypeScript
- [x] Serviço de integração com API

### Fase 2: Integrações Essenciais 🔄
- [ ] API de preços em tempo real
- [ ] Scraping de investimentos.com.br
- [ ] Integração com Gemini API
- [ ] Download automático de relatórios de RI
- [ ] Banco de dados (PostgreSQL/MongoDB)

### Fase 3: Automação 🔄
- [ ] Cron job diário
- [ ] Pipeline de processamento
- [ ] Sistema de notificações
- [ ] Backup automático

### Fase 4: Features Avançadas 🔄
- [ ] Backtesting engine
- [ ] Dashboard de performance
- [ ] Histórico de recomendações
- [ ] Comparação com IBOV
- [ ] Sistema de alertas push

---

## 🚀 Como Começar

### 1. Setup do Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY

# Executar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Setup do Frontend

```bash
# Na raiz do projeto
npm install

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env se necessário

# Executar dev server
npm run dev
```

### 3. Testar Integração

Abra o navegador:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Docs da API: http://localhost:8000/docs

---

## 🔧 Integrações Necessárias

### 1. API de Preços (Yahoo Finance / Alpha Vantage)

```python
# backend/app/services/price_service.py
import yfinance as yf

class PriceService:
    def get_current_price(self, ticker: str) -> float:
        """Busca preço atual da ação"""
        stock = yf.Ticker(f"{ticker}.SA")  # .SA para B3
        data = stock.history(period="1d")
        return data['Close'].iloc[-1]
    
    def get_historical_prices(self, ticker: str, days: int = 30):
        """Busca histórico de preços"""
        stock = yf.Ticker(f"{ticker}.SA")
        data = stock.history(period=f"{days}d")
        return data['Close'].tolist()
```

### 2. Scraping de investimentos.com.br

```python
# backend/app/services/scraper_service.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

class InvestimentosScraper:
    def download_stocks_data(self) -> pd.DataFrame:
        """
        Baixa dados de ações de investimentos.com.br
        """
        url = "https://investimentos.com.br/ativos/"
        
        # TODO: Implementar lógica de scraping
        # Opções:
        # 1. Selenium para páginas dinâmicas
        # 2. Requests + BeautifulSoup para HTML estático
        # 3. API não documentada (inspecionar network tab)
        
        # Por enquanto, retorna dados mockados
        return pd.read_csv("data/stocks.csv")
```

### 3. Gemini API para Análise de Contexto

```python
# backend/app/services/gemini_context.py
import google.generativeai as genai

class GeminiContextAnalyzer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def analyze_global_context(self, stocks: list) -> dict:
        """
        Analisa contexto global e filtra ações
        """
        prompt = f"""
Você é um analista quantitativo especializado.

Contexto Global Atual:
- Bitcoin: Tendência de alta/baixa?
- Ouro: Refúgio seguro ativo?
- Nvidia/Tech: Boom de IA continua?
- Juros EUA: Impacto no Brasil?
- Commodities: Ciclo de alta/baixa?

Ações Candidatas:
{[s.ticker for s in stocks]}

Tarefa:
1. Analise o contexto macro global
2. Identifique quais ações têm maior probabilidade de subir
3. Considere correlações (ex: dólar alto = exportadoras bem)
4. Retorne JSON com top 15 ações rankeadas

Formato de resposta:
{{
  "contexto_global": "resumo do cenário",
  "top_picks": ["TICKER1", "TICKER2", ...],
  "justificativa": {{"TICKER1": "razão", ...}}
}}
"""
        
        response = self.model.generate_content(prompt)
        # Parse e retorna
        return response.text
```

### 4. Download Automático de Relatórios de RI

```python
# backend/app/services/ri_downloader.py
import requests
from pathlib import Path

class RIDownloader:
    def __init__(self):
        self.download_dir = Path("data/reports")
        self.download_dir.mkdir(exist_ok=True)
    
    def download_report(self, ticker: str) -> str:
        """
        Baixa relatório de RI mais recente
        
        Fontes:
        1. Site de RI da empresa
        2. CVM (Comissão de Valores Mobiliários)
        3. B3
        """
        # TODO: Implementar lógica de download
        # Exemplo para CVM:
        # https://www.rad.cvm.gov.br/ENET/frmConsultaExternaCVM.aspx
        
        pass
```

---

## 🤖 Automação Diária

### Setup do Cron Job

**Linux/Mac:**
```bash
cd backend/scripts
chmod +x setup_cron.sh
./setup_cron.sh
```

**Windows:**
```powershell
cd backend\scripts
.\setup_task_windows.ps1
```

### Fluxo de Automação

```
18:00 - Fechamento da Bolsa
  ↓
18:05 - Cron Job Inicia
  ↓
1. Download CSV de investimentos.com.br
  ↓
2. Processamento Camada 1 (Quant)
   - Filtra por ROE, CAGR, P/L
   - Calcula Efficiency Score
  ↓
3. Processamento Camada 2 (Macro)
   - Busca Selic e IPCA
   - Ajusta pesos dos setores
  ↓
4. Filtro Gemini
   - Analisa contexto global
   - Filtra top 15 ações
  ↓
5. Download de Relatórios de RI
   - Busca PDFs mais recentes
  ↓
6. Processamento Camada 3 (Surgical)
   - Analisa PDFs com Gemini
   - Extrai catalisadores
  ↓
7. Análise de Sentimento
   - Monitora redes sociais
   - Detecta risco de manada
  ↓
8. Cálculo de Estratégias
   - Define preços teto
   - Calcula upside
   - Estima tempo na carteira
  ↓
9. Salva Resultados
   - Atualiza banco de dados
   - Gera JSON para frontend
  ↓
10. Envia Notificações
    - Email digest
    - Push notifications
  ↓
18:30 - Processo Concluído
```

---

## 📊 Banco de Dados

### Schema Sugerido (PostgreSQL)

```sql
-- Tabela de ações
CREATE TABLE stocks (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(10) UNIQUE NOT NULL,
    nome VARCHAR(100),
    setor VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de dados fundamentalistas
CREATE TABLE fundamentals (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    data_referencia DATE NOT NULL,
    pl DECIMAL(10,2),
    roe DECIMAL(10,2),
    cagr DECIMAL(10,2),
    divida DECIMAL(10,2),
    preco DECIMAL(10,2),
    efficiency_score DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de recomendações
CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    data_recomendacao DATE NOT NULL,
    tipo VARCHAR(20), -- COMPRA_FORTE, COMPRA, AGUARDAR, VENDER
    preco_entrada DECIMAL(10,2),
    preco_teto DECIMAL(10,2),
    upside_potencial DECIMAL(10,2),
    tempo_estimado_dias INTEGER,
    status VARCHAR(20), -- ATIVA, REALIZADA, CANCELADA
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de alertas
CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    stock_id INTEGER REFERENCES stocks(id),
    tipo VARCHAR(50), -- OPORTUNIDADE_COMPRA, REALIZAR_LUCROS, RISCO_MANADA
    mensagem TEXT,
    lido BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela de performance
CREATE TABLE performance (
    id SERIAL PRIMARY KEY,
    recommendation_id INTEGER REFERENCES recommendations(id),
    data_fechamento DATE,
    preco_saida DECIMAL(10,2),
    retorno_percentual DECIMAL(10,2),
    dias_na_carteira INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🎨 Melhorias de Design

### Componentes a Criar

1. **StockCard.tsx** - Card de ação individual
2. **PriceGauge.tsx** - Gauge de preço teto
3. **CatalystBadge.tsx** - Badge de catalisador
4. **SentimentIndicator.tsx** - Indicador de sentimento
5. **MacroBar.tsx** - Barra de indicadores macro
6. **ThesisPanel.tsx** - Painel lateral de tese
7. **AlertCard.tsx** - Card de alerta
8. **PerformanceChart.tsx** - Gráfico de performance

### Animações

```typescript
// Exemplo de animação com Framer Motion
import { motion } from "framer-motion";

const StockCard = ({ stock }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    whileHover={{ scale: 1.02, boxShadow: "0 0 20px rgba(0,255,136,0.3)" }}
    transition={{ duration: 0.2 }}
  >
    {/* Conteúdo do card */}
  </motion.div>
);
```

---

## 🔐 Segurança

### Rate Limiting

```python
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

@app.get("/api/v1/top-picks")
@limiter.limit("10/minute")
async def get_top_picks():
    # ...
```

### Validação de Inputs

```python
from pydantic import BaseModel, validator

class StockQuery(BaseModel):
    ticker: str
    
    @validator('ticker')
    def validate_ticker(cls, v):
        if not v.isalnum() or len(v) > 10:
            raise ValueError('Ticker inválido')
        return v.upper()
```

---

## 📈 Métricas e Monitoramento

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/alpha_terminal.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Métricas

- Taxa de acerto das recomendações
- Retorno médio por ação
- Tempo médio na carteira
- Performance vs IBOV
- Uptime da API
- Tempo de resposta

---

## 🚀 Deploy

### Backend (Railway/Render/Heroku)

```bash
# Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel/Netlify)

```bash
# Build command
npm run build

# Output directory
dist
```

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs em `backend/logs/`
2. Teste os endpoints em `/docs`
3. Valide as variáveis de ambiente

---

## 🎯 Próximos Passos

1. Implementar integrações de API de preços
2. Configurar banco de dados
3. Criar sistema de notificações
4. Implementar backtesting
5. Deploy em produção
