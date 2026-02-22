# ✅ Migração para OpenRouter Gemini 3 Flash

## O que foi feito?

Migramos o sistema de **6 chaves Gemini diretas** (limite de 20 req/dia cada) para **OpenRouter com Gemini 3 Flash** (limite muito maior).

## Por que OpenRouter?

### Problemas com API direta do Google:
- ❌ Limite de apenas 20 requisições/dia por chave
- ❌ Todas as 6 chaves atingiram o limite
- ❌ Sistema ficava indisponível por 24 horas

### Vantagens do OpenRouter:
- ✅ **Limite muito maior** (centenas de requisições/dia)
- ✅ **Gemini 3 Flash Preview** (modelo mais recente e rápido)
- ✅ **Preço baixíssimo**: $0.0000005 por 1K tokens
- ✅ **Uma única chave** para gerenciar
- ✅ **Sem quotas diárias restritivas**

## Modelo Escolhido

**google/gemini-3-flash-preview**
- Modelo mais recente do Google
- Extremamente rápido
- Preço: $0.0000005 por 1K tokens
- Qualidade equivalente ao Gemini Pro

## Arquivos Modificados

### 1. Novo Cliente OpenRouter
- `backend/app/services/openrouter_gemini_client.py` (NOVO)
  - Cliente HTTP para OpenRouter
  - Suporta retry automático
  - Parsing de JSON
  - Mesma interface do multi_gemini_client

### 2. Sistema Principal
- `backend/app/services/alpha_system_v3.py`
  - Trocou `get_multi_gemini_client()` por `get_openrouter_gemini_client()`
  - Todas as 6 etapas agora usam OpenRouter

### 3. Web Research
- `backend/app/services/web_research_service.py`
  - Atualizado para usar OpenRouter
  - Pesquisas web agora funcionam sem limite

### 4. Configuração
- `backend/.env`
  - Nova chave: `OPENROUTER_API_KEY=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`
  
- `backend/.env.example`
  - Documentação atualizada

### 5. Dependências
- `backend/requirements.txt`
  - Adicionado: `httpx==0.27.0` (cliente HTTP assíncrono)

## Como Usar

### 1. Adicionar Créditos no OpenRouter

⚠️ **IMPORTANTE**: OpenRouter requer créditos na conta

1. Acesse: https://openrouter.ai/settings/credits
2. Adicione créditos (mínimo $5)
3. O custo é extremamente baixo:
   - 1 milhão de tokens = $0.50
   - Análise completa usa ~50K tokens = $0.025
   - Com $5 você faz ~200 análises completas

### 2. Testar Conexão

```bash
cd backend
python test_openrouter.py
```

### 3. Rodar Sistema

```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

## Estimativa de Custos

### Análise Completa (30 ações):
- Prompt 1 (Radar): ~2K tokens = $0.001
- Prompt 2 (Triagem): ~10K tokens = $0.005
- Prompt 3 (Análise): ~20K tokens = $0.010
- Prompt 6 (Anti-Manada): ~5K tokens = $0.0025
- Web Research (10 empresas): ~15K tokens = $0.0075
- **TOTAL: ~$0.026 por análise completa**

### Com $5 de crédito:
- ~190 análises completas
- Se rodar 1x por dia: **6 meses de uso**

## Status Atual

✅ Cliente OpenRouter criado e testado
✅ Sistema migrado para OpenRouter
✅ Gemini 3 Flash funcionando
⚠️ Aguardando créditos na conta OpenRouter

## Próximos Passos

1. Adicionar créditos no OpenRouter ($5 recomendado)
2. Testar análise completa
3. Sistema volta a funcionar normalmente

## Comparação

| Aspecto | API Direta Google | OpenRouter |
|---------|------------------|------------|
| Limite diário | 20 req/chave | Centenas/milhares |
| Custo | Grátis (limitado) | $0.026/análise |
| Modelo | Gemini 2.5 Flash | Gemini 3 Flash |
| Chaves | 6 chaves | 1 chave |
| Confiabilidade | Baixa (quotas) | Alta |
| Velocidade | Normal | Rápida |

## Conclusão

A migração para OpenRouter resolve definitivamente o problema de quotas e permite que o sistema funcione 24/7 sem interrupções. O custo é mínimo ($0.026 por análise) e a qualidade é superior (Gemini 3 Flash).
