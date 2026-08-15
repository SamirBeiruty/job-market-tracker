from src.store import connect, upsert


def make_job(job_id, position="Engineer"):
    return {
        "id": str(job_id),
        "date": "2026-08-26",
        "position": position,
        "company": "Acme",
        "location": "Remote",
        "salary_min": 0,
        "salary_max": 0,
        "tags": "python",
        "url": "https://example.com",
    }


def test_upsert_inserts_new_jobs(tmp_path):
    db = tmp_path / "test.db"
    added = upsert([make_job(1), make_job(2)], db_path=db)
    assert added == 2


def test_upsert_ignores_duplicates(tmp_path):
    db = tmp_path / "test.db"
    upsert([make_job(1)], db_path=db)
    added = upsert([make_job(1), make_job(2)], db_path=db)
    assert added == 1
    conn = connect(db)
    count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    conn.close()
    assert count == 2


def test_duplicate_does_not_overwrite_first_seen(tmp_path):
    db = tmp_path / "test.db"
    upsert([make_job(1)], db_path=db)
    conn = connect(db)
    conn.execute("UPDATE jobs SET first_seen = '2020-01-01'")
    conn.commit()
    conn.close()
    upsert([make_job(1)], db_path=db)
    conn = connect(db)
    first_seen = conn.execute("SELECT first_seen FROM jobs WHERE id = '1'").fetchone()[0]
    conn.close()
    assert first_seen == "2020-01-01"
