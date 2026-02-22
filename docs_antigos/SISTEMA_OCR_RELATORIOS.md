# 📄 SISTEMA OCR DE RELATÓRIOS - MISTRAL AI

## 🎯 VISÃO GERAL

Sistema automático de extração de dados de relatórios trimestrais usando **Mistral AI Document OCR**.

### Capacidades
- ✅ Upload de PDFs de relatórios trimestrais
- ✅ Extração automática de dados financeiros
- ✅ OCR inteligente com IA
- ✅ Análise customizada com perguntas
- ✅ Integração com sistema Multi-IA

---

## 🔧 CONFIGURAÇÃO

### API Key Mistral AI
```env
MISTRAL_API_KEY=YlD9P2x2rRKbZiagsVYS3THWPU7BMHUd
```

### Modelo Usado
- **pixtral-large-latest**: Modelo multimodal com visão para PDFs

---

## 📊 DADOS EXTRAÍDOS AUTOMATICAMENTE

### Dados Financeiros
1. Receita Líquida (R$ milhões)
2. Lucro Líquido (R$ milhões)
3. EBITDA (R$ milhões)
4. Margem Líquida (%)
5. Margem EBITDA (%)
6. Crescimento Receita YoY (%)
7. Crescimento Lucro YoY (%)

### Análise Qualitativa
8. Principais destaques do trimestre
9. Riscos mencionados
10. Guidance/Perspectivas futuras

---

## 🚀 ENDPOINTS DISPONÍVEIS

### 1. Upload de Relatório
```http
POST /api/v1/ocr/upload-relatorio/{ticker}
Content-Type: multipart/form-data

file: relatorio_q4_2025.pdf
```

**Resposta**:
```json
{
  "success": true,
  "ticker": "PRIO3",
  "arquivo_salvo": "data/relatorios/PRIO3_Q4_2025.pdf",
  "dados_extraidos": {
    "ticker": "PRIO3",
    "trimestre": "Q4 2025",
    "receita_liquida": 1500.5,
    "lucro_liquido": 250.3,
    "ebitda": 450.2,
    "margem_liquida": 16.7,
    "margem_ebitda": 30.0,
    "crescimento_receita_yoy": 15.2,
    "crescimento_lucro_yoy": 20.5,
    "destaques": [
      "Expansão de margens",
      "Redução de custos"
    ],
    "riscos": [
      "Volatilidade cambial"
    ],
    "guidance": "Crescimento de 10-15% em 2026"
  }
}
```

### 2. Análise Customizada
```http
POST /api/v1/ocr/analisar-pdf?ticker=PRIO3&perguntas=Qual foi o crescimento?|A empresa está lucrativa?
Content-Type: multipart/form-data

file: relatorio.pdf
```

**Resposta**:
```json
{
  "success": true,
  "ticker": "PRIO3",
  "perguntas": [
    "Qual foi o crescimento?",
    "A empresa está lucrativa?"
  ],
  "respostas": "1. O crescimento da receita foi de 15.2% YoY...\n2. Sim, a empresa apresentou lucro líquido de R$ 250M..."
}
```

### 3. Listar Relatórios Disponíveis
```http
GET /api/v1/ocr/relatorios-disponiveis
```

**Resposta**:
```json
{
  "total": 3,
  "relatorios": [
    {
      "ticker": "PRIO3",
      "trimestre": "Q4_2025",
      "arquivo": "PRIO3_Q4_2025.pdf",
      "caminho": "data/relatorios/PRIO3_Q4_2025.pdf"
    }
  ]
}
```

### 4. Deletar Relatório
```http
DELETE /api/v1/ocr/relatorio/{ticker}/{trimestre}
```

---

## 🔄 INTEGRAÇÃO COM SISTEMA MULTI-IA

### Fluxo Completo

1. **Upload de PDFs**
   ```
   POST /api/v1/ocr/upload-relatorio/PRIO3
   → Mistral AI extrai dados
   → Salva em data/relatorios/
   ```

2. **Análise Multi-IA**
   ```
   GET /api/v1/aiml/top-picks-inteligente
   → Gemini 2.5 Pro seleciona top 15
   → Para cada ação:
     - Verifica se existe PDF em data/relatorios/
     - Se sim: usa dados extraídos pelo Mistral OCR
     - Claude Sonnet 4.6 analisa com dados reais
   ```

3. **Resultado Final**
   - Preços reais (Alpha Vantage)
   - Fundamentos (CSV)
   - Dados trimestrais (Mistral OCR)
   - Análise IA (Gemini + Claude)

---

## 📝 COMO USAR

### Passo 1: Baixar Relatórios
Acesse o site de RI das empresas:
- PRIO3: https://ri.prioenergia.com.br
- VULC3: https://ri.vulcabras.com.br
- etc.

