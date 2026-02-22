# 🖥️ DEPLOY EM VPS (Servidor Próprio)

Deploy do Alpha System em servidor VPS (Ubuntu/Debian)

## 📋 PRÉ-REQUISITOS

- VPS com Ubuntu 20.04+ ou Debian 11+
- Acesso SSH root
- Domínio (opcional, mas recomendado)
- Mínimo: 2GB RAM, 2 CPU cores, 20GB disco

---

## 🔧 PASSO 1: PREPARAR O SERVIDOR

### 1.1 Conectar via SSH
```bash
ssh root@SEU_IP
```

### 1.2 Atualizar sistema
```bash
apt update && apt upgrade -y
```

### 1.3 Instalar dependências
```bash
# Python 3.11
apt install -y python3.11 python3.11-venv python3-pip

# Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# Nginx (proxy reverso)
apt install -y nginx

# Certbot (SSL gratuito)
apt install -y certbot python3-certbot-nginx

# Git
apt install -y git
```

---

## 📦 PASSO 2: CLONAR E CONFIGURAR

### 2.1 Criar usuário
```bash
adduser alpha
usermod -aG sudo alpha
su - alpha
```

### 2.2 Clonar repositório
```bash
cd /home/alpha
git clone https://github.com/SEU_USUARIO/alpha-system.git
cd alpha-system
```

### 2.3 Configurar Backend
```bash
cd backend

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
nano .env
# Preencher com suas API keys
```

### 2.4 Configurar Frontend
```bash
cd ..
npm install
npm run build
```

---

## 🚀 PASSO 3: CONFIGURAR SERVIÇOS

### 3.1 Criar serviço do Backend (systemd)
```bash
sudo nano /etc/systemd/system/alpha-backend.service
```

Conteúdo:
```ini
[Unit]
Description=Alpha System Backend
After=network.target

[Service]
Type=simple
User=alpha
WorkingDirectory=/home/alpha/alpha-system/backend
Environment="PATH=/home/alpha/alpha-system/backend/venv/bin"
ExecStart=/home/alpha/alpha-system/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --log-level warning
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3.2 Criar serviço do Frontend (systemd)
```bash
sudo nano /etc/systemd/system/alpha-frontend.service
```

Conteúdo:
```ini
[Unit]
Description=Alpha System Frontend
After=network.target

[Service]
Type=simple
User=alpha
WorkingDirectory=/home/alpha/alpha-system
ExecStart=/usr/bin/npm run preview -- --host 0.0.0.0 --port 8080
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3.3 Iniciar serviços
```bash
sudo systemctl daemon-reload
sudo systemctl enable alpha-backend
sudo systemctl enable alpha-frontend
sudo systemctl start alpha-backend
sudo systemctl start alpha-frontend

# Verificar status
sudo systemctl status alpha-backend
sudo systemctl status alpha-frontend
```

---

## 🌐 PASSO 4: CONFIGURAR NGINX

### 4.1 Criar configuração
```bash
sudo nano /etc/nginx/sites-available/alpha
```

Conteúdo:
```nginx
# Backend
server {
    listen 80;
    server_name api.seudominio.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Frontend
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4.2 Ativar configuração
```bash
sudo ln -s /etc/nginx/sites-available/alpha /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 PASSO 5: CONFIGURAR SSL (HTTPS)

### 5.1 Obter certificado
```bash
sudo certbot --nginx -d seudominio.com -d www.seudominio.com -d api.seudominio.com
```

### 5.2 Renovação automática
```bash
sudo certbot renew --dry-run
```

---

## 🔄 PASSO 6: ATUALIZAR O SISTEMA

### 6.1 Script de atualização
```bash
nano /home/alpha/update.sh
```

Conteúdo:
```bash
#!/bin/bash
cd /home/alpha/alpha-system

# Pull latest code
git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart alpha-backend

# Update frontend
cd ..
npm install
npm run build
sudo systemctl restart alpha-frontend

echo "✅ Sistema atualizado!"
```

### 6.2 Tornar executável
```bash
chmod +x /home/alpha/update.sh
```

### 6.3 Usar
```bash
/home/alpha/update.sh
```

---

## 📊 PASSO 7: MONITORAMENTO

### 7.1 Ver logs
```bash
# Backend
sudo journalctl -u alpha-backend -f

# Frontend
sudo journalctl -u alpha-frontend -f

# Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 7.2 Status dos serviços
```bash
sudo systemctl status alpha-backend
sudo systemctl status alpha-frontend
sudo systemctl status nginx
```

---

## 🔥 FIREWALL

### Configurar UFW
```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
sudo ufw status
```

---

## 💾 BACKUP

### Script de backup
```bash
nano /home/alpha/backup.sh
```

Conteúdo:
```bash
#!/bin/bash
BACKUP_DIR="/home/alpha/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do .env
cp /home/alpha/alpha-system/backend/.env $BACKUP_DIR/env_$DATE.bak

# Backup dos dados
tar -czf $BACKUP_DIR/data_$DATE.tar.gz /home/alpha/alpha-system/backend/data

# Manter apenas últimos 7 backups
ls -t $BACKUP_DIR/*.tar.gz | tail -n +8 | xargs rm -f

echo "✅ Backup concluído: $DATE"
```

### Agendar backup diário
```bash
crontab -e
```

Adicionar:
```cron
0 2 * * * /home/alpha/backup.sh
```

---

## 🐛 TROUBLESHOOTING

### Serviço não inicia
```bash
# Ver logs detalhados
sudo journalctl -u alpha-backend -n 100 --no-pager

# Verificar permissões
ls -la /home/alpha/alpha-system

# Testar manualmente
cd /home/alpha/alpha-system/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Nginx erro 502
```bash
# Verificar se backend está rodando
curl http://localhost:8000

# Ver logs do Nginx
sudo tail -f /var/log/nginx/error.log
```

### SSL não funciona
```bash
# Renovar certificado
sudo certbot renew --force-renewal

# Verificar configuração
sudo nginx -t
```

---

## 💰 CUSTOS

### VPS Recomendados
- **DigitalOcean**: $6/mês (2GB RAM)
- **Linode**: $5/mês (1GB RAM)
- **Vultr**: $6/mês (2GB RAM)
- **Hetzner**: €4/mês (2GB RAM)

### Domínio
- **Namecheap**: ~$10/ano
- **Cloudflare**: Gratuito (registro)

---

## ✅ CHECKLIST

- [ ] VPS criado e acessível
- [ ] Dependências instaladas
- [ ] Repositório clonado
- [ ] .env configurado
- [ ] Serviços systemd criados
- [ ] Nginx configurado
- [ ] SSL configurado
- [ ] Firewall configurado
- [ ] Backup agendado
- [ ] Sistema acessível via domínio
- [ ] Login funciona (senha: 123)

---

**Tempo estimado**: 1-2 horas  
**Dificuldade**: Médio ⭐⭐  
**Custo**: $5-10/mês  
**Status**: Produção ✅
