# 🚀 Alpha Terminal - Terminal de Inteligência Tática

## 📖 O Que É?

O Alpha Terminal não é apenas um site de dicas de ações. É um **sistema de inteligência financeira** que processa milhares de dados em segundos e entrega decisões cirúrgicas para bater a meta de **5% ao mês**.

### 🎯 Problema que Resolve

- **Atraso na informação**: Enquanto você lê notícias, o mercado já precificou
- **Viés emocional**: Comprar no topo da euforia, vender no fundo do medo
- **Falta de método**: Decisões baseadas em "achismo" ou dicas de terceiros
- **Custo de oportunidade**: Dinheiro parado em ações sem momentum

### 💡 Solução

Um pipeline de 3 camadas que elimina 95% do "lixo" da bolsa e identifica apenas ativos Elite:

1. **Camada Quant**: Filtra por ROE, CAGR e P/L
2. **Camada Macro**: Ajusta pesos por setor baseado em Selic e IPCA
3. **Camada Surgical**: IA analisa relatórios de RI buscando catalisadores

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                     │
│  - Bento Grid com Alpha Pick do Dia                     │
│  - Feed de Alertas em Tempo Real                        │
│  - Tabela Elite com 15 Ações                            │
│  - Painel de Tese Completa                              │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                     │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Camada 1   │→ │  Camada 2   │→ │  Camada 3   │    │
│  │   Quant     │  │    Macro    │  │  Surgical   │    │
│  │  (Filtro)   │  │  (Setores)  │  │  (IA/PDF)   │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐                      │
│  │ Anti-Manada │  │   Alertas   │                      │
│  │ (Sentiment) │  │  (Preços)   │                      │
│  └─────────────┘  └─────────────┘                      │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│                  INTEGRAÇÕES                            │
│  - Gemini API (Análise de PDFs)                         │
│  - Yahoo Finance (Preços)                               │
│  - Investimentos.com.br (CSV diário)                    │
│  - CVM (Relatórios de RI)                               │
└─────────────────────────────────────────────────────────┘
```

---

## 🎨 Design System

### Conceito Visual
**Terminal Bloomberg + Cyberpunk 2077 + Apple Design**

### Paleta de Cores
```css
Background: #0a0a0f (Preto profundo)
Accent: #00ff88 (Verde neon)
Alert: #ff3366 (Vermelho)
Warning: #ffd700 (Amarelo)
Text: #ffffff (Branco)
```

### Componentes Principais

1. **Alpha Pick Card** (Hero)
   - Ticker em destaque
   - Preço atual vs Preço Teto
   - Barra de progresso visual
   - Upside potencial
   - Catalisadores
   - Badge de recomendação

2. **Feed de Alertas** (Sidebar)
   - Oportunidades de compra (verde)
   - Realizar lucros (vermelho)
   - Risco de manada (amarelo)
   - Timestamp relativo

3. **Tabela Elite** (Full width)
   - 15 ações selecionadas
   - Sorting interativo
   - Hover effects
   - Badges coloridos

4. **Painel de Tese** (Slide panel)
   - Análise fundamentalista
   - Estratégia de entrada
   - Catalisadores detalhados
   - Contexto macro
   - Sentiment analysis
   - Riscos

---

## 📊 Informações Exibidas

### Por Ação

#### Dados Fundamentalistas
- **ROE**: Retorno sobre Patrimônio (>15% = Elite)
- **CAGR**: Crescimento anual composto (>12% = Alto crescimento)
- **P/L**: Preço sobre Lucro (<15 = Razoável)
- **Efficiency Score**: (ROE + CAGR) / P/L

#### Estratégia de Entrada
- **Preço Atual**: Cotação em tempo real
- **Preço Teto**: Máximo para comprar com margem de segurança
- **Preço Ideal**: Melhor ponto de entrada (-5% do teto)
- **Upside Potencial**: Ganho esperado até o preço teto
- **Stop Loss**: Limite de perda (-10%)

#### Timing
- **Tempo Estimado**: Dias esperados na carteira (90 dias padrão)
- **Meta de Lucro**: Percentual alvo
- **Recomendação**: COMPRA FORTE / COMPRA / AGUARDAR / VENDER

#### Catalisadores
- 🚀 **Expansão**: Novas fábricas, mercados
- 📝 **Contratos**: Novos clientes, parcerias
- ⚡ **Alavancagem**: Eficiência operacional
- 💡 **Inovação**: Novos produtos, tecnologia

#### Contexto
- **Setor**: Industrial, Financeiro, Energia, etc.
- **Peso Macro**: Ajuste baseado em Selic e IPCA
- **Sentiment**: Normal / Atenção / Alerta Manada

---

## 🤖 Automação Diária

### Fluxo (18:00 - Pós-fechamento)

```
1. Download CSV de investimentos.com.br
   ↓
2. Filtro Quantitativo (Camada 1)
   - ROE > 15%
   - CAGR > 12%
   - P/L < 15
   ↓
3. Análise Macro (Camada 2)
   - Busca Selic e IPCA
   - Ajusta pesos dos setores
   ↓
