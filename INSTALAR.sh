#!/bin/bash

echo "============================================================"
echo "🚀 INSTALAÇÃO - ALPHA SYSTEM"
echo "============================================================"
echo ""

echo "[1/4] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado! Instale Python 3.10+ primeiro."
    exit 1
fi
echo "✅ Python encontrado"

echo ""
echo "[2/4] Instalando dependências do Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências do backend"
    exit 1
fi
echo "✅ Backend instalado"
cd ..

echo ""
echo "[3/4] Verificando Node.js..."
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado! Instale Node.js 18+ primeiro."
    exit 1
fi
echo "✅ Node.js encontrado"

echo ""
echo "[4/4] Instalando dependências do Frontend..."
npm install --silent
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências do frontend"
    exit 1
fi
echo "✅ Frontend instalado"

echo ""
echo "============================================================"
echo "✅ INSTALAÇÃO CONCLUÍDA!"
echo "============================================================"
echo ""
echo "Próximos passos:"
echo "1. Configure as API keys em backend/.env"
echo "2. Execute ./INICIAR.sh para iniciar o sistema"
echo ""
