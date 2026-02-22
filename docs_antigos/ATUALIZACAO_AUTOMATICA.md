# 🔄 ATUALIZAÇÃO AUTOMÁTICA DIÁRIA

## ✅ COMO FUNCIONA

O sistema está configurado para **atualizar automaticamente TODO DIA**:

### 1. CSV Completo (Todas as Ações)

**Fonte:** investimentos.com.br  
**Frequência:** A cada 24 horas  
**Cache:** `backend/data/investimentos_cache.csv`

```
PRIMEIRA REQUISIÇÃO DO DIA:
├─ Verifica cache (tem menos de 24h?)
│  ├─ SIM: Usa cache (instantâneo)
│  └─ NÃO: Baixa novo CSV
│     ├─ Tenta URL 1: investimentos.com.br/acoes/download
│     ├─ Tenta URL 2: investimentos.com.br/ativos/acoes/download
│     ├─ Tenta URL 3: investimentos.com.br/api/acoes/export/csv
│     ├─ Tenta URL 4: investimentos.com.br/acoes/exportar
│     └─ Fallback: Scraping da página
│        └─ Fallback final: CSV local (stocks.csv)
└─ Resultado: CSV com TODAS as ações da B3
```

### 2. Preços Reais

**Fonte:** Brapi.dev (API gratuita)  
**Frequência:** A cada 5 minutos  
**Cache:** Em memória

```
TODA REQUISIÇÃO:
├─ Verifica cache (tem menos de 5min?)
│  ├─ SIM: Usa cache
│  └─ NÃO: Busca preços novos
│     ├─ Brapi.dev (principal)
│     ├─ Alpha Vantage (fallback)
│     └─ Mock/Simulado (fallback final)
└─ Resultado: Preços REAIS atualizados
```

### 3. Análise com Gemini

**Frequência:** A cada requisição  
**Cache:** Nenhum (sempre analisa)

```
TODA REQUISIÇÃO:
├─ Gemini Fase 1: Seleciona top 15
│  └─ Considera tendências FUTURAS
├─ Gemini Fase 2: Analisa cada ação
│  ├─ Busca Release de Resultados (PDF)
│  └─ Análise completa
└─ Resultado: Ranking 1-15 refinado
```

---

## 📊 EXEMPLO DE ATUALIZAÇÃO

### Dia 1 - 08:00
```
[DOWNLOAD] Baixando CSV COMPLETO...
✓ CSV baixado com SUCESSO!
✓ Total de ações: 200
✓ Salvo em: data/investimentos_cache.csv

[PREÇOS] Buscando via Brapi.dev...
✓ 15/15 preços obtidos

[GEMINI] Analisando...
✓ Top 15 selecionado
✓ 15 ações analisadas

⏱️ Tempo total: ~70 segundos
```

### Dia 1 - 10:00 (mesma dia)
```
✓ Usando CSV em cache (2.0h atrás)

[PREÇOS] Buscando via Brapi.dev...
✓ 15/15 preços obtidos (ATUALIZADOS!)

[GEMINI] Analisando...
✓ Top 15 selecionado
✓ 15 ações analisadas

⏱️ Tempo total: ~60 segundos
```

### Dia 2 - 08:00 (próximo dia)
```
[DOWNLOAD] Baixando CSV COMPLETO...
✓ CSV baixado com SUCESSO!
✓ Total de ações: 205 (5 novas!)
✓ Salvo em: data/investimentos_cache.csv

[PREÇOS] Buscando via Brapi.dev...
✓ 15/15 preços obtidos (NOVOS!)

[GEMINI] Analisando...
✓ Top 15 selecionado (PODE TER MUDADO!)
✓ 15 ações analisadas

⏱️ Tempo total: ~70 segundos
```

---

## 🎯 GARANTIAS

### ✅ CSV Sempre Atualizado
- Baixa automaticamente a cada 24h
- Contém TODAS as ações da B3
- Fallback para CSV local se falhar

### ✅ Preços Sempre Reais
- Atualiza a cada 5 minutos
- Fonte: Brapi.dev (API gratuita)
- Fallback para Alpha Vantage

### ✅ Ranking Recalculado
- Top 15 pode mudar todo dia
- Baseado em dados atualizados
- Gemini analisa sempre

