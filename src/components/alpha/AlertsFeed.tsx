import { AlertTriangle, TrendingUp, AlertCircle } from "lucide-react";
import { motion } from "framer-motion";
import { alerts } from "@/data/stockData";

const iconMap = {
  euforia: <AlertTriangle className="w-4 h-4 text-alpha-red" />,
  oportunidade: <TrendingUp className="w-4 h-4 text-alpha-green" />,
  cautela: <AlertCircle className="w-4 h-4 text-accent" />,
};

const borderMap = {
  euforia: "border-l-alpha-red",
  oportunidade: "border-l-alpha-green",
  cautela: "border-l-accent",
};

const AlertsFeed = () => {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-accent" />
        <h3 className="text-[10px] uppercase tracking-[0.2em] text-accent font-mono font-semibold">
          Feed Anti-Manada
        </h3>
      </div>

      {alerts.map((alert, i) => (
        <motion.div
          key={alert.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
          className={`alpha-card !rounded-lg border-l-2 ${borderMap[alert.type]}`}
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5">{iconMap[alert.type]}</div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between gap-2">
                <h4 className="text-sm font-display font-semibold text-foreground truncate">
                  {alert.title}
                </h4>
                <span className="text-[10px] text-muted-foreground font-mono whitespace-nowrap">
                  {alert.timestamp}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                {alert.description}
              </p>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
};

export default AlertsFeed;
