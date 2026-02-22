# Sistema de Gerenciamento de Releases

## 🎯 Objetivo

Permitir que você faça upload dos releases de resultados das empresas aprovadas na triagem, garantindo análises mais precisas com dados reais.

---

## 🔄 Fluxo Completo

### Fase 1: Triagem Automática
```
1. Sistema executa Prompt 1 (Radar de Oportunidades)
   → Identifica setores quentes

2. Sistema executa Prompt 2 (Triagem Fundamentalista)
   → Filtra 30 empresas com potencial
   → Retorna lista: PRIO3, VALE3, PETR4, ...

3. Sistema PAUSA e mostra no admin:
   "30 empresas aprovadas - Aguardando releases"
```

### Fase 2: Upload de Releases (VOCÊ)
```
1. Acessa painel admin
2. Vê lista de empresas pendentes:
   ✅ PRIO3 - Release Q4 2025 (já tem)
   ⏳ VALE3 - Aguardando release
   ⏳ PETR4 - Aguardando release
   ...

3. Faz upload dos releases (PDFs):
   - VALE3_Q4_2025.pdf
   - PETR4_Q4_2025.pdf
   - ...

4. Sistema valida e armazena em: data/releases/
```

### Fase 3: Análise Profunda
```
1. Quando todos os releases estiverem prontos
2. Clica em "Continuar Análise"
3. Sistema executa Prompt 3 com releases REAIS
4. Gera ranking final com análises precisas
```

---

## 📁 Estrutura de Armazenamento

### Diretório de Releases
```
data/
├── releases/
│   ├── PRIO3_Q4_2025.pdf
│   ├── PRIO3_Q3_2025.pdf
│   ├── VALE3_Q4_2025.pdf
│   ├── PETR4_Q4_2025.pdf
│   └── ...
└── releases_metadata.json
```

### Metadados (releases_metadata.json)
```json
{
  "PRIO3": [
    {
      "trimestre": "Q4",
      "ano": 2025,
      "filename": "PRIO3_Q4_2025.pdf",
      "path": "data/releases/PRIO3_Q4_2025.pdf",
      "data_upload": "2025-02-20T15:30:00",
      "usuario": "admin",
      "tamanho_kb": 2048.5
    },
    {
      "trimestre": "Q3",
      "ano": 2025,
      "filename": "PRIO3_Q3_2025.pdf",
      "path": "data/releases/PRIO3_Q3_2025.pdf",
      "data_upload": "2025-01-15T10:20:00",
      "usuario": "admin",
      "tamanho_kb": 1856.2
    }
  ],
  "VALE3": [
    {
      "trimestre": "Q4",
      "ano": 2025,
      "filename": "VALE3_Q4_2025.pdf",
      "path": "data/releases/VALE3_Q4_2025.pdf",
      "data_upload": "2025-02-20T15:35:00",
      "usuario": "admin",
      "tamanho_kb": 3120.8
    }
  ]
}
```

---

## 🖥️ Interface Admin

### Seção "Releases Pendentes"
```
┌─────────────────────────────────────────────────┐
│ 📄 Releases de Resultados                       │
├─────────────────────────────────────────────────┤
│                                                  │
│ Status: 15/30 empresas com releases (50%)       │
│                                                  │
│ ✅ PRIO3  - Q4 2025 (20/02/2025 15:30)          │
│ ✅ VALE3  - Q4 2025 (20/02/2025 15:35)          │
│ ✅ PETR4  - Q4 2025 (20/02/2025 15:40)          │
│                                                  │
│ ⏳ WEGE3  - Aguardando release                  │
│ ⏳ BBDC4  - Aguardando release                  │
│ ⏳ ITUB4  - Aguardando release                  │
│ ...                                              │
│                                                  │
│ [📤 Upload Release]  [🔄 Atualizar]             │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Modal de Upload
```
┌─────────────────────────────────────────────────┐
│ Upload de Release                                │
├─────────────────────────────────────────────────┤
│                                                  │
│ Ticker: [WEGE3     ▼]                           │
│                                                  │
│ Trimestre: [Q4 ▼]                               │
│                                                  │
│ Ano: [2025]                                      │
│                                                  │
│ Arquivo PDF:                                     │
│ ┌─────────────────────────────────────────┐     │
│ │  📄 Arraste o PDF aqui                  │     │
│ │     ou clique para selecionar           │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ [Cancelar]  [Upload Release]                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🔌 API Endpoints

