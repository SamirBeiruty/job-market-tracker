from src.fetch import normalize


def test_normalize_skips_non_job_items():
    raw = [
        {"legal": "terms of service blurb"},
        {"id": 123, "position": "Data Analyst", "tags": ["Data", " SQL "]},
    ]
    jobs = normalize(raw)
    assert len(jobs) == 1
    assert jobs[0]["id"] == "123"
    assert jobs[0]["tags"] == "data,sql"


def test_normalize_handles_missing_fields():
    jobs = normalize([{"id": 1}])
    job = jobs[0]
    assert job["position"] == ""
    assert job["salary_min"] == 0
    assert job["salary_max"] == 0
    assert job["tags"] == ""


def test_normalize_truncates_date():
    jobs = normalize([{"id": 1, "date": "2026-08-26T09:00:00+00:00"}])
    assert jobs[0]["date"] == "2026-08-26"
