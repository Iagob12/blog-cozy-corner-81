# Guia de Uso: Sistema de Releases

## 🎯 Como Usar o Sistema de Releases

### 1. Acesse o Painel Admin
```
http://localhost:8081/admin
Senha: admin
```

### 2. Teste o Sistema (Mock)
Para testar sem fazer análise completa:

1. Na seção "Releases de Resultados"
2. Clique em **"Carregar 30 Empresas (Mock)"**
3. Sistema carrega 30 empresas fictícias
4. Você verá a lista de empresas pendentes

### 3. Faça Upload de um Release

**Opção A: Upload Individual**
1. Clique no botão "Upload" ao lado da empresa
2. Modal abre com ticker pré-selecionado
3. Selecione trimestre (Q1, Q2, Q3, Q4)
4. Selecione ano (2025)
5. Arraste ou selecione o PDF
6. Clique em "Upload"

**Opção B: Upload Geral**
1. Clique em "Upload Release" (topo da seção)
2. Selecione ticker manualmente
3. Selecione trimestre e ano
4. Arraste ou selecione o PDF
5. Clique em "Upload"

### 4. Acompanhe o Progresso
- Barra de progresso mostra % completo
- Lista verde: Empresas com release
- Lista amarela: Empresas pendentes

### 5. Continue a Análise
Quando 100% completo:
- Botão "Continuar Análise" aparece
- Clique para prosseguir com Prompt 3
- Sistema usa releases reais

---

## 📁 Formato dos Arquivos

### Nome do Arquivo (Recomendado)
```
TICKER_TRIMESTRE_ANO.pdf

Exemplos:
- PRIO3_Q4_2025.pdf
- VALE3_Q4_2025.pdf
- PETR4_Q3_2025.pdf
```

### Conteúdo do PDF
- Release oficial de resultados
- Relatório trimestral
- Apresentação de resultados
- Qualquer documento oficial da empresa

---

## 🔄 Fluxo Completo

### Primeira Vez (Sem Releases Salvos)
```
1. Iniciar Análise
   ↓
2. Prompt 1: Radar (setores quentes)
   ↓
3. Prompt 2: Triagem (30 empresas)
   ↓
4. Sistema mostra: 0/30 releases
   ↓
5. Você faz upload de 30 PDFs
   ↓
6. Sistema salva em data/releases/
   ↓
7. Clica "Continuar Análise"
   ↓
8. Prompt 3: Análise com releases reais
   ↓
9. Ranking final gerado
```

### Segunda Vez (Com Releases Salvos)
```
1. Iniciar Análise
   ↓
2. Prompt 1: Radar
   ↓
3. Prompt 2: Triagem (30 empresas)
   ↓
4. Sistema mostra: 25/30 releases (reutiliza!)
   ↓
5. Você faz upload de apenas 5 novos
   ↓
6. Clica "Continuar Análise"
   ↓
7. Análise completa (muito mais rápida)
```

---

## 💡 Dicas

### 1. Organize seus PDFs
Crie uma pasta local:
```
C:\Releases\
├── PRIO3_Q4_2025.pdf
├── VALE3_Q4_2025.pdf
├── PETR4_Q4_2025.pdf
└── ...
```

### 2. Nomeie Corretamente
Use o padrão: `TICKER_TRIMESTRE_ANO.pdf`
- Facilita identificação
- Evita confusão
- Organização melhor

### 3. Mantenha Atualizados
- Faça upload de releases novos mensalmente
- Sistema reutiliza releases existentes
- Não precisa fazer upload toda vez

### 4. Verifique Antes
- Confira se o PDF está correto
- Verifique trimestre e ano
- Confirme que é o release oficial

---

## 🧪 Teste Rápido

### Teste 1: Upload Básico
```
1. Acesse /admin
2. Clique "Carregar 30 Empresas (Mock)"
3. Veja lista de 30 empresas pendentes
4. Clique "Upload" em PRIO3
5. Selecione Q4, 2025
6. Faça upload de um PDF qualquer (teste)
7. Veja PRIO3 aparecer na lista verde
8. Progresso: 1/30 (3%)
```

### Teste 2: Upload Múltiplo
```
1. Faça upload de 5 releases diferentes
2. Veja progresso subir: 5/30 (17%)
3. Lista verde com 5 empresas
4. Lista amarela com 25 empresas
```

