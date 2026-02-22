import express from "express";
import cors from "cors";

const app = express();
const PORT = 8000;

app.use(cors());
app.use(express.json());

function getDefaultStocks() {
	return [
		{
			Ticker: "WEGE3",
			PL: 28.5,
			ROE: 22.3,
			CAGR: 18.5,
			Divida: 0.35,
			Setor: "Industrial",
			Preco: 45.8,
		},
		{
			Ticker: "ITUB4",
			PL: 6.8,
			ROE: 18.9,
			CAGR: 12.8,
			Divida: 0.45,
			Setor: "Financeiro",
			Preco: 28.9,
		},
		{
			Ticker: "PETR4",
			PL: 4.2,
			ROE: 25.6,
			CAGR: 15.2,
			Divida: 0.68,
			Setor: "Energia",
			Preco: 38.5,
		},
		{
			Ticker: "VALE3",
			PL: 3.8,
			ROE: 28.4,
			CAGR: 10.5,
			Divida: 0.52,
			Setor: "Industrial",
			Preco: 65.2,
		},
		{
			Ticker: "BBDC4",
			PL: 5.9,
			ROE: 17.2,
			CAGR: 11.9,
			Divida: 0.48,
			Setor: "Financeiro",
			Preco: 24.3,
		},
		{
			Ticker: "RENT3",
			PL: 12.5,
			ROE: 19.8,
			CAGR: 22.4,
			Divida: 0.28,
			Setor: "Varejo",
			Preco: 58.7,
		},
		{
			Ticker: "RADL3",
			PL: 18.3,
			ROE: 20.5,
			CAGR: 16.8,
			Divida: 0.15,
			Setor: "Saúde",
			Preco: 42.1,
		},
		{
			Ticker: "LREN3",
			PL: 14.2,
			ROE: 21.7,
			CAGR: 19.3,
			Divida: 0.22,
			Setor: "Varejo",
			Preco: 18.9,
		},
		{
			Ticker: "EGIE3",
			PL: 16.8,
			ROE: 18.2,
			CAGR: 13.5,
			Divida: 0.58,
			Setor: "Energia",
			Preco: 44.6,
		},
		{
			Ticker: "TAEE11",
			PL: 12.4,
			ROE: 16.8,
			CAGR: 11.2,
			Divida: 0.62,
			Setor: "Energia",
			Preco: 38.2,
		},
		{
			Ticker: "CPLE6",
			PL: 11.9,
			ROE: 17.5,
			CAGR: 12.8,
			Divida: 0.55,
			Setor: "Energia",
			Preco: 42.8,
		},
		{
			Ticker: "VIVT3",
			PL: 8.5,
			ROE: 22.8,
			CAGR: 14.6,
			Divida: 0.72,
			Setor: "Tecnologia",
			Preco: 52.3,
		},
		{
			Ticker: "TOTS3",
			PL: 9.2,
			ROE: 19.4,
			CAGR: 13.9,
			Divida: 0.48,
			Setor: "Tecnologia",
			Preco: 28.7,
		},
		{
			Ticker: "PRIO3",
			PL: 6.8,
			ROE: 24.5,
			CAGR: 28.3,
			Divida: 0.42,
			Setor: "Energia",
			Preco: 48.9,
		},
		{
			Ticker: "EMBR3",
			PL: 18.7,
			ROE: 16.2,
			CAGR: 15.8,
			Divida: 0.68,
			Setor: "Industrial",
			Preco: 22.5,
		},
		{
			Ticker: "SUZB3",
			PL: 11.3,
			ROE: 19.6,
			CAGR: 17.2,
			Divida: 0.38,
			Setor: "Industrial",
			Preco: 54.8,
		},
		{
			Ticker: "KLBN11",
			PL: 8.9,
			ROE: 18.7,
			CAGR: 13.4,
			Divida: 0.72,
			Setor: "Industrial",
			Preco: 24.6,
		},
	];
}

function filterEliteStocks(stocks, minROE = 15, minCAGR = 12, maxPL = 15) {
	return stocks.filter(
		(stock) =>
			stock.ROE > minROE &&
			stock.CAGR > minCAGR &&
			stock.PL < maxPL &&
			stock.PL > 0,
	);
}

function calculateEfficiencyScore(stock) {
	if (stock.PL <= 0) return 0;
	return parseFloat(((stock.ROE + stock.CAGR) / stock.PL).toFixed(2));
}

function rankStocks(stocks) {
	return stocks
		.map((stock) => ({
			...stock,
			efficiency_score: calculateEfficiencyScore(stock),
		}))
		.sort((a, b) => b.efficiency_score - a.efficiency_score)
		.map((stock, index) => ({ ...stock, rank: index + 1 }));
}

function getMacroContext() {
	return {
		juros_selic: 10.75,
		inflacao_ipca: 4.5,
		setor_favorecido: ["Financeiro", "Energia", "Industrial"],
		setor_desfavorecido: ["Construção", "Consumo", "Varejo"],
		peso_ajuste: {
			Financeiro: 1.15,
			Energia: 1.08,
			Industrial: 1.05,
			Saúde: 1.02,
			Tecnologia: 0.95,
			Consumo: 0.88,
			Varejo: 0.85,
			Construção: 0.75,
		},
	};
}

