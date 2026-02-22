import { useState, useEffect, useRef } from 'react';
import { 
  Upload, FileText, Clock, CheckCircle, LogOut, 
  Database, Activity, TrendingUp, RefreshCw, AlertCircle, 
  Home, Settings, Shield, Power, Terminal,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { ReleasesSection } from './ReleasesSection';
import { RankingSection } from './RankingSection';
import { SchedulerSection } from './SchedulerSection';
import { alphaApi } from '@/services/alphaApi';

interface CSVInfo {
  existe: boolean;
  total_acoes?: number;
  ultima_modificacao?: string;
  idade_horas?: number;
  atualizado?: boolean;
  erro?: string;
}

interface SystemStats {
  groq_keys_available?: number;
  cache_status?: string;
  last_analysis?: string;
  total_analyzed?: number;
}

export function AdminPanel() {
  const navigate = useNavigate();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [password, setPassword] = useState('');
  const [token, setToken] = useState<string | null>(null);
  const [csvInfo, setCsvInfo] = useState<CSVInfo | null>(null);
  const [historico, setHistorico] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [autoUpdate, setAutoUpdate] = useState(() => {
    // Carrega estado do localStorage ao iniciar
    const saved = localStorage.getItem('admin_auto_update');
    return saved === 'true';
  });
  const [systemStats, setSystemStats] = useState<SystemStats>({});
  const [empresasAprovadas, setEmpresasAprovadas] = useState<string[]>([]);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  
  // Ref para evitar carregamento duplicado
  const hasLoadedInitialData = useRef(false);
  
  // Salva estado do autoUpdate no localStorage quando muda
  useEffect(() => {
    localStorage.setItem('admin_auto_update', autoUpdate.toString());
    console.log(`📊 Estado autoUpdate mudou para: ${autoUpdate ? 'ON' : 'OFF'} (salvo no localStorage)`);
  }, [autoUpdate]);

  // Verifica autenticação ao carregar
  useEffect(() => {
    const savedToken = localStorage.getItem('admin_token');
    if (savedToken) {
      validateToken(savedToken);
    }
  }, []);

  // Auto-update quando ligado
  useEffect(() => {
    // Reset flag quando desliga
    if (!autoUpdate) {
      hasLoadedInitialData.current = false;
      console.log('🛑 Auto-update DESATIVADO');
      return;
    }
    
    if (!token) {
      console.log('⏳ Aguardando token para iniciar auto-update...');
      return;
    }
    
    console.log('🔄 Auto-update ATIVADO - Atualizando a cada 10s');
    
    // Atualiza imediatamente ao ligar (se ainda não carregou)
    if (!hasLoadedInitialData.current) {
      loadCSVInfo(token);
      loadSystemStats(token);
      loadEmpresasAprovadas(token);
      hasLoadedInitialData.current = true;
    }
    
    const interval = setInterval(() => {
      console.log('🔄 Auto-update executando...');
      loadCSVInfo(token);
      loadSystemStats(token);
      loadEmpresasAprovadas(token);
    }, 10000); // 10s (mais rápido para releases)

    return () => {
      console.log('🧹 Limpando intervalo do auto-update');
      clearInterval(interval);
    };
  }, [autoUpdate, token]);

  const validateToken = async (authToken: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/status', {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });

      if (response.ok) {
        setToken(authToken);
        setIsAuthenticated(true);
        loadCSVInfo(authToken);
        loadSystemStats(authToken);
        loadEmpresasAprovadas(authToken);
      } else {
        localStorage.removeItem('admin_token');
        setIsAuthenticated(false);
        setToken(null);
      }
    } catch (error) {
      localStorage.removeItem('admin_token');
      setIsAuthenticated(false);
      setToken(null);
    }
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password })
      });

      if (!response.ok) {
        throw new Error('Senha incorreta');
      }

      const data = await response.json();
      setToken(data.token);
      setIsAuthenticated(true);
      localStorage.setItem('admin_token', data.token);
      
      // Configura token na API
      alphaApi.setToken(data.token);
      
      setPassword('');
      setMessage({ type: 'success', text: 'Login realizado com sucesso!' });
      
      loadCSVInfo(data.token);
      loadSystemStats(data.token);
      loadEmpresasAprovadas(data.token);
    } catch (error) {
      setMessage({ type: 'error', text: 'Senha incorreta' });
    }
  };

  const handleLogout = async () => {
    localStorage.removeItem('admin_token');
    
    // Limpa token da API
    alphaApi.clearToken();
    
    if (token) {
      try {
        await fetch('http://localhost:8000/api/v1/admin/logout', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        });
      } catch (error) {
        console.log('Erro ao fazer logout:', error);
      }
    }
    
    setIsAuthenticated(false);
    setToken(null);
    setCsvInfo(null);
    setHistorico([]);
    setSystemStats({});
    // NÃO reseta autoUpdate - mantém preferência do usuário
    setMessage({ type: 'success', text: 'Logout realizado!' });
  };

  const loadCSVInfo = async (authToken: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/csv/info', {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });

      if (!response.ok) return;

      const data = await response.json();
      setCsvInfo(data.csv_atual);
      setHistorico(data.historico_recente || []);
    } catch (error) {
      console.error('Erro ao carregar CSV:', error);
    }
  };

  const loadSystemStats = async (authToken: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/status', {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });

      if (response.ok) {
        const data = await response.json();
        setSystemStats({
          groq_keys_available: 6,
          cache_status: data.csv?.atualizado ? 'Atualizado' : 'Desatualizado',
          total_analyzed: data.csv?.total_acoes || 0
        });
      }
    } catch (error) {
      console.error('Erro ao carregar stats:', error);
    }
  };

  const loadEmpresasAprovadas = async (authToken: string) => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/empresas-aprovadas', {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('📊 Empresas aprovadas carregadas:', data);
        console.log('📊 Total de empresas:', data.empresas?.length || 0);
        setEmpresasAprovadas(data.empresas || []);
      }
    } catch (error) {
      console.error('Erro ao carregar empresas:', error);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !token) return;

    setUploading(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/v1/admin/csv/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao fazer upload');
      }

      const data = await response.json();
      setMessage({ 
        type: 'success', 
        text: `CSV atualizado! ${data.detalhes.total_acoes} ações carregadas.` 
      });
      
      loadCSVInfo(token);
      loadSystemStats(token);
    } catch (error: unknown) {
      setMessage({ type: 'error', text: error instanceof Error ? error.message : 'Erro desconhecido' });
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  const handleRefresh = () => {
    if (token) {
      loadCSVInfo(token);
      loadSystemStats(token);
      loadEmpresasAprovadas(token);
      setMessage({ type: 'success', text: 'Dados atualizados!' });
    }
  };

  // Login Screen
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background">
        <div className="flex items-center justify-center min-h-screen p-4">
          <div className="w-full max-w-md">
            <div className="alpha-card p-8">
              <div className="flex justify-center mb-6">
                <div className="w-16 h-16 bg-primary/10 border border-primary/20 rounded-lg flex items-center justify-center">
                  <Shield className="w-8 h-8 text-primary" />
                </div>
              </div>
              
              <h2 className="font-display text-3xl font-bold text-foreground mb-2 text-center">
                Admin Panel
              </h2>
              <p className="text-muted-foreground text-center mb-8">
                Sistema de Gerenciamento
              </p>
              
              <form onSubmit={handleLogin} className="space-y-6">
                <div>
                  <label htmlFor="password-input" className="block text-sm font-medium text-foreground mb-2">
                    Senha de Acesso
                  </label>
                  <input
                    id="password-input"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="w-full px-4 py-3 bg-muted border border-border rounded-lg text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
                    placeholder="Digite a senha admin"
                    required
                  />
                </div>

                {message && (
                  <div className={`p-4 rounded-lg border ${
                    message.type === 'success' 
                      ? 'bg-alpha-green/10 border-alpha-green/20 text-alpha-green' 
                      : 'bg-alpha-red/10 border-alpha-red/20 text-alpha-red'
                  }`}>
                    {message.text}
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full bg-primary hover:bg-primary/90 text-primary-foreground font-semibold py-3 px-6 rounded-lg transition-all"
                >
                  Acessar Painel
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Admin Dashboard
  return (
    <div className="min-h-screen bg-background">
      {/* Header - Mesmo estilo do AlphaHeader */}
      <header className="border-b border-border bg-card/30 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-[1440px] mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <Terminal className="w-5 h-5 text-primary" />
              <h1 className="font-display font-bold text-lg tracking-tight text-foreground">
                ALPHA<span className="text-primary">ADMIN</span>
              </h1>
            </div>
            
            {/* Toggle Auto-Update */}
            <button
              type="button"
              onClick={() => {
                const newState = !autoUpdate;
                console.log(`🔘 Toggle clicado: ${autoUpdate ? 'ON' : 'OFF'} → ${newState ? 'ON' : 'OFF'}`);
                setAutoUpdate(newState);
                setMessage({ 
                  type: 'success', 
                  text: newState ? 'Auto-update ATIVADO (30s)' : 'Auto-update DESATIVADO' 
                });
              }}
              className={`flex items-center gap-1 px-2 py-0.5 rounded-full border transition-all ${
                autoUpdate 
                  ? 'bg-primary/10 border-primary/20' 
                  : 'bg-muted border-border'
              }`}
              title={autoUpdate ? 'Auto-update ON' : 'Auto-update OFF'}
            >
              <Power size={12} className={autoUpdate ? 'text-primary' : 'text-muted-foreground'} />
              <span className={`text-[10px] font-mono font-medium ${autoUpdate ? 'text-primary' : 'text-muted-foreground'}`}>
                {autoUpdate ? 'ON' : 'OFF'}
              </span>
            </button>
          </div>
          
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="text-muted-foreground hover:text-foreground transition-colors"
              title="Voltar ao Terminal"
            >
              <Home size={18} />
            </button>
            <button
              type="button"
              onClick={handleRefresh}
              className="text-muted-foreground hover:text-foreground transition-colors"
              title="Atualizar"
            >
              <RefreshCw size={18} />
            </button>
            <button
              type="button"
              onClick={handleLogout}
              className="text-alpha-red hover:text-alpha-red/80 transition-colors"
              title="Sair"
            >
              <LogOut size={18} />
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-[1440px] mx-auto px-4 py-6">
        {/* Message Banner */}
        {message && (
          <div className={`mb-4 p-4 rounded-lg border ${
            message.type === 'success' 
              ? 'bg-alpha-green/10 border-alpha-green/20 text-alpha-green' 
              : 'bg-alpha-red/10 border-alpha-red/20 text-alpha-red'
          }`}>
            <div className="flex items-center gap-3">
              {message.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
              <span className="text-sm">{message.text}</span>
            </div>
          </div>
        )}

        {/* Auto-Update Status */}
        {autoUpdate && (
          <div className="mb-4 bg-primary/10 border border-primary/20 rounded-lg p-4">
            <div className="flex items-center gap-3">
              <Activity className="w-5 h-5 text-primary animate-pulse" />
              <div>
                <p className="text-primary font-medium text-sm">Atualização Automática Ativa</p>
                <p className="text-primary/70 text-xs">Atualizando a cada 10 segundos (releases em tempo real)</p>
              </div>
            </div>
          </div>
        )}

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="alpha-card">
            <div className="flex items-center justify-between mb-2">
              <Database className="w-6 h-6 text-alpha-blue" />
              <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-medium ${
                csvInfo?.atualizado ? 'bg-alpha-green/10 text-alpha-green' : 'bg-alpha-amber/10 text-alpha-amber'
              }`}>
                {csvInfo?.atualizado ? 'OK' : 'OLD'}
              </span>
            </div>
            <p className="text-2xl font-bold text-foreground font-mono">{csvInfo?.total_acoes || 0}</p>
            <p className="text-xs text-muted-foreground">Ações no CSV</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center justify-between mb-2">
              <Clock className="w-6 h-6 text-alpha-amber" />
            </div>
            <p className="text-2xl font-bold text-foreground font-mono">{csvInfo?.idade_horas?.toFixed(1) || 0}h</p>
            <p className="text-xs text-muted-foreground">Idade do CSV</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center justify-between mb-2">
              <Activity className="w-6 h-6 text-alpha-green" />
            </div>
            <p className="text-2xl font-bold text-foreground font-mono">{systemStats.groq_keys_available || 6}</p>
            <p className="text-xs text-muted-foreground">Chaves Groq</p>
          </div>

          <div className="alpha-card">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-6 h-6 text-primary" />
            </div>
            <p className="text-2xl font-bold text-foreground font-mono">{empresasAprovadas.length}</p>
            <p className="text-xs text-muted-foreground">Empresas Aprovadas</p>
          </div>
        </div>

        {/* CSV Management */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
          {/* CSV Info */}
          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-alpha-blue" />
              <h3 className="font-display font-bold text-foreground">Informações do CSV</h3>
            </div>
            
            {csvInfo ? (
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <span className="text-sm text-muted-foreground">Status</span>
                  <span className={`flex items-center gap-2 text-sm font-medium ${
                    csvInfo.atualizado ? 'text-alpha-green' : 'text-alpha-amber'
                  }`}>
                    {csvInfo.atualizado ? <CheckCircle size={16} /> : <Clock size={16} />}
                    {csvInfo.atualizado ? 'Atualizado' : 'Desatualizado'}
                  </span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <span className="text-sm text-muted-foreground">Total</span>
                  <span className="text-foreground font-mono font-bold">{csvInfo.total_acoes || 0}</span>
                </div>
                
                <div className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                  <span className="text-sm text-muted-foreground">Atualização</span>
                  <span className="text-foreground font-mono text-xs">{csvInfo.ultima_modificacao || 'N/A'}</span>
                </div>
              </div>
            ) : (
              <p className="text-muted-foreground text-sm">Carregando...</p>
            )}
          </div>

          {/* CSV Upload */}
          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-4">
              <Upload className="w-5 h-5 text-primary" />
              <h3 className="font-display font-bold text-foreground">Upload de CSV</h3>
            </div>
            
            <div className="space-y-3">
              <p className="text-muted-foreground text-xs">
                Faça upload de um CSV atualizado com dados das ações.
              </p>
              
              <div className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-primary/30 transition-all cursor-pointer">
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  disabled={uploading}
                  className="hidden"
                  id="csv-upload"
                />
                <label
                  htmlFor="csv-upload"
                  className={`cursor-pointer block ${uploading ? 'opacity-50' : ''}`}
                >
                  <Upload size={32} className="mx-auto mb-3 text-muted-foreground" />
                  <p className="text-foreground font-medium text-sm mb-1">
                    {uploading ? 'Enviando...' : 'Clique para selecionar CSV'}
                  </p>
                  <p className="text-muted-foreground text-xs">
                    Colunas: ticker, roe, pl
                  </p>
                </label>
              </div>
            </div>
          </div>
        </div>

        {/* Botão de Consenso - SEMPRE VISÍVEL */}
        <div className="alpha-card mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Settings className="w-5 h-5 text-primary" />
            <h3 className="font-display font-bold text-foreground">Análise com Consenso (Groq - 6 Chaves)</h3>
          </div>
          <div className="text-center py-6">
            <p className="text-muted-foreground text-sm mb-4">
              Passo 1 (1x) + Passo 2 (3x consenso) usando Groq. Rotação entre 6 chaves com delays de 90s.
            </p>
            <button
              type="button"
              onClick={async () => {
                if (!token) return;
                setMessage({ type: 'success', text: 'Análise iniciada! Tempo: ~8-12 minutos (delays entre chaves)' });
                try {
                  await fetch('http://localhost:8000/api/v1/admin/iniciar-analise?usar_consenso=true', {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${token}` }
                  });
                } catch (error) {
                  console.error('Erro ao iniciar análise:', error);
                }
              }}
              className="px-6 py-3 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold rounded-lg transition-all"
            >
              🔄 Passo 1 (1x) + Passo 2 (3x) - GROQ
            </button>
          </div>
        </div>

        {/* Releases Section */}
        {empresasAprovadas.length > 0 ? (
          <ReleasesSection token={token || ''} empresasAprovadas={empresasAprovadas} />
        ) : (
          <div className="alpha-card">
            <div className="flex items-center gap-2 mb-4">
              <FileText className="w-5 h-5 text-primary" />
              <h3 className="font-display font-bold text-foreground">Releases de Resultados</h3>
            </div>
            <div className="text-center py-8">
              <div className="w-16 h-16 bg-alpha-amber/10 border border-alpha-amber/20 rounded-lg flex items-center justify-center mx-auto mb-4">
                <AlertCircle className="w-8 h-8 text-alpha-amber" />
              </div>
              <p className="text-foreground font-medium text-sm mb-2">
                Nenhuma empresa aprovada ainda
              </p>
              <p className="text-muted-foreground text-xs">
                Execute a análise com consenso acima para gerar a lista de empresas
              </p>
            </div>
          </div>
        )}

        {/* Ranking e Scheduler - TEMPORARIAMENTE DESABILITADO PARA DEBUG */}
        {/* 
        {token && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mt-6">
            <SchedulerSection token={token} />
          </div>
        )}

        {token && (
          <div className="mt-6">
            <RankingSection token={token} />
          </div>
        )}
        */}

        {/* History */}
        {historico.length > 0 && (
          <div className="alpha-card mt-6">
            <div className="flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-alpha-green" />
              <h3 className="font-display font-bold text-foreground">Histórico</h3>
            </div>
            
            <div className="space-y-2">
              {historico.map((entry) => (
                <div key={entry} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg hover:bg-muted transition-colors">
                  <CheckCircle size={14} className="text-alpha-green flex-shrink-0" />
                  <span className="text-muted-foreground text-xs font-mono flex-1">{entry}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
