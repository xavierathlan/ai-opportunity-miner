from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# =========================
# LOAD ENV
# =========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

# =========================
# AGENTE
# =========================

class OpportunityAgent:

    def analyze(self, text):

        prompt = f"""
Você é um especialista em oportunidades de negócios.

Analise o problema abaixo.

Responda APENAS em JSON válido.

Formato obrigatório:

{{
  "category": "...",
  "idea": "...",
  "score": 0,
  "reason": "...",
  "saas": "..."
}}

Problema:
{text}
"""

        try:

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7
            )

            content = response.choices[0].message.content

            return json.loads(content)

        except Exception:

            return self.local_analysis(text)

    # =========================
    # FALLBACK LOCAL
    # =========================

    def local_analysis(self, text):

        text = text.lower()

        # =========================
        # RETAIL
        # =========================

        if (
            "mercado" in text or
            "supermercado" in text or
            "preço" in text or
            "compras" in text
        ):

            return {

                "category": "Retail",

                "idea": (
                    "Plataforma inteligente de "
                    "comparação de preços locais"
                ),

                "score": 8,

                "reason": (
                    "Consumidores buscam economia e "
                    "pequenos mercados possuem "
                    "dificuldade competitiva."
                ),

                "saas": (
                    "Sistema SaaS de inteligência "
                    "de preços regionais"
                )
            }

        # =========================
        # HEALTHTECH
        # =========================

        elif (
            "farmácia" in text or
            "hospital" in text or
            "consulta" in text or
            "clínica" in text
        ):

            return {

                "category": "HealthTech",

                "idea": (
                    "Sistema automatizado de "
                    "captação de pacientes"
                ),

                "score": 8,

                "reason": (
                    "Clínicas e farmácias possuem "
                    "baixa presença digital."
                ),

                "saas": (
                    "CRM SaaS para saúde"
                )
            }

        # =========================
        # FOODTECH
        # =========================

        elif (
            "restaurante" in text or
            "delivery" in text or
            "comida" in text or
            "lanche" in text
        ):

            return {

                "category": "FoodTech",

                "idea": (
                    "Sistema de fidelização e "
                    "promoções inteligentes"
                ),

                "score": 9,

                "reason": (
                    "Restaurantes possuem dificuldade "
                    "em retenção de clientes."
                ),

                "saas": (
                    "Plataforma SaaS para retenção "
                    "e campanhas"
                )
            }

        # =========================
        # AI
        # =========================

        elif (
            "ia" in text or
            "inteligência artificial" in text or
            "automação" in text
        ):

            return {

                "category": "AI",

                "idea": (
                    "Sistema automatizado de "
                    "análise e produtividade"
                ),

                "score": 10,

                "reason": (
                    "Empresas buscam automação "
                    "e redução de custos."
                ),

                "saas": (
                    "Plataforma de automação com IA"
                )
            }

        # =========================
        # FALLBACK
        # =========================

        else:

            return {

                "category": "General",

                "idea": (
                    "Necessário coletar mais dados "
                    "sobre o problema"
                ),

                "score": 5,

                "reason": (
                    "Poucos sinais detectados."
                ),

                "saas": (
                    "Sistema de análise de tendências"
                )
            }