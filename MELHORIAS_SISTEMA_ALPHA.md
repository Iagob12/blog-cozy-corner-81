# 🚀 MELHORIAS DO SISTEMA ALPHA — PLANO COMPLETO

**Data**: 21/02/2026  
**Objetivo**: Tornar o sistema mais preciso, confiável e automatizado

---

## 📋 RESUMO DAS MELHORIAS

### 1. PASSO 1 (Análise Macro) — Repetir 5x para Consenso
### 2. PASSO 2 (Seleção de Empresas) — Repetir 5x + Critérios Rigorosos
### 3. PASSO 3 (Análise com Preços) — Cache de Preços + Notas Justas
### 4. PASSO 4 (Estratégia) — Atualização Automática a cada 1h
### 5. ADMIN — Unificar Releases + Data de Upload

---

## 🎯 PROBLEMA 1: PASSO 2 — EMPRESAS ALEATÓRIAS

### Problema Atual:
- IA seleciona empresas aleatórias
- Não foca nas MELHORES para atingir 5% ao mês
- Resultados inconsistentes entre execuções

### Solução:
**Executar 5 vezes e pegar empresas em comum**

#### Como Funciona:

1. Sistema executa Passo 2 (triagem CSV) **5 vezes**
2. Cada execução retorna ~15-20 empresas
3. Sistema identifica empresas que aparecem em **pelo menos 3 das 5 execuções**
4. Resultado: Apenas empresas CONSISTENTEMENTE boas são aprovadas

#### Exemplo:

```
Execução 1: PRIO3, VALE3, BBSE3, PETR4, ITUB4, WEGE3, ...
Execução 2: PRIO3, VALE3, PETR4, ITUB4, RENT3, WEGE3, ...
Execução 3: PRIO3, VALE3, BBSE3, PETR4, WEGE3, SUZB3, ...
Execução 4: PRIO3, VALE3, PETR4, ITUB4, WEGE3, RENT3, ...
Execução 5: PRIO3, VALE3, BBSE3, PETR4, WEGE3, ITUB4, ...

RESULTADO (aparecem em 3+ execuções):
✅ PRIO3 (5/5) — APROVADA
✅ VALE3 (5/5) — APROVADA
✅ PETR4 (5/5) — APROVADA
✅ WEGE3 (5/5) — APROVADA
✅ ITUB4 (4/5) — APROVADA
✅ BBSE3 (3/5) — APROVADA
❌ RENT3 (2/5) — REJEITADA
❌ SUZB3 (1/5) — REJEITADA
```

#### Benefícios:
- ✅ Elimina empresas "aleatórias"
- ✅ Foca nas MELHORES consistentemente
- ✅ Reduz viés de uma única execução
- ✅ Aumenta confiança nas escolhas

---

## 🎯 PROBLEMA 2: PASSO 1 — ANÁLISE MACRO INCONSISTENTE

### Problema Atual:
- Análise macro executada 1x
- Pode ter viés ou informações incompletas


### Solução:
**Executar 5 vezes e consolidar respostas**

#### Como Funciona:

1. Sistema executa Passo 1 (análise macro) **5 vezes**
2. Cada execução retorna:
   - Setores acelerando
   - Setores a evitar
   - Catalisadores
   - Megatendências
3. Sistema consolida:
   - Setores que aparecem em **3+ execuções** são confirmados
   - Catalisadores mencionados em **3+ execuções** são priorizados
   - Megatendências consistentes são mantidas

#### Exemplo:

```
Execução 1: Setores quentes: [Petróleo, Bancos, Energia]
Execução 2: Setores quentes: [Petróleo, Tecnologia, Energia]
Execução 3: Setores quentes: [Petróleo, Bancos, Infraestrutura]
Execução 4: Setores quentes: [Petróleo, Energia, Bancos]
Execução 5: Setores quentes: [Petróleo, Bancos, Energia]

RESULTADO CONSOLIDADO:
✅ Petróleo (5/5) — CONFIRMADO
✅ Bancos (4/5) — CONFIRMADO
✅ Energia (4/5) — CONFIRMADO
❌ Tecnologia (1/5) — DESCARTADO
❌ Infraestrutura (1/5) — DESCARTADO
```

