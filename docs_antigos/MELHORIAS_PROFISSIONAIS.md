# 🎯 MELHORIAS PROFISSIONAIS - SISTEMA ALPHA TERMINAL

## 📋 ANÁLISE DO SISTEMA ATUAL

### Pontos Fortes ✅
1. Arquitetura bem estruturada (6 prompts especializados)
2. Sistema de cache inteligente
3. Múltiplas chaves Gemini para distribuir carga
4. Fallback para pesquisa web quando Release não encontrado
5. Frontend com UX profissional

### Pontos Críticos ❌
1. **Dependência total de APIs gratuitas com quota limitada**
2. **Falta de validação rigorosa de dados**
3. **Análise superficial em caso de erro**
4. **Sem redundância de fontes de dados**
5. **Timeout frequente com volume de dados**

---

## 🔧 MELHORIAS OBRIGATÓRIAS PARA PRODUÇÃO

### 1. SISTEMA DE DADOS ROBUSTO

#### A. Múltiplas Fontes de Preços (Redundância)
```python
# Prioridade de fontes:
1. Brapi.dev (gratuito, brasileiro)
2. Yahoo Finance (gratuito, global)
3. Alpha Vantage (pago, confiável)
4. B3 oficial (scraping como último recurso)

# Implementação:
async def get_price_with_fallback(ticker: str) -> float:
    """Tenta múltiplas fontes até conseguir preço válido"""
    sources = [
        brapi_service.get_quote,
        yahoo_finance.get_quote,
        alpha_vantage.get_quote,
        b3_scraper.get_quote
    ]
    
    for source in sources:
        try:
            price = await source(ticker)
            if price and price > 0:
                return price
        except Exception as e:
            logger.warning(f"Fonte {source.__name__} falhou: {e}")
            continue
    
    raise ValueError(f"Nenhuma fonte retornou preço para {ticker}")
```

#### B. Validação Rigorosa de Dados
```python
class DataValidator:
    """Valida qualidade dos dados antes de enviar para IA"""
    
    @staticmethod
    def validate_csv(df: pd.DataFrame) -> bool:
        """
        Valida CSV:
        - Mínimo 100 ações
        - Colunas obrigatórias presentes
        - Valores numéricos válidos
        - Sem dados zerados em massa
        """
        if len(df) < 100:
            raise ValueError("CSV com poucas ações")
        
        required_cols = ['ticker', 'roe', 'cagr', 'pl', 'setor']
        if not all(col in df.columns for col in required_cols):
            raise ValueError("Colunas obrigatórias faltando")
        
        # Valida que pelo menos 80% tem dados válidos
        valid_rows = df[
            (df['roe'] > 0) & 
            (df['cagr'] != 0) & 
            (df['pl'] > 0)
        ]
        
        if len(valid_rows) / len(df) < 0.8:
            raise ValueError("Muitos dados inválidos no CSV")
        
        return True
    
    @staticmethod
    def validate_price(ticker: str, price: float, df: pd.DataFrame) -> bool:
        """
        Valida se preço faz sentido:
        - Não pode ser zero
        - Não pode variar mais de 50% do P/L esperado
        - Não pode ser absurdamente diferente do histórico
        """
        if price <= 0:
            return False
        
        # Busca P/L no CSV
        stock_data = df[df['ticker'] == ticker]
        if stock_data.empty:
            return True  # Não tem como validar
        
        pl = stock_data.iloc[0]['pl']
        lucro_por_acao = stock_data.iloc[0].get('lpa', 0)
        
        if pl > 0 and lucro_por_acao > 0:
            expected_price = pl * lucro_por_acao
            # Aceita variação de até 50%
            if abs(price - expected_price) / expected_price > 0.5:
                logger.warning(
                    f"{ticker}: Preço {price} muito diferente do esperado {expected_price}"
                )
                return False
        
        return True
```

