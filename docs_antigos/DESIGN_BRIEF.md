# Alpha Terminal - Design Brief & Prompt Perfeito

## 🎯 Visão Geral

O Alpha Terminal é um **Terminal de Inteligência Tática** que transforma investidores comuns em operadores profissionais. Não é apenas um site de dicas - é uma sala de controle financeira que processa milhares de dados em segundos e entrega decisões cirúrgicas.

---

## 🎨 PROMPT PERFEITO PARA DESIGN

```
Crie um design de terminal financeiro de alta performance com estética cyberpunk-minimalista.

CONCEITO VISUAL:
- Inspiração: Terminal Bloomberg + Cyberpunk 2077 + Apple Design System
- Paleta: Fundo escuro (#0a0a0f), acentos em verde neon (#00ff88), vermelho (#ff3366), amarelo (#ffd700)
- Tipografia: Monospace para números (JetBrains Mono), Sans-serif moderna para texto (Inter)
- Elementos: Glassmorphism sutil, bordas com glow effect, animações micro-interativas

LAYOUT PRINCIPAL (Bento Grid):
1. Hero Section - "Alpha Pick do Dia"
   - Card grande com destaque visual
   - Ticker em fonte grande e bold
   - Preço atual vs Preço Teto com barra de progresso
   - Upside potencial em destaque (verde se >10%, amarelo se 5-10%)
   - Badge de recomendação (COMPRA FORTE, COMPRA, AGUARDAR)
   - Mini-gráfico sparkline dos últimos 30 dias

2. Feed de Alertas (Sidebar direita)
   - Cards compactos com ícones de alerta
   - Cores por tipo: Verde (oportunidade de compra), Vermelho (vender), Amarelo (atenção)
   - Timestamp relativo ("há 2 horas")
   - Animação de entrada suave

3. Tabela Elite (Full width abaixo)
   - Tabela responsiva com hover effects
   - Colunas: Rank, Ticker, Setor, ROE, CAGR, P/L, Efficiency Score, Upside, Recomendação
   - Sorting interativo
   - Badges coloridos para setores
   - Ícones de tendência (↑↓)

4. Painel Macro (Top bar)
   - Indicadores em linha: Selic, IPCA, Setores Favorecidos
   - Ícones minimalistas
   - Atualização em tempo real com pulse animation

COMPONENTES ESPECIAIS:
- Preço Teto Indicator: Gauge circular mostrando margem de segurança
- Catalisadores: Tags com ícones (🚀 expansão, 📝 contrato, ⚡ alavancagem)
- Sentiment Status: Badge com emoji (😊 normal, ⚠️ atenção, 🚨 alerta manada)
- Tempo na Carteira: Countdown visual (90 dias → barra de progresso)

INTERAÇÕES:
- Hover nos cards: Elevação + glow effect
- Click no ticker: Slide panel lateral com tese completa
- Scroll: Parallax sutil no background
- Loading states: Skeleton screens com shimmer effect

RESPONSIVIDADE:
- Desktop: Bento grid 3 colunas
- Tablet: 2 colunas, sidebar vira accordion
- Mobile: 1 coluna, cards empilhados, bottom navigation

DARK MODE NATIVO:
- Fundo: Gradiente sutil de preto para azul escuro
- Contraste alto para acessibilidade
- Glow effects mais intensos

MICRO-ANIMAÇÕES:
- Números: Count-up animation ao carregar
- Badges: Pulse quando há nova recomendação
- Alertas: Slide in from right
- Gráficos: Draw animation
```

---

## 🎯 Estrutura de Informações por Seção

### 1. ALPHA PICK DO DIA (Hero Card)
```
┌─────────────────────────────────────────┐
│ 🏆 ALPHA PICK DO DIA                    │
│                                         │
│ WEGE3                    Industrial     │
│ WEG S.A.                                │
│                                         │
│ R$ 45,80  →  R$ 52,30 (Teto)           │
│ ████████░░ 85% do teto                  │
│                                         │
│ 📈 Upside: +14.2%                       │
│ ⏱️ Tempo estimado: 90 dias              │
│                                         │
│ 🚀 Catalisadores:                       │
│ • Expansão internacional                │
│ • Novo contrato com Tesla               │
│                                         │
│ 💡 Efficiency Score: 1.43               │
│ ROE: 22.3% | CAGR: 18.5% | P/L: 28.5   │
│                                         │
│ [COMPRA FORTE] 😊 Sentiment Normal      │
│                                         │
│ [Ver Tese Completa →]                   │
└─────────────────────────────────────────┘
```

### 2. FEED DE ALERTAS (Sidebar)
```
┌─────────────────────────┐
│ 🔔 ALERTAS ATIVOS       │
├─────────────────────────┤
│ 🟢 OPORTUNIDADE         │
│ ITUB4 - R$ 28,90        │
│ Abaixo do teto (-8%)    │
│ há 2 horas              │
├─────────────────────────┤
│ 🔴 REALIZAR LUCROS      │
│ PETR4 - R$ 38,50        │
│ Acima do teto (+12%)    │
│ há 5 horas              │
├─────────────────────────┤
│ ⚠️ RISCO MANADA         │
│ MGLU3                   │
│ Volume 3.2x acima       │
│ há 1 dia                │
└─────────────────────────┘
```

