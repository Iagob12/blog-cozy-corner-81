import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, AlertCircle, Target } from 'lucide-react';

interface SetorAceleracao {
  setor: string;
  catalisador: string;
  estagio_ciclo: 'começo' | 'meio' | 'fim';
  potencial_upside: string;
}

interface MovimentoSilencioso {
  ativo_tipo: string;
  nome: string;
  similaridade: string;
  radar_varejo: 'baixo' | 'medio' | 'alto';
}

interface RadarData {
  setores_aceleracao: SetorAceleracao[];
  movimentos_silenciosos: MovimentoSilencioso[];
  narrativa_institucional?: {
    tema: string;
    descricao: string;
    tempo_ate_varejo: string;
  };
}

export function RadarOportunidades() {
  const [data, setData] = useState<RadarData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchRadar();
  }, []);

  const fetchRadar = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/v1/alpha/radar-oportunidades`);
      const result = await response.json();
      setData(result);
    } catch (error) {
      console.error('Erro ao buscar radar:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Analisando mercado...</div>;
  if (!data) return null;

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Target className="w-5 h-5" />
            Radar de Oportunidades
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Setores em Aceleração */}
          <div>
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Setores em Aceleração
            </h3>
            <div className="space-y-3">
              {data.setores_aceleracao?.map((setor, idx) => (
                <div key={idx} className="border rounded-lg p-3">
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-medium">{setor.setor}</span>
                    <Badge variant={
                      setor.estagio_ciclo === 'começo' ? 'default' :
                      setor.estagio_ciclo === 'meio' ? 'secondary' : 'outline'
                    }>
                      {setor.estagio_ciclo}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">{setor.catalisador}</p>
                  <div className="text-sm font-medium text-green-600">
                    Upside: {setor.potencial_upside}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Movimentos Silenciosos */}
          <div>
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <AlertCircle className="w-4 h-4" />
              Movimentos Silenciosos (Antes da Manada)
            </h3>
            <div className="space-y-3">
              {data.movimentos_silenciosos?.map((mov, idx) => (
                <div key={idx} className="border rounded-lg p-3 bg-blue-50">
                  <div className="flex items-start justify-between mb-2">
                    <span className="font-medium">{mov.nome}</span>
                    <Badge variant={mov.radar_varejo === 'baixo' ? 'default' : 'destructive'}>
                      Radar: {mov.radar_varejo}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{mov.similaridade}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Narrativa Institucional */}
          {data.narrativa_institucional && (
            <div className="border-t pt-4">
              <h3 className="font-semibold mb-2">Narrativa Institucional</h3>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <div className="font-medium mb-1">{data.narrativa_institucional.tema}</div>
                <p className="text-sm text-muted-foreground mb-2">
                  {data.narrativa_institucional.descricao}
                </p>
                <div className="text-xs text-yellow-700">
                  Tempo até varejo descobrir: {data.narrativa_institucional.tempo_ate_varejo}
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
