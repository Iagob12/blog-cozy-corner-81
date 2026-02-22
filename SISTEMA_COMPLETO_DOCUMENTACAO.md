# 📚 DOCUMENTAÇÃO COMPLETA DO SISTEMA ALPHA TERMINAL

> **Última atualização:** 20/02/2026  
> **Versão:** 3.0 Final  
> **Status:** Produção

---

## 🎯 VISÃO GERAL

Sistema de análise de investimentos em ações brasileiras que combina:
- **IA Multi-Provider** (Groq com 6 chaves rotativas)
- **Dados Fundamentalistas** (yfinance + IA + Brapi)
- **Admin Panel** (Upload CSV + Releases + Auto-update)
- **Zero Mock Data** (100% dados reais ou erro explícito)

---

## 🏗️ ARQUITETURA

### Stack Tecnológico
```
Frontend: React + TypeScript + Vite + TailwindCSS
Backend: FastAPI + Python 3.11+
IA: Groq (6 chaves rotativas, modelo llama-3.3-70b-versatile)
Dados: yfinance + Brapi.dev + CSV manual
Design: Green/Black theme, Space Grotesk/Inter/JetBrains Mono
```

### Estrutura de Pastas
```
blog-cozy-corner-81/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app + SafeJSONResponse
│   │   ├── routes/
│   │   │   └── admin.py               # Rotas admin (CSV + Releases)
│   │   ├── services/
│   │   │   ├── multi_groq_client.py   # Cliente Groq com 6 chaves
│   │   │   ├── alpha_system_v3.py     # Sistema principal de análise
│   │   │   ├── dados_fundamentalistas_service.py  # yfinance + IA
│   │   │   ├── csv_manager.py         # Gerenciador de CSV
│   │   │   ├── auth_service.py        # Autenticação admin
│   │   │   └── release_manager.py     # Gerenciador de releases
│   │   └── utils/
│   │       └── json_sanitizer.py      # Sanitiza NaN/Infinity
│   └── data/
│       ├── stocks.csv                 # CSV principal (admin upload)
│       └── releases/                  # PDFs de releases
├── src/
│   ├── components/
│   │   ├── admin/
│   │   │   ├── AdminPanel.tsx         # Painel admin completo
│   │   │   └── ReleasesSection.tsx    # Seção de releases
│   │   └── alpha/
│   │       └── AlphaTerminal.tsx      # Terminal principal
│   └── App.tsx
└── .env                               # Variáveis de ambiente
```

---

## 🔑 CONFIGURAÇÃO

### Variáveis de Ambiente (.env)

```bash
# === GROQ API KEYS (6 chaves rotativas) ===
GROQ_API_KEY_1=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
GROQ_API_KEY_2=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
GROQ_API_KEY_3=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
GROQ_API_KEY_4=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
GROQ_API_KEY_5=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
GROQ_API_KEY_6=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

# === BRAPI (Preços de ações BR - Gratuito) ===
BRAPI_TOKEN=9s8J4vWFeh8BwDFvoYSj6T

# === ADMIN ===
ADMIN_PASSWORD_HASH=<gerado por gerar_senha_admin.py>

# === FRONTEND ===
VITE_API_URL=http://localhost:8000
```

### Senha Admin
```bash
# Gerar hash da senha
cd backend
python gerar_senha_admin.py

# Senha padrão: "admin"
```

---

## 🚀 COMO RODAR

### Backend
```bash
cd blog-cozy-corner-81/backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd blog-cozy-corner-81
npm install
npm run dev
# Abre em http://localhost:8080
```

### Acessar Admin
```
URL: http://localhost:8080/admin
Senha: admin
```

---

## 📊 FLUXO DO SISTEMA

### 1. Sistema Principal (Alpha System V3)

