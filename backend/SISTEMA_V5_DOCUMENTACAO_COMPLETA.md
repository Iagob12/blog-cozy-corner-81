# 🚀 ALPHA SYSTEM V5 — DOCUMENTAÇÃO COMPLETA

**Versão**: 5.0 — Metodologia Avançada  
**Data**: 21/02/2026  
**Status**: ✅ IMPLEMENTADO E TESTADO

---

## 📋 VISÃO GERAL

Sistema completo de análise de investimentos implementando a metodologia avançada de 5 etapas com:

- ✅ **Gestão de Contexto Persistente** — Resolve perda de contexto entre sessões do Groq
- ✅ **Perfis Operacionais A/B** — Momentum (2-15 dias) vs Position (1-3 meses)
- ✅ **Prompts Profundos** — Análise institucional, não genérica
- ✅ **Etapa 4: Estratégia Operacional** — Entrada/Saída/Stop/R/R
- ✅ **Etapa 5: Revisão de Carteira** — Sem apego, foco em oportunidades atuais
- ✅ **Critérios Rigorosos** — Nota < 6 = descarte, R/R < 2.0 = não executar

---

## 🏗️ ARQUITETURA

### Módulos Implementados

```
backend/app/services/
├── context_manager.py              # Gestão de contexto persistente
├── perfis_operacionais.py          # Perfis A/B e critérios de eliminação
├── estrategia_operacional.py       # Etapa 4: Estratégia
├── revisao_carteira.py             # Etapa 5: Revisão
└── alpha_system_v5_completo.py     # Sistema integrado (5 etapas)

backend/
├── rodar_alpha_v5_completo.py      # Script principal
└── rodar_revisao_carteira.py       # Script Etapa 5
```

### Fluxo Completo

```
1. ETAPA 1 — RADAR MACRO
   ↓ (contexto salvo)
2. ETAPA 2 — TRIAGEM CSV (Perfis A/B)
   ↓ (contexto atualizado)
3. ETAPA 3 — ANÁLISE DE RELEASES
   ↓ (contexto atualizado)
   ↓ (filtro: nota >= 6)
4. ETAPA 4 — ESTRATÉGIA OPERACIONAL
   ↓ (contexto atualizado)
   ↓ (filtro: R/R >= 2.0)
5. ETAPA 5 — REVISÃO DE CARTEIRA (mensal)
```

---

## 🎯 ETAPA 1 — RADAR MACRO

### Objetivo
Identificar tendências, setores e catalisadores que o varejo ainda não percebeu.

### Prompt Profundo
```
- Não traga manchetes — foque no que ainda não está no radar do varejo
- narrativa_institucional: O que fundos estão comprando
- armadilhas_momento: Onde o varejo está comprando euforia
- megatendencias: Com paralelos históricos (ex: Nvidia 2022)
- resumo_executivo: O que o analista FARIA agora (ação, não descrição)
```

### Cache
- Válido por 24 horas
- Arquivo: `data/cache/macro_context_v5.json`
- Forçar nova análise: `forcar_nova_macro=True`

### Output
```json
{
  "cenario_macro": {
    "selic_atual": "...",
    "dolar_patamar": "...",
    "risco_politico_fiscal": "baixo/médio/alto",
    "fluxo_estrangeiro": "..."
  },
  "setores_acelerando": [...],
  "setores_a_evitar": [...],
  "narrativa_institucional": "...",
  "armadilhas_momento": [...],
  "megatendencias": [...],
  "resumo_executivo": "..."
}
```

---

## 🎯 ETAPA 2 — TRIAGEM CSV

### Objetivo
Filtrar empresas por perfis operacionais e critérios rigorosos.

### Perfis Operacionais

#### PERFIL A — MOMENTUM RÁPIDO (2 a 15 dias)
```
ROE > 12%
P/L < 15
ROIC > 10%
Dívida/EBITDA < 3,0
Margem EBITDA > 10%
Setor com catalisador no macro
```

#### PERFIL B — POSIÇÃO CONSISTENTE (1 a 3 meses)
```
ROE > 15%
CAGR Receita > 8%
CAGR Lucro > 10%
Dívida/EBITDA < 2,5
Margem Líquida > 8%
Setor com vento a favor
```

### Eliminação Imediata (sem análise)
```
Dívida/EBITDA > 4,0
ROE negativo
CAGR Receita negativo
Setor "a evitar" no macro
Liquidez Corrente < 0,7
```

