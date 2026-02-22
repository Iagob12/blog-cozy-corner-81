#!/bin/bash

echo "============================================================"
echo "🚀 INICIANDO ALPHA SYSTEM"
echo "============================================================"
echo ""

echo "[1/3] Verificando instalação..."
if [ ! -d "backend/venv" ]; then
    echo "❌ Backend não instalado! Execute ./INSTALAR.sh primeiro."
    exit 1
fi
if [ ! -d "node_modules" ]; then
    echo "❌ Frontend não instalado! Execute ./INSTALAR.sh primeiro."
    exit 1
fi
echo "✅ Sistema instalado"

echo ""
echo "[2/3] Iniciando Backend (porta 8000)..."
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level warning &
BACKEND_PID=$!
cd ..
sleep 5
echo "✅ Backend iniciado (PID: $BACKEND_PID)"

echo ""
echo "[3/3] Iniciando Frontend (porta 8080)..."
npm run dev &
FRONTEND_PID=$!
sleep 3
echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"

echo ""
echo "============================================================"
echo "✅ SISTEMA INICIADO COM SUCESSO!"
echo "============================================================"
echo ""
echo "URLs:"
echo "  Frontend:    http://localhost:8080"
echo "  Admin Panel: http://localhost:8080/admin"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo ""
echo "Credenciais Admin:"
echo "  Senha: 123"
echo ""
echo "PIDs dos processos:"
echo "  Backend:  $BACKEND_PID"
echo "  Frontend: $FRONTEND_PID"
echo ""
echo "Para parar o sistema:"
echo "  kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo "Pressione Ctrl+C para parar o sistema..."

# Aguarda Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo ''; echo 'Sistema parado.'; exit" INT
wait
