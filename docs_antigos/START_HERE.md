# 🚀 COMECE AQUI - Alpha Terminal

## ⚡ Quick Start (5 minutos)

### 1. Backend

```bash
# Entrar na pasta backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar (escolha seu sistema)
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY (opcional por enquanto)

# Rodar servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ Backend rodando em: http://localhost:8000
📚 Documentação da API: http://localhost:8000/docs

---

### 2. Frontend

```bash
# Voltar para raiz (abrir novo terminal)
cd ..

# Instalar dependências
npm install

# Configurar variáveis
cp .env.example .env

# Rodar dev server
npm run dev
```

✅ Frontend rodando em: http://localhost:5173

---

## 🧪 Testar

### Testar Backend

Abra http://localhost:8000/docs e teste:

1. **GET /api/v1/top-picks** - Ver top picks
2. **GET /api/v1/macro-context** - Ver contexto macro
3. **GET /api/v1/alerts** - Ver alertas

Ou via curl:
```bash
curl http://localhost:8000/api/v1/top-picks?limit=5
```

### Testar Frontend

Abra http://localhost:5173 e veja a interface

---

## 📁 Arquivos Importantes

### Documentação
- **RESUMO_EXECUTIVO.md** ← Leia primeiro!
- **ALPHA_TERMINAL_README.md** - Visão completa
- **NEXT_STEPS.md** - O que fazer agora
- **DESIGN_BRIEF.md** - Conceito visual
- **IMPLEMENTATION_GUIDE.md** - Guia técnico

### Código Backend
- `backend/app/main.py` - API REST
- `backend/app/layers/quant_layer.py` - Filtro quantitativo
- `backend/app/layers/macro_layer.py` - Análise macro
- `backend/app/layers/surgical_layer.py` - IA + PDFs
- `backend/data/stocks.csv` - Dados de exemplo

### Código Frontend
- `src/pages/AlphaTerminal.tsx` - Página principal
- `src/services/alphaApi.ts` - Integração com API
- `src/components/alpha/` - Componentes

---

## 🎯 Próximos Passos

### Passo 1: Integrar Preços Reais (2-3 horas)

```bash
# Instalar yfinance
cd backend
pip install yfinance
```

Criar `backend/app/services/price_service.py`:
```python
import yfinance as yf

class PriceService:
    def get_current_price(self, ticker: str) -> float:
        try:
            stock = yf.Ticker(f"{ticker}.SA")
            data = stock.history(period="1d")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return 0.0
        except Exception as e:
            print(f"Erro: {e}")
            return 0.0
```

Testar:
```python
python
>>> from app.services.price_service import PriceService
>>> ps = PriceService()
>>> ps.get_current_price("WEGE3")
45.80
```

---

### Passo 2: Configurar Gemini API (30 minutos)

1. Obter chave: https://makersuite.google.com/app/apikey
2. Adicionar ao `.env`:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   ```
3. Reiniciar backend

---

### Passo 3: Atualizar Frontend (3-4 horas)

Modificar `src/pages/AlphaTerminal.tsx`:
```typescript
import { useQuery } from '@tanstack/react-query';
import { alphaApi } from '@/services/alphaApi';

const { data: topPicks, isLoading } = useQuery({
  queryKey: ['topPicks'],
  queryFn: () => alphaApi.getTopPicks(15),
  refetchInterval: 60000 // Atualiza a cada 1 min
});

if (isLoading) return <div>Carregando...</div>;

// Usar topPicks nos componentes
```

---

## 🐛 Troubleshooting

### Backend não inicia

```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Verificar dependências
pip list

# Verificar .env
cat .env  # Linux/Mac
type .env  # Windows
```

### Frontend não conecta

```bash
# Verificar se backend está rodando
curl http://localhost:8000

# Verificar CORS
# Abrir DevTools → Network → Ver erros

# Verificar .env
cat .env
```

### Erro ao importar módulos

```bash
# Reinstalar dependências
cd backend
pip install -r requirements.txt --force-reinstall
```

---

## 📊 Estrutura do Projeto