### Output
```json
{
  "acoes_selecionadas": [
    {
      "ticker": "PRIO3",
      "perfil": "A+B",
      "roe": 25.0,
      "pl": 12.5,
      "motivo_selecao": "...",
      "catalisador_provavel": "...",
      "risco_principal": "..."
    }
  ],
  "total_selecionadas": 15,
  "principais_motivos_descarte": "...",
  "observacao_do_analista": "..."
}
```

---

## 🎯 ETAPA 3 — ANÁLISE DE RELEASES

### Objetivo
Análise profunda com release de resultados (ou sem, se não disponível).

### Prompt Profundo
```
1. SAÚDE FINANCEIRA: geração de caixa, tendência de margens, 
   qualidade do lucro (caixa real ou contábil?)

2. GESTÃO: execução, alocação de capital (CAPEX, recompras, M&A), 
   transparência com o acionista

3. CATALISADORES: o que especificamente pode fazer subir em 1-6 meses?

4. RISCOS REAIS: não os genéricos — os concretos DESTA empresa

5. VALUATION: cara/justa/barata? Calcule preço teto e upside %

6. NOTA: 0-10. Abaixo de 6 = DESCARTAR
```

### Critério de Corte
```
Nota < 6.0 = DESCARTADA (não avança para Etapa 4)
```

### Output
```json
{
  "ticker": "PRIO3",
  "nota": 8.5,
  "recomendacao": "COMPRA FORTE",
  "saude_financeira": {
    "geracao_caixa": "...",
    "tendencia_margens": "...",
    "endividamento": "...",
    "qualidade_lucro": "..."
  },
  "catalisadores": [
    {
      "descricao": "...",
      "prazo": "semanas/meses",
      "impacto": "alto/médio/baixo"
    }
  ],
  "riscos_reais": [...],
  "valuation": {
    "situacao": "barata",
    "preco_teto_estimado": 55.00,
    "upside_potencial_pct": 25.0,
    "justificativa": "..."
  },
  "tese_resumida": "...",
  "ponto_critico": "..."
}
```

---

## 🎯 ETAPA 4 — ESTRATÉGIA OPERACIONAL

### Objetivo
Criar estratégia executável para empresas aprovadas (nota >= 6).

### Prompt Profundo
```
Para cada ação:
1. ENTRADA: pode entrar agora ou aguardar? Preço ideal e gatilhos
2. ALVOS: conservador e otimista (R$) + critério de saída antecipada
3. STOP: preço exato e justificativa
4. R/R: (Alvo - Entrada) / (Entrada - Stop). Se < 2,0, descarte
5. TEMPO: horizonte + aceleradores/freios
6. ALOCAÇÃO: % do portfólio + convicção
7. ANTI-MANADA: manchete? Fundamento ou euforia?
```

### Critério de Execução
```
R/R < 2.0 = NÃO EXECUTAR
```

### Output
```json
{
  "estrategias": [
    {
      "ticker": "PRIO3",
      "tipo_operacao": "Position Trade",
      "preco_atual": 48.20,
      "entrada": {
        "pode_entrar_agora": true,
        "preco_ideal": 47.50,
        "gatilho": "..."
      },
      "alvos": {
        "conservador": 55.00,
        "otimista": 60.00,
        "upside_conservador_pct": 15.8,
        "saida_antecipada": "..."
      },
      "stop": {
        "preco": 44.00,
        "perda_pct": -7.4,
        "justificativa": "..."
      },
      "risco_retorno": 2.14,
      "tempo_estimado": "2-3 meses",
      "alocacao_pct": 12.0,
      "convicao": "Alta",
      "anti_manada": {
        "ja_e_manchete": false,
        "sustentado_por_fundamento": true,
        "conclusao": "..."
      }
    }
  ],
  "ranking": [...],
  "carteira": {
    "total_alocado_pct": 75.0,
    "caixa_reserva_pct": 25.0,
    "total_posicoes": 6
  }
}
```

---

## 🎯 ETAPA 5 — REVISÃO DE CARTEIRA

### Objetivo
Revisar carteira ativa sem apego. Foco: melhores oportunidades de AGORA.

### Prompt Profundo
```
Para cada posição:
- A tese original ainda vale?
- O upside ainda existe?
- Há algo melhor para esse capital agora?

Critério único: carteira deve ter as melhores oportunidades de agora,
não defender o que foi comprado.
```

