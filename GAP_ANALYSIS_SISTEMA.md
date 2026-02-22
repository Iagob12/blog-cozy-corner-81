# 📊 GAP ANALYSIS - SISTEMA ATUAL vs METODOLOGIA PROPOSTA

**Data**: 21/02/2026  
**Objetivo**: Identificar o que falta implementar para atingir a metodologia completa de 5 etapas

---

## 🎯 RESUMO EXECUTIVO

O sistema atual já tem uma base sólida com 5 etapas implementadas, mas os **prompts são simplificados** e falta a **gestão de contexto manual** entre sessões do Groq. A metodologia proposta traz prompts muito mais profundos e um sistema de contexto persistente.

### Status Geral:
- ✅ **Estrutura em 5 etapas**: Implementada
- ⚠️ **Prompts**: Simplificados (precisam ser aprofundados)
- ❌ **Bloco de contexto manual**: Não implementado
- ⚠️ **Critérios de eliminação**: Parcialmente implementados
- ❌ **Perfis operacionais (A/B)**: Não separados claramente
- ❌ **Etapa 4 (Estratégia)**: Não implementada no fluxo principal
- ❌ **Etapa 5 (Revisão)**: Não implementada

---

## 📋 COMPARAÇÃO DETALHADA POR ETAPA

### ETAPA 1 — RADAR MACRO

#### ✅ O QUE JÁ EXISTE:
```python
# Arquivo: alpha_v4_otimizado.py - Linha 125
# Prompt atual (simplificado):
prompt = f"""Você é um analista sênior de investimentos focado em valorização de preço no mercado brasileiro (B3).
Data de hoje: {data_hoje}

Responda em JSON com o seguinte formato:
{{
  "cenario_macro": {{
    "resumo": "Resumo do cenário atual em 3-4 linhas",
    "taxa_selic": "valor atual e tendência",
    "dolar": "patamar atual e impacto nas ações",
    "setores_acelerando": ["setor1", "setor2", "setor3"],
    "setores_evitar": ["setor1", "setor2"],
    ...
  }}
}}"""
```

**Características**:
- ✅ Cache de 24h implementado
- ✅ Análise de setores
- ✅ Megatendências básicas
- ⚠️ Prompt genérico (não pede análise profunda)

#### ❌ O QUE FALTA (Metodologia Proposta):
```
Prompt muito mais profundo:
- "Não traga manchetes — foque no que ainda não está no radar do varejo"
- "narrativa_institucional": "O que fundos estão comprando que o varejo ainda não percebeu"
- "armadilhas_momento": ["Onde o investidor comum está comprando euforia"]
- "paralelo_historico": "ex: Nvidia 2022, ouro 2018"
- "resumo_executivo": "4-5 linhas do que o analista FARIA agora — ação, não descrição"
```

**GAP**: Prompt precisa ser **muito mais específico e profundo**

---

### ETAPA 2 — TRIAGEM CSV

#### ✅ O QUE JÁ EXISTE:
```python
# Arquivo: alpha_v4_otimizado.py - Linha 201
def _filtro_rapido(self, limite: int) -> List[str]:
    """Filtro rápido por fundamentos"""
    df = pd.read_csv("data/stocks.csv")
    
    # Filtros básicos
    df = df[df['roe'] > 0.10]  # ROE > 10%
    df = df[df['pl'] > 0]
    df = df[df['pl'] < 20]
    ...
```

**Características**:
- ✅ Filtro por fundamentos (ROE, P/L, etc)
- ✅ Processa CSV completo
- ❌ Não usa contexto macro
- ❌ Não separa perfis A/B

#### ❌ O QUE FALTA (Metodologia Proposta):

**1. Perfis Operacionais Separados**:
```
PERFIL A — MOMENTUM RÁPIDO (2 a 15 dias):
ROE > 12% | P/L < 15 | ROIC > 10% | Dívida/EBITDA < 3,0 
Margem EBITDA > 10% | Setor com catalisador no macro

PERFIL B — POSIÇÃO CONSISTENTE (1 a 3 meses):
ROE > 15% | CAGR Receita > 8% | CAGR Lucro > 10%
Dívida/EBITDA < 2,5 | Margem Líquida > 8%
```