#### C. Sistema de Releases Mais Robusto
```python
class ReleaseDownloaderV2:
    """Versão melhorada com múltiplas estratégias"""
    
    async def buscar_release_com_fallback(self, ticker: str) -> Optional[Dict]:
        """
        Estratégias em ordem:
        1. Site oficial de RI (PDF)
        2. CVM - Comissão de Valores Mobiliários (oficial)
        3. B3 - Bolsa oficial
        4. Status Invest (agregador)
        5. Web scraping de notícias financeiras
        """
        
        strategies = [
            self._download_from_ri_site,
            self._download_from_cvm,
            self._download_from_b3,
            self._download_from_status_invest,
            self._web_research_fallback
        ]
        
        for strategy in strategies:
            try:
                release = await strategy(ticker)
                if release and self._validate_release(release):
                    return release
            except Exception as e:
                logger.warning(f"Estratégia {strategy.__name__} falhou: {e}")
                continue
        
        return None
    
    def _validate_release(self, release: Dict) -> bool:
        """
        Valida qualidade do Release:
        - Tem data recente (últimos 6 meses)
        - Tem conteúdo mínimo (500 chars)
        - Contém palavras-chave financeiras
        """
        if not release.get('resumo') or len(release['resumo']) < 500:
            return False
        
        # Verifica palavras-chave financeiras
        keywords = ['receita', 'lucro', 'ebitda', 'margem', 'resultado']
        content_lower = release['resumo'].lower()
        
        if not any(kw in content_lower for kw in keywords):
            return False
        
        # Verifica data
        data_relatorio = release.get('data_relatorio')
        if data_relatorio:
            idade_dias = (datetime.now() - data_relatorio).days
            if idade_dias > 180:  # Mais de 6 meses
                logger.warning(f"Release muito antigo: {idade_dias} dias")
                return False
        
        return True
```

---

### 2. SISTEMA DE IA MAIS INTELIGENTE

#### A. Redução de Dados para IA (Evitar Timeout)
```python
class DataOptimizer:
    """Otimiza dados antes de enviar para IA"""
    
    @staticmethod
    def prepare_for_ai(df: pd.DataFrame, max_stocks: int = 50) -> str:
        """
        Prepara dados de forma otimizada:
        1. Pré-filtra por fundamentos (ROE>15%, CAGR>12%, P/L<15)
        2. Agrupa por setor
        3. Seleciona melhores de cada setor
        4. Formata de forma compacta
        """
        
        # Pré-filtro rigoroso
        filtered = df[
            (df['roe'] > 15) &
            (df['cagr'] > 12) &
            (df['pl'] < 15) &
            (df['pl'] > 0)
        ].copy()
        
        # Agrupa por setor e pega top 5 de cada
        top_by_sector = []
        for setor in filtered['setor'].unique():
            setor_stocks = filtered[filtered['setor'] == setor]
            # Ordena por score composto
            setor_stocks['score'] = (
                setor_stocks['roe'] * 0.4 +
                setor_stocks['cagr'] * 0.3 +
                (15 / setor_stocks['pl']) * 0.3
            )
            top_5 = setor_stocks.nlargest(5, 'score')
            top_by_sector.append(top_5)
        
        result = pd.concat(top_by_sector).nlargest(max_stocks, 'score')
        
        # Formata de forma compacta (JSON)
        compact_data = []
        for _, row in result.iterrows():
            compact_data.append({
                't': row['ticker'],
                'r': round(row['roe'], 1),
                'c': round(row['cagr'], 1),
                'p': round(row['pl'], 1),
                's': row['setor'][:20]  # Setor abreviado
            })
        
        return json.dumps(compact_data, ensure_ascii=False)
```

