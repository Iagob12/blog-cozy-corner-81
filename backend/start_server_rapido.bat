@echo off
echo ========================================
echo   INICIANDO SERVIDOR RAPIDO
echo ========================================
echo.

python carregar_ranking_rapido.py
if errorlevel 1 (
    echo.
    echo ERRO ao carregar ranking!
    pause
    exit /b 1
)

echo.
echo Iniciando servidor na porta 8000...
echo.

python -m uvicorn app.main:app --reload --port 8000
