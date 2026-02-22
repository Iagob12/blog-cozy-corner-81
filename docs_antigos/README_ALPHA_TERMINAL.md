# 🎯 Alpha Terminal - Sistema Completo de Análise de Investimentos

## O Que É

Sistema **100% automatizado** que replica seu processo de análise de investimentos usando IA (Gemini) e dados de mercado em tempo real.

**Meta: 5% ao mês através de valorização de preço**

---

## ✨ O Que Foi Implementado

### 🤖 Inteligência Artificial
- ✅ **6 Prompts** integrados com Gemini API
- ✅ Análise de mercado em tempo real
- ✅ Leitura e interpretação de PDFs de resultados
- ✅ Identificação de catalisadores de valorização
- ✅ Verificação anti-manada

### 📊 Dados de Mercado
- ✅ Preços em tempo real (API brapi.dev - B3)
- ✅ Coleta automática de dados (investimentos.com.br)
- ✅ Scraping de relatórios de RI
- ✅ Download e análise de PDFs
- ✅ Cálculo de momentum e indicadores técnicos

### 🎯 Fluxo Automatizado
1. **Prompt 1**: Radar de oportunidades (setores em ascensão)
2. **Coleta**: Dados de centenas de ações
3. **Prompt 2**: Filtra top 15 com fundamentos sólidos
4. **Busca**: Relatórios de resultados (PDFs)
5. **Prompt 3**: Análise profunda e comparativa
6. **Carteira**: Top 5 com justificativas
7. **Preços**: Atualização em tempo real
8. **Prompt 6**: Verificação anti-manada

---

## 🚀 Início Rápido (5 minutos)

```bash
# 1. Backend
cd backend
pip install -r requirements.txt

# 2. Configure Gemini API
cp .env.example .env
# Edite .env e adicione: GEMINI_API_KEY=sua_chave
# Obter chave: https://makersuite.google.com/app/apikey

# 3. Teste
python test_fluxo_completo.py

# 4. Inicie servidor
python -m uvicorn app.main:app --reload

# 5. Frontend (opcional)
cd ..
npm install
npm run dev
```

**Pronto!** Acesse: http://localhost:8000/docs

---

## 📱 Como Usar

### Opção 1: Interface Web

```bash
npm run dev
# Acesse: http://localhost:5173
# Clique em "Executar Fluxo Completo"
```

### Opção 2: API Direta

```bash
# Fluxo completo
curl -X POST http://localhost:8000/api/v1/portfolio/executar-fluxo-completo

# Análise rápida de um ticker
curl http://localhost:8000/api/v1/portfolio/analise-rapida/PRIO3

# Preços em tempo real
curl http://localhost:8000/api/v1/market/quote/PRIO3
```

### Opção 3: Script Python

```python
import asyncio
from app.services.portfolio_orchestrator import PortfolioOrchestrator

async def main():
    orchestrator = PortfolioOrchestrator()
    resultado = await orchestrator.executar_fluxo_completo()
    print(resultado['carteira_final'])

asyncio.run(main())
```

---

## 📊 Exemplo de Resultado

```json
{
  "carteira_final": [
    {
      "posicao": 1,
      "ticker": "PRIO3",
      "acao": "entrar_primeiro",
      "preco_atual": 48.50,
      "variacao_dia": 2.3,
      "justificativa": "Forte crescimento de produção com Campo de Wahoo. ROE de 35%, P/L de 8.5. Gestão eficiente com histórico de recompra de ações.",
      "anti_manada": {
        "veredito": "ENTRAR_AGORA",
        "exposicao_midia": "baixa",
        "fundamento_vs_narrativa": "fundamento_solido"
      }
    }
  ],
  "etapas": {
    "dados_coletados": 347,
    "top_15": 15,
    "relatorios_processados": 12,
    "carteira_final": 5
  }
}
```

---

## 🎯 Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                   ALPHA TERMINAL                         │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │ Frontend│      │  Backend  │     │    IA     │
   │ (React) │      │ (FastAPI) │     │ (Gemini)  │
   └─────────┘      └───────────┘     └───────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │ Market  │      │   Data    │     │ Surgical  │
   │  Data   │      │ Collector │     │   Layer   │
   └─────────┘      └───────────┘     └───────────┘
        │                  │                  │
   ┌────▼────┐      ┌─────▼─────┐     ┌─────▼─────┐
   │brapi.dev│      │investimen-│     │ PDFs de   │
   │  (B3)   │      │tos.com.br │     │    RI     │
   └─────────┘      └───────────┘     └───────────┘
