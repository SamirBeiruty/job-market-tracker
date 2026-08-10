from __future__ import annotations

import requests

from . import config


def fetch_raw() -> list:
    resp = requests.get(
        config.API_URL, headers={"User-Agent": config.USER_AGENT}, timeout=30
    )
    resp.raise_for_status()
    return resp.json()


def normalize(raw: list) -> list[dict]:
    jobs = []
    for item in raw:
        if not isinstance(item, dict) or not item.get("id"):
            continue
        tags = [t.strip().lower() for t in (item.get("tags") or []) if t and t.strip()]
        jobs.append(
            {
                "id": str(item["id"]),
                "date": str(item.get("date") or "")[:10],
                "position": item.get("position") or "",
                "company": item.get("company") or "",
                "location": item.get("location") or "",
                "salary_min": int(item.get("salary_min") or 0),
                "salary_max": int(item.get("salary_max") or 0),
                "tags": ",".join(tags),
                "url": item.get("url") or "",
            }
        )
    return jobs
