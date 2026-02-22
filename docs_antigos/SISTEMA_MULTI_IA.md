# 🤖 SISTEMA MULTI-IA - AIML API

## 🎯 VISÃO GERAL

Sistema premium de análise de ações usando **2 IAs diferentes** via AIML API:

1. **Gemini 2.0 Flash Thinking** - Raciocínio profundo sobre mercado
2. **Claude 3.5 Sonnet** - Análise cirúrgica de cada ação

---

## 🧠 ARQUITETURA DO SISTEMA

### FASE 1: Gemini 2.0 Flash Thinking
**Objetivo**: Análise macro e seleção das melhores ações

**Capacidades**:
- Modo de raciocínio profundo (thinking mode)
- Análise do contexto macroeconômico
- Identificação de setores em aceleração
- Seleção das top 15 ações
- Detecção de armadilhas (ações no topo, setores em queda)

**Input**:
- Lista de ações candidatas (fundamentos)
- Contexto macro (juros, inflação, setores)
- Data atual

**Output**:
```json
{
  "analise_macro": "Cenário atual favorável para...",
  "setores_favoritos": ["Energia", "Consumo"],
  "top_15_acoes": [
    {
      "ticker": "PRIO3",
      "score": 9.5,
      "razao": "ROE excepcional + setor em alta",
      "catalisadores": ["Petróleo em alta", "Eficiência operacional"],
      "risco": "baixo"
    }
  ],
  "alertas": ["Evitar setor X por motivo Y"]
}
```

### FASE 2: Claude 3.5 Sonnet
**Objetivo**: Análise profunda de cada ação selecionada

**Capacidades**:
- Análise fundamentalista detalhada
- Interpretação de relatórios trimestrais
- Cálculo de preço justo (valuation)
- Identificação de riscos específicos
- Recomendação final com confiança

**Input**:
- Ticker da ação
- Fundamentos (ROE, CAGR, P/L, Dívida)
- Preço atual
- Relatório trimestral Q4 2025 (mais recente)

**Output**:
```json
{
  "ticker": "PRIO3",
  "analise_fundamentalista": {
    "qualidade_roe": "Excepcional - 35% indica alta eficiência",
    "crescimento": "CAGR de 18.5% é muito forte",
    "valuation": "P/L de 8.5 está barato",
    "endividamento": "Controlado em 1.2x"
  },
  "analise_trimestral": {
    "receita": "Cresceu 15% YoY",
    "lucro": "Margens em expansão",
    "destaques": ["Eficiência operacional", "Redução de custos"]
  },
  "preco_justo": 52.00,
  "preco_teto": 58.00,
  "upside": 19.6,
  "recomendacao": "COMPRA FORTE",
  "confianca": "ALTA",
  "tempo_estimado_dias": 90,
  "riscos": ["Volatilidade do petróleo", "Câmbio"]
}
```

---

## 🚀 ENDPOINTS DISPONÍVEIS

### 1. Top Picks Inteligente (Multi-IA)
```
GET /api/v1/aiml/top-picks-inteligente?limit=15
```

**Fluxo completo**:
1. Filtra ações por fundamentos (ROE, CAGR, P/L)
2. Busca preços reais (Alpha Vantage)
3. Gemini analisa mercado e seleciona top 15
4. Claude analisa cada uma em profundidade
5. Retorna portfolio final com análises completas

**Tempo estimado**: ~2-3 minutos (15 ações)

### 2. Análise de Mercado (Gemini)
```
GET /api/v1/aiml/analise-mercado
```

Apenas Fase 1: Análise macro com Gemini Thinking

### 3. Análise de Ação (Claude)
```
GET /api/v1/aiml/analise-acao/{ticker}
```

Apenas Fase 2: Análise profunda de uma ação específica

---

## 🔧 CONFIGURAÇÃO

### 1. API Key AIML
Adicione no `.env`:
```env
AIML_API_KEY=3d1ad51f660b4adfadfb6bead232d998
```

### 2. Modelos Configurados
```python
models = {
    "gemini_thinking": "gemini-2.0-flash-thinking-exp-1219",
    "claude_sonnet": "claude-3-5-sonnet-20241022",
    "gemini_flash": "gemini-2.0-flash-exp"  # Backup rápido
}
```

