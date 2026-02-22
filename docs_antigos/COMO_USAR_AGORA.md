# 🚀 COMO USAR O SISTEMA AGORA

## ✅ STATUS ATUAL

### Backend
- ✅ Rodando em http://localhost:8000
- ⚡ MODO MOCK ATIVADO (respostas instantâneas)
- ✅ 3 chaves Alpha Vantage configuradas
- ✅ Multi-IA configurada (AIML + Mistral)

### Frontend
- ✅ Rodando em http://localhost:8081
- ✅ Conectado ao backend
- ✅ Atualização automática a cada 5 minutos

---

## 🎯 ACESSO RÁPIDO

### Frontend (Interface)
```
http://localhost:8081
```

### Backend (API Docs)
```
http://localhost:8000/docs
```

---

## ⚡ MODO MOCK (ATIVO)

O sistema está em **MODO MOCK** para desenvolvimento rápido:

### Vantagens
- ✅ Respostas instantâneas (sem esperar APIs)
- ✅ Sem limite de requisições
- ✅ Sem custo de API
- ✅ Dados simulados realistas

### Como Funciona
- Usa dados simulados baseados em preços reais
- 15 ações disponíveis
- Variações de preço simuladas

### Desativar Modo Mock
Para usar APIs reais, edite `.env`:
```env
USE_MOCK_DATA=false
```

Depois reinicie o backend.

---

## 📊 ENDPOINTS DISPONÍVEIS

### 1. Top Picks (Rápido)
```http
GET http://localhost:8000/api/v1/top-picks?limit=15
```
- ⚡ Instantâneo (modo mock)
- Retorna 15 melhores ações
- Com preços e análise

### 2. Top Picks Multi-IA (Premium)
```http
GET http://localhost:8000/api/v1/aiml/top-picks-inteligente?limit=15
```
- Usa Gemini + Claude
- Análise profunda
- ⚠️ Requer verificação AIML

### 3. Market Overview
```http
GET http://localhost:8000/api/v1/market/overview
```
- Visão geral do mercado
- Ibovespa e Dólar

### 4. Alertas
```http
GET http://localhost:8000/api/v1/alerts
```
- Alertas inteligentes
- Oportunidades de compra

---

## 🔧 CONFIGURAÇÕES

### Modo Desenvolvimento (Atual)
```env
USE_MOCK_DATA=true  ← Ativo
```
- Respostas instantâneas
- Sem custo de API
- Ideal para testes

### Modo Produção
```env
USE_MOCK_DATA=false
```
- APIs reais (Alpha Vantage)
- Delay de 3 segundos entre requisições
- Cache de 30 minutos

---

## 🎨 INTERFACE

### Componentes Principais

1. **Alpha Header**
   - Logo e título
   - Status do sistema

2. **Market Pulse**
   - Ibovespa
   - Dólar
   - Atualização em tempo real

3. **Alpha Pick**
   - Melhor ação do momento
   - Dados detalhados
   - Botão "Ver Tese"

4. **Elite Table**
   - Tabela com 15 ações
   - Ordenação por rank
   - Filtros e busca

5. **Alerts Feed**
   - Alertas inteligentes
   - Top 3 ações
   - Oportunidades

---

## 🚀 FLUXO DE USO

### 1. Acesse o Frontend
```
http://localhost:8081
```

### 2. Visualize as Ações
- Tabela mostra 15 melhores ações
- Ordenadas por efficiency score
- Com preços atualizados

### 3. Veja Detalhes
- Clique em "Ver Tese" para análise completa
- Veja catalisadores e recomendações
- Confira preço teto e upside

### 4. Monitore Alertas
- Painel lateral com alertas
- Top 3 ações destacadas
- Oportunidades de compra

---

## 📈 DADOS EXIBIDOS

### Por Ação
- **Ticker**: Código da ação
- **Rank**: Posição no ranking
- **Efficiency Score**: Nota de eficiência
- **Preço Atual**: Cotação em tempo real
- **Preço Teto**: Alvo calculado
- **Upside**: Potencial de valorização
- **ROE**: Retorno sobre patrimônio
- **CAGR**: Crescimento anual
- **P/L**: Preço sobre lucro
- **Recomendação**: COMPRA/MONITORAR/EVITAR

---

## ⚙️ OTIMIZAÇÕES APLICADAS

### Cache Inteligente
- ✅ 30 minutos de cache
- ✅ Reduz chamadas à API
- ✅ Respostas mais rápidas

### Delay Reduzido
- ✅ 3 segundos (antes 4s)
- ✅ Análise mais rápida
- ✅ Melhor experiência

### Modo Mock
- ✅ Desenvolvimento rápido
- ✅ Testes sem limites
- ✅ Sem custos

---

## 🔄 ATUALIZAÇÃO AUTOMÁTICA

### Frontend
- Atualiza a cada 5 minutos
- Busca novos preços
- Recalcula rankings

### Backend
- Cache de 30 minutos
- Rotação de 3 chaves API
- Fallback automático

---

## 🐛 TROUBLESHOOTING

### Frontend não carrega
```bash
# Reinicie o frontend
cd blog-cozy-corner-81
npm run dev
```

### Backend com erro
```bash
# Reinicie o backend
cd blog-cozy-corner-81/backend
python -m uvicorn app.main:app --reload --port 8000
```

### Dados não atualizam
1. Verifique se backend está rodando
2. Limpe cache do navegador (Ctrl+Shift+R)
3. Verifique console do navegador (F12)

### Modo Mock não funciona
1. Verifique `.env`: `USE_MOCK_DATA=true`
2. Reinicie o backend
3. Veja logs do backend

---

## 📝 PRÓXIMOS PASSOS

### Para Produção
1. Desative modo mock: `USE_MOCK_DATA=false`
2. Verifique cartão na AIML API
3. Faça upload de relatórios trimestrais
4. Teste análise completa

### Para Melhorias
1. Adicione mais ações no CSV
2. Configure alertas personalizados
3. Implemente notificações
4. Crie dashboard de performance

---

## 💡 DICAS

### Performance
- Use modo mock para desenvolvimento
- Ative cache agressivo em produção
- Monitore limites de API

### Análise
- Compare múltiplas ações
- Veja histórico de recomendações
- Acompanhe alertas diariamente

### Custos
- Modo mock: $0
- Modo produção: ~$0.31 por análise
- Com relatórios: ~$6-9 por análise completa

---

## 🎉 SISTEMA PRONTO!

O Alpha Terminal está rodando e otimizado para uso imediato:

✅ Backend rodando (modo mock)
✅ Frontend rodando
✅ 15 ações disponíveis
✅ Respostas instantâneas
✅ Interface profissional

**Acesse agora**: http://localhost:8081

---

**Última atualização**: 19/02/2026
**Versão**: 2.1.0 (Otimizada)
