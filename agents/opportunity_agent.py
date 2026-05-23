from openai import OpenAI
from dotenv import load_dotenv

import os

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# OPENAI CONFIG
# =========================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# =========================
# OPPORTUNITY AGENT
# =========================

class OpportunityAgent:

    def __init__(self):

        self.model = "gpt-4.1-mini"

    # =========================
    # ANALYZE OPPORTUNITY
    # =========================

    def analyze(self, market_problem):

        try:

            prompt = f"""
            Você é um especialista em:

            - startups
            - SaaS
            - inteligência de mercado
            - analytics
            - tendências digitais
            - oportunidades escaláveis

            Analise o problema abaixo:

            "{market_problem}"

            Retorne EXATAMENTE neste formato:

            category:
            idea:
            score:
            reason:
            saas:

            Regras:
            - score entre 0 e 10
            - foco em SaaS
            - foco em escalabilidade
            - resposta objetiva
            """

            response = client.chat.completions.create(

                model=self.model,

                messages=[

                    {
                        "role": "system",
                        "content": (
                            "Você é um analista especialista "
                            "em oportunidades SaaS."
                        )
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ],

                temperature=0.7

            )

            content = response.choices[0].message.content

            # =========================
            # RESULT STRUCTURE
            # =========================

            result = {

                "category": "",
                "idea": "",
                "score": 0,
                "reason": "",
                "saas": ""

            }

            # =========================
            # PARSE RESPONSE
            # =========================

            lines = content.split("\n")

            for line in lines:

                line = line.strip()

                # CATEGORY
                if line.lower().startswith("category:"):

                    result["category"] = (

                        line.replace(
                            "category:",
                            ""
                        ).strip()

                    )

                # IDEA
                elif line.lower().startswith("idea:"):

                    result["idea"] = (

                        line.replace(
                            "idea:",
                            ""
                        ).strip()

                    )

                # SCORE
                elif line.lower().startswith("score:"):

                    score_text = (

                        line.replace(
                            "score:",
                            ""
                        ).strip()

                    )

                    try:

                        result["score"] = int(
                            float(score_text)
                        )

                    except:

                        result["score"] = 0

                # REASON
                elif line.lower().startswith("reason:"):

                    result["reason"] = (

                        line.replace(
                            "reason:",
                            ""
                        ).strip()

                    )

                # SAAS
                elif line.lower().startswith("saas:"):

                    result["saas"] = (

                        line.replace(
                            "saas:",
                            ""
                        ).strip()

                    )

            # =========================
            # FALLBACK VALIDATION
            # =========================

            if result["idea"] == "":

                result["idea"] = (
                    "Sistema inteligente "
                    "de análise de oportunidades"
                )

            if result["category"] == "":

                result["category"] = "Tendências"

            return result

        except Exception as error:

            print("\n❌ ERRO OPENAI\n")

            print(error)

            # =========================
            # FALLBACK RESPONSE
            # =========================

            return {

                "category": "Tendências",

                "idea": (
                    "Sistema inteligente "
                    "de análise de mercado"
                ),

                "score": 5,

                "reason": (
                    "Fallback automático ativado "
                    "devido a erro na OpenAI."
                ),

                "saas": (
                    "Plataforma SaaS "
                    "de analytics inteligente"
                )

            }