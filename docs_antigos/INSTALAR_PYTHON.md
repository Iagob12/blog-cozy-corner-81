# 🐍 Como Instalar o Python no Windows

## Opção 1: Instalador Oficial (Recomendado)

### Passo 1: Download
1. Acesse: https://www.python.org/downloads/
2. Clique em "Download Python 3.11.x" (versão mais recente)
3. Aguarde o download

### Passo 2: Instalação
1. Execute o instalador baixado
2. **IMPORTANTE**: Marque a opção "Add Python to PATH" ✅
3. Clique em "Install Now"
4. Aguarde a instalação
5. Clique em "Close"

### Passo 3: Verificar
Abra um novo terminal (PowerShell ou CMD) e digite:
```bash
python --version
```

Deve mostrar: `Python 3.11.x`

## Opção 2: Microsoft Store (Mais Fácil)

1. Abra a Microsoft Store
2. Busque por "Python 3.11"
3. Clique em "Obter" ou "Instalar"
4. Aguarde a instalação
5. Abra um novo terminal e teste:
```bash
python --version
```

## Opção 3: Chocolatey (Para Desenvolvedores)

Se você tem Chocolatey instalado:
```bash
choco install python
```

## Após Instalar

### 1. Feche e abra um NOVO terminal

### 2. Verifique a instalação:
```bash
python --version
pip --version
```

### 3. Instale as dependências do projeto:
```bash
cd blog-cozy-corner-81\backend
pip install -r requirements.txt
```

### 4. Configure a API Key:
```bash
# Copie o arquivo de exemplo
copy .env.example .env

# Edite o .env e adicione sua chave do Gemini
notepad .env
```

### 5. Teste o sistema:
```bash
python test_alpha.py
```

### 6. Inicie o servidor:
```bash
python -m uvicorn app.main:app --reload
```

## Troubleshooting

### "Python não é reconhecido"
**Solução**: Você esqueceu de marcar "Add Python to PATH" durante a instalação.

**Correção**:
1. Desinstale o Python
2. Reinstale marcando a opção "Add Python to PATH"

OU

Adicione manualmente ao PATH:
1. Pressione Win + R
2. Digite: `sysdm.cpl`
3. Aba "Avançado" → "Variáveis de Ambiente"
4. Em "Variáveis do sistema", encontre "Path"
5. Clique em "Editar"
6. Adicione: `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python311`
7. Adicione: `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python311\Scripts`
8. Clique em "OK" em todas as janelas
9. Feche e abra um NOVO terminal

### "pip não é reconhecido"
```bash
python -m ensurepip --upgrade
```

### Erro ao instalar dependências
```bash
# Atualize o pip primeiro
python -m pip install --upgrade pip

# Tente novamente
pip install -r requirements.txt
```

## Alternativa: Usar o Backend do Projeto Alpha

Se você já tem o Python funcionando no projeto Alpha, pode usar aquele backend:

```bash
cd Alpha
python -m uvicorn app.main:app --reload --port 8000
```

E configurar o frontend do blog-cozy-corner-81 para apontar para ele.
