# Alpha Terminal - Backend

## Instalação

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

## Configuração

Edite o arquivo `.env` e adicione sua chave da API Gemini:

```
GEMINI_API_KEY=sua_chave_aqui
```

## Executar

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints

- GET `/api/v1/top-picks` - Top picks do dia
- GET `/api/v1/alerts` - Alertas de preço
- GET `/api/v1/macro-context` - Contexto macroeconômico
- GET `/api/v1/sentiment/{ticker}` - Análise de sentimento
- POST `/api/v1/analyze-pdf` - Análise de PDF de RI

## Estrutura

- `app/layers/` - Camadas de processamento (Quant, Macro, Surgical)
- `app/services/` - Serviços (Alertas, Sentiment)
- `data/` - Dados CSV