function analyzeSentiment(ticker) {
	const currentMentions = 50 + Math.floor(Math.random() * 220) - 20;
	const ratio = currentMentions / 50;
	const riscoManada = ratio >= 3.0;

	return {
		ticker,
		volume_mencoes: currentMentions,
		media_historica: 50,
		ratio: parseFloat(ratio.toFixed(2)),
		risco_manada: riscoManada,
		recomendacao: riscoManada ? "ALERTA: Possível distribuição" : "Normal",
	};
}

function calculatePriceCeiling(stock) {
	const multiplier = 1 + stock.efficiency_score / 20;
	const fairValue = stock.Preco * multiplier;
	return parseFloat((fairValue / 1.2).toFixed(2));
}

function generateCatalysts(setor) {
	const catalysts = {
		Industrial: [
			"Expansão internacional em andamento",
			"Novos contratos com grandes clientes",
		],
		Financeiro: [
			"Melhoria na eficiência operacional",
			"Expansão da base de clientes",
		],
		Energia: [
			"Novos projetos de exploração",
			"Investimento em energias renováveis",
		],
		Tecnologia: [
			"Lançamento de novos produtos",
			"Expansão para novos mercados",
		],
		Varejo: ["Abertura de novas lojas", "Otimização da cadeia logística"],
		Saúde: [
			"Expansão da rede de atendimento",
			"Novos tratamentos e tecnologias",
		],
	};
	return catalysts[setor] || ["Crescimento orgânico"];
}

app.get("/", (req, res) => {
	res.json({
		message: "Alpha Terminal API",
		version: "1.0.0",
		status: "operational",
	});
});

app.get("/api/v1/top-picks", (req, res) => {
	try {
		const limit = parseInt(req.query.limit) || 15;
		const stocks = getDefaultStocks();
		const eliteStocks = filterEliteStocks(stocks);

		if (eliteStocks.length === 0) {
			return res
				.status(404)
				.json({ error: "Nenhum ativo passou pelos filtros" });
		}

		const rankedStocks = rankStocks(eliteStocks);
		const macroContext = getMacroContext();

		const topPicks = rankedStocks.slice(0, limit).map((stock) => {
			const sentiment = analyzeSentiment(stock.Ticker);
			const precoTeto = calculatePriceCeiling(stock);
			const upside = (precoTeto / stock.Preco - 1) * 100;
			const macroWeight = macroContext.peso_ajuste[stock.Setor] || 1.0;

			let recomendacao;
			if (sentiment.risco_manada) {
				recomendacao = "AGUARDAR - Risco de Manada";
			} else if (upside > 15) {
				recomendacao = "COMPRA FORTE";
			} else if (upside > 5) {
				recomendacao = "COMPRA";
			} else {
				recomendacao = "NEUTRO";
			}

			return {
				ticker: stock.Ticker,
				efficiency_score: stock.efficiency_score,
				macro_weight: macroWeight,
				catalisadores: generateCatalysts(stock.Setor),
				preco_teto: precoTeto,
				preco_atual: stock.Preco,
				upside_potencial: parseFloat(upside.toFixed(2)),
				sentiment_status: sentiment.risco_manada ? "Alerta" : "Normal",
				recomendacao_final: recomendacao,
				setor: stock.Setor,
				roe: stock.ROE,
				cagr: stock.CAGR,
				pl: stock.PL,
				tempo_estimado_dias: 90,
				rank: stock.rank,
				divida: stock.Divida,
				sentiment_ratio: sentiment.ratio,
			};
		});

		res.json(topPicks);
	} catch (error) {
		res.status(500).json({ error: error.message });
	}
});

app.get("/api/v1/macro-context", (req, res) => {
	res.json(getMacroContext());
});

app.get("/api/v1/sentiment/:ticker", (req, res) => {
	res.json(analyzeSentiment(req.params.ticker));
});

app.get("/api/v1/alerts", (req, res) => {
	try {
		const stocks = getDefaultStocks();
		const eliteStocks = filterEliteStocks(stocks);
		const rankedStocks = rankStocks(eliteStocks);

		const alerts = rankedStocks.slice(0, 10).map((stock) => {
			const precoTeto = calculatePriceCeiling(stock);
			const margem = (precoTeto / stock.Preco - 1) * 100;

			let acaoRecomendada;
			if (stock.Preco <= precoTeto * 0.95) {
				acaoRecomendada = "COMPRAR";
			} else if (stock.Preco <= precoTeto * 1.05) {
				acaoRecomendada = "AGUARDAR";
			} else {
				acaoRecomendada = "VENDER";
			}

			return {
				ticker: stock.Ticker,
				preco_atual: stock.Preco,
				preco_teto: precoTeto,
				margem_seguranca: parseFloat(margem.toFixed(2)),
				acao_recomendada: acaoRecomendada,
			};
		});

		res.json(alerts);
	} catch (error) {
		res.status(500).json({ error: error.message });
	}
});

app.listen(PORT, () => {
	console.log("");
	console.log("🚀 ========================================");
	console.log("   ALPHA TERMINAL API");
	console.log("========================================");
	console.log(`✅ Servidor rodando em http://localhost:${PORT}`);
	console.log(`📚 Top Picks: http://localhost:${PORT}/api/v1/top-picks`);
	console.log("========================================");
	console.log("");
});