```
blog-cozy-corner-81/
├── backend/              ← API FastAPI
│   ├── app/
│   │   ├── layers/      ← 3 Camadas
│   │   ├── services/    ← Serviços
│   │   ├── models.py    ← Modelos
│   │   └── main.py      ← API
│   ├── data/
│   │   └── stocks.csv   ← Dados
│   └── scripts/         ← Automação
│
├── src/                 ← Frontend React
│   ├── services/
│   │   └── alphaApi.ts  ← Integração
│   ├── components/
│   └── pages/
│
└── Documentação/
    ├── RESUMO_EXECUTIVO.md
    ├── ALPHA_TERMINAL_README.md
    ├── NEXT_STEPS.md
    ├── DESIGN_BRIEF.md
    └── IMPLEMENTATION_GUIDE.md
```

---

## 🎨 Design

O site usa:
- **Tema**: Dark (preto profundo)
- **Accent**: Verde neon (#00ff88)
- **Layout**: Bento Grid
- **Componentes**: shadcn/ui
- **Animações**: Framer Motion

Ver **DESIGN_BRIEF.md** para detalhes completos.

---

## 🤖 Como Funciona

### Pipeline de 3 Camadas

1. **Quant** → Filtra por ROE, CAGR, P/L
2. **Macro** → Ajusta pesos por setor
3. **Surgical** → IA analisa PDFs

### Sistema Anti-Manada

Monitora volume de menções:
- Normal: < 2x média
- Atenção: 2-3x média
- Alerta: > 3x média

### Sistema de Alertas

Compara preço atual vs preço teto:
- 🟢 Abaixo do teto → COMPRAR
- 🟡 Próximo ao teto → AGUARDAR
- 🔴 Acima do teto → VENDER

---

## 📈 Meta: 5% ao Mês

**Estratégia**:
- 15 ações na carteira
- Upside médio: 15%
- Rotação: 4x ao ano
- Resultado: 60% ao ano

**Como**:
- Comprar no medo (preço baixo)
- Vender na euforia (preço alto)
- Evitar manada
- Rotação ativa

---

## 🎯 Checklist MVP

- [ ] Backend rodando
- [ ] Frontend rodando
- [ ] Preços reais (yfinance)
- [ ] Gemini API configurada
- [ ] Frontend consumindo API
- [ ] Pelo menos 1 ação exibida corretamente

**Tempo estimado**: 1 semana

---

## 📚 Leitura Recomendada

1. **RESUMO_EXECUTIVO.md** - Visão geral (10 min)
2. **NEXT_STEPS.md** - O que fazer (15 min)
3. **DESIGN_BRIEF.md** - Conceito visual (20 min)
4. **IMPLEMENTATION_GUIDE.md** - Guia técnico (30 min)

---

## 💡 Dicas

### Performance
- Use cache para preços
- Implemente rate limiting
- Otimize queries

### Segurança
- Valide inputs
- Use HTTPS em produção
- Proteja API keys

### UX
- Loading states
- Error boundaries
- Feedback visual
- Responsividade

---

## 🚀 Deploy (Quando Estiver Pronto)

### Backend
- Railway: https://railway.app/
- Render: https://render.com/
- Heroku: https://heroku.com/

### Frontend
- Vercel: https://vercel.com/
- Netlify: https://netlify.com/

---

## 📞 Ajuda

### Logs
```bash
# Backend
tail -f backend/logs/alpha_terminal.log

# Frontend
# Ver console do navegador (F12)
```

### Documentação da API
http://localhost:8000/docs

### Testar Endpoints
```bash
# Top picks
curl http://localhost:8000/api/v1/top-picks

# Macro context
curl http://localhost:8000/api/v1/macro-context

# Alerts
curl http://localhost:8000/api/v1/alerts
```

---

## 🎉 Pronto!

Agora você tem:
- ✅ Backend completo
- ✅ Frontend base
- ✅ Documentação completa
- ✅ Scripts de automação
- ✅ Guias de implementação

**Próximo passo**: Integrar preços reais (ver NEXT_STEPS.md)

---

🚀 **Boa sorte! Você está a 1 semana de ter seu próprio Terminal de Inteligência Tática funcionando!**
