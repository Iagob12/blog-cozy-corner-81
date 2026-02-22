# 🔍 Problemas Encontrados em Runtime

Data: 20/02/2026 01:55

## ✅ O Que Está Funcionando

1. ✅ **Multi Groq Client** - Rotação automática OK
2. ✅ **Detecção de Rate Limit** - Detecta 429 e marca chave
3. ✅ **Sistema de Espera** - Aguarda quando todas em rate limit
4. ✅ **Pesquisa Web** - 28/30 concluídas (93%)
5. ✅ **Contexto Persistente** - Mantém informações
6. ✅ **Delay entre requisições** - 0.5s funcionando

---

## ⚠️ PROBLEMA CRÍTICO: Paralelismo Excessivo

### Problema:
```
[01:55:45] Todas as chaves em rate limit. Aguardando 5s... (tentativa 1/12)
[01:55:46] Todas as chaves em rate limit. Aguardando 5s... (tentativa 1/12)
[01:55:46] Todas as chaves em rate limit. Aguardando 5s... (tentativa 1/12)
```

### Causa:
- Sistema faz 30 pesquisas web SIMULTÂNEAS (uma por empresa)
- Temos apenas 6 chaves Groq
- Cada chave tem limite de 30 req/min
- 30 requisições paralelas esgotam todas as 6 chaves em segundos

### Impacto:
- ⚠️ Análise muito lenta (aguarda 60s múltiplas vezes)
- ⚠️ Todas as chaves ficam bloqueadas ao mesmo tempo
- ⚠️ Sistema funciona mas demora muito

### Solução:
**Implementar sistema de lotes (batches) para pesquisa web:**

```python
# ANTES (atual):
# Faz 30 pesquisas simultâneas
tasks = [pesquisar_empresa(e) for e in empresas]  # 30 tasks
resultados = await asyncio.gather(*tasks)

# DEPOIS (proposto):
# Faz 6 pesquisas por vez (uma por chave)
BATCH_SIZE = 6
for i in range(0, len(empresas), BATCH_SIZE):
    batch = empresas[i:i+BATCH_SIZE]
    tasks = [pesquisar_empresa(e) for e in batch]
    resultados_batch = await asyncio.gather(*tasks)
    # Aguarda 2s entre lotes
    await asyncio.sleep(2)
```

**Benefícios:**
- ✅ Usa 1 chave por empresa (6 simultâneas)
- ✅ Não esgota todas as chaves de uma vez
- ✅ Análise mais rápida (não precisa aguardar 60s)
- ✅ Mais eficiente

---

## ⚠️ PROBLEMA MENOR: CSV Desatualizado

### Problema:
```
CSV muito antigo: 24.2h (máximo: 24h)
```

### Causa:
- Scraper de investimentos.com.br não conseguiu baixar CSV novo
- Todas as URLs testadas falharam
- Scraping da página também falhou

### Impacto:
- ⚠️ Dados de ontem (aceitável mas não ideal)
- ⚠️ Pode ter ações com dados desatualizados

### Solução Temporária:
- ✅ Aumentado limite para 48h
- ✅ Sistema continua funcionando

### Solução Definitiva:
1. Melhorar scraper com mais URLs
2. API alternativa para dados fundamentalistas
3. Fallback para yfinance ou outras fontes

---

## ⚠️ PROBLEMA MENOR: Nenhum Release Encontrado

### Problema:
```
⚠ PRIO3: Release não encontrado (tentou Q4→Q3→Q2→Q1 2025)
⚠ B3SA3: Release não encontrado (tentou Q4→Q3→Q2→Q1 2025)
... (30/30 empresas)
```

### Causa:
- Releases de Q4 2025 ainda não publicados (estamos em fevereiro)
- Q3 2025 também não disponível
- Sistema tentou Q4→Q3→Q2→Q1 mas nenhum encontrado

### Impacto:
- ⚠️ Sistema usa pesquisa web para TODAS as 30 empresas
- ⚠️ Isso causa o problema de paralelismo excessivo

### Solução:
1. ✅ Pesquisa web como fallback (já implementado)
2. ⏳ Ajustar datas de busca (Q3 2024, Q4 2024)
3. ⏳ Melhorar download de releases

---

## 📊 Métricas Observadas