**2. Eliminação Imediata Rigorosa**:
```
Dívida/EBITDA > 4,0 | ROE negativo | CAGR Receita negativo
Setor "a evitar" no macro | Liquidez Corrente < 0,7
```

**3. Prompt com Contexto Macro**:
```
[COLE O BLOCO DE CONTEXTO DA ETAPA 1]

Você é analista de ações da B3 focado em valorização de preço.
Meta: 5% ao mês, operações de 2 dias a 3 meses.

[Usa contexto macro para filtrar empresas alinhadas]
```

**4. Output Detalhado**:
```json
{
  "acoes_selecionadas": [
    {
      "ticker": "XXXX3",
      "perfil": "A/B/A+B",
      "motivo_selecao": "o que nos dados chama atenção — seja preciso",
      "catalisador_provavel": "o que pode mover o preço",
      "risco_principal": "o que pode derrubar a tese"
    }
  ],
  "principais_motivos_descarte": "padrões que eliminaram a maioria",
  "observacao_do_analista": "o que o conjunto de dados revela sobre o mercado hoje"
}
```

**GAP**: 
- ❌ Filtro não usa contexto macro
- ❌ Não separa perfis A/B
- ❌ Não envia CSV para IA analisar (faz filtro local)
- ❌ Não retorna motivos de seleção/descarte

---

### ETAPA 3 — ANÁLISE DO RELEASE

#### ✅ O QUE JÁ EXISTE:
```python
# Arquivo: alpha_v4_otimizado.py - Linha 287
prompt = f"""[CONTEXTO MACRO E TRIAGEM]
Cenário macro: {contexto_resumo}
Empresa selecionada na triagem: {ticker}
Preço atual na bolsa: R$ {preco:.2f}
...

Analisar o lançamento de resultados abaixo da empresa {ticker}.

Avalie os seguintes pontos:
1. SAÚDE FINANCEIRA REAL
2. QUALIDADE DA GESTÃO
3. CATALISADORES DE VALORIZAÇÃO
4. RISCOS CONCRETOS
5. VALORIZAÇÃO
6. NOTA DE RECOMENDAÇÃO (0 a 10)
"""
```

**Características**:
- ✅ Análise com release
- ✅ Preço atual incluído
- ✅ Contexto macro resumido
- ✅ Nota 0-10
- ⚠️ Prompt bom, mas pode ser mais profundo

#### ⚠️ O QUE PODE MELHORAR (Metodologia Proposta):

**1. Prompt Mais Específico**:
```
Analise com precisão — sem generalismos:
1. SAÚDE FINANCEIRA: geração de caixa, tendência de margens, 
   qualidade do lucro (caixa real ou contábil?)
2. GESTÃO: execução, alocação de capital (CAPEX, recompras, M&A), 
   transparência com o acionista
3. CATALISADORES: o que especificamente pode fazer subir em 1-6 meses? 
   (contratos, expansão, ciclo, margem)
4. RISCOS REAIS: não os genéricos do release — os concretos DESTA 
   empresa que podem derrubar o preço
5. VALUATION: com preço de R${PRECO_ATUAL}, está cara/justa/barata? 
   Calcule preço teto e upside %
6. NOTA: 0-10. Abaixo de 6 = DESCARTAR. 6-7 = MONITORAR. 8-10 = COMPRA.
```

**2. Output Mais Estruturado**:
```json
{
  "saude_financeira": {
    "geracao_caixa": "",
    "tendencia_margens": "",
    "endividamento": "",
    "qualidade_lucro": ""
  },
  "catalisadores": [
    {
      "descricao": "",
      "prazo": "semanas/meses",
      "impacto": "alto/médio/baixo"
    }
  ],
  "riscos_reais": [
    {
      "descricao": "",
      "probabilidade": "alta/média/baixa",
      "impacto": "alto/médio/baixo"
    }
  ],
  "valuation": {
    "situacao": "cara/justa/barata",
    "preco_teto_estimado": 0.00,
    "upside_potencial_pct": 0.0,
    "justificativa": ""
  },
  "ponto_critico": "o único fator que mudaria sua opinião sobre essa ação"
}
```

