# ⚡ INÍCIO RÁPIDO - ALPHA SYSTEM

## 🚀 3 PASSOS PARA COMEÇAR

### 1️⃣ INSTALAR (5 minutos)
```bash
# Windows
INSTALAR.bat

# Linux/Mac
chmod +x INSTALAR.sh
./INSTALAR.sh
```

### 2️⃣ INICIAR (30 segundos)
```bash
# Windows
INICIAR.bat

# Linux/Mac
chmod +x INICIAR.sh
./INICIAR.sh
```

### 3️⃣ USAR
1. Abra: http://localhost:8080/admin
2. Login: senha `123`
3. Clique: "Passo 1 (1x) + Passo 2 (3x) - GROQ"
4. Aguarde: ~6-8 minutos
5. Pronto! ✅

---

## 📋 O QUE VOCÊ PRECISA

### Obrigatório
- Python 3.10+
- Node.js 18+
- Chaves Groq (6x) → https://console.groq.com
- Tokens Brapi (9x) → https://brapi.dev

### Opcional
- Chaves Gemini (backup)
- Chaves Alpha Vantage (backup)
- Chave Mistral (OCR de PDFs)

---

## 🔑 CONFIGURAR API KEYS

Edite `backend/.env`:
```env
# Groq (OBRIGATÓRIO)
GROQ_API_KEY_1=sua_chave_1
GROQ_API_KEY_2=sua_chave_2
# ... até GROQ_API_KEY_6

# Brapi (OBRIGATÓRIO)
BRAPI_TOKEN_1=seu_token_1
BRAPI_TOKEN_2=seu_token_2
# ... até BRAPI_TOKEN_9

# Senha Admin (JÁ CONFIGURADA)
ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

---

## 🎯 FLUXO DE USO

```
1. Análise com Consenso (6-8 min)
   ↓
2. Empresas Aprovadas (45 empresas)
   ↓
3. Upload de Releases (PDFs)
   ↓
4. Ranking Atualizado
   ↓
5. Visualizar no Frontend
```

---

## 📞 PROBLEMAS?

### Porta em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Reinstalar
```bash
INSTALAR.bat  # Windows
./INSTALAR.sh # Linux/Mac
```

### Verificar
```bash
VERIFICAR.bat # Windows
```

---

## 📚 DOCUMENTAÇÃO COMPLETA

- **README.md**: Visão geral
- **DEPLOY.md**: Guia completo
- **CHECKLIST_DEPLOY.md**: Checklist passo a passo

---

## ✅ PRONTO!

Sistema instalado e rodando em:
- **Admin**: http://localhost:8080/admin (senha: 123)
- **Frontend**: http://localhost:8080
- **API**: http://localhost:8000/docs

**Tempo total**: ~10 minutos  
**Dificuldade**: Fácil ⭐  
**Status**: Produção ✅
