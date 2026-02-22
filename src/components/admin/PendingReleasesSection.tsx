import { useState, useEffect } from 'react';
import { FileText, AlertCircle, Upload, CheckCircle, Clock } from 'lucide-react';

interface PendingRelease {
  ticker: string;
  empresa: string;
  setor: string;
  perfil: string;
  preco_atual: number;
  status: string;
}

interface PendingReleasesData {
  total: number;
  empresas: PendingRelease[];
  timestamp: string | null;
  idade_horas: number;
  mensagem: string;
}

interface Props {
  token: string;
}

export function PendingReleasesSection({ token }: Props) {
  const [data, setData] = useState<PendingReleasesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState<string | null>(null);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadPendingReleases();
  }, [token]);

  const loadPendingReleases = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/admin/releases-pendentes', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const result = await response.json();
        setData(result);
      }
    } catch (error) {
      console.error('Erro ao carregar releases pendentes:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (ticker: string, e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(ticker);
    setMessage(null);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('ticker', ticker);
      formData.append('trimestre', 'Q4');
      formData.append('ano', '2025');

      const response = await fetch('http://localhost:8000/api/v1/admin/releases/upload', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao fazer upload');
      }

      setMessage({ 
        type: 'success', 
        text: `Release de ${ticker} enviado com sucesso!` 
      });
      
      // Recarrega lista
      setTimeout(() => loadPendingReleases(), 2000);
    } catch (error: unknown) {
      setMessage({ 
        type: 'error', 
        text: error instanceof Error ? error.message : 'Erro desconhecido' 
      });
    } finally {
      setUploading(null);
      e.target.value = '';
    }
  };

  if (loading) {
    return (
      <div className="alpha-card">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-alpha-amber" />
          <h3 className="font-display font-bold text-foreground">Releases Pendentes</h3>
        </div>
        <p className="text-muted-foreground text-sm">Carregando...</p>
      </div>
    );
  }

  if (!data || data.total === 0) {
    return (
      <div className="alpha-card">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-alpha-green" />
          <h3 className="font-display font-bold text-foreground">Releases Pendentes</h3>
        </div>
        <div className="text-center py-8">
          <div className="w-16 h-16 bg-alpha-green/10 border border-alpha-green/20 rounded-lg flex items-center justify-center mx-auto mb-4">
            <CheckCircle className="w-8 h-8 text-alpha-green" />
          </div>
          <p className="text-foreground font-medium text-sm mb-2">
            Nenhum release pendente
          </p>
          <p className="text-muted-foreground text-xs">
            Todas as empresas aprovadas têm releases
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="alpha-card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-alpha-amber" />
          <h3 className="font-display font-bold text-foreground">Releases Pendentes</h3>
          <span className="px-2 py-0.5 bg-alpha-amber/10 border border-alpha-amber/20 rounded text-alpha-amber text-xs font-mono font-medium">
            {data.total}
          </span>
        </div>
        {data.idade_horas !== undefined && (
          <div className="flex items-center gap-1 text-muted-foreground text-xs">
            <Clock size={12} />
            <span>{data.idade_horas.toFixed(1)}h atrás</span>
          </div>
        )}
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

      <div className="bg-alpha-amber/5 border border-alpha-amber/20 rounded-lg p-3 mb-4">
        <div className="flex items-start gap-2">
          <AlertCircle className="w-4 h-4 text-alpha-amber flex-shrink-0 mt-0.5" />
          <div>
            <p className="text-alpha-amber text-xs font-medium mb-1">
              Ação Necessária
            </p>
            <p className="text-alpha-amber/80 text-xs">
              {data.total} empresas aguardando upload de releases Q4 2025. 
              O sistema só pode analisar empresas com releases disponíveis.
            </p>
          </div>
        </div>
      </div>

      <div className="space-y-2 max-h-[400px] overflow-y-auto">
        {data.empresas.map((empresa) => (
          <div 
            key={empresa.ticker}
            className="flex items-center justify-between p-3 bg-muted/50 rounded-lg hover:bg-muted transition-colors"
          >
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-mono font-bold text-foreground text-sm">
                  {empresa.ticker}
                </span>
                <span className="px-1.5 py-0.5 bg-primary/10 border border-primary/20 rounded text-primary text-[10px] font-mono font-medium">
                  {empresa.perfil}
                </span>
              </div>
              <p className="text-muted-foreground text-xs mb-1">
                {empresa.empresa}
              </p>
              <div className="flex items-center gap-3 text-[10px] text-muted-foreground">
                <span>{empresa.setor}</span>
                <span>•</span>
                <span className="font-mono">R$ {empresa.preco_atual.toFixed(2)}</span>
              </div>
            </div>

            <div>
              <input
                type="file"
                accept=".pdf"
                onChange={(e) => handleFileUpload(empresa.ticker, e)}
                disabled={uploading === empresa.ticker}
                className="hidden"
                id={`upload-${empresa.ticker}`}
              />
              <label
                htmlFor={`upload-${empresa.ticker}`}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all cursor-pointer ${
                  uploading === empresa.ticker
                    ? 'bg-muted border-border text-muted-foreground cursor-not-allowed'
                    : 'bg-primary/10 border-primary/20 text-primary hover:bg-primary/20'
                }`}
              >
                <Upload size={14} />
                <span className="text-xs font-medium">
                  {uploading === empresa.ticker ? 'Enviando...' : 'Upload'}
                </span>
              </label>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
