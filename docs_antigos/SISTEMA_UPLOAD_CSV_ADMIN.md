# 📊 Sistema de Upload de CSV - Painel Admin

## 🎯 Objetivo

Sistema completo para você fazer upload do CSV atualizado diariamente, garantindo que as IAs sempre usem os dados mais recentes para gerar o ranking.

---

## ✅ O Que Foi Implementado

### 1. Backend - Gerenciamento de CSV

**Arquivo:** `backend/app/services/csv_manager.py`

**Features:**
- ✅ Upload de CSV com validação
- ✅ Backup automático do CSV anterior
- ✅ Validação de colunas obrigatórias
- ✅ Verificação de mínimo 50 ações
- ✅ Histórico de atualizações
- ✅ Limpeza automática de backups antigos (mantém últimos 10)

**Validações:**
- Colunas obrigatórias: `ticker`, `roe`, `cagr`, `pl`
- Mínimo: 50 ações
- Formato: CSV válido

### 2. Backend - Autenticação Admin

**Arquivo:** `backend/app/services/auth_service.py`

**Features:**
- ✅ Login com senha
- ✅ Token de sessão (válido por 24h)
- ✅ Logout
- ✅ Validação de token

**Segurança:**
- Senha com hash SHA256
- Token seguro (32 bytes)
- Expiração automática

### 3. Backend - Rotas Admin

**Arquivo:** `backend/app/routes/admin.py`

**Endpoints:**
```
POST   /api/v1/admin/login              - Login admin
POST   /api/v1/admin/logout             - Logout
GET    /api/v1/admin/csv/info           - Info do CSV atual
POST   /api/v1/admin/csv/upload         - Upload de novo CSV
POST   /api/v1/admin/csv/validar        - Valida CSV sem fazer upload
GET    /api/v1/admin/csv/historico      - Histórico de atualizações
GET    /api/v1/admin/status             - Status geral
```

### 4. Frontend - Painel Admin

**Arquivo:** `src/components/admin/AdminPanel.tsx`

**Features:**
- ✅ Tela de login
- ✅ Dashboard com info do CSV atual
- ✅ Upload de CSV (drag & drop)
- ✅ Histórico de atualizações
- ✅ Status visual (atualizado/desatualizado)
- ✅ Logout

---

## 🔐 Como Usar

### 1. Acessar Painel Admin

```
http://localhost:8081/admin
```

### 2. Fazer Login

**Senha padrão:** `admin`

(Você pode mudar a senha - veja seção "Configuração")

### 3. Ver Status do CSV Atual

O painel mostra:
- Total de ações
- Última atualização
- Idade do CSV (em horas)
- Status: Atualizado (< 24h) ou Desatualizado (> 24h)

### 4. Fazer Upload de Novo CSV

1. Clique na área de upload
2. Selecione o arquivo CSV
3. Sistema valida automaticamente
4. Se válido, substitui o CSV atual
5. Backup do CSV anterior é criado automaticamente

### 5. Ver Histórico

Veja as últimas atualizações:
- Data e hora
- Usuário
- Quantidade de ações
- Backup criado

---

## 📋 Formato do CSV

### Colunas Obrigatórias:

```csv
ticker,roe,cagr,pl,setor,nome
PRIO3,25.5,18.2,8.5,Energia,PRIO
VALE3,22.1,15.8,6.2,Mineração,VALE
...
```

**Mínimo:** 50 ações

**Colunas aceitas (case-insensitive):**
- `ticker` ou `Ticker`
- `roe` ou `ROE`
- `cagr` ou `CAGR`
- `pl` ou `PL`
- `setor` ou `Setor` (opcional)
- `nome` ou `Nome` (opcional)

---

## 🔄 Como o Sistema Usa o CSV

### 1. Alpha System V3

O sistema lê o CSV em:
```python
# backend/app/services/alpha_system_v3.py
csv_path, csv_timestamp = await self.scraper.baixar_csv_diario()
```

**Fluxo:**
1. Tenta baixar CSV de investimentos.com.br
2. Se falhar, usa CSV local (`data/stocks.csv`)
3. Valida freshness (< 48h)
4. Envia TODAS as ações para IA (Prompt 2)
5. IA seleciona top 30
6. Sistema Híbrido coleta dados (yfinance + IA)
7. Análise profunda das 30 empresas
8. Gera ranking final

### 2. Dados Usados pelas IAs

**Prompt 1 (Radar):**
- Não usa CSV (análise macro)

**Prompt 2 (Triagem):**
- ✅ **USA CSV COMPLETO**
- Recebe TODAS as ações do CSV
- Filtra por ROE, CAGR, P/L
- Considera setores quentes
- Retorna top 30

**Prompt 3 (Análise Profunda):**
- Usa dados do Sistema Híbrido (yfinance + IA)
- Não usa CSV diretamente
- Mas as 30 empresas vieram do CSV (Prompt 2)

**Prompt 6 (Anti-Manada):**
- Não usa CSV (análise de timing)

### 3. Confirmação de Uso

Para confirmar que o CSV está sendo usado:

1. **Logs do Backend:**
```
[CSV] CSV carregado: 183 ações
[PROMPT_2] Enviando 183 ações para análise
```

