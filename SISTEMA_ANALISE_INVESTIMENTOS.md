# SISTEMA DE ANÁLISE DE INVESTIMENTOS — GROQ + LLAMA 3.1 405B
**Meta: 5% ao mês | B3 | Valorização de Preço**

---

## PROBLEMAS DO SISTEMA ATUAL

1. **Perda de contexto ao trocar de conta no Groq** — o modelo recomeça do zero, gerando análises incoerentes sem base de referência.
2. **Prompts fracos** — pedir só ROE e P/L desperdiça o potencial do Llama 3.1 405B. Teses rasas não batem 5% ao mês.
3. **Preço não persiste entre prompts** — sem o preço atual em cada etapa, upside, stop e alvo ficam incorretos.
4. **Sem critério duro de descarte** — o modelo sempre acha algo positivo. Precisamos de eliminação explícita.
5. **Perfis de operação misturados** — swing de 2 dias e position de 3 meses têm lógicas completamente diferentes.

---

## A SOLUÇÃO: BLOCO DE CONTEXTO MANUAL

O Groq não tem memória entre sessões. A solução é manter um documento de texto com as respostas de cada etapa e colar esse conteúdo no início de cada novo prompt.

**Template do bloco — cole no início de cada prompt a partir da Etapa 2:**

```
[===== CONTEXTO DO DIA =====]
DATA: DD/MM/AAAA
MACRO: Selic XX%, Dólar R$XX, Setores quentes: [X,Y], Evitar: [Z], Alerta: [descreva]
AÇÕES SELECIONADAS (Etapa 2):
- TICK1 | R$XX | ROE XX% | P/L XX | Perfil A/B | Motivo: [resumo]
RELEASES ANALISADOS (Etapa 3):
- TICK1: Nota X/10 | COMPRA/MONITORAR | Tese: [resumo]
[===== FIM DO CONTEXTO =====]
```

**Regra:** nunca envie um prompt avançado sem o contexto das etapas anteriores.

---

## FLUXO COMPLETO — 5 ETAPAS

| Etapa | Objetivo | Input | Output |
|-------|----------|-------|--------|
| 1 — Macro | Radar do cenário | Data de hoje | JSON: setores, alertas, tendências |
| 2 — Triagem CSV | Filtrar 318 empresas | Contexto + CSV completo | Tickers aprovados com motivos |
| 3 — Release | Análise profunda | Contexto + preço atual + PDF | Nota 0-10, tese, riscos |
| 4 — Estratégia | Montar operação | Contexto + preços atuais | Entrada, alvo, stop, R/R, ranking |
| 5 — Revisão | Revisar carteira ativa | Contexto + carteira atual | Manter, cortar ou aumentar |

---

## ETAPA 1 — RADAR MACRO

```
Você é um analista sênior de investimentos especializado na B3. Foco em valorização de preço, não dividendos.
Data de hoje: [DATA]. Não traga manchetes — foque no que ainda não está no radar do varejo.
Responda SOMENTE com JSON válido:

{
  "cenario_macro": {
    "selic_atual": "valor e tendência",
    "dolar_patamar": "valor e impacto em exportadoras/importadoras",
    "risco_politico_fiscal": "baixo/médio/alto — o que está em jogo",
    "fluxo_estrangeiro": "entrando ou saindo da B3 — impacto em quais setores"
  },
  "setores_acelerando": [
    { "setor": "nome", "motivo": "catalisador específico, não genérico", "estagio_ciclo": "começo/meio/fim", "timing": "curto/médio prazo" }
  ],
  "setores_a_evitar": [{ "setor": "nome", "motivo": "por que evitar agora" }],
  "catalisadores_proximas_semanas": [{ "evento": "descrição", "impacto": "quais setores e como" }],
  "narrativa_institucional": "O que fundos estão comprando que o varejo ainda não percebeu.",
  "armadilhas_momento": ["Onde o investidor comum está comprando euforia ou vendo topo como piso"],
  "megatendencias": [
    { "nome": "tendência", "setores_beneficiados": ["setor"], "estagio_ciclo": "começo/meio/fim", "paralelo_historico": "ex: Nvidia 2022, ouro 2018" }
  ],
  "resumo_executivo": "4-5 linhas do que o analista FARIA agora — ação, não descrição"
}
```

---

## ETAPA 2 — TRIAGEM DO CSV

O CSV tem 318 empresas e colunas: Empresa, Ticker, Setor, Valor de Mercado, P/L, P/VP, LPA, ROE, ROIC, Margem Líquida, Margem Bruta, Margem EBITDA, CAGR de Lucro, CAGR de Receita, Dívida Líq./EBITDA, Liquidez Corrente. Cole o arquivo completo no final do prompt.

