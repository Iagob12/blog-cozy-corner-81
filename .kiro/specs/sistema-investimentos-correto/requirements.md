# Requirements Document - Sistema de Investimentos com IA

## Introduction

Sistema completo de análise de investimentos que utiliza IA (Gemini) para identificar as melhores oportunidades de valorização de preço (5% ao mês). O sistema deve seguir um fluxo específico de 3 prompts sequenciais, garantindo que todos os dados estejam atualizados e corretos.

## Glossary

- **Gemini**: Modelo de IA do Google usado para análise
- **CSV**: Arquivo com dados fundamentalistas das ações
- **Release de Resultados**: Relatório trimestral oficial da empresa
- **Ticker**: Código da ação (ex: PETR4, VALE3)
- **ROE**: Return on Equity (Retorno sobre Patrimônio)
- **CAGR**: Compound Annual Growth Rate (Taxa de Crescimento Anual Composta)
- **P/L**: Preço sobre Lucro
- **Upside**: Potencial de valorização
- **Swing Trade**: Operação de curto prazo (5-20 dias)

## Requirements

### Requirement 1: Radar de Oportunidades (Prompt 1)

**User Story:** Como investidor, quero que a IA identifique setores em fase inicial de aceleração ANTES da manada, para entrar no começo do movimento e não comprar o topo.

#### Acceptance Criteria

1. WHEN o sistema inicia a análise THEN a IA SHALL executar o Prompt 1 para identificar setores quentes
2. WHEN o Prompt 1 é executado THEN a IA SHALL analisar o cenário macroeconômico atual (data de hoje)
3. WHEN a análise macro é feita THEN a IA SHALL identificar setores em fase inicial de aceleração com catalisador claro nos próximos 3-12 meses
4. WHEN setores são identificados THEN a IA SHALL classificar cada setor em: começo, meio ou fim do ciclo
5. WHEN a análise é concluída THEN o sistema SHALL retornar lista de setores promissores com justificativa

**Prompt 1 Completo:**
```
Você é um analista especializado em identificar movimentos de valorização de preço antes da manada. 

Analise o cenário macroeconômico atual (DATA DE HOJE: {data_hoje}) e responda:

1) Quais setores estão em fase inicial de aceleração com catalisador claro nos próximos 3-12 meses? Não me traga o que já virou manchete.

2) Existe algum movimento se formando agora parecido com o que aconteceu com Nvidia, Ouro ou Bitcoin antes de explodirem — algo que ainda não está no radar do investidor comum?

3) Quais países, moedas ou commodities estão sinalizando mudança de ciclo?

4) Tem alguma narrativa sendo construída no mercado institucional que o varejo ainda não percebeu?

Para cada ponto, me diga em que estágio do ciclo está — começo, meio ou fim. Quero entrar no começo, não comprar o topo.
```

### Requirement 2: Triagem Fundamentalista (Prompt 2)

**User Story:** Como investidor, quero que a IA analise o CSV de ações DE HOJE e filtre apenas empresas com potencial de valorização de preço (não dividendos), para ter uma lista ranqueada das melhores oportunidades.

#### Acceptance Criteria

1. WHEN o Prompt 1 é concluído THEN o sistema SHALL baixar o CSV mais recente de investimentos.com.br
2. WHEN o CSV é baixado THEN o sistema SHALL verificar que os dados são de hoje (data atual)
3. WHEN o CSV é validado THEN o sistema SHALL enviar o CSV completo junto com o Prompt 2 para a IA
4. WHEN a IA recebe o CSV THEN a IA SHALL filtrar empresas com: P/L < 15, ROE > 15%, CAGR > 12%, Dívida/EBITDA < 2.5
5. WHEN a filtragem é feita THEN a IA SHALL considerar os setores identificados no Prompt 1
6. WHEN a análise é concluída THEN a IA SHALL retornar tabela ranqueada do maior para menor potencial de valorização
7. WHEN a tabela é retornada THEN cada empresa SHALL ter justificativa do "por que ela aparece aqui"

