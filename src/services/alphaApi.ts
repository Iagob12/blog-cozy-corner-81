const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export interface TopPick {
	ticker: string;
	efficiency_score: number;
	macro_weight: number;
	catalisadores: string[];
	preco_teto: number;
	preco_atual: number | null;
	upside_potencial: number;
	sentiment_status: string;
	recomendacao_final: string;
	setor: string | null;
	roe: number;
	cagr: number;
	pl: number;
	tempo_estimado_dias: number;
	sentiment_ratio?: number;
	variacao_30d?: number;
	rank?: number;
}

export interface RankingAtual {
	timestamp: string;
	total_aprovadas: number;
	ranking: TopPick[];
	versao: string;
}

export interface EstrategiaAlerta {
	ticker: string;
	tipo: 'OPORTUNIDADE' | 'STOP' | 'ALVO' | 'AGUARDAR';
	preco_atual: number;
	preco_entrada: number;
	preco_stop: number;
	preco_alvo: number;
	mensagem: string;
	timestamp: string;
}

export interface ConfigSistema {
	versao: string;
	ultima_atualizacao: string;
	scheduler_estrategia: {
		ativo: boolean;
		intervalo_minutos: number;
		auto_start: boolean;
	};
	analise: {
		usar_consenso_padrao: boolean;
		num_execucoes_consenso: number;
		min_aparicoes_consenso: number;
	};
	cache_precos: {
		ativo: boolean;
		tempo_expiracao_horas: number;
		usar_fallback: boolean;
	};
	notas_estruturadas: {
		ativo: boolean;
		divergencia_maxima: number;
		pesos: {
			fundamentos: number;
			catalisadores: number;
			valuation: number;
			gestao: number;
		};
	};
}

export interface CacheStats {
	total: number;
	atualizados: number;
	recentes: number;
	antigos: number;
}

class AlphaAPI {
	private baseUrl: string;
	private token: string | null = null;

	constructor(baseUrl: string = API_BASE_URL) {
		this.baseUrl = baseUrl;
		// Tenta carregar token do localStorage
		this.token = localStorage.getItem('admin_token');
	}

	setToken(token: string) {
		this.token = token;
		localStorage.setItem('admin_token', token);
	}

	clearToken() {
		this.token = null;
		localStorage.removeItem('admin_token');
	}

	private getHeaders(): HeadersInit {
		const headers: HeadersInit = {
			'Content-Type': 'application/json',
		};
		if (this.token) {
			headers['Authorization'] = `Bearer ${this.token}`;
		}
		return headers;
	}

	// ===== RANKING =====
	async getRankingAtual(): Promise<RankingAtual> {
		// Usa endpoint público (sem autenticação)
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/ranking-publico`
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar ranking");
		}
		return response.json();
	}

	// ===== ANÁLISE =====
	async iniciarAnalise(usarConsenso: boolean = true): Promise<{ mensagem: string; tempo_estimado: string; detalhes: string }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/iniciar-analise?usar_consenso=${usarConsenso}`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao iniciar análise");
		}
		return response.json();
	}

	async getStatusAnalise(): Promise<any> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/status`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar status");
		}
		return response.json();
	}

	// ===== ESTRATÉGIA DINÂMICA =====
	async getAlertasEstrategia(limite: number = 50): Promise<EstrategiaAlerta[]> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia/alertas?limite=${limite}`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar alertas");
		}
		const data = await response.json();
		return data.alertas || [];
	}

	async atualizarEstrategias(): Promise<{ success: boolean; total_atualizadas: number }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia/atualizar`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao atualizar estratégias");
		}
		return response.json();
	}

	async getHistoricoEstrategia(ticker: string, limite: number = 10): Promise<any[]> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia/historico/${ticker}?limite=${limite}`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar histórico");
		}
		const data = await response.json();
		return data.historico || [];
	}

	// ===== SCHEDULER =====
	async iniciarScheduler(): Promise<{ success: boolean; message: string }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia-scheduler/iniciar`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao iniciar scheduler");
		}
		return response.json();
	}

	async pararScheduler(): Promise<{ success: boolean; message: string }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia-scheduler/parar`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao parar scheduler");
		}
		return response.json();
	}

	async getStatusScheduler(): Promise<any> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/estrategia-scheduler/status`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar status do scheduler");
		}
		return response.json();
	}

	// ===== CONFIGURAÇÕES =====
	async getConfig(): Promise<ConfigSistema> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/config`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar configurações");
		}
		const data = await response.json();
		return data.config;
	}

	async getConfigSecao(secao: string): Promise<any> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/config/${secao}`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar seção");
		}
		const data = await response.json();
		return data.config;
	}

	async atualizarConfig(chave: string, valor: any): Promise<{ success: boolean; novo_valor: any }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/config`,
			{
				method: 'PUT',
				headers: this.getHeaders(),
				body: JSON.stringify({ chave, valor })
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao atualizar configuração");
		}
		return response.json();
	}

	async resetarConfig(): Promise<{ success: boolean; config: ConfigSistema }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/config/resetar`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao resetar configurações");
		}
		return response.json();
	}

	// ===== CACHE DE PREÇOS =====
	async getCacheStats(): Promise<CacheStats> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/precos-cache/stats`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao buscar stats do cache");
		}
		const data = await response.json();
		return data.estatisticas;
	}

	async limparCache(maxDias: number = 7): Promise<{ success: boolean; removidos: number }> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/precos-cache/limpar?max_dias=${maxDias}`,
			{
				method: 'POST',
				headers: this.getHeaders()
			}
		);
		if (!response.ok) {
			throw new Error("Erro ao limpar cache");
		}
		return response.json();
	}

	// ===== NOTAS ESTRUTURADAS =====
	async calcularNota(ticker: string): Promise<any> {
		const response = await fetch(
			`${this.baseUrl}/api/v1/admin/notas-estruturadas/calcular/${ticker}`,
			{ headers: this.getHeaders() }
		);
		if (!response.ok) {
			throw new Error("Erro ao calcular nota");
		}
		return response.json();
	}
}

export const alphaApi = new AlphaAPI();
