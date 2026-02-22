# 📝 PROMPTS ENVIADOS PARA O GROQ

## Todos os prompts que o sistema envia para o modelo Llama 3.1 405B

---

## PROMPT 1: ANÁLISE MACRO (MEGATENDÊNCIAS) 🌍

**Frequência**: 1x a cada 24 horas (cache)  
**Objetivo**: Identificar tendências globais para investimentos

### Prompt Enviado:

```
Identifique rapidamente as 3 principais megatendências para investimentos em 2026:
1. Nome da tendência
2. Setores beneficiados
3. Timing (curto/médio/longo prazo)

Retorne JSON: {"megatendencias": [...], "resumo_executivo": "..."}
```

### Exemplo de Resposta:

```json
{
  "megatendencias": [
    {
      "nome": "Inteligência Artificial Aplicada",
      "setores": ["Tecnologia", "Saúde", "Finanças"],
      "timing": "curto prazo"
    },
    {
      "nome": "Transição Energética",
      "setores": ["Energia Renovável", "Utilities", "Infraestrutura"],
      "timing": "médio prazo"
    },
    {
      "nome": "Envelhecimento Populacional",
      "setores": ["Saúde", "Farmacêutico", "Seguros"],
      "timing": "longo prazo"
    }
  ],
  "resumo_executivo": "As megatendências de 2026 estão relacionadas à transição energética, digitalização e mudanças demográficas..."
}
```

---

## PROMPT 2: ANÁLISE INDIVIDUAL DE EMPRESA 🏢

**Frequência**: 1x por empresa (15 empresas por análise)  
**Objetivo**: Avaliar cada empresa e dar nota + recomendação

### Prompt Enviado (Exemplo com CTKA4):

```
Analise CTKA4 rapidamente:
ROE: 39.0%, P/L: 14.43, Preço: R$ 47.25
Release: Não
Contexto: As megatendências de 2026 estão relacionadas à transição energética, digitalização...

Retorne JSON:
{
  "ticker": "CTKA4",
  "score": 7.5,
  "recomendacao": "COMPRA|MANTER|VENDA",
  "preco_teto": 56.70,
  "upside": 20.0,
  "tese": "Breve análise"
}
```

### Exemplo de Resposta:

```json
{
  "ticker": "CTKA4",
  "score": 7.5,
  "recomendacao": "COMPRA",
  "preco_teto": 56.70,
  "upside": 20.0,
  "tese": "Empresa com ROE alto de 39%, indicando boa rentabilidade. P/L de 14.43 está abaixo da média do setor, sugerindo subvalorização. Setor de construção se beneficia de infraestrutura e crescimento econômico. Potencial de valorização de 20% até o preço teto."
}
```

---

## PROMPT 2B: ANÁLISE COM RELEASE 📄

**Quando**: Se a empresa tiver relatório trimestral disponível

### Prompt Enviado (Exemplo com BBSE3 + Release):

```
Analise BBSE3 rapidamente:
ROE: 25.0%, P/L: 12.50, Preço: R$ 34.05
Release: Sim
Contexto: As megatendências de 2026 estão relacionadas à transição energética, digitalização...

RELEASE DISPONÍVEL:
[Conteúdo do relatório trimestral da empresa]

Retorne JSON:
{
  "ticker": "BBSE3",
  "score": 8.5,
  "recomendacao": "COMPRA|MANTER|VENDA",
  "preco_teto": 40.86,
  "upside": 20.0,
  "tese": "Análise considerando o release"
}
```

### Exemplo de Resposta:

```json
{
  "ticker": "BBSE3",
  "score": 9.0,
  "recomendacao": "COMPRA",
  "preco_teto": 40.86,
  "upside": 20.0,
  "tese": "Empresa apresenta ROE de 25% com crescimento consistente. Segundo o release trimestral, houve aumento de 15% na receita e 20% no lucro líquido. Margem operacional melhorou de 18% para 22%. Setor de seguros se beneficia de digitalização e crescimento da classe média. P/L de 12.5x está atrativo comparado à média do setor (15x). Catalisadores: expansão digital, aumento de prêmios, eficiência operacional."
}
```

---

## 📊 ESTRUTURA COMPLETA DOS PROMPTS

### Variáveis Usadas:

