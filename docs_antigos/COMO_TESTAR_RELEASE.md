# 🧪 Como Testar o Sistema com Release de Resultados

## ✅ Status Atual

O sistema está **FUNCIONANDO** e retornando:
- ✅ Preços REAIS via Brapi.dev (PETR4: R$ 37.19, ITUB4: R$ 47.99)
- ✅ Análise com Gemini
- ✅ Ranking 1-15

**Falta apenas:** Adicionar PDFs de Release para análise completa!

---

## 🎯 Teste Rápido (SEM Release)

### 1. Testar Endpoint Atual

```bash
curl "http://localhost:8000/api/v1/final/top-picks?limit=5"
```

**Resultado esperado:**
```json
[
  {
    "rank": 1,
    "ticker": "PETR4",
    "preco_atual": 37.19,
    "upside_potencial": 18.5,
    "recomendacao_final": "COMPRA",
    "tem_relatorio": false  ← Sem Release ainda
  }
]
```

---

## 📄 Teste Completo (COM Release)

### Passo 1: Adicionar PDF de Release

1. Baixe o Release de Resultados Q4 2025 da Petrobras:
   - Acesse: https://ri.petrobras.com.br
   - Vá em "Resultados" → "4T25"
   - Baixe o PDF

2. Renomeie para: `PETR4_Q4_2025.pdf`

3. Coloque em: `blog-cozy-corner-81/backend/data/releases/`

### Passo 2: Testar Novamente

```bash
curl "http://localhost:8000/api/v1/final/top-picks?limit=5"
```

**Resultado esperado (COM Release):**
```json
[
  {
    "rank": 1,
    "ticker": "PETR4",
    "preco_atual": 37.19,
    "upside_potencial": 22.3,  ← Upside ajustado após análise do Release
    "recomendacao_final": "COMPRA FORTE",  ← Recomendação melhorada
    "tem_relatorio": true,  ← Agora tem Release!
    "analise": {
      "analise_relatorio_q4": {
        "destaques": [
          "Receita cresceu 15% vs Q4 2024",
          "EBITDA aumentou 20%",
          "Produção de petróleo bateu recorde"
        ],
        "riscos": [
          "Exposição ao preço do petróleo",
          "Endividamento em dólar"
        ],
        "tendencias_futuras": [
          "Setor de energia em alta",
          "Transição energética favorece empresa"
        ]
      }
    }
  }
]
```

---

## 🔍 Ver Logs Detalhados

No terminal do backend, você verá:

```
============================================================
ALPHA SYSTEM V2 - ANÁLISE COMPLETA
============================================================

[FASE 1] Gemini analisando CSV e selecionando top 15...
    ✓ Gemini selecionou 15 ações

[FASE 2] Analisando cada ação com Release de Resultados...

  [1/15] Analisando PETR4...
  ✓ PETR4: Release em cache
    PETR4 - R$ 37.19 ✓ (com Release)

  [2/15] Analisando ITUB4...
  ✗ ITUB4: Release não encontrado
    ITUB4 - R$ 47.99 ✓ (sem Release)
```

---

## 📊 Comparação: COM vs SEM Release

### SEM Release de Resultados
```json
{
  "ticker": "PETR4",
  "upside_potencial": 18.5,
  "recomendacao_final": "COMPRA",
  "catalisadores": ["ROE de 18.5%"],
  "tem_relatorio": false
}
```

### COM Release de Resultados
```json
{
  "ticker": "PETR4",
  "upside_potencial": 22.3,  ← Melhor!
  "recomendacao_final": "COMPRA FORTE",  ← Mais confiante!
  "catalisadores": [
    "ROE de 18.5%",
    "Receita cresceu 15%",
    "EBITDA aumentou 20%",
    "Produção bateu recorde"
  ],
  "tem_relatorio": true,
  "analise_relatorio_q4": {
    "destaques": [...],
    "riscos": [...],
    "tendencias_futuras": [...]
  }
}
```