```
[COLE O BLOCO DE CONTEXTO DA ETAPA 1]

Você é analista de ações da B3 focado em valorização de preço. Meta: 5% ao mês, operações de 2 dias a 3 meses.
Ignore empresas cujo único atrativo é dividendo sem crescimento.

PERFIL A — MOMENTUM RÁPIDO (2 a 15 dias):
ROE > 12% | P/L < 15 | ROIC > 10% | Dívida/EBITDA < 3,0 | Margem EBITDA > 10% | Setor com catalisador no macro

PERFIL B — POSIÇÃO CONSISTENTE (1 a 3 meses):
ROE > 15% | CAGR Receita > 8% | CAGR Lucro > 10% | Dívida/EBITDA < 2,5 | Margem Líquida > 8% | Setor com vento a favor

ELIMINAÇÃO IMEDIATA (sem análise):
Dívida/EBITDA > 4,0 | ROE negativo | CAGR Receita negativo | Setor "a evitar" no macro | Liquidez Corrente < 0,7

Responda SOMENTE com JSON válido:

{
  "acoes_selecionadas": [
    {
      "ticker": "XXXX3", "empresa": "Nome", "setor": "Setor", "perfil": "A/B/A+B",
      "roe": 0.0, "roic": 0.0, "pl": 0.0, "margem_ebitda": 0.0, "divida_ebitda": 0.0, "cagr_receita": 0.0,
      "motivo_selecao": "o que nos dados chama atenção — seja preciso",
      "catalisador_provavel": "o que pode mover o preço",
      "risco_principal": "o que pode derrubar a tese"
    }
  ],
  "total_selecionadas": 0,
  "principais_motivos_descarte": "padrões que eliminaram a maioria",
  "observacao_do_analista": "o que o conjunto de dados revela sobre o mercado hoje"
}

[CSV COMPLETO ABAIXO]
```

---

## ETAPA 3 — ANÁLISE DO RELEASE

Um prompt por empresa. Só empresas com **nota ≥ 6** avançam para a Etapa 4. **Sempre passe o preço atual** — sem ele o valuation não tem sentido.

```
[COLE O BLOCO DE CONTEXTO ATUALIZADO]

Você é analista sênior especializado em value investing e momentum na B3.
Analise o release da empresa {TICKER} — {NOME}.

DADOS ATUAIS:
Preço atual: R$ {PRECO_ATUAL} | ROE: {ROE}% | P/L: {PL} | ROIC: {ROIC}% | Dívida/EBITDA: {DIV_EBITDA}
Motivo da pré-seleção: {MOTIVO DO PASSO 2}

Analise com precisão — sem generalismos:
1. SAÚDE FINANCEIRA: geração de caixa, tendência de margens, qualidade do lucro (caixa real ou contábil?)
2. GESTÃO: execução, alocação de capital (CAPEX, recompras, M&A), transparência com o acionista
3. CATALISADORES: o que especificamente pode fazer subir em 1-6 meses? (contratos, expansão, ciclo, margem)
4. RISCOS REAIS: não os genéricos do release — os concretos DESTA empresa que podem derrubar o preço
5. VALUATION: com preço de R${PRECO_ATUAL}, está cara/justa/barata? Calcule preço teto e upside %
6. NOTA: 0-10. Abaixo de 6 = DESCARTAR. 6-7 = MONITORAR. 8-10 = COMPRA.

Responda SOMENTE com JSON válido:

{
  "ticker": "XXXX3", "preco_atual_usado": 0.00, "nota": 0.0,
  "recomendacao": "COMPRA FORTE / COMPRA / MONITORAR / DESCARTAR",
  "saude_financeira": { "geracao_caixa": "", "tendencia_margens": "", "endividamento": "", "qualidade_lucro": "" },
  "qualidade_gestao": "análise em 3-4 linhas",
  "catalisadores": [{ "descricao": "", "prazo": "semanas/meses", "impacto": "alto/médio/baixo" }],
  "riscos_reais": [{ "descricao": "", "probabilidade": "alta/média/baixa", "impacto": "alto/médio/baixo" }],
  "valuation": { "situacao": "cara/justa/barata", "preco_teto_estimado": 0.00, "upside_potencial_pct": 0.0, "justificativa": "" },
  "tese_resumida": "por que comprar ou não — 4 a 6 linhas diretas",
  "ponto_critico": "o único fator que mudaria sua opinião sobre essa ação"
}

[RELEASE ABAIXO]
```

