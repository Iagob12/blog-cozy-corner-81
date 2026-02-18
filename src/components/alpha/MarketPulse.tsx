import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { motion } from "framer-motion";
import { macroIndicators } from "@/data/stockData";

const MarketPulse = () => {
  return (
    <div className="w-full border-b border-border bg-card/50 backdrop-blur-sm">
      <div className="max-w-[1440px] mx-auto px-4">
        <div className="flex items-center gap-6 py-2 overflow-x-auto scrollbar-hide">
          <span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground font-mono whitespace-nowrap">
            Market Pulse
          </span>
          <div className="flex items-center gap-6">
            {macroIndicators.map((indicator, i) => (
              <motion.div
                key={indicator.label}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="flex items-center gap-2 whitespace-nowrap"
              >
                <span className="text-xs text-muted-foreground font-mono">
                  {indicator.label}
                </span>
                <span className="text-sm font-semibold text-foreground font-mono">
                  {indicator.value}{indicator.unit}
                </span>
                <span
                  className={`flex items-center gap-0.5 text-xs font-mono ${
                    indicator.change > 0
                      ? "text-alpha-green"
                      : indicator.change < 0
                      ? "text-alpha-red"
                      : "text-muted-foreground"
                  }`}
                >
                  {indicator.change > 0 ? (
                    <TrendingUp className="w-3 h-3" />
                  ) : indicator.change < 0 ? (
                    <TrendingDown className="w-3 h-3" />
                  ) : (
                    <Minus className="w-3 h-3" />
                  )}
                  {indicator.change > 0 ? "+" : ""}
                  {indicator.change}%
                </span>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MarketPulse;
