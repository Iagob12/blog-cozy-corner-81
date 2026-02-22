# 🎯 SISTEMA DE ANÁLISE - 4 PASSOS (METODOLOGIA PRIMO RICO)

## STATUS: ✅ IMPLEMENTADO E FUNCIONANDO

Sistema profissional de análise de ações focado em **VALORIZAÇÃO DE PREÇO** (não dividendos).

**Meta**: 5% ao mês de valorização

---

## 📊 FLUXO COMPLETO

### PASSO 1 - ANÁLISE MACRO (Radar de Oportunidades)

**Objetivo**: Entender o cenário atual para filtrar ações com mais inteligência

**Frequência**: 1x por dia (cache de 24h)

**O que analisa**:
- Taxa Selic atual e tendência
- Dólar: patamar e impacto nas ações
- Setores em aceleração
- Setores a evitar
- Catalisadores das próximas semanas
- Narrativa institucional (o que fundos estão comprando)
- Megatendências e timing

**Arquivo**: `backend/data/cache/macro_context.json`

---

### PASSO 2 - TRIAGEM CSV (Perfil A e B)

**Objetivo**: Filtrar ações com maior potencial de valorização

**Perfil A - Momentum Rápido** (2 dias a 2 semanas):
- ROE > 12%
- P/L < 20 (abaixo da média do setor)
- Catalisador próximo

**Perfil B - Consistência com Upside** (até 3 meses):
- ROE > 15%
- P/L < 25
- Setor com vento a favor no cenário macro

**Critérios de ELIMINAÇÃO**:
- Empresas cujo único atrativo é dividendo sem crescimento
- P/L > 25 sem justificativa
- Setor em contração

**Fonte**: `backend/data/stocks.csv`

---

### PASSO 3 - ANÁLISE PROFUNDA COM RELEASE

**Objetivo**: Analisar profundamente cada empresa usando release de resultados

**6 Pontos de Avaliação**:

1. **SAÚDE FINANCEIRA REAL**
   - Geração de caixa operacional
   - Tendência de margens
   - Endividamento real

2. **QUALIDADE DA GESTÃO**
   - Execução
   - Alocação de capital
   - Transparência com acionista

3. **CATALISADORES DE VALORIZAÇÃO** (CRÍTICO!)
   - O que pode fazer a ação SUBIR nos próximos 6-18 meses
   - Deve ser ESPECÍFICO: contrato, expansão, ciclo setorial
   - NÃO genérico!

4. **RISCOS REAIS E CONCRETOS**
   - Não os genéricos de qualquer relatório
   - Os que REALMENTE podem derrubar o preço DESTA empresa

5. **VALORIZAÇÃO**
   - Está cara, justa ou barata?
   - Com base nos fundamentos
   - Comparado ao setor

6. **NOTA DE RECOMENDAÇÃO** (0 a 10)
   - Se ruim para valorização de preço: nota 0
   - Explica por quê descartar

**Fonte**: `backend/data/releases/` (releases baixados)

---

### PASSO 4 - RANKING FINAL

**Objetivo**: Montar ranking das melhores oportunidades

**Critérios**:
- Apenas ações com **nota >= 6** (aprovadas)
- Ordenadas por nota (melhor para pior)
- Cada ação tem:
  - Tese resumida (4-5 linhas)
  - Catalisadores específicos
  - Riscos concretos
  - Preço teto calculado
  - Upside potencial

**Arquivo**: `backend/data/ranking_cache.json`

---

## 🤖 MODELO E CONFIGURAÇÃO

**Modelo**: Llama 3.1 405B Reasoning (Groq)
- 405 bilhões de parâmetros
- Qualidade MUITO superior
- Análises mais elaboradas e rigorosas

**Rate Limit**:
- 3 segundos entre requisições
- 1 análise por vez (evita sobrecarga)
- 6 chaves Groq em rotação

**Análises Automáticas**:
- A cada 1 hora
- 100% automático
- Não precisa clicar em nada

---

## 📁 ARQUIVOS PRINCIPAIS

```
backend/app/services/
├── alpha_v4_otimizado.py      # Sistema de 4 passos
├── multi_groq_client.py        # Cliente Groq com 6 chaves
├── release_manager.py          # Gerencia releases
└── precos_service.py           # Busca preços reais

backend/data/
├── stocks.csv                  # Dados fundamentalistas
├── ranking_cache.json          # Ranking atual
└── cache/
    └── macro_context.json      # Contexto macro (24h)
```

---

## 🔄 CONTEXTO ENTRE CHAVES

**PROBLEMA**: Groq perde contexto ao trocar de chave

**SOLUÇÃO IMPLEMENTADA**:
- Cada prompt inclui `[CONTEXTO ANTERIOR]` no início
- Contexto macro é passado para todas as análises
- Não depende de memória do modelo
- Contexto é reconstruído manualmente em cada prompt

---

## 📊 EXEMPLO DE SAÍDA

```json
{
  "ticker": "BBSE3",
  "nota": 9.0,
  "recomendacao": "COMPRA FORTE",
  "preco_atual": 34.05,
  "preco_teto": 44.27,
  "upside": 30.0,
  "saude_financeira": "ROE de 79% indica rentabilidade excepcional...",
  "qualidade_gestao": "Gestão eficiente com foco em crescimento...",
  "catalisadores": [
    "Expansão no segmento de seguros corporativos",
    "Crescimento de 25% no lucro líquido no último trimestre"
  ],
  "riscos_reais": [
    "Aumento da concorrência no setor de seguros",
    "Possível regulação mais rígida do setor"
  ],
  "valorizacao": "barata - P/L de 7.5 está abaixo da média do setor",
  "tese_resumida": "BBSE3 apresenta ROE excepcional de 79% com P/L atrativo..."
}
```

---

## ✅ DIFERENÇAS DO SISTEMA ANTERIOR

| Aspecto | Antes | Agora |
|---------|-------|-------|
| Prompts | Genéricos | Profissionais (Primo Rico) |
| Modelo | Llama 3.3 70B | Llama 3.1 405B |
| Catalisadores | Genéricos | Específicos e concretos |
| Análise | Superficial | 6 pontos profundos |
| Contexto | Perdido | Mantido entre prompts |
| Filtro | ROE > 10% | Perfil A e B |
| Aprovação | Todas | Apenas nota >= 6 |

---

## 🚀 PRÓXIMOS PASSOS

1. ✅ Sistema implementado
2. ✅ Backend reiniciado
3. ⏳ Aguardar próxima análise automática (~10 minutos)
4. 📊 Comparar qualidade das análises
5. ✅ Validar catalisadores específicos
6. ✅ Verificar scores mais rigorosos

---

## 📝 NOTAS IMPORTANTES

- **Foco**: Valorização de preço (NÃO dividendos)
- **Meta**: 5% ao mês
- **Rigor**: Se ruim, nota baixa (honesto)
- **Catalisadores**: Devem ser ESPECÍFICOS
- **Análise**: Profunda e fundamentalista
- **Automático**: Roda sozinho a cada 1 hora

---

**Data de Implementação**: 21/02/2026
**Versão**: 4.0 Otimizado (Metodologia Primo Rico)
**Status**: ✅ Funcionando