---

## 🧪 COMO TESTAR

### Teste Rápido
```bash
cd blog-cozy-corner-81/backend
python test_aiml.py
```

Deve mostrar:
```
✓ Gemini Thinking - SUCESSO
✓ Claude Sonnet - SUCESSO
🎉 SISTEMA MULTI-IA FUNCIONANDO!
```

### Teste via API
```bash
# Inicia backend
uvicorn app.main:app --reload --port 8000

# Em outro terminal
curl http://localhost:8000/api/v1/aiml/analise-mercado
```

---

## 📊 COMPARAÇÃO: Tradicional vs Multi-IA

### Sistema Tradicional
- ✓ Rápido (~10 segundos)
- ✓ Preços reais (Alpha Vantage)
- ✓ Filtros quantitativos
- ✗ Análise básica
- ✗ Sem contexto macro profundo
- ✗ Valuation simplificado

### Sistema Multi-IA
- ✓ Preços reais (Alpha Vantage)
- ✓ Filtros quantitativos
- ✓ Análise macro profunda (Gemini)
- ✓ Raciocínio sobre mercado
- ✓ Análise cirúrgica (Claude)
- ✓ Valuation preciso
- ✓ Relatórios trimestrais
- ✗ Mais lento (~2-3 min)
- ✗ Custo de API

---

## 💰 CUSTOS ESTIMADOS

### AIML API Pricing
- Gemini 2.0 Flash Thinking: ~$0.01 por análise
- Claude 3.5 Sonnet: ~$0.02 por ação

**Custo por análise completa (15 ações)**:
- Fase 1 (Gemini): $0.01
- Fase 2 (Claude × 15): $0.30
- **Total**: ~$0.31 por análise

**Com cache de 15 minutos**: ~$0.31 a cada 15 min

---

## 🎯 QUANDO USAR CADA SISTEMA

### Use Sistema Tradicional quando:
- Precisa de resposta rápida
- Quer apenas preços atualizados
- Já conhece as ações
- Faz análise própria

### Use Sistema Multi-IA quando:
- Quer análise profunda
- Precisa de contexto macro
- Quer valuation preciso
- Busca recomendações fundamentadas
- Tem relatórios trimestrais

---

## 🔄 FLUXO COMPLETO

```
1. Frontend solicita análise
   ↓
2. Backend filtra ações (fundamentos)
   ↓
3. Busca preços reais (Alpha Vantage)
   ↓
4. FASE 1: Gemini analisa mercado
   - Contexto macro
   - Setores favoritos
   - Seleciona top 15
   ↓
5. FASE 2: Claude analisa cada ação
   - Fundamentos
   - Relatório trimestral
   - Valuation
   - Recomendação
   ↓
6. Retorna portfolio final
   - Preços reais
   - Análises IA
   - Recomendações
```

---

## 📝 PRÓXIMAS MELHORIAS

### Curto Prazo
- [ ] Scraping automático de relatórios trimestrais
- [ ] Cache inteligente de análises
- [ ] Modo "express" (só Gemini)

### Médio Prazo
- [ ] Análise de notícias (sentiment)
- [ ] Comparação com analistas do mercado
- [ ] Backtesting de recomendações

### Longo Prazo
- [ ] Fine-tuning de modelos
- [ ] Análise técnica integrada
- [ ] Alertas proativos

---

## 🐛 TROUBLESHOOTING

### Erro: "API Key inválida"
```bash
# Verifique se a key está no .env
cat backend/.env | grep AIML_API_KEY
```

### Erro: "Timeout"
- Aumente timeout em `aiml_service.py`
- Verifique conexão com internet
- Tente novamente (pode ser instabilidade da API)

### Erro: "Rate limit"
- AIML API tem limites por minuto
- Aguarde alguns segundos
- Considere upgrade do plano

---

## 📚 DOCUMENTAÇÃO AIML API

- Website: https://aimlapi.com
- Docs: https://docs.aimlapi.com
- Dashboard: https://aimlapi.com/app/keys
- Modelos: https://docs.aimlapi.com/models

---

**Status**: ✅ IMPLEMENTADO E TESTADO
**Versão**: 1.0.0
**Data**: 19/02/2026
