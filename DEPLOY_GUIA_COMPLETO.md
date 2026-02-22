# 🚀 GUIA COMPLETO DE DEPLOY - ALPHA SYSTEM

## 📋 ESCOLHA SUA PLATAFORMA

### 🟢 RENDER (RECOMENDADO - Mais Fácil)
- ✅ **Gratuito** (com limitações)
- ✅ **Fácil**: Deploy em 10 minutos
- ✅ **SSL automático**
- ⚠️ **Sleep**: 15 min de inatividade
- 📖 **Guia**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)

### 🔵 VPS (Mais Controle)
- ✅ **Sem limitações**
- ✅ **Performance**: Sempre ativo
- ✅ **Controle total**
- ⚠️ **Custo**: $5-10/mês
- ⚠️ **Complexo**: Requer conhecimento Linux
- 📖 **Guia**: [DEPLOY_VPS.md](DEPLOY_VPS.md)

---

## ⚡ DEPLOY RÁPIDO (RENDER)

### 1. Preparar Repositório
```bash
cd c:\Users\bonde\Alpha\blog-cozy-corner-81

# Inicializar Git
git init
git add .
git commit -m "Deploy: Alpha System v5.0"

# Criar repositório no GitHub
# https://github.com/new

# Push
git remote add origin https://github.com/SEU_USUARIO/alpha-system.git
git branch -M main
git push -u origin main
```

### 2. Deploy no Render
1. Acesse https://render.com
2. Login com GitHub
3. New + → Blueprint
4. Conecte seu repositório
5. Render detecta `render.yaml` automaticamente
6. Clique "Apply"

### 3. Configurar Variáveis
No dashboard do Render, adicione:

**Backend Service:**
```env
GROQ_API_KEY_1=sua_chave_1
GROQ_API_KEY_2=sua_chave_2
GROQ_API_KEY_3=sua_chave_3
GROQ_API_KEY_4=sua_chave_4
GROQ_API_KEY_5=sua_chave_5
GROQ_API_KEY_6=sua_chave_6

BRAPI_TOKEN_1=seu_token_1
BRAPI_TOKEN_2=seu_token_2
BRAPI_TOKEN_3=seu_token_3
BRAPI_TOKEN_4=seu_token_4
BRAPI_TOKEN_5=seu_token_5
BRAPI_TOKEN_6=seu_token_6
BRAPI_TOKEN_7=seu_token_7
BRAPI_TOKEN_8=seu_token_8
BRAPI_TOKEN_9=seu_token_9

ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3

FRONTEND_URL=https://seu-frontend.onrender.com
```

**Frontend Service:**
```env
VITE_API_URL=https://seu-backend.onrender.com
```

### 4. Atualizar URLs
Após primeiro deploy:
1. Copie URLs geradas pelo Render
2. Atualize `FRONTEND_URL` no backend
3. Atualize `VITE_API_URL` no frontend
4. Redeploy ambos os services

### 5. Testar
1. Acesse `https://seu-frontend.onrender.com/admin`
2. Login com senha: `123`
3. Execute análise com consenso

---

## 📁 ESTRUTURA DO PROJETO

```
blog-cozy-corner-81/
├── backend/                    # API FastAPI
│   ├── app/
│   │   ├── main.py            # Entrada
│   │   ├── routes/            # Endpoints
│   │   └── services/          # Lógica
│   ├── data/                  # Dados e cache
│   ├── .env                   # Configurações (NÃO COMMITAR!)
│   └── requirements.txt       # Dependências Python
├── src/                       # Frontend React
│   ├── components/            # Componentes
│   └── services/              # API client
├── render.yaml                # Config Render
├── DEPLOY_RENDER.md           # Guia Render
├── DEPLOY_VPS.md              # Guia VPS
└── README.md                  # Documentação
```

---

## 🔑 VARIÁVEIS DE AMBIENTE

### Backend (.env)
```env
# OBRIGATÓRIO
GROQ_API_KEY_1-6=...          # 6 chaves Groq
BRAPI_TOKEN_1-9=...           # 9 tokens Brapi
ADMIN_PASSWORD_HASH=...       # Hash da senha (padrão: "123")
FRONTEND_URL=...              # URL do frontend

# OPCIONAL
GEMINI_API_KEY=...            # Backup
ALPHAVANTAGE_API_KEY=...      # Backup preços
MISTRAL_API_KEY=...           # OCR PDFs
```

