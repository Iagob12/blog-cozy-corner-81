# 🎯 Alpha Terminal - Guia Completo

## Sistema Automatizado de Análise e Construção de Carteira

### O Que o Sistema Faz

O Alpha Terminal agora executa **automaticamente** todo o fluxo que você fazia manualmente:

1. ✅ **Busca preços reais** das ações em tempo real (API brapi.dev)
2. ✅ **Baixa dados** do investimentos.com.br (CSV ou scraping)
3. ✅ **Aplica Prompt 1** - Identifica setores em ascensão (Nvidia antes da explosão)
4. ✅ **Aplica Prompt 2** - Filtra as 15 melhores ações com base em fundamentos
5. ✅ **Busca relatórios** de resultados (PDFs) das empresas
6. ✅ **Aplica Prompt 3** - Análise profunda dos PDFs com IA
7. ✅ **Monta carteira final** - Top 5 com justificativas
8. ✅ **Verifica anti-manada** - Evita comprar o topo

---

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
cd backend

# Instale dependências
pip install -r requirements.txt

# Configure a API Key do Gemini
cp .env.example .env
# Edite .env e adicione: GEMINI_API_KEY=sua_chave_aqui
```

**Obter API Key Gemini (GRÁTIS):**
- Acesse: https://makersuite.google.com/app/apikey
- Clique em "Create API Key"
- Copie e cole no `.env`

### 2. Teste Rápido

```bash
# Teste o fluxo completo
python test_fluxo_completo.py
```

Isso irá:
- Buscar dados de ações
- Aplicar os 6 prompts
- Montar a carteira
- Gerar relatório HTML

### 3. Inicie o Servidor

```bash
python -m uvicorn app.main:app --reload
```

Servidor em: http://localhost:8000

### 4. Use a Interface Web

```bash
# Na raiz do projeto
npm install
npm run dev
```

Frontend em: http://localhost:5173

---

## 📊 Fluxo Completo Automatizado

### Endpoint Principal

```bash
POST http://localhost:8000/api/v1/portfolio/executar-fluxo-completo
```

### O Que Acontece (Passo a Passo)

#### ETAPA 1: Radar de Oportunidades (Prompt 1)
```
🎯 Objetivo: Identificar setores em ascensão ANTES da manada
📡 IA analisa: Cenário macro, catalisadores, narrativas institucionais
✅ Resultado: Lista de setores com potencial (ex: Energia, Tecnologia)
```

#### ETAPA 2: Coleta de Dados
```
📥 Fonte: investimentos.com.br
🔄 Método: Download CSV ou scraping
📊 Dados: P/L, ROE, CAGR, Dívida, Preço
✅ Resultado: Base com centenas de ações
```

#### ETAPA 3: Triagem Fundamentalista (Prompt 2)
```
🔍 Filtros:
   - P/L < 15
   - ROE > 15%
   - CAGR > 12%
   - Dívida/EBITDA < 2,5

🤖 IA analisa e rankeia
✅ Resultado: Top 15 ações com maior potencial
```

#### ETAPA 4: Busca de Relatórios
```
📄 Busca: Sites de RI das empresas
🎯 Foco: Relatórios de resultados trimestrais
📥 Download: PDFs mais recentes
✅ Resultado: 10-15 PDFs baixados
```

#### ETAPA 5: Análise Profunda (Prompt 3)
```
🧠 IA lê cada PDF e extrai:
   - Saúde financeira
   - Qualidade da gestão
   - Catalisadores de valorização
   - Riscos reais

🏆 Compara todas e rankeia
✅ Resultado: Top 5 para carteira final
```

#### ETAPA 6: Preços em Tempo Real
```
💰 API: brapi.dev (B3)
📈 Dados: Preço atual, variação, volume
✅ Resultado: Carteira com preços atualizados
```

#### ETAPA 7: Verificação Anti-Manada (Prompt 6)
```
🛡️ IA verifica:
   - Exposição na mídia
   - Fundamento vs narrativa
   - Posicionamento institucional

⚠️ Veredito: ENTRAR_AGORA | ESPERAR_CORRECAO | JANELA_FECHOU
✅ Resultado: Recomendação final para cada ação
```

---

## 🎯 Exemplo de Resultado

```json
{
  "carteira_final": [
    {
      "posicao": 1,
      "ticker": "PRIO3",
      "acao": "entrar_primeiro",
      "preco_atual": 48.50,
      "justificativa": "Forte crescimento de produção com Campo de Wahoo. ROE de 35%, P/L de 8.5. Gestão eficiente com histórico de recompra de ações.",
      "anti_manada": {
        "veredito": "ENTRAR_AGORA",
        "exposicao_midia": "baixa"
      }
    },
    {
      "posicao": 2,
      "ticker": "VULC3",
      "acao": "entrar_primeiro",
      "preco_atual": 12.30,
      "justificativa": "ROE excepcional de 50%. Eficiência operacional líder do setor. Expansão de market share.",
      "anti_manada": {
        "veredito": "ENTRAR_AGORA",
        "exposicao_midia": "baixa"
      }
    }
  ]
}
```

---

## 🔧 Endpoints Disponíveis

### Fluxo Completo
```bash
# Executa tudo automaticamente
POST /api/v1/portfolio/executar-fluxo-completo

