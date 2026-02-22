import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, AlertTriangle } from 'lucide-react';

interface SwingAnalysis {
  saude_empresa: string;
  eventos_proximos: string[];
  momento_tecnico: string;
  gatilho_concreto: string;
  stop_loss: number;
  alvo: number;
  relacao_risco_retorno: number;
  recomendacao: string;
  justificativa: string;
  momentum?: any;
}

export function SwingTradeAnalysis() {
  const [ticker, setTicker] = useState('');
  const [analysis, setAnalysis] = useState<SwingAnalysis | null>(null);
  const [loading, setLoading] = useState(false);

  const analyze = async () => {
    if (!ticker) return;
    
    setLoading(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/v1/alpha/swing-trade/${ticker}`
      );
      const result = await response.json();
      setAnalysis(result);
    } catch (error) {
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Análise Swing Trade (5-20 dias)</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Input
            placeholder="Digite o ticker (ex: PRIO3)"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            onKeyPress={(e) => e.key === 'Enter' && analyze()}
          />
          <Button onClick={analyze} disabled={loading}>
            {loading ? 'Analisando...' : 'Analisar'}
          </Button>
        </div>

        {analysis && (
          <div className="space-y-4">
            {/* Recomendação */}
            <div className={`border-2 rounded-lg p-4 ${
              analysis.recomendacao === 'ENTRAR' ? 'border-green-500 bg-green-50' :
              analysis.recomendacao === 'AGUARDAR' ? 'border-yellow-500 bg-yellow-50' :
              'border-red-500 bg-red-50'
            }`}>
              <div className="flex items-center gap-2 mb-2">
                <TrendingUp className="w-5 h-5" />
                <span className="font-bold text-lg">{analysis.recomendacao}</span>
              </div>
              <p className="text-sm">{analysis.justificativa}</p>
            </div>

            {/* Saúde e Momento */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <div className="text-sm text-muted-foreground mb-1">Saúde da Empresa</div>
                <Badge variant={analysis.saude_empresa === 'saudável' ? 'default' : 'destructive'}>
                  {analysis.saude_empresa}
                </Badge>
              </div>
              <div>
                <div className="text-sm text-muted-foreground mb-1">Momento Técnico</div>
                <Badge variant={analysis.momento_tecnico === 'favoravel' ? 'default' : 'secondary'}>
                  {analysis.momento_tecnico}
                </Badge>
              </div>
            </div>

            {/* Gatilho */}
            <div>
              <div className="text-sm font-semibold mb-1">Gatilho Concreto</div>
              <p className="text-sm">{analysis.gatilho_concreto}</p>
            </div>

            {/* Eventos Próximos */}
            {analysis.eventos_proximos?.length > 0 && (
              <div>
                <div className="text-sm font-semibold mb-2">Eventos Próximos</div>
                <ul className="space-y-1">
                  {analysis.eventos_proximos.map((evento, idx) => (
                    <li key={idx} className="text-sm flex items-start gap-2">
                      <AlertTriangle className="w-4 h-4 mt-0.5 text-yellow-600" />
                      {evento}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Risco/Retorno */}
            <div className="border rounded-lg p-4 bg-gray-50">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-xs text-muted-foreground mb-1">Stop Loss</div>
                  <div className="font-bold text-red-600">R$ {analysis.stop_loss?.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground mb-1">Alvo</div>
                  <div className="font-bold text-green-600">R$ {analysis.alvo?.toFixed(2)}</div>
                </div>
                <div>
                  <div className="text-xs text-muted-foreground mb-1">Risco/Retorno</div>
                  <div className="font-bold">{analysis.relacao_risco_retorno?.toFixed(1)}:1</div>
                </div>
              </div>
            </div>

            {/* Momentum */}
            {analysis.momentum && (
              <div className="border-t pt-4">
                <div className="text-sm font-semibold mb-2">Indicadores de Momentum</div>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div>Tendência: <span className="font-medium">{analysis.momentum.tendencia}</span></div>
                  <div>Força: <span className="font-medium">{analysis.momentum.forca_momentum}</span></div>
                  <div>Var. 30d: <span className="font-medium">{analysis.momentum.variacao_30d_pct}%</span></div>
                  <div>Dist. MA20: <span className="font-medium">{analysis.momentum.distancia_ma20_pct}%</span></div>
                </div>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
