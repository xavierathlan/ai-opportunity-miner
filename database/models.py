from database.db import get_connection

# =========================
# CREATE TABLES
# =========================

def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================
    # COMPANIES
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS companies (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        plan TEXT DEFAULT 'free',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # =========================
    # USERS
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id INTEGER,

        name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password_hash TEXT NOT NULL,

        role TEXT DEFAULT 'viewer',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(company_id)
        REFERENCES companies(id)

    )

    """)

    # =========================
    # OPPORTUNITIES
    # =========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS opportunities (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id INTEGER,

        user_id INTEGER,

        problem TEXT,

        category TEXT,

        idea TEXT,

        score INTEGER,

        reason TEXT,

        saas TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(company_id)
        REFERENCES companies(id),

        FOREIGN KEY(user_id)
        REFERENCES users(id)

    )

    """)

    conn.commit()

    conn.close()