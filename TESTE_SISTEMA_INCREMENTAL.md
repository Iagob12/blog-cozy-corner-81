# 🧪 Guia de Teste - Sistema de Análise Incremental

## 🎯 OBJETIVO

Testar o sistema de análise incremental automática para garantir que tudo funciona perfeitamente.

## 📋 PRÉ-REQUISITOS

- ✅ Backend rodando na porta 8000
- ✅ Frontend rodando na porta 8080
- ✅ 30 releases já enviados (salvos em `data/releases/`)
- ✅ Empresas aprovadas existem (`data/empresas_aprovadas.json`)
- ✅ Admin autenticado (senha: "admin")

## 🚀 PASSO A PASSO

### 1. Reiniciar Backend (Carregar Novos Módulos)

```bash
# Parar backend (Ctrl+C)
# Iniciar novamente
cd blog-cozy-corner-81/backend
python -m uvicorn app.main:app --reload --port 8000
```

**Verificar no console**:
```
✓ Análise Automática Service inicializado
✓ Cache carregado: X análises
✓ Scheduler inicializado (intervalo: 60min)
```

### 2. Acessar Admin Panel

```
http://localhost:8080/admin
```

**Login**: senha "admin"

### 3. Verificar Seções Novas

Você deve ver:
- ✅ Seção "Releases de Resultados" (já existia)
- ✅ Seção "Scheduler Automático" (NOVA)
- ✅ Seção "Ranking Atual" (NOVA)

### 4. Testar Análise Incremental

#### 4.1. Primeira Análise (Criar Cache)

1. Na seção "Releases", clique em **"Analisar com Releases"**
2. Aguarde 1-3 minutos
3. Observe o console do backend:
   ```
   ===================================================================
   ANÁLISE INCREMENTAL AUTOMÁTICA
   ===================================================================
   📊 Total de empresas: 30
   🔄 Forçar reanálise: Não
   ⚡ Análises paralelas: 3
   ===================================================================
   
   📋 RESUMO:
      Para analisar: 30
      Com cache válido: 0
   
   💰 Buscando preços...
      ✓ 30 preços obtidos
   
   🤖 Analisando empresas...
   🔍 PRIO3: Iniciando análise...
      📊 Buscando dados fundamentalistas...
      ✓ yfinance OK
      🤖 Consultando IA...
   ✅ PRIO3: Análise concluída (Score: 8.5)
   ...
   
   🏆 Gerando ranking...
   ✓ Ranking salvo: 30 empresas
   
   ===================================================================
   ✅ ANÁLISE CONCLUÍDA
   ===================================================================
   ✓ Novas análises: 30
   💾 Cache mantido: 0
   ❌ Falhas: 0
   🏆 Ranking: 30 empresas
   ⏱️  Tempo total: 120.5s
   ===================================================================
   ```

4. Verifique que foram criados:
   - `data/cache/analises_cache.json`
   - `data/cache/ranking_atual.json`
   - `data/cache/historico_analises.json`

#### 4.2. Segunda Análise (Usar Cache)

1. Clique novamente em **"Analisar com Releases"**
2. Observe o console:
   ```
   📋 RESUMO:
      Para analisar: 0
      Com cache válido: 30
   
   ✅ Todas as empresas já têm cache válido!
   ```

3. Tempo: ~0 segundos (instantâneo!)

#### 4.3. Forçar Reanálise

1. Use a API diretamente:
   ```bash
   curl -X POST http://localhost:8000/api/v1/admin/analise-incremental \
     -H "Authorization: Bearer SEU_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"forcar_reanalise": true}'
   ```

2. Observe que todas as 30 empresas são reanalisadas

### 5. Testar Ranking

#### 5.1. Visualizar Ranking

1. Role até a seção **"Ranking Atual"**
2. Verifique:
   - ✅ Estatísticas no topo (Total, Com Release, Sem Release, Score Médio)
   - ✅ Lista de empresas ordenadas por score
   - ✅ Rank visual (1-3 destacados)
   - ✅ Indicador de release (✓ verde)
   - ✅ Score colorido (verde >8, amarelo 6-8, vermelho <6)
   - ✅ Recomendação colorida
   - ✅ Métricas (Preço Teto, Upside)

#### 5.2. Atualizar Ranking

1. Clique no botão **"Atualizar"** (ícone de refresh)
2. Dados devem recarregar

### 6. Testar Scheduler

#### 6.1. Iniciar Scheduler

1. Na seção **"Scheduler Automático"**, clique em **"Iniciar Scheduler"**
2. Verifique:
   - ✅ Status muda para "ATIVO" (verde pulsante)
   - ✅ Mostra "Próxima execução: HH:MM:SS"
   - ✅ Botão muda para "Parar Scheduler" (vermelho)

3. Observe o console do backend:
   ```
   ✅ Scheduler iniciado (intervalo: 60min)
   
   ======================================================================
   🕐 SCHEDULER - Próxima execução: 17:00:00
   ======================================================================
   ```

#### 6.2. Aguardar Execução Automática

**ATENÇÃO**: O scheduler executa a cada 60 minutos. Para testar mais rápido:

1. Edite `backend/app/services/analise_automatica/scheduler.py`:
   ```python
   # Linha 17 - Mude de 60 para 2 minutos
   def __init__(self, intervalo_minutos: int = 2):  # Era 60
   ```

2. Reinicie o backend

