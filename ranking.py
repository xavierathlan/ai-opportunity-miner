import sqlite3
import pandas as pd

# =========================
# DATABASE
# =========================

DATABASE = "data/database.db"

# =========================
# GET RANKING
# =========================

def get_ranking():

    conn = sqlite3.connect(DATABASE)

    query = """

    SELECT
        idea,
        category,
        score,
        saas,
        created_at

    FROM opportunities

    ORDER BY score DESC

    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df

# =========================
# MAIN
# =========================

if __name__ == "__main__":

    ranking = get_ranking()

    print("\n🏆 RANKING DE OPORTUNIDADES\n")

    print(ranking)