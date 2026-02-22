# Como Rodar o Alpha Terminal

## 🚀 Início Rápido

### 1. Configurar Backend (Python)

```bash
# Entre na pasta do backend
cd backend

# Crie ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
copy .env.example .env

# Edite o arquivo .env e adicione sua chave do Gemini:
# GEMINI_API_KEY=sua_chave_aqui
```

### 2. Obter API Key do Gemini (GRÁTIS)

1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave
4. Cole no arquivo `.env`:
   ```
   GEMINI_API_KEY=AIzaSy...sua_chave_aqui
   ```

### 3. Testar o Sistema

```bash
# Ainda na pasta backend
python test_alpha.py
```

Você deve ver:
- ✅ Cotações em tempo real
- ✅ Análise de mercado (se configurou Gemini)
- ✅ Recomendações de swing trade

### 4. Iniciar o Servidor

```bash
# Ainda na pasta backend
python -m uvicorn app.main:app --reload
```

O servidor estará rodando em: http://localhost:8000

### 5. Testar os Endpoints

Abra outro terminal e teste:

```bash
# Visão geral do mercado
curl http://localhost:8000/api/v1/market/overview

# Cotação de uma ação
curl http://localhost:8000/api/v1/market/quote/PRIO3

# Radar de oportunidades (precisa de Gemini API)
curl http://localhost:8000/api/v1/alpha/radar-oportunidades

# Análise swing trade (precisa de Gemini API)
curl http://localhost:8000/api/v1/alpha/swing-trade/PRIO3
```

### 6. Frontend (Opcional)

```bash
# Volte para a raiz do projeto
cd ..

# Instale dependências
npm install

# Configure a URL da API
# Crie arquivo .env na raiz:
echo "VITE_API_URL=http://localhost:8000" > .env

# Inicie o frontend
npm run dev
```

Frontend estará em: http://localhost:5173

## 📊 Testando com Dados Reais

### Adicionar Ações ao CSV

Edite `backend/data/stocks.csv`:

```csv
Ticker,P/L,ROE,CAGR,Dívida,Setor,Preço
PRIO3,8.5,35.2,18.5,1.2,Energia,48.50
VULC3,6.2,50.1,15.3,0.8,Consumo,12.30
GMAT3,7.8,28.5,22.1,1.5,Varejo,8.90
CURY3,5.5,32.8,19.7,1.1,Construção,15.20
POMO3,9.2,25.3,14.8,1.8,Industrial,3.45
```

### Testar Top Picks

```bash
curl http://localhost:8000/api/v1/top-picks
```

Você receberá:
- Ranking das melhores ações
- Preços reais (via API)
- Catalisadores identificados por IA
- Recomendação final (COMPRA FORTE, COMPRA, etc)

## 🎯 Fluxo de Uso Diário

### Manhã (Antes da Abertura)

1. **Visão Geral do Mercado**
   ```bash
   curl http://localhost:8000/api/v1/market/overview
   ```

2. **Radar de Oportunidades** (semanal)
   ```bash
   curl http://localhost:8000/api/v1/alpha/radar-oportunidades
   ```

### Durante o Dia

3. **Monitorar Cotações**
   ```bash
   curl http://localhost:8000/api/v1/market/quote/PRIO3
   curl http://localhost:8000/api/v1/market/quote/VULC3
   ```

4. **Análise Swing Trade** (antes de comprar)
   ```bash
   curl http://localhost:8000/api/v1/alpha/swing-trade/PRIO3
   ```

5. **Verificação Anti-Manada** (antes de comprar)
   ```bash
   curl http://localhost:8000/api/v1/alpha/anti-manada/PRIO3
   ```

### Mensal

6. **Revisão de Carteira**
   ```bash
   curl -X POST http://localhost:8000/api/v1/alpha/revisao-carteira \
     -H "Content-Type: application/json" \
     -d '{
       "carteira": [
         {"ticker": "PRIO3", "qtd": 100, "preco_medio": 45.50, "resultado_pct": 12.5},
         {"ticker": "VULC3", "qtd": 200, "preco_medio": 11.80, "resultado_pct": 4.2}
       ]
     }'
   ```

## 🔧 Troubleshooting

### Erro: "GEMINI_API_KEY não configurada"

**Solução:**
1. Obtenha a chave em: https://makersuite.google.com/app/apikey
2. Adicione no arquivo `backend/.env`
3. Reinicie o servidor

### Erro: "Não foi possível buscar cotação"

**Causa:** API brapi.dev pode estar fora do ar ou ticker inválido

**Solução:**
- Verifique se o ticker está correto (ex: PRIO3, não PRIO)
- Tente novamente em alguns minutos
- Verifique sua conexão com internet

### Erro: "Arquivo CSV não encontrado"

**Solução:**
```bash
# Certifique-se de estar na pasta backend
cd backend

# Verifique se o arquivo existe
ls data/stocks.csv

# Se não existir, crie:
mkdir -p data
# Copie o exemplo ou crie seu próprio
```

### Servidor não inicia

**Solução:**
```bash
# Verifique se a porta 8000 está livre
# Windows:
netstat -ano | findstr :8000

# Linux/Mac:
lsof -i :8000

# Se estiver ocupada, mate o processo ou use outra porta:
python -m uvicorn app.main:app --reload --port 8001
```

## 📚 Documentação da API

Acesse: http://localhost:8000/docs

Você verá a documentação interativa (Swagger) com todos os endpoints disponíveis.

## 💡 Dicas

1. **Use o teste primeiro**: `python test_alpha.py` mostra se tudo está funcionando

2. **Cache de análises**: A Gemini API tem rate limits. Considere cachear resultados por algumas horas

3. **Dados históricos**: Use `/api/v1/market/momentum/{ticker}` para ver tendências

4. **Análise comparativa**: Envie múltiplos tickers de uma vez para economizar chamadas de API

5. **Logs**: Adicione `--log-level debug` ao uvicorn para ver mais detalhes

## 🎓 Próximos Passos

1. Explore a documentação em `/docs`
2. Teste cada endpoint manualmente
3. Adicione suas ações favoritas no CSV
4. Configure alertas (em desenvolvimento)
5. Integre com seu workflow de investimentos

---

**Dúvidas?** Verifique os arquivos:
- `ALPHA_SYSTEM_GUIDE.md` - Guia completo do sistema
- `IMPLEMENTACAO_ALPHA.md` - Detalhes técnicos
- `backend/test_alpha.py` - Exemplos de uso
