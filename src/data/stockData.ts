export interface Stock {
  ticker: string;
  name: string;
  sector: string;
  price: number;
  change: number;
  roe: number;
  pl: number;
  cagr5y: number;
  upside: number;
  sparkline: number[];
  confidence: "alta" | "média" | "baixa";
  maxBuyPrice: number;
  targetPrice: number;
  catalyst: string;
  thesis: string;
}

export interface MacroIndicator {
  label: string;
  value: string;
  change: number;
  unit?: string;
}

export interface Alert {
  id: string;
  type: "euforia" | "oportunidade" | "cautela";
  ticker: string;
  title: string;
  description: string;
  timestamp: string;
}

export const macroIndicators: MacroIndicator[] = [
  { label: "SELIC", value: "13.25", change: -0.5, unit: "%" },
  { label: "IPCA", value: "4.87", change: 0.12, unit: "%" },
  { label: "USD/BRL", value: "5.72", change: -1.3, unit: "" },
  { label: "IBOV", value: "132.450", change: 1.8, unit: "pts" },
  { label: "DI Jan/26", value: "14.85", change: -0.15, unit: "%" },
  { label: "S&P 500", value: "6.012", change: 0.45, unit: "pts" },
];

export const alphaPickStock: Stock = {
  ticker: "PRIO3",
  name: "PRIO S.A.",
  sector: "Petróleo & Gás",
  price: 42.15,
  change: 3.2,
  roe: 38.5,
  pl: 6.8,
  cagr5y: 45.2,
  upside: 32,
  sparkline: [30, 32, 31, 35, 34, 38, 36, 40, 39, 42],
  confidence: "alta",
  maxBuyPrice: 44.00,
  targetPrice: 55.60,
  catalyst: "Aquisição do Campo de Peregrino finalizada em Q1/2026. Produção estimada saltará de 90k para 130k barris/dia, diluindo custo de lifting para $6/barril — menor do setor.",
  thesis: `## Tese PRIO3 — Assimetria Extrema

PRIO é a junior oil mais eficiente da América Latina. Com ROE de 38.5% e P/L de 6.8x, negocia com desconto de 40% vs. peers internacionais.

### Catalisador Principal
A conclusão da aquisição de Peregrino (Equinor) no Q1/2026 adicionará ~40k bbl/dia à produção. O mercado ainda precifica a empresa sem esse volume.

### Margem de Segurança
Mesmo com petróleo a $60/bbl (cenário pessimista), o breakeven da PRIO é $12/bbl — margem operacional de 80%.

### Riscos Monitorados
- Volatilidade do Brent abaixo de $55
- Atraso regulatório na transferência de operação
- Exposição cambial (receita em USD, custos em BRL — hedge natural)

**Veredicto: COMPRA FORTE até R$44.00**`,
};