### 1. Upload de Release
```http
POST /api/v1/admin/releases/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

Body:
- file: arquivo.pdf
- ticker: PRIO3
- trimestre: Q4
- ano: 2025

Response:
{
  "mensagem": "Release de PRIO3 Q4 2025 adicionado com sucesso",
  "detalhes": {
    "sucesso": true,
    "ticker": "PRIO3",
    "trimestre": "Q4",
    "ano": 2025,
    "filename": "PRIO3_Q4_2025.pdf",
    "path": "data/releases/PRIO3_Q4_2025.pdf"
  }
}
```

### 2. Verificar Releases Pendentes
```http
GET /api/v1/admin/releases/pendentes?tickers=PRIO3,VALE3,PETR4
Authorization: Bearer {token}

Response:
{
  "total": 3,
  "com_release": [
    {
      "ticker": "PRIO3",
      "trimestre": "Q4",
      "ano": 2025,
      "data_upload": "2025-02-20T15:30:00"
    }
  ],
  "sem_release": ["VALE3", "PETR4"],
  "percentual_completo": 33.33
}
```

### 3. Listar Releases de uma Empresa
```http
GET /api/v1/admin/releases/empresa/PRIO3
Authorization: Bearer {token}

Response:
{
  "ticker": "PRIO3",
  "total": 2,
  "releases": [
    {
      "trimestre": "Q4",
      "ano": 2025,
      "filename": "PRIO3_Q4_2025.pdf",
      "path": "data/releases/PRIO3_Q4_2025.pdf",
      "data_upload": "2025-02-20T15:30:00",
      "usuario": "admin",
      "tamanho_kb": 2048.5
    },
    {
      "trimestre": "Q3",
      "ano": 2025,
      "filename": "PRIO3_Q3_2025.pdf",
      "path": "data/releases/PRIO3_Q3_2025.pdf",
      "data_upload": "2025-01-15T10:20:00",
      "usuario": "admin",
      "tamanho_kb": 1856.2
    }
  ]
}
```

### 4. Estatísticas Gerais
```http
GET /api/v1/admin/releases/estatisticas
Authorization: Bearer {token}

Response:
{
  "total_empresas": 25,
  "total_releases": 32,
  "por_trimestre": {
    "Q1": 5,
    "Q2": 8,
    "Q3": 10,
    "Q4": 9
  },
  "por_ano": {
    "2024": 15,
    "2025": 17
  },
  "empresas": ["PRIO3", "VALE3", "PETR4", ...]
}
```

### 5. Remover Release
```http
DELETE /api/v1/admin/releases/PRIO3/Q3/2025
Authorization: Bearer {token}

Response:
{
  "mensagem": "Release de PRIO3 Q3 2025 removido com sucesso"
}
```

### 6. Listar Todas as Empresas com Releases
```http
GET /api/v1/admin/releases/listar
Authorization: Bearer {token}

Response:
{
  "total": 25,
  "empresas": [
    {
      "ticker": "PRIO3",
      "release_mais_recente": {
        "trimestre": "Q4",
        "ano": 2025,
        "data_upload": "2025-02-20T15:30:00"
      }
    },
    ...
  ]
}
```

---

## ✅ Vantagens do Sistema

### 1. Dados Reais e Precisos
- Você fornece os releases oficiais
- Sistema analisa dados reais (não estimativas)
- Análises muito mais confiáveis