**Prompt 2 Completo:**
```
Analise a planilha de ações anexada (DATA DO CSV: {data_csv}) e filtre as empresas com maior potencial de valorização de preço. 

IMPORTANTE: Ignore empresas cujo principal atrativo seja dividendo.

Critérios obrigatórios:
- P/L abaixo de 15
- ROE acima de 15%
- CAGR de receita acima de 12% nos últimos 3 anos
- Dívida Líquida/EBITDA abaixo de 2,5
- Margem líquida crescente ou estável nos últimos 3 trimestres

Critérios de desempate — valorize empresas com:
- Histórico de recompra de ações
- Expansão de mercado endereçável
- Setor com vento a favor no cenário atual (considere os setores identificados anteriormente: {setores_prompt1})

Retorne uma tabela ranqueada do maior para o menor potencial de valorização de preço. Para cada empresa, adicione uma linha de 'por que ela aparece aqui' — o que nos dados chama atenção.

[CSV ANEXADO]
```

### Requirement 3: Análise Profunda com Release de Resultados (Prompt 3)

**User Story:** Como investidor, quero que a IA analise os relatórios trimestrais MAIS RECENTES de cada empresa selecionada, para ter uma análise profunda e comparativa antes de decidir onde investir.

#### Acceptance Criteria

1. WHEN o Prompt 2 retorna as empresas ranqueadas THEN o sistema SHALL buscar o Release de Resultados mais recente de cada empresa
2. WHEN busca o Release THEN o sistema SHALL acessar o site oficial de RI da empresa
3. WHEN acessa o site de RI THEN o sistema SHALL identificar o relatório trimestral mais recente (Q4 2025 ou mais atual)
4. WHEN identifica o relatório THEN o sistema SHALL baixar o PDF completo
5. WHEN o PDF é baixado THEN o sistema SHALL extrair o texto completo do documento
6. WHEN todos os Releases são coletados THEN o sistema SHALL enviar TODOS os documentos junto com o Prompt 3 para a IA
7. WHEN a IA recebe os documentos THEN a IA SHALL analisar cada empresa individualmente
8. WHEN análise individual é feita THEN a IA SHALL comparar todas as empresas entre si
9. WHEN comparação é feita THEN a IA SHALL retornar ranking das 3 MELHORES para valorização de preço
10. WHEN ranking é retornado THEN cada empresa SHALL ter: saúde financeira, qualidade da gestão, catalisadores, riscos reais, e avaliação de preço (cara/justa/barata)

**Prompt 3 Completo:**
```
Você vai receber relatórios administrativos, demonstrações financeiras ou qualquer documentação de múltiplas empresas (DATA DOS RELATÓRIOS: {data_relatorios}).

Analise cada uma individualmente e depois compare todas entre si.

Para cada empresa avalie:

1) Saúde financeira real — endividamento, geração de caixa, margem e tendência dos últimos trimestres.

2) Qualidade da gestão — o que os relatórios mostram sobre execução, alocação de capital e transparência com o acionista?

3) Catalisadores de valorização de preço — o que pode fazer essa ação subir nos próximos 6 a 18 meses? Seja específico: contrato, expansão, ciclo setorial, melhora de margem.

4) Riscos reais e concretos — não os genéricos de qualquer relatório, os que realmente podem derrubar o preço dessa empresa específica.

5) Preço: com base nos fundamentos, a ação está cara, justa ou barata agora? IMPORTANTE: Compare com o preço ATUAL de mercado (DATA: {data_hoje}, PREÇO: {preco_atual}).

Após analisar todas individualmente, faça uma comparação final e me entregue um ranking das 3 melhores para o meu objetivo, que é: valorização de preço, não dividendos. Quero comprar bem, esperar o movimento e vender com lucro.

Me diga qual entrar primeiro, qual monitorar e qual descartar — com justificativa real para cada decisão.

[RELATÓRIOS DAS EMPRESAS ANEXADOS]
```

### Requirement 4: Validação de Dados Atualizados

**User Story:** Como investidor, quero garantir que TODOS os dados usados pela IA estejam atualizados (de hoje), para evitar recomendações baseadas em informações antigas.