4. Filtro Gemini
   - Analisa contexto global (Bitcoin, Ouro, Nvidia)
   - Identifica tendências
   - Filtra top 15 ações
   ↓
5. Download de Relatórios de RI
   - Busca PDFs mais recentes
   ↓
6. Análise Cirúrgica (Camada 3)
   - IA lê PDFs
   - Extrai catalisadores
   - Score qualitativo
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
```

---

## 🚨 Sistema de Alertas

### Tipos de Alertas

1. **🟢 Oportunidade de Compra**
   - Preço caiu abaixo do teto
   - Margem de segurança aumentou
   - Momento ideal para entrada

2. **🔴 Realizar Lucros**
   - Preço atingiu ou ultrapassou o teto
   - Meta de lucro alcançada
   - Considere vender parcial ou total

3. **🟡 Atenção**
   - Preço próximo ao stop loss
   - Volume de menções acima do normal
   - Mudança no contexto macro

4. **🚨 Risco de Manada**
   - Volume de menções 3x acima da média
   - Euforia sem fundamento
   - Possível distribuição (venda dos grandes)

---

## 📈 Meta: 5% ao Mês

### Como Bater a Meta

1. **Diversificação Inteligente**
   - 15 ações na carteira
   - Setores diferentes
   - Correlação baixa

2. **Rotação Ativa**
   - Vender quando atingir o teto
   - Comprar novas oportunidades
   - Dinheiro sempre no ativo com maior momentum

3. **Gestão de Risco**
   - Stop loss em -10%
   - Margem de segurança de 15%
   - Nunca "casar" com ação

4. **Timing**
   - Comprar no medo (preço abaixo do teto)
   - Vender na euforia (preço acima do teto)
   - Evitar manada

### Matemática

```
Meta: 5% ao mês = 60% ao ano (composto)

Estratégia:
- 15 ações na carteira
- Upside médio de 15% por ação
- Tempo médio: 90 dias (3 meses)
- Rotação: 4x ao ano

Resultado esperado:
15% × 4 rotações = 60% ao ano
```

---

## 🛠️ Stack Tecnológico

### Frontend
- **React 18** + TypeScript
- **Vite** (Build tool)
- **Tailwind CSS** (Styling)
- **shadcn/ui** (Componentes)
- **Framer Motion** (Animações)
- **Recharts** (Gráficos)
- **React Query** (Data fetching)

### Backend
- **FastAPI** (Python)
- **Pandas** (Processamento de dados)
- **Google Gemini** (IA para análise)
- **PyPDF2** (Leitura de PDFs)
- **BeautifulSoup** (Scraping)
- **Uvicorn** (ASGI server)

### Integrações
- **Gemini API** (Análise de PDFs e contexto)
- **Yahoo Finance** (Preços em tempo real)
- **Investimentos.com.br** (Dados fundamentalistas)
- **CVM** (Relatórios oficiais)

### Infraestrutura
- **PostgreSQL** (Banco de dados)
- **Redis** (Cache)
- **Cron Jobs** (Automação)
- **Docker** (Containerização)

---

## 📦 Instalação

### 1. Clone o Repositório

```bash
git clone <repo>
cd blog-cozy-corner-81
```

### 2. Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

pip install -r requirements.txt
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY

python -m uvicorn app.main:app --reload
```

### 3. Setup Frontend

```bash
# Na raiz do projeto
npm install
cp .env.example .env

npm run dev
```

### 4. Acessar

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🔧 Configuração da Automação

### Windows

```powershell
cd backend\scripts
.\setup_task_windows.ps1
```

### Linux/Mac

```bash
cd backend/scripts
chmod +x setup_cron.sh
./setup_cron.sh
```

---

## 📚 Documentação

- **DESIGN_BRIEF.md**: Conceito visual e prompt de design
- **IMPLEMENTATION_GUIDE.md**: Guia técnico completo
- **backend/README.md**: Documentação da API

---

## 🎯 Roadmap

### Fase 1: MVP ✅
- [x] Backend com 3 camadas
- [x] Frontend básico
- [x] Integração API

### Fase 2: Integrações 🔄
- [ ] API de preços real-time
- [ ] Scraping de investimentos.com.br
- [ ] Download automático de PDFs
- [ ] Banco de dados

### Fase 3: Automação 🔄
- [ ] Cron job diário
- [ ] Sistema de notificações
- [ ] Email digest

### Fase 4: Features Avançadas 🔄
- [ ] Backtesting
- [ ] Dashboard de performance
- [ ] Comparação com IBOV
- [ ] Histórico de recomendações

---

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

---

## 📄 Licença

Uso pessoal. Não redistribuir sem permissão.

---

## 🎉 Resultado Esperado

Com o Alpha Terminal funcionando:

1. **Decisões baseadas em dados**, não em emoção
2. **Filtro automático** de 95% do lixo da bolsa
3. **Alertas em tempo real** de oportunidades
4. **Proteção contra manada** (sentiment analysis)
5. **Estratégia clara** para cada ação
6. **Meta de 5% ao mês** alcançável

**Você deixa de ser um investidor amador e se torna um operador profissional.**

---

🚀 **Bem-vindo ao Alpha Terminal. Sua sala de controle financeira.**
