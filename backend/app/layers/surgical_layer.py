import google.generativeai as genai
import PyPDF2
import os
from typing import List
from app.models import PDFAnalysis, Catalisador

class SurgicalLayer:
    """Camada 3: Análise Cirúrgica com IA"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extrai texto do PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            raise Exception(f"Erro ao ler PDF: {str(e)}")
        return text
    
    def build_analysis_prompt(self, text: str, ticker: str) -> str:
        """Constrói o prompt para a IA"""
        prompt = f"""
Você é um analista quantitativo especializado em identificar catalisadores de valor.

Analise o relatório de RI da empresa {ticker} e retorne APENAS um JSON válido:

{{
  "catalisadores": [
    {{
      "tipo": "expansao|novo_contrato|alavancagem_operacional|inovacao",
      "descricao": "descrição objetiva",
      "impacto_estimado": "alto|medio|baixo"
    }}
  ],
  "tese_qualitativa": "resumo em 2-3 frases",
  "score_qualitativo": 7.5,
  "alerta_dividendo_trap": false
}}

CRITÉRIOS:
1. Busque: expansão, novos contratos, alavancagem operacional, inovação
2. IGNORE teses baseadas apenas em dividendos
3. Se só fala de dividendos sem crescimento, marque alerta_dividendo_trap como true
4. Score de 0 a 10 baseado na força dos catalisadores
5. Retorne APENAS o JSON

TEXTO:
{text[:8000]}
"""
        return prompt
    
    async def analyze_with_gemini(self, text: str, ticker: str) -> dict:
        """Envia para a Gemini API"""
        if not self.api_key:
            return {
                "catalisadores": [],
                "tese_qualitativa": "Configure GEMINI_API_KEY",
                "score_qualitativo": 5.0,
                "alerta_dividendo_trap": False
            }
        
        try:
            prompt = self.build_analysis_prompt(text, ticker)
            response = self.model.generate_content(prompt)
            
            response_text = response.text.strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            import json
            analysis = json.loads(response_text.strip())
            return analysis
            
        except Exception as e:
            print(f"Erro na análise Gemini: {e}")
            return {
                "catalisadores": [],
                "tese_qualitativa": f"Erro: {str(e)}",
                "score_qualitativo": 0.0,
                "alerta_dividendo_trap": False
            }
    
    async def process(self, pdf_path: str, ticker: str) -> PDFAnalysis:
        """Pipeline completo da Camada 3"""
        text = self.extract_text_from_pdf(pdf_path)
        analysis_data = await self.analyze_with_gemini(text, ticker)
        
        catalisadores = [
            Catalisador(**cat) for cat in analysis_data.get("catalisadores", [])
        ]
        
        return PDFAnalysis(
            ticker=ticker,
            catalisadores=catalisadores,
            tese_qualitativa=analysis_data.get("tese_qualitativa", ""),
            score_qualitativo=analysis_data.get("score_qualitativo", 0.0),
            alerta_dividendo_trap=analysis_data.get("alerta_dividendo_trap", False)
        )