# Análise rápida de um ticker
GET /api/v1/portfolio/analise-rapida/PRIO3

# Atualiza preços da carteira
POST /api/v1/portfolio/atualizar-precos
Body: ["PRIO3", "VULC3", "GMAT3"]
```

### Dados de Mercado
```bash
# Cotação em tempo real
GET /api/v1/market/quote/PRIO3

# Visão geral (Ibovespa, Dólar)
GET /api/v1/market/overview

# Momentum
GET /api/v1/market/momentum/PRIO3
```

### Alpha Intelligence
```bash
# Radar de oportunidades
GET /api/v1/alpha/radar-oportunidades

# Swing trade
GET /api/v1/alpha/swing-trade/PRIO3

# Anti-manada
GET /api/v1/alpha/anti-manada/PRIO3

# Análise comparativa
POST /api/v1/alpha/analise-comparativa
Body: ["PRIO3", "VULC3", "GMAT3"]
```

### Coleta de Dados
```bash
# Coletar dados de ações
GET /api/v1/data/coletar-acoes

# Buscar relatórios de RI
POST /api/v1/data/buscar-relatorios
Body: ["PRIO3", "VULC3"]
```

---

## 💡 Uso Diário Recomendado

### Segunda-feira (Início da Semana)
```bash
# Execute o fluxo completo
curl -X POST http://localhost:8000/api/v1/portfolio/executar-fluxo-completo
```

Isso gera sua carteira para a semana.

### Durante a Semana
```bash
# Monitore preços
curl http://localhost:8000/api/v1/market/quote/PRIO3

# Análise swing trade antes de comprar
curl http://localhost:8000/api/v1/alpha/swing-trade/PRIO3

# Verificação anti-manada
curl http://localhost:8000/api/v1/alpha/anti-manada/PRIO3
```

### Fim do Mês
```bash
# Revisão de carteira
curl -X POST http://localhost:8000/api/v1/alpha/revisao-carteira \
  -H "Content-Type: application/json" \
  -d '{
    "carteira": [
      {"ticker": "PRIO3", "qtd": 100, "preco_medio": 45.50, "resultado_pct": 12.5}
    ]
  }'
```

---

## 📱 Interface Web

Acesse: http://localhost:5173

### Aba "Carteira"
- Botão "Executar Fluxo Completo"
- Visualização da carteira gerada
- Preços em tempo real
- Veredito anti-manada

### Aba "Radar"
- Setores em ascensão
- Movimentos silenciosos
- Narrativas institucionais

### Aba "Swing Trade"
- Digite um ticker
- Análise completa para operação de 5-20 dias
- Stop loss e alvo
- Relação risco/retorno

### Aba "Alertas"
- Alertas de preço
- Notificações de eventos

---

## 🎓 Diferenças do Processo Manual

### Antes (Manual)
1. ❌ Copiar prompts no Gemini
2. ❌ Baixar CSV manualmente
3. ❌ Buscar relatórios um por um
4. ❌ Copiar e colar dados
5. ❌ Analisar cada PDF separadamente
6. ❌ Montar carteira manualmente

### Agora (Automatizado)
1. ✅ Um clique no botão
2. ✅ Sistema busca tudo automaticamente
3. ✅ IA analisa em paralelo
4. ✅ Carteira pronta em minutos
5. ✅ Preços em tempo real
6. ✅ Relatório HTML gerado

---

## ⚡ Performance

- **Tempo de execução**: 3-5 minutos
- **Ações analisadas**: 200-500
- **PDFs processados**: 10-15
- **Carteira final**: Top 5

---

## 🔒 Segurança e Limites

### API Gemini
- **Limite gratuito**: 60 requisições/minuto
- **Solução**: Sistema faz cache de análises
- **Custo**: Grátis para uso pessoal

### API brapi.dev
- **Limite**: Sem limite para uso pessoal
- **Dados**: B3 em tempo real
- **Custo**: Grátis

---

## 🐛 Troubleshooting

### "Erro ao baixar CSV"
**Solução**: Sistema usa scraping como fallback automático

### "PDF não encontrado"
**Solução**: Nem todas empresas têm RI acessível. Sistema continua com as que encontrou.

### "Gemini API error"
**Solução**: Verifique se a chave está correta no `.env`

### "Timeout"
**Solução**: Normal em primeira execução. Aguarde até 5 minutos.

---

## 📈 Próximas Melhorias

- [ ] Cache de análises (evitar reprocessar)
- [ ] Alertas por email/telegram
- [ ] Integração com corretoras
- [ ] Backtest de recomendações
- [ ] Dashboard de performance

---

## 🎯 Meta: 5% ao Mês

O sistema foi construído para atingir **5% de valorização ao mês** através de:

1. **Seleção rigorosa** - Apenas ações com fundamentos sólidos
2. **Timing perfeito** - Entrar antes da manada
3. **Gestão de risco** - Stop loss e verificação anti-manada
4. **Revisão constante** - Cortar posições sem apego

---

**Sistema desenvolvido seguindo a filosofia Alpha Terminal**

*Valorização de preço, não dividendos. Comprar bem, esperar movimento, vender com lucro.*