### Teste 3: Verificar Salvamento
```
1. Faça upload de um release
2. Feche o navegador
3. Abra novamente
4. Faça login no admin
5. Clique "Carregar 30 Empresas (Mock)"
6. Release ainda está lá! (persistido)
```

---

## 📊 Interface Visual

### Seção de Releases
```
┌─────────────────────────────────────────────────┐
│ 📄 Releases de Resultados    [Upload Release]   │
├─────────────────────────────────────────────────┤
│                                                  │
│ Progresso                          15/30        │
│ ████████████░░░░░░░░░░░░░░░░░░░░░░ 50%         │
│                                                  │
│ ✅ Com Release (15)                             │
│ ┌─────────────────────────────────────────┐     │
│ │ ✓ PRIO3  Q4 2025  20/02/2025           │     │
│ │ ✓ VALE3  Q4 2025  20/02/2025           │     │
│ │ ✓ PETR4  Q4 2025  20/02/2025           │     │
│ │ ...                                     │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ ⏳ Aguardando Release (15)                      │
│ ┌─────────────────────────────────────────┐     │
│ │ ⏰ WEGE3                    [Upload]    │     │
│ │ ⏰ RENT3                    [Upload]    │     │
│ │ ⏰ EGIE3                    [Upload]    │     │
│ │ ...                                     │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
└─────────────────────────────────────────────────┘
```

### Modal de Upload
```
┌─────────────────────────────────────────────────┐
│ Upload de Release                          [X]   │
├─────────────────────────────────────────────────┤
│                                                  │
│ Ticker                                           │
│ ┌─────────────────────────────────────────┐     │
│ │ WEGE3                                   │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ Trimestre                                        │
│ ┌─────────────────────────────────────────┐     │
│ │ Q4 ▼                                    │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ Ano                                              │
│ ┌─────────────────────────────────────────┐     │
│ │ 2025                                    │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ Arquivo PDF                                      │
│ ┌─────────────────────────────────────────┐     │
│ │  📄 Arraste o PDF aqui                  │     │
│ │     ou clique para selecionar           │     │
│ │                                          │     │
│ │  WEGE3_Q4_2025.pdf                      │     │
│ └─────────────────────────────────────────┘     │
│                                                  │
│ [Cancelar]                        [Upload]       │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## ⚠️ Troubleshooting

### Erro: "Apenas arquivos PDF são aceitos"
**Causa**: Arquivo não é PDF
**Solução**: Converta para PDF ou use arquivo correto

### Erro: "Ticker não encontrado"
**Causa**: Ticker não está na lista de empresas aprovadas
**Solução**: Verifique se carregou empresas mock ou fez triagem

### Erro: "Trimestre inválido"
**Causa**: Trimestre diferente de Q1, Q2, Q3, Q4
**Solução**: Use apenas Q1, Q2, Q3 ou Q4

### Release não aparece na lista
**Causa**: Upload falhou ou não foi salvo
**Solução**: 
1. Verifique mensagem de sucesso
2. Clique em "Atualizar" no header
3. Tente fazer upload novamente

### Progresso não atualiza
**Causa**: Cache do navegador
**Solução**: 
1. Clique em "Atualizar" no header
2. Ou recarregue a página (F5)

---

## 🔍 Verificação Manual

### Ver Releases Salvos
```bash
# Windows
dir blog-cozy-corner-81\backend\data\releases

# Deve mostrar:
# PRIO3_Q4_2025.pdf
# VALE3_Q4_2025.pdf
# ...
```

### Ver Metadados
```bash
# Windows
type blog-cozy-corner-81\backend\data\releases_metadata.json

# Deve mostrar JSON com informações dos releases
```

---

## 📈 Próximos Passos

Após dominar o sistema de releases:

1. **Integração com Análise Real**
   - Sistema pausará após Prompt 2
   - Mostrará empresas aprovadas automaticamente
   - Você faz upload dos releases
   - Sistema continua com Prompt 3

2. **Busca Automática** (futuro)
   - Sistema tentará buscar releases automaticamente
   - Se não encontrar, você faz upload manual
   - Melhor dos dois mundos

3. **OCR Automático** (futuro)
   - Sistema extrai dados dos PDFs automaticamente
   - Valida informações
   - Estrutura dados para análise

---

**Status**: ✅ Sistema completo e funcional
**Teste**: Carregue empresas mock e faça upload de PDFs
**Produção**: Aguardando integração com Alpha System V3