2. **Endpoint de Info:**
```bash
curl http://localhost:8000/api/v1/admin/csv/info \
  -H "Authorization: Bearer SEU_TOKEN"
```

3. **Painel Admin:**
- Mostra total de ações
- Mostra última atualização
- Mostra se está sendo usado

---

## ⚙️ Configuração

### 1. Mudar Senha Admin

**Opção 1: Via .env**

```bash
# backend/.env
ADMIN_PASSWORD_HASH=seu_hash_aqui
```

**Opção 2: Gerar novo hash**

```python
# backend/test_generate_password.py
from app.services.auth_service import get_auth_service

auth = get_auth_service()
nova_senha = "sua_senha_aqui"
hash_gerado = auth.gerar_hash_senha(nova_senha)

print(f"Hash da senha '{nova_senha}':")
print(hash_gerado)
```

Execute:
```bash
cd backend
python test_generate_password.py
```

Copie o hash e adicione no `.env`:
```
ADMIN_PASSWORD_HASH=hash_gerado_aqui
```

### 2. Mudar Duração do Token

```python
# backend/app/services/auth_service.py
self.token_duration = timedelta(hours=24)  # Mude aqui
```

### 3. Mudar Quantidade de Backups

```python
# backend/app/services/csv_manager.py
self._limpar_backups_antigos(manter=10)  # Mude aqui
```

---

## 📁 Estrutura de Arquivos

```
backend/
├── app/
│   ├── services/
│   │   ├── csv_manager.py          # Gerenciador de CSV
│   │   └── auth_service.py         # Autenticação
│   └── routes/
│       └── admin.py                # Rotas admin
├── data/
│   ├── stocks.csv                  # CSV atual (usado pelas IAs)
│   ├── backups/                    # Backups automáticos
│   │   ├── stocks_20260220_143022.csv
│   │   └── stocks_20260220_150145.csv
│   └── csv_updates.log             # Log de atualizações

frontend/
└── src/
    └── components/
        └── admin/
            └── AdminPanel.tsx      # Painel admin
```

---

## 🧪 Como Testar

### 1. Testar Upload

```bash
# Criar CSV de teste
echo "ticker,roe,cagr,pl,setor,nome" > test.csv
echo "TEST1,20,15,10,Teste,Empresa Teste 1" >> test.csv
# ... adicione mais 49 linhas (mínimo 50)

# Fazer login
curl -X POST http://localhost:8000/api/v1/admin/login \
  -H "Content-Type: application/json" \
  -d '{"password":"admin"}'

# Copie o token retornado

# Fazer upload
curl -X POST http://localhost:8000/api/v1/admin/csv/upload \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "file=@test.csv"
```

### 2. Testar Validação

```bash
# CSV inválido (sem colunas obrigatórias)
echo "coluna1,coluna2" > invalid.csv
echo "valor1,valor2" >> invalid.csv

curl -X POST http://localhost:8000/api/v1/admin/csv/validar \
  -H "Authorization: Bearer SEU_TOKEN" \
  -F "file=@invalid.csv"

# Deve retornar erro de validação
```

### 3. Verificar Info

```bash
curl http://localhost:8000/api/v1/admin/csv/info \
  -H "Authorization: Bearer SEU_TOKEN"
```

---

## ✅ Checklist de Validação

Para confirmar que o sistema está funcionando:

- [ ] Consegue acessar `/admin`
- [ ] Consegue fazer login
- [ ] Vê informações do CSV atual
- [ ] Consegue fazer upload de CSV válido
- [ ] CSV é validado corretamente
- [ ] Backup é criado automaticamente
- [ ] Histórico é atualizado
- [ ] Logs do backend mostram CSV sendo usado
- [ ] Análise usa o novo CSV
- [ ] Consegue fazer logout

---

## 🎯 Fluxo Completo

```
1. Você baixa CSV atualizado de investimentos.com.br
   ↓
2. Acessa http://localhost:8081/admin
   ↓
3. Faz login com senha admin
   ↓
4. Vê status do CSV atual (idade, total de ações)
   ↓
5. Faz upload do novo CSV
   ↓
6. Sistema valida:
   - Colunas obrigatórias ✓
   - Mínimo 50 ações ✓
   - Formato CSV válido ✓
   ↓
7. Sistema cria backup do CSV anterior
   ↓
8. Sistema substitui CSV
   ↓
9. Sistema registra no log
   ↓
10. Próxima análise usa o novo CSV
    ↓
11. IAs recebem dados atualizados
    ↓
12. Ranking gerado com dados frescos ✓
```

---

## 🚀 Resultado

Agora você tem controle total sobre os dados:

1. ✅ Faz upload do CSV atualizado quando quiser
2. ✅ Sistema valida automaticamente
3. ✅ Backup automático (segurança)
4. ✅ IAs sempre usam dados mais recentes
5. ✅ Histórico completo de atualizações
6. ✅ Interface visual simples e clara

**O CSV que você faz upload é EXATAMENTE o que as IAs usam para gerar o ranking!**

---

## 📞 Próximos Passos

1. Acesse `/admin` e faça login
2. Veja o status do CSV atual
3. Faça upload de um CSV de teste
4. Verifique os logs do backend
5. Execute uma análise e confirme que usa o novo CSV

**Pronto para usar!** 🎉