**3. Critério de Corte Rigoroso**:
```
Nota < 6 na Etapa 3 = empresa descartada, não avança
```

**GAP**: 
- ⚠️ Prompt pode ser mais específico
- ⚠️ Output pode ser mais estruturado
- ⚠️ Falta "ponto_critico" no output

---

### ETAPA 4 — ESTRATÉGIA OPERACIONAL

#### ❌ O QUE NÃO EXISTE:

O sistema atual **NÃO implementa a Etapa 4** no fluxo principal (`alpha_v4_otimizado.py`).

Existe uma implementação separada em `alpha_system_v4_professional.py` (Passo 5), mas não é usada no fluxo automático.

#### ❌ O QUE FALTA (Metodologia Proposta):

**Prompt Completo de Estratégia**:
```
[COLE O BLOCO DE CONTEXTO COMPLETO — MACRO + TRIAGEM + RELEASES]

Você é estrategista de operações de curto e médio prazo na B3. Meta: 5% ao mês.

APROVADAS com preços ATUAIS:
- {TICKER1} | Nota {X}/10 | Preço ATUAL: R${PRECO} | Perfil: {A/B}

Para cada ação, monte:
1. ENTRADA: pode entrar agora ou aguardar? Se aguardar, qual preço e qual gatilho?
2. ALVOS: alvo conservador e otimista (R$) | critério de saída antecipada
3. STOP: preço exato e justificativa do nível
4. R/R: calcule (Alvo - Entrada) / (Entrada - Stop). Se < 2,0, descarte ou ajuste.
5. TEMPO: dias/semanas estimados | o que pode acelerar ou atrasar a tese
6. ALOCAÇÃO: % do portfólio sugerido | convicção: Alta/Média/Baixa
7. ANTI-MANADA: já é manchete? Sustentado por fundamento ou euforia?
```

**Output Esperado**:
```json
{
  "estrategias": [
    {
      "ticker": "",
      "tipo_operacao": "Swing Trade / Position Trade",
      "entrada": {
        "pode_entrar_agora": true,
        "preco_ideal": 0.00,
        "gatilho": ""
      },
      "alvos": {
        "conservador": 0.00,
        "otimista": 0.00,
        "upside_conservador_pct": 0.0,
        "saida_antecipada": ""
      },
      "stop": {
        "preco": 0.00,
        "perda_pct": 0.0,
        "justificativa": ""
      },
      "risco_retorno": 0.0,
      "tempo_estimado": "",
      "alocacao_pct": 0.0,
      "convicao": "Alta/Média/Baixa",
      "anti_manada": {
        "ja_e_manchete": false,
        "sustentado_por_fundamento": true,
        "conclusao": ""
      }
    }
  ],
  "ranking": [
    {
      "posicao": 1,
      "ticker": "",
      "justificativa": "2 linhas — por que é a melhor entrada agora"
    }
  ],
  "carteira": {
    "total_alocado_pct": 0.0,
    "caixa_reserva_pct": 0.0,
    "observacao": ""
  }
}
```

**Regra Crítica**:
```
Só execute operações com R/R ≥ 2,0
```

**GAP**: 
- ❌ Etapa 4 não implementada no fluxo principal
- ❌ Falta análise de entrada/saída/stop
- ❌ Falta cálculo de R/R
- ❌ Falta análise anti-manada

---

### ETAPA 5 — REVISÃO MENSAL

#### ❌ O QUE NÃO EXISTE:

O sistema atual **NÃO implementa a Etapa 5**.

#### ❌ O QUE FALTA (Metodologia Proposta):