export const eliteStocks: Stock[] = [
  alphaPickStock,
  {
    ticker: "WEGE3", name: "WEG S.A.", sector: "Industriais", price: 52.30, change: 1.5,
    roe: 32.1, pl: 35.2, cagr5y: 28.4, upside: 18, confidence: "alta",
    sparkline: [40, 42, 44, 43, 46, 48, 47, 50, 51, 52],
    maxBuyPrice: 54.00, targetPrice: 61.70,
    catalyst: "Expansão de fábricas na China e México para atender demanda de data centers e veículos elétricos.",
    thesis: "WEG continua sendo a melhor compounding machine da B3. ROE consistente acima de 30% há 5 anos."
  },
  {
    ticker: "VIVT3", name: "Telefônica Brasil", sector: "Telecom", price: 53.80, change: 0.8,
    roe: 22.4, pl: 14.5, cagr5y: 12.3, upside: 15, confidence: "alta",
    sparkline: [45, 46, 47, 48, 49, 50, 51, 52, 53, 54],
    maxBuyPrice: 56.00, targetPrice: 61.87,
    catalyst: "Dividend yield de 7.8% com payout crescente. Migração para fibra ótica elevando ARPU.",
    thesis: "Vivo é a blue chip defensiva com melhor relação risco/retorno do setor de telecom."
  },
  {
    ticker: "ITUB4", name: "Itaú Unibanco", sector: "Financeiro", price: 34.20, change: 2.1,
    roe: 21.8, pl: 8.2, cagr5y: 15.6, upside: 22, confidence: "alta",
    sparkline: [28, 29, 30, 29, 31, 32, 31, 33, 34, 34],
    maxBuyPrice: 36.00, targetPrice: 41.72,
    catalyst: "Expansão do crédito consignado e inadimplência em queda. ROE projetado de 23% para 2026.",
    thesis: "Melhor banco do Brasil. Eficiência operacional incomparável no setor."
  },
  {
    ticker: "MRCP3", name: "Marcopolo", sector: "Industriais", price: 8.45, change: 5.8,
    roe: 28.7, pl: 9.1, cagr5y: 52.1, upside: 35, confidence: "alta",
    sparkline: [4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5],
    maxBuyPrice: 9.00, targetPrice: 11.41,
    catalyst: "Programa Caminho da Escola + exportações recordes. Backlog de pedidos de 18 meses.",
    thesis: "Marcopolo é a turnaround story do ano. De quase-falência para ROE de 28%."
  },
  {
    ticker: "BBAS3", name: "Banco do Brasil", sector: "Financeiro", price: 28.90, change: 1.2,
    roe: 19.5, pl: 5.1, cagr5y: 18.2, upside: 28, confidence: "média",
    sparkline: [22, 23, 24, 25, 24, 26, 27, 27, 28, 29],
    maxBuyPrice: 30.50, targetPrice: 37.00,
    catalyst: "Dividend yield de 9.5%. Agronegócio sustentando carteira de crédito.",
    thesis: "BB negocia a 5x lucros com DY de quase 10%. Desconto injustificado vs. Itaú."
  },
  {
    ticker: "SUZB3", name: "Suzano", sector: "Papel & Celulose", price: 58.70, change: -0.5,
    roe: 15.2, pl: 7.8, cagr5y: 22.1, upside: 20, confidence: "média",
    sparkline: [50, 52, 54, 56, 55, 57, 58, 57, 59, 59],
    maxBuyPrice: 60.00, targetPrice: 70.44,
    catalyst: "Preço da celulose em alta global. Projeto Cerrado adicionando 2.5M ton/ano de capacidade.",
    thesis: "Suzano é a maior produtora de celulose do mundo com custo de produção imbatível."
  },
  {
    ticker: "RENT3", name: "Localiza", sector: "Consumo", price: 48.20, change: 2.4,
    roe: 18.9, pl: 15.3, cagr5y: 19.8, upside: 24, confidence: "média",
    sparkline: [38, 39, 40, 42, 43, 44, 45, 46, 47, 48],
    maxBuyPrice: 50.00, targetPrice: 59.77,
    catalyst: "Sinergias da fusão com Unidas. Frota otimizada para depreciar menos e lucrar mais.",
    thesis: "Localiza domina 40% do mercado de locação. Poder de precificação incomparável."
  },
  {
    ticker: "CPLE6", name: "Copel", sector: "Energia", price: 10.80, change: 1.9,
    roe: 14.5, pl: 8.9, cagr5y: 16.7, upside: 19, confidence: "média",
    sparkline: [8, 8.5, 9, 9.2, 9.5, 9.8, 10, 10.2, 10.5, 10.8],
    maxBuyPrice: 11.50, targetPrice: 12.85,
    catalyst: "Privatização gerando ganhos de eficiência. Redução de 30% nos custos operacionais.",
    thesis: "Copel pós-privatização é outra empresa. Margens em expansão acelerada."
  },
  {
    ticker: "TOTS3", name: "TOTVS", sector: "Tecnologia", price: 31.50, change: 0.6,
    roe: 16.8, pl: 28.4, cagr5y: 20.5, upside: 16, confidence: "média",
    sparkline: [25, 26, 27, 28, 28, 29, 30, 30, 31, 31],
    maxBuyPrice: 33.00, targetPrice: 36.54,
    catalyst: "Cross-sell de Techfin e Business Performance. NRR acima de 110%.",
    thesis: "TOTVS é o SAP brasileiro. Receita recorrente de 80%+ garante previsibilidade."
  },
  {
    ticker: "ELET3", name: "Eletrobras", sector: "Energia", price: 42.10, change: -0.3,
    roe: 8.2, pl: 12.1, cagr5y: 14.3, upside: 30, confidence: "média",
    sparkline: [35, 36, 37, 38, 39, 40, 41, 40, 41, 42],
    maxBuyPrice: 45.00, targetPrice: 54.73,
    catalyst: "Reestruturação pós-privatização. Desligamento de 3.500 funcionários reduzindo OPEX em 25%.",
    thesis: "Eletrobras é a maior geradora da América Latina. Potencial de ROE de 15%+ em 3 anos."
  },
  {
    ticker: "SBSP3", name: "Sabesp", sector: "Saneamento", price: 88.50, change: 1.1,
    roe: 12.5, pl: 11.8, cagr5y: 18.9, upside: 25, confidence: "alta",
    sparkline: [70, 72, 75, 78, 80, 82, 84, 86, 87, 88],
    maxBuyPrice: 92.00, targetPrice: 110.63,
    catalyst: "Privatização concluída. Meta de universalização até 2029 gera pipeline de R$70bi em investimentos.",
    thesis: "Sabesp privatizada é um case de infraestrutura com crescimento garantido por marco regulatório."
  },
  {
    ticker: "VALE3", name: "Vale S.A.", sector: "Mineração", price: 62.30, change: -1.8,
    roe: 24.1, pl: 5.5, cagr5y: 8.2, upside: 18, confidence: "baixa",
    sparkline: [68, 67, 65, 64, 63, 62, 63, 62, 61, 62],
    maxBuyPrice: 64.00, targetPrice: 73.51,
    catalyst: "Estímulos chineses e acordo de Mariana podem destravar rerating. DY de 8%.",
    thesis: "Vale negocia a 5.5x lucros. Risco-China é real mas preço já desconta cenário pessimista."
  },
  {
    ticker: "RADL3", name: "RD Saúde", sector: "Saúde", price: 26.80, change: 0.4,
    roe: 19.2, pl: 32.5, cagr5y: 24.1, upside: 12, confidence: "média",
    sparkline: [22, 23, 23, 24, 24, 25, 25, 26, 26, 27],
    maxBuyPrice: 28.00, targetPrice: 30.02,
    catalyst: "Expansão agressiva: 300 novas lojas/ano. Digitalização do marketplace de saúde.",
    thesis: "RD Saúde é a rede de farmácias mais eficiente do Brasil com moat regulatório."
  },
  {
    ticker: "ABEV3", name: "Ambev", sector: "Consumo", price: 13.20, change: 0.9,
    roe: 17.8, pl: 14.2, cagr5y: 5.1, upside: 14, confidence: "baixa",
    sparkline: [12, 12.2, 12.5, 12.8, 13, 12.8, 13, 13.1, 13.2, 13.2],
    maxBuyPrice: 14.00, targetPrice: 15.05,
    catalyst: "Premiumização do portfólio. Marcas como Spaten e Corona crescendo 30% a.a.",
    thesis: "Ambev é cash cow. Não é growth, mas DY + recompra entregam retorno sólido."
  },
];

