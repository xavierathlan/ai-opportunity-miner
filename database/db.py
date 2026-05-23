import sqlite3
import os

# =========================
# BASE DIR
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

# =========================
# DATA FOLDER
# =========================

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

# cria pasta data automaticamente
os.makedirs(DATA_DIR, exist_ok=True)

# =========================
# DATABASE FILE
# =========================

DATABASE_NAME = os.path.join(
    DATA_DIR,
    "database.db"
)

# =========================
# CONNECTION
# =========================

def get_connection():

    conn = sqlite3.connect(DATABASE_NAME)

    conn.row_factory = sqlite3.Row

    return conn