Baixe o relatório trimestral mais recente (Q4 2025).

### Passo 2: Upload via API
```bash
curl -X POST "http://localhost:8000/api/v1/ocr/upload-relatorio/PRIO3" \
  -F "file=@PRIO3_Q4_2025.pdf"
```

### Passo 3: Análise Automática
```bash
curl "http://localhost:8000/api/v1/aiml/top-picks-inteligente?limit=15"
```

O sistema vai:
1. Filtrar ações por fundamentos
2. Buscar preços reais
3. Gemini analisa mercado
4. Para cada ação com PDF:
   - Usa dados do Mistral OCR
   - Claude faz análise profunda
5. Retorna recomendações

---

## 💡 EXEMPLOS DE USO

### Exemplo 1: Upload Simples
```python
import requests

url = "http://localhost:8000/api/v1/ocr/upload-relatorio/PRIO3"
files = {"file": open("PRIO3_Q4_2025.pdf", "rb")}

response = requests.post(url, files=files)
print(response.json())
```

### Exemplo 2: Análise Customizada
```python
url = "http://localhost:8000/api/v1/ocr/analisar-pdf"
params = {
    "ticker": "PRIO3",
    "perguntas": "Qual foi o EBITDA?|A dívida aumentou?|Quais os riscos?"
}
files = {"file": open("relatorio.pdf", "rb")}

response = requests.post(url, params=params, files=files)
print(response.json()["respostas"])
```

### Exemplo 3: Listar Relatórios
```python
url = "http://localhost:8000/api/v1/ocr/relatorios-disponiveis"
response = requests.get(url)

for rel in response.json()["relatorios"]:
    print(f"{rel['ticker']} - {rel['trimestre']}")
```

---

## 🎯 VANTAGENS DO SISTEMA

### Antes (Manual)
- ❌ Ler PDFs manualmente
- ❌ Copiar dados para planilha
- ❌ Análise demorada
- ❌ Erros de digitação
- ❌ Dados desatualizados

### Agora (Automático)
- ✅ Upload de PDF
- ✅ Extração automática
- ✅ Análise em segundos
- ✅ Dados precisos
- ✅ Sempre atualizado

---

## 📊 ESTRUTURA DE ARQUIVOS

```
backend/
├── data/
│   └── relatorios/
│       ├── PRIO3_Q4_2025.pdf
│       ├── VULC3_Q4_2025.pdf
│       └── WEGE3_Q4_2025.pdf
├── app/
│   └── services/
│       ├── mistral_ocr_service.py  ← Novo
│       └── aiml_service.py         ← Atualizado
└── .env
    └── MISTRAL_API_KEY=...
```

---

## 🔍 FORMATO DE NOMENCLATURA

### PDFs Salvos
```
{TICKER}_{TRIMESTRE}.pdf

Exemplos:
- PRIO3_Q4_2025.pdf
- VULC3_Q3_2025.pdf
- WEGE3_Q4_2025.pdf
```

### Trimestres
- Q1_2025 (Jan-Mar)
- Q2_2025 (Abr-Jun)
- Q3_2025 (Jul-Set)
- Q4_2025 (Out-Dez)

---

## 💰 CUSTOS ESTIMADOS

### Mistral AI Pricing
- **pixtral-large-latest**: ~$0.02 por página

**Custo por relatório**:
- Relatório típico: 20-30 páginas
- Custo: $0.40 - $0.60 por relatório
- Com 15 ações: ~$6-9 por análise completa

**Otimização**:
- Cache de dados extraídos
- Reutilização por 3 meses (trimestre)
- Custo amortizado: ~$2-3 por mês

---

## 🐛 TROUBLESHOOTING

### Erro: "Model not found"
- Verifique se o modelo está correto: `pixtral-large-latest`
- Confirme que a API key é válida

### Erro: "PDF too large"
- Limite: ~10MB por PDF
- Comprima o PDF antes do upload

### Erro: "Failed to extract data"
- PDF pode estar protegido
- Tente converter para imagens primeiro
- Use análise customizada com perguntas específicas

---

## 📚 PRÓXIMAS MELHORIAS

### Curto Prazo
- [ ] Download automático de sites de RI
- [ ] Suporte para múltiplos trimestres
- [ ] Comparação trimestre a trimestre

### Médio Prazo
- [ ] Análise de tendências (4 trimestres)
- [ ] Alertas de mudanças significativas
- [ ] Dashboard de evolução trimestral

### Longo Prazo
- [ ] Scraping automático de todos os sites de RI
- [ ] Atualização automática a cada trimestre
- [ ] Previsões baseadas em histórico

---

**Status**: ✅ IMPLEMENTADO E PRONTO
**Versão**: 1.0.0
**Data**: 19/02/2026