```
┌─────────────────────────────────────────────────────────────┐
│ FLUXO COMPLETO DE ANÁLISE                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. PROMPT 1: Radar de Oportunidades (Groq)                 │
│    └─> Identifica setores em aceleração                    │
│                                                             │
│ 2. CARREGA CSV (data/stocks.csv)                           │
│    └─> APENAS se admin fez upload                          │
│    └─> Se não existe: ERRO (não busca automaticamente)     │
│                                                             │
│ 3. PROMPT 2: Triagem Fundamentalista (Groq)                │
│    └─> Analisa TODAS as ~200 ações do CSV                  │
│    └─> Considera setores do Prompt 1                       │
│    └─> Retorna ~30 empresas aprovadas                      │
│                                                             │
│ 4. BUSCA DADOS FUNDAMENTALISTAS (Híbrido)                  │
│    └─> yfinance: Dados financeiros (ROE, P/L, etc)         │
│    └─> IA (Groq): Análise de contexto                      │
│    └─> Brapi: Preços atuais (APENAS das ~30 aprovadas)     │
│                                                             │
│ 5. PROMPT 3: Análise Profunda (Groq)                       │
│    └─> Analisa cada empresa com releases (se disponível)   │
│    └─> Gera recomendações finais                           │
│                                                             │
│ 6. RETORNA RANKING FINAL                                   │
│    └─> Top 15 ações com scores e recomendações             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2. Admin Panel

```
┌─────────────────────────────────────────────────────────────┐
│ FUNCIONALIDADES DO ADMIN                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. UPLOAD DE CSV                                            │
│    ├─> Validação: mínimo 50 ações                          │
│    ├─> Colunas obrigatórias: ticker, roe, pl               │
│    ├─> Backup automático do CSV anterior                   │
│    ├─> Normalização de colunas (ROE/roe/Roe → roe)         │
│    └─> Histórico de uploads com timestamp                  │
│                                                             │
│ 2. GERENCIAMENTO DE RELEASES                                │
│    ├─> Upload de PDFs por empresa                          │
│    ├─> Formato: TICKER_Q4_2025.pdf                         │
│    ├─> Validação de trimestre e ano                        │
│    ├─> Lista de empresas pendentes                         │
│    └─> Remoção de releases antigos                         │
│                                                             │
│ 3. AUTO-UPDATE (Toggle ON/OFF)                             │
│    ├─> Atualiza dados a cada 30 segundos                   │
│    ├─> Estado persistido no localStorage                   │
│    ├─> Mantém preferência após reload/logout               │
│    └─> Indicador visual quando ativo                       │
│                                                             │
│ 4. DASHBOARD                                                │
│    ├─> Status do CSV (idade, total de ações)               │
│    ├─> Empresas aprovadas pela IA                          │
│    ├─> Chaves Groq disponíveis                             │
│    └─> Histórico de atualizações                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 COMPONENTES CRÍTICOS

### 1. SafeJSONResponse (main.py)

**Problema:** FastAPI não serializa NaN/Infinity para JSON, causando crashes.

**Solução:**
```python
class SafeJSONResponse(FastAPIJSONResponse):
    def render(self, content: Any) -> bytes:
        safe_content = sanitize_for_json(content)
        return json.dumps(
            safe_content,
            ensure_ascii=False,
            allow_nan=False,  # CRÍTICO
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")

# Configurado como default
app = FastAPI(default_response_class=SafeJSONResponse)
```

### 2. Multi Groq Client (multi_groq_client.py)

**Rotação de 6 chaves com rate limit ULTRA conservador:**

```python
CONFIGURAÇÃO:
- 6 chaves Groq
- 2 requisições paralelas (máx)
- 2 segundos de delay entre requisições
- 40% de capacidade (conservador)
- 120 segundos de cooldown se erro
- Contexto persistente entre chaves
```

**Benefícios:**
- Zero erros de rate limit
- Sistema nunca para (se uma chave falha, usa outra)
- Contexto mantido entre requisições

### 3. Admin Panel Auto-Update (AdminPanel.tsx)

**Implementação com persistência:**

```typescript
// Estado inicial do localStorage
const [autoUpdate, setAutoUpdate] = useState(() => {
  const saved = localStorage.getItem('admin_auto_update');
  return saved === 'true';
});

// Salva automaticamente quando muda
useEffect(() => {
  localStorage.setItem('admin_auto_update', autoUpdate.toString());
}, [autoUpdate]);

// Intervalo de 30s quando ON
useEffect(() => {
  if (!autoUpdate || !token) return;
  
  // Carrega dados imediatamente
  loadData();
  
  // Depois a cada 30s
  const interval = setInterval(loadData, 30000);
  
  return () => clearInterval(interval);
}, [autoUpdate, token]);
```

### 4. Sistema Híbrido de Dados (dados_fundamentalistas_service.py)

