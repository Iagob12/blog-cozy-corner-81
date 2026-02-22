# Correção: Sistema Agora Usa CSV do Admin

## 🎯 Problema Resolvido

**ANTES**: Sistema ignorava CSV do admin e sempre baixava novo CSV
**AGORA**: Sistema usa CSV do admin como prioridade

---

## 🔧 Como Funciona Agora

### Prioridade de CSV

O Alpha System V3 agora segue esta ordem:

```
1. CSV do Admin (data/stocks.csv)
   ✓ Se existe
   ✓ Se idade < 48 horas
   → USA ESTE

2. Baixa Novo CSV (investimentos.com.br)
   ✓ Se CSV do admin não existe
   ✓ Ou se CSV do admin > 48 horas
   → BAIXA NOVO
```

---

## 📋 Fluxo Completo

### 1. Você Faz Upload do CSV
```
1. Acessa http://localhost:8081/admin
2. Faz login (senha: admin)
3. Faz upload do CSV atualizado
4. Sistema salva em: data/stocks.csv
```

### 2. Sistema Valida o CSV
```
✓ Colunas obrigatórias: ticker, roe, pl
✓ Coluna opcional: cagr (auto-adiciona se não existir)
✓ Mínimo: 30 ações (reduzido de 50)
✓ Normaliza nomes das colunas
```

### 3. Você Inicia Análise
```
1. Clica em "Iniciar Análise" no admin
2. Sistema verifica CSV disponível:
   
   SE data/stocks.csv existe E idade < 48h:
      ✓ USA CSV DO ADMIN
      ✓ Log: "Usando CSV do admin: 20/02/2026 14:30 (2.5h)"
   
   SENÃO:
      ⚠ Baixa novo CSV de investimentos.com.br
      ⚠ Log: "CSV do admin muito antigo (50h), baixando novo"
```

### 4. Sistema Processa
```
✓ Lê CSV (do admin ou baixado)
✓ Envia TODAS as ações para IA
✓ Sistema Híbrido coleta dados
✓ Gera ranking final
```

---

## 📊 Logs de Exemplo

### Usando CSV do Admin (Sucesso)
```
[CSV] Verificando CSV disponível
[CSV] ✓ Usando CSV do admin: 20/02/2026 14:30 (2.5h)
[CSV] ✓ CSV validado: 20/02/2026 14:30
```

### CSV do Admin Muito Antigo
```
[CSV] Verificando CSV disponível
[CSV] ⚠ CSV do admin muito antigo (50.2h), baixando novo
[CSV] Baixando CSV de investimentos.com.br
[CSV] ✓ CSV validado: 20/02/2026 16:45
```

### CSV do Admin Não Existe
```
[CSV] Verificando CSV disponível
[CSV] Baixando CSV de investimentos.com.br
[CSV] ✓ CSV validado: 20/02/2026 16:45
```

---

## ✅ Garantias

### 1. Seu CSV Sempre Tem Prioridade
- Se você fez upload < 48h atrás
- Sistema usa SEU CSV
- Não baixa novo

### 2. Validação Automática
- Colunas normalizadas
- CAGR auto-adicionado se faltar
- Mínimo 30 ações (flexível)

### 3. Backup Automático
- Antes de substituir CSV
- Mantém últimos 10 backups
- Em: `data/backups/`

### 4. Logs Completos
- Histórico de uploads
- Em: `data/csv_updates.log`
- Visível no painel admin

---

## 🔍 Como Verificar

### 1. Veja os Logs do Backend
Quando você clicar em "Iniciar Análise", veja os logs:

```bash
# Se usar CSV do admin:
[CSV] ✓ Usando CSV do admin: 20/02/2026 14:30 (2.5h)

# Se baixar novo:
[CSV] Baixando CSV de investimentos.com.br
```

### 2. Verifique o Arquivo
```bash
# Windows
dir blog-cozy-corner-81\backend\data\stocks.csv

# Veja data de modificação
# Se for recente (< 48h), sistema vai usar
```

### 3. Painel Admin
- Mostra idade do CSV
- "Atualizado" = verde (< 24h)
- "Desatualizado" = amarelo (> 24h)

---

## 📝 Formato do CSV

### Colunas Obrigatórias
```csv
ticker,roe,pl
PRIO3,35.2,8.5
VALE3,22.1,3.8
PETR4,18.5,4.2
```

### Colunas Opcionais (Recomendadas)
```csv
ticker,nome,setor,roe,cagr,pl
PRIO3,PRIO,Energia,35.2,18.5,8.5
VALE3,VALE,Mineração,22.1,11.5,3.8
PETR4,PETROBRAS,Energia,18.5,12.8,4.2
```

### Variações Aceitas
O sistema aceita várias variações de nomes:

**ticker**: ticker, Ticker, código, codigo, ação, acao, papel
**roe**: roe, ROE, Return on Equity
**pl**: pl, PL, P/L, preço/lucro, preco/lucro
**cagr**: cagr, CAGR, crescimento, Cresc. Receitas 5 Anos
**setor**: setor, Setor, sector, segmento
**nome**: nome, Nome, empresa, razão social

---

## 🚀 Teste Rápido

### 1. Faça Upload de um CSV
```
1. Acesse /admin
2. Faça upload do CSV
3. Veja mensagem: "CSV atualizado com sucesso! 200 ações carregadas"
```

### 2. Inicie Análise
```
1. Clique em "Iniciar Análise"
2. Veja logs do backend
3. Deve aparecer: "Usando CSV do admin"
```

### 3. Confirme nos Logs
```
Backend deve mostrar:
[CSV] ✓ Usando CSV do admin: 20/02/2026 14:30 (2.5h)
[PROMPT_2] CSV carregado: 200 ações
[PROMPT_2] Enviando 200 ações para análise
```

---

## ⚠️ Troubleshooting

### Sistema Ainda Baixa CSV Novo

**Causa 1**: CSV do admin > 48h
```
Solução: Faça upload de CSV novo no admin
```

**Causa 2**: CSV do admin não existe
```
Solução: Faça upload do CSV pela primeira vez
```

**Causa 3**: CSV do admin com erro
```
Solução: Verifique formato do CSV
- Colunas obrigatórias: ticker, roe, pl
- Mínimo: 30 ações
```

### Como Forçar Uso do CSV do Admin

Se você quer que o sistema SEMPRE use o CSV do admin (mesmo > 48h):

```python
# Em alpha_system_v3.py, linha ~160
# Mude de:
if idade_horas < 48:

# Para:
if idade_horas < 720:  # 30 dias
```

---

## 📈 Benefícios

### 1. Controle Total
- Você decide quais ações analisar
- Atualiza quando quiser
- Não depende de scraping

### 2. Dados Confiáveis
- Você valida os dados antes
- Sabe exatamente o que está sendo analisado
- Sem surpresas

### 3. Performance
- Não precisa baixar CSV toda vez
- Análise mais rápida
- Menos requisições externas

### 4. Flexibilidade
- Pode adicionar colunas customizadas
- Filtrar ações específicas
- Testar diferentes cenários

---

**Status**: ✅ Correção implementada e testada
**Prioridade**: CSV do admin sempre tem prioridade (se < 48h)
**Fallback**: Baixa novo CSV se necessário
