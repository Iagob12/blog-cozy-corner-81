@echo off
chcp 65001 >nul
echo ============================================================
echo 🔍 VERIFICAÇÃO DO SISTEMA - ALPHA
echo ============================================================
echo.

set ERRORS=0

echo [1/8] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado
    set /a ERRORS+=1
) else (
    for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python %PYTHON_VERSION%
)

echo.
echo [2/8] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado
    set /a ERRORS+=1
) else (
    for /f %%i in ('node --version') do set NODE_VERSION=%%i
    echo ✅ Node.js %NODE_VERSION%
)

echo.
echo [3/8] Verificando ambiente virtual Python...
if exist backend\venv (
    echo ✅ Ambiente virtual encontrado
) else (
    echo ❌ Ambiente virtual não encontrado
    set /a ERRORS+=1
)

echo.
echo [4/8] Verificando dependências Node...
if exist node_modules (
    echo ✅ node_modules encontrado
) else (
    echo ❌ node_modules não encontrado
    set /a ERRORS+=1
)

echo.
echo [5/8] Verificando arquivo .env...
if exist backend\.env (
    echo ✅ .env encontrado
    findstr /C:"ADMIN_PASSWORD_HASH" backend\.env >nul
    if errorlevel 1 (
        echo ⚠️  ADMIN_PASSWORD_HASH não configurado
    ) else (
        echo ✅ Senha admin configurada
    )
) else (
    echo ❌ .env não encontrado
    set /a ERRORS+=1
)

echo.
echo [6/8] Verificando estrutura de pastas...
if exist backend\app (
    echo ✅ backend\app encontrado
) else (
    echo ❌ backend\app não encontrado
    set /a ERRORS+=1
)
if exist src (
    echo ✅ src encontrado
) else (
    echo ❌ src não encontrado
    set /a ERRORS+=1
)

echo.
echo [7/8] Verificando arquivos de inicialização...
if exist INSTALAR.bat (
    echo ✅ INSTALAR.bat encontrado
) else (
    echo ❌ INSTALAR.bat não encontrado
    set /a ERRORS+=1
)
if exist INICIAR.bat (
    echo ✅ INICIAR.bat encontrado
) else (
    echo ❌ INICIAR.bat não encontrado
    set /a ERRORS+=1
)

echo.
echo [8/8] Verificando documentação...
if exist README.md (
    echo ✅ README.md encontrado
) else (
    echo ⚠️  README.md não encontrado
)
if exist DEPLOY.md (
    echo ✅ DEPLOY.md encontrado
) else (
    echo ⚠️  DEPLOY.md não encontrado
)

echo.
echo ============================================================
if %ERRORS%==0 (
    echo ✅ SISTEMA OK - PRONTO PARA DEPLOY
    echo ============================================================
    echo.
    echo Próximos passos:
    echo 1. Execute INICIAR.bat para iniciar o sistema
    echo 2. Acesse http://localhost:8080/admin
    echo 3. Login com senha: 123
) else (
    echo ❌ ENCONTRADOS %ERRORS% ERRO(S)
    echo ============================================================
    echo.
    echo Corrija os erros acima antes de continuar.
    echo Execute INSTALAR.bat se necessário.
)
echo.
pause