### Input
```json
{
  "posicoes": [
    {
      "ticker": "PRIO3",
      "preco_medio": 45.50,
      "preco_atual": 48.20,
      "resultado_pct": 5.9,
      "pct_carteira": 15.0,
      "data_entrada": "2026-01-15",
      "tese_original": "..."
    }
  ]
}
```

### Output
```json
{
  "analise_posicoes": [
    {
      "ticker": "PRIO3",
      "resultado_pct": 5.9,
      "tese_valida": true,
      "upside_restante": "médio",
      "acao": "MANTER",
      "justificativa": "...",
      "prioridade": "média"
    }
  ],
  "parecer_geral": {
    "cortar": ["TICK1"],
    "manter": ["PRIO3", "VALE3"],
    "aumentar": ["TICK2"],
    "oportunidade_faltando": "...",
    "saude_carteira": "...",
    "risco_atual": "médio",
    "diversificacao": "adequada"
  }
}
```

---

## 🔧 COMO USAR

### 1. Análise Completa (Etapas 1-4)

```bash
cd backend
python rodar_alpha_v5_completo.py
```

**Configurações** (edite no script):
```python
PERFIL = "A+B"              # "A", "B" ou "A+B"
LIMITE_EMPRESAS = 15        # Número de empresas
FORCAR_NOVA_MACRO = False   # True para ignorar cache
```

**Tempo estimado**: 3-5 minutos para 15 empresas

**Resultado**:
- `data/resultados/alpha_v5_latest.json` — Resultado completo
- `data/contexto/contexto_atual.json` — Contexto persistente
- `data/contexto/contexto_atual.txt` — Contexto formatado

### 2. Revisão de Carteira (Etapa 5)

**Pré-requisito**: Criar `data/carteira_atual.json`

```json
{
  "posicoes": [
    {
      "ticker": "PRIO3",
      "preco_medio": 45.50,
      "preco_atual": 48.20,
      "resultado_pct": 5.9,
      "pct_carteira": 15.0,
      "data_entrada": "2026-01-15",
      "tese_original": "Empresa de petróleo com bons fundamentos..."
    }
  ]
}
```

**Executar**:
```bash
cd backend
python rodar_revisao_carteira.py
```

**Resultado**:
- `data/revisoes/revisao_latest.json` — Resultado da revisão
- Relatório formatado no console

---

## 📊 GESTÃO DE CONTEXTO

### O Problema
> "Perda de contexto ao trocar de conta no Groq — o modelo recomeça do zero, gerando análises incoerentes sem base de referência."

### A Solução
**ContextManager** — Persiste contexto entre etapas

### Arquivos Gerados
```
data/contexto/
├── contexto_atual.json      # Contexto completo (JSON)
├── contexto_atual.txt        # Contexto formatado (TXT)
└── historico_contextos.json  # Histórico (últimos 30 dias)
```

### Formato do Contexto (TXT)
```
[===== CONTEXTO DO DIA =====]
DATA: 21/02/2026
MACRO: Selic 10.75%, Dólar R$5.45
Setores quentes: [Tecnologia, Energia, Saúde]
Evitar: [Varejo, Construção]
Narrativa Institucional: Fundos estão comprando...

AÇÕES SELECIONADAS (Etapa 2):
- PRIO3 | R$48.20 | ROE 25.0% | P/L 12.5 | Perfil A+B | ...

RELEASES ANALISADOS (Etapa 3):
- PRIO3: Nota 8.5/10 | COMPRA FORTE | ...

ESTRATÉGIAS MONTADAS (Etapa 4):
- PRIO3: Entry R$47.50 | Alvo R$55.00 | Stop R$44.00 | R/R 2.14
[===== FIM DO CONTEXTO =====]
```

### API do ContextManager
```python
from app.services.context_manager import get_context_manager

context = get_context_manager()

# Iniciar novo contexto
context.iniciar_novo_contexto()

# Atualizar etapas
context.atualizar_etapa_1_macro(resultado_macro)
context.atualizar_etapa_2_triagem(resultado_triagem)
context.adicionar_etapa_3_release(resultado_release)
context.atualizar_etapa_4_estrategias(estrategias)
context.atualizar_etapa_5_revisao(resultado_revisao)

# Obter contexto
contexto_texto = context.obter_contexto_texto()  # Para prompts
contexto_json = context.obter_contexto_json()    # Para processamento

# Obter partes específicas
macro = context.obter_macro()
triagem = context.obter_triagem()
releases = context.obter_releases()
estrategias = context.obter_estrategias()
revisao = context.obter_revisao()
```

