#!/bin/bash
# Script para configurar cron job no Linux/Mac

# Adiciona job para rodar às 18h todos os dias
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_PATH=$(which python3)

# Cron job: 0 18 * * * = às 18:00 todos os dias
CRON_JOB="0 18 * * * cd $SCRIPT_DIR/.. && $PYTHON_PATH scripts/daily_update.py >> logs/daily_update.log 2>&1"

# Adiciona ao crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job configurado!"
echo "📅 Execução diária às 18:00"
echo "📝 Logs em: logs/daily_update.log"
