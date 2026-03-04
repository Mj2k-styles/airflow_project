import os
import sqlite3

paths = [
    "/tmp/weather_data.db",
    "/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1/weather_data.db",
    "/mnt/c/Users/jmike/OneDrive/Desktop/airflow_project-1/votre_base.db",
]

for path in paths:
    print(f"\n--- {path}")
    exists = os.path.exists(path)
    print(f"exists: {exists}")
    if not exists:
        continue

    conn = sqlite3.connect(path)
    cur = conn.cursor()
    has_table = cur.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='weather_data'"
    ).fetchone()[0]
    print(f"weather_data table: {bool(has_table)}")

    if has_table:
        row_count = cur.execute("SELECT COUNT(*) FROM weather_data").fetchone()[0]
        print(f"rows: {row_count}")

    conn.close()
