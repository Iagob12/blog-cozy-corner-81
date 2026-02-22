"""
Serviço de Consenso — Executa análises múltiplas vezes

Executa Passo 1 (macro) e Passo 2 (triagem) 5 vezes cada
e consolida resultados para eliminar viés e escolhas aleatórias
"""
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from collections import Counter
import json
import os


class ConsensoService:
    """
    Executa análises múltiplas vezes e consolida resultados
    
    Features:
    - Passo 1: Análise macro 5x → Consolida setores/catalisadores
    - Passo 2: Triagem CSV 5x → Empresas que aparecem 3+ vezes
    - Elimina viés de execução única
    - Foca nas MELHORES empresas consistentemente
    """
    
    def __init__(self, ai_client):
        self.ai_client = ai_client
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        print("✓ Consenso Service inicializado")
    
    async def executar_passo1_consenso(
        self,
        num_execucoes: int = 1,  # 1 execução (sem consenso)
        min_aparicoes: int = 1   # 1 aparição
    ) -> Dict:
        """
        Executa Passo 1 (análise macro) múltiplas vezes
        
        Args:
            num_execucoes: Quantas vezes executar (padrão: 5)
            min_aparicoes: Mínimo de aparições para confirmar (padrão: 3)
        
        Returns:
            Análise macro consolidada
        """
        print(f"\n{'='*70}")
        print(f"PASSO 1 — ANÁLISE MACRO (CONSENSO {num_execucoes}x)")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        execucoes = []
        
        # Executa N vezes
        for i in range(num_execucoes):
            print(f"🔄 Execução {i+1}/{num_execucoes}...")
            
            # RETRY INFINITO até conseguir resposta
            tentativa = 0
            while True:
                tentativa += 1
                if tentativa > 1:
                    print(f"   🔄 Retry {tentativa} (não desiste até conseguir)...")
                
                try:
                    resultado = await self._executar_analise_macro()
                    if resultado:
                        execucoes.append(resultado)
                        print(f"   ✅ Sucesso!")
                        break  # Sucesso, sai do loop
                    else:
                        print(f"   ⚠️ Resposta vazia, retry em 5s...")
                        await asyncio.sleep(5)
                except Exception as e:
                    print(f"   ❌ Erro: {str(e)[:80]}")
                    print(f"   🔄 Retry em 5s...")
                    await asyncio.sleep(5)
            
            # Delay entre execuções (Gemini não tem rate limit agressivo)
            if i < num_execucoes - 1:
                print(f"   ⏳ Aguardando 3s antes da próxima execução...")
                await asyncio.sleep(3)
        
        if len(execucoes) < 1:  # Mínimo 1 execução
            print(f"\n❌ Nenhuma execução bem-sucedida")
            return None
        
        # Consolida resultados
        print(f"\n📊 Consolidando {len(execucoes)} execuções...")
        consolidado = self._consolidar_analise_macro(execucoes, min_aparicoes)
        
        # Salva cache
        self._salvar_cache_macro(consolidado)
        
        tempo = (datetime.now() - inicio).total_seconds()
        print(f"\n✅ Análise macro consolidada em {tempo:.1f}s")
        
        return consolidado

    
    async def executar_passo2_consenso(
        self,
        csv_path: str,
        contexto_macro: Dict,
        num_execucoes: int = 3,  # 3 execuções com consenso
        min_aparicoes: int = 2   # 2 aparições para aprovar
    ) -> List[str]:
        """
        Executa Passo 2 (triagem CSV) múltiplas vezes
        
        Args:
            csv_path: Caminho do CSV
            contexto_macro: Contexto da análise macro
            num_execucoes: Quantas vezes executar (padrão: 5)
            min_aparicoes: Mínimo de aparições para aprovar (padrão: 3)
        
        Returns:
            Lista de tickers aprovados (aparecem 3+ vezes)
        """
        print(f"\n{'='*70}")
        print(f"PASSO 2 — TRIAGEM CSV (CONSENSO {num_execucoes}x)")
        print(f"{'='*70}\n")
        
        inicio = datetime.now()
        execucoes = []
        
        # Executa N vezes
        for i in range(num_execucoes):
            print(f"🔄 Execução {i+1}/{num_execucoes}...")
            
            # RETRY INFINITO até conseguir resposta
            tentativa = 0
            while True:
                tentativa += 1
                if tentativa > 1:
                    print(f"   🔄 Retry {tentativa} (não desiste até conseguir)...")
                
                try:
                    resultado = await self._executar_triagem_csv(csv_path, contexto_macro)
                    if resultado:
                        execucoes.append(resultado)
                        print(f"   ✅ {len(resultado)} empresas selecionadas")
                        break  # Sucesso, sai do loop
                    else:
                        print(f"   ⚠️ Resposta vazia, retry em 30s...")
                        await asyncio.sleep(30)
                except Exception as e:
                    print(f"   ❌ Erro: {str(e)[:80]}")
                    print(f"   🔄 Retry em 30s...")
                    await asyncio.sleep(30)
            
            # Delay entre execuções
            if i < num_execucoes - 1:
                print(f"   ⏳ Aguardando 90s antes da próxima execução (chaves se recuperando)...")
                await asyncio.sleep(90)
        
        if len(execucoes) < 2:  # Mínimo 2 execuções para consenso
            print(f"\n❌ Poucas execuções bem-sucedidas ({len(execucoes)}/{num_execucoes})")
            return []
        
        # Consolida resultados
        print(f"\n📊 Consolidando {len(execucoes)} execuções...")
        empresas_aprovadas = self._consolidar_triagem_csv(execucoes, min_aparicoes)
        
        # Salva cache
        self._salvar_cache_empresas(empresas_aprovadas, execucoes)
        
        tempo = (datetime.now() - inicio).total_seconds()
        print(f"\n✅ {len(empresas_aprovadas)} empresas aprovadas em {tempo:.1f}s")
        
        return empresas_aprovadas
    
    async def _executar_analise_macro(self) -> Optional[Dict]:
        """Executa uma análise macro"""
        prompt = """Identifique 3 setores quentes para 2026.

Retorne JSON:
{
  "setores_quentes": ["Setor A", "Setor B", "Setor C"],
  "setores_evitar": ["Setor X", "Setor Y"]
}"""
        
        try:
            resposta = await self.ai_client.executar_prompt(
                prompt=prompt,
                task_type="analise_macro",
                usar_contexto=False  # Desabilita contexto
            )
            
            # Parse da resposta com tratamento robusto
            import json
            import re
            
            if isinstance(resposta, dict):
                # Se tem "resposta" dentro, extrai
                if "resposta" in resposta:
                    dados = resposta["resposta"]
                    
                    # Se resposta é string, faz parse do JSON
                    if isinstance(dados, str):
                        # Remove markdown code blocks
                        dados = re.sub(r'```json\s*', '', dados)
                        dados = re.sub(r'```\s*', '', dados)
                        dados = dados.strip()
                        
                        try:
                            dados = json.loads(dados)
                        except json.JSONDecodeError as e:
                            # Tenta extrair JSON do texto
                            match = re.search(r'\{.*\}', dados, re.DOTALL)
                            if match:
                                try:
                                    dados = json.loads(match.group(0))
                                except:
                                    print(f"      Erro JSON: {str(e)[:50]}")
                                    print(f"      Resposta: {dados[:150]}...")
                                    return None
                            else:
                                print(f"      Erro JSON: {str(e)[:50]}")
                                return None
                    
                    return dados if isinstance(dados, dict) else None
                
                # Se já é o dict direto, retorna
                return resposta
            
            # Se resposta é string, tenta parsear
            elif isinstance(resposta, str):
                # Remove markdown code blocks
                resposta = re.sub(r'```json\s*', '', resposta)
                resposta = re.sub(r'```\s*', '', resposta)
                resposta = resposta.strip()
                
                try:
                    return json.loads(resposta)
                except json.JSONDecodeError:
                    # Tenta extrair JSON do texto
                    match = re.search(r'\{.*\}', resposta, re.DOTALL)
                    if match:
                        try:
                            return json.loads(match.group(0))
                        except:
                            print(f"      Erro ao parsear JSON")
                            print(f"      Resposta: {resposta[:150]}...")
                            return None
            
            return None
        except Exception as e:
            print(f"      Erro: {e}")
            return None
    
    async def _executar_triagem_csv(
        self,
        csv_path: str,
        contexto_macro: Dict
    ) -> Optional[List[str]]:
        """Executa uma triagem do CSV"""
        import pandas as pd
        
        # Lê CSV com encoding correto para UTF-8 BOM
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        
        # TOP 30 empresas por ROE
        colunas_essenciais = ['ticker', 'roe', 'pl', 'cagr']
        df_reduzido = df[colunas_essenciais].copy()
        df_reduzido = df_reduzido[
            (df_reduzido['roe'] > 0) & 
            (df_reduzido['pl'] > 0) & 
            (df_reduzido['pl'] < 50)
        ]
        df_reduzido = df_reduzido.nlargest(30, 'roe')
        
        print(f"      CSV: {len(df)} → {len(df_reduzido)} empresas (TOP 30 ROE)")
        
        # Converte para formato mais limpo
        csv_texto = df_reduzido.to_csv(index=False, float_format='%.2f')
        
        # Prompt ULTRA MINIMALISTA
        prompt = f"""Analise o CSV e selecione TODAS as ações que atendem TODOS os critérios:

1. ROE maior que 15%
2. P/L entre 5 e 15
3. CAGR maior que 10%

CSV:
{csv_texto}

Retorne APENAS um JSON válido com a lista de tickers selecionados:
{{"empresas_selecionadas": ["TICK1", "TICK2", "TICK3"]}}

IMPORTANTE: Não limite a quantidade. Selecione TODAS que atendem os 3 critérios."""
        
        try:
            resposta = await self.ai_client.executar_prompt(
                prompt=prompt,
                task_type="triagem_csv",
                usar_contexto=False  # Desabilita contexto
            )
            
            # Parse da resposta com tratamento robusto
            import json
            import re
            
            if isinstance(resposta, dict):
                # Se tem "resposta" dentro, extrai
                if "resposta" in resposta:
                    dados = resposta["resposta"]
                    
                    # Se resposta é string, faz parse do JSON
                    if isinstance(dados, str):
                        # Remove markdown code blocks
                        dados = re.sub(r'```json\s*', '', dados)
                        dados = re.sub(r'```\s*', '', dados)
                        dados = dados.strip()
                        
                        try:
                            dados = json.loads(dados)
                        except json.JSONDecodeError as e:
                            # Tenta extrair JSON do texto
                            match = re.search(r'\{.*\}', dados, re.DOTALL)
                            if match:
                                try:
                                    dados = json.loads(match.group(0))
                                except:
                                    print(f"      Erro JSON: {str(e)[:50]}")
                                    print(f"      Resposta: {dados[:150]}...")
                                    return None
                            else:
                                print(f"      Erro JSON: {str(e)[:50]}")
                                return None
                else:
                    dados = resposta
                
                # Extrai empresas
                if isinstance(dados, dict):
                    empresas = dados.get("empresas_selecionadas", [])
                    return empresas if empresas else None
            
            # Se resposta é string, tenta parsear
            elif isinstance(resposta, str):
                # Remove markdown code blocks
                resposta = re.sub(r'```json\s*', '', resposta)
                resposta = re.sub(r'```\s*', '', resposta)
                resposta = resposta.strip()
                
                try:
                    dados = json.loads(resposta)
                    empresas = dados.get("empresas_selecionadas", [])
                    return empresas if empresas else None
                except json.JSONDecodeError:
                    # Tenta extrair JSON do texto
                    match = re.search(r'\{.*\}', resposta, re.DOTALL)
                    if match:
                        try:
                            dados = json.loads(match.group(0))
                            empresas = dados.get("empresas_selecionadas", [])
                            return empresas if empresas else None
                        except:
                            print(f"      Erro ao parsear JSON")
                            print(f"      Resposta: {resposta[:150]}...")
                            return None
            
            return None
        except Exception as e:
            print(f"      Erro: {e}")
            return None
    
    def _consolidar_analise_macro(
        self,
        execucoes: List[Dict],
        min_aparicoes: int
    ) -> Dict:
        """Consolida múltiplas análises macro"""
        
        # Conta aparições de setores
        setores_quentes_counter = Counter()
        setores_evitar_counter = Counter()
        catalisadores_counter = Counter()
        
        for exec in execucoes:
            for setor in exec.get("setores_quentes", []):
                setores_quentes_counter[setor] += 1
            
            for setor in exec.get("setores_evitar", []):
                setores_evitar_counter[setor] += 1
            
            for cat in exec.get("catalisadores", []):
                catalisadores_counter[cat] += 1
        
        # Filtra por mínimo de aparições
        setores_quentes = [
            setor for setor, count in setores_quentes_counter.items()
            if count >= min_aparicoes
        ]
        
        setores_evitar = [
            setor for setor, count in setores_evitar_counter.items()
            if count >= min_aparicoes
        ]
        
        catalisadores = [
            cat for cat, count in catalisadores_counter.items()
            if count >= min_aparicoes
        ]
        
        # Pega primeira megatendência (mais comum)
        megatendencias = []
        if execucoes:
            megatendencias = execucoes[0].get("megatendencias", [])
        
        return {
            "megatendencias": megatendencias,
            "setores_quentes": setores_quentes,
            "setores_evitar": setores_evitar,
            "catalisadores": catalisadores,
            "resumo_executivo": execucoes[0].get("resumo_executivo", ""),
            "num_execucoes": len(execucoes),
            "timestamp": datetime.now().isoformat()
        }
    
    def _consolidar_triagem_csv(
        self,
        execucoes: List[List[str]],
        min_aparicoes: int
    ) -> List[str]:
        """Consolida múltiplas triagens do CSV"""
        
        # Conta aparições de cada ticker
        ticker_counter = Counter()
        
        for empresas in execucoes:
            for ticker in empresas:
                ticker_counter[ticker] += 1
        
        # Filtra por mínimo de aparições
        empresas_aprovadas = [
            ticker for ticker, count in ticker_counter.items()
            if count >= min_aparicoes
        ]
        
        # Ordena por número de aparições (mais aparições = mais confiável)
        empresas_aprovadas.sort(
            key=lambda t: ticker_counter[t],
            reverse=True
        )
        
        # Mostra estatísticas
        print(f"\n📊 ESTATÍSTICAS DE CONSENSO:")
        for ticker in empresas_aprovadas[:10]:  # Top 10
            count = ticker_counter[ticker]
            pct = (count / len(execucoes)) * 100
            print(f"   {ticker}: {count}/{len(execucoes)} ({pct:.0f}%)")
        
        return empresas_aprovadas
    
    def _salvar_cache_macro(self, consolidado: Dict):
        """Salva cache da análise macro"""
        cache_path = os.path.join(self.cache_dir, "consenso_macro.json")
        
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(consolidado, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Cache macro salvo: {cache_path}")
    
    def _salvar_cache_empresas(
        self,
        empresas_aprovadas: List[str],
        execucoes: List[List[str]]
    ):
        """Salva cache das empresas aprovadas"""
        cache_path = os.path.join(self.cache_dir, "consenso_empresas.json")
        
        # Conta aparições
        ticker_counter = Counter()
        for empresas in execucoes:
            for ticker in empresas:
                ticker_counter[ticker] += 1
        
        dados = {
            "empresas_aprovadas": empresas_aprovadas,
            "estatisticas": {
                ticker: {
                    "aparicoes": count,
                    "percentual": (count / len(execucoes)) * 100
                }
                for ticker, count in ticker_counter.items()
                if count >= 3
            },
            "num_execucoes": len(execucoes),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Cache empresas salvo: {cache_path}")
    
    def carregar_cache_macro(self) -> Optional[Dict]:
        """Carrega cache da análise macro"""
        cache_path = os.path.join(self.cache_dir, "consenso_macro.json")
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        except:
            return None
    
    def carregar_cache_empresas(self) -> Optional[List[str]]:
        """Carrega cache das empresas aprovadas"""
        cache_path = os.path.join(self.cache_dir, "consenso_empresas.json")
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8-sig") as f:
                dados = json.load(f)
                return dados.get("empresas_aprovadas", [])
        except:
            return None


# Singleton
_consenso_service = None

def get_consenso_service(ai_client) -> ConsensoService:
    """Retorna instância singleton"""
    global _consenso_service
    if _consenso_service is None:
        _consenso_service = ConsensoService(ai_client)
    return _consenso_service
