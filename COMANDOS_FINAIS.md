# COMANDOS FINAIS - SISTEMA FUNCIONANDO

## SITUAÇÃO ATUAL

✅ Backend funcionando (porta 8000)
✅ Frontend funcionando (porta 8080)
✅ API retornando dados
✅ Prompts melhorados implementados
⚠️ Site não mostra ranking (problema no frontend)
⚠️ Ranking atual ruim (precisa rodar nova análise)

## PARA RODAR NOVA ANÁLISE COM PROMPTS MELHORADOS

### Opção 1: Via Admin Panel (RECOMENDADO)

1. Acesse: http://localhost:8080/admin
2. Senha: admin
3. Faça upload de um release qualquer
4. Sistema roda análise automática com novos prompts

### Opção 2: Via Backend Direto

```bash
cd backend

# Limpa cache
Remove-Item data\cache\* -Force

# Para o backend atual
# (Ctrl+C no terminal do backend)

# Inicia backend (ele vai rodar análise automática)
python -m uvicorn app.main:app --reload --port 8000
```

## PARA VER O RANKING

### Via API (FUNCIONANDO)

```bash
curl http://localhost:8000/api/v1/alpha-v3/top-picks?limit=10
```

### Via Site (NÃO FUNCIONANDO - INVESTIGAR)

http://localhost:8080

**Problema:** Frontend não está carregando os dados mesmo com API funcionando.

**Possíveis causas:**
1. Erro no console do navegador (F12)
2. Problema no React Query
3. Timeout na requisição

## PROMPTS MELHORADOS IMPLEMENTADOS

✅ Arquivo: `backend/app/services/analise_automatica/analise_service.py`

**Novos critérios:**
- Foco em potencial de 5% ao mês
- ROE > 12% (alta rentabilidade)
- P/L entre 5-15 (preço justo)
- CAGR > 10% (crescimento forte)
- Análise qualitativa profunda
- Score rigoroso (apenas ações boas têm score alto)

## PRÓXIMOS PASSOS

1. **Investigar por que site não carrega**
   - Abrir console do navegador (F12)
   - Ver erros JavaScript
   - Verificar requisições na aba Network

2. **Rodar nova análise**
   - Usar admin panel para fazer upload de release
   - Ou reiniciar backend com cache limpo

3. **Comparar resultado**
   - Ver novo ranking via API
   - Comparar com seu resultado manual
   - Ajustar prompts se necessário

## ARQUIVOS IMPORTANTES

- `backend/app/services/analise_automatica/analise_service.py` - Prompts melhorados
- `backend/NOVOS_PROMPTS_PRIMO_RICO.md` - Documentação dos prompts
- `backend/data/ranking_cache.json` - Ranking atual
- `src/pages/AlphaTerminal.tsx` - Frontend (investigar)

## TESTE RÁPIDO

```powershell
# Testar API
$data = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/alpha-v3/top-picks?limit=5"
$data | ForEach-Object { Write-Host "$($_.ticker) - Score: $($_.efficiency_score)" }
```

Se retornar dados = API OK
Se site não mostrar = Problema no frontend
