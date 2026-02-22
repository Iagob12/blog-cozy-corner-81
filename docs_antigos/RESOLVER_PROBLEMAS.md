# 🔧 Resolver Problemas - Alpha Terminal

## Problema: Site não mostra dados

### Solução 1: Verificar se o Backend está rodando

```bash
# Abra um terminal e teste:
curl http://localhost:8000/

# Deve retornar:
# {"message":"Alpha Terminal API","version":"1.0.0","status":"operational"}
```

Se não funcionar:
```bash
cd Alpha
python -m uvicorn app.main:app --reload
```

### Solução 2: Testar a API

Abra o arquivo: **teste-api.html**

Clique nos botões para testar cada endpoint.

### Solução 3: Verificar CORS

O backend deve ter CORS configurado para aceitar requisições do frontend.

Verifique se no terminal do backend aparece:
```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/top-picks HTTP/1.1" 200 OK
```

### Solução 4: Limpar Cache do Navegador

1. Pressione `Ctrl + Shift + Delete`
2. Limpe cache e cookies
3. Recarregue a página (`Ctrl + F5`)

### Solução 5: Verificar Console do Navegador

1. Pressione `F12` no navegador
2. Vá na aba "Console"
3. Veja se há erros em vermelho
4. Copie o erro e analise

### Solução 6: Reiniciar Tudo

```bash
# Parar frontend (Ctrl + C no terminal)
# Parar backend (Ctrl + C no terminal)

# Reiniciar backend
cd Alpha
python -m uvicorn app.main:app --reload

# Reiniciar frontend (em outro terminal)
cd blog-cozy-corner-81
npm run dev
```

### Solução 7: Verificar Portas

Backend deve estar em: **http://localhost:8000**
Frontend deve estar em: **http://localhost:8081**

Se as portas estiverem diferentes, atualize o `.env`:
```
VITE_API_URL=http://localhost:PORTA_DO_BACKEND
```

## Problema: Erro de CORS

### Sintoma:
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:8081' 
has been blocked by CORS policy
```

### Solução:
O CORS já está configurado no backend. Reinicie o servidor backend.

## Problema: Dados não atualizam

### Solução:
1. Verifique se o backend está respondendo
2. Limpe o cache do navegador
3. Recarregue a página com `Ctrl + F5`

## Problema: Erro 404

### Solução:
Verifique se os endpoints estão corretos:
- `/api/v1/top-picks` ✅
- `/api/v1/market/quote/{ticker}` ✅
- `/api/v1/alpha/radar-oportunidades` ✅

## Teste Rápido

Execute este comando para testar tudo:

```bash
# Teste 1: Backend
curl http://localhost:8000/

# Teste 2: Top Picks
curl http://localhost:8000/api/v1/top-picks?limit=3

# Teste 3: Cotação
curl http://localhost:8000/api/v1/market/quote/PETR4
```

Se todos funcionarem, o problema está no frontend.

## Logs Úteis

### Backend:
Veja o terminal onde o backend está rodando.
Deve mostrar cada requisição:
```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/top-picks HTTP/1.1" 200 OK
```

### Frontend:
Pressione `F12` no navegador e veja a aba "Network".
Deve mostrar as requisições para a API.

## Ainda com Problemas?

1. Abra: **teste-api.html**
2. Teste cada endpoint
3. Veja qual está falhando
4. Verifique os logs do backend
5. Verifique o console do navegador (F12)

## Contato de Emergência

Se nada funcionar:
1. Feche tudo (Ctrl + C em todos os terminais)
2. Reinicie o computador
3. Execute novamente:
   ```bash
   cd Alpha
   python -m uvicorn app.main:app --reload
   ```
4. Em outro terminal:
   ```bash
   cd blog-cozy-corner-81
   npm run dev
   ```
5. Abra: http://localhost:8081