---

## 📈 PERFIS OPERACIONAIS

### API dos Perfis
```python
from app.services.perfis_operacionais import PerfisOperacionais

# Aplicar eliminação imediata
df_filtrado, motivos = PerfisOperacionais.aplicar_eliminacao_imediata(df)

# Filtrar por perfil
df_perfil_a = PerfisOperacionais.filtrar_por_perfil(df, "A")
df_perfil_b = PerfisOperacionais.filtrar_por_perfil(df, "B")
df_ambos = PerfisOperacionais.filtrar_por_perfil(df, "A+B")

# Identificar perfil de uma empresa
perfil = PerfisOperacionais.identificar_perfil(row)  # "A", "B", "A+B" ou "NENHUM"

# Obter descrição
desc = PerfisOperacionais.obter_descricao_perfil("A")
# "MOMENTUM RÁPIDO (2 a 15 dias)"

# Obter critérios
criterios = PerfisOperacionais.obter_criterios_perfil("A")
```

---

## 🎯 VALIDAÇÕES RIGOROSAS

### Etapa 3: Nota < 6 = Descarte
```python
empresas_aprovadas = [
    r for r in resultado_releases
    if r.get('nota', 0) >= 6.0
]
```

### Etapa 4: R/R < 2.0 = Não Executar
```python
estrategias_executaveis = [
    e for e in estrategias
    if e.get('risco_retorno', 0) >= 2.0
]
```

### Cálculo de R/R
```python
entrada = 47.50
alvo_conservador = 55.00
stop = 44.00

rr = (alvo_conservador - entrada) / (entrada - stop)
# rr = (55.00 - 47.50) / (47.50 - 44.00) = 2.14 ✓
```

---

## 📁 ESTRUTURA DE ARQUIVOS

```
data/
├── stocks.csv                          # CSV com empresas
├── releases/                           # PDFs de releases
│   ├── PRIO3_Q4_2025.pdf
│   └── ...
├── cache/
│   └── macro_context_v5.json          # Cache macro (24h)
├── contexto/
│   ├── contexto_atual.json            # Contexto persistente
│   ├── contexto_atual.txt             # Contexto formatado
│   └── historico_contextos.json       # Histórico
├── resultados/
│   ├── alpha_v5_latest.json           # Último resultado
│   └── alpha_v5_20260221_153045.json  # Resultados timestamped
├── revisoes/
│   ├── revisao_latest.json            # Última revisão
│   └── revisao_20260221_160000.json   # Revisões timestamped
└── carteira_atual.json                # Carteira para revisão
```

---

## 🔍 EXEMPLO DE USO COMPLETO

### 1. Primeira Análise
```bash
cd backend
python rodar_alpha_v5_completo.py
```

**Output**:
```
ALPHA SYSTEM V5 — ANÁLISE COMPLETA
==================================================

[ETAPA 1] Radar Macro...
[ETAPA 1] ✓ Concluída

[ETAPA 2] Triagem CSV (Perfil A+B)...
[ETAPA 2] ✓ 15 empresas selecionadas

[ETAPA 3] Analisando 15 empresas...
[ETAPA 3] PRIO3: Nota 8.5/10 - COMPRA FORTE
[ETAPA 3] VALE3: Nota 7.2/10 - COMPRA
[ETAPA 3] PETR4: Nota 5.8/10 - DESCARTAR
...
[ETAPA 3] ✓ 15 análises concluídas

[FILTRO] 10/15 empresas aprovadas (nota >= 6)

[ETAPA 4] Criando estratégias para 10 empresas...
[ETAPA 4] ✓ Estratégias criadas

RESUMO EXECUTIVO
==================================================
Tempo Total: 245.3s
Empresas Analisadas: 15
Empresas Aprovadas (nota >= 6): 10
Estratégias Executáveis (R/R >= 2.0): 8

TOP 5 ESTRATÉGIAS:
  1. PRIO3  - R/R 2.14 - Upside 15.8% - Alta
  2. VALE3  - R/R 2.05 - Upside 12.5% - Alta
  3. BBDC4  - R/R 2.32 - Upside 18.2% - Média
  4. ITUB4  - R/R 2.18 - Upside 16.0% - Média
  5. WEGE3  - R/R 2.08 - Upside 14.5% - Média
```

