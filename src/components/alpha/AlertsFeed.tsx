import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, AlertTriangle, ArrowUp, ArrowDown, XCircle } from "lucide-react";
import { type TopPick } from "@/services/alphaApi";

interface AlertsFeedProps {
  topPicks: TopPick[];
  previousRanks: Record<string, number>;
}

interface Alert {
  type: 'rank_up' | 'rank_down' | 'sell' | 'buy' | 'warning' | 'removed';
  ticker: string;
  message: string;
  time: string;
  priority: number;
}

const AlertsFeed = ({ topPicks, previousRanks }: AlertsFeedProps) => {
  const generateAlerts = (): Alert[] => {
    const alerts: Alert[] = [];
    const currentTickers = new Set(topPicks.map(s => s.ticker));
    
    // 1. Detecta ações que SAÍRAM do ranking (VENDER)
    Object.keys(previousRanks).forEach(ticker => {
      if (!currentTickers.has(ticker)) {
        alerts.push({
          type: 'removed',
          ticker,
          message: `Saiu do ranking - Considere vender`,
          time: 'Agora',
          priority: 10
        });
      }
    });
    
    // 2. Detecta mudanças de rank e oportunidades
    topPicks.forEach((stock, index) => {
      const currentRank = index + 1;
      const previousRank = previousRanks[stock.ticker];
      
      // Mudança de rank
      if (previousRank && previousRank !== currentRank) {
        const diff = previousRank - currentRank;
        if (diff > 0) {
          // Subiu no ranking
          alerts.push({
            type: 'rank_up',
            ticker: stock.ticker,
            message: `Subiu ${diff} ${diff === 1 ? 'posição' : 'posições'} no ranking`,
            time: 'Agora',
            priority: 8
          });
        } else {
          // Desceu no ranking
          alerts.push({
            type: 'rank_down',
            ticker: stock.ticker,
            message: `Desceu ${Math.abs(diff)} ${Math.abs(diff) === 1 ? 'posição' : 'posições'}`,
            time: 'Agora',
            priority: 7
          });
        }
      }
      
      // 3. Oportunidade de compra (preço abaixo do teto)
      const ratio = stock.preco_atual ? stock.preco_atual / stock.preco_teto : 1;
      if (ratio <= 0.90 && stock.recomendacao_final === 'COMPRAR') {
        alerts.push({
          type: 'buy',
          ticker: stock.ticker,
          message: `${((1 - ratio) * 100).toFixed(0)}% abaixo do teto - Oportunidade`,
          time: 'Agora',
          priority: 9
        });
      }
      
      // 4. Realizar lucros (preço acima do teto)
      if (ratio >= 1.05) {
        alerts.push({
          type: 'sell',
          ticker: stock.ticker,
          message: `${((ratio - 1) * 100).toFixed(0)}% acima do teto - Realizar lucros`,
          time: 'Agora',
          priority: 9
        });
      }
      
      // 5. Risco de manada (volume anormal)
      if (stock.sentiment_ratio && stock.sentiment_ratio >= 2.5) {
        alerts.push({
          type: 'warning',
          ticker: stock.ticker,
          message: `Volume ${stock.sentiment_ratio.toFixed(1)}x acima - Risco manada`,
          time: 'Agora',
          priority: 6
        });
      }
    });
    
    // Ordena por prioridade e limita a 8 alertas
    return alerts
      .sort((a, b) => b.priority - a.priority)
      .slice(0, 8);
  };

  const alerts = generateAlerts();

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'buy':
        return <TrendingDown className="w-4 h-4 text-green-500" />;
      case 'sell':
        return <TrendingUp className="w-4 h-4 text-red-500" />;
      case 'removed':
        return <XCircle className="w-4 h-4 text-red-500" />;
      case 'rank_up':
        return <ArrowUp className="w-4 h-4 text-green-500" />;
      case 'rank_down':
        return <ArrowDown className="w-4 h-4 text-orange-500" />;
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />;
      default:
        return null;
    }
  };

  const getAlertStyle = (type: string) => {
    switch (type) {
      case 'buy':
        return 'border-l-green-500 bg-green-500/5';
      case 'sell':
      case 'removed':
        return 'border-l-red-500 bg-red-500/5';
      case 'rank_up':
        return 'border-l-green-500 bg-green-500/5';
      case 'rank_down':
        return 'border-l-orange-500 bg-orange-500/5';
      case 'warning':
        return 'border-l-yellow-500 bg-yellow-500/5';
      default:
        return 'border-l-border';
    }
  };

  const getAlertTitle = (type: string) => {
    switch (type) {
      case 'buy':
        return 'OPORTUNIDADE';
      case 'sell':
        return 'REALIZAR LUCROS';
      case 'removed':
        return 'VENDER';
      case 'rank_up':
        return 'SUBIU';
      case 'rank_down':
        return 'DESCEU';
      case 'warning':
        return 'ATENÇÃO';
      default:
        return 'ALERTA';
    }
  };

  return (
    <div className="alpha-card h-full">
      <div className="flex items-center gap-2 mb-4">
        <div className="w-1.5 h-1.5 rounded-full bg-alpha-red animate-pulse-glow" />
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-alpha-red font-mono font-semibold">
          Alertas Ativos
        </h3>
      </div>

      <div className="space-y-2.5">
        {alerts.length === 0 ? (
          <div className="text-center py-8">
            <p className="text-sm text-muted-foreground">Nenhum alerta no momento</p>
          </div>
        ) : (
          alerts.map((alert, i) => (
            <motion.div
              key={`${alert.ticker}-${alert.type}-${i}`}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.05 }}
              className={`p-3 rounded-lg border-l-2 ${getAlertStyle(alert.type)} transition-all hover:scale-[1.02] cursor-pointer`}
            >
              <div className="flex items-start gap-2">
                {getAlertIcon(alert.type)}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] uppercase tracking-wider font-mono font-semibold text-muted-foreground">
                      {getAlertTitle(alert.type)}
                    </span>
                    <span className="text-[9px] text-muted-foreground font-mono">
                      {alert.time}
                    </span>
                  </div>
                  <p className="font-mono font-semibold text-sm text-foreground mb-0.5">
                    {alert.ticker}
                  </p>
                  <p className="text-xs text-muted-foreground leading-tight">
                    {alert.message}
                  </p>
                </div>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
};

export default AlertsFeed;
