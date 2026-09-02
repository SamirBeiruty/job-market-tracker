from __future__ import annotations

from datetime import datetime, timezone

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from . import config, store

START = "<!-- dashboard:start -->"
END = "<!-- dashboard:end -->"


def load(db_path=None) -> pd.DataFrame:
    conn = store.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


def is_data_job(tags: str) -> bool:
    return bool(set(tags.split(",")) & config.DATA_TAGS)


def save_postings_chart(df: pd.DataFrame) -> None:
    dated = df[df["date"] != ""].copy()
    dated["week"] = pd.to_datetime(dated["date"]).dt.to_period("W").dt.start_time
    counts = dated.groupby("week").size()
    fig, ax = plt.subplots(figsize=(9, 4))
    counts.plot(ax=ax, marker="o", color="#16324f")
    ax.set_title("Postings tracked per week")
    ax.set_xlabel("")
    ax.set_ylabel("postings")
    fig.tight_layout()
    fig.savefig(config.FIGURES_DIR / "postings_per_week.png", dpi=120)
    plt.close(fig)


def save_tags_chart(df: pd.DataFrame) -> None:
    tags = df["tags"].str.split(",").explode()
    top = tags[tags != ""].value_counts().head(15).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    top.plot(kind="barh", ax=ax, color="#16324f")
    ax.set_title("Most common tags across tracked postings")
    ax.set_xlabel("postings")
    fig.tight_layout()
    fig.savefig(config.FIGURES_DIR / "top_tags.png", dpi=120)
    plt.close(fig)


def stats(df: pd.DataFrame) -> dict:
    today = datetime.now(timezone.utc).date().isoformat()
    return {
        "total": len(df),
        "companies": df["company"].nunique(),
        "new_today": int((df["first_seen"] == today).sum()),
        "data_share": df["tags"].apply(is_data_job).mean() if len(df) else 0.0,
    }


def render_dashboard(s: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        START,
        f"*Last updated: {now}*",
        "",
        "| | |",
        "|---|---|",
        f"| Postings tracked | {s['total']:,} |",
        f"| Companies | {s['companies']:,} |",
        f"| New since last run | {s['new_today']:,} |",
        f"| Data/ML-related share | {s['data_share']:.0%} |",
        "",
        "![Postings per week](reports/figures/postings_per_week.png)",
        "",
        "![Top tags](reports/figures/top_tags.png)",
        END,
    ]
    return "\n".join(lines)


def update_readme(dashboard: str) -> None:
    text = config.README_PATH.read_text()
    before = text.split(START)[0]
    after = text.split(END)[1]
    config.README_PATH.write_text(before + dashboard + after)


def build(db_path=None) -> None:
    config.FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = load(db_path)
    save_postings_chart(df)
    save_tags_chart(df)
    update_readme(render_dashboard(stats(df)))
