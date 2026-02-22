import { X, TrendingUp, Shield, AlertTriangle, Target } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { type TopPick } from "@/services/alphaApi";

interface ThesisPanelProps {
	stock: TopPick | null;
	onClose: () => void;
}

const ThesisPanel = ({ stock, onClose }: ThesisPanelProps) => {
  if (!stock) return null;

		// Proteção contra valores nulos
		const precoAtual = stock.preco_atual || 0;
		const precoTeto = stock.preco_teto || precoAtual * 1.05;
		const stopLoss = precoAtual * 0.9; // -10%
		const precoIdeal = precoTeto * 0.95; // -5% do teto

		return (
			<AnimatePresence>
				<motion.div
					initial={{ opacity: 0 }}
					animate={{ opacity: 1 }}
					exit={{ opacity: 0 }}
					className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50"
					onClick={onClose}
				>
					<motion.div
						initial={{ x: "100%" }}
						animate={{ x: 0 }}
						exit={{ x: "100%" }}
						transition={{ type: "spring", damping: 30, stiffness: 300 }}
						className="fixed right-0 top-0 h-full w-full max-w-2xl bg-card border-l border-border overflow-y-auto"
						onClick={(e) => e.stopPropagation()}
					>
						{/* Header */}
						<div className="sticky top-0 bg-card/95 backdrop-blur-sm border-b border-border p-6 flex items-center justify-between z-10">
							<div>
								<h2 className="text-2xl font-display font-bold text-foreground">
									{stock.ticker}
								</h2>
								<p className="text-sm text-muted-foreground mt-0.5">
									{stock.setor} · Rank #{stock.rank}
								</p>
							</div>
							<button
								onClick={onClose}
								className="p-2 rounded-lg hover:bg-muted transition-colors"
							>
								<X className="w-5 h-5" />
							</button>
						</div>

						{/* Content */}
						<div className="p-6 space-y-6">
							{/* Recomendação */}
							<div
								className={`p-4 rounded-lg border-2 ${
									stock.recomendacao_final?.includes("FORTE")
										? "border-alpha-green bg-alpha-green/10"
										: stock.recomendacao_final?.includes("COMPRA")
											? "border-primary bg-primary/10"
											: "border-yellow-500 bg-yellow-500/10"
								}`}
							>
								<div className="flex items-center gap-2 mb-2">
									<Target className="w-5 h-5" />
									<span className="font-mono font-bold text-sm uppercase tracking-wider">
										{stock.recomendacao_final || "AGUARDAR"}
									</span>
								</div>
								<p className="text-sm text-muted-foreground">
									{stock.sentiment_status === "Alerta"
										? "Atenção: Volume de menções acima do normal. Monitore antes de entrar."
										: "Condições favoráveis para entrada. Siga a estratégia definida."}
								</p>
							</div>

							{/* Análise Fundamentalista */}
							<div>
								<h3 className="text-sm font-mono font-semibold uppercase tracking-wider text-foreground mb-3 flex items-center gap-2">
									<Shield className="w-4 h-4" />
									Análise Fundamentalista
								</h3>
								<div className="grid grid-cols-2 gap-3">
									<div className="p-3 rounded-lg bg-muted/50">
										<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-1">
											Efficiency Score
										</p>
										<p className="text-xl font-mono font-bold text-primary">
											{(stock.efficiency_score || 0).toFixed(2)}
										</p>
										<p className="text-[10px] text-muted-foreground mt-1">
											Top {Math.ceil((stock.rank / 15) * 100)}%
										</p>
									</div>
									<div className="p-3 rounded-lg bg-muted/50">
										<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-1">
											Macro Weight
										</p>
										<p className="text-xl font-mono font-bold text-foreground">
											{(stock.macro_weight || 1).toFixed(2)}x
										</p>
										<p className="text-[10px] text-muted-foreground mt-1">
											{(stock.macro_weight || 1) > 1
												? "Setor favorecido"
												: "Setor neutro"}
										</p>
									</div>
									<div className="p-3 rounded-lg bg-muted/50">
										<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-1">
											ROE
										</p>
										<p className="text-xl font-mono font-bold text-foreground">
											{(stock.roe || 0).toFixed(1)}%
										</p>
										<p className="text-[10px] text-muted-foreground mt-1">
											{(stock.roe || 0) > 20
												? "Excelente"
												: (stock.roe || 0) > 15
													? "Bom"
													: "Moderado"}
										</p>
									</div>
									<div className="p-3 rounded-lg bg-muted/50">
										<p className="text-[10px] uppercase tracking-wider text-muted-foreground font-mono mb-1">
											CAGR
										</p>
										<p className="text-xl font-mono font-bold text-foreground">
											{(stock.cagr || 0).toFixed(1)}%
										</p>
										<p className="text-[10px] text-muted-foreground mt-1">
											{(stock.cagr || 0) > 20
												? "Alto crescimento"
												: "Crescimento sólido"}
										</p>
									</div>
								</div>
							</div>

							{/* Estratégia de Entrada */}
							<div>
								<h3 className="text-sm font-mono font-semibold uppercase tracking-wider text-foreground mb-3 flex items-center gap-2">
									<TrendingUp className="w-4 h-4" />
									Estratégia de Entrada
								</h3>
								<div className="space-y-3">
									<div className="flex items-center justify-between p-3 rounded-lg bg-muted/50">
										<span className="text-sm text-muted-foreground">
											Preço Atual
										</span>
										<span className="font-mono font-bold text-lg">
											R$ {precoAtual.toFixed(2)}
										</span>
									</div>
									<div className="flex items-center justify-between p-3 rounded-lg bg-alpha-green/10 border border-alpha-green/30">
										<span className="text-sm text-alpha-green">Preço Teto</span>
										<span className="font-mono font-bold text-lg text-alpha-green">
											R$ {precoTeto.toFixed(2)}
										</span>
									</div>
									<div className="flex items-center justify-between p-3 rounded-lg bg-primary/10 border border-primary/30">
										<span className="text-sm text-primary">
											Preço Ideal (-5%)
										</span>
										<span className="font-mono font-bold text-lg text-primary">
											R$ {precoIdeal.toFixed(2)}
										</span>
									</div>
									<div className="flex items-center justify-between p-3 rounded-lg bg-alpha-red/10 border border-alpha-red/30">
										<span className="text-sm text-alpha-red">
											Stop Loss (-10%)
										</span>
										<span className="font-mono font-bold text-lg text-alpha-red">
											R$ {stopLoss.toFixed(2)}
										</span>
									</div>
								</div>

								<div className="mt-4 p-4 rounded-lg bg-primary/5 border border-primary/20">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm font-medium">Meta de Lucro</span>
										<span className="text-2xl font-mono font-bold text-primary">
											+{(stock.upside_potencial || 0).toFixed(1)}%
										</span>
									</div>
									<div className="flex items-center justify-between text-sm text-muted-foreground">
										<span>Tempo Estimado</span>
										<span className="font-mono">
											{stock.tempo_estimado_dias || 90} dias
										</span>
									</div>
								</div>
							</div>

							{/* Catalisadores */}
							<div>
								<h3 className="text-sm font-mono font-semibold uppercase tracking-wider text-foreground mb-3">
									🚀 Catalisadores
								</h3>
								<div className="space-y-2">
									{(stock.catalisadores || []).length > 0 ? (
										stock.catalisadores.map((cat, idx) => (
											<div
												key={idx}
												className="p-3 rounded-lg bg-muted/50 border border-border"
											>
												<p className="text-sm text-foreground">{cat}</p>
											</div>
										))
									) : (
										<div className="p-3 rounded-lg bg-muted/50 border border-border">
											<p className="text-sm text-muted-foreground">
												Nenhum catalisador identificado
											</p>
										</div>
									)}
								</div>
							</div>

							{/* Sentiment Analysis */}
							<div>
								<h3 className="text-sm font-mono font-semibold uppercase tracking-wider text-foreground mb-3">
									😊 Sentiment Analysis
								</h3>
								<div className="p-4 rounded-lg bg-muted/50">
									<div className="flex items-center justify-between mb-2">
										<span className="text-sm text-muted-foreground">
											Status
										</span>
										<span
											className={`font-mono font-bold ${
												stock.sentiment_status === "Alerta"
													? "text-yellow-500"
													: "text-alpha-green"
											}`}
										>
											{stock.sentiment_status || "NEUTRO"}
										</span>
									</div>
									{stock.sentiment_ratio && (
										<div className="flex items-center justify-between">
											<span className="text-sm text-muted-foreground">
												Ratio de Menções
											</span>
											<span className="font-mono">
												{stock.sentiment_ratio.toFixed(2)}x
											</span>
										</div>
									)}
								</div>
							</div>

							{/* Riscos */}
							<div>
								<h3 className="text-sm font-mono font-semibold uppercase tracking-wider text-foreground mb-3 flex items-center gap-2">
									<AlertTriangle className="w-4 h-4" />
									Riscos
								</h3>
								<div className="space-y-2">
									<div className="p-3 rounded-lg bg-alpha-red/10 border border-alpha-red/30">
										<p className="text-sm text-muted-foreground">
											• Volatilidade do mercado
										</p>
									</div>
									<div className="p-3 rounded-lg bg-alpha-red/10 border border-alpha-red/30">
										<p className="text-sm text-muted-foreground">
											• Mudanças no cenário macroeconômico
										</p>
									</div>
									{stock.divida && stock.divida > 0.5 && (
										<div className="p-3 rounded-lg bg-alpha-red/10 border border-alpha-red/30">
											<p className="text-sm text-muted-foreground">
												• Nível de endividamento:{" "}
												{(stock.divida * 100).toFixed(0)}%
											</p>
										</div>
									)}
								</div>
							</div>

							{/* CTA */}
							<button className="w-full py-3 rounded-lg bg-primary text-primary-foreground font-display font-semibold hover:bg-primary/90 transition-colors">
								Adicionar à Carteira
							</button>
						</div>
					</motion.div>
				</motion.div>
			</AnimatePresence>
		);
};

export default ThesisPanel;
