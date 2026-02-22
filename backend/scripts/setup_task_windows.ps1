# Script para configurar Task Scheduler no Windows

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = (Get-Command python).Source
$taskName = "AlphaTerminalDailyUpdate"

# Cria ação
$action = New-ScheduledTaskAction -Execute $pythonPath `
    -Argument "$scriptPath\daily_update.py" `
    -WorkingDirectory "$scriptPath\.."

# Cria trigger (18:00 todos os dias)
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00PM

# Cria task
Register-ScheduledTask -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Description "Atualização diária do Alpha Terminal"

Write-Host "✅ Task agendada criada!"
Write-Host "📅 Execução diária às 18:00"
Write-Host "🔧 Gerenciar: taskschd.msc"