---

## ETAPA 4 — ESTRATÉGIA OPERACIONAL

Apenas para aprovadas (nota ≥ 6). Atualize os preços no momento de montar o prompt. Só execute operações com **R/R ≥ 2,0**.

```
[COLE O BLOCO DE CONTEXTO COMPLETO — MACRO + TRIAGEM + RELEASES]

Você é estrategista de operações de curto e médio prazo na B3. Meta: 5% ao mês.

APROVADAS com preços ATUAIS:
- {TICKER1} | Nota {X}/10 | Preço ATUAL: R${PRECO} | Perfil: {A/B}
- {TICKER2} | Nota {X}/10 | Preço ATUAL: R${PRECO} | Perfil: {A/B}

Para cada ação, monte:
1. ENTRADA: pode entrar agora ou aguardar? Se aguardar, qual preço e qual gatilho?
2. ALVOS: alvo conservador e otimista (R$) | critério de saída antecipada
3. STOP: preço exato e justificativa do nível
4. R/R: calcule (Alvo - Entrada) / (Entrada - Stop). Se < 2,0, descarte ou ajuste.
5. TEMPO: dias/semanas estimados | o que pode acelerar ou atrasar a tese
6. ALOCAÇÃO: % do portfólio sugerido | convicção: Alta/Média/Baixa
7. ANTI-MANADA: já é manchete? Sustentado por fundamento ou euforia? Institucionais ainda comprando?

Responda SOMENTE com JSON válido:

{
  "estrategias": [
    {
      "ticker": "", "tipo_operacao": "Swing Trade / Position Trade", "preco_atual": 0.00,
      "entrada": { "pode_entrar_agora": true, "preco_ideal": 0.00, "gatilho": "" },
      "alvos": { "conservador": 0.00, "otimista": 0.00, "upside_conservador_pct": 0.0, "saida_antecipada": "" },
      "stop": { "preco": 0.00, "perda_pct": 0.0, "justificativa": "" },
      "risco_retorno": 0.0, "tempo_estimado": "", "alocacao_pct": 0.0, "convicao": "Alta/Média/Baixa",
      "anti_manada": { "ja_e_manchete": false, "sustentado_por_fundamento": true, "conclusao": "" }
    }
  ],
  "ranking": [{ "posicao": 1, "ticker": "", "justificativa": "2 linhas — por que é a melhor entrada agora" }],
  "carteira": { "total_alocado_pct": 0.0, "caixa_reserva_pct": 0.0, "observacao": "" }
}
```

---

## ETAPA 5 — REVISÃO MENSAL

```
[COLE O BLOCO DE CONTEXTO COM O CENÁRIO MAIS RECENTE]

Você é analista de carteiras na B3. Revise as posições abaixo sem apego.
Critério único: a carteira deve ter as melhores oportunidades de agora, não defender o que foi comprado.

CARTEIRA ATUAL:
- {TICKER1} | PM: R${PM} | Atual: R${PA} | Resultado: {+/-X%} | % carteira: {X%}

Para cada posição: a tese original ainda vale? O upside ainda existe? Há algo melhor para esse capital agora?

Responda SOMENTE com JSON válido:

{
  "analise_posicoes": [
    {
      "ticker": "", "resultado_pct": 0.0, "tese_valida": true,
      "upside_restante": "alto/médio/baixo/nenhum",
      "acao": "MANTER / AUMENTAR / REDUZIR PARCIAL / VENDER TUDO",
      "justificativa": "2-3 linhas diretas"
    }
  ],
  "parecer_geral": {
    "cortar": [], "manter": [], "aumentar": [],
    "oportunidade_faltando": "existe algo melhor para esse capital?",
    "saude_carteira": "resumo honesto em 3-4 linhas"
  }
}
```

---

## REGRAS DE OURO

- Etapa 1 é obrigatória toda sessão — especialmente ao trocar de conta no Groq
- Nunca pule etapas. Cada filtro protege o capital
- Nota < 6 na Etapa 3 = empresa descartada, não avança
- R/R < 2,0 na Etapa 4 = operação não executada
- Sempre atualize o preço atual antes das Etapas 3 e 4
- Se o JSON vier truncado: `"Continue o JSON a partir de onde parou"`
- Se o JSON vier inválido: `"Corrija o JSON anterior, estava malformado"`
- O Llama 3.1 405B processa o CSV completo de 318 empresas sem problema — sempre mande o arquivo inteiro