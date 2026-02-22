# 🚀 DEPLOY NO RENDER (RECOMENDADO)

Deploy gratuito e fácil do Alpha System no Render.com

## 📋 PRÉ-REQUISITOS

- Conta no GitHub
- Conta no Render (https://render.com - gratuita)
- Repositório Git do projeto

---

## 🔧 PASSO 1: PREPARAR O PROJETO

### 1.1 Criar arquivos de configuração

Já criados automaticamente:
- ✅ `render.yaml` - Configuração do Render
- ✅ `backend/requirements.txt` - Dependências Python
- ✅ `package.json` - Dependências Node

### 1.2 Commitar no Git

```bash
cd c:\Users\bonde\Alpha\blog-cozy-corner-81

# Inicializar Git (se ainda não tiver)
git init

# Adicionar arquivos
git add .

# Commit
git commit -m "Deploy: Alpha System v5.0"

# Criar repositório no GitHub e fazer push
git remote add origin https://github.com/SEU_USUARIO/alpha-system.git
git branch -M main
git push -u origin main
```

---

## 🌐 PASSO 2: DEPLOY NO RENDER

### 2.1 Criar conta no Render
1. Acesse https://render.com
2. Clique em "Get Started"
3. Faça login com GitHub

### 2.2 Conectar repositório
1. No dashboard, clique em "New +"
2. Selecione "Blueprint"
3. Conecte seu repositório GitHub
4. Render detectará automaticamente o `render.yaml`

### 2.3 Configurar variáveis de ambiente

No dashboard do Render, adicione as variáveis:

#### Backend Service
```env
# Groq (OBRIGATÓRIO)
GROQ_API_KEY_1=sua_chave_1
GROQ_API_KEY_2=sua_chave_2
GROQ_API_KEY_3=sua_chave_3
GROQ_API_KEY_4=sua_chave_4
GROQ_API_KEY_5=sua_chave_5
GROQ_API_KEY_6=sua_chave_6

# Brapi (OBRIGATÓRIO)
BRAPI_TOKEN_1=seu_token_1
BRAPI_TOKEN_2=seu_token_2
BRAPI_TOKEN_3=seu_token_3
BRAPI_TOKEN_4=seu_token_4
BRAPI_TOKEN_5=seu_token_5
BRAPI_TOKEN_6=seu_token_6
BRAPI_TOKEN_7=seu_token_7
BRAPI_TOKEN_8=seu_token_8
BRAPI_TOKEN_9=seu_token_9

# Senha Admin
ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3

# CORS (URL do frontend - será fornecida pelo Render)
FRONTEND_URL=https://seu-frontend.onrender.com
```

#### Frontend Service
```env
# URL do backend (será fornecida pelo Render)
VITE_API_URL=https://seu-backend.onrender.com
```

### 2.4 Deploy
1. Clique em "Apply"
2. Render começará o build automaticamente
3. Aguarde ~5-10 minutos

---

## 🔗 PASSO 3: CONFIGURAR URLS

### 3.1 Obter URLs
Após deploy, você terá:
- Backend: `https://alpha-backend-xxxx.onrender.com`
- Frontend: `https://alpha-frontend-xxxx.onrender.com`

### 3.2 Atualizar variáveis de ambiente

#### No Backend Service:
```env
FRONTEND_URL=https://alpha-frontend-xxxx.onrender.com
```

#### No Frontend Service:
```env
VITE_API_URL=https://alpha-backend-xxxx.onrender.com
```

### 3.3 Redeploy
1. Vá em cada service
2. Clique em "Manual Deploy" → "Deploy latest commit"

---

## ✅ PASSO 4: TESTAR

### 4.1 Acessar o sistema
1. Abra: `https://alpha-frontend-xxxx.onrender.com/admin`
2. Login com senha: `123`
3. Execute análise com consenso

### 4.2 Verificar logs
1. No dashboard do Render
2. Clique no Backend Service
3. Vá em "Logs"
4. Verifique se não há erros

---

## 🔄 ATUALIZAÇÕES

### Atualizar código
```bash
# Fazer mudanças no código
git add .
git commit -m "Atualização: descrição"
git push

# Render fará deploy automático
```

### Forçar redeploy
1. Dashboard do Render
2. Selecione o service
3. "Manual Deploy" → "Deploy latest commit"

---

## 💰 CUSTOS

### Plano Gratuito (Free Tier)
- ✅ Backend: 750 horas/mês
- ✅ Frontend: Ilimitado (static site)
- ✅ SSL/HTTPS automático
- ⚠️ Sleep após 15 min de inatividade
- ⚠️ Cold start: ~30s

### Plano Pago (Starter - $7/mês)
- ✅ Sem sleep
- ✅ Mais recursos
- ✅ Melhor performance

---

## 🐛 TROUBLESHOOTING

### Build falha
```bash
# Verificar logs no Render
# Comum: dependências faltando

# Solução: Atualizar requirements.txt
pip freeze > backend/requirements.txt
git add backend/requirements.txt
git commit -m "Fix: requirements"
git push
```

### CORS error
```bash
# Verificar FRONTEND_URL no backend
# Deve ser exatamente a URL do frontend

# Atualizar no Render:
# Backend Service → Environment → FRONTEND_URL
```

### Cold start lento
```bash
# Plano gratuito: normal (30s)
# Solução: Upgrade para Starter ($7/mês)
# Ou: Usar serviço de "keep alive" (ping a cada 10 min)
```

---

## 📊 MONITORAMENTO

### Logs
```bash
# Render Dashboard → Service → Logs
# Logs em tempo real
```

### Métricas
```bash
# Render Dashboard → Service → Metrics
# CPU, RAM, Requests
```

### Alertas
```bash
# Render Dashboard → Service → Settings → Notifications
# Email quando deploy falha
```

---

## 🔒 SEGURANÇA

### Variáveis de ambiente
- ✅ Nunca commite `.env`
- ✅ Use variáveis de ambiente do Render
- ✅ Rotacione chaves periodicamente

### HTTPS
- ✅ Automático no Render
- ✅ Certificado SSL gratuito

### Backup
```bash
# Fazer backup do .env localmente
# Guardar em local seguro
```

---

## 🎯 CHECKLIST FINAL

- [ ] Repositório no GitHub
- [ ] Conta no Render criada
- [ ] Blueprint aplicado
- [ ] Variáveis de ambiente configuradas
- [ ] URLs atualizadas (FRONTEND_URL, VITE_API_URL)
- [ ] Deploy bem-sucedido
- [ ] Sistema acessível
- [ ] Login funciona (senha: 123)
- [ ] Análise com consenso funciona

---

## 📞 SUPORTE

### Render
- Docs: https://render.com/docs
- Status: https://status.render.com
- Support: https://render.com/support

### Projeto
- Logs: Render Dashboard
- Issues: GitHub Issues
- Docs: README.md

---

**Tempo estimado**: 30 minutos  
**Dificuldade**: Fácil ⭐  
**Custo**: Gratuito (com limitações)  
**Status**: Produção ✅
