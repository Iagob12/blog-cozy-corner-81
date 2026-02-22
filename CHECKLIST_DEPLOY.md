# ✅ CHECKLIST DE DEPLOY - ALPHA SYSTEM

## 📋 PRÉ-DEPLOY

### Ambiente
- [ ] Python 3.10+ instalado
- [ ] Node.js 18+ instalado
- [ ] Git instalado
- [ ] Conexão com internet estável

### Arquivos
- [ ] `.env` configurado com todas as API keys
- [ ] `.gitignore` atualizado (não commitar `.env`)
- [ ] `README.md` presente
- [ ] `DEPLOY.md` presente
- [ ] Scripts de instalação (`INSTALAR.bat/sh`)
- [ ] Scripts de inicialização (`INICIAR.bat/sh`)

---

## 🔧 INSTALAÇÃO

### 1. Clonar Repositório
```bash
git clone <seu-repositorio>
cd blog-cozy-corner-81
```
- [ ] Repositório clonado
- [ ] Pasta correta

### 2. Executar Instalação
```bash
# Windows
INSTALAR.bat

# Linux/Mac
chmod +x INSTALAR.sh
./INSTALAR.sh
```
- [ ] Backend instalado (venv criado)
- [ ] Dependências Python instaladas
- [ ] Frontend instalado (node_modules criado)
- [ ] Dependências Node instaladas

### 3. Verificar Sistema
```bash
# Windows
VERIFICAR.bat
```
- [ ] Todas as verificações passaram
- [ ] Sem erros críticos

---

## 🔑 CONFIGURAÇÃO

### API Keys (backend/.env)

#### Groq (OBRIGATÓRIO)
- [ ] `GROQ_API_KEY_1` configurada
- [ ] `GROQ_API_KEY_2` configurada
- [ ] `GROQ_API_KEY_3` configurada
- [ ] `GROQ_API_KEY_4` configurada
- [ ] `GROQ_API_KEY_5` configurada
- [ ] `GROQ_API_KEY_6` configurada

#### Brapi (OBRIGATÓRIO)
- [ ] `BRAPI_TOKEN_1` configurado
- [ ] `BRAPI_TOKEN_2` configurado
- [ ] `BRAPI_TOKEN_3` configurado
- [ ] `BRAPI_TOKEN_4` configurado
- [ ] `BRAPI_TOKEN_5` configurado
- [ ] `BRAPI_TOKEN_6` configurado
- [ ] `BRAPI_TOKEN_7` configurado
- [ ] `BRAPI_TOKEN_8` configurado
- [ ] `BRAPI_TOKEN_9` configurado

#### Senha Admin (OBRIGATÓRIO)
- [ ] `ADMIN_PASSWORD_HASH` configurado
- [ ] Hash correto: `a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3` (senha: "123")

#### Outros (OPCIONAL)
- [ ] `GEMINI_API_KEY` configurada (backup)
- [ ] `ALPHAVANTAGE_API_KEY` configurada (backup)
- [ ] `MISTRAL_API_KEY` configurada (OCR de PDFs)

---

## 🚀 INICIALIZAÇÃO

### 1. Iniciar Sistema
```bash
# Windows
INICIAR.bat

# Linux/Mac
chmod +x INICIAR.sh
./INICIAR.sh
```
- [ ] Backend iniciado (porta 8000)
- [ ] Frontend iniciado (porta 8080)
- [ ] Sem erros no console

### 2. Verificar URLs
- [ ] Backend: http://localhost:8000 (responde)
- [ ] API Docs: http://localhost:8000/docs (abre)
- [ ] Frontend: http://localhost:8080 (carrega)
- [ ] Admin Panel: http://localhost:8080/admin (carrega)

### 3. Testar Login
- [ ] Acessa http://localhost:8080/admin
- [ ] Login com senha "123" funciona
- [ ] Painel admin carrega corretamente

---

## 🧪 TESTES FUNCIONAIS