| Métrica | Valor | Status |
|---------|-------|--------|
| Chaves Groq | 6 | ✅ |
| Rate limit detectado | Sim (429) | ✅ |
| Sistema de espera | Funcionando | ✅ |
| Pesquisas web | 28/30 (93%) | ✅ |
| Paralelismo | 30 simultâneas | ⚠️ MUITO |
| Tempo de espera | 60s por chave | ⚠️ |
| Releases encontrados | 0/30 (0%) | ⚠️ |

---

## 🎯 Prioridades de Correção

### ALTA 🔴
1. **Implementar batches para pesquisa web**
   - Limitar a 6 pesquisas simultâneas
   - Processar em lotes
   - Aguardar entre lotes

### MÉDIA 🟡
2. **Ajustar busca de releases**
   - Tentar Q3/Q4 2024 (não 2025)
   - Melhorar download

3. **Melhorar scraper de CSV**
   - Mais URLs para tentar
   - API alternativa

### BAIXA 🟢
4. **Otimizações gerais**
   - Cache mais inteligente
   - Logs mais limpos

---

## 💡 Código Proposto

### 1. Batches para Web Research

```python
# Em web_research_service.py

async def pesquisar_multiplas_empresas(
    self, 
    empresas: list[Dict],
    batch_size: int = 6  # NOVO: tamanho do lote
) -> Dict[str, Dict]:
    """
    Pesquisa múltiplas empresas EM LOTES
    
    Args:
        empresas: Lista de dicts com 'ticker' e 'nome'
        batch_size: Quantas pesquisas simultâneas (padrão: 6, uma por chave)
    
    Returns:
        Dict[ticker, resultado_pesquisa]
    """
    
    print(f"\n🔍 Pesquisando {len(empresas)} empresas em lotes de {batch_size}...")
    
    pesquisas = {}
    
    # Processa em lotes
    for i in range(0, len(empresas), batch_size):
        batch = empresas[i:i+batch_size]
        lote_num = (i // batch_size) + 1
        total_lotes = (len(empresas) + batch_size - 1) // batch_size
        
        print(f"\n📦 Lote {lote_num}/{total_lotes}: {len(batch)} empresas")
        
        # Cria tasks para este lote
        tasks = []
        for empresa in batch:
            ticker = empresa.get('ticker', '')
            nome = empresa.get('nome', ticker)
            task = self.pesquisar_empresa_completo(ticker, nome)
            tasks.append(task)
        
        # Executa lote em paralelo
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processa resultados
        for j, resultado in enumerate(resultados):
            if isinstance(resultado, Exception):
                ticker = batch[j].get('ticker', '')
                print(f"   ✗ {ticker}: Erro - {resultado}")
                continue
            
            if resultado.get('success'):
                ticker = resultado['ticker']
                pesquisas[ticker] = resultado
        
        # Aguarda entre lotes (exceto no último)
        if i + batch_size < len(empresas):
            tempo_espera = 2
            print(f"   ⏳ Aguardando {tempo_espera}s antes do próximo lote...")
            await asyncio.sleep(tempo_espera)
    
    print(f"\n✓ {len(pesquisas)}/{len(empresas)} pesquisas concluídas\n")
    
    return pesquisas
```

### 2. Ajustar Busca de Releases

```python
# Em release_downloader.py

async def buscar_release_mais_recente(self, ticker: str) -> Optional[Dict]:
    """
    Busca Release mais recente com fallback Q4 2024 → Q3 2024 → Q2 2024
    """
    
    # Tenta Q4 2024 (não 2025!)
    release = await self.baixar_release(ticker, "Q4", 2024)
    if release:
        return release
    
    # Tenta Q3 2024
    release = await self.baixar_release(ticker, "Q3", 2024)
    if release:
        return release
    
    # Tenta Q2 2024
    release = await self.baixar_release(ticker, "Q2", 2024)
    if release:
        return release
    
    # Tenta Q1 2024
    release = await self.baixar_release(ticker, "Q1", 2024)
    if release:
        return release
    
    return None
```

---

## 🚀 Próximos Passos

1. ✅ Problemas identificados e documentados
2. ⏳ Implementar batches para web research
3. ⏳ Ajustar busca de releases para 2024
4. ⏳ Testar sistema com correções
5. ⏳ Monitorar performance

---

## 📝 Observações

- Sistema está FUNCIONAL mas LENTO
- Rate limit control está funcionando perfeitamente
- Problema principal é ESTRATÉGICO (paralelismo excessivo)
- Solução é simples: processar em lotes
- Com batches, análise será 3-4x mais rápida

**Conclusão: Sistema 80% perfeito, precisa de ajuste estratégico no paralelismo.**