```python
# Para cada empresa:
ticker = "CTKA4"           # Código da ação
roe = 39.0                 # Return on Equity (%)
pl = 14.43                 # Preço/Lucro
preco = 47.25              # Preço atual (R$)
setor = "Construção"       # Setor da empresa
release = True/False       # Tem relatório?
contexto = "..."           # Megatendências

# Prompt montado dinamicamente:
prompt = f"""Analise {ticker} rapidamente:
ROE: {roe:.1f}%, P/L: {pl:.2f}, Preço: R$ {preco:.2f}
Release: {"Sim" if release else "Não"}
Contexto: {contexto[:100]}

Retorne JSON:
{{
  "ticker": "{ticker}",
  "score": 7.5,
  "recomendacao": "COMPRA|MANTER|VENDA",
  "preco_teto": {preco * 1.2:.2f},
  "upside": 20.0,
  "tese": "Breve análise"
}}"""
```

---

## 🎯 CARACTERÍSTICAS DOS PROMPTS

### 1. **Simplicidade**
- ✅ Prompts curtos e diretos
- ✅ Informações essenciais
- ✅ Formato JSON estruturado

### 2. **Contexto**
- ✅ Inclui megatendências
- ✅ Dados fundamentalistas (ROE, P/L)
- ✅ Preço atual
- ✅ Release (se disponível)

### 3. **Formato de Resposta**
- ✅ JSON estruturado
- ✅ Campos obrigatórios
- ✅ Fácil de processar
- ✅ Consistente

---

## 🔄 FLUXO COMPLETO

```
1. PROMPT MACRO (1x a cada 24h)
   ↓
   Resposta: Megatendências

2. FILTRO CSV (sem prompt)
   ↓
   15 empresas selecionadas

3. BUSCA PREÇOS (sem prompt)
   ↓
   Preços atuais

4. PROMPT INDIVIDUAL (15x)
   ↓
   Para cada empresa:
   - Monta prompt com dados
   - Envia para Groq (405B)
   - Recebe análise JSON
   - Processa resposta
   ↓
   15 análises completas

5. RANKING (sem prompt)
   ↓
   Ordena por score
```

---

## 💡 POR QUE PROMPTS SIMPLES?

### Vantagens:

1. **Velocidade**
   - Prompts curtos = respostas mais rápidas
   - Menos tokens = menos processamento

2. **Consistência**
   - Formato fixo = respostas previsíveis
   - JSON estruturado = fácil de processar

3. **Eficiência**
   - Informações essenciais
   - Sem "fluff" desnecessário
   - Direto ao ponto

4. **Qualidade**
   - Modelo 405B é inteligente
   - Não precisa de prompts longos
   - Entende contexto implícito

---

## 🚀 COM MODELO 405B

### O que muda:

**Mesmos prompts**, mas:
- ✅ Respostas mais profundas
- ✅ Teses mais elaboradas
- ✅ Scores mais precisos
- ✅ Análise mais rigorosa

### Exemplo de diferença:

**70B**:
```
"tese": "Empresa com ROE alto e P/L atrativo."
```

**405B**:
```
"tese": "Empresa apresenta ROE de 39% sustentado por margem 
operacional de 25% e ROIC de 18%, indicando vantagem competitiva. 
P/L de 14.4x está 30% abaixo da média do setor (20x), sugerindo 
subvalorização. Catalisadores: (1) Expansão regional, (2) Redução 
de dívida, (3) Alinhamento com infraestrutura. Riscos: Exposição 
a juros e ciclo econômico."
```

---

## 📝 RESUMO

### Prompts Enviados:

1. **Análise Macro**: 1x a cada 24h
2. **Análise Individual**: 15x por análise completa

### Total por Análise Completa:
- **1 prompt macro** (se cache expirou)
- **15 prompts individuais**
- **Total**: 15-16 prompts

### Frequência:
- **A cada 1 hora** (automático)
- **~360 prompts por dia** (24 análises × 15 empresas)

### Custo:
- **GRATUITO** (Groq)
- **6 chaves** em rotação
- **Rate limit respeitado**

---

## ✅ CONCLUSÃO

Os prompts são **simples e eficientes**:
- ✅ Curtos e diretos
- ✅ Informações essenciais
- ✅ Formato JSON estruturado
- ✅ Contexto relevante

Com o **modelo 405B**, as respostas ficam **muito melhores** mesmo com prompts simples!

**Não precisa mudar os prompts - o modelo 405B já entrega qualidade superior!** 🚀
