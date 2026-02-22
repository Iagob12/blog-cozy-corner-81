import { useState, useEffect } from 'react';
import { Upload, FileText, CheckCircle, Clock, X, RefreshCw, Calendar } from 'lucide-react';

interface Release {
  ticker: string;
  trimestre: string;
  ano: number;
  data_upload?: string;
  filename?: string;
}

interface ReleasesPendentes {
  total: number;
  com_release: Release[];
  sem_release: string[];
  percentual_completo: number;
}

interface Props {
  token: string;
  empresasAprovadas?: string[];
}

export function ReleasesSection({ token, empresasAprovadas = [] }: Props) {
  const [releasesPendentes, setReleasesPendentes] = useState<ReleasesPendentes | null>(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadTicker, setUploadTicker] = useState('');
  const [uploadTrimestre, setUploadTrimestre] = useState('Q4');
  const [uploadAno, setUploadAno] = useState(2025);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [atualizandoRelease, setAtualizandoRelease] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [ultimaAtualizacao, setUltimaAtualizacao] = useState<Date | null>(null);

  useEffect(() => {
    if (empresasAprovadas.length > 0) {
      loadReleasesPendentes();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [empresasAprovadas]);

  // Auto-update a cada 10s quando há empresas aprovadas
  useEffect(() => {
    if (empresasAprovadas.length === 0) return;

    const interval = setInterval(() => {
      console.log('🔄 ReleasesSection: Atualizando releases...');
      loadReleasesPendentes();
    }, 10000); // 10s

    return () => clearInterval(interval);
  }, [empresasAprovadas]);

  const loadReleasesPendentes = async () => {
    if (empresasAprovadas.length === 0) return;

    try {
      const tickers = empresasAprovadas.join(',');
      const response = await fetch(
        `http://localhost:8000/api/v1/admin/releases/pendentes?tickers=${tickers}`,
        { headers: { 'Authorization': `Bearer ${token}` } }
      );

      if (response.ok) {
        const data = await response.json();
        setReleasesPendentes(data);
        setUltimaAtualizacao(new Date());
      }
    } catch (error) {
      console.error('Erro ao carregar releases:', error);
    }
  };

  const handleUploadRelease = async () => {
    if (!uploadFile || !uploadTicker) {
      setMessage({ type: 'error', text: 'Selecione arquivo e ticker' });
      return;
    }

    setUploading(true);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('ticker', uploadTicker);
      formData.append('trimestre', uploadTrimestre);
      formData.append('ano', uploadAno.toString());

      const response = await fetch('http://localhost:8000/api/v1/admin/releases/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao fazer upload');
      }

      setMessage({ type: 'success', text: `Release de ${uploadTicker} adicionado!` });
      setShowUploadModal(false);
      setUploadFile(null);
      setUploadTicker('');
      setAtualizandoRelease(null);
      
      // Atualiza lista imediatamente
      setTimeout(() => loadReleasesPendentes(), 500);
    } catch (error: unknown) {
      setMessage({ type: 'error', text: error instanceof Error ? error.message : 'Erro desconhecido' });
    } finally {
      setUploading(false);
    }
  };

  const handleAtualizarRelease = async (ticker: string, trimestre: string, ano: number) => {
    setAtualizandoRelease(ticker);
    setUploadTicker(ticker);
    setUploadTrimestre(trimestre);
    setUploadAno(ano);
    setShowUploadModal(true);
  };

  const openUploadModal = (ticker?: string) => {
    if (ticker) setUploadTicker(ticker);
    setShowUploadModal(true);
  };

  const formatarData = (dataISO?: string) => {
    if (!dataISO) return 'N/A';
    try {
      const data = new Date(dataISO);
      return data.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return 'N/A';
    }
  };

  if (!releasesPendentes) {
    return (
      <div className="alpha-card">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-primary" />
          <h3 className="font-display font-bold text-foreground">Releases</h3>
        </div>
        <p className="text-muted-foreground text-sm">Aguardando triagem...</p>
      </div>
    );
  }

  const { total, com_release, sem_release, percentual_completo } = releasesPendentes;

  return (
    <>
      <div className="alpha-card">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-primary" />
            <h3 className="font-display font-bold text-foreground">Releases de Resultados</h3>
            {releasesPendentes && (
              <span className="text-xs text-muted-foreground font-mono">
                ({com_release.length}/{total})
              </span>
            )}
            {ultimaAtualizacao && (
              <span className="text-[10px] text-muted-foreground/70 font-mono">
                • {ultimaAtualizacao.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
              </span>
            )}
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => loadReleasesPendentes()}
              className="flex items-center gap-1 px-2 py-1 bg-muted hover:bg-muted/80 text-foreground text-xs rounded transition-all"
              title="Atualizar lista"
            >
              <RefreshCw size={12} />
            </button>
            <button
              type="button"
              onClick={() => openUploadModal()}
              className="flex items-center gap-2 px-3 py-1.5 bg-primary hover:bg-primary/90 text-primary-foreground text-sm rounded-lg transition-all"
            >
              <Upload size={14} />
              Upload
            </button>
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

        {/* Progress */}
        <div className="mb-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm text-muted-foreground">Progresso</span>
            <span className="text-foreground font-mono text-sm font-bold">{com_release.length}/{total}</span>
          </div>
          <div className="w-full bg-muted rounded-full h-2">
            <div 
              className="bg-primary h-2 rounded-full transition-all"
              style={{ width: `${percentual_completo}%` }}
            />
          </div>
          <p className="text-xs text-muted-foreground mt-1">{percentual_completo.toFixed(0)}% completo</p>
        </div>

        {/* Com Release */}
        {com_release.length > 0 && (
          <div className="mb-4">
            <h4 className="text-xs font-mono text-muted-foreground mb-2">COM RELEASE ({com_release.length})</h4>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {com_release.map((release) => (
                <div 
                  key={`${release.ticker}-${release.trimestre}-${release.ano}`}
                  className="flex items-center justify-between p-3 bg-alpha-green/10 border border-alpha-green/20 rounded-lg hover:bg-alpha-green/20 transition-colors"
                >
                  <div className="flex items-center gap-3 flex-1">
                    <CheckCircle size={16} className="text-alpha-green flex-shrink-0" />
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-foreground font-mono font-medium text-sm">{release.ticker}</span>
                        <span className="text-muted-foreground text-xs">
                          {release.trimestre} {release.ano}
                        </span>
                      </div>
                      <div className="flex items-center gap-1 text-xs text-muted-foreground">
                        <Calendar size={12} />
                        <span>{formatarData(release.data_upload)}</span>
                      </div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleAtualizarRelease(release.ticker, release.trimestre, release.ano)}
                    className="flex items-center gap-1 px-2 py-1 bg-primary/10 hover:bg-primary/20 border border-primary/20 text-primary text-xs rounded transition-all"
                    title="Atualizar release"
                  >
                    <RefreshCw size={12} />
                    <span>Atualizar</span>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Sem Release */}
        {sem_release.length > 0 && (
          <div>
            <h4 className="text-xs font-mono text-muted-foreground mb-2">PENDENTE ({sem_release.length})</h4>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {sem_release.map((ticker) => (
                <div 
                  key={ticker}
                  className="flex items-center justify-between p-3 bg-alpha-amber/10 border border-alpha-amber/20 rounded-lg hover:bg-alpha-amber/20 transition-colors"
                >
                  <div className="flex items-center gap-3">
                    <Clock size={16} className="text-alpha-amber" />
                    <span className="text-foreground font-mono font-medium text-sm">{ticker}</span>
                  </div>
                  <button
                    type="button"
                    onClick={() => openUploadModal(ticker)}
                    className="px-3 py-1 bg-primary hover:bg-primary/90 text-primary-foreground text-xs rounded transition-all"
                  >
                    Upload
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Completo */}
        {percentual_completo === 100 && (
          <div className="mt-4 p-4 bg-alpha-green/10 border border-alpha-green/20 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <p className="text-alpha-green font-bold text-sm mb-1">✅ Todos os releases prontos!</p>
                <p className="text-alpha-green/70 text-xs mb-3">
                  Sistema pronto para análise incremental (analisa apenas empresas com releases)
                </p>
              </div>
              <button
                type="button"
                onClick={async () => {
                  setMessage({ type: 'success', text: 'Análise completa iniciada! Aguarde 10-20 minutos...' });
                  try {
                    await fetch('http://localhost:8000/api/v1/admin/analise-com-releases/executar', {
                      method: 'POST',
                      headers: { 
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                      }
                    });
                  } catch (error) {
                    console.error('Erro ao iniciar análise:', error);
                    setMessage({ type: 'error', text: 'Erro ao iniciar análise' });
                  }
                }}
                className="px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground text-sm font-semibold rounded-lg transition-all whitespace-nowrap"
              >
                Analisar com Releases
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Modal de Upload */}
      {showUploadModal && (
        <div className="fixed inset-0 bg-background/80 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="alpha-card w-full max-w-md">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-display font-bold text-foreground">
                {atualizandoRelease ? 'Atualizar Release' : 'Upload de Release'}
              </h3>
              <button
                type="button"
                onClick={() => {
                  setShowUploadModal(false);
                  setAtualizandoRelease(null);
                }}
                className="text-muted-foreground hover:text-foreground transition-colors"
              >
                <X size={20} />
              </button>
            </div>

            {atualizandoRelease && (
              <div className="mb-4 p-3 bg-primary/10 border border-primary/20 rounded-lg">
                <p className="text-primary text-sm">
                  ℹ️ Você está atualizando o release de <strong>{atualizandoRelease}</strong>. 
                  O arquivo anterior será substituído.
                </p>
              </div>
            )}

            <div className="space-y-4">
              {/* Ticker */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Ticker
                </label>
                {uploadTicker ? (
                  <div className="px-4 py-3 bg-muted border border-border rounded-lg text-foreground font-mono">
                    {uploadTicker}
                  </div>
                ) : (
                  <select
                    value={uploadTicker}
                    onChange={(e) => setUploadTicker(e.target.value)}
                    className="w-full px-4 py-3 bg-muted border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  >
                    <option value="">Selecione...</option>
                    {sem_release.map(ticker => (
                      <option key={ticker} value={ticker}>{ticker}</option>
                    ))}
                  </select>
                )}
              </div>

              {/* Trimestre */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Trimestre
                </label>
                <select
                  value={uploadTrimestre}
                  onChange={(e) => setUploadTrimestre(e.target.value)}
                  className="w-full px-4 py-3 bg-muted border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                >
                  <option value="Q1">Q1</option>
                  <option value="Q2">Q2</option>
                  <option value="Q3">Q3</option>
                  <option value="Q4">Q4</option>
                </select>
              </div>

              {/* Ano */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Ano
                </label>
                <input
                  type="number"
                  value={uploadAno}
                  onChange={(e) => setUploadAno(parseInt(e.target.value))}
                  className="w-full px-4 py-3 bg-muted border border-border rounded-lg text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  min="2020"
                  max="2030"
                />
              </div>

              {/* Arquivo */}
              <div>
                <label className="block text-sm font-medium text-foreground mb-2">
                  Arquivo PDF
                </label>
                <div className="border-2 border-dashed border-border rounded-lg p-6 text-center hover:border-primary/30 transition-colors">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="hidden"
                    id="release-file"
                  />
                  <label htmlFor="release-file" className="cursor-pointer block">
                    <Upload size={24} className="mx-auto mb-2 text-muted-foreground" />
                    {uploadFile ? (
                      <p className="text-foreground font-medium text-sm">{uploadFile.name}</p>
                    ) : (
                      <>
                        <p className="text-foreground font-medium text-sm mb-1">Selecionar PDF</p>
                        <p className="text-muted-foreground text-xs">Apenas arquivos PDF</p>
                      </>
                    )}
                  </label>
                </div>
              </div>

              {/* Botões */}
              <div className="flex gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  className="flex-1 px-4 py-3 bg-muted hover:bg-muted/80 text-foreground rounded-lg transition-colors"
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleUploadRelease}
                  disabled={uploading || !uploadFile || !uploadTicker}
                  className="flex-1 px-4 py-3 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {uploading ? 'Enviando...' : 'Upload'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