**Prompt de Revisão**:
```
[COLE O BLOCO DE CONTEXTO COM O CENÁRIO MAIS RECENTE]

Você é analista de carteiras na B3. Revise as posições abaixo sem apego.
Critério único: a carteira deve ter as melhores oportunidades de agora, 
não defender o que foi comprado.

CARTEIRA ATUAL:
- {TICKER1} | PM: R${PM} | Atual: R${PA} | Resultado: {+/-X%} | % carteira: {X%}

Para cada posição: a tese original ainda vale? O upside ainda existe? 
Há algo melhor para esse capital agora?
```

**Output Esperado**:
```json
{
  "analise_posicoes": [
    {
      "ticker": "",
      "resultado_pct": 0.0,
      "tese_valida": true,
      "upside_restante": "alto/médio/baixo/nenhum",
      "acao": "MANTER / AUMENTAR / REDUZIR PARCIAL / VENDER TUDO",
      "justificativa": "2-3 linhas diretas"
    }
  ],
  "parecer_geral": {
    "cortar": [],
    "manter": [],
    "aumentar": [],
    "oportunidade_faltando": "existe algo melhor para esse capital?",
    "saude_carteira": "resumo honesto em 3-4 linhas"
  }
}
```

**GAP**: 
- ❌ Etapa 5 não implementada
- ❌ Falta sistema de revisão de carteira
- ❌ Falta análise de "manter vs vender"

---

## 🔑 PROBLEMA CRÍTICO: BLOCO DE CONTEXTO MANUAL

### ❌ O QUE NÃO EXISTE:

O sistema atual **NÃO implementa o bloco de contexto manual** para persistir informações entre sessões do Groq.

### Por que isso é crítico?

**Problema identificado na metodologia**:
> "Perda de contexto ao trocar de conta no Groq — o modelo recomeça do zero, gerando análises incoerentes sem base de referência."

### ❌ O QUE FALTA:

**1. Template do Bloco de Contexto**:
```
[===== CONTEXTO DO DIA =====]
DATA: DD/MM/AAAA
MACRO: Selic XX%, Dólar R$XX, Setores quentes: [X,Y], Evitar: [Z], Alerta: [descreva]
AÇÕES SELECIONADAS (Etapa 2):
- TICK1 | R$XX | ROE XX% | P/L XX | Perfil A/B | Motivo: [resumo]
RELEASES ANALISADOS (Etapa 3):
- TICK1: Nota X/10 | COMPRA/MONITORAR | Tese: [resumo]
[===== FIM DO CONTEXTO =====]
```

**2. Sistema de Gestão de Contexto**:
- Salvar contexto após cada etapa
- Carregar contexto antes de cada prompt
- Atualizar contexto incrementalmente
- Persistir em arquivo texto

**3. Regra de Uso**:
```
Regra: nunca envie um prompt avançado sem o contexto das etapas anteriores.
```

**GAP**: 
- ❌ Não existe sistema de contexto persistente
- ❌ Cada prompt é independente
- ❌ Contexto macro é resumido (não completo)
- ❌ Não há "memória" entre etapas

---

## 📊 RESUMO DOS GAPS

### 🔴 CRÍTICO (Não Implementado):

1. **Bloco de Contexto Manual**
   - Sistema de persistência de contexto entre etapas
   - Template de contexto estruturado
   - Gestão de contexto incremental

2. **Etapa 4 — Estratégia Operacional**
   - Análise de entrada/saída/stop
   - Cálculo de R/R (Risk/Reward)
   - Análise anti-manada
   - Perfis de operação (Swing vs Position)

3. **Etapa 5 — Revisão Mensal**
   - Sistema de revisão de carteira
   - Análise de manter vs vender
   - Comparação com novas oportunidades

4. **Perfis Operacionais (A/B)**
   - Separação clara entre Perfil A (momentum) e B (position)
   - Critérios específicos para cada perfil
   - Estratégias diferentes por perfil

### 🟡 IMPORTANTE (Parcialmente Implementado):

5. **Etapa 2 — Triagem com IA**
   - Enviar CSV completo para IA analisar (não filtro local)
   - Usar contexto macro na triagem
   - Retornar motivos de seleção/descarte

