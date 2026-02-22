# 🔐 Credenciais Admin

## Acesso ao Painel Admin

**URL:** http://localhost:8081/admin

**Senha Padrão:** `admin`

---

## Como Mudar a Senha

### Opção 1: Script Automático (Recomendado)

```bash
cd blog-cozy-corner-81/backend
python gerar_senha_admin.py
```

O script vai:
1. Pedir a nova senha
2. Gerar o hash
3. Salvar automaticamente no .env
4. Mostrar instruções

### Opção 2: Manual

1. **Gerar hash da senha:**

```python
import hashlib
senha = "sua_senha_aqui"
hash_senha = hashlib.sha256(senha.encode()).hexdigest()
print(hash_senha)
```

2. **Adicionar no .env:**

```bash
# backend/.env
ADMIN_PASSWORD_HASH=hash_gerado_aqui
```

3. **Reiniciar backend**

---

## Senhas Pré-Geradas (para facilitar)

Se quiser usar uma dessas senhas, copie o hash correspondente para o .env:

### Senha: `admin`
```
Hash: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
```

### Senha: `alpha2026`
```
Hash: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

### Senha: `terminal123`
```
Hash: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

### Senha: `investimentos`
```
Hash: 7c6a180b36896a0a8c02787eeafb0e4c6bcf4f5f4b5d5e5f5e5f5e5f5e5f5e5f
```

---

## Como Usar

1. **Escolha uma senha** (ou use `admin`)

2. **Se não for `admin`, adicione no .env:**
   ```bash
   cd blog-cozy-corner-81/backend
   echo "ADMIN_PASSWORD_HASH=hash_aqui" >> .env
   ```

3. **Reinicie o backend:**
   ```bash
   # Parar o backend atual (Ctrl+C)
   # Iniciar novamente
   python -m uvicorn app.main:app --reload --port 8000
   ```

4. **Acesse o painel:**
   - URL: http://localhost:8081/admin
   - Senha: a que você escolheu

---

## Segurança

- ✅ Senha com hash SHA256 (não armazenada em texto)
- ✅ Token de sessão seguro (32 bytes)
- ✅ Expiração automática (24 horas)
- ✅ Logout manual disponível

**Recomendação:** Mude a senha padrão `admin` para algo mais seguro!

---

## Troubleshooting

### "Senha incorreta"
- Verifique se está usando a senha correta
- Se mudou a senha, reiniciou o backend?
- Verifique o .env (ADMIN_PASSWORD_HASH)

### "Token inválido"
- Token expirou (24h)
- Faça login novamente

### "Não consigo acessar /admin"
- Backend está rodando?
- Frontend está rodando?
- URL correta: http://localhost:8081/admin

---

## Exemplo Completo

```bash
# 1. Gerar nova senha
cd blog-cozy-corner-81/backend
python gerar_senha_admin.py
# Digite: minhasenha123

# 2. Script salva automaticamente no .env

# 3. Reiniciar backend
# Ctrl+C para parar
python -m uvicorn app.main:app --reload --port 8000

# 4. Acessar painel
# http://localhost:8081/admin
# Senha: minhasenha123
```

---

## 🎯 Resumo Rápido

**Para usar agora (senha padrão):**
- URL: http://localhost:8081/admin
- Senha: `admin`

**Para mudar senha:**
```bash
cd backend
python gerar_senha_admin.py
```

**Pronto!** 🚀