#### Acceptance Criteria

1. WHEN o sistema busca CSV THEN o sistema SHALL verificar a data do arquivo
2. WHEN a data do CSV é verificada THEN o sistema SHALL rejeitar CSV com mais de 24 horas
3. WHEN o sistema busca preços THEN o sistema SHALL usar apenas preços de hoje via API em tempo real
4. WHEN preços são obtidos THEN o sistema SHALL incluir timestamp de quando o preço foi consultado
5. WHEN Release é baixado THEN o sistema SHALL verificar a data do relatório trimestral
6. WHEN envia dados para IA THEN o sistema SHALL incluir data de cada informação no prompt
7. WHEN IA faz recomendação THEN a recomendação SHALL incluir data de referência de todos os dados usados

### Requirement 5: Swing Trade (Prompt 4 - Opcional)

**User Story:** Como investidor, quero analisar uma ação específica para operação de curto prazo (5-20 dias), para aproveitar movimentos rápidos com boa relação risco/retorno.

#### Acceptance Criteria

1. WHEN usuário solicita análise de swing trade THEN o sistema SHALL executar Prompt 4 para o ticker específico
2. WHEN Prompt 4 é executado THEN a IA SHALL verificar saúde atual da empresa
3. WHEN saúde é verificada THEN a IA SHALL identificar eventos próximos que podem mover o preço
4. WHEN eventos são identificados THEN a IA SHALL analisar momento técnico (suporte, rompimento, esgotamento)
5. WHEN análise técnica é feita THEN a IA SHALL identificar gatilho concreto para movimento nos próximos dias
6. WHEN gatilho é identificado THEN a IA SHALL calcular risco/retorno (stop e alvo)
7. WHEN risco/retorno é calculado THEN a IA SHALL recomendar operação APENAS se retorno >= 2x risco

### Requirement 6: Revisão Mensal de Carteira (Prompt 5 - Opcional)

**User Story:** Como investidor, quero revisar minha carteira mensalmente sem apego emocional, para garantir que meu capital está sempre na melhor alocação possível.

#### Acceptance Criteria

1. WHEN usuário solicita revisão de carteira THEN o sistema SHALL executar Prompt 5
2. WHEN Prompt 5 é executado THEN a IA SHALL analisar cada posição individualmente
3. WHEN posição é analisada THEN a IA SHALL verificar se tese original ainda está de pé
4. WHEN tese é verificada THEN a IA SHALL avaliar se preço atual ainda tem upside real
5. WHEN upside é avaliado THEN a IA SHALL comparar com oportunidades atuais no mercado
6. WHEN comparação é feita THEN a IA SHALL recomendar: cortar, manter, aumentar ou substituir
7. WHEN recomendações são feitas THEN a IA SHALL ser direta e honesta (sem validação emocional)

### Requirement 7: Verificação Anti-Manada (Prompt 6 - Obrigatório)

**User Story:** Como investidor, quero verificar se não estou comprando o topo (seguindo a manada), para entrar apenas no começo de movimentos reais.

#### Acceptance Criteria

1. WHEN sistema recomenda uma ação THEN o sistema SHALL executar Prompt 6 automaticamente
2. WHEN Prompt 6 é executado THEN a IA SHALL verificar se ativo virou pauta comum em mídias
3. WHEN pauta é verificada THEN a IA SHALL analisar se movimento é sustentado por fundamento ou euforia
4. WHEN fundamento é analisado THEN a IA SHALL verificar posicionamento de institucionais
5. WHEN posicionamento é verificado THEN a IA SHALL comparar com histórico de situações similares
6. WHEN comparação é feita THEN a IA SHALL concluir: entrar agora, esperar correção, ou janela fechou
7. WHEN conclusão é "janela fechou" THEN o sistema SHALL remover ação da lista de recomendações

### Requirement 8: Fluxo Completo Integrado

**User Story:** Como investidor, quero que o sistema execute automaticamente todo o fluxo de análise na sequência correta, para ter recomendações precisas e atualizadas.