#### Quando Executar:
- **1x por dia** (quando passar 24h)
- **Antes do Passo 2** (triagem CSV)

---

## 🎯 PROBLEMA 3: BRAPI OSCILA — PREÇOS DESATUALIZADOS

### Problema Atual:
- Brapi API falha frequentemente
- Preços ficam desatualizados
- Análises ficam incorretas

### Solução:
**Cache inteligente de preços com fallback**


#### Como Funciona:

1. **Busca Preços Atuais** (Brapi)
   - Tenta buscar preços de todas empresas
   - Se sucesso: Atualiza cache
   - Se falha: Usa cache anterior

2. **Cache de Preços** (`data/cache/precos_cache.json`)
   ```json
   {
     "PRIO3": {
       "preco": 47.25,
       "timestamp": "2026-02-21T10:30:00",
       "idade_minutos": 15,
       "fonte": "brapi"
     },
     "VALE3": {
       "preco": 65.80,
       "timestamp": "2026-02-21T10:25:00",
       "idade_minutos": 20,
       "fonte": "cache"
     }
   }
   ```

3. **Lógica de Uso**:
   - Preço < 30min: Usa direto
   - Preço 30min-2h: Usa com aviso
   - Preço > 2h: Tenta atualizar, se falhar usa com alerta

4. **Indicadores Visuais**:
   - 🟢 Preço atualizado (< 30min)
   - 🟡 Preço recente (30min-2h)
   - 🔴 Preço antigo (> 2h)

#### Benefícios:
- ✅ Sistema continua funcionando mesmo com Brapi offline
- ✅ Sempre usa preços mais recentes disponíveis
- ✅ Transparência sobre idade dos dados
- ✅ Atualização automática quando Brapi volta

---

## 🎯 PROBLEMA 4: NOTAS DO PASSO 3 SÃO "JOGADAS"

### Problema Atual:
- IA dá notas sem critério claro
- Notas inconsistentes entre empresas similares
- Difícil confiar nas avaliações

### Solução:
**Sistema de notas estruturado e rigoroso**

#### Critérios de Avaliação (0-10):


```
NOTA FINAL = (Fundamentos × 0.3) + (Catalisadores × 0.3) + (Valuation × 0.2) + (Gestão × 0.2)

1. FUNDAMENTOS (0-10):
   - ROE > 20%: +3 pontos
   - ROE 15-20%: +2 pontos
   - ROE 10-15%: +1 ponto
   - Margem EBITDA > 20%: +2 pontos
   - Margem EBITDA 10-20%: +1 ponto
   - Dívida/EBITDA < 2.0: +2 pontos
   - Dívida/EBITDA 2.0-3.0: +1 ponto
   - CAGR Receita > 10%: +2 pontos
   - CAGR Receita 5-10%: +1 ponto

2. CATALISADORES (0-10):
   - 3+ catalisadores de curto prazo: +4 pontos
   - 2 catalisadores de curto prazo: +2 pontos
   - 1 catalisador de curto prazo: +1 ponto
   - Setor em alta no macro: +3 pontos
   - Setor neutro no macro: +1 ponto
   - Release positivo: +3 pontos

3. VALUATION (0-10):
   - P/L < 10: +4 pontos
   - P/L 10-15: +3 pontos
   - P/L 15-20: +2 pontos
   - Upside > 30%: +3 pontos
   - Upside 20-30%: +2 pontos
   - Upside 10-20%: +1 ponto
   - P/VP < 2.0: +3 pontos

4. GESTÃO (0-10):
   - Execução consistente: +3 pontos
   - Alocação de capital eficiente: +3 pontos
   - Transparência com acionistas: +2 pontos
   - Histórico de crescimento: +2 pontos
```

#### Validação Automática:
- Sistema calcula nota baseado nos critérios
- IA deve justificar cada ponto
- Se nota da IA diverge >1.5 pontos: Reanálise automática

#### Exemplo:

```
PRIO3:
- Fundamentos: 8.5/10 (ROE 25%, Margem 30%, Dívida baixa)
- Catalisadores: 9.0/10 (Petróleo em alta, 3 catalisadores)
- Valuation: 7.0/10 (P/L 12, Upside 25%)
- Gestão: 8.0/10 (Execução excelente, transparente)

NOTA FINAL: (8.5×0.3) + (9.0×0.3) + (7.0×0.2) + (8.0×0.2) = 8.25/10
```

