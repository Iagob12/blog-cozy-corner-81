# Tasks - Sistema de Investimentos Correto

## Overview

Este documento lista todas as tarefas necessárias para implementar o sistema de investimentos que segue o fluxo correto de 3 prompts com validação de freshness.

## Task 1: Criar Gemini Client Unificado

**Status:** ⬜ Not Started

**Descrição:** Criar classe unificada para comunicação com Gemini AI.

**Arquivos:**
- `backend/app/services/gemini_client.py` (criar)

**Checklist:**
- [ ] Criar classe GeminiClient
- [ ] Implementar método executar_prompt()
- [ ] Adicionar timestamp automático em todos os prompts
- [ ] Implementar parser de JSON robusto
- [ ] Adicionar retry logic (3 tentativas)
- [ ] Adicionar logging detalhado
- [ ] Tratar erros de API (rate limit, timeout, etc)
- [ ] Testar com prompt simples

**Acceptance Criteria:**
- Gemini responde corretamente a prompts
- JSON é parseado sem erros
- Timestamps são incluídos automaticamente
- Retry funciona em caso de falha
- Logs mostram todas as chamadas

---

## Task 2: Melhorar Investimentos Scraper (V2)

**Status:** ⬜ Not Started

**Descrição:** Adicionar validação rigorosa de freshness no CSV.

**Arquivos:**
- `backend/app/services/investimentos_scraper.py` (modificar)

**Checklist:**
- [ ] Adicionar método validar_freshness()
- [ ] Rejeitar CSV com > 24 horas
- [ ] Adicionar timestamp em cada linha do CSV
- [ ] Implementar fallback para múltiplas fontes
- [ ] Adicionar logging com data do CSV
- [ ] Retornar tupla (csv_path, timestamp)
- [ ] Testar com CSV antigo (deve rejeitar)
- [ ] Testar com CSV novo (deve aceitar)

**Acceptance Criteria:**
- CSV antigo é rejeitado
- CSV novo é aceito
- Timestamp é registrado
- Logs mostram data do CSV
- Fallback funciona se fonte principal falhar

---

## Task 3: Melhorar Release Downloader (V2)

**Status:** ⬜ Not Started

**Descrição:** Adicionar validação de trimestre (Q4 2025+).

**Arquivos:**
- `backend/app/services/release_downloader.py` (modificar)

**Checklist:**
- [ ] Adicionar método extrair_data_relatorio()
- [ ] Implementar validação de trimestre (Q4 2025+)
- [ ] Rejeitar relatórios antigos
- [ ] Adicionar suporte para mais sites de RI
- [ ] Implementar OCR como fallback
- [ ] Retornar tupla (pdf_path, trimestre, data)
- [ ] Adicionar logging com data do relatório
- [ ] Testar com PDF real

**Acceptance Criteria:**
- Data é extraída corretamente do PDF
- Relatórios antigos são rejeitados
- Relatórios Q4 2025+ são aceitos
- Logs mostram trimestre e data
- OCR funciona se extração falhar

---

## Task 4: Implementar Alpha System V3

**Status:** ⬜ Not Started

**Descrição:** Criar sistema completo que segue fluxo de 6 prompts.

**Arquivos:**
- `backend/app/services/alpha_system_v3.py` (criar)

**Checklist:**
- [ ] Criar classe AlphaSystemV3
- [ ] Implementar método executar_analise_completa()
- [ ] Implementar _prompt_1_radar_oportunidades()
- [ ] Implementar _validar_csv_freshness()
- [ ] Implementar _prompt_2_triagem_fundamentalista()
- [ ] Implementar _baixar_releases_recentes()
- [ ] Implementar _prompt_3_analise_profunda()
- [ ] Implementar _prompt_6_anti_manada()
- [ ] Implementar _buscar_precos_atuais()
- [ ] Implementar _gerar_log_completo()
- [ ] Adicionar tratamento de erros em cada etapa
- [ ] Adicionar logging detalhado
- [ ] Testar fluxo completo

**Acceptance Criteria:**
- Prompt 1 identifica setores quentes
- CSV é validado (< 24h)
- Prompt 2 filtra empresas considerando setores do Prompt 1
- Releases são baixados e validados (Q4 2025+)
- Prompt 3 analisa Releases e compara empresas
- Prompt 6 valida cada recomendação
- Preços atuais são buscados com timestamp
- Ranking final inclui todas as informações
- Logs mostram data de cada dado usado

---

## Task 5: Criar Prompt Templates

**Status:** ⬜ Not Started

**Descrição:** Criar templates para os 6 prompts.