#### B. Validação de Respostas da IA
```python
class AIResponseValidator:
    """Valida se resposta da IA faz sentido"""
    
    @staticmethod
    def validate_ranking(ranking: List[Dict], precos: Dict) -> bool:
        """
        Valida ranking retornado pela IA:
        - Tem pelo menos 10 ações
        - Preços teto são realistas (não mais que 2x preço atual)
        - Upside é razoável (5-50%)
        - Recomendações fazem sentido
        """
        
        if len(ranking) < 10:
            logger.error("Ranking com poucas ações")
            return False
        
        for item in ranking:
            ticker = item.get('ticker')
            preco_atual = precos.get(ticker, 0)
            preco_teto = item.get('preco_teto', 0)
            
            if preco_atual <= 0 or preco_teto <= 0:
                logger.error(f"{ticker}: Preços inválidos")
                return False
            
            # Preço teto não pode ser mais que 2x o atual
            if preco_teto > preco_atual * 2:
                logger.warning(
                    f"{ticker}: Preço teto muito alto "
                    f"({preco_teto} vs {preco_atual})"
                )
                return False
            
            # Upside deve estar entre 5% e 50%
            upside = ((preco_teto / preco_atual) - 1) * 100
            if upside < 5 or upside > 50:
                logger.warning(f"{ticker}: Upside fora do esperado ({upside}%)")
                return False
        
        return True
    
    @staticmethod
    def validate_analysis(analysis: Dict) -> bool:
        """
        Valida análise individual:
        - Tem todos os campos obrigatórios
        - Catalisadores são específicos (não genéricos)
        - Riscos são concretos
        """
        
        required_fields = [
            'ticker', 'recomendacao', 'preco_teto',
            'catalisadores', 'riscos', 'confianca'
        ]
        
        if not all(field in analysis for field in required_fields):
            return False
        
        # Valida catalisadores (não podem ser genéricos)
        generic_phrases = [
            'fundamentos sólidos',
            'boa empresa',
            'setor promissor'
        ]
        
        catalisadores = ' '.join(analysis['catalisadores']).lower()
        if any(phrase in catalisadores for phrase in generic_phrases):
            logger.warning("Catalisadores muito genéricos")
            return False
        
        return True
```

#### C. Sistema de Retry Inteligente
```python
class SmartRetry:
    """Retry inteligente para chamadas de IA"""
    
    @staticmethod
    async def execute_with_retry(
        func: Callable,
        max_retries: int = 3,
        backoff_factor: float = 2.0,
        reduce_data_on_retry: bool = True
    ):
        """
        Retry inteligente:
        - Se timeout: reduz quantidade de dados
        - Se quota: espera e tenta chave backup
        - Se erro de parsing: reformula prompt
        """
        
        last_error = None
        data_size = 1.0  # 100% dos dados
        
        for attempt in range(max_retries):
            try:
                # Reduz dados progressivamente se timeout
                if reduce_data_on_retry and attempt > 0:
                    data_size *= 0.7  # Reduz 30% a cada retry
                    logger.info(f"Tentativa {attempt + 1}: usando {data_size*100}% dos dados")
                
                result = await func(data_size=data_size)
                return result
                
            except TimeoutError as e:
                last_error = e
                logger.warning(f"Timeout na tentativa {attempt + 1}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_factor ** attempt)
                    
            except QuotaExceededError as e:
                last_error = e
                logger.warning(f"Quota excedida na tentativa {attempt + 1}")
                # Tenta chave backup
                if attempt < max_retries - 1:
                    await asyncio.sleep(60)  # Espera 1 minuto
                    
            except Exception as e:
                last_error = e
                logger.error(f"Erro na tentativa {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(backoff_factor ** attempt)
        
        raise last_error
```

---

### 3. SISTEMA DE MONITORAMENTO E ALERTAS