---

## 🎯 PROBLEMA 5: ESTRATÉGIA NÃO ATUALIZA COM PREÇO

### Problema Atual:
- Estratégia (entrada/stop/alvo) calculada 1x
- Preços mudam mas estratégia não atualiza
- Oportunidades perdidas ou riscos não identificados


### Solução:
**Atualização automática a cada 1 hora**

#### Como Funciona:

1. **Scheduler de Estratégias**
   - Executa a cada 1 hora
   - Busca preços atuais de todas empresas aprovadas
   - Recalcula entrada/stop/alvo/R/R
   - Atualiza ranking

2. **Recálculo Inteligente**:
   ```python
   # Para cada empresa aprovada:
   preco_atual = buscar_preco(ticker)
   
   # Recalcula baseado na tese original:
   entrada = calcular_entrada(preco_atual, tese)
   stop = calcular_stop(preco_atual, volatilidade)
   alvo_conservador = calcular_alvo(preco_atual, upside_conservador)
   alvo_otimista = calcular_alvo(preco_atual, upside_otimista)
   rr = (alvo_conservador - entrada) / (entrada - stop)
   
   # Atualiza status:
   if preco_atual <= entrada:
       status = "PODE ENTRAR AGORA"
   elif preco_atual > entrada * 1.05:
       status = "AGUARDAR CORREÇÃO"
   elif preco_atual <= stop:
       status = "STOP ATINGIDO - SAIR"
   ```

3. **Alertas Automáticos**:
   - 🟢 Nova oportunidade de entrada
   - 🔴 Stop atingido
   - 🟡 Preço próximo do alvo
   - ⚠️ R/R caiu abaixo de 2.0

4. **Histórico de Mudanças**:
   ```json
   {
     "ticker": "PRIO3",
     "historico": [
       {
         "timestamp": "2026-02-21T10:00:00",
         "preco": 47.25,
         "entrada": 46.50,
         "stop": 44.00,
         "alvo": 52.00,
         "rr": 2.2,
         "status": "AGUARDAR"
       },
       {
         "timestamp": "2026-02-21T11:00:00",
         "preco": 46.30,
         "entrada": 46.50,
         "stop": 44.00,
         "alvo": 52.00,
         "rr": 2.2,
         "status": "PODE ENTRAR AGORA",
         "alerta": "Preço atingiu entrada!"
       }
     ]
   }
   ```

#### Benefícios:
- ✅ Estratégias sempre atualizadas
- ✅ Não perde oportunidades
- ✅ Identifica stops atingidos
- ✅ Ranking dinâmico

---

## 🎯 PROBLEMA 6: ADMIN — RELEASES DUPLICADOS

### Problema Atual:
- Tela de admin tem 2 seções de releases
- Funções duplicadas
- Confuso para o usuário
- Falta data de upload


### Solução:
**Unificar em uma seção com todas funcionalidades**

#### Nova Seção Unificada:

```
┌─────────────────────────────────────────────────────────┐
│ 📄 RELEASES DE RESULTADOS                    [Upload]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ Progresso: ████████████░░░░░░░░ 25/30 (83%)            │
│                                                          │
│ ┌─ COM RELEASE (25) ─────────────────────────────────┐ │
│ │ ✅ PRIO3  Q4 2025  📅 21/02/2026 10:30  [Atualizar]│ │
│ │ ✅ VALE3  Q4 2025  📅 21/02/2026 09:15  [Atualizar]│ │
│ │ ✅ PETR4  Q4 2025  📅 20/02/2026 16:45  [Atualizar]│ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ ┌─ PENDENTE (5) ──────────────────────────────────────┐ │
│ │ ⏳ BBSE3  [Upload Release]                          │ │
│ │ ⏳ ITUB4  [Upload Release]                          │ │
│ │ ⏳ WEGE3  [Upload Release]                          │ │
│ └────────────────────────────────────────────────────┘ │
│                                                          │
│ [Atualizar Todos os Releases]  [Analisar com Releases] │
└─────────────────────────────────────────────────────────┘
```

