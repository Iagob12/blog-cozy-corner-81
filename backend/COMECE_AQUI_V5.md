# 🚀 COMECE AQUI — ALPHA SYSTEM V5

**Sistema completo implementado!** Siga estes passos para começar.

---

## ✅ PRÉ-REQUISITOS

1. **CSV com empresas**: `data/stocks.csv` (já deve existir)
2. **Chaves Groq**: Configuradas no `.env` (já deve estar)
3. **Python 3.8+**: Com dependências instaladas

---

## 🎯 USO RÁPIDO (3 COMANDOS)

### 1️⃣ Análise Completa (Etapas 1-4)

```bash
cd backend
python rodar_alpha_v5_completo.py
```

**Tempo**: 3-5 minutos para 15 empresas

**O que faz**:
- ✅ Etapa 1: Radar Macro (tendências, setores)
- ✅ Etapa 2: Triagem CSV (perfis A/B)
- ✅ Etapa 3: Análise de Releases (nota 0-10)
- ✅ Etapa 4: Estratégia Operacional (entrada/saída/stop/R/R)

**Resultado**:
- `data/resultados/alpha_v5_latest.json` — Resultado completo
- `data/contexto/contexto_atual.txt` — Contexto persistente

### 2️⃣ Revisar Carteira (Etapa 5)

**Primeiro**: Crie `data/carteira_atual.json`

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

**Depois**: Execute revisão

```bash
python rodar_revisao_carteira.py
```

**Resultado**:
- `data/revisoes/revisao_latest.json` — Análise da carteira
- Relatório formatado no console

### 3️⃣ Ver Resultados

```bash
# Ver resultado completo
cat data/resultados/alpha_v5_latest.json

# Ver contexto persistente
cat data/contexto/contexto_atual.txt

# Ver revisão de carteira
cat data/revisoes/revisao_latest.json
```

---

## 📊 O QUE VOCÊ VAI VER

### Exemplo de Output (Etapas 1-4)

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

[FILTRO] 10/15 empresas aprovadas (nota >= 6)

[ETAPA 4] Criando estratégias para 10 empresas...

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

CARTEIRA SUGERIDA:
  Total alocado: 75.0%
  Caixa reserva: 25.0%
  Total posições: 8