### 1. Análise com Consenso
- [ ] Botão "Passo 1 (1x) + Passo 2 (3x) - GROQ" visível
- [ ] Clica no botão
- [ ] Mensagem de sucesso aparece
- [ ] Logs aparecem no terminal do backend
- [ ] Passo 1 completa (~2-3s)
- [ ] Delay de 60s entre passos
- [ ] Passo 2 inicia (3 execuções)
- [ ] Empresas aprovadas aparecem no painel (~6-8 min)

### 2. Upload de CSV
- [ ] Botão de upload visível
- [ ] Seleciona arquivo CSV
- [ ] Upload bem-sucedido
- [ ] Total de ações atualizado
- [ ] Sem erros

### 3. Upload de Release
- [ ] Empresas aprovadas listadas
- [ ] Seleciona empresa
- [ ] Seleciona trimestre (Q1/Q2/Q3/Q4)
- [ ] Seleciona ano
- [ ] Upload de PDF funciona
- [ ] Mensagem de sucesso

### 4. Visualizar Ranking
- [ ] Acessa http://localhost:8080
- [ ] Ranking carrega
- [ ] Empresas ordenadas por nota
- [ ] Clica em empresa
- [ ] Detalhes aparecem
- [ ] Estratégia visível (entrada/stop/alvo)

---

## 🔒 SEGURANÇA

### Verificações
- [ ] `.env` NÃO está no git
- [ ] `.gitignore` inclui `.env`
- [ ] Senha admin é hash SHA256
- [ ] API keys não estão hardcoded no código
- [ ] CORS configurado corretamente

### Backup
- [ ] Backup do `.env` em local seguro
- [ ] Backup das API keys
- [ ] Documentação de senhas

---

## 📊 MONITORAMENTO

### Logs
- [ ] Backend: Logs aparecem no terminal
- [ ] Frontend: Logs aparecem no console do navegador
- [ ] Erros são visíveis e claros

### Performance
- [ ] Backend responde em < 1s
- [ ] Frontend carrega em < 3s
- [ ] Análise completa em ~6-8 min
- [ ] Sem travamentos

---

## 🐛 TROUBLESHOOTING

### Problemas Comuns
- [ ] Porta 8000 livre (backend)
- [ ] Porta 8080 livre (frontend)
- [ ] Firewall não bloqueia
- [ ] Antivírus não bloqueia

### Soluções
- [ ] Documentação de erros comuns
- [ ] Comandos de debug disponíveis
- [ ] Logs detalhados habilitados

---

## 📝 DOCUMENTAÇÃO

### Arquivos Criados
- [ ] `README.md` - Visão geral
- [ ] `DEPLOY.md` - Guia de deploy
- [ ] `CHECKLIST_DEPLOY.md` - Este arquivo
- [ ] `INSTALAR.bat/sh` - Script de instalação
- [ ] `INICIAR.bat/sh` - Script de inicialização
- [ ] `VERIFICAR.bat` - Script de verificação

### Conteúdo
- [ ] Instruções claras
- [ ] Exemplos práticos
- [ ] Troubleshooting
- [ ] URLs e credenciais

---

## ✅ DEPLOY COMPLETO

### Checklist Final
- [ ] Todos os itens acima verificados
- [ ] Sistema funcionando 100%
- [ ] Documentação completa
- [ ] Backup realizado
- [ ] Equipe treinada (se aplicável)

### Próximos Passos
1. [ ] Monitorar logs por 24h
2. [ ] Executar análise completa
3. [ ] Testar todos os fluxos
4. [ ] Documentar problemas encontrados
5. [ ] Ajustar configurações se necessário

---

## 📞 SUPORTE

### Em caso de problemas:
1. Verificar logs do backend
2. Verificar logs do frontend
3. Consultar `DEPLOY.md`
4. Verificar `.env` configurado
5. Reiniciar sistema

### Comandos úteis:
```bash
# Parar sistema
Ctrl+C (em cada terminal)

# Limpar cache
rm -rf backend/data/cache/*

# Reinstalar
INSTALAR.bat/sh

# Verificar
VERIFICAR.bat
```

---

**Data**: 2026-02-22  
**Versão**: 5.0  
**Status**: ✅ Pronto para Deploy
