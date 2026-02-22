# 🔑 Alpha Vantage API - Setup

## 📊 Sobre Alpha Vantage

Alpha Vantage é uma das melhores APIs gratuitas para dados financeiros:

### Vantagens
✅ **Gratuita** - Sem custo
✅ **Dados reais** - Preços em tempo real
✅ **Global** - Suporta B3 (Brasil)
✅ **Confiável** - Dados de qualidade
✅ **Fácil** - API REST simples

### Limites (Free Tier)
- **25 requisições/dia**
- **5 requisições/minuto**
- Suficiente para desenvolvimento e uso pessoal

---

## 🚀 Como Obter sua Chave API (GRÁTIS)

### Passo 1: Acesse o Site
```
https://www.alphavantage.co/support/#api-key
```

### Passo 2: Preencha o Formulário
- **Email**: Seu email
- **Organization**: Seu nome ou "Personal"
- **Purpose**: "Personal use" ou "Development"

### Passo 3: Receba a Chave
- Você receberá a chave **instantaneamente** na tela
- Também será enviada por email
- Formato: `ABCD1234EFGH5678` (16 caracteres)

### Passo 4: Configure no Sistema
Edite o arquivo `.env`:

```env
ALPHAVANTAGE_API_KEY=SUA_CHAVE_AQUI
```

---

## 📝 Exemplo de Uso

### Buscar Preço de uma Ação
```
GET https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=PETR4.SAO&apikey=SUA_CHAVE
```

### Resposta
```json
{
  "Global Quote": {
    "01. symbol": "PETR4.SAO",
    "05. price": "37.19",
    "06. volume": "15000000",
    "10. change percent": "2.5%"
  }
}
```

---

## 🔧 Configuração no Sistema

### 1. Obtenha a Chave
Acesse: https://www.alphavantage.co/support/#api-key

### 2. Edite o .env
```bash
cd blog-cozy-corner-81/backend
# Edite o arquivo .env
ALPHAVANTAGE_API_KEY=SUA_CHAVE_AQUI
```

### 3. Reinicie o Backend
```bash
# O backend recarrega automaticamente
# Ou reinicie manualmente:
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Teste
```bash
curl http://localhost:8000/api/v1/top-picks?limit=5
```

---

## 📊 Dados Disponíveis

### 1. Cotação em Tempo Real
- Preço atual
- Variação do dia
- Volume negociado
- Máxima e mínima

### 2. Dados Intraday
- Preços a cada 1, 5, 15, 30 ou 60 minutos
- Últimos 100 pontos
- Para gráficos em tempo real

### 3. Histórico
- Preços diários
- Preços semanais
- Preços mensais

---

## ⚠️ Limites e Otimizações

### Limites Free Tier
```
25 requisições/dia
5 requisições/minuto
```

### Como o Sistema Otimiza

1. **Cache de 15 minutos**
   - Reduz chamadas à API
   - Melhora performance

2. **Busca apenas 5 ações por vez**
   - Respeita limite de 5/minuto
   - Demais usam CSV como fallback

3. **Delay entre requisições**
   - 0.5s entre cada chamada
   - Evita rate limit

### Exemplo de Log
```
[ALPHA VANTAGE] Buscando 15 ações...
⚠ Limite: 5 requisições/minuto (free tier)
✓ PRIO3: R$ 48.50 (Alpha Vantage)
✓ PETR4: R$ 37.19 (Alpha Vantage)
✓ VALE3: R$ 62.45 (Alpha Vantage)
✓ VULC3: R$ 12.30 (Alpha Vantage)
✓ ITUB4: R$ 28.90 (Alpha Vantage)
✓ 5/5 preços obtidos
⚠ 10 ações usarão preços do CSV (limite da API)
```

---

## 🚀 Upgrade para Premium (Opcional)

Se precisar de mais requisições:

### Alpha Vantage Premium
- **$49.99/mês**: 120 requisições/minuto
- **$149.99/mês**: 600 requisições/minuto
- **$499.99/mês**: 1200 requisições/minuto

### Quando Considerar
- Produção com muitos usuários
- Atualizações frequentes
- Mais de 25 ações monitoradas

---

## 🎯 Formato dos Tickers

### B3 (Brasil)
Alpha Vantage usa formato `.SAO`:

```
PETR4 → PETR4.SAO
VALE3 → VALE3.SAO
ITUB4 → ITUB4.SAO
```

O sistema converte automaticamente!

---

## ✅ Checklist de Setup

- [ ] Acessar https://www.alphavantage.co/support/#api-key
- [ ] Preencher formulário
- [ ] Copiar chave recebida
- [ ] Editar `backend/.env`
- [ ] Adicionar `ALPHAVANTAGE_API_KEY=SUA_CHAVE`
- [ ] Reiniciar backend
- [ ] Testar endpoint `/api/v1/top-picks`
- [ ] Verificar logs (deve mostrar "Alpha Vantage")

---

## 🆘 Troubleshooting

### Erro: "Invalid API key"
- Verifique se copiou a chave corretamente
- Sem espaços antes/depois
- 16 caracteres alfanuméricos

### Erro: "API call frequency"
- Atingiu limite de 5/minuto
- Aguarde 1 minuto
- Sistema usa cache automaticamente

### Erro: "Thank you for using Alpha Vantage"
- Limite de 25/dia atingido
- Aguarde até meia-noite (UTC)
- Sistema usa CSV como fallback

---

## 📚 Documentação Oficial

- **Site**: https://www.alphavantage.co
- **Docs**: https://www.alphavantage.co/documentation
- **Suporte**: https://www.alphavantage.co/support

---

## 🎉 Pronto!

Com Alpha Vantage configurado, você terá:
- ✅ Preços em tempo real
- ✅ Dados confiáveis
- ✅ API gratuita
- ✅ Fácil de usar

**Obtenha sua chave agora**: https://www.alphavantage.co/support/#api-key