### 2. Revisar Carteira (1 mês depois)
```bash
# Criar data/carteira_atual.json com posições atuais
python rodar_revisao_carteira.py
```

**Output**:
```
ETAPA 5 — REVISÃO DE CARTEIRA
==================================================

CARTEIRA ATUAL: 5 posições
  - PRIO3: +8.5% (20.0% da carteira)
  - VALE3: +3.2% (15.0% da carteira)
  - BBDC4: -2.1% (12.0% da carteira)
  - ITUB4: +5.8% (18.0% da carteira)
  - WEGE3: +12.3% (15.0% da carteira)

RESULTADO DA REVISÃO
==================================================

PARECER GERAL:
  Saúde da Carteira: Carteira saudável com 4/5 posições no lucro...
  Risco Atual: MÉDIO
  Diversificação: ADEQUADA

🔴 VENDER TUDO:
  - BBDC4 (Prioridade: alta)
    Tese não se confirmou, setor bancário sob pressão...

🟢 AUMENTAR POSIÇÃO:
  - WEGE3 (Prioridade: alta)
    Tese se confirmou, upside ainda alto (25%)...

✅ MANTER:
  - PRIO3 (Upside restante: médio)
  - VALE3 (Upside restante: baixo)
  - ITUB4 (Upside restante: médio)

💡 OPORTUNIDADES:
  Nova oportunidade identificada: RENT3 (Nota 8.8/10)
```

---

## 🚨 REGRAS DE OURO

1. **Etapa 1 é obrigatória toda sessão** — especialmente ao trocar de conta no Groq
2. **Nunca pule etapas** — cada filtro protege o capital
3. **Nota < 6 na Etapa 3 = empresa descartada**, não avança
4. **R/R < 2,0 na Etapa 4 = operação não executada**
5. **Sempre atualize o preço atual** antes das Etapas 3 e 4
6. **Se o JSON vier truncado**: `"Continue o JSON a partir de onde parou"`
7. **Se o JSON vier inválido**: `"Corrija o JSON anterior, estava malformado"`
8. **O Llama 3.1 405B processa o CSV completo** de 318 empresas sem problema

---

## 🎓 DIFERENÇAS: V4 vs V5

| Aspecto | V4 (Anterior) | V5 (Novo) |
|---------|---------------|-----------|
| Contexto | ❌ Não persiste | ✅ ContextManager |
| Perfis A/B | ❌ Não separados | ✅ Separados e rigorosos |
| Etapa 4 | ❌ Não implementada | ✅ Completa (R/R, stop, etc) |
| Etapa 5 | ❌ Não existe | ✅ Revisão de carteira |
| Prompts | ⚠️ Simplificados | ✅ Profundos (institucional) |
| Eliminação | ⚠️ Parcial | ✅ Rigorosa (nota < 6, R/R < 2.0) |
| Triagem | Filtro local | ✅ Com perfis e contexto macro |

---

## 📞 TROUBLESHOOTING

### Erro: "CSV não encontrado"
```bash
# Verifique que data/stocks.csv existe
ls data/stocks.csv
```

### Erro: "Contexto macro não disponível"
```bash
# Execute análise completa primeiro
python rodar_alpha_v5_completo.py
```

### Erro: "Carteira não encontrada" (Etapa 5)
```bash
# Crie data/carteira_atual.json
# Veja exemplo na seção "Como Usar"
```

### Prompts truncados
- O Groq pode truncar JSONs grandes
- Sistema já trata isso automaticamente
- Se persistir, reduza `LIMITE_EMPRESAS`

---

## ✅ CONCLUSÃO

O **Alpha System V5** implementa completamente a metodologia avançada proposta:

- ✅ Gestão de contexto persistente (resolve perda de memória)
- ✅ Perfis operacionais A/B separados
- ✅ Prompts profundos (nível institucional)
- ✅ Etapa 4: Estratégia operacional completa
- ✅ Etapa 5: Revisão de carteira sem apego
- ✅ Validações rigorosas (nota < 6, R/R < 2.0)
- ✅ Documentação completa

**Sistema pronto para uso em produção!** 🚀

---

**Desenvolvido por**: Kiro AI Assistant  
**Data**: 21/02/2026  
**Versão**: 5.0 — Metodologia Avançada