**Arquivos:**
- `backend/app/prompts/prompt_templates.py` (criar)

**Checklist:**
- [ ] Criar PROMPT_1_RADAR_TEMPLATE
- [ ] Criar PROMPT_2_TRIAGEM_TEMPLATE
- [ ] Criar PROMPT_3_ANALISE_TEMPLATE
- [ ] Criar PROMPT_6_ANTI_MANADA_TEMPLATE
- [ ] Adicionar placeholders para variáveis
- [ ] Adicionar instruções para retorno JSON
- [ ] Documentar cada prompt
- [ ] Testar formatação de cada template

**Acceptance Criteria:**
- Todos os prompts incluem data/hora
- Placeholders são substituídos corretamente
- Instruções de JSON são claras
- Templates são reutilizáveis

---

## Task 6: Implementar Data Models

**Status:** ⬜ Not Started

**Descrição:** Criar dataclasses para estruturar dados.

**Arquivos:**
- `backend/app/models/investment_models.py` (criar)

**Checklist:**
- [ ] Criar StockData dataclass
- [ ] Criar ReleaseData dataclass
- [ ] Criar PriceData dataclass
- [ ] Criar AnaliseCompleta dataclass
- [ ] Adicionar validação de tipos
- [ ] Adicionar métodos to_dict()
- [ ] Adicionar métodos from_dict()
- [ ] Documentar cada campo

**Acceptance Criteria:**
- Dataclasses são type-safe
- Conversão para/de dict funciona
- Validação de tipos funciona
- Documentação está clara

---

## Task 7: Atualizar Endpoint Principal

**Status:** ⬜ Not Started

**Descrição:** Atualizar endpoint para usar Alpha System V3.

**Arquivos:**
- `backend/app/main.py` (modificar)

**Checklist:**
- [ ] Importar AlphaSystemV3
- [ ] Atualizar endpoint /api/v1/final/top-picks
- [ ] Adicionar tratamento de erros
- [ ] Adicionar logging
- [ ] Adicionar cache (5 minutos)
- [ ] Retornar estrutura correta
- [ ] Testar endpoint

**Acceptance Criteria:**
- Endpoint retorna ranking completo
- Estrutura JSON está correta
- Erros são tratados gracefully
- Cache funciona
- Logs mostram execução

---

## Task 8: Adicionar Validação de Freshness

**Status:** ⬜ Not Started

**Descrição:** Adicionar validação rigorosa em todos os pontos.

**Arquivos:**
- `backend/app/utils/validators.py` (criar)

**Checklist:**
- [ ] Criar função validar_csv_freshness()
- [ ] Criar função validar_release_freshness()
- [ ] Criar função validar_preco_freshness()
- [ ] Criar exceção DataFreshnessError
- [ ] Adicionar logging de validações
- [ ] Testar cada validação

**Acceptance Criteria:**
- CSV antigo é rejeitado
- Release antigo é rejeitado
- Preço antigo é rejeitado
- Exceções são lançadas corretamente
- Logs mostram validações

---

## Task 9: Implementar Logging Completo

**Status:** ⬜ Not Started

**Descrição:** Adicionar logging detalhado em todo o sistema.

**Arquivos:**
- `backend/app/utils/logger.py` (criar)
- Todos os arquivos de serviços (modificar)

**Checklist:**
- [ ] Configurar logger com formato padrão
- [ ] Adicionar timestamp em todos os logs
- [ ] Adicionar contexto (etapa, ticker, etc)
- [ ] Criar arquivo de log (alpha_system.log)
- [ ] Adicionar rotação de logs
- [ ] Testar logging em cada etapa

**Acceptance Criteria:**
- Todos os logs incluem timestamp
- Logs incluem contexto relevante
- Arquivo de log é criado
- Rotação funciona
- Logs são legíveis

---

## Task 10: Melhorar Brapi Service

**Status:** ⬜ Not Started

**Descrição:** Adicionar timestamp e validação em preços.

**Arquivos:**
- `backend/app/services/brapi_service.py` (modificar)

**Checklist:**
- [ ] Adicionar timestamp em cada preço
- [ ] Validar que preço é de hoje
- [ ] Implementar fallback para Alpha Vantage
- [ ] Adicionar cache de 5 minutos
- [ ] Adicionar logging
- [ ] Testar com múltiplos tickers

**Acceptance Criteria:**
- Preços incluem timestamp
- Validação de freshness funciona
- Fallback funciona
- Cache funciona
- Logs mostram fonte de cada preço

---

## Task 11: Criar Testes Unitários

**Status:** ⬜ Not Started

