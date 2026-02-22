# 🚀 Próximos Passos - Alpha Terminal

## ✅ O Que Já Está Pronto

### Backend (FastAPI)
- ✅ Estrutura completa com 3 camadas
- ✅ Camada 1 (Quant): Filtro por ROE, CAGR, P/L
- ✅ Camada 2 (Macro): Ajuste de pesos por setor
- ✅ Camada 3 (Surgical): Integração com Gemini API
- ✅ Sistema de Alertas
- ✅ Análise de Sentimento (Anti-Manada)
- ✅ Endpoints REST completos
- ✅ CSV de exemplo com 17 ações

### Frontend (React)
- ✅ Estrutura base com React + TypeScript
- ✅ Tailwind CSS + shadcn/ui
- ✅ Componentes alpha existentes
- ✅ Serviço de integração com API (alphaApi.ts)
- ✅ Roteamento configurado

### Documentação
- ✅ README principal (ALPHA_TERMINAL_README.md)
- ✅ Design Brief (DESIGN_BRIEF.md)
- ✅ Prompt Visual (VISUAL_DESIGN_PROMPT.md)
- ✅ Guia de Implementação (IMPLEMENTATION_GUIDE.md)
- ✅ Scripts de automação

---

## 🔄 O Que Precisa Ser Feito

### Prioridade ALTA (Essencial para MVP)

#### 1. Integração de Preços Real-Time
**Objetivo**: Substituir preços mockados por dados reais

**Opções**:
- Yahoo Finance (yfinance) - GRÁTIS
- Alpha Vantage - GRÁTIS (500 calls/dia)
- Brapi.dev - API brasileira - GRÁTIS

**Implementação**:
```python
# backend/app/services/price_service.py
import yfinance as yf

def get_price(ticker: str) -> float:
    stock = yf.Ticker(f"{ticker}.SA")
    return stock.history(period="1d")['Close'].iloc[-1]
```

**Tempo estimado**: 2-3 horas

---

#### 2. Scraping de investimentos.com.br
**Objetivo**: Baixar CSV diário automaticamente

**Opções**:
- Selenium (para páginas dinâmicas)
- Requests + BeautifulSoup (se for HTML estático)
- Inspecionar Network tab para API não documentada

**Implementação**:
```python
# backend/app/services/scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By

def download_csv():
    driver = webdriver.Chrome()
    driver.get("https://investimentos.com.br/ativos/")
    # Clicar em "Exportar CSV"
    # Salvar arquivo
    driver.quit()
```

**Tempo estimado**: 4-6 horas

---

#### 3. Configurar Gemini API
**Objetivo**: Ativar análise de PDFs e contexto global

**Passos**:
1. Obter API key: https://makersuite.google.com/app/apikey
2. Adicionar ao `.env`:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```
3. Testar análise de PDF

**Tempo estimado**: 30 minutos

---

#### 4. Atualizar Componentes do Frontend
**Objetivo**: Consumir API real ao invés de dados mockados

**Arquivos a modificar**:
- `src/pages/AlphaTerminal.tsx`
- `src/components/alpha/AlphaPick.tsx`
- `src/components/alpha/EliteTable.tsx`
- `src/components/alpha/AlertsFeed.tsx`

**Exemplo**:
```typescript
// src/pages/AlphaTerminal.tsx
import { useQuery } from '@tanstack/react-query';
import { alphaApi } from '@/services/alphaApi';

const { data: topPicks } = useQuery({
  queryKey: ['topPicks'],
  queryFn: () => alphaApi.getTopPicks(15),
  refetchInterval: 60000 // Atualiza a cada 1 minuto
});
```

**Tempo estimado**: 3-4 horas

---

### Prioridade MÉDIA (Importante mas não bloqueante)

#### 5. Banco de Dados
**Objetivo**: Persistir dados e histórico

**Opções**:
- PostgreSQL (relacional, robusto)
- MongoDB (NoSQL, flexível)
- SQLite (simples, local)

**Schema sugerido**: Ver IMPLEMENTATION_GUIDE.md

**Tempo estimado**: 6-8 horas

---

#### 6. Sistema de Notificações
**Objetivo**: Alertar usuário sobre oportunidades

**Opções**:
- Email (SendGrid, Mailgun)
- Push Notifications (Firebase Cloud Messaging)
- Telegram Bot

**Implementação**:
```python
# backend/app/services/notification_service.py
import smtplib

def send_email_alert(ticker: str, message: str):
    # Configurar SMTP
    # Enviar email
    pass