```

---

## 📁 Estrutura do Projeto

```
blog-cozy-corner-81/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── alpha_intelligence.py    # 6 Prompts
│   │   │   ├── market_data.py           # Preços reais
│   │   │   ├── data_collector.py        # Coleta dados
│   │   │   └── portfolio_orchestrator.py # Orquestrador
│   │   ├── layers/
│   │   │   ├── quant_layer.py           # Filtros
│   │   │   ├── macro_layer.py           # Contexto macro
│   │   │   └── surgical_layer.py        # Análise PDFs
│   │   └── main.py                      # API
│   ├── test_fluxo_completo.py           # Teste
│   └── requirements.txt
├── src/
│   ├── components/alpha/
│   │   ├── PortfolioBuilder.tsx         # Construtor
│   │   ├── RadarOportunidades.tsx       # Radar
│   │   └── SwingTradeAnalysis.tsx       # Swing
│   └── pages/
│       └── AlphaDashboard.tsx           # Dashboard
├── GUIA_COMPLETO_ALPHA.md               # Guia de uso
├── DEPLOY_PRODUCAO.md                   # Deploy
└── README_ALPHA_TERMINAL.md             # Este arquivo
```

---

## 🔧 Tecnologias

### Backend
- **FastAPI** - API REST
- **Gemini API** - Análise de IA
- **brapi.dev** - Cotações B3
- **BeautifulSoup** - Web scraping
- **PyPDF2** - Leitura de PDFs
- **Pandas** - Análise de dados

### Frontend
- **React** - Interface
- **TypeScript** - Type safety
- **Tailwind CSS** - Estilização
- **shadcn/ui** - Componentes

---

## 📚 Documentação

- **[GUIA_COMPLETO_ALPHA.md](GUIA_COMPLETO_ALPHA.md)** - Guia detalhado de uso
- **[DEPLOY_PRODUCAO.md](DEPLOY_PRODUCAO.md)** - Como fazer deploy
- **[ALPHA_SYSTEM_GUIDE.md](ALPHA_SYSTEM_GUIDE.md)** - Filosofia e prompts
- **[IMPLEMENTACAO_ALPHA.md](IMPLEMENTACAO_ALPHA.md)** - Detalhes técnicos

---

## 🎓 Filosofia Alpha

### Perfil de Ativo Elite
- ROE > 15% (idealmente 30-50%)
- CAGR > 12%
- P/L < 15
- Dívida/EBITDA < 2,5

### Mentalidade
- **Antecipação**: Encontrar "Nvidias" antes da manada
- **Swing Trade**: 5-20 dias, capturando ciclos
- **Assimetria**: Risco/retorno mínimo de 2:1
- **Anti-Manada**: Evitar euforia do varejo

### Regras de Ouro
1. Nunca compre o que já virou manchete
2. Risco/retorno mínimo de 2:1
3. Corte posições sem apego
4. Entre no começo do ciclo, não no fim
5. Ignore dividend traps

---

## 💰 Custos

### APIs (Todas Gratuitas)
- ✅ **Gemini**: Grátis (60 req/min)
- ✅ **brapi.dev**: Grátis (B3)
- ✅ **Total**: R$ 0/mês

### Hospedagem (Opcional)
- **VPS**: $5-10/mês
- **Serverless**: $0-5/mês
- **Local**: R$ 0

---

## 🚀 Performance

- **Tempo de execução**: 3-5 minutos
- **Ações analisadas**: 200-500
- **PDFs processados**: 10-15
- **Carteira final**: Top 5
- **Atualização de preços**: Tempo real

---

## 🔒 Segurança

- ✅ API Keys em variáveis de ambiente
- ✅ Rate limiting
- ✅ HTTPS em produção
- ✅ Validação de dados
- ✅ Logs de auditoria

---

## 📈 Roadmap

- [ ] Cache de análises (Redis)
- [ ] Alertas por email/Telegram
- [ ] Integração com corretoras
- [ ] Backtest de recomendações
- [ ] Dashboard de performance
- [ ] App mobile

---

## 🐛 Troubleshooting

### "Erro ao baixar CSV"
✅ Sistema usa scraping como fallback automático

### "PDF não encontrado"
✅ Normal, nem todas empresas têm RI acessível

### "Gemini API error"
✅ Verifique se a chave está correta no `.env`

### "Timeout"
✅ Normal em primeira execução (até 5 minutos)

---

## 📞 Suporte

### Documentação
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Logs
```bash
# Backend
tail -f backend/logs/app.log

# Teste
python backend/test_fluxo_completo.py
```

---

## 📄 Licença

Este projeto é de uso pessoal. Não é recomendação de investimento.

---

## ⚠️ Disclaimer

Este sistema é uma ferramenta de apoio à decisão. Sempre:
- Faça sua própria análise
- Considere seu perfil de risco
- Diversifique seus investimentos
- Não invista mais do que pode perder

**Rentabilidade passada não garante rentabilidade futura.**

---

## 🎯 Meta

**5% ao mês através de valorização de preço**

*Valorização de preço, não dividendos. Comprar bem, esperar movimento, vender com lucro.*

---

**Sistema desenvolvido seguindo a filosofia Alpha Terminal** 🚀