### 3. TABELA ELITE
```
┌──────────────────────────────────────────────────────────────────────┐
│ 📊 CARTEIRA ELITE - 15 AÇÕES SELECIONADAS                            │
├────┬────────┬──────────┬──────┬──────┬──────┬───────┬────────┬──────┤
│ #  │ Ticker │ Setor    │ ROE  │ CAGR │ P/L  │ Score │ Upside │ Rec  │
├────┼────────┼──────────┼──────┼──────┼──────┼───────┼────────┼──────┤
│ 1  │ WEGE3  │ Indust.  │ 22.3 │ 18.5 │ 28.5 │ 1.43  │ +14.2% │ 🟢   │
│ 2  │ RENT3  │ Varejo   │ 19.8 │ 22.4 │ 12.5 │ 3.38  │ +18.5% │ 🟢   │
│ 3  │ PRIO3  │ Energia  │ 24.5 │ 28.3 │ 6.8  │ 7.76  │ +22.1% │ 🟢   │
└────┴────────┴──────────┴──────┴──────┴──────┴───────┴────────┴──────┘
```

### 4. PAINEL MACRO (Top Bar)
```
┌──────────────────────────────────────────────────────────────┐
│ 📈 Selic: 10.75%  │  📊 IPCA: 4.5%  │  ✅ Favorecidos: Financeiro, Energia, Saúde  │
└──────────────────────────────────────────────────────────────┘
```

### 5. PAINEL DE TESE (Slide Panel)
```
┌─────────────────────────────────────────┐
│ ← Voltar          WEGE3                 │
├─────────────────────────────────────────┤
│                                         │
│ 📊 ANÁLISE FUNDAMENTALISTA              │
│                                         │
│ Efficiency Score: 1.43 (Top 5%)         │
│ ROE: 22.3% (Excelente)                  │
│ CAGR: 18.5% (Alto crescimento)          │
│ P/L: 28.5 (Razoável para o setor)      │
│                                         │
│ 💰 ESTRATÉGIA DE ENTRADA                │
│                                         │
│ Preço Atual: R$ 45,80                   │
│ Preço Teto: R$ 52,30                    │
│ Preço Ideal: R$ 43,50 (-5%)             │
│                                         │
│ Meta de Lucro: +14.2% (R$ 52,30)        │
│ Stop Loss: R$ 41,00 (-10%)              │
│ Tempo Estimado: 90 dias                 │
│                                         │
│ 🚀 CATALISADORES                        │
│                                         │
│ 1. Expansão Internacional               │
│    Impacto: Alto                        │
│    Nova fábrica no México prevista      │
│    para Q2/2026                         │
│                                         │
│ 2. Novo Contrato com Tesla              │
│    Impacto: Médio                       │
│    Fornecimento de motores elétricos    │
│                                         │
│ 📈 CONTEXTO MACRO                       │
│                                         │
│ Setor Industrial: Peso 1.05 (Neutro)    │
│ Juros em 10.75%: Impacto moderado       │
│ Inflação em 4.5%: Favorável             │
│                                         │
│ 😊 SENTIMENT ANALYSIS                   │
│                                         │
│ Status: Normal                          │
│ Volume de menções: 52 (média: 50)       │
│ Ratio: 1.04x                            │
│                                         │
│ ⚠️ RISCOS                               │
│                                         │
│ • Exposição cambial (30% receita USD)   │
│ • Concorrência chinesa                  │
│ • Dependência de commodities            │
│                                         │
│ [Adicionar à Carteira]                  │
└─────────────────────────────────────────┘
```

---

## 🎨 Paleta de Cores Detalhada

```css
/* Background */
--bg-primary: #0a0a0f;
--bg-secondary: #141419;
--bg-tertiary: #1a1a24;

/* Accent Colors */
--green-neon: #00ff88;
--green-dark: #00cc6a;
--red-alert: #ff3366;
--red-dark: #cc2952;
--yellow-warning: #ffd700;
--blue-info: #00d4ff;

/* Text */
--text-primary: #ffffff;
--text-secondary: #a0a0b0;
--text-muted: #606070;

/* Borders */
--border-subtle: rgba(255, 255, 255, 0.1);
--border-glow: rgba(0, 255, 136, 0.3);
```

---

## 🚀 Funcionalidades Especiais

### 1. Atualização Automática Diária
- Cron job que roda às 18h (após fechamento da bolsa)
- Baixa CSV de investimentos.com.br
- Processa com IA (Gemini)
- Atualiza banco de dados
- Envia notificações push

### 2. Sistema de Notificações
- Push notifications no navegador
- Email digest diário
- Alertas de preço em tempo real
- Avisos de risco de manada

### 3. Histórico e Backtesting
- Gráfico de performance da carteira
- Comparação com IBOV
- Taxa de acerto das recomendações
- Retorno médio por ação

### 4. Upload de Relatórios
- Drag & drop de PDFs de RI
- Análise automática com Gemini
- Extração de catalisadores
- Score qualitativo

---

## 📱 Responsividade

### Desktop (>1024px)
- Bento grid 3 colunas
- Sidebar fixa
- Hover effects completos

### Tablet (768px - 1024px)
- Bento grid 2 colunas
- Sidebar colapsável
- Touch-friendly

### Mobile (<768px)
- Cards empilhados
- Bottom navigation
- Swipe gestures
- Simplified charts

---

## ⚡ Performance

- Lazy loading de componentes
- Virtual scrolling na tabela
- Debounce em searches
- Cache de API calls
- Service Worker para offline

---

## 🔐 Segurança

- Rate limiting na API
- Validação de inputs
- Sanitização de dados
- HTTPS obrigatório
- CORS configurado

---

## 📊 Métricas de Sucesso

- Tempo de carregamento < 2s
- Taxa de conversão (visitante → usuário ativo)
- Engagement (tempo no site)
- Taxa de acerto das recomendações
- Retorno médio da carteira

---

## 🎯 Próximos Passos

1. ✅ Backend FastAPI funcionando
2. ✅ Integração com Gemini API
3. 🔄 Automação de download de CSV
4. 🔄 Integração com API de preços real-time
5. 🔄 Sistema de notificações
6. 🔄 Backtesting engine
7. 🔄 Dashboard de performance