```

**Tempo estimado**: 4-6 horas

---

#### 7. Automação Diária
**Objetivo**: Rodar pipeline automaticamente às 18h

**Passos**:
1. Testar `backend/scripts/daily_update.py`
2. Configurar cron job (Linux/Mac) ou Task Scheduler (Windows)
3. Monitorar logs

**Tempo estimado**: 2-3 horas

---

### Prioridade BAIXA (Nice to have)

#### 8. Backtesting Engine
**Objetivo**: Validar estratégia com dados históricos

**Tempo estimado**: 10-15 horas

---

#### 9. Dashboard de Performance
**Objetivo**: Mostrar retorno da carteira vs IBOV

**Tempo estimado**: 8-10 horas

---

#### 10. Download Automático de PDFs de RI
**Objetivo**: Buscar relatórios automaticamente

**Fontes**:
- Site de RI da empresa
- CVM (rad.cvm.gov.br)
- B3

**Tempo estimado**: 8-12 horas

---

## 📅 Cronograma Sugerido

### Semana 1: MVP Funcional
- [ ] Dia 1-2: Integração de preços real-time
- [ ] Dia 3-4: Scraping de investimentos.com.br
- [ ] Dia 5: Configurar Gemini API
- [ ] Dia 6-7: Atualizar frontend para consumir API

**Resultado**: Sistema funcionando com dados reais

---

### Semana 2: Automação
- [ ] Dia 1-2: Configurar banco de dados
- [ ] Dia 3-4: Sistema de notificações
- [ ] Dia 5: Automação diária (cron job)
- [ ] Dia 6-7: Testes e ajustes

**Resultado**: Sistema rodando automaticamente

---

### Semana 3: Refinamento
- [ ] Dia 1-3: Melhorias de design
- [ ] Dia 4-5: Otimizações de performance
- [ ] Dia 6-7: Deploy em produção

**Resultado**: Sistema em produção

---

### Semana 4+: Features Avançadas
- [ ] Backtesting
- [ ] Dashboard de performance
- [ ] Download automático de PDFs
- [ ] Histórico de recomendações

---

## 🛠️ Como Começar AGORA

### 1. Testar o Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env

# Testar
python -m uvicorn app.main:app --reload
```

Abra: http://localhost:8000/docs

---

### 2. Testar o Frontend

```bash
# Na raiz do projeto
npm install
npm run dev
```

Abra: http://localhost:5173

---

### 3. Primeira Integração: Preços

**Instalar yfinance**:
```bash
cd backend
pip install yfinance
```

**Criar serviço**:
```python
# backend/app/services/price_service.py
import yfinance as yf

class PriceService:
    def get_current_price(self, ticker: str) -> float:
        try:
            stock = yf.Ticker(f"{ticker}.SA")
            data = stock.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return 0.0
        except Exception as e:
            print(f"Erro ao buscar preço de {ticker}: {e}")
            return 0.0
```

**Usar no main.py**:
```python
from app.services.price_service import PriceService

price_service = PriceService()

@app.get("/api/v1/top-picks")
async def get_top_picks():
    # ... código existente ...
    
    for stock in ranked_stocks[:limit]:
        # Buscar preço real
        preco_atual = price_service.get_current_price(stock.ticker)
        
        # ... resto do código ...
```

**Testar**:
```bash
curl http://localhost:8000/api/v1/top-picks
```

---

### 4. Segunda Integração: Frontend

**Atualizar AlphaTerminal.tsx**:
```typescript
import { useQuery } from '@tanstack/react-query';
import { alphaApi } from '@/services/alphaApi';

const AlphaTerminal = () => {
  const { data: topPicks, isLoading } = useQuery({
    queryKey: ['topPicks'],
    queryFn: () => alphaApi.getTopPicks(15)
  });

  if (isLoading) return <div>Carregando...</div>;

  return (
    <div>
      {topPicks?.map(stock => (
        <div key={stock.ticker}>
          {stock.ticker}: R$ {stock.preco_atual}
        </div>
      ))}
    </div>
  );
};
```

---

## 🎯 Meta Imediata

**Objetivo**: Ter o sistema funcionando com dados reais em 1 semana

**Checklist**:
- [ ] Backend rodando
- [ ] Frontend rodando
- [ ] Preços reais (yfinance)
- [ ] CSV sendo processado
- [ ] Gemini API configurada
- [ ] Frontend consumindo API
- [ ] Pelo menos 1 ação sendo exibida corretamente

---

## 💡 Dicas

### Performance
- Use cache para preços (Redis ou memória)
- Implemente rate limiting
- Otimize queries do banco

### Segurança
- Valide todos os inputs
- Use HTTPS em produção
- Proteja API keys
- Implemente CORS corretamente

### UX
- Loading states em todos os componentes
- Error boundaries
- Feedback visual para ações
- Responsividade mobile

### Monitoramento
- Logs estruturados
- Métricas de performance
- Alertas de erro
- Uptime monitoring

---

## 📞 Troubleshooting

### Backend não inicia
```bash
# Verificar dependências
pip list

# Verificar .env
cat .env

# Verificar logs
tail -f logs/alpha_terminal.log
```

### Frontend não conecta na API
```bash
# Verificar CORS no backend
# Verificar VITE_API_URL no .env
# Verificar network tab no browser
```

### Preços não carregam
```bash
# Testar yfinance manualmente
python
>>> import yfinance as yf
>>> yf.Ticker("WEGE3.SA").history(period="1d")
```

---

## 🎉 Quando Estiver Pronto

1. **Deploy Backend**: Railway, Render, ou Heroku
2. **Deploy Frontend**: Vercel ou Netlify
3. **Configurar domínio**: alphaterminal.com.br
4. **Monitoramento**: Sentry, LogRocket
5. **Analytics**: Google Analytics, Mixpanel

---

## 📚 Recursos Úteis

### APIs de Preços
- Yahoo Finance: https://pypi.org/project/yfinance/
- Brapi: https://brapi.dev/
- Alpha Vantage: https://www.alphavantage.co/

### Scraping
- Selenium: https://selenium-python.readthedocs.io/
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/

### IA
- Gemini API: https://ai.google.dev/
- OpenAI: https://platform.openai.com/

### Deploy
- Railway: https://railway.app/
- Vercel: https://vercel.com/
- Render: https://render.com/

---

🚀 **Comece pelo item 1 (Integração de Preços) e vá avançando. Boa sorte!**