```

---

## ⚙️ CONFIGURAÇÕES

Edite `rodar_alpha_v5_completo.py`:

```python
PERFIL = "A+B"              # "A" (momentum), "B" (position) ou "A+B"
LIMITE_EMPRESAS = 15        # Número de empresas para analisar
FORCAR_NOVA_MACRO = False   # True para ignorar cache de 24h
```

### Perfis Operacionais

**PERFIL A — MOMENTUM RÁPIDO (2 a 15 dias)**
- ROE > 12%, P/L < 15, ROIC > 10%
- Para operações rápidas

**PERFIL B — POSIÇÃO CONSISTENTE (1 a 3 meses)**
- ROE > 15%, CAGR > 8%, Margem > 8%
- Para operações mais longas

**PERFIL A+B — AMBOS**
- Combina os dois perfis
- Mais empresas selecionadas

---

## 🎯 CRITÉRIOS RIGOROSOS

### Eliminação Imediata (sem análise)
```
❌ Dívida/EBITDA > 4,0
❌ ROE negativo
❌ CAGR Receita negativo
❌ Liquidez Corrente < 0,7
```

### Etapa 3: Nota < 6 = Descarte
```
Nota 0-5: DESCARTADA (não avança)
Nota 6-7: MONITORAR
Nota 8-10: COMPRA
```

### Etapa 4: R/R < 2.0 = Não Executar
```
R/R < 2.0: NÃO EXECUTAR
R/R >= 2.0: EXECUTÁVEL
```

---

## 📁 ARQUIVOS GERADOS

```
data/
├── resultados/
│   └── alpha_v5_latest.json        # Resultado completo
├── contexto/
│   ├── contexto_atual.json         # Contexto persistente (JSON)
│   └── contexto_atual.txt          # Contexto formatado (TXT)
├── revisoes/
│   └── revisao_latest.json         # Última revisão de carteira
└── carteira_atual.json             # Sua carteira (você cria)
```

---

## 🔍 ESTRUTURA DO RESULTADO

### alpha_v5_latest.json

```json
{
  "success": true,
  "tempo_segundos": 245.3,
  "total_analisadas": 15,
  "total_aprovadas": 10,
  "total_executaveis": 8,
  
  "etapa_1_macro": {
    "cenario_macro": {...},
    "megatendencias": [...],
    "resumo_executivo": "..."
  },
  
  "etapa_2_triagem": {
    "acoes_selecionadas": [...]
  },
  
  "etapa_3_releases": [
    {
      "ticker": "PRIO3",
      "nota": 8.5,
      "recomendacao": "COMPRA FORTE",
      "tese_resumida": "...",
      "catalisadores": [...],
      "riscos_reais": [...]
    }
  ],
  
  "etapa_4_estrategia": {
    "estrategias": [
      {
        "ticker": "PRIO3",
        "entrada": {...},
        "alvos": {...},
        "stop": {...},
        "risco_retorno": 2.14,
        "convicao": "Alta"
      }
    ],
    "ranking": [...],
    "carteira": {...}
  }
}
```

---

## 💡 DICAS DE USO

### Rotina Diária
```bash
# 1x por dia (manhã)
python rodar_alpha_v5_completo.py
```

### Rotina Mensal
```bash
# 1x por mês
python rodar_revisao_carteira.py
```

### Forçar Nova Análise Macro
```python
# Edite rodar_alpha_v5_completo.py
FORCAR_NOVA_MACRO = True  # Ignora cache de 24h
```

### Analisar Menos Empresas (mais rápido)
```python
# Edite rodar_alpha_v5_completo.py
LIMITE_EMPRESAS = 10  # Padrão: 15
```

---

## 🚨 REGRAS DE OURO

1. ✅ **Execute Etapas 1-4 primeiro** (análise completa)
2. ✅ **Só opere com R/R >= 2.0** (proteção de capital)
3. ✅ **Respeite stops rigorosamente** (disciplina)
4. ✅ **Revise carteira mensalmente** (Etapa 5)
5. ✅ **Mantenha 20-30% em caixa** (oportunidades)

---

## 🐛 PROBLEMAS COMUNS

### "CSV não encontrado"
```bash
# Verifique que existe
ls data/stocks.csv
```

### "Erro ao buscar preços"
```bash
# Verifique token Brapi no .env
cat .env | grep BRAPI_TOKEN
```

### "Contexto macro não disponível"
```bash
# Execute análise completa primeiro
python rodar_alpha_v5_completo.py
```

### Análise muito lenta
```python
# Reduza número de empresas
LIMITE_EMPRESAS = 10  # Padrão: 15
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

Para detalhes técnicos, veja:
- `SISTEMA_V5_DOCUMENTACAO_COMPLETA.md` — Documentação técnica completa
- `GAP_ANALYSIS_SISTEMA.md` — Comparação V4 vs V5

---

## ✅ CHECKLIST RÁPIDO

Antes de começar:

- [ ] CSV existe (`data/stocks.csv`)
- [ ] Chaves Groq configuradas (`.env`)
- [ ] Dependências instaladas (`pip install -r requirements.txt`)

Para análise completa:

- [ ] Execute `python rodar_alpha_v5_completo.py`
- [ ] Aguarde 3-5 minutos
- [ ] Veja resultado em `data/resultados/alpha_v5_latest.json`

Para revisão de carteira:

- [ ] Crie `data/carteira_atual.json` com suas posições
- [ ] Execute `python rodar_revisao_carteira.py`
- [ ] Veja resultado em `data/revisoes/revisao_latest.json`

---

## 🎉 PRONTO!

O sistema está completo e pronto para uso.

**Próximos passos**:
1. Execute análise completa
2. Revise estratégias geradas
3. Execute apenas operações com R/R >= 2.0
4. Respeite stops
5. Revise carteira mensalmente

**Boa sorte com seus investimentos!** 🚀

---

**Desenvolvido por**: Kiro AI Assistant  
**Data**: 21/02/2026  
**Versão**: 5.0 — Metodologia Avançada