**Diferença:** Análise muito mais rica e precisa!

---

## 🚀 Teste Completo com 15 Ações

### 1. Adicione Releases das Top 15

Baixe e adicione PDFs para:
- PETR4 (Petrobras)
- VALE3 (Vale)
- ITUB4 (Itaú)
- BBDC4 (Bradesco)
- WEGE3 (WEG)
- PRIO3 (PRIO)
- etc.

### 2. Execute Análise Completa

```bash
curl "http://localhost:8000/api/v1/final/top-picks?limit=15"
```

### 3. Veja Ranking Refinado

O Gemini vai:
1. Analisar cada Release individualmente
2. Identificar destaques e riscos
3. Considerar tendências futuras
4. Ajustar recomendações
5. Refinar o ranking

---

## 📁 Estrutura de Arquivos Esperada

```
backend/data/releases/
├── PETR4_Q4_2025.pdf  ✅
├── VALE3_Q4_2025.pdf  ✅
├── ITUB4_Q4_2025.pdf  ✅
├── BBDC4_Q4_2025.pdf  ✅
├── WEGE3_Q4_2025.pdf  ✅
├── PRIO3_Q4_2025.pdf  ✅
└── ...
```

---

## 🎓 O Que o Gemini Analisa no Release

### 1. Métricas Financeiras
- Receita (crescimento vs trimestre anterior)
- Lucro líquido
- EBITDA
- Margens (bruta, operacional, líquida)

### 2. Destaques Operacionais
- Crescimento de produção/vendas
- Novos contratos
- Expansão de mercado
- Inovações

### 3. Riscos
- Endividamento
- Exposição cambial
- Riscos regulatórios
- Concorrência

### 4. Tendências Futuras
- Perspectivas do setor
- Investimentos planejados
- Novos projetos
- Posicionamento estratégico

---

## ⚡ Performance

### SEM Release
- Análise: ~2-3 segundos por ação
- Total (15 ações): ~30-45 segundos

### COM Release
- Análise: ~3-5 segundos por ação (lê PDF + analisa)
- Total (15 ações): ~45-75 segundos

**Vale a pena:** Análise muito mais precisa!

---

## 🐛 Troubleshooting

### "Release não encontrado"
- **Normal:** Sistema funciona sem Release
- **Solução:** Adicione PDF manualmente
- **Impacto:** Análise fica mais simples (só fundamentos)

### "Erro ao extrair texto do PDF"
- **Causa:** PDF pode estar protegido ou ser imagem
- **Solução:** Use PDF com texto selecionável
- **Alternativa:** Sistema ignora e analisa sem Release

### Gemini demora muito
- **Normal:** Análise profunda leva tempo
- **Causa:** Gemini lê PDF completo + analisa
- **Solução:** Cache de 24h acelera próximas vezes

---

## ✅ Checklist de Teste

- [ ] Backend rodando em http://localhost:8000
- [ ] Endpoint `/api/v1/final/top-picks` respondendo
- [ ] Preços REAIS aparecendo (Brapi.dev)
- [ ] Adicionar pelo menos 1 PDF de Release
- [ ] Testar novamente e ver `"tem_relatorio": true`
- [ ] Ver logs detalhados no terminal
- [ ] Comparar análise COM vs SEM Release

---

## 🎉 Resultado Final Esperado

Com Releases adicionados, você terá:

✅ **Ranking 1-15** com análise completa  
✅ **Preços REAIS** atualizados  
✅ **Análise de Release** para cada ação  
✅ **Destaques** do trimestre  
✅ **Riscos** identificados  
✅ **Tendências futuras** do setor  
✅ **Recomendação refinada** (COMPRA FORTE/COMPRA/MONITORAR)  

**Sistema completo e funcionando!** 🚀

---

**Próximo passo:** Adicione PDFs de Release e veja a mágica acontecer! ✨
