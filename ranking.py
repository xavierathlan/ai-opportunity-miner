import json

JSON_FILE = "data/opportunities.json"


def load_opportunities():

    try:

        with open(
            JSON_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def show_ranking():

    data = load_opportunities()

    if not data:

        print("\n❌ Nenhuma oportunidade encontrada.")
        return

    # ordena pelo score
    ranked = sorted(
        data,
        key=lambda x: x.get("score", 0),
        reverse=True
    )

    print("\n🏆 RANKING DE OPORTUNIDADES\n")

    for index, item in enumerate(ranked, start=1):

        print(f"\n#{index}")

        print(f"💡 IDEIA:")
        print(item.get("idea", "N/A"))

        print(f"\n🔥 SCORE:")
        print(item.get("score", 0))

        print(f"\n🧠 MOTIVO:")
        print(item.get("reason", "N/A"))

        print(f"\n🖥 SAAS:")
        print(item.get("saas", "N/A"))

        print("\n" + "=" * 40)


if __name__ == "__main__":
    show_ranking()