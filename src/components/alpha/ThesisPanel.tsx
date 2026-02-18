import { X, Target, TrendingUp, Zap, ShieldCheck } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import type { Stock } from "@/data/stockData";

interface ThesisPanelProps {
  stock: Stock | null;
  onClose: () => void;
}

const ThesisPanel = ({ stock, onClose }: ThesisPanelProps) => {
  return (
    <AnimatePresence>
      {stock && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-background/80 backdrop-blur-sm z-40"
          />

          {/* Panel */}
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: 0 }}
            exit={{ x: "100%" }}
            transition={{ type: "spring", damping: 30, stiffness: 300 }}
            className="fixed right-0 top-0 h-full w-full max-w-lg bg-card border-l border-border z-50 overflow-y-auto"
          >
            {/* Header */}
            <div className="sticky top-0 bg-card/95 backdrop-blur-sm border-b border-border px-6 py-4 flex items-center justify-between z-10">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-xl font-display font-bold text-foreground">
                    {stock.ticker}
                  </h2>
                  <div className={`flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-medium border ${
                    stock.confidence === "alta"
                      ? "bg-primary/10 border-primary/20 text-primary"
                      : stock.confidence === "média"
                      ? "bg-alpha-amber/10 border-alpha-amber/20 text-accent"
                      : "bg-alpha-red/10 border-alpha-red/20 text-destructive"
                  }`}>
                    <ShieldCheck className="w-3 h-3" />
                    {stock.confidence.toUpperCase()}
                  </div>
                </div>
                <p className="text-sm text-muted-foreground">{stock.name}</p>
              </div>
              <button
                onClick={onClose}
                className="p-2 rounded-lg hover:bg-muted transition-colors"
              >
                <X className="w-5 h-5 text-muted-foreground" />
              </button>
            </div>

            {/* Content */}
            <div className="px-6 py-6 space-y-6">
              {/* Price targets */}
              <div className="grid grid-cols-2 gap-3">
                <div className="rounded-lg bg-muted/50 border border-border p-4">
                  <div className="flex items-center gap-1.5 mb-1">
                    <Target className="w-3.5 h-3.5 text-alpha-amber" />
                    <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
                      Preço Máx. Compra
                    </span>
                  </div>
                  <p className="text-xl font-mono font-bold text-accent">
                    R${stock.maxBuyPrice.toFixed(2)}
                  </p>
                </div>
                <div className="rounded-lg bg-muted/50 border border-border p-4">
                  <div className="flex items-center gap-1.5 mb-1">
                    <TrendingUp className="w-3.5 h-3.5 text-primary" />
                    <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
                      Alvo de Saída
                    </span>
                  </div>
                  <p className="text-xl font-mono font-bold text-primary">
                    R${stock.targetPrice.toFixed(2)}
                  </p>
                </div>
              </div>

              {/* Catalyst */}
              <div className="rounded-lg bg-secondary/5 border border-secondary/20 p-4">
                <div className="flex items-center gap-1.5 mb-2">
                  <Zap className="w-3.5 h-3.5 text-secondary" />
                  <span className="text-[10px] uppercase tracking-[0.2em] text-secondary font-mono font-semibold">
                    Catalisador
                  </span>
                </div>
                <p className="text-sm text-foreground/90 leading-relaxed">
                  {stock.catalyst}
                </p>
              </div>

              {/* Thesis */}
              <div>
                <h3 className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground font-mono font-semibold mb-3">
                  Análise Tática
                </h3>
                <div className="font-mono text-sm text-foreground/80 leading-relaxed whitespace-pre-wrap bg-muted/30 rounded-lg p-4 border border-border/50">
                  {stock.thesis}
                </div>
              </div>

              {/* Metrics summary */}
              <div className="grid grid-cols-4 gap-2">
                {[
                  { label: "ROE", value: `${stock.roe}%` },
                  { label: "P/L", value: `${stock.pl}x` },
                  { label: "CAGR", value: `${stock.cagr5y}%` },
                  { label: "Upside", value: `+${stock.upside}%`, highlight: true },
                ].map((m) => (
                  <div key={m.label} className="text-center rounded-lg bg-muted/30 border border-border/50 py-3">
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-1">
                      {m.label}
                    </p>
                    <p className={`text-sm font-mono font-bold ${m.highlight ? "text-primary" : "text-foreground"}`}>
                      {m.value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default ThesisPanel;
