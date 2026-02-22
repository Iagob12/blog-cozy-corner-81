# 🚀 Deploy em Produção - Alpha Terminal

## Opções de Deploy

### Opção 1: VPS (Recomendado)

#### Requisitos
- VPS com 2GB RAM mínimo
- Ubuntu 20.04+
- Python 3.9+
- Node.js 18+

#### Passo a Passo

```bash
# 1. Conecte ao VPS
ssh usuario@seu-servidor.com

# 2. Instale dependências
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# 3. Clone o repositório
git clone seu-repositorio.git
cd blog-cozy-corner-81

# 4. Configure Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
nano .env
# Adicione: GEMINI_API_KEY=sua_chave

# 5. Configure Frontend
cd ..
npm install
npm run build

# 6. Configure Nginx
sudo nano /etc/nginx/sites-available/alpha-terminal
```

**Configuração Nginx:**
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    # Frontend
    location / {
        root /caminho/para/blog-cozy-corner-81/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Ative o site
sudo ln -s /etc/nginx/sites-available/alpha-terminal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 7. Configure Systemd para Backend
sudo nano /etc/systemd/system/alpha-terminal.service
```

**Arquivo systemd:**
```ini
[Unit]
Description=Alpha Terminal API
After=network.target

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/caminho/para/blog-cozy-corner-81/backend
Environment="PATH=/caminho/para/blog-cozy-corner-81/backend/venv/bin"
ExecStart=/caminho/para/blog-cozy-corner-81/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Inicie o serviço
sudo systemctl daemon-reload
sudo systemctl enable alpha-terminal
sudo systemctl start alpha-terminal
sudo systemctl status alpha-terminal
```

---

### Opção 2: Docker

#### Dockerfile Backend

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Dockerfile Frontend

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    volumes:
      - ./backend/data:/app/data
    restart: always

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: always
```

```bash
# Deploy com Docker
docker-compose up -d
```

---

### Opção 3: Vercel + Railway

#### Frontend (Vercel)

```bash
# Instale Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

**vercel.json:**
```json
{
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://seu-backend.railway.app/api/:path*"
    }
  ]
}
```

#### Backend (Railway)

1. Acesse: https://railway.app
2. Conecte seu repositório
3. Configure variáveis de ambiente:
   - `GEMINI_API_KEY`
   - `FRONTEND_URL`
4. Deploy automático

---

### Opção 4: Heroku

#### Backend

```bash
# Crie Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Deploy
heroku create alpha-terminal-api
heroku config:set GEMINI_API_KEY=sua_chave
git subtree push --prefix backend heroku main
```

#### Frontend

```bash
# Deploy no Netlify
npm run build
netlify deploy --prod --dir=dist
```

---

## 🔒 Segurança em Produção

### 1. HTTPS (SSL)

```bash
# Certbot (Let's Encrypt)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

### 2. Firewall

```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 3. Variáveis de Ambiente

**NUNCA** commite `.env` no git!

```bash
# .gitignore
.env
*.env
```

### 4. Rate Limiting

Adicione no `main.py`:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/portfolio/executar-fluxo-completo")
@limiter.limit("5/hour")  # Máximo 5 execuções por hora
async def executar_fluxo_completo(request: Request):
    ...
```

---

## 📊 Monitoramento

### 1. Logs

```bash
# Backend logs
sudo journalctl -u alpha-terminal -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 2. Uptime Monitoring

Use serviços como:
- UptimeRobot (grátis)
- Pingdom
- StatusCake

### 3. Performance

```bash
# Instale htop
sudo apt install htop
htop

# Monitore uso de memória
free -h

# Monitore disco
df -h
```

---

## 🔄 Atualizações

### Deploy Automático (GitHub Actions)

**.github/workflows/deploy.yml:**

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to VPS
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.VPS_HOST }}
        username: ${{ secrets.VPS_USER }}
        key: ${{ secrets.VPS_SSH_KEY }}
        script: |
          cd /caminho/para/blog-cozy-corner-81
          git pull
          cd backend
          source venv/bin/activate
          pip install -r requirements.txt
          sudo systemctl restart alpha-terminal
          cd ..
          npm install
          npm run build
          sudo systemctl reload nginx
```

---

## 💾 Backup

### Script de Backup

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backup/alpha-terminal"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup dados
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /caminho/para/blog-cozy-corner-81/backend/data

# Backup .env
cp /caminho/para/blog-cozy-corner-81/backend/.env $BACKUP_DIR/env_$DATE

# Remove backups antigos (mantém últimos 7 dias)
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup concluído: $DATE"
```

```bash
# Agende com cron
crontab -e

# Adicione (backup diário às 3h)
0 3 * * * /caminho/para/backup.sh
```

---

## 🎯 Checklist de Deploy

- [ ] Servidor configurado (VPS/Docker/Cloud)
- [ ] Python 3.9+ instalado
- [ ] Node.js 18+ instalado
- [ ] Dependências instaladas
- [ ] `.env` configurado com GEMINI_API_KEY
- [ ] Nginx configurado
- [ ] SSL/HTTPS ativado
- [ ] Firewall configurado
- [ ] Systemd service criado
- [ ] Logs funcionando
- [ ] Backup configurado
- [ ] Monitoramento ativo
- [ ] Deploy automático (opcional)

---

## 📞 Suporte

### Logs de Erro

```bash
# Backend
tail -f backend/logs/error.log

# Sistema
sudo journalctl -xe
```

### Teste de Saúde

```bash
# API Health Check
curl http://seu-dominio.com/api/v1/

# Teste fluxo completo
curl -X POST http://seu-dominio.com/api/v1/portfolio/executar-fluxo-completo
```

---

## 💰 Custos Estimados

### VPS (Recomendado)
- **DigitalOcean**: $6/mês (1GB RAM)
- **Linode**: $5/mês (1GB RAM)
- **Vultr**: $6/mês (1GB RAM)

### Serverless (Alternativa)
- **Vercel**: Grátis (frontend)
- **Railway**: $5/mês (backend)
- **Total**: $5/mês

### APIs
- **Gemini**: Grátis (60 req/min)
- **brapi.dev**: Grátis
- **Total APIs**: R$ 0

---

**Sistema pronto para produção!** 🚀