3. Inicie o scheduler novamente

4. Aguarde 2 minutos

5. Observe o console:
   ```
   ======================================================================
   🤖 SCHEDULER - Executando análise automática
   ======================================================================
   
   [Análise incremental executada]
   
   ✅ Análise automática concluída em 45.2s
   ```

6. Verifique a seção "Últimos Eventos" no frontend

#### 6.3. Parar Scheduler

1. Clique em **"Parar Scheduler"**
2. Verifique:
   - ✅ Status muda para "INATIVO" (cinza)
   - ✅ "Próxima execução" desaparece
   - ✅ Botão muda para "Iniciar Scheduler" (verde)

### 7. Testar Estatísticas

1. Use a API:
   ```bash
   curl http://localhost:8000/api/v1/admin/estatisticas-analise \
     -H "Authorization: Bearer SEU_TOKEN"
   ```

2. Verifique resposta:
   ```json
   {
     "total_analises": 30,
     "com_release": 30,
     "sem_release": 0,
     "timestamp_criacao": "2026-02-20T10:00:00",
     "timestamp_atualizacao": "2026-02-20T16:00:00",
     "total_historico": 2,
     "validacao": {
       "total_erros": 0,
       "erros_por_tipo": {}
     }
   }
   ```

### 8. Testar Detecção de Mudanças

#### 8.1. Simular Release Novo

1. Faça upload de um release novo para uma empresa:
   ```bash
   # Via interface ou API
   POST /api/v1/admin/releases/upload
   ticker: PRIO3
   trimestre: Q1
   ano: 2026
   file: novo_release.pdf
   ```

2. Execute análise incremental

3. Observe que APENAS PRIO3 é reanalisada:
   ```
   📋 RESUMO:
      Para analisar: 1
      Com cache válido: 29
   
   🔄 PRIO3: Release novo detectado
   ```

#### 8.2. Simular Cache Antigo

1. Edite `data/cache/analises_cache.json`
2. Mude o timestamp de uma empresa para 48h atrás
3. Execute análise incremental
4. Observe que essa empresa é reanalisada:
   ```
   🔄 VALE3: Cache antigo (48.0h)
   ```

### 9. Testar Validação

#### 9.1. Forçar Erro de Validação

Para testar a validação, você pode:

1. Modificar temporariamente o validador para ser mais restritivo
2. Ou observar erros naturais nos logs

#### 9.2. Ver Estatísticas de Validação

```bash
curl http://localhost:8000/api/v1/admin/estatisticas-analise \
  -H "Authorization: Bearer SEU_TOKEN"
```

Verifique seção `validacao`:
```json
{
  "validacao": {
    "total_erros": 3,
    "erros_por_tipo": {
      "upside": 2,
      "score": 1
    }
  }
}
```

## ✅ CHECKLIST DE TESTES

### Backend
- [ ] Módulos carregam sem erro
- [ ] Cache é criado corretamente
- [ ] Análise incremental funciona
- [ ] Validação detecta erros
- [ ] Scheduler inicia/para
- [ ] Scheduler executa automaticamente
- [ ] Logs são salvos
- [ ] Ranking é gerado

### Frontend
- [ ] Seção de Ranking aparece
- [ ] Seção de Scheduler aparece
- [ ] Estatísticas são exibidas
- [ ] Ranking é exibido corretamente
- [ ] Cores e ícones corretos
- [ ] Botões funcionam
- [ ] Auto-refresh funciona
- [ ] Mensagens de sucesso/erro aparecem

### Integração
- [ ] Backend ↔ Frontend comunicam
- [ ] Cache persiste entre reinícios
- [ ] Scheduler sobrevive a reinícios
- [ ] Releases são detectados
- [ ] Mudanças são detectadas
- [ ] Validação funciona
- [ ] Erros são tratados

## 🐛 PROBLEMAS COMUNS

### Erro: "Module not found"
**Solução**: Reinicie o backend para carregar novos módulos

### Erro: "empresas_aprovadas.json not found"
**Solução**: Execute análise completa primeiro (Prompt 1+2)

### Erro: "Nenhum ranking disponível"
**Solução**: Execute análise incremental primeiro

### Scheduler não executa
**Solução**: Verifique se está ativo e aguarde o intervalo

### Validação falha muito
**Solução**: Verifique prompts da IA e ajuste se necessário

## 📊 RESULTADOS ESPERADOS

### Performance
- Análise completa (30 empresas): 2-3 minutos
- Análise incremental (5 empresas): 30-60 segundos
- Análise incremental (0 empresas): <1 segundo
- Scheduler overhead: <1% CPU

### Confiabilidade
- Taxa de sucesso: >95%
- Validação: >98% de precisão
- Uptime scheduler: >99%

### Eficiência
- Economia de tempo: 80-90%
- Economia de chamadas IA: 80-90%
- Uso de cache: >90%

## 🎉 SUCESSO!

Se todos os testes passaram, o sistema está funcionando perfeitamente! 🚀

O sistema de análise incremental está:
- ✅ Analisando apenas o necessário
- ✅ Validando resultados rigorosamente
- ✅ Executando automaticamente
- ✅ Mantendo dados persistentes
- ✅ Tratando erros robustamente

**Próximos passos**:
1. Deixar scheduler ativo
2. Monitorar logs periodicamente
3. Fazer upload de releases novos conforme disponíveis
4. Sistema se atualiza automaticamente!