export const alerts: Alert[] = [
  {
    id: "1",
    type: "euforia",
    ticker: "MGLU3",
    title: "⚠️ Euforia Extrema — MGLU3",
    description: "Volume de menções em redes sociais 4x acima da média. RSI em 82. Historicamente, esse nível antecede correções de -15% em 30 dias. EVITE COMPRA.",
    timestamp: "há 2h",
  },
  {
    id: "2",
    type: "oportunidade",
    ticker: "VALE3",
    title: "🟢 Buy the Dip — VALE3",
    description: "Queda de -6% em 5 dias por medo macro da China. Fundamentos intactos. P/L em 5.5x (mínima de 3 anos). Sentimento negativo em 78% — zona de reversão histórica.",
    timestamp: "há 45min",
  },
  {
    id: "3",
    type: "cautela",
    ticker: "PETR4",
    title: "🟡 Risco Político — PETR4",
    description: "Ruídos sobre mudança na política de dividendos. Aguardar definição do conselho em 15/03 antes de novas posições.",
    timestamp: "há 1h",
  },
  {
    id: "4",
    type: "oportunidade",
    ticker: "MRCP3",
    title: "🟢 Momentum — MRCP3",
    description: "CAGR de 52% e ROE de 28%. Backlog recorde. Ação rompeu resistência de R$8.00 com volume 3x acima da média. Alvo em R$11.40.",
    timestamp: "há 3h",
  },
];