### 2. Reutilização
- Releases ficam salvos
- Próximas análises usam releases existentes
- Não precisa fazer upload toda vez

### 3. Controle Total
- Você decide quais releases usar
- Pode atualizar quando quiser
- Histórico completo de uploads

### 4. Organização
- Releases organizados por ticker
- Metadados completos
- Fácil de gerenciar

### 5. Flexibilidade
- Aceita múltiplos trimestres
- Mantém histórico
- Pode remover releases antigos

---

## 🔄 Workflow Recomendado

### Análise Mensal
```
1. Início do mês:
   - Faz upload do CSV atualizado
   - Inicia análise (Prompt 1 + 2)

2. Sistema retorna 30 empresas aprovadas

3. Você coleta releases:
   - Busca releases Q4 2025 das 30 empresas
   - Faz upload no admin
   - Sistema valida e armazena

4. Continua análise:
   - Sistema usa releases reais
   - Gera ranking final preciso

5. Próximo mês:
   - Apenas atualiza releases novos
   - Reutiliza releases existentes
```

### Análise Rápida (Releases Já Salvos)
```
1. Faz upload do CSV atualizado
2. Inicia análise completa
3. Sistema usa releases já salvos
4. Análise completa em 3-5 minutos
```

---

## 📊 Exemplo Prático

### Cenário: Análise de Fevereiro 2025

**Passo 1**: Upload CSV
```
✅ CSV com 200 ações carregado
```

**Passo 2**: Triagem
```
🔍 Prompt 1: Setores identificados (Energia, Mineração, Consumo)
🔍 Prompt 2: 30 empresas aprovadas

Empresas aprovadas:
1. PRIO3 (Energia)
2. VALE3 (Mineração)
3. PETR4 (Energia)
...
30. WEGE3 (Industrial)
```

**Passo 3**: Verificar Releases
```
Status: 20/30 empresas com releases (66%)

✅ Já tem release (20):
   PRIO3, VALE3, PETR4, BBDC4, ITUB4, ...

⏳ Precisa de release (10):
   WEGE3, RENT3, EGIE3, CSAN3, ...
```

**Passo 4**: Upload Releases Faltantes
```
📤 Upload: WEGE3_Q4_2025.pdf ✅
📤 Upload: RENT3_Q4_2025.pdf ✅
📤 Upload: EGIE3_Q4_2025.pdf ✅
...

Status: 30/30 empresas com releases (100%) ✅
```

**Passo 5**: Continuar Análise
```
🚀 Análise Profunda com releases reais
⏱️ Tempo: 3-5 minutos
✅ Ranking final gerado
```

---

## 🛠️ Implementação Técnica

### Backend
- ✅ `ReleaseManager` - Gerencia releases
- ✅ Rotas API completas
- ✅ Validação de PDFs
- ✅ Metadados em JSON
- ✅ Backup automático

### Frontend (A Implementar)
- ⏳ Seção "Releases" no admin
- ⏳ Lista de empresas pendentes
- ⏳ Modal de upload
- ⏳ Indicador de progresso
- ⏳ Botão "Continuar Análise"

### Integração com Alpha System V3
- ⏳ Pausar após Prompt 2
- ⏳ Verificar releases disponíveis
- ⏳ Usar releases reais no Prompt 3
- ⏳ Fallback para Sistema Híbrido se não tiver release

---

## 📝 Próximos Passos

1. **Implementar UI no Admin** (próximo)
   - Seção de releases
   - Upload de PDFs
   - Lista de pendências

2. **Integrar com Alpha System V3**
   - Pausar após triagem
   - Verificar releases
   - Continuar com releases reais

3. **Melhorias Futuras**
   - OCR automático dos PDFs
   - Extração de dados estruturados
   - Validação de conteúdo
   - Notificações de releases faltantes

---

**Status**: ✅ Backend implementado
**Próximo**: Implementar UI no painel admin
**Benefício**: Análises muito mais precisas com dados reais
