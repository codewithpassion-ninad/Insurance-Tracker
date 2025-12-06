import os
import sqlite3
import pandas as pd
from typing import Dict, Any

DB_PATH = "data/employee.db"
CSV_PATH = "data/claims_dataset_v3.csv"


def init_employee_db(csv_path: str = CSV_PATH) -> bool:
    """Creates the SQLite DB from CSV."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    print("🔄 Creating employee database from CSV...")

    df = pd.read_csv(csv_path)

    # Use claim_id as key
    required_cols = {"claim_id"}

    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")

    # Create folder if missing
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    df.to_sql("employees", conn, if_exists="replace", index=False)
    conn.close()

    print("✅ Employee DB created at:", DB_PATH)
    return True


def ensure_db_ready():
    """Auto-create DB if missing."""
    if not os.path.exists(DB_PATH):
        print("⚠️ employee.db not found. Auto-generating...")
        init_employee_db()


def is_valid_employee(employee_id: str) -> Dict[str, Any]:
    ensure_db_ready()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE claim_id = ?", (employee_id,))
    row = cur.fetchone()
    conn.close()

    if row:
        record = _convert_row_to_dict(row)
        return {"valid": True, "record": record}

    return {"valid": False, "reason": "not_found"}

def _convert_row_to_dict(row_tuple):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(employees)")
    cols = [c[1] for c in cur.fetchall()]
    conn.close()
    return dict(zip(cols, row_tuple))