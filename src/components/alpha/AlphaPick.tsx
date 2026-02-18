import { ArrowUpRight, ShieldCheck, Eye } from "lucide-react";
import { motion } from "framer-motion";
import { alphaPickStock } from "@/data/stockData";
import Sparkline from "./Sparkline";

interface AlphaPickProps {
  onViewThesis: (ticker: string) => void;
}

const AlphaPick = ({ onViewThesis }: AlphaPickProps) => {
  const stock = alphaPickStock;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden rounded-xl border border-primary/30 bg-gradient-to-br from-card via-card to-primary/5 p-6 alpha-glow"
    >
      {/* Badge */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
          <span className="text-[10px] uppercase tracking-[0.2em] text-primary font-mono font-semibold">
            The Alpha Pick
          </span>
        </div>
        <div className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-primary/10 border border-primary/20">
          <ShieldCheck className="w-3 h-3 text-primary" />
          <span className="text-[10px] text-primary font-mono font-medium">
            Confiança {stock.confidence.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Main info */}
      <div className="flex items-start justify-between">
        <div>
          <h2 className="text-3xl font-display font-bold text-foreground tracking-tight">
            {stock.ticker}
          </h2>
          <p className="text-sm text-muted-foreground mt-0.5">
            {stock.name} · {stock.sector}
          </p>
        </div>
        <div className="text-right">
          <p className="text-2xl font-mono font-bold text-foreground">
            R${stock.price.toFixed(2)}
          </p>
          <p className={`text-sm font-mono font-semibold ${stock.change >= 0 ? "text-alpha-green" : "text-alpha-red"}`}>
            {stock.change >= 0 ? "+" : ""}{stock.change}%
          </p>
        </div>
      </div>

      {/* Metrics row */}
      <div className="grid grid-cols-4 gap-4 mt-6 pt-4 border-t border-border/50">
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">Upside</p>
          <p className="text-lg font-mono font-bold text-primary">+{stock.upside}%</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">ROE</p>
          <p className="text-lg font-mono font-bold text-foreground">{stock.roe}%</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">P/L</p>
          <p className="text-lg font-mono font-bold text-foreground">{stock.pl}x</p>
        </div>
        <div>
          <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">CAGR 5A</p>
          <p className="text-lg font-mono font-bold text-foreground">{stock.cagr5y}%</p>
        </div>
      </div>

      {/* Sparkline + CTA */}
      <div className="flex items-end justify-between mt-4 pt-4 border-t border-border/50">
        <Sparkline data={stock.sparkline} width={160} height={40} />
        <button
          onClick={() => onViewThesis(stock.ticker)}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground font-display font-semibold text-sm hover:bg-primary/90 transition-colors"
        >
          <Eye className="w-4 h-4" />
          Ver Tese
          <ArrowUpRight className="w-3 h-3" />
        </button>
      </div>
    </motion.div>
  );
};

export default AlphaPick;
