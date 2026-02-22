# 🔄 Como Reiniciar o Sistema

## 📋 INSTRUÇÕES RÁPIDAS

### 1. Parar Processos Atuais

#### Backend
```bash
# No terminal do backend, pressione:
Ctrl + C
```

#### Frontend
```bash
# No terminal do frontend, pressione:
Ctrl + C
```

### 2. Reiniciar Backend

```bash
cd blog-cozy-corner-81/backend
python -m uvicorn app.main:app --reload --port 8000
```

**Aguarde ver no console**:
```
✓ Multi-Groq Client inicializado com 6 chaves
✓ Dados Fundamentalistas Service: Sistema Híbrido + yfinance otimizado
✓ Análise Automática Service inicializado
✓ Cache carregado: X análises
✓ Scheduler inicializado (intervalo: 60min)
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Reiniciar Frontend

```bash
cd blog-cozy-corner-81
npm run dev
```

**Aguarde ver no console**:
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:8080/
➜  Network: use --host to expose
```

### 4. Acessar Sistema

```
Frontend: http://localhost:8080
Admin Panel: http://localhost:8080/admin
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
```

## 🧪 VERIFICAR SE ESTÁ FUNCIONANDO

### 1. Backend
```bash
# Teste rápido
curl http://localhost:8000/health

# Deve retornar:
{"status":"ok"}
```

### 2. Frontend
```bash
# Abra no navegador
http://localhost:8080

# Deve carregar a página principal
```

### 3. Admin Panel
```bash
# Abra no navegador
http://localhost:8080/admin

# Login: admin
# Deve carregar o painel
```

### 4. Novo Sistema de Análise
```bash
# No admin panel, verifique:
✓ Seção "Scheduler Automático" aparece
✓ Seção "Ranking Atual" aparece
✓ Botão "Analisar com Releases" funciona
```

## 🐛 PROBLEMAS COMUNS

### Backend não inicia
```bash
# Erro: "Address already in use"
# Solução: Matar processo na porta 8000

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Ou use outra porta
python -m uvicorn app.main:app --reload --port 8001
```

### Frontend não inicia
```bash
# Erro: "Port 8080 is already in use"
# Solução: Matar processo na porta 8080

# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Ou edite vite.config.ts para usar outra porta
```

### Módulos não carregam
```bash
# Erro: "Module not found"
# Solução: Verificar se arquivos foram criados

# Verificar backend
ls blog-cozy-corner-81/backend/app/services/analise_automatica/

# Deve listar:
__init__.py
analise_service.py
cache_manager.py
validador.py
scheduler.py
```

### Cache não funciona
```bash
# Criar pasta manualmente
mkdir blog-cozy-corner-81/data/cache

# Verificar permissões
# Windows: Propriedades → Segurança → Permitir escrita
```

## 📊 LOGS IMPORTANTES

### Backend Console
```
✓ Multi-Groq Client inicializado com 6 chaves
✓ Dados Fundamentalistas Service: Sistema Híbrido
✓ Análise Automática Service inicializado
✓ Cache carregado: X análises
✓ Scheduler inicializado (intervalo: 60min)
```

### Análise Incremental
```
===================================================================
ANÁLISE INCREMENTAL AUTOMÁTICA
===================================================================
📊 Total de empresas: 30
🔄 Forçar reanálise: Não
⚡ Análises paralelas: 3
===================================================================

📋 RESUMO:
   Para analisar: X
   Com cache válido: Y

[... análise ...]

===================================================================
✅ ANÁLISE CONCLUÍDA
===================================================================
✓ Novas análises: X
💾 Cache mantido: Y
❌ Falhas: Z
🏆 Ranking: 30 empresas
⏱️  Tempo total: XX.Xs
===================================================================
```

### Scheduler
```
======================================================================
🕐 SCHEDULER - Próxima execução: HH:MM:SS
======================================================================

[... aguarda ...]

======================================================================
🤖 SCHEDULER - Executando análise automática
======================================================================

[... análise ...]

✅ Análise automática concluída em XX.Xs
```

## 🎯 CHECKLIST PÓS-REINÍCIO

- [ ] Backend rodando na porta 8000
- [ ] Frontend rodando na porta 8080
- [ ] Admin panel acessível
- [ ] Seção "Scheduler" aparece
- [ ] Seção "Ranking" aparece
- [ ] Botão "Analisar com Releases" funciona
- [ ] Cache carrega (se existir)
- [ ] Scheduler pode ser iniciado
- [ ] Logs aparecem no console

## 🚀 PRÓXIMOS PASSOS

1. ✅ Sistema reiniciado
2. ✅ Verificações OK
3. 🎯 Testar análise incremental
4. 🎯 Ativar scheduler
5. 🎯 Monitorar logs

## 📞 AJUDA

Se algo não funcionar:

1. **Verifique os logs** do backend e frontend
2. **Leia a documentação**:
   - `SISTEMA_ANALISE_INCREMENTAL.md`
   - `TESTE_SISTEMA_INCREMENTAL.md`
3. **Verifique os arquivos** foram criados corretamente
4. **Reinicie tudo** do zero se necessário

---

**Última atualização**: 20/02/2026
**Status**: ✅ Sistema pronto para uso