**Descrição:** Criar testes para cada componente.

**Arquivos:**
- `backend/tests/test_gemini_client.py` (criar)
- `backend/tests/test_alpha_system_v3.py` (criar)
- `backend/tests/test_validators.py` (criar)

**Checklist:**
- [ ] Testar GeminiClient
- [ ] Testar AlphaSystemV3
- [ ] Testar validadores
- [ ] Testar scrapers
- [ ] Criar mock data
- [ ] Testar error handling
- [ ] Atingir 80%+ coverage

**Acceptance Criteria:**
- Todos os testes passam
- Coverage > 80%
- Mock data funciona
- Error handling é testado

---

## Task 12: Criar Testes de Integração

**Status:** ⬜ Not Started

**Descrição:** Testar fluxo completo end-to-end.

**Arquivos:**
- `backend/tests/test_integration.py` (criar)

**Checklist:**
- [ ] Testar fluxo completo (Prompt 1 → 6)
- [ ] Testar com dados reais (opcional)
- [ ] Testar com mock data
- [ ] Testar error scenarios
- [ ] Testar validações de freshness
- [ ] Verificar estrutura de saída

**Acceptance Criteria:**
- Fluxo completo funciona
- Validações funcionam
- Erros são tratados
- Saída está correta

---

## Task 13: Atualizar Frontend

**Status:** ⬜ Not Started

**Descrição:** Atualizar UI para mostrar novas informações.

**Arquivos:**
- `src/pages/AlphaTerminal.tsx` (modificar)
- `src/components/alpha/StockCard.tsx` (modificar)

**Checklist:**
- [ ] Adicionar exibição de timestamps
- [ ] Adicionar status anti-manada
- [ ] Adicionar data do CSV
- [ ] Adicionar data do Release
- [ ] Adicionar data do preço
- [ ] Melhorar layout
- [ ] Testar responsividade

**Acceptance Criteria:**
- Timestamps são exibidos
- Status anti-manada é visível
- Datas de todos os dados são mostradas
- Layout está limpo
- Responsivo funciona

---

## Task 14: Criar Documentação de Uso

**Status:** ⬜ Not Started

**Descrição:** Documentar como usar o sistema.

**Arquivos:**
- `blog-cozy-corner-81/COMO_USAR_SISTEMA.md` (criar)

**Checklist:**
- [ ] Documentar fluxo completo
- [ ] Explicar cada prompt
- [ ] Documentar validações
- [ ] Adicionar exemplos
- [ ] Adicionar troubleshooting
- [ ] Adicionar FAQ

**Acceptance Criteria:**
- Documentação está completa
- Exemplos funcionam
- Troubleshooting é útil
- FAQ responde dúvidas comuns

---

## Task 15: Testar Sistema Completo

**Status:** ⬜ Not Started

**Descrição:** Teste final do sistema completo.

**Checklist:**
- [ ] Rodar backend
- [ ] Rodar frontend
- [ ] Executar análise completa
- [ ] Verificar logs
- [ ] Verificar timestamps
- [ ] Verificar validações
- [ ] Verificar ranking final
- [ ] Verificar UI
- [ ] Testar com dados reais
- [ ] Documentar resultados

**Acceptance Criteria:**
- Sistema roda sem erros
- Análise completa funciona
- Validações funcionam
- Ranking está correto
- UI mostra todas as informações
- Logs estão completos

---

## Ordem de Execução Recomendada

1. Task 1: Gemini Client (base para tudo)
2. Task 5: Prompt Templates (necessário para Task 4)
3. Task 6: Data Models (estrutura de dados)
4. Task 8: Validação de Freshness (crítico)
5. Task 2: Investimentos Scraper V2
6. Task 3: Release Downloader V2
7. Task 10: Brapi Service (melhorias)
8. Task 4: Alpha System V3 (orquestração)
9. Task 7: Endpoint Principal
10. Task 9: Logging Completo
11. Task 11: Testes Unitários
12. Task 12: Testes de Integração
13. Task 13: Frontend
14. Task 14: Documentação
15. Task 15: Teste Final

---

## Estimativa de Tempo

- Tasks 1-6: 4-6 horas (core implementation)
- Tasks 7-10: 2-3 horas (integration)
- Tasks 11-12: 2-3 horas (testing)
- Tasks 13-15: 2-3 horas (frontend + docs)

**Total:** 10-15 horas de desenvolvimento

---

## Próximos Passos

1. Revisar este documento com o usuário
2. Confirmar prioridades
3. Começar implementação pela Task 1
4. Fazer commits incrementais
5. Testar cada componente antes de avançar
