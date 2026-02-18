import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import AlphaHeader from "@/components/alpha/AlphaHeader";
import MarketPulse from "@/components/alpha/MarketPulse";
import AlphaPick from "@/components/alpha/AlphaPick";
import EliteTable from "@/components/alpha/EliteTable";
import AlertsFeed from "@/components/alpha/AlertsFeed";
import ThesisPanel from "@/components/alpha/ThesisPanel";
import { eliteStocks, type Stock } from "@/data/stockData";

const AlphaTerminal = () => {
  const [selectedStock, setSelectedStock] = useState<Stock | null>(null);

  const handleViewThesis = useCallback(
    (ticker: string) => {
      const stock = eliteStocks.find((s) => s.ticker === ticker);
      if (stock) setSelectedStock(stock);
    },
    []
  );

  return (
    <div className="min-h-screen bg-background">
      <AlphaHeader />
      <MarketPulse />

      <main className="max-w-[1440px] mx-auto px-4 py-6">
        {/* Bento Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Alpha Pick - spans 2 cols */}
          <motion.div
            className="lg:col-span-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <AlphaPick onViewThesis={handleViewThesis} />
          </motion.div>

          {/* Alerts Feed - 1 col */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <AlertsFeed />
          </motion.div>

          {/* Elite Table - full width */}
          <motion.div
            className="lg:col-span-3"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <EliteTable onSelectStock={setSelectedStock} />
          </motion.div>
        </div>
      </main>

      {/* Thesis Panel */}
      <ThesisPanel stock={selectedStock} onClose={() => setSelectedStock(null)} />
    </div>
  );
};

export default AlphaTerminal;