#### Funcionalidades:

1. **Upload Individual**:
   - Botão ao lado de cada empresa pendente
   - Modal com ticker pré-preenchido
   - Salva data/hora do upload

2. **Upload em Lote**:
   - Botão "Upload" no topo
   - Permite selecionar múltiplos PDFs
   - Sistema detecta ticker pelo nome do arquivo

3. **Atualizar Release**:
   - Botão ao lado de cada release existente
   - Substitui PDF antigo
   - Mantém histórico de versões

4. **Data de Upload**:
   - Mostra quando foi feito upload
   - Indica idade do release
   - Alerta se > 90 dias

5. **Atualizar Todos**:
   - Botão para atualizar releases em lote
   - Útil quando sai novo trimestre
   - Mantém histórico

#### Estrutura de Dados:

```json
{
  "releases": [
    {
      "ticker": "PRIO3",
      "trimestre": "Q4",
      "ano": 2025,
      "arquivo": "PRIO3_Q4_2025.pdf",
      "data_upload": "2026-02-21T10:30:00",
      "tamanho_kb": 1250,
      "versao": 1,
      "historico": [
        {
          "versao": 1,
          "data_upload": "2026-02-21T10:30:00",
          "arquivo": "PRIO3_Q4_2025.pdf"
        }
      ]
    }
  ]
}
```

---

## 📊 FLUXO COMPLETO ATUALIZADO

### Dia 1 (Primeira Análise):

```
1. PASSO 1 — ANÁLISE MACRO (5x)
   ├─ Executa 5 vezes
   ├─ Consolida setores/catalisadores
   └─ Salva contexto consolidado
   ⏱️ Tempo: ~2 minutos

2. PASSO 2 — TRIAGEM CSV (5x)
   ├─ Executa 5 vezes
   ├─ Identifica empresas em comum (3+ aparições)
   └─ Salva lista de aprovadas (~15-20 empresas)
   ⏱️ Tempo: ~5 minutos

3. ADMIN — UPLOAD RELEASES
   ├─ Admin faz upload dos releases
   └─ Sistema registra data/hora
   ⏱️ Tempo: Manual

4. PASSO 3 — ANÁLISE COM RELEASES
   ├─ Busca preços (com cache)
   ├─ Analisa cada empresa
   ├─ Calcula notas estruturadas
   └─ Salva análises
   ⏱️ Tempo: ~3 minutos

5. PASSO 4 — ESTRATÉGIA INICIAL
   ├─ Calcula entrada/stop/alvo
   ├─ Calcula R/R
   └─ Gera ranking
   ⏱️ Tempo: ~2 minutos
```

### Dias Seguintes (Automático):

```
A CADA 24H:
├─ Executa Passo 1 (5x) — Atualiza macro
└─ Se admin atualizar CSV: Executa Passo 2 (5x)

A CADA 1H:
├─ Busca preços atuais (com cache)
├─ Recalcula estratégias
├─ Atualiza ranking
└─ Gera alertas
```

---

## 🛠️ IMPLEMENTAÇÃO

### Arquivos a Criar/Modificar:


#### Backend:

1. **`app/services/consenso_service.py`** (NOVO)
   - Executa análises múltiplas vezes
   - Consolida resultados
   - Identifica padrões comuns

2. **`app/services/precos_cache_service.py`** (NOVO)
   - Gerencia cache de preços
   - Fallback inteligente
   - Indicadores de idade

3. **`app/services/notas_estruturadas_service.py`** (NOVO)
   - Calcula notas baseado em critérios
   - Valida notas da IA
   - Força reanálise se divergir

4. **`app/services/estrategia_dinamica_service.py`** (NOVO)
   - Recalcula estratégias periodicamente
   - Gera alertas
   - Mantém histórico

5. **`app/services/release_manager.py`** (MODIFICAR)
   - Adiciona data de upload
   - Suporta atualização de releases
   - Mantém histórico de versões

6. **`app/routes/admin.py`** (MODIFICAR)
   - Endpoint para atualizar release
   - Endpoint para histórico
   - Endpoint para alertas de estratégia

#### Frontend:

