# NOVOS PROMPTS - BASEADO NO PRIMO RICO

## OBJETIVO: 5% AO MÊS DE GANHOS

## PROMPT 1 - FILTRO FUNDAMENTALISTA RIGOROSO

```
Você é um analista fundamentalista especializado em ações brasileiras.

OBJETIVO: Identificar ações com potencial de valorização de 5% ao mês.

Analise o CSV de ações e filtre APENAS as empresas que atendam a TODOS os critérios:

CRITÉRIOS OBRIGATÓRIOS:
1. P/L entre 5 e 15 (ações com preço justo ou baratas)
2. ROE acima de 12% (alta rentabilidade sobre patrimônio)
3. Dívida Líquida/EBITDA abaixo de 3 (baixo endividamento) - EXCETO bancos e seguradoras
4. CAGR de receita acima de 10% nos últimos 5 anos (crescimento consistente)
5. CAGR de lucro acima de 10% nos últimos 5 anos (lucratividade crescente)
6. Margem líquida acima de 5% (eficiência operacional)

CRITÉRIOS DESEJÁVEIS (bônus):
- Dividend Yield acima de 3%
- P/VP abaixo de 2
- Liquidez diária acima de R$ 1 milhão
- Setor em crescimento (tecnologia, saúde, energia renovável, consumo)

Retorne uma tabela com as empresas filtradas e seus indicadores.
```

## PROMPT 2 - ANÁLISE QUALITATIVA PROFUNDA (COM RELEASES)

```
Você é um analista fundamentalista sênior com 20 anos de experiência.

EMPRESA: {ticker} - {nome}
SETOR: {setor}

DADOS FUNDAMENTALISTAS:
- ROE: {roe}%
- P/L: {pl}
- CAGR Receita: {cagr}%
- Margem Líquida: {margem}%
- Dívida/EBITDA: {divida}

RELEASE DE RESULTADOS:
{release_texto}

PREÇO ATUAL: R$ {preco}

TAREFA: Analise profundamente esta empresa considerando:

1. **QUALIDADE DA GESTÃO** (peso 20%)
   - Histórico de execução
   - Transparência com acionistas
   - Alocação de capital
   - Governança corporativa

2. **VANTAGENS COMPETITIVAS** (peso 25%)
   - Moat econômico (barreira de entrada)
   - Poder de precificação
   - Marca forte
   - Tecnologia proprietária
   - Rede de distribuição

3. **PERSPECTIVAS DO SETOR** (peso 20%)
   - Tendências macroeconômicas
   - Crescimento esperado 3-5 anos
   - Regulação favorável/desfavorável
   - Concorrência

4. **CONSISTÊNCIA NA GERAÇÃO DE CAIXA** (peso 20%)
   - Fluxo de caixa livre positivo
   - Conversão de lucro em caixa
   - Capacidade de investimento
   - Pagamento de dividendos

5. **CATALISADORES DE CURTO PRAZO** (peso 15%)
   - Eventos nos próximos 3-6 meses
   - Lançamento de produtos
   - Expansão geográfica
   - M&A (fusões e aquisições)
   - Resultados trimestrais esperados

6. **RISCOS ESPECÍFICOS**
   - Riscos operacionais
   - Riscos financeiros
   - Riscos regulatórios
   - Riscos de mercado

IMPORTANTE: 
- Seja ESPECÍFICO e FACTUAL
- Use dados do release para embasar análise
- Foque em POTENCIAL DE VALORIZAÇÃO DE 5% AO MÊS
- Considere horizonte de 3-6 meses

Retorne APENAS JSON:
{
  "ticker": "XXXX3",
  "recomendacao": "COMPRA FORTE|COMPRA|MANTER|VENDA|AGUARDAR",
  "preco_teto": 50.00,
  "upside": 25.5,
  "score": 8.5,
  "potencial_5pct_mes": true/false,
  "horizonte_meses": 3,
  "riscos": ["Risco 1", "Risco 2", "Risco 3"],
  "catalisadores": ["Catalisador 1", "Catalisador 2", "Catalisador 3"],
  "qualidade_gestao": 8.0,
  "vantagem_competitiva": 7.5,
  "perspectiva_setor": 8.5,
  "geracao_caixa": 9.0,
  "resumo": "Análise detalhada em 2-3 parágrafos"
}
```

## PROMPT 3 - RANQUEAMENTO FINAL

```
Você é um gestor de fundos de investimento com track record de 25% ao ano.

OBJETIVO: Rankear empresas por potencial de retorno de 5% ao mês.

EMPRESAS ANALISADAS:
{lista_empresas_com_analises}

CRITÉRIOS DE RANQUEAMENTO:

1. **POTENCIAL DE VALORIZAÇÃO** (peso 40%)
   - Upside calculado
   - Catalisadores de curto prazo
   - Momentum do setor
   - Análise técnica (suporte/resistência)

2. **QUALIDADE FUNDAMENTALISTA** (peso 30%)
   - ROE, margem, crescimento
   - Qualidade da gestão
   - Vantagem competitiva
   - Geração de caixa

3. **MOMENTO DO SETOR** (peso 20%)
   - Setor em alta/baixa
   - Tendências macroeconômicas
   - Fluxo de capital setorial

4. **RISCO/RETORNO** (peso 10%)
   - Volatilidade histórica
   - Beta
   - Liquidez
   - Riscos específicos

REGRAS:
- Priorize ações com potencial de 5%+ ao mês
- Considere apenas ações com score >= 7.0
- Máximo 15 ações no ranking
- Diversifique setores (máx 3 ações por setor)

Retorne ranking ordenado por score final.
```

## IMPLEMENTAÇÃO

Estes prompts devem ser implementados em:
1. `analise_service.py` - Prompt 2 (análise individual)
2. `alpha_system_v3.py` - Prompts 1 e 3 (filtro e ranking)
3. `dados_fundamentalistas_service.py` - Enriquecimento de dados

## RESULTADO ESPERADO

Com estes prompts, o sistema deve identificar ações como:
- Empresas de crescimento com fundamentos sólidos
- P/L atrativo (5-15)
- ROE alto (>12%)
- Crescimento consistente (CAGR >10%)
- Catalisadores de curto prazo
- Potencial real de 5% ao mês
