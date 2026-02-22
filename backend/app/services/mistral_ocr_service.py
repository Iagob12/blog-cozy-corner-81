"""
Mistral AI Document OCR Service
Extrai dados de relatórios trimestrais em PDF usando Mistral AI
"""
import aiohttp
import os
from typing import Dict, Optional
import base64

class MistralOCRService:
    """Serviço para extrair dados de PDFs usando Mistral AI"""
    
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        self.base_url = "https://api.mistral.ai/v1"
        
        print(f"✓ Mistral AI OCR configurado")
    
    async def extrair_dados_relatorio_trimestral(
        self, 
        pdf_path: str,
        ticker: str
    ) -> Dict:
        """
        Extrai dados financeiros de um relatório trimestral em PDF
        
        Dados extraídos:
        - Receita líquida
        - Lucro líquido
        - EBITDA
        - Margem líquida
        - Margem EBITDA
        - Crescimento YoY
        - Destaques do trimestre
        """
        
        try:
            # Lê o PDF e converte para base64
            with open(pdf_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode('utf-8')
            
            # Prompt para extração estruturada
            prompt = f"""Analise este relatório trimestral da empresa {ticker} e extraia os seguintes dados financeiros:

DADOS OBRIGATÓRIOS:
1. Receita Líquida (em milhões de R$)
2. Lucro Líquido (em milhões de R$)
3. EBITDA (em milhões de R$)
4. Margem Líquida (%)
5. Margem EBITDA (%)
6. Crescimento da Receita YoY (%)
7. Crescimento do Lucro YoY (%)

ANÁLISE QUALITATIVA:
8. Principais destaques do trimestre
9. Riscos mencionados
10. Guidance/Perspectivas

FORMATO DE RESPOSTA (JSON):
{{
    "ticker": "{ticker}",
    "trimestre": "Q4 2025",
    "receita_liquida": 1500.5,
    "lucro_liquido": 250.3,
    "ebitda": 450.2,
    "margem_liquida": 16.7,
    "margem_ebitda": 30.0,
    "crescimento_receita_yoy": 15.2,
    "crescimento_lucro_yoy": 20.5,
    "destaques": [
        "Expansão de margens",
        "Redução de custos operacionais"
    ],
    "riscos": [
        "Volatilidade cambial",
        "Aumento de juros"
    ],
    "guidance": "Empresa espera crescimento de 10-15% em 2026"
}}

Seja preciso e extraia apenas dados que estão explicitamente no documento."""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "pixtral-large-latest",  # Modelo com visão para PDFs
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:application/pdf;base64,{pdf_content}"
                            }
                        ]
                    }
                ],
                "temperature": 0.1,  # Muito conservador para extração
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content = data["choices"][0]["message"]["content"]
                        
                        # Tenta extrair JSON da resposta
                        import json
                        if "```json" in content:
                            content = content.split("```json")[1].split("```")[0]
                        elif "```" in content:
                            content = content.split("```")[1].split("```")[0]
                        
                        dados_extraidos = json.loads(content.strip())
                        
                        print(f"✓ Dados extraídos de {ticker}")
                        return {
                            "success": True,
                            "dados": dados_extraidos,
                            "fonte": "Mistral AI OCR"
                        }
                    else:
                        error_text = await response.text()
                        print(f"Erro Mistral AI ({response.status}): {error_text}")
                        return {"success": False, "error": error_text}
        
        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return {"success": False, "error": str(e)}
    
    async def extrair_texto_completo_pdf(self, pdf_path: str) -> Optional[str]:
        """
        Extrai todo o texto de um PDF usando OCR
        Útil para análise posterior com outras IAs
        """
        
        try:
            with open(pdf_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode('utf-8')
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "pixtral-large-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extraia todo o texto deste documento PDF. Mantenha a estrutura e formatação."
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:application/pdf;base64,{pdf_content}"
                            }
                        ]
                    }
                ],
                "temperature": 0.0,
                "max_tokens": 4000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        texto = data["choices"][0]["message"]["content"]
                        return texto
                    else:
                        return None
        
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
            return None
    
    async def analisar_relatorio_com_ia(
        self,
        pdf_path: str,
        ticker: str,
        perguntas: list[str]
    ) -> Dict:
        """
        Faz perguntas específicas sobre um relatório trimestral
        
        Exemplo:
        perguntas = [
            "Qual foi o crescimento da receita?",
            "A empresa está reduzindo custos?",
            "Quais são os principais riscos?"
        ]
        """
        
        try:
            with open(pdf_path, 'rb') as f:
                pdf_content = base64.b64encode(f.read()).decode('utf-8')
            
            perguntas_texto = "\n".join([f"{i+1}. {p}" for i, p in enumerate(perguntas)])
            
            prompt = f"""Analise este relatório trimestral de {ticker} e responda as seguintes perguntas:

{perguntas_texto}

Seja objetivo e baseie suas respostas apenas no que está explícito no documento."""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "pixtral-large-latest",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": f"data:application/pdf;base64,{pdf_content}"
                            }
                        ]
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        respostas = data["choices"][0]["message"]["content"]
                        
                        return {
                            "success": True,
                            "ticker": ticker,
                            "perguntas": perguntas,
                            "respostas": respostas
                        }
                    else:
                        error_text = await response.text()
                        return {"success": False, "error": error_text}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