### Frontend (.env)
```env
VITE_API_URL=...              # URL do backend
```

---

## 🔄 ATUALIZAR CÓDIGO

### Render (Automático)
```bash
git add .
git commit -m "Atualização: descrição"
git push

# Render faz deploy automático
```

### VPS (Manual)
```bash
ssh alpha@SEU_IP
/home/alpha/update.sh
```

---

## 🐛 PROBLEMAS COMUNS

### Build falha
```bash
# Verificar logs no Render
# Ou localmente:
cd backend
pip install -r requirements.txt

cd ..
npm install
npm run build
```

### CORS error
```bash
# Verificar FRONTEND_URL no backend
# Deve ser exatamente a URL do frontend
```

### Cold start lento (Render)
```bash
# Normal no plano gratuito (~30s)
# Solução: Upgrade para Starter ($7/mês)
```

### Porta em uso (local)
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

---

## 💰 CUSTOS

### Render (Gratuito)
- ✅ Backend: 750h/mês
- ✅ Frontend: Ilimitado
- ⚠️ Sleep após 15 min
- ⚠️ Cold start: ~30s

### Render (Starter - $7/mês)
- ✅ Sem sleep
- ✅ Mais recursos
- ✅ Melhor performance

### VPS
- **DigitalOcean**: $6/mês
- **Linode**: $5/mês
- **Vultr**: $6/mês
- **Hetzner**: €4/mês

---

## 📊 MONITORAMENTO

### Render
- Dashboard → Service → Logs
- Dashboard → Service → Metrics
- Dashboard → Service → Settings → Notifications

### VPS
```bash
# Logs
sudo journalctl -u alpha-backend -f
sudo journalctl -u alpha-frontend -f

# Status
sudo systemctl status alpha-backend
sudo systemctl status alpha-frontend
```

---

## 🔒 SEGURANÇA

### Checklist
- [ ] `.env` NÃO está no Git
- [ ] `.gitignore` inclui `.env`
- [ ] Senha admin é hash SHA256
- [ ] API keys não estão hardcoded
- [ ] CORS configurado corretamente
- [ ] HTTPS habilitado (automático no Render)

### Backup
```bash
# Fazer backup do .env
# Guardar em local seguro
# Rotacionar chaves periodicamente
```

---

## ✅ CHECKLIST FINAL

### Pré-Deploy
- [ ] Código commitado no Git
- [ ] Repositório no GitHub
- [ ] API keys obtidas (Groq, Brapi)
- [ ] `.env.example` atualizado
- [ ] Documentação completa

### Deploy
- [ ] Plataforma escolhida (Render/VPS)
- [ ] Serviços criados
- [ ] Variáveis de ambiente configuradas
- [ ] URLs atualizadas
- [ ] Build bem-sucedido
- [ ] Deploy bem-sucedido

### Pós-Deploy
- [ ] Sistema acessível
- [ ] Login funciona (senha: 123)
- [ ] Análise com consenso funciona
- [ ] Upload de CSV funciona
- [ ] Upload de releases funciona
- [ ] Ranking atualiza
- [ ] Sem erros nos logs

---

## 📞 SUPORTE

### Documentação
- **Render**: https://render.com/docs
- **Vite**: https://vitejs.dev
- **FastAPI**: https://fastapi.tiangolo.com

### Projeto
- **README**: [README.md](README.md)
- **Deploy Render**: [DEPLOY_RENDER.md](DEPLOY_RENDER.md)
- **Deploy VPS**: [DEPLOY_VPS.md](DEPLOY_VPS.md)
- **Início Rápido**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Escolher plataforma (Render recomendado)
2. ✅ Seguir guia específico
3. ✅ Configurar variáveis de ambiente
4. ✅ Fazer deploy
5. ✅ Testar sistema
6. ✅ Monitorar logs
7. ✅ Fazer backup do .env

---

**Tempo estimado**: 30 minutos (Render) ou 2 horas (VPS)  
**Dificuldade**: Fácil (Render) ou Médio (VPS)  
**Custo**: Gratuito (Render) ou $5-10/mês (VPS)  
**Status**: Produção ✅
