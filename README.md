# 🚀 ALPHA SYSTEM - Sistema de Análise de Investimentos com IA

Sistema completo de análise de ações da B3 usando IA (Groq + Gemini) com consenso, releases trimestrais e ranking inteligente.

## ⚡ INÍCIO RÁPIDO

### 1. Instalar
```bash
# Windows
INSTALAR.bat

# Linux/Mac
chmod +x INSTALAR.sh
./INSTALAR.sh
```

### 2. Iniciar
```bash
# Windows
INICIAR.bat

# Linux/Mac
chmod +x INICIAR.sh
./INICIAR.sh
```

### 3. Acessar
- **Admin Panel**: http://localhost:8080/admin (senha: `123`)
- **Frontend**: http://localhost:8080
- **API Docs**: http://localhost:8000/docs

---

## 🎯 FUNCIONALIDADES

### ✅ Análise com Consenso
- Passo 1: Análise Macro (1x)
- Passo 2: Triagem CSV (3x com consenso)
- Rotação automática entre 6 chaves Groq
- Retry infinito até conseguir resposta

### ✅ Sistema de Releases
- Upload de PDFs trimestrais (Q1, Q2, Q3, Q4)
- Análise automática com IA
- Extração de catalisadores e riscos

### ✅ Ranking Inteligente
- Ordenação por nota (fundamentos + releases + catalisadores)
- Estratégia de entrada/stop/alvo
- Atualização automática de preços

### ✅ APIs Integradas
- **Groq**: 6 chaves com rotação (análise IA)
- **Brapi**: 9 tokens com rotação (preços B3)
- **Alpha Vantage**: 3 chaves (preços backup)
- **Mistral AI**: OCR de PDFs

---

## 📊 ARQUITETURA

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                      │
│  - Admin Panel (upload CSV/releases)                    │
│  - Ranking (visualização)                               │
│  - Detalhes de empresas                                 │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                      │
│  ┌─────────────────────────────────────────────────┐   │
│  │  CONSENSO SERVICE (Groq - 6 chaves)             │   │
│  │  - Passo 1: Análise Macro                       │   │
│  │  - Passo 2: Triagem CSV (3x consenso)           │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  ANÁLISE COM RELEASES (Groq)                    │   │
│  │  - Lê PDFs (Mistral OCR)                        │   │
│  │  - Analisa com IA                               │   │
│  │  - Gera ranking                                 │   │
│  └─────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────┐   │
│  │  PREÇOS SERVICE (Brapi - 9 tokens)              │   │
│  │  - Rotação automática                           │   │
│  │  - Cache de 5 minutos                           │   │
│  │  - Fallback Alpha Vantage                       │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 CONFIGURAÇÃO

### Arquivo: `backend/.env`

```env
# Groq (6 chaves para rotação)
GROQ_API_KEY_1=sua_chave_1
GROQ_API_KEY_2=sua_chave_2
GROQ_API_KEY_3=sua_chave_3
GROQ_API_KEY_4=sua_chave_4
GROQ_API_KEY_5=sua_chave_5
GROQ_API_KEY_6=sua_chave_6

# Brapi (9 tokens para preços)
BRAPI_TOKEN_1=seu_token_1
# ... até BRAPI_TOKEN_9

# Senha Admin (hash SHA256 de "123")
ADMIN_PASSWORD_HASH=a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3
```

---

## 📖 DOCUMENTAÇÃO

- **[DEPLOY.md](DEPLOY.md)**: Guia completo de deploy
- **[SISTEMA_ANALISE_INVESTIMENTOS.md](SISTEMA_ANALISE_INVESTIMENTOS.md)**: Documentação técnica
- **[CHANGELOG_V5.md](CHANGELOG_V5.md)**: Histórico de versões

---

## 🔐 SEGURANÇA

### Senha Admin
- **Padrão**: `123`
- **Hash**: SHA256 armazenado no `.env`
- **Mudar**: Edite `ADMIN_PASSWORD_HASH` no `.env`

### API Keys
- Todas as chaves estão no `.env` (não commitado)
- Use `.env.example` como template
- Nunca commite o `.env` real

---

## 🐛 TROUBLESHOOTING

### Porta em uso
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### Dependências
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
npm install
```

### Rate Limit
- Sistema usa 6 chaves Groq com rotação
- Delays automáticos entre execuções
- Retry infinito até conseguir

---

## 📈 FLUXO DE USO

### 1. Primeira Execução
```
1. Acesse Admin Panel (http://localhost:8080/admin)
2. Login com senha "123"
3. Clique "Passo 1 (1x) + Passo 2 (3x) - GROQ"
4. Aguarde ~6-8 minutos
5. Empresas aprovadas aparecem no painel
```

### 2. Upload de Releases
```
1. Selecione empresa aprovada
2. Faça upload do PDF (Q1, Q2, Q3, Q4)
3. Sistema analisa automaticamente
4. Ranking atualizado em tempo real
```

### 3. Visualizar Ranking
```
1. Acesse Frontend (http://localhost:8080)
2. Veja ranking ordenado por nota
3. Clique em empresa para detalhes
4. Veja estratégia (entrada/stop/alvo)
```

---

## 🚀 TECNOLOGIAS

### Backend
- **FastAPI**: Framework web
- **Groq**: IA para análise (6 chaves)
- **Mistral AI**: OCR de PDFs
- **Brapi**: Preços B3 (9 tokens)
- **Alpha Vantage**: Preços backup (3 chaves)

### Frontend
- **React**: UI framework
- **Vite**: Build tool
- **TailwindCSS**: Styling
- **shadcn/ui**: Componentes

### IA
- **Consenso**: 3 execuções com 2/3 aparições
- **Retry infinito**: Não desiste até conseguir
- **Rotação de chaves**: 6 chaves Groq

---

## 📊 MÉTRICAS

### Performance
- **Passo 1**: ~2-3s (1 execução)
- **Passo 2**: ~5-6 minutos (3 execuções × 90s delay)
- **Análise com release**: ~30s por empresa
- **Total**: ~6-8 minutos para consenso completo

### Capacidade
- **Groq**: 6 chaves × 30 req/min = 180 req/min
- **Brapi**: 9 tokens × rate limit = alta capacidade
- **Empresas**: Sem limite (todas que atendem critérios)

---

## 📝 LICENÇA

Proprietary - Todos os direitos reservados

---

## 👨‍💻 AUTOR

Sistema desenvolvido para análise automatizada de investimentos na B3.

**Versão**: 5.0  
**Data**: 2026-02-22  
**Status**: Produção ✅
