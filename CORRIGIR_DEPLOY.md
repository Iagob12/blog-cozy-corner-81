# 🔧 CORRIGIR ERRO DE DEPLOY

## ❌ Erro: "Exited with status 2"

Este erro geralmente indica problema no build ou na inicialização do backend.

---

## 🔍 DIAGNÓSTICO

### 1. Ver logs completos no Render
1. Acesse o dashboard do Render
2. Clique no service "alpha-backend"
3. Vá em "Logs"
4. Procure por mensagens de erro (linhas em vermelho)

### Erros comuns:
- `ModuleNotFoundError`: Dependência faltando
- `ImportError`: Problema de importação
- `SyntaxError`: Erro de sintaxe no código
- `Port already in use`: Porta ocupada (raro no Render)

---

## ✅ CORREÇÕES APLICADAS

Acabei de criar/atualizar estes arquivos:

### 1. `backend/Procfile`
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level warning
```

### 2. `backend/runtime.txt`
```
python-3.11.0
```

### 3. `render.yaml` (atualizado)
- Build command melhorado: `pip install --upgrade pip && pip install -r requirements.txt`
- Variáveis de ambiente como strings
- Auto-deploy habilitado

---

## 🚀 PRÓXIMOS PASSOS

### Opção 1: Commit e Push (RECOMENDADO)

```powershell
cd c:\Users\bonde\Alpha\blog-cozy-corner-81

# Adicionar arquivos corrigidos
git add backend/Procfile
git add backend/runtime.txt
git add render.yaml

# Commit
git commit -m "Fix: Corrigir deploy no Render"

# Push
git push

# Render fará deploy automático
```

### Opção 2: Deploy Manual no Render

1. Dashboard do Render
2. Clique no service "alpha-backend"
3. "Manual Deploy" → "Clear build cache & deploy"

---

## 🐛 SE AINDA FALHAR

### Verificar logs específicos

Procure por estas mensagens nos logs:

#### 1. Erro de dependência
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solução**: Verificar `requirements.txt`

#### 2. Erro de importação
```
ImportError: cannot import name 'app' from 'app.main'
```

**Solução**: Verificar estrutura de pastas

#### 3. Erro de porta
```
Error: Port 8000 is already in use
```

**Solução**: Usar variável `$PORT` do Render

#### 4. Erro de Python
```
python: command not found
```

**Solução**: Verificar `runtime.txt`

---

## 🔧 CORREÇÕES ADICIONAIS

### Se o erro persistir, tente:

### 1. Simplificar o startCommand

No Render Dashboard → Backend Service → Settings:

**Build Command:**
```bash
pip install --upgrade pip && pip install -r requirements.txt
```

**Start Command:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### 2. Verificar estrutura de pastas

Certifique-se que existe:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   └── services/
├── requirements.txt
├── Procfile
└── runtime.txt
```

### 3. Testar localmente

```powershell
cd c:\Users\bonde\Alpha\blog-cozy-corner-81\backend

# Ativar venv
venv\Scripts\activate.bat

# Instalar dependências
pip install -r requirements.txt

# Testar
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Se funcionar localmente, problema é no Render
```

---

## 📋 CHECKLIST DE VERIFICAÇÃO

- [ ] `backend/Procfile` existe
- [ ] `backend/runtime.txt` existe
- [ ] `backend/requirements.txt` está completo
- [ ] `backend/app/__init__.py` existe
- [ ] `backend/app/main.py` existe
- [ ] Variáveis de ambiente configuradas no Render
- [ ] Build command correto
- [ ] Start command correto
- [ ] Logs verificados

---

## 💡 DICAS

### 1. Logs em tempo real
```bash
# No Render Dashboard
# Logs → Enable Auto-scroll
# Veja o build acontecendo em tempo real
```

### 2. Clear build cache
```bash
# Se mudou dependências
# Manual Deploy → Clear build cache & deploy
```

### 3. Testar health check
```bash
# Após deploy bem-sucedido
curl https://seu-backend.onrender.com/

# Deve retornar algo (não erro 502)
```

---

## 🆘 ÚLTIMA OPÇÃO: DEPLOY MANUAL

Se nada funcionar, tente deploy sem Blueprint:

### 1. Deletar services atuais no Render

### 2. Criar Backend manualmente
1. New + → Web Service
2. Connect repository
3. Name: `alpha-backend`
4. Root Directory: `backend`
5. Runtime: Python 3
6. Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
7. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --log-level warning`
8. Add environment variables (todas as GROQ_API_KEY_*, BRAPI_TOKEN_*, etc)

### 3. Criar Frontend manualmente
1. New + → Web Service
2. Connect repository
3. Name: `alpha-frontend`
4. Root Directory: `.` (raiz)
5. Runtime: Node
6. Build Command: `npm install && npm run build`
7. Start Command: `npm run preview -- --host 0.0.0.0 --port $PORT`
8. Add environment variable: `VITE_API_URL`

---

## 📞 SUPORTE

### Render Support
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Logs úteis
```bash
# Copie e cole os logs completos do Render
# Procure por:
# - "ERROR"
# - "FAILED"
# - "ModuleNotFoundError"
# - "ImportError"
```

---

**Próximo passo**: Commit e push das correções, depois monitore os logs no Render! 🚀