**Combinação de 3 fontes:**

```python
1. yfinance (Dados financeiros)
   └─> ROE, P/L, Dívida, Margem, etc.

2. IA Groq (Análise de contexto)
   └─> Interpreta dados, identifica tendências

3. Brapi (Preços atuais)
   └─> APENAS para empresas aprovadas (~30)
   └─> Economia de 85% de requisições
```

---

## ⚠️ REGRAS CRÍTICAS

### 1. NUNCA Use Mock Data
```python
# ❌ ERRADO
if not data:
    return mock_data()

# ✅ CORRETO
if not data:
    raise HTTPException(
        status_code=503,
        detail="Dados não disponíveis. Faça upload do CSV no admin."
    )
```

### 2. SEMPRE Sanitize JSON
```python
# Todos os endpoints devem usar SafeJSONResponse
# NaN, Infinity, -Infinity → 0
```

### 3. CSV é OBRIGATÓRIO
```python
# Sistema NÃO busca CSV automaticamente
# Admin DEVE fazer upload manualmente
# Se não existe: ERRO explícito
```

### 4. Rate Limits ULTRA Conservadores
```python
# Groq: 40% de capacidade, 2s delay
# Brapi: APENAS empresas aprovadas (~30)
# yfinance: Sem limite, mas com timeout
```

### 5. Design Consistente
```css
/* Admin Panel DEVE ter mesmo design do site principal */
- Cores: Green (#00ff41) / Black (#0a0a0a)
- Fontes: Space Grotesk / Inter / JetBrains Mono
- Componentes: alpha-card, alpha-button, etc.
```

---

## 🐛 PROBLEMAS COMUNS E SOLUÇÕES

### 1. "NaN is not valid JSON"
**Causa:** Dados financeiros com NaN/Infinity  
**Solução:** SafeJSONResponse já implementado em main.py

### 2. "Rate limit exceeded"
**Causa:** Muitas requisições para Groq  
**Solução:** Multi Groq Client com 6 chaves e delays

### 3. "CSV não encontrado"
**Causa:** Admin não fez upload  
**Solução:** Mostrar erro explícito, não buscar automaticamente

### 4. "Toggle não funciona"
**Causa:** Estado não persistido ou intervalo não limpo  
**Solução:** localStorage + cleanup correto do useEffect

### 5. "Empresas aprovadas vazio"
**Causa:** Análise não foi executada  
**Solução:** Verificar se data/empresas_aprovadas.json existe

---

## 📁 ARQUIVOS DE DADOS

### data/stocks.csv
```csv
ticker,roe,pl,cagr,setor
PRIO3,35.2,8.5,18.5,Energia
VULC3,50.1,6.2,15.3,Consumo
...
```

### data/empresas_aprovadas.json
```json
{
  "timestamp": "2026-02-20T15:30:00",
  "total": 30,
  "empresas": ["PRIO3", "VULC3", ...],
  "detalhes": [...]
}
```

### data/releases/PRIO3_Q4_2025.pdf
```
Releases organizados por ticker e trimestre
```

---

## 🔐 SEGURANÇA

### Autenticação Admin
```python
# Hash bcrypt da senha
# Token JWT com expiração de 24h
# Validação em todas as rotas admin
```

### Proteção de Rotas
```typescript
// Frontend: Redirect se não autenticado
if (!isAuthenticated) {
  return <LoginScreen />;
}
```

### Sanitização de Dados
```python
# Todos os inputs validados
# CSV: mínimo 50 ações, colunas obrigatórias
# Releases: apenas PDFs, validação de trimestre
```

---

## 📈 PERFORMANCE

### Otimizações Implementadas

1. **Cache Global** (main.py)
   - Análise roda 1x quando backend inicia
   - Cache válido por 1 hora
   - Serve para todos os usuários

2. **Brapi Otimizado**
   - Busca preços APENAS de ~30 empresas aprovadas
   - Economia de 85% de requisições (antes: ~200, agora: ~30)
   - Tempo reduzido de ~20s para ~3s

3. **Rate Limit Conservador**
   - 40% de capacidade das chaves Groq
   - Zero erros de rate limit
   - Sistema nunca para

4. **Auto-Update Inteligente**
   - Apenas quando toggle ON
   - Intervalo de 30s (não sobrecarrega)
   - Cleanup correto quando desliga