#### A. Health Check Completo
```python
class SystemHealthCheck:
    """Monitora saúde do sistema"""
    
    async def check_all(self) -> Dict:
        """
        Verifica:
        - APIs de dados funcionando
        - Chaves Gemini com quota
        - Cache válido
        - Dados atualizados
        """
        
        health = {
            'timestamp': datetime.now().isoformat(),
            'status': 'healthy',
            'checks': {}
        }
        
        # 1. Verifica APIs de preços
        health['checks']['prices'] = await self._check_price_apis()
        
        # 2. Verifica chaves Gemini
        health['checks']['gemini'] = await self._check_gemini_keys()
        
        # 3. Verifica cache
        health['checks']['cache'] = self._check_cache()
        
        # 4. Verifica dados
        health['checks']['data'] = await self._check_data_freshness()
        
        # Status geral
        if any(check['status'] == 'critical' for check in health['checks'].values()):
            health['status'] = 'critical'
        elif any(check['status'] == 'warning' for check in health['checks'].values()):
            health['status'] = 'degraded'
        
        return health
    
    async def _check_price_apis(self) -> Dict:
        """Testa todas as APIs de preços"""
        results = {
            'status': 'healthy',
            'sources': {}
        }
        
        test_ticker = 'PETR4'
        
        # Testa cada fonte
        sources = {
            'brapi': brapi_service.get_quote,
            'yahoo': yahoo_finance.get_quote,
            'alpha_vantage': alpha_vantage.get_quote
        }
        
        working_sources = 0
        for name, func in sources.items():
            try:
                price = await func(test_ticker)
                if price and price > 0:
                    results['sources'][name] = 'ok'
                    working_sources += 1
                else:
                    results['sources'][name] = 'invalid_data'
            except Exception as e:
                results['sources'][name] = f'error: {str(e)[:50]}'
        
        # Precisa de pelo menos 1 fonte funcionando
        if working_sources == 0:
            results['status'] = 'critical'
        elif working_sources == 1:
            results['status'] = 'warning'
        
        return results
    
    async def _check_gemini_keys(self) -> Dict:
        """Verifica quota das chaves Gemini"""
        results = {
            'status': 'healthy',
            'keys': {}
        }
        
        working_keys = 0
        for i, key in enumerate(multi_gemini_client.keys, 1):
            try:
                # Tenta chamada simples
                response = await multi_gemini_client.executar_prompt_raw(
                    "Responda apenas: OK",
                    task_type="backup"
                )
                if "OK" in response.upper():
                    results['keys'][f'key_{i}'] = 'ok'
                    working_keys += 1
                else:
                    results['keys'][f'key_{i}'] = 'invalid_response'
            except QuotaExceededError:
                results['keys'][f'key_{i}'] = 'quota_exceeded'
            except Exception as e:
                results['keys'][f'key_{i}'] = f'error: {str(e)[:30]}'
        
        # Precisa de pelo menos 3 chaves funcionando
        if working_keys < 2:
            results['status'] = 'critical'
        elif working_keys < 4:
            results['status'] = 'warning'
        
        return results
```

#### B. Sistema de Alertas para Admin
```python
class AdminAlertSystem:
    """Envia alertas para administrador"""
    
    async def send_alert(self, level: str, message: str):
        """
        Envia alerta via:
        - Email
        - Telegram
        - Webhook
        """
        
        alert = {
            'timestamp': datetime.now().isoformat(),
            'level': level,  # 'info', 'warning', 'critical'
            'message': message,
            'system': 'Alpha Terminal'
        }
        
        if level == 'critical':
            # Envia por todos os canais
            await self._send_email(alert)
            await self._send_telegram(alert)
            await self._send_webhook(alert)
        elif level == 'warning':
            # Apenas Telegram e Webhook
            await self._send_telegram(alert)
            await self._send_webhook(alert)
        else:
            # Apenas log
            logger.info(f"Alert: {message}")
```

---

### 4. MELHORIAS NO FLUXO DE ANÁLISE

#### A. Análise em Etapas com Validação
```python
class ImprovedAnalysisFlow:
    """Fluxo de análise melhorado"""
    
    async def executar_analise_completa(self) -> RankingFinal:
        """
        Fluxo otimizado:
        1. Validação de dados
        2. Pré-filtro rigoroso
        3. Análise em lotes pequenos
        4. Validação de resultados
        5. Fallback inteligente
        """
        
        try:
            # ETAPA 1: Validação de Dados
            csv_path, csv_timestamp = await self._get_validated_csv()
            precos = await self._get_validated_prices()
            
            # ETAPA 2: Pré-filtro (reduz de 200 para 50 ações)
            df = pd.read_csv(csv_path)
            df_filtered = self._pre_filter_stocks(df)
            
            # ETAPA 3: Análise IA em lotes pequenos (10 ações por vez)
            analises = []
            for i in range(0, len(df_filtered), 10):
                batch = df_filtered.iloc[i:i+10]
                batch_analises = await self._analyze_batch(batch, precos)
                analises.extend(batch_analises)
            
            # ETAPA 4: Validação de Resultados
            analises_validas = [
                a for a in analises 
                if AIResponseValidator.validate_analysis(a)
            ]
            
            # ETAPA 5: Ranking Final
            ranking = self._generate_final_ranking(analises_validas)
            
            return ranking
            
        except Exception as e:
            logger.error(f"Erro na análise: {e}")
            # Fallback: usa análise simplificada
            return await self._fallback_analysis()
    
    def _pre_filter_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pré-filtro rigoroso:
        - ROE > 15%
        - CAGR > 12%
        - P/L < 15 e > 0
        - Dívida/EBITDA < 2.5
        - Liquidez mínima
        """
        
        filtered = df[
            (df['roe'] > 15) &
            (df['cagr'] > 12) &
            (df['pl'] < 15) &
            (df['pl'] > 0) &
            (df.get('divida_ebitda', 999) < 2.5) &
            (df.get('volume_medio', 0) > 1000000)  # Liquidez mínima
        ].copy()
        
        # Calcula score composto
        filtered['score'] = (
            filtered['roe'] * 0.4 +
            filtered['cagr'] * 0.3 +
            (15 / filtered['pl']) * 0.3
        )
        
        # Retorna top 50
        return filtered.nlargest(50, 'score')
```

