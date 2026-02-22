import { useState, useCallback, useEffect } from "react";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import AlphaHeader from "@/components/alpha/AlphaHeader";
import MarketPulse from "@/components/alpha/MarketPulse";
import AlphaPick from "@/components/alpha/AlphaPick";
import EliteTable from "@/components/alpha/EliteTable";
import AlertsFeed from "@/components/alpha/AlertsFeed";
import ThesisPanel from "@/components/alpha/ThesisPanel";
import LoadingScreen from "@/components/alpha/LoadingScreen";
import { alphaApi, type TopPick } from "@/services/alphaApi";

const AlphaTerminal = () => {
	const [selectedStock, setSelectedStock] = useState<TopPick | null>(null);
	const [previousRanks, setPreviousRanks] = useState<Record<string, number>>(
		{},
	);
	const [isLoading, setIsLoading] = useState(true);

	// Buscar ranking atual da API
	const {
		data: rankingData,
		error,
		isLoading: queryLoading,
		dataUpdatedAt,
	} = useQuery({
		queryKey: ["rankingAtual"],
		queryFn: async () => {
			try {
				return await alphaApi.getRankingAtual();
			} catch (err) {
				console.error("Erro ao buscar ranking:", err);
				throw err;
			}
		},
		refetchInterval: 60000, // Atualiza a cada 1 minuto
		retry: 2,
		staleTime: 0, // Sempre busca dados frescos
	});

	const topPicks = rankingData?.ranking || [];

	// Controla loading inicial
	useEffect(() => {
		if (!queryLoading) {
			setIsLoading(false);
		}
	}, [queryLoading]);

	// Atualiza ranks anteriores quando dados mudam
	useEffect(() => {
		if (topPicks && topPicks.length > 0) {
			const newRanks: Record<string, number> = {};
			topPicks.forEach((stock, index) => {
				newRanks[stock.ticker] = index + 1;
			});

			setPreviousRanks(newRanks);
		}
	}, [topPicks]);

	const handleViewThesis = useCallback(
		(ticker: string) => {
			const stock = topPicks?.find((s) => s.ticker === ticker);
			if (stock) setSelectedStock(stock);
		},
		[topPicks],
	);

	if (isLoading) {
		// Loading inicial
		return <LoadingScreen />;
	}

	if (error && !topPicks.length) {
		// Erro de conexão
		return (
			<div className="min-h-screen bg-background flex items-center justify-center">
				<div className="text-center max-w-md">
					<div className="text-red-500 text-6xl mb-4">⚠️</div>
					<h2 className="text-2xl font-bold mb-2">Erro ao Conectar</h2>
					<p className="text-muted-foreground mb-4">
						Não foi possível conectar ao backend.
					</p>
					<p className="text-sm text-muted-foreground mb-4">
						Verifique se o servidor está rodando em:
						<br />
						<code className="bg-muted px-2 py-1 rounded">
							http://localhost:8000
						</code>
					</p>
					<button
						type="button"
						onClick={() => window.location.reload()}
						className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
					>
						Tentar Novamente
					</button>
				</div>
			</div>
		);
	}

	if (!topPicks.length) {
		// Sem dados
		return (
			<div className="min-h-screen bg-background flex items-center justify-center">
				<div className="text-center max-w-md">
					<div className="text-yellow-500 text-6xl mb-4">📊</div>
					<h2 className="text-2xl font-bold mb-2">
						Nenhuma Análise Disponível
					</h2>
					<p className="text-muted-foreground mb-4">
						Execute uma análise no painel admin para ver os resultados aqui.
					</p>
					<button
						type="button"
						onClick={() => (window.location.href = "/admin")}
						className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90"
					>
						Ir para Admin
					</button>
				</div>
			</div>
		);
	}

	return (
		<div className="min-h-screen bg-background">
			<AlphaHeader />

			{/* Banner com info do ranking */}
			{rankingData && (
				<div className="bg-primary/10 border-b border-primary/20 px-4 py-2">
					<div className="max-w-[1440px] mx-auto flex items-center gap-4 text-sm">
						<span className="text-primary font-medium">
							📊 {rankingData.total_aprovadas} empresas aprovadas
						</span>
						<span className="text-muted-foreground">
							Versão: {rankingData.versao}
						</span>
						<span className="text-muted-foreground ml-auto">
							Atualizado:{" "}
							{new Date(rankingData.timestamp).toLocaleString("pt-BR")}
						</span>
					</div>
				</div>
			)}

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
						<AlphaPick onViewThesis={handleViewThesis} topPicks={topPicks} />
					</motion.div>

					{/* Alerts Feed - 1 col */}
					<motion.div
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ delay: 0.2 }}
					>
						<AlertsFeed topPicks={topPicks} previousRanks={previousRanks} />
					</motion.div>

					{/* Elite Table - full width */}
					<motion.div
						className="lg:col-span-3"
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ delay: 0.3 }}
					>
						<EliteTable
							onSelectStock={setSelectedStock}
							topPicks={topPicks}
							previousRanks={previousRanks}
						/>
					</motion.div>
				</div>
			</main>

			{/* Thesis Panel */}
			<ThesisPanel
				stock={selectedStock}
				onClose={() => setSelectedStock(null)}
			/>
		</div>
	);
};

export default AlphaTerminal;
