import { TrendingUp, TrendingDown, Minus } from "lucide-react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface MarketOverview {
	timestamp: string;
	ibovespa: {
		pontos: number;
		variacao_pct: number;
	};
	dolar: {
		cotacao: number;
		variacao_pct: number;
	};
}

const MarketPulse = () => {
	const { data: marketData } = useQuery<MarketOverview>({
		queryKey: ["marketOverview"],
		queryFn: async () => {
			const response = await fetch(`${API_BASE_URL}/api/v1/market/overview`);
			if (!response.ok) throw new Error("Erro ao buscar dados do mercado");
			return response.json();
		},
		refetchInterval: 60000, // Atualiza a cada 1 minuto
		retry: 2,
	});

	const indicators = [
		{
			label: "IBOV",
			value: marketData?.ibovespa?.pontos?.toLocaleString('pt-BR', { maximumFractionDigits: 0 }) || "---",
			unit: " pts",
			change: marketData?.ibovespa?.variacao_pct || 0,
		},
		{
			label: "USD/BRL",
			value: marketData?.dolar?.cotacao?.toFixed(2) || "---",
			unit: "",
			change: marketData?.dolar?.variacao_pct || 0,
		},
		{
			label: "SELIC",
			value: "14.25",
			unit: "%",
			change: 0,
		},
		{
			label: "IPCA",
			value: "4.83",
			unit: "%",
			change: -0.12,
		},
	];

	return (
		<div className="w-full border-b border-border bg-card/50 backdrop-blur-sm">
			<div className="max-w-[1440px] mx-auto px-4">
				<div className="flex items-center gap-6 py-2 overflow-x-auto scrollbar-hide">
					<span className="text-[10px] uppercase tracking-[0.2em] text-muted-foreground font-mono whitespace-nowrap">
						Market Pulse
					</span>
					<div className="flex items-center gap-6">
						{indicators.map((indicator, i) => (
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
								{indicator.change !== 0 && (
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
										{indicator.change.toFixed(2)}%
									</span>
								)}
							</motion.div>
						))}
					</div>
				</div>
			</div>
		</div>
	);
};

export default MarketPulse;
