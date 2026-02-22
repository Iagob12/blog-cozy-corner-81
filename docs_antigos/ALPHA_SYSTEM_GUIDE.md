# Alpha Terminal - Sistema de Inteligência Tática

## 🎯 Objetivo
Meta de **5% ao mês** através de valorização de preço (não dividendos).

## 🧠 Filosofia Alpha

### Perfil de Ativo Elite
- **ROE > 15%** (idealmente 30-50%)
- **CAGR > 12%** (crescimento real)
- **P/L < 15** (não comprar o topo)
- **Dívida Líquida/EBITDA < 2,5**

### Mentalidade
- Antecipação: encontrar "Nvidias" antes da manada
- Swing Trade: 5-20 dias, capturando ciclos
- Assimetria: risco/retorno mínimo de 2:1
- Anti-Manada: evitar euforia do varejo

## 🚀 Como Usar

### 1. Configuração

```bash
# Backend
cd backend
pip install -r requirements.txt

# Configure a API Key do Gemini
cp .env.example .env
# Edite .env e adicione: GEMINI_API_KEY=sua_chave_aqui

# Inicie o servidor
python -m uvicorn app.main:app --reload
```

### 2. Os 6 Prompts Implementados

#### PROMPT 1 - Radar de Oportunidades
**Endpoint:** `GET /api/v1/alpha/radar-oportunidades`

Identifica setores em aceleração ANTES da manada.

**Retorna:**
- Setores em fase inicial de aceleração
- Movimentos silenciosos (próximas "Nvidias")
- Mudanças de ciclo
- Narrativas institucionais

**Quando usar:** Semanalmente para identificar onde o dinheiro vai entrar.

---

#### PROMPT 2 - Triagem Fundamentalista
**Integrado em:** `GET /api/v1/top-picks`

Filtra empresas com maior potencial de valorização.

**Critérios:**
- P/L < 15, ROE > 15%, CAGR > 12%
- Dívida controlada
- Margem crescente

**Retorna:** Ranking com score de valorização e catalisadores.

---

#### PROMPT 3 - Análise Comparativa
**Endpoint:** `POST /api/v1/alpha/analise-comparativa`

Busca relatórios de RI e compara múltiplas empresas.

**Body:**
```json
{
  "tickers": ["PRIO3", "VULC3", "GMAT3"]
}
```

**Retorna:**
- Análise individual de cada empresa
- Ranking das 3 melhores
- Ação: entrar_primeiro | monitorar | descartar

---

#### PROMPT 4 - Swing Trade
**Endpoint:** `GET /api/v1/alpha/swing-trade/{ticker}`

Análise para operação de 5-20 dias.

**Retorna:**
- Saúde da empresa
- Eventos próximos que podem mover o preço
- Momento técnico
- Stop loss e alvo
- Relação risco/retorno

**Só recomenda se risco/retorno >= 2:1**

---

#### PROMPT 5 - Revisão de Carteira
**Endpoint:** `POST /api/v1/alpha/revisao-carteira`

Análise SEM APEGO das posições atuais.

**Body:**
```json
{
  "carteira": [
    {"ticker": "PRIO3", "qtd": 100, "preco_medio": 45.50, "resultado_pct": 12.5}
  ]
}
```

**Retorna:**
- O que CORTAR
- O que MANTER
- O que AUMENTAR
- Oportunidades melhores no mercado

---

#### PROMPT 6 - Verificação Anti-Manada
**Endpoint:** `GET /api/v1/alpha/anti-manada/{ticker}`

Checa se não estamos comprando o topo.

**Retorna:**
- Exposição na mídia
- Fundamento vs narrativa
- Posicionamento institucional
- Veredito: ENTRAR_AGORA | ESPERAR_CORRECAO | JANELA_FECHOU

---

### 3. Dados de Mercado em Tempo Real

#### Cotação
```
GET /api/v1/market/quote/{ticker}
```

#### Visão Geral (Ibovespa, Dólar)
```
GET /api/v1/market/overview
```

#### Momentum
```
GET /api/v1/market/momentum/{ticker}
```

---

## 📊 Fluxo de Trabalho Recomendado

### Semanal
1. **Radar de Oportunidades** - Identificar setores quentes
2. **Top Picks** - Filtrar empresas nesses setores
3. **Análise Comparativa** - Analisar finalistas com relatórios de RI

### Antes de Comprar
4. **Verificação Anti-Manada** - Checar se não é fumaça
5. **Swing Trade** (se for operação curta) - Confirmar momento técnico

### Mensal
6. **Revisão de Carteira** - Cortar peso morto, realocar capital

---

## 🎯 Carteira Atual (Exemplo)

- **PRIO3** - Motor de crescimento (Wahoo)
- **VULC3** - Eficiência industrial (ROE 50%)
- **GMAT3** - Domínio regional (P/L descontado)
- **CURY3** - Rentabilidade imobiliária
- **POMO3** - Superciclo de exportação

---

## ⚠️ Regras de Ouro

1. **Nunca compre o que já virou manchete**
2. **Risco/retorno mínimo de 2:1**
3. **Corte posições sem apego**
4. **Entre no começo do ciclo, não no fim**
5. **Ignore dividend traps**

---

## 🔧 Próximos Passos

- [ ] Integrar mais fontes de dados de RI
- [ ] Adicionar alertas automáticos de preço
- [ ] Dashboard com gráficos de momentum
- [ ] Histórico de recomendações e performance
- [ ] Integração com corretoras para execução

---

## 📝 Notas

Este sistema usa **Gemini 1.5 Pro** para análise de mercado e relatórios.
A API gratuita **brapi.dev** fornece cotações em tempo real da B3.

**Importante:** Este é um sistema de apoio à decisão. Sempre faça sua própria análise antes de investir.