1. **`src/components/admin/ReleasesSection.tsx`** (MODIFICAR)
   - Unifica seções
   - Mostra data de upload
   - Botão de atualizar release

2. **`src/components/admin/AlertasEstrategia.tsx`** (NOVO)
   - Mostra alertas em tempo real
   - Histórico de mudanças
   - Indicadores visuais

#### Dados:

1. **`data/cache/precos_cache.json`** (NOVO)
2. **`data/cache/consenso_macro.json`** (NOVO)
3. **`data/cache/consenso_empresas.json`** (NOVO)
4. **`data/estrategias/historico.json`** (NOVO)
5. **`data/releases/metadata.json`** (MODIFICAR)

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Consenso (Passos 1 e 2)
- [ ] Criar `consenso_service.py`
- [ ] Implementar execução 5x do Passo 1
- [ ] Implementar consolidação de setores
- [ ] Implementar execução 5x do Passo 2
- [ ] Implementar identificação de empresas comuns
- [ ] Testar com dados reais
- [ ] Validar resultados

### Fase 2: Cache de Preços
- [ ] Criar `precos_cache_service.py`
- [ ] Implementar salvamento de preços
- [ ] Implementar fallback inteligente
- [ ] Adicionar indicadores de idade
- [ ] Integrar com Passo 3
- [ ] Testar com Brapi offline
- [ ] Validar precisão

### Fase 3: Notas Estruturadas
- [ ] Criar `notas_estruturadas_service.py`
- [ ] Implementar cálculo de notas
- [ ] Implementar validação
- [ ] Adicionar reanálise automática
- [ ] Integrar com Passo 3
- [ ] Testar com empresas reais
- [ ] Validar consistência

### Fase 4: Estratégia Dinâmica
- [ ] Criar `estrategia_dinamica_service.py`
- [ ] Implementar scheduler (1h)
- [ ] Implementar recálculo
- [ ] Implementar alertas
- [ ] Criar histórico
- [ ] Integrar com frontend
- [ ] Testar automação

### Fase 5: Admin Unificado
- [ ] Modificar `ReleasesSection.tsx`
- [ ] Adicionar data de upload
- [ ] Implementar atualização de releases
- [ ] Criar histórico de versões
- [ ] Remover seção duplicada
- [ ] Testar fluxo completo
- [ ] Validar UX

---

## 🎯 RESULTADOS ESPERADOS

### Antes:
- ❌ Empresas aleatórias selecionadas
- ❌ Análise macro inconsistente
- ❌ Preços desatualizados quando Brapi falha
- ❌ Notas sem critério claro
- ❌ Estratégias estáticas
- ❌ Admin confuso com duplicatas

### Depois:
- ✅ Apenas MELHORES empresas (consenso 5x)
- ✅ Análise macro consolidada e confiável
- ✅ Preços sempre disponíveis (cache inteligente)
- ✅ Notas justas e estruturadas
- ✅ Estratégias atualizadas a cada 1h
- ✅ Admin limpo e funcional

---

## 📈 MÉTRICAS DE SUCESSO

### Qualidade:
- **Consenso**: 80%+ das empresas aparecem em 3+ execuções
- **Preços**: 95%+ de disponibilidade (mesmo com Brapi offline)
- **Notas**: Divergência < 1.0 ponto entre cálculo e IA
- **Estratégias**: 100% atualizadas a cada hora

### Performance:
- **Passo 1 (5x)**: < 3 minutos
- **Passo 2 (5x)**: < 6 minutos
- **Atualização estratégias**: < 30 segundos
- **Cache de preços**: < 5 segundos

### Confiabilidade:
- **Uptime**: 99%+ (mesmo com APIs offline)
- **Consistência**: 90%+ de empresas repetidas entre dias
- **Precisão**: 95%+ de notas validadas

---

## 🚀 PRÓXIMOS PASSOS

1. **Revisar este documento** com o time
2. **Priorizar fases** (sugestão: 1 → 2 → 3 → 4 → 5)
3. **Implementar Fase 1** (consenso)
4. **Testar em produção**
5. **Iterar baseado em feedback**

---

**Documento criado em**: 21/02/2026  
**Versão**: 1.0  
**Status**: Aguardando aprovação
