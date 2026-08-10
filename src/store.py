from __future__ import annotations

import sqlite3
from datetime import date, timezone, datetime

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    date TEXT,
    position TEXT,
    company TEXT,
    location TEXT,
    salary_min INTEGER,
    salary_max INTEGER,
    tags TEXT,
    url TEXT,
    first_seen TEXT
)
"""


def connect(db_path=None) -> sqlite3.Connection:
    path = db_path or config.DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute(SCHEMA)
    return conn


def upsert(jobs: list[dict], db_path=None) -> int:
    conn = connect(db_path)
    today = datetime.now(timezone.utc).date().isoformat()
    added = 0
    with conn:
        for job in jobs:
            cur = conn.execute(
                """INSERT OR IGNORE INTO jobs
                   (id, date, position, company, location,
                    salary_min, salary_max, tags, url, first_seen)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    job["id"],
                    job["date"],
                    job["position"],
                    job["company"],
                    job["location"],
                    job["salary_min"],
                    job["salary_max"],
                    job["tags"],
                    job["url"],
                    today,
                ),
            )
            added += cur.rowcount
    conn.close()
    return added