---

## 📊 MÉTRICAS DE QUALIDADE

### Indicadores de Saúde do Sistema
```python
class QualityMetrics:
    """Métricas de qualidade para monitorar"""
    
    def calculate_metrics(self, ranking: RankingFinal) -> Dict:
        """
        Calcula métricas:
        - Taxa de sucesso de dados
        - Qualidade das análises
        - Diversificação do portfólio
        - Confiabilidade das recomendações
        """
        
        metrics = {}
        
        # 1. Taxa de Sucesso de Dados
        metrics['data_success_rate'] = {
            'csv': 1.0 if ranking.csv_fresh else 0.0,
            'prices': len([a for a in ranking.ranking if a.preco_atual > 0]) / len(ranking.ranking),
            'releases': len([a for a in ranking.ranking if a.analise_release]) / len(ranking.ranking)
        }
        
        # 2. Qualidade das Análises
        metrics['analysis_quality'] = {
            'avg_confidence': sum(
                1.0 if a.confianca == 'ALTA' else 0.5 if a.confianca == 'MÉDIA' else 0.0
                for a in ranking.ranking
            ) / len(ranking.ranking),
            'specific_catalysts': sum(
                1 for a in ranking.ranking 
                if len(a.catalisadores) >= 3
            ) / len(ranking.ranking)
        }
        
        # 3. Diversificação
        setores = [a.setor for a in ranking.ranking]
        metrics['diversification'] = {
            'unique_sectors': len(set(setores)),
            'max_concentration': max(setores.count(s) for s in set(setores)) / len(setores)
        }
        
        # 4. Confiabilidade
        metrics['reliability'] = {
            'avg_upside': sum(a.upside_percent for a in ranking.ranking) / len(ranking.ranking),
            'realistic_targets': sum(
                1 for a in ranking.ranking 
                if 5 <= a.upside_percent <= 50
            ) / len(ranking.ranking)
        }
        
        return metrics
```

---

## 🎯 IMPLEMENTAÇÃO PRIORITÁRIA

### Fase 1 (Crítico - 1 semana)
1. ✅ Múltiplas fontes de preços com fallback
2. ✅ Validação rigorosa de dados
3. ✅ Redução de dados para IA (evitar timeout)
4. ✅ Sistema de health check

### Fase 2 (Importante - 2 semanas)
1. ✅ Releases de múltiplas fontes (CVM, B3, Status Invest)
2. ✅ Validação de respostas da IA
3. ✅ Sistema de retry inteligente
4. ✅ Métricas de qualidade

### Fase 3 (Desejável - 1 mês)
1. ✅ Sistema de alertas para admin
2. ✅ Dashboard de monitoramento
3. ✅ Histórico de recomendações
4. ✅ Backtesting de performance

---

## 💰 CUSTOS ESTIMADOS (Produção)

### APIs Pagas (Recomendado)
- **Alpha Vantage Premium**: $50/mês (500 req/dia)
- **Gemini API Pro**: $100/mês (quota maior)
- **Servidor VPS**: $20/mês (DigitalOcean/AWS)
- **Total**: ~$170/mês

### Alternativa Gratuita (Limitada)
- Brapi.dev + Yahoo Finance (gratuito)
- 6 chaves Gemini gratuitas (120 req/dia)
- Servidor local
- **Total**: $0/mês (mas com limitações)

---

## 🚀 PRÓXIMOS PASSOS

1. **Implementar validação de dados** (crítico)
2. **Adicionar múltiplas fontes de preços** (crítico)
3. **Otimizar chamadas para IA** (crítico)
4. **Implementar health check** (importante)
5. **Testar com dados reais por 1 semana** (validação)
6. **Ajustar baseado em resultados** (iteração)

---

**Este documento deve ser revisado e aprovado antes de implementação em produção.**
