import sqlite3
import time

DB_PATH = "control_plane_metrics.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            latency_ms REAL,
            timestamp REAL
        )
    """)
    conn.commit()
    conn.close()


def record_request(model, latency_ms):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO requests (model, latency_ms, timestamp) VALUES (?, ?, ?)",
        (model, latency_ms, time.time())
    )
    conn.commit()
    conn.close()


def get_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT model,
               COUNT(*) as calls,
               AVG(latency_ms) as avg_latency
        FROM requests
        GROUP BY model
    """)
    rows = cursor.fetchall()
    conn.close()

    return {
        row[0]: {
            "calls": row[1],
            "avg_latency_ms": round(row[2], 2)
        }
        for row in rows
    }
