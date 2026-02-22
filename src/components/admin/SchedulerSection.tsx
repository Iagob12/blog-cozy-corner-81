import { useState, useEffect } from 'react';
import { Clock, Play, Square, Activity, CheckCircle, XCircle } from 'lucide-react';

interface SchedulerStatus {
  ativo: boolean;
  intervalo_minutos: number;
  ultima_execucao: string | null;
  proxima_execucao: string | null;
}

interface Log {
  tipo: string;
  timestamp: string;
  empresas_analisadas?: number;
  empresas_falhadas?: number;
  tempo_segundos?: number;
  erro?: string;
}

interface Props {
  token: string;
}

export function SchedulerSection({ token }: Props) {
  const [status, setStatus] = useState<SchedulerStatus | null>(null);
  const [logs, setLogs] = useState<Log[]>([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadStatus();
    
    // Atualiza status a cada 10s
    const interval = setInterval(loadStatus, 10000);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/scheduler/status', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setStatus(data.status);
        setLogs(data.ultimos_logs || []);
      }
    } catch (error) {
      console.error('Erro ao carregar status:', error);
    }
  };

  const handleIniciar = async () => {
    setLoading(true);
    setMessage(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/scheduler/iniciar', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error('Erro ao iniciar scheduler');
      }

      setMessage({ type: 'success', text: 'Scheduler iniciado! Análises automáticas a cada hora.' });
      await loadStatus();
    } catch (error) {
      setMessage({ type: 'error', text: error instanceof Error ? error.message : 'Erro desconhecido' });
    } finally {
      setLoading(false);
    }
  };

  const handleParar = async () => {
    setLoading(true);
    setMessage(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/scheduler/parar', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error('Erro ao parar scheduler');
      }

      setMessage({ type: 'success', text: 'Scheduler parado.' });
      await loadStatus();
    } catch (error) {
      setMessage({ type: 'error', text: error instanceof Error ? error.message : 'Erro desconhecido' });
    } finally {
      setLoading(false);
    }
  };

  const getLogIcon = (tipo: string) => {
    switch (tipo) {
      case 'scheduler_iniciado':
        return <Play size={14} className="text-alpha-green" />;
      case 'scheduler_parado':
        return <Square size={14} className="text-alpha-red" />;
      case 'analise_executada':
        return <CheckCircle size={14} className="text-alpha-green" />;
      case 'erro_analise':
      case 'erro_scheduler':
        return <XCircle size={14} className="text-alpha-red" />;
      default:
        return <Activity size={14} className="text-muted-foreground" />;
    }
  };

  const getLogText = (log: Log) => {
    switch (log.tipo) {
      case 'scheduler_iniciado':
        return 'Scheduler iniciado';
      case 'scheduler_parado':
        return 'Scheduler parado';
      case 'analise_executada':
        return `Análise concluída: ${log.empresas_analisadas || 0} empresas (${log.tempo_segundos?.toFixed(1)}s)`;
      case 'erro_analise':
        return `Erro na análise: ${log.erro?.substring(0, 50) || 'Erro desconhecido'}`;
      case 'erro_scheduler':
        return `Erro no scheduler: ${log.erro?.substring(0, 50) || 'Erro desconhecido'}`;
      default:
        return log.tipo;
    }
  };

  if (!status) {
    return (
      <div className="alpha-card">
        <div className="flex items-center gap-2 mb-4">
          <Clock className="w-5 h-5 text-primary" />
          <h3 className="font-display font-bold text-foreground">Scheduler Automático</h3>
        </div>
        <p className="text-muted-foreground text-sm">Carregando...</p>
      </div>
    );
  }

  return (
    <div className="alpha-card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Clock className="w-5 h-5 text-primary" />
          <h3 className="font-display font-bold text-foreground">Scheduler Automático</h3>
        </div>
        
        {/* Status Badge */}
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full border ${
          status.ativo 
            ? 'bg-alpha-green/10 border-alpha-green/20' 
            : 'bg-muted border-border'
        }`}>
          <div className={`w-2 h-2 rounded-full ${status.ativo ? 'bg-alpha-green animate-pulse' : 'bg-muted-foreground'}`} />
          <span className={`text-xs font-mono font-medium ${status.ativo ? 'text-alpha-green' : 'text-muted-foreground'}`}>
            {status.ativo ? 'ATIVO' : 'INATIVO'}
          </span>
        </div>
      </div>

      {message && (
        <div className={`mb-4 p-3 rounded-lg border text-sm ${
          message.type === 'success' 
            ? 'bg-alpha-green/10 border-alpha-green/20 text-alpha-green' 
            : 'bg-alpha-red/10 border-alpha-red/20 text-alpha-red'
        }`}>
          {message.text}
        </div>
      )}

      {/* Info */}
      <div className="space-y-3 mb-4">
        <div className="p-3 bg-muted/50 rounded-lg border border-border">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-xs text-muted-foreground">Intervalo</span>
              <p className="text-sm font-mono font-medium text-foreground">
                {status.intervalo_minutos} minutos
              </p>
            </div>
            <div>
              <span className="text-xs text-muted-foreground">Última Execução</span>
              <p className="text-sm font-mono font-medium text-foreground">
                {status.ultima_execucao 
                  ? new Date(status.ultima_execucao).toLocaleTimeString('pt-BR')
                  : 'Nunca'
                }
              </p>
            </div>
          </div>
        </div>

        {status.ativo && status.proxima_execucao && (
          <div className="p-3 bg-primary/10 border border-primary/20 rounded-lg">
            <div className="flex items-center gap-2">
              <Clock size={14} className="text-primary" />
              <span className="text-xs text-muted-foreground">Próxima execução:</span>
              <span className="text-sm font-mono font-medium text-primary">
                {new Date(status.proxima_execucao).toLocaleTimeString('pt-BR')}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Controles */}
      <div className="flex gap-3 mb-4">
        {!status.ativo ? (
          <button
            type="button"
            onClick={handleIniciar}
            disabled={loading}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg transition-all disabled:opacity-50"
          >
            <Play size={16} />
            Iniciar Scheduler
          </button>
        ) : (
          <button
            type="button"
            onClick={handleParar}
            disabled={loading}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-3 bg-alpha-red hover:bg-alpha-red/90 text-white rounded-lg transition-all disabled:opacity-50"
          >
            <Square size={16} />
            Parar Scheduler
          </button>
        )}
      </div>

      {/* Logs */}
      {logs.length > 0 && (
        <div>
          <h4 className="text-xs font-mono text-muted-foreground mb-2">ÚLTIMOS EVENTOS</h4>
          <div className="space-y-2 max-h-48 overflow-y-auto">
            {logs.map((log, index) => (
              <div 
                key={index}
                className="flex items-start gap-3 p-3 bg-muted/30 border border-border rounded-lg"
              >
                {getLogIcon(log.tipo)}
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-foreground">{getLogText(log)}</p>
                  <p className="text-xs text-muted-foreground font-mono mt-1">
                    {new Date(log.timestamp).toLocaleString('pt-BR')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Descrição */}
      <div className="mt-4 p-3 bg-muted/30 border border-border rounded-lg">
        <p className="text-xs text-muted-foreground">
          O scheduler executa análises incrementais automaticamente a cada hora. 
          Apenas empresas com releases novos ou dados atualizados são reanalisadas.
        </p>
      </div>
    </div>
  );
}
