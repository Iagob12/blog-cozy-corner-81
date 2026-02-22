@echo off
chcp 65001 >nul
echo ============================================================
echo 🚀 INICIANDO ALPHA SYSTEM
echo ============================================================
echo.

echo [1/3] Verificando instalação...
if not exist backend\venv (
    echo ❌ Backend não instalado! Execute INSTALAR.bat primeiro.
    pause
    exit /b 1
)
if not exist node_modules (
    echo ❌ Frontend não instalado! Execute INSTALAR.bat primeiro.
    pause
    exit /b 1
)
echo ✅ Sistema instalado

echo.
echo [2/3] Iniciando Backend (porta 8000)...
start "ALPHA BACKEND" cmd /k "cd backend && venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level warning"
timeout /t 5 /nobreak >nul
echo ✅ Backend iniciado

echo.
echo [3/3] Iniciando Frontend (porta 8080)...
start "ALPHA FRONTEND" cmd /k "npm run dev"
timeout /t 3 /nobreak >nul
echo ✅ Frontend iniciado

echo.
echo ============================================================
echo ✅ SISTEMA INICIADO COM SUCESSO!
echo ============================================================
echo.
echo URLs:
echo   Frontend:    http://localhost:8080
echo   Admin Panel: http://localhost:8080/admin
echo   Backend API: http://localhost:8000
echo   API Docs:    http://localhost:8000/docs
echo.
echo Credenciais Admin:
echo   Senha: 123
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause >nul

start http://localhost:8080/admin