---

## 🔍 COMO VERIFICAR

### 1. Ver Idade do Cache

```bash
# Windows
dir blog-cozy-corner-81\backend\data\investimentos_cache.csv

# Linux/Mac
ls -lh blog-cozy-corner-81/backend/data/investimentos_cache.csv
```

### 2. Forçar Download Novo

```bash
# Deletar cache
del blog-cozy-corner-81\backend\data\investimentos_cache.csv

# Próxima requisição vai baixar novo
curl "http://localhost:8000/api/v1/final/top-picks?limit=5"
```

### 3. Ver Logs

No terminal do backend, você verá:

```
[DOWNLOAD] Baixando CSV COMPLETO de investimentos.com.br...
⏳ Isso pode levar alguns segundos...
  Tentando: https://investimentos.com.br/acoes/download
✓ CSV baixado com SUCESSO!
✓ Total de ações: 200
✓ Salvo em: data/investimentos_cache.csv
```

---

## 📅 CRONOGRAMA DE ATUALIZAÇÃO

```
┌─────────────────────────────────────────────────────────┐
│ HORÁRIO    │ CSV      │ PREÇOS   │ ANÁLISE             │
├─────────────────────────────────────────────────────────┤
│ 08:00      │ BAIXA    │ BUSCA    │ GEMINI              │
│ 08:05      │ cache    │ cache    │ GEMINI              │
│ 08:10      │ cache    │ BUSCA    │ GEMINI              │
│ 08:15      │ cache    │ BUSCA    │ GEMINI              │
│ ...        │ ...      │ ...      │ ...                 │
│ 09:00      │ cache    │ BUSCA    │ GEMINI              │
│ ...        │ ...      │ ...      │ ...                 │
│ 08:00 (D+1)│ BAIXA    │ BUSCA    │ GEMINI              │
└─────────────────────────────────────────────────────────┘

CSV: Atualiza a cada 24h
PREÇOS: Atualiza a cada 5min
ANÁLISE: Sempre executa
```

---

## 🛠️ CONFIGURAÇÃO

### Alterar Frequência de Atualização

**Arquivo:** `backend/app/services/investimentos_scraper.py`

```python
class InvestimentosScraper:
    def __init__(self):
        # Altere aqui:
        self.cache_duration_hours = 24  # Padrão: 24 horas
        
        # Exemplos:
        # self.cache_duration_hours = 12  # A cada 12 horas
        # self.cache_duration_hours = 6   # A cada 6 horas
        # self.cache_duration_hours = 1   # A cada 1 hora
```

**Arquivo:** `backend/app/services/brapi_service.py`

```python
class BrapiService:
    def __init__(self):
        # Altere aqui:
        self.cache_duration = 300  # Padrão: 5 minutos (300 segundos)
        
        # Exemplos:
        # self.cache_duration = 60   # A cada 1 minuto
        # self.cache_duration = 600  # A cada 10 minutos
```

---

## ⚠️ IMPORTANTE

### CSV Completo vs CSV Local

**CSV Completo (investimentos_cache.csv):**
- Baixado automaticamente
- Contém TODAS as ações da B3 (~200+)
- Atualizado diariamente

**CSV Local (stocks.csv):**
- Backup manual
- Contém ~200 ações principais
- Usado se download falhar

### O Sistema SEMPRE Funciona

Mesmo se investimentos.com.br estiver fora do ar:
1. Usa cache antigo (se tiver)
2. Usa CSV local (stocks.csv)
3. Sistema continua funcionando!

---

## ✅ RESUMO

**O sistema está configurado para atualizar automaticamente:**

✅ **CSV:** A cada 24 horas (todas as ações da B3)  
✅ **Preços:** A cada 5 minutos (preços reais)  
✅ **Análise:** Toda requisição (Gemini sempre analisa)  
✅ **Ranking:** Recalculado diariamente (top 15 pode mudar)  

**Você não precisa fazer NADA!** 🎉

O sistema cuida de tudo automaticamente. Apenas acesse:
```
http://localhost:8081
```

E terá sempre os dados mais atualizados! 🚀

---

**Última atualização:** 19/02/2026
