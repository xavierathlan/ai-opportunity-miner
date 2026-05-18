from agents.opportunity_agent import OpportunityAgent

import csv
import json
import os

CSV_FILE = "data/history.csv"
JSON_FILE = "data/opportunities.json"

agent = OpportunityAgent()

# =========================
# SALVAR CSV
# =========================

def save_csv(problem, result):

    file_exists = os.path.isfile(CSV_FILE)

    with open(
        CSV_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        if not file_exists or os.path.getsize(CSV_FILE) == 0:

            writer.writerow([
                "problem",
                "category",
                "idea",
                "score",
                "reason",
                "saas"
            ])

        writer.writerow([
            problem,
            result.get("category", ""),
            result.get("idea", ""),
            result.get("score", ""),
            result.get("reason", ""),
            result.get("saas", "")
        ])


# =========================
# SALVAR JSON
# =========================

def save_json(problem, result):

    data = []

    if os.path.exists(JSON_FILE):

        try:

            with open(
                JSON_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except Exception:

            data = []

    data.append({

        "problem": problem,
        "category": result.get("category", ""),
        "idea": result.get("idea", ""),
        "score": result.get("score", ""),
        "reason": result.get("reason", ""),
        "saas": result.get("saas", "")

    })

    with open(
        JSON_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================
# MAIN
# =========================

def main():

    print("\n🚀 AI Opportunity Miner\n")

    while True:

        text = input(
            "\nDigite um problema de mercado (ou 'sair'):\n> "
        )

        if text.lower() == "sair":

            print("\n👋 Encerrando sistema...")
            break

        result = agent.analyze(text)

        print("\n📊 ANÁLISE DA IA\n")

        if isinstance(result, dict):

            print(f"🏷 CATEGORIA:\n{result.get('category', '')}")

            print(f"\n💡 IDEIA:\n{result.get('idea', '')}")

            print(f"\n🔥 SCORE:\n{result.get('score', '')}")

            print(f"\n🧠 MOTIVO:\n{result.get('reason', '')}")

            print(f"\n🖥 SAAS:\n{result.get('saas', '')}")

            save_csv(text, result)
            save_json(text, result)

            print("\n💾 Dados salvos com sucesso!")

        else:

            print("\n❌ Erro na resposta da IA:")
            print(result)


if __name__ == "__main__":
    main()