6. **Prompts Mais Profundos**
   - Etapa 1: Adicionar narrativa institucional, armadilhas, paralelos históricos
   - Etapa 3: Estruturar melhor output (saúde financeira, catalisadores, riscos)

7. **Critérios de Eliminação Rigorosos**
   - Nota < 6 = descarte automático
   - R/R < 2,0 = operação não executada
   - Eliminação imediata por fundamentos ruins

### 🟢 BOM (Já Implementado):

8. **Estrutura em 5 Etapas** ✅
9. **Cache de Análise Macro (24h)** ✅
10. **Análise com Release** ✅
11. **Preço Atual em Cada Etapa** ✅
12. **Sistema de Ranking** ✅

---

## 🎯 PLANO DE IMPLEMENTAÇÃO SUGERIDO

### FASE 1 — FUNDAÇÃO (Crítico)
**Prioridade**: 🔴 ALTA

1. **Implementar Bloco de Contexto Manual**
   - Criar `ContextManager` class
   - Template de contexto estruturado
   - Salvar/carregar contexto entre etapas
   - Arquivo: `app/services/context_manager.py`

2. **Separar Perfis A/B na Etapa 2**
   - Critérios específicos para cada perfil
   - Filtro separado por perfil
   - Tag de perfil no output

### FASE 2 — ESTRATÉGIA (Crítico)
**Prioridade**: 🔴 ALTA

3. **Implementar Etapa 4 — Estratégia Operacional**
   - Prompt completo de estratégia
   - Cálculo de R/R
   - Análise de entrada/saída/stop
   - Análise anti-manada
   - Integrar no fluxo principal

### FASE 3 — APROFUNDAMENTO (Importante)
**Prioridade**: 🟡 MÉDIA

4. **Aprofundar Prompts**
   - Etapa 1: Adicionar narrativa institucional, armadilhas
   - Etapa 2: Enviar CSV para IA (não filtro local)
   - Etapa 3: Estruturar melhor output

5. **Critérios de Eliminação Rigorosos**
   - Implementar descarte automático (nota < 6)
   - Validar R/R antes de executar operação
   - Eliminação imediata por fundamentos

### FASE 4 — REVISÃO (Importante)
**Prioridade**: 🟡 MÉDIA

6. **Implementar Etapa 5 — Revisão Mensal**
   - Sistema de carteira ativa
   - Análise de manter vs vender
   - Comparação com novas oportunidades

---

## 📝 ARQUIVOS A CRIAR/MODIFICAR

### Novos Arquivos:

1. `app/services/context_manager.py`
   - Classe `ContextManager`
   - Métodos: `salvar_contexto()`, `carregar_contexto()`, `atualizar_contexto()`

2. `app/services/estrategia_operacional.py`
   - Classe `EstrategiaOperacional`
   - Implementa Etapa 4 completa

3. `app/services/revisao_carteira.py`
   - Classe `RevisaoCarteira`
   - Implementa Etapa 5 completa

4. `data/contexto_atual.txt`
   - Arquivo de texto com contexto persistente

### Arquivos a Modificar:

1. `app/services/alpha_v4_otimizado.py`
   - Integrar `ContextManager`
   - Aprofundar prompts
   - Adicionar perfis A/B
   - Integrar Etapa 4

2. `app/routes/admin.py`
   - Endpoint para Etapa 4
   - Endpoint para Etapa 5
   - Endpoint para visualizar contexto

---

## ✅ CONCLUSÃO

O sistema atual tem uma **base sólida** com as 5 etapas estruturadas, mas precisa de:

1. **Bloco de Contexto Manual** (CRÍTICO)
2. **Etapa 4 — Estratégia** (CRÍTICO)
3. **Perfis A/B** (IMPORTANTE)
4. **Prompts Mais Profundos** (IMPORTANTE)
5. **Etapa 5 — Revisão** (IMPORTANTE)

Com essas implementações, o sistema atingirá o nível da metodologia proposta: análise profissional, rigorosa e com gestão de contexto entre sessões.

---

**Próximo Passo**: Escolher qual fase implementar primeiro (recomendo Fase 1 — Fundação).
