# 🚀 DEPLOY AGORA - COMANDOS PRONTOS

Execute estes comandos para fazer deploy AGORA!

## 📋 PRÉ-REQUISITOS

- [ ] Conta no GitHub
- [ ] Conta no Render (https://render.com)
- [ ] Chaves Groq (6x) - https://console.groq.com
- [ ] Tokens Brapi (9x) - https://brapi.dev

---

## ⚡ PASSO 1: PREPARAR GIT

Abra o PowerShell e execute:

```powershell
# Ir para a pasta do projeto
cd c:\Users\bonde\Alpha\blog-cozy-corner-81

# Inicializar Git (se ainda não tiver)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "Deploy: Alpha System v5.0 - Sistema completo de análise de investimentos"

# Ver status
git status
```

---

## 🌐 PASSO 2: CRIAR REPOSITÓRIO NO GITHUB

1. Acesse: https://github.com/new
2. Nome: `alpha-system`
3. Descrição: `Sistema de análise de investimentos com IA`
4. Visibilidade: **Private** (recomendado)
5. Clique: "Create repository"

---

## 📤 PASSO 3: FAZER PUSH

Copie os comandos que o GitHub mostrar, ou use estes:

```powershell
# Adicionar remote (SUBSTITUA SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/alpha-system.git

# Renomear branch para main
git branch -M main

# Push
git push -u origin main
```

Se pedir autenticação:
- Use Personal Access Token (não senha)
- Gere em: https://github.com/settings/tokens

---

## 🎨 PASSO 4: DEPLOY NO RENDER

### 4.1 Criar conta
1. Acesse: https://render.com
2. Clique: "Get Started"
3. Login com GitHub

### 4.2 Criar Blueprint
1. Dashboard → "New +" → "Blueprint"
2. Conecte seu repositório GitHub
3. Selecione: `alpha-system`
4. Render detecta `render.yaml` automaticamente
5. Clique: "Apply"

### 4.3 Aguardar build
- Backend: ~5 minutos
- Frontend: ~3 minutos
- Total: ~8 minutos

---

## 🔑 PASSO 5: CONFIGURAR VARIÁVEIS

### 5.1 Backend Service

No Render Dashboard:
1. Clique no service "alpha-backend"
2. Vá em "Environment"
3. Adicione estas variáveis:

```env
GROQ_API_KEY_1=SUA_CHAVE_GROQ_1
GROQ_API_KEY_2=SUA_CHAVE_GROQ_2
GROQ_API_KEY_3=SUA_CHAVE_GROQ_3
GROQ_API_KEY_4=SUA_CHAVE_GROQ_4
GROQ_API_KEY_5=SUA_CHAVE_GROQ_5
GROQ_API_KEY_6=SUA_CHAVE_GROQ_6

BRAPI_TOKEN_1=SEU_TOKEN_BRAPI_1
BRAPI_TOKEN_2=SEU_TOKEN_BRAPI_2
BRAPI_TOKEN_3=SEU_TOKEN_BRAPI_3
BRAPI_TOKEN_4=SEU_TOKEN_BRAPI_4
BRAPI_TOKEN_5=SEU_TOKEN_BRAPI_5
BRAPI_TOKEN_6=SEU_TOKEN_BRAPI_6
BRAPI_TOKEN_7=SEU_TOKEN_BRAPI_7
BRAPI_TOKEN_8=SEU_TOKEN_BRAPI_8
BRAPI_TOKEN_9=SEU_TOKEN_BRAPI_9

ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3

FRONTEND_URL=https://alpha-frontend-XXXX.onrender.com
```

**IMPORTANTE**: Substitua `XXXX` pela URL real do frontend (veja no passo 5.3)

### 5.2 Frontend Service

1. Clique no service "alpha-frontend"
2. Vá em "Environment"
3. Adicione:

```env
VITE_API_URL=https://alpha-backend-XXXX.onrender.com
```

**IMPORTANTE**: Substitua `XXXX` pela URL real do backend (veja no passo 5.3)

### 5.3 Obter URLs

Após primeiro deploy:
- Backend: Clique no service → Copie a URL (ex: `https://alpha-backend-abc123.onrender.com`)
- Frontend: Clique no service → Copie a URL (ex: `https://alpha-frontend-xyz789.onrender.com`)

### 5.4 Atualizar e Redeploy

1. Atualize `FRONTEND_URL` no backend com a URL do frontend
2. Atualize `VITE_API_URL` no frontend com a URL do backend
3. Clique "Save Changes" em cada service
4. Render fará redeploy automático

---

## ✅ PASSO 6: TESTAR

### 6.1 Acessar sistema
```
URL: https://alpha-frontend-XXXX.onrender.com/admin
Senha: 123
```

### 6.2 Executar análise
1. Login com senha `123`
2. Clique: "Passo 1 (1x) + Passo 2 (3x) - GROQ"
3. Aguarde: ~6-8 minutos
4. Empresas aprovadas aparecem

### 6.3 Verificar logs
1. Render Dashboard
2. Clique no "alpha-backend"
3. Vá em "Logs"
4. Veja progresso em tempo real

---

## 🎉 PRONTO!

Seu sistema está no ar!

### URLs
- **Admin**: `https://alpha-frontend-XXXX.onrender.com/admin`
- **Frontend**: `https://alpha-frontend-XXXX.onrender.com`
- **API**: `https://alpha-backend-XXXX.onrender.com`
- **Docs**: `https://alpha-backend-XXXX.onrender.com/docs`

### Credenciais
- **Senha**: `123`

### Próximos passos
1. ✅ Fazer upload de CSV
2. ✅ Fazer upload de releases (PDFs)
3. ✅ Visualizar ranking
4. ✅ Compartilhar com usuários

---

## 🔄 ATUALIZAR CÓDIGO

Quando fizer mudanças:

```powershell
cd c:\Users\bonde\Alpha\blog-cozy-corner-81

git add .
git commit -m "Atualização: descrição da mudança"
git push

# Render faz deploy automático!
```

---

## 🐛 PROBLEMAS?

### Build falha
1. Veja logs no Render
2. Verifique `requirements.txt` e `package.json`
3. Teste localmente: `INSTALAR.bat` e `INICIAR.bat`

### CORS error
1. Verifique `FRONTEND_URL` no backend
2. Deve ser exatamente a URL do frontend
3. Sem barra no final

### Cold start lento
1. Normal no plano gratuito (~30s)
2. Primeira requisição após 15 min de inatividade
3. Solução: Upgrade para Starter ($7/mês)

---

## 📞 AJUDA

### Documentação
- **Guia Completo**: [DEPLOY_GUIA_COMPLETO.md](DEPLOY_GUIA_COMPLETO.md)
- **Render**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
- **VPS**: [DEPLOY_VPS.md](DEPLOY_VPS.md)

### Suporte
- **Render Docs**: https://render.com/docs
- **Render Status**: https://status.render.com
- **GitHub Issues**: Crie issue no seu repositório

---

**Tempo total**: 30 minutos  
**Dificuldade**: Fácil ⭐  
**Custo**: Gratuito  
**Status**: Produção ✅

**BOA SORTE! 🚀**
