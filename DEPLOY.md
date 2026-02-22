# 🚀 GUIA DE DEPLOY - ALPHA SYSTEM

## 📋 PRÉ-REQUISITOS

### Obrigatórios
- Python 3.10+ instalado
- Node.js 18+ instalado
- Git instalado

### Verificar instalação
```bash
python --version  # Deve ser 3.10+
node --version    # Deve ser 18+
npm --version
```

---

## 🔧 INSTALAÇÃO RÁPIDA

### 1. Clone o repositório (se ainda não tiver)
```bash
git clone <seu-repositorio>
cd blog-cozy-corner-81
```

### 2. Execute o script de instalação

**Windows:**
```bash
.\INSTALAR.bat
```

**Linux/Mac:**
```bash
chmod +x INSTALAR.sh
./INSTALAR.sh
```

---

## 🚀 INICIAR O SISTEMA

### Opção 1: Script Automático (RECOMENDADO)

**Windows:**
```bash
.\INICIAR.bat
```

**Linux/Mac:**
```bash
chmod +x INICIAR.sh
./INICIAR.sh
```

Este script inicia automaticamente:
- ✅ Backend (FastAPI) na porta 8000
- ✅ Frontend (React) na porta 8080
- ✅ Sistema de IA com consenso

### Opção 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level warning
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

---

## 🔐 ACESSO AO SISTEMA

### URLs
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Admin Panel**: http://localhost:8080/admin
- **API Docs**: http://localhost:8000/docs

### Credenciais Admin
- **Senha**: `123`
- **Nota**: Esta senha está hardcoded no sistema. Para mudar, edite `backend/.env`

---

## 📊 FLUXO DE USO

### 1. Primeiro Acesso
1. Acesse http://localhost:8080/admin
2. Faça login com senha `123`
3. Clique em "Passo 1 (1x) + Passo 2 (3x) - GROQ"
4. Aguarde ~6-8 minutos (análise com consenso)

### 2. Upload de Releases
1. Após análise, empresas aprovadas aparecem no painel
2. Faça upload dos PDFs de releases (Q1, Q2, Q3, Q4)
3. Sistema atualiza ranking automaticamente

### 3. Visualizar Ranking
1. Acesse http://localhost:8080
2. Veja ranking atualizado em tempo real
3. Clique em empresas para ver detalhes

---

## 🔑 CONFIGURAÇÃO DE API KEYS

### Arquivo: `backend/.env`

```env
# Groq (PRINCIPAL - 6 chaves)
GROQ_API_KEY_1=sua_chave_1
GROQ_API_KEY_2=sua_chave_2
GROQ_API_KEY_3=sua_chave_3
GROQ_API_KEY_4=sua_chave_4
GROQ_API_KEY_5=sua_chave_5
GROQ_API_KEY_6=sua_chave_6

# Brapi (9 tokens para preços)
BRAPI_TOKEN_1=sua_chave_1
BRAPI_TOKEN_2=sua_chave_2
# ... até BRAPI_TOKEN_9

# Senha Admin (hash SHA256 de "123")
ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

---

## 🛠️ COMANDOS ÚTEIS

### Parar o sistema
```bash
# Windows: Ctrl+C em cada terminal
# Linux/Mac: Ctrl+C em cada terminal
```

### Limpar cache
```bash
cd backend
rm -rf data/cache/*
```

### Reinstalar dependências
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
npm install
```

### Ver logs do backend
```bash
cd backend
tail -f logs/app.log  # Linux/Mac
Get-Content logs/app.log -Wait  # Windows PowerShell
```

---

## 📁 ESTRUTURA DO PROJETO

```
blog-cozy-corner-81/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── main.py         # Entrada principal
│   │   ├── routes/         # Endpoints
│   │   └── services/       # Lógica de negócio
│   ├── data/               # Dados e cache
│   ├── .env                # Configurações (API keys)
│   └── requirements.txt    # Dependências Python
├── src/                    # Frontend React
│   ├── components/         # Componentes React
│   └── services/           # API client
├── INSTALAR.bat/sh         # Script de instalação
├── INICIAR.bat/sh          # Script de inicialização
└── DEPLOY.md              # Este arquivo
```

---

## 🐛 TROUBLESHOOTING

### Erro: "Port 8000 already in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Erro: "Module not found"
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
npm install
```

### Erro: "CORS policy"
- Verifique se backend está rodando na porta 8000
- Verifique se frontend está rodando na porta 8080

### Erro: "Rate limit exceeded"
- Sistema usa 6 chaves Groq com rotação automática
- Aguarde 60s entre execuções
- Verifique se todas as chaves estão configuradas no `.env`

---

## 📈 MONITORAMENTO

### Logs importantes
- Backend: Terminal onde rodou `uvicorn`
- Frontend: Terminal onde rodou `npm run dev`
- Análise IA: Logs aparecem no terminal do backend

### Métricas
- Total de empresas aprovadas: Admin Panel
- Ranking atualizado: Frontend principal
- Status das chaves: Logs do backend

---

## 🔄 ATUALIZAÇÃO

### Atualizar código
```bash
git pull origin main
```

### Atualizar dependências
```bash
# Backend
cd backend
pip install -r requirements.txt --upgrade

# Frontend
npm install
```

### Reiniciar sistema
```bash
# Parar (Ctrl+C)
# Iniciar novamente
.\INICIAR.bat  # Windows
./INICIAR.sh   # Linux/Mac
```

---

## 📞 SUPORTE

### Problemas comuns
1. **Sistema lento**: Verifique conexão com internet (APIs externas)
2. **Análise falha**: Verifique chaves Groq no `.env`
3. **Ranking vazio**: Execute análise com consenso primeiro

### Logs detalhados
```bash
cd backend
python -m uvicorn app.main:app --reload --log-level debug
```

---

## ✅ CHECKLIST DE DEPLOY

- [ ] Python 3.10+ instalado
- [ ] Node.js 18+ instalado
- [ ] Dependências instaladas (`INSTALAR.bat/sh`)
- [ ] Arquivo `.env` configurado com API keys
- [ ] Senha admin configurada (padrão: "123")
- [ ] Backend iniciado (porta 8000)
- [ ] Frontend iniciado (porta 8080)
- [ ] Análise com consenso executada
- [ ] Empresas aprovadas visíveis no admin
- [ ] Ranking visível no frontend

---

## 🎯 PRÓXIMOS PASSOS

1. ✅ Sistema instalado e rodando
2. ✅ Análise com consenso executada
3. ⏳ Upload de releases no admin panel
4. ⏳ Visualizar ranking atualizado
5. ⏳ Monitorar alertas e oportunidades

---

**Versão**: 5.0  
**Última atualização**: 2026-02-22  
**Status**: Produção
