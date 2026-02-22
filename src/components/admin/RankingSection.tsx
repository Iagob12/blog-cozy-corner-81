import { useState, useEffect } from 'react';
import { TrendingUp, Award, Clock, RefreshCw, Activity, CheckCircle, AlertCircle } from 'lucide-react';

interface Analise {
  ticker: string;
  rank: number;
  score: number;
  recomendacao: string;
  preco_teto: number;
  upside: number;
  tem_release: boolean;
  timestamp_analise: string;
  resumo?: string;
}

interface Ranking {
  total: number;
  ranking: Analise[];
  timestamp: string;
  metadados: {
    com_release: number;
    sem_release: number;
    score_medio: number;
  };
}

interface Estatisticas {
  total_analises: number;
  com_release: number;
  sem_release: number;
  timestamp_criacao: string;
  timestamp_atualizacao: string;
  total_historico: number;
}

interface Props {
  token: string;
}

export function RankingSection({ token }: Props) {
  const [ranking, setRanking] = useState<Ranking | null>(null);
  const [estatisticas, setEstatisticas] = useState<Estatisticas | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadRanking();
    loadEstatisticas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadRanking = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/ranking-atual', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setRanking(data);
      }
    } catch (error) {
      console.error('Erro ao carregar ranking:', error);
    }
  };

  const loadEstatisticas = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/estatisticas-analise', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        setEstatisticas(data);
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    setMessage(null);
    
    try {
      await loadRanking();
      await loadEstatisticas();
      setMessage({ type: 'success', text: 'Dados atualizados!' });
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao atualizar dados' });
    } finally {
      setLoading(false);
    }
  };

  const getRecomendacaoColor = (recomendacao: string) => {
    switch (recomendacao) {
      case 'COMPRA FORTE':
        return 'text-alpha-green';
      case 'COMPRA':
        return 'text-alpha-green/70';
      case 'MANTER':
        return 'text-alpha-amber';
      case 'VENDA':
        return 'text-alpha-red';
      case 'AGUARDAR':
        return 'text-muted-foreground';
      default:
        return 'text-foreground';
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-alpha-green';
    if (score >= 6) return 'text-alpha-amber';
    return 'text-alpha-red';
  };

  if (!ranking) {
    return (
      <div className="alpha-card">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-primary" />
          <h3 className="font-display font-bold text-foreground">Ranking Atual</h3>
        </div>
        <div className="text-center py-8">
          <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-3" />
          <p className="text-muted-foreground text-sm">Nenhum ranking disponível</p>
          <p className="text-muted-foreground text-xs mt-1">Execute análise incremental primeiro</p>
        </div>
      </div>
    );
  }

  const { total, ranking: empresas, timestamp, metadados } = ranking;

  return (
    <div className="space-y-4">
      {/* Estatísticas */}
      {estatisticas && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-2">
              <Activity className="w-4 h-4 text-primary" />
              <span className="text-xs text-muted-foreground font-mono">TOTAL</span>
            </div>
            <p className="text-2xl font-bold text-foreground font-mono">{estatisticas.total_analises}</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-2">
              <CheckCircle className="w-4 h-4 text-alpha-green" />
              <span className="text-xs text-muted-foreground font-mono">COM RELEASE</span>
            </div>
            <p className="text-2xl font-bold text-alpha-green font-mono">{estatisticas.com_release}</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-4 h-4 text-alpha-amber" />
              <span className="text-xs text-muted-foreground font-mono">SEM RELEASE</span>
            </div>
            <p className="text-2xl font-bold text-alpha-amber font-mono">{estatisticas.sem_release}</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-2">
              <Award className="w-4 h-4 text-primary" />
              <span className="text-xs text-muted-foreground font-mono">SCORE MÉDIO</span>
            </div>
            <p className="text-2xl font-bold text-primary font-mono">{metadados.score_medio.toFixed(1)}</p>
          </div>
        </div>
      )}

      {/* Ranking */}
      <div className="alpha-card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            <h3 className="font-display font-bold text-foreground">Ranking Atual</h3>
            <span className="text-xs text-muted-foreground font-mono">
              ({total} empresas)
            </span>
          </div>
          <button
            type="button"
            onClick={handleRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-3 py-1.5 bg-muted hover:bg-muted/80 text-foreground text-sm rounded-lg transition-all disabled:opacity-50"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Atualizar
          </button>
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

        {/* Timestamp */}
        <div className="mb-4 p-3 bg-muted/50 rounded-lg border border-border">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Clock size={12} />
            <span>Última atualização: {new Date(timestamp).toLocaleString('pt-BR')}</span>
          </div>
        </div>

        {/* Lista de Empresas */}
        <div className="space-y-2 max-h-[600px] overflow-y-auto">
          {empresas.map((empresa) => (
            <div
              key={empresa.ticker}
              className="p-4 bg-muted/30 hover:bg-muted/50 border border-border rounded-lg transition-all"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-3">
                  {/* Rank */}
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-bold text-sm ${
                    empresa.rank <= 3 
                      ? 'bg-primary/20 text-primary border border-primary/30' 
                      : 'bg-muted text-muted-foreground'
                  }`}>
                    {empresa.rank}
                  </div>

                  {/* Ticker */}
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-foreground">{empresa.ticker}</span>
                      {empresa.tem_release && (
                        <CheckCircle size={14} className="text-alpha-green" title="Com release" />
                      )}
                    </div>
                    <span className={`text-xs font-medium ${getRecomendacaoColor(empresa.recomendacao)}`}>
                      {empresa.recomendacao}
                    </span>
                  </div>
                </div>

                {/* Score */}
                <div className="text-right">
                  <div className={`text-2xl font-bold font-mono ${getScoreColor(empresa.score)}`}>
                    {empresa.score.toFixed(1)}
                  </div>
                  <span className="text-xs text-muted-foreground">score</span>
                </div>
              </div>

              {/* Métricas */}
              <div className="grid grid-cols-2 gap-3 mt-3 pt-3 border-t border-border">
                <div>
                  <span className="text-xs text-muted-foreground">Preço Teto</span>
                  <p className="text-sm font-mono font-medium text-foreground">
                    R$ {empresa.preco_teto.toFixed(2)}
                  </p>
                </div>
                <div>
                  <span className="text-xs text-muted-foreground">Upside</span>
                  <p className={`text-sm font-mono font-medium ${
                    empresa.upside > 0 ? 'text-alpha-green' : 'text-alpha-red'
                  }`}>
                    {empresa.upside > 0 ? '+' : ''}{empresa.upside.toFixed(1)}%
                  </p>
                </div>
              </div>

              {/* Resumo */}
              {empresa.resumo && (
                <div className="mt-3 pt-3 border-t border-border">
                  <p className="text-xs text-muted-foreground line-clamp-2">{empresa.resumo}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
