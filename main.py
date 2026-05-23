from agents.opportunity_agent import OpportunityAgent

import sqlite3
import os

# =========================
# DATABASE
# =========================

DATABASE = "data/database.db"

os.makedirs("data", exist_ok=True)

# =========================
# CREATE DATABASE
# =========================

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS opportunities (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    problem TEXT,

    category TEXT,

    idea TEXT,

    score INTEGER,

    reason TEXT,

    saas TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)

""")

conn.commit()

conn.close()

# =========================
# AGENT
# =========================

agent = OpportunityAgent()

# =========================
# SAVE OPPORTUNITY
# =========================

def save_opportunity(problem, result):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO opportunities (

        problem,
        category,
        idea,
        score,
        reason,
        saas

    )

    VALUES (?, ?, ?, ?, ?, ?)

    """, (

        problem,

        result["category"],
        result["idea"],
        result["score"],
        result["reason"],
        result["saas"]

    ))

    conn.commit()

    conn.close()

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

        print("\n📊 ANÁLISE\n")

        print(f"🏷 Categoria:\n{result['category']}")

        print(f"\n💡 IDEIA:\n{result['idea']}")

        print(f"\n🔥 SCORE:\n{result['score']}")

        print(f"\n🧠 MOTIVO:\n{result['reason']}")

        print(f"\n🖥 SAAS:\n{result['saas']}")

        save_opportunity(text, result)

        print("\n💾 Oportunidade salva!")

if __name__ == "__main__":
    main()