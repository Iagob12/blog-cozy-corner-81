import { motion } from "framer-motion";
import { ChevronRight, ArrowUp, ArrowDown, Minus } from "lucide-react";
import { type TopPick } from "@/services/alphaApi";
import Sparkline from "./Sparkline";

interface EliteTableProps {
	onSelectStock: (stock: TopPick) => void;
	topPicks: TopPick[];
	previousRanks: Record<string, number>;
}

const EliteTable = ({
	onSelectStock,
	topPicks,
	previousRanks,
}: EliteTableProps) => {
	// Ordena por efficiency_score para garantir ranking correto
	const sortedPicks = [...topPicks].sort(
		(a, b) => b.efficiency_score - a.efficiency_score,
	);

	const getRankChange = (ticker: string, currentRank: number) => {
		const previousRank = previousRanks[ticker];
		if (!previousRank) return null;

		const diff = previousRank - currentRank;
		if (diff === 0) return { type: "same", value: 0 };
		if (diff > 0) return { type: "up", value: diff };
		return { type: "down", value: Math.abs(diff) };
	};

	const generateSparkline = (stock: TopPick) => {
		const points = 20;
		const data = [];
		const baseValue = stock.preco_atual || 50;

		for (let i = 0; i < points; i++) {
			const progress = i / points;
			const trend = stock.upside_potencial > 0 ? 1 : -1;
			const value = baseValue * (1 + progress * trend * 0.05);
			const noise = (Math.random() - 0.5) * baseValue * 0.02;
			data.push(value + noise);
		}
		return data;
	};

	return (
		<div className="alpha-card !p-0 overflow-hidden">
			<div className="px-4 py-3 border-b border-border flex items-center justify-between">
				<div className="flex items-center gap-2">
					<div className="w-1.5 h-1.5 rounded-full bg-secondary" />
					<h3 className="text-[10px] uppercase tracking-[0.2em] text-secondary font-mono font-semibold">
						Elite Stocks — Top {sortedPicks.length} Ranking
					</h3>
				</div>
				<div className="text-[10px] text-muted-foreground font-mono">
					Ordenado por Score de Eficiência
				</div>
			</div>

			<div className="overflow-x-auto">
				<table className="w-full">
					<thead>
						<tr className="border-b border-border">
							{[
								"#",
								"Ticker",
								"Setor",
								"Preço",
								"Teto",
								"ROE",
								"P/L",
								"CAGR",
								"Upside",
								"Rec",
								"Gráfico",
								"",
							].map((header) => (
								<th
									key={header}
									className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono font-medium px-3 py-2 text-left whitespace-nowrap"
								>
									{header}
								</th>
							))}
						</tr>
					</thead>
					<tbody>
						{sortedPicks.map((stock, i) => (
							<motion.tr
								key={stock.ticker}
								initial={{ opacity: 0, x: -10 }}
								animate={{ opacity: 1, x: 0 }}
								transition={{ delay: i * 0.03 }}
								onClick={() => onSelectStock(stock)}
								className="border-b border-border/50 hover:bg-muted/30 cursor-pointer transition-colors group"
								role="button"
								tabIndex={0}
								onKeyDown={(e) => {
									if (e.key === "Enter" || e.key === " ") {
										e.preventDefault();
										onSelectStock(stock);
									}
								}}
								aria-label={`Ver detalhes de ${stock.ticker}`}
							>
								<td className="px-3 py-2.5 font-mono text-xs">
									<div className="flex items-center gap-2">
										<span
											className={`inline-flex items-center justify-center w-6 h-6 rounded-full text-xs font-bold ${
												i === 0
													? "bg-yellow-500/20 text-yellow-500 border border-yellow-500/50"
													: i === 1
														? "bg-gray-400/20 text-gray-400 border border-gray-400/50"
														: i === 2
															? "bg-orange-500/20 text-orange-500 border border-orange-500/50"
															: "bg-muted/50 text-muted-foreground"
											}`}
										>
											{i + 1}
										</span>
										{(() => {
											const change = getRankChange(stock.ticker, i + 1);
											if (!change) return null;

											if (change.type === "up") {
												return (
													<div className="flex items-center gap-0.5 text-green-500">
														<ArrowUp className="w-3 h-3" />
														<span className="text-[10px] font-mono font-bold">
															{change.value}
														</span>
													</div>
												);
											}
											if (change.type === "down") {
												return (
													<div className="flex items-center gap-0.5 text-red-500">
														<ArrowDown className="w-3 h-3" />
														<span className="text-[10px] font-mono font-bold">
															{change.value}
														</span>
													</div>
												);
											}
											return (
												<Minus className="w-3 h-3 text-muted-foreground/50" />
											);
										})()}
									</div>
								</td>
								<td className="px-3 py-2.5">
									<span className="font-mono font-semibold text-sm text-foreground">
										{stock.ticker}
									</span>
								</td>
								<td className="px-3 py-2.5 text-xs text-muted-foreground whitespace-nowrap">
									{stock.setor || "N/A"}
								</td>
								<td className="px-3 py-2.5 font-mono text-sm text-foreground">
									R${(stock.preco_atual || 0).toFixed(2)}
								</td>
								<td className="px-3 py-2.5 font-mono text-sm text-alpha-green">
									R${(stock.preco_teto || 0).toFixed(2)}
								</td>
								<td className="px-3 py-2.5 font-mono text-sm text-foreground">
									{(stock.roe || 0).toFixed(1)}%
								</td>
								<td className="px-3 py-2.5 font-mono text-sm text-foreground">
									{(stock.pl || 0).toFixed(1)}x
								</td>
								<td className="px-3 py-2.5 font-mono text-sm text-foreground">
									{(stock.cagr || 0).toFixed(1)}%
								</td>
								<td className="px-3 py-2.5 font-mono text-sm font-semibold text-primary">
									+{(stock.upside_potencial || 0).toFixed(1)}%
								</td>
								<td className="px-3 py-2.5">
									<span
										className={`text-[10px] px-2 py-0.5 rounded-full font-mono font-medium whitespace-nowrap ${
											(stock.recomendacao_final || "").includes("FORTE")
												? "bg-alpha-green/20 text-alpha-green border border-alpha-green/30"
												: (stock.recomendacao_final || "").includes("COMPRA")
													? "bg-primary/20 text-primary border border-primary/30"
													: (stock.recomendacao_final || "").includes(
																"AGUARDAR",
															)
														? "bg-yellow-500/20 text-yellow-500 border border-yellow-500/30"
														: "bg-muted text-muted-foreground border border-border"
										}`}
									>
										{(stock.recomendacao_final || "N/A").split(" ")[0]}
									</span>
								</td>
								<td className="px-3 py-2.5">
									<Sparkline data={generateSparkline(stock)} />
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
