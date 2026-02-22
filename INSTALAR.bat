@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 INSTALAÇÃO - ALPHA SYSTEM
echo ============================================================
echo.

echo [1/4] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.10+ primeiro.
    pause
    exit /b 1
)
echo ✅ Python encontrado

echo.
echo [2/4] Instalando dependências do Backend...
cd backend
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências do backend
    pause
    exit /b 1
)
echo ✅ Backend instalado
cd ..

echo.
echo [3/4] Verificando Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js não encontrado! Instale Node.js 18+ primeiro.
    pause
    exit /b 1
)
echo ✅ Node.js encontrado

echo.
echo [4/4] Instalando dependências do Frontend...
call npm install --silent
if errorlevel 1 (
    echo ❌ Erro ao instalar dependências do frontend
    pause
    exit /b 1
)
echo ✅ Frontend instalado

echo.
echo ============================================================
echo ✅ INSTALAÇÃO CONCLUÍDA!
echo ============================================================
echo.
echo Próximos passos:
echo 1. Configure as API keys em backend\.env
echo 2. Execute INICIAR.bat para iniciar o sistema
echo.
pause
