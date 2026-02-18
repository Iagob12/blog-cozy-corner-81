import { motion } from "framer-motion";
import { ChevronRight } from "lucide-react";
import { eliteStocks, type Stock } from "@/data/stockData";
import Sparkline from "./Sparkline";

interface EliteTableProps {
  onSelectStock: (stock: Stock) => void;
}

const EliteTable = ({ onSelectStock }: EliteTableProps) => {
  return (
    <div className="alpha-card !p-0 overflow-hidden">
      <div className="px-4 py-3 border-b border-border flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-secondary" />
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-secondary font-mono font-semibold">
          Quantitative Layer — Top 15
        </h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-border">
              {["#", "Ticker", "Setor", "Preço", "Δ%", "ROE", "P/L", "CAGR 5A", "Upside", "Gráfico", ""].map(
                (header) => (
                  <th
                    key={header}
                    className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono font-medium px-3 py-2 text-left whitespace-nowrap"
                  >
                    {header}
                  </th>
                )
              )}
            </tr>
          </thead>
          <tbody>
            {eliteStocks.map((stock, i) => (
              <motion.tr
                key={stock.ticker}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.03 }}
                onClick={() => onSelectStock(stock)}
                className="border-b border-border/50 hover:bg-muted/30 cursor-pointer transition-colors group"
              >
                <td className="px-3 py-2.5 font-mono text-xs text-muted-foreground">
                  {i + 1}
                </td>
                <td className="px-3 py-2.5">
                  <span className="font-mono font-semibold text-sm text-foreground">
                    {stock.ticker}
                  </span>
                </td>
                <td className="px-3 py-2.5 text-xs text-muted-foreground whitespace-nowrap">
                  {stock.sector}
                </td>
                <td className="px-3 py-2.5 font-mono text-sm text-foreground">
                  R${stock.price.toFixed(2)}
                </td>
                <td className={`px-3 py-2.5 font-mono text-sm font-medium ${stock.change >= 0 ? "text-alpha-green" : "text-alpha-red"}`}>
                  {stock.change >= 0 ? "+" : ""}{stock.change}%
                </td>
                <td className="px-3 py-2.5 font-mono text-sm text-foreground">
                  {stock.roe}%
                </td>
                <td className="px-3 py-2.5 font-mono text-sm text-foreground">
                  {stock.pl}x
                </td>
                <td className="px-3 py-2.5 font-mono text-sm text-foreground">
                  {stock.cagr5y}%
                </td>
                <td className="px-3 py-2.5 font-mono text-sm font-semibold text-primary">
                  +{stock.upside}%
                </td>
                <td className="px-3 py-2.5">
                  <Sparkline data={stock.sparkline} />
                </td>
                <td className="px-3 py-2.5">
                  <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors" />
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default EliteTable;
