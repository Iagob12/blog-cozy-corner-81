import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Loader2, TrendingUp, AlertTriangle, CheckCircle, Download } from 'lucide-react';

interface CarteiraItem {
  posicao: number;
  ticker: string;
  acao: string;
  justificativa: string;
  preco_atual?: number;
  variacao_dia?: number;
  anti_manada?: {
    veredito: string;
    exposicao_midia: string;
  };
}

interface FluxoResultado {
  timestamp: string;
  carteira_final: CarteiraItem[];
  etapas: {
    radar: any;
    dados_coletados: number;
    top_15: any[];
    relatorios_processados: number;
  };
}

export function PortfolioBuilder() {
  const [loading, setLoading] = useState(false);
  const [resultado, setResultado] = useState<FluxoResultado | null>(null);
  const [etapaAtual, setEtapaAtual] = useState('');

  const executarFluxo = async () => {
    setLoading(true);
    setEtapaAtual('Iniciando análise...');
    
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/v1/portfolio/executar-fluxo-completo`,
        { method: 'POST' }
      );
      
      const data = await response.json();
      setResultado(data);
      setEtapaAtual('Concluído!');
    } catch (error) {
      console.error('Erro:', error);
      setEtapaAtual('Erro ao executar fluxo');
    } finally {
      setLoading(false);
    }
  };

  const getVereditoColor = (veredito: string) => {
    if (veredito === 'ENTRAR_AGORA') return 'bg-green-500';
    if (veredito === 'ESPERAR_CORRECAO') return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getAcaoIcon = (acao: string) => {
    if (acao === 'entrar_primeiro') return <CheckCircle className="w-5 h-5 text-green-600" />;
    if (acao === 'monitorar') return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
    return <TrendingUp className="w-5 h-5 text-blue-600" />;
  };

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <span>🎯 Construtor de Carteira Alpha</span>
            <Button 
              onClick={executarFluxo} 
              disabled={loading}
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analisando...
                </>
              ) : (
                '🚀 Executar Fluxo Completo'
              )}
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading && (
            <div className="text-center py-8">
              <Loader2 className="w-12 h-12 animate-spin mx-auto mb-4 text-blue-600" />
              <p className="text-lg font-medium">{etapaAtual}</p>
              <p className="text-sm text-muted-foreground mt-2">
                Isso pode levar alguns minutos...
              </p>
            </div>
          )}

          {!loading && !resultado && (
            <div className="text-center py-12">
              <p className="text-muted-foreground mb-4">
                Clique no botão acima para iniciar a análise completa
              </p>
              <div className="text-sm text-left max-w-2xl mx-auto space-y-2">
                <p className="font-semibold">O fluxo irá:</p>
                <ol className="list-decimal list-inside space-y-1 text-muted-foreground">
                  <li>Identificar setores em ascensão (Prompt 1)</li>
                  <li>Coletar dados de ações do mercado</li>
                  <li>Filtrar as 15 melhores (Prompt 2)</li>
                  <li>Buscar relatórios de resultados</li>
                  <li>Análise profunda com IA (Prompt 3)</li>
                  <li>Montar carteira final</li>
                  <li>Buscar preços em tempo real</li>
                  <li>Verificação anti-manada</li>
                </ol>
              </div>
            </div>
          )}

          {resultado && (
            <div className="space-y-6">
              {/* Resumo das Etapas */}
              <div className="grid grid-cols-4 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">
                    {resultado.etapas?.dados_coletados || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Ações Analisadas</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {resultado.etapas?.top_15?.length || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Top Selecionadas</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {resultado.etapas?.relatorios_processados || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">PDFs Analisados</div>
                </div>
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <div className="text-2xl font-bold text-yellow-600">
                    {resultado.carteira_final?.length || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Carteira Final</div>
                </div>
              </div>

              {/* Carteira Final */}
              <div>
                <h3 className="text-xl font-bold mb-4">✨ Carteira Recomendada</h3>
                <div className="space-y-4">
                  {resultado.carteira_final?.map((item) => (
                    <Card key={item.ticker} className="border-l-4 border-l-blue-500">
                      <CardContent className="pt-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <div className="text-3xl font-bold text-blue-600">
                              {item.posicao}
                            </div>
                            <div>
                              <div className="text-xl font-bold">{item.ticker}</div>
                              <div className="flex items-center gap-2 mt-1">
                                {getAcaoIcon(item.acao)}
                                <span className="text-sm font-medium capitalize">
                                  {item.acao.replace('_', ' ')}
                                </span>
                              </div>
                            </div>
                          </div>
                          
                          <div className="text-right">
                            {item.preco_atual && (
                              <>
                                <div className="text-2xl font-bold">
                                  R$ {item.preco_atual.toFixed(2)}
                                </div>
                                {item.variacao_dia !== undefined && (
                                  <div className={`text-sm ${
                                    item.variacao_dia >= 0 ? 'text-green-600' : 'text-red-600'
                                  }`}>
                                    {item.variacao_dia >= 0 ? '+' : ''}
                                    {item.variacao_dia.toFixed(2)}%
                                  </div>
                                )}
                              </>
                            )}
                          </div>
                        </div>

                        <p className="text-sm text-muted-foreground mb-4">
                          {item.justificativa}
                        </p>

                        {item.anti_manada && (
                          <div className="flex items-center gap-2 pt-3 border-t">
                            <Badge 
                              className={getVereditoColor(item.anti_manada.veredito)}
                            >
                              {item.anti_manada.veredito.replace('_', ' ')}
                            </Badge>
                            <span className="text-xs text-muted-foreground">
                              Exposição: {item.anti_manada.exposicao_midia}
                            </span>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Setores em Ascensão */}
              {resultado.etapas?.radar?.setores_aceleracao && (
                <div>
                  <h3 className="text-lg font-bold mb-3">📊 Setores em Ascensão</h3>
                  <div className="grid grid-cols-2 gap-3">
                    {resultado.etapas.radar.setores_aceleracao.slice(0, 4).map((setor: any, idx: number) => (
                      <div key={idx} className="p-3 border rounded-lg">
                        <div className="font-medium">{setor.setor}</div>
                        <div className="text-xs text-muted-foreground mt-1">
                          {setor.catalisador.substring(0, 80)}...
                        </div>
                        <Badge variant="outline" className="mt-2">
                          {setor.estagio_ciclo}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Ações */}
              <div className="flex gap-2 pt-4 border-t">
                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Exportar Relatório
                </Button>
                <Button variant="outline" size="sm" onClick={executarFluxo}>
                  🔄 Atualizar Análise
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
