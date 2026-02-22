# 🎯 COMECE AQUI - Alpha Terminal

> Guia rápido para iniciar o sistema em 5 minutos

---

## ⚡ Quick Start

### 1️⃣ Instale as Dependências

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ..
npm install
```

### 2️⃣ Inicie os Servidores

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

### 3️⃣ Acesse o Sistema

- **Terminal Principal:** http://localhost:8080
- **Admin Panel:** http://localhost:8080/admin (senha: `admin`)

---

## 📋 Primeiro Uso

### Passo 1: Faça Upload do CSV
1. Acesse http://localhost:8080/admin
2. Login com senha: `admin`
3. Faça upload de um CSV com colunas: `ticker`, `roe`, `pl`
4. Mínimo 50 ações

### Passo 2: Execute a Análise
1. No admin, clique em "Iniciar Análise"
2. Aguarde 3-5 minutos
3. Sistema analisa ~200 ações e retorna top 30

### Passo 3: Veja os Resultados
1. Acesse http://localhost:8080
2. Veja o ranking das melhores ações
3. Análise completa com IA

---

## 🔧 Configuração (Opcional)

### Chaves de API

O sistema já vem com 6 chaves Groq configuradas no `.env.example`.

Se quiser usar suas próprias chaves:

1. Copie `.env.example` para `.env`
2. Edite as chaves:
```bash
GROQ_API_KEY_1=sua_chave_aqui
GROQ_API_KEY_2=sua_chave_aqui
# ... até 6 chaves
```

### Senha Admin

Para mudar a senha do admin:

```bash
cd backend
python gerar_senha_admin.py
# Digite a nova senha
# Copie o hash gerado para .env
```

---

## 📚 Documentação Completa

Para informações detalhadas, consulte:

**[SISTEMA_COMPLETO_DOCUMENTACAO.md](./SISTEMA_COMPLETO_DOCUMENTACAO.md)**

Inclui:
- Arquitetura completa
- Fluxo do sistema
- Componentes críticos
- Problemas comuns e soluções
- API endpoints
- Design system

---

## 🆘 Problemas?

### Backend não inicia
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Frontend não inicia
```bash
# Limpe o cache e reinstale
rm -rf node_modules
npm install
```

### "CSV não encontrado"
- Faça upload do CSV no admin panel
- Sistema NÃO busca CSV automaticamente

### "Rate limit exceeded"
- Sistema já configurado com 6 chaves
- Rate limit ULTRA conservador (40% de capacidade)
- Erro não deve acontecer

---

## ✅ Checklist de Verificação

Antes de usar, verifique:

- [ ] Backend rodando na porta 8000
- [ ] Frontend rodando na porta 8080
- [ ] Admin acessível em /admin
- [ ] CSV com mínimo 50 ações
- [ ] Senha admin funcionando

---

## 🎨 Features Principais

### Admin Panel
- ✅ Upload de CSV com validação
- ✅ Gerenciamento de releases (PDFs)
- ✅ Auto-update a cada 30s (toggle ON/OFF)
- ✅ Dashboard com estatísticas
- ✅ Histórico de atualizações

### Sistema de Análise
- ✅ IA Multi-Provider (Groq com 6 chaves)
- ✅ Dados híbridos (yfinance + IA + Brapi)
- ✅ Zero mock data (100% real)
- ✅ Rate limit conservador (zero erros)
- ✅ Análise de ~200 ações em 3-5 minutos

### Design
- ✅ Green/Black theme profissional
- ✅ Responsivo (mobile + desktop)
- ✅ Componentes consistentes
- ✅ Animações suaves

---

## 📞 Próximos Passos

1. ✅ Inicie o sistema
2. ✅ Faça upload do CSV
3. ✅ Execute a análise
4. ✅ Veja os resultados
5. 📚 Leia a documentação completa
6. 🚀 Customize conforme necessário

---

**Versão:** 3.0 Final  
**Status:** Produção ✅  
**Tempo de setup:** ~5 minutos