---

## 🎨 DESIGN SYSTEM

### Cores
```css
--primary: #00ff41 (green)
--background: #0a0a0a (black)
--foreground: #ffffff (white)
--muted: #1a1a1a (dark gray)
--border: #2a2a2a (gray)
--alpha-green: #00ff41
--alpha-red: #ff0040
--alpha-blue: #0080ff
--alpha-amber: #ffaa00
```

### Tipografia
```css
--font-display: 'Space Grotesk' (headings)
--font-body: 'Inter' (body text)
--font-mono: 'JetBrains Mono' (code/numbers)
```

### Componentes
```css
.alpha-card: Card com border green e background dark
.alpha-button: Button com hover effect
.alpha-badge: Badge com cores temáticas
```

---

## 🔄 FLUXO DE DESENVOLVIMENTO

### Adicionar Nova Feature

1. **Backend**
   ```python
   # 1. Criar serviço em app/services/
   # 2. Adicionar rota em app/routes/
   # 3. Testar com curl/Postman
   # 4. Adicionar ao main.py
   ```

2. **Frontend**
   ```typescript
   // 1. Criar componente em src/components/
   // 2. Adicionar rota em App.tsx
   // 3. Testar no navegador
   // 4. Verificar design consistency
   ```

3. **Integração**
   ```bash
   # 1. Testar backend + frontend juntos
   # 2. Verificar erros no console
   # 3. Testar edge cases
   # 4. Documentar mudanças
   ```

### Debugging

```bash
# Backend logs
tail -f backend/logs/app.log

# Frontend console
F12 → Console

# Network requests
F12 → Network → Filter: XHR

# React DevTools
Instalar extensão React DevTools
```

---

## 📞 ENDPOINTS PRINCIPAIS

### Admin
```
POST   /api/v1/admin/login
POST   /api/v1/admin/logout
GET    /api/v1/admin/status
GET    /api/v1/admin/csv/info
POST   /api/v1/admin/csv/upload
GET    /api/v1/admin/empresas-aprovadas
POST   /api/v1/admin/releases/upload
GET    /api/v1/admin/releases/pendentes
```

### Alpha System
```
GET    /api/v1/alpha-v3/analise-completa
GET    /api/v1/alpha-v3/status
GET    /api/v1/alpha-v3/top-picks
POST   /api/v1/alpha-v3/refresh
```

---

## 🎯 PRÓXIMOS PASSOS (Sugestões)

1. **Notificações Push**
   - Alertar quando análise completa
   - Notificar quando CSV desatualizado

2. **Histórico de Análises**
   - Salvar análises anteriores
   - Comparar rankings ao longo do tempo

3. **Exportação de Dados**
   - Exportar ranking para Excel/PDF
   - Gerar relatórios automáticos

4. **Multi-usuário**
   - Múltiplos admins com permissões
   - Auditoria de ações

5. **API Pública**
   - Expor endpoints para terceiros
   - Rate limiting por usuário

---

## 📝 NOTAS FINAIS

### O Que NUNCA Fazer

❌ Usar dados mock em produção  
❌ Ignorar erros de NaN/Infinity  
❌ Buscar CSV automaticamente  
❌ Ultrapassar rate limits  
❌ Quebrar consistência de design  
❌ Remover SafeJSONResponse  
❌ Desabilitar validações  

### O Que SEMPRE Fazer

✅ Validar todos os inputs  
✅ Sanitizar dados antes de JSON  
✅ Usar SafeJSONResponse  
✅ Respeitar rate limits  
✅ Manter design consistente  
✅ Documentar mudanças  
✅ Testar edge cases  

---

## 🆘 SUPORTE

### Logs Importantes
```bash
# Backend
backend/logs/app.log

# Frontend
Console do navegador (F12)

# Groq API
Verificar rate limits em groq.com/console
```

### Comandos Úteis
```bash
# Resetar sistema
rm -rf data/stocks.csv data/empresas_aprovadas.json
rm -rf data/releases/*

# Limpar cache
rm -rf __pycache__ .pytest_cache node_modules/.cache

# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
npm install --force
```

---

**Documento criado em:** 20/02/2026  
**Autor:** Sistema Alpha Terminal  
**Versão:** 3.0 Final  
**Status:** Produção ✅