#### Acceptance Criteria

1. WHEN sistema inicia THEN o sistema SHALL executar Prompt 1 (Radar de Oportunidades)
2. WHEN Prompt 1 termina THEN o sistema SHALL baixar CSV de hoje
3. WHEN CSV é baixado THEN o sistema SHALL executar Prompt 2 (Triagem Fundamentalista)
4. WHEN Prompt 2 termina THEN o sistema SHALL buscar Releases das empresas selecionadas
5. WHEN Releases são coletados THEN o sistema SHALL executar Prompt 3 (Análise Profunda)
6. WHEN Prompt 3 termina THEN o sistema SHALL executar Prompt 6 (Anti-Manada) para cada recomendação
7. WHEN Prompt 6 aprova THEN o sistema SHALL buscar preços ATUAIS de mercado
8. WHEN preços são obtidos THEN o sistema SHALL retornar ranking final com todas as informações
9. WHEN ranking é retornado THEN cada ação SHALL ter: rank, ticker, preço atual (com data/hora), upside, recomendação, catalisadores, riscos, e data de todos os dados usados

### Requirement 9: Logs e Rastreabilidade

**User Story:** Como investidor, quero ver logs detalhados de todo o processo, para entender exatamente quais dados foram usados e quando.

#### Acceptance Criteria

1. WHEN cada etapa é executada THEN o sistema SHALL registrar log com timestamp
2. WHEN CSV é baixado THEN o log SHALL incluir: data do CSV, número de ações, fonte
3. WHEN preços são buscados THEN o log SHALL incluir: hora da consulta, fonte, número de preços obtidos
4. WHEN Release é baixado THEN o log SHALL incluir: empresa, data do relatório, trimestre
5. WHEN IA é consultada THEN o log SHALL incluir: prompt usado, modelo, tempo de resposta
6. WHEN erro ocorre THEN o log SHALL incluir: tipo de erro, etapa que falhou, fallback usado
7. WHEN análise é concluída THEN o sistema SHALL gerar relatório com todas as datas e fontes usadas

### Requirement 10: Interface de Resultados

**User Story:** Como investidor, quero ver os resultados de forma clara e organizada, com todas as informações relevantes para tomar decisão.

#### Acceptance Criteria

1. WHEN análise é concluída THEN o sistema SHALL exibir ranking de 1 a 15
2. WHEN ranking é exibido THEN cada ação SHALL mostrar: ticker, nome, setor, preço atual (com hora)
3. WHEN ação é exibida THEN SHALL mostrar: preço de entrada recomendado, preço teto, upside %
4. WHEN upside é mostrado THEN SHALL mostrar: tempo estimado, confiança da recomendação
5. WHEN recomendação é exibida THEN SHALL mostrar: catalisadores (lista), riscos (lista)
6. WHEN riscos são mostrados THEN SHALL mostrar: análise anti-manada (aprovado/reprovado)
7. WHEN análise anti-manada é mostrada THEN SHALL mostrar: data e hora de todos os dados usados
8. WHEN usuário clica em ação THEN SHALL exibir: análise completa do Release, comparação com concorrentes

---

## Resumo do Fluxo

```
1. PROMPT 1 (Radar) → Identifica setores quentes
   ↓
2. Baixa CSV DE HOJE
   ↓
3. PROMPT 2 (Triagem) → Filtra empresas (considera setores do Prompt 1)
   ↓
4. Busca Releases MAIS RECENTES de cada empresa
   ↓
5. PROMPT 3 (Análise Profunda) → Analisa Releases + Compara empresas
   ↓
6. PROMPT 6 (Anti-Manada) → Valida cada recomendação
   ↓
7. Busca PREÇOS ATUAIS (com timestamp)
   ↓
8. Retorna RANKING FINAL com todas as informações
```

---

**Objetivo:** Carteira que renda 5% ao mês através de VALORIZAÇÃO DE PREÇO (não dividendos).

**Garantia:** Todos os dados (CSV, preços, releases) devem ser de HOJE ou mais recentes, com data/hora registrada.
