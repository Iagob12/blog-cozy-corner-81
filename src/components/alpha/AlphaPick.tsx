import { ArrowUpRight, ShieldCheck, Eye } from "lucide-react";
import { motion } from "framer-motion";
import { type TopPick } from "@/services/alphaApi";
import Sparkline from "./Sparkline";

interface AlphaPickProps {
	onViewThesis: (ticker: string) => void;
	topPicks: TopPick[];
}

const AlphaPick = ({ onViewThesis, topPicks }: AlphaPickProps) => {
	const stock = topPicks[0]; // Alpha Pick é sempre o primeiro (rank 1)

	if (!stock) {
		return (
			<div className="rounded-xl border border-border bg-card p-6">
				<p className="text-muted-foreground">Carregando Alpha Pick...</p>
			</div>
		);
	}

	// Gerar sparkline simulado baseado no upside
	const generateSparkline = () => {
		const points = 30;
		const data = [];
		const baseValue = stock.preco_atual;
		const targetValue = stock.preco_teto;

		for (let i = 0; i < points; i++) {
			const progress = i / points;
			const value = baseValue + (targetValue - baseValue) * progress * 0.7;
			const noise = (Math.random() - 0.5) * baseValue * 0.05;
			data.push(value + noise);
		}
		return data;
	};

	const getConfidenceLevel = () => {
		if (stock.upside_potencial > 20) return "ALTA";
		if (stock.upside_potencial > 10) return "MÉDIA";
		return "MODERADA";
	};

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
						Confiança {getConfidenceLevel()}
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
						{stock.setor} · Rank #{stock.rank}
					</p>
				</div>
				<div className="text-right">
					<p className="text-2xl font-mono font-bold text-foreground">
						R${stock.preco_atual?.toFixed(2) || "0.00"}
					</p>
					<p className="text-sm font-mono font-semibold text-alpha-green">
						Teto: R${stock.preco_teto?.toFixed(2) || "0.00"}
					</p>
				</div>
			</div>

			{/* Metrics row */}
			<div className="grid grid-cols-4 gap-4 mt-6 pt-4 border-t border-border/50">
				<div>
					<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
						Upside
					</p>
					<p className="text-lg font-mono font-bold text-primary">
						+{(stock.upside_potencial || 0).toFixed(1)}%
					</p>
				</div>
				<div>
					<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
						ROE
					</p>
					<p className="text-lg font-mono font-bold text-foreground">
						{(stock.roe || 0).toFixed(1)}%
					</p>
				</div>
				<div>
					<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
						P/L
					</p>
					<p className="text-lg font-mono font-bold text-foreground">
						{(stock.pl || 0).toFixed(1)}x
					</p>
				</div>
				<div>
					<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono">
						CAGR
					</p>
					<p className="text-lg font-mono font-bold text-foreground">
						{(stock.cagr || 0).toFixed(1)}%
					</p>
				</div>
			</div>

			{/* Catalisadores */}
			<div className="mt-4 pt-4 border-t border-border/50">
				<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-2">
					Catalisadores
				</p>
				<div className="flex flex-wrap gap-2">
					{(stock.catalisadores || []).slice(0, 2).map((cat, idx) => (
						<span
							key={idx}
							className="text-xs px-2 py-1 rounded-md bg-primary/10 text-primary border border-primary/20"
						>
							{cat}
						</span>
					))}
				</div>
			</div>

			{/* Sparkline + CTA */}
			<div className="flex items-end justify-between mt-4 pt-4 border-t border-border/50">
				<Sparkline data={generateSparkline()} width={160} height={40} />
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
