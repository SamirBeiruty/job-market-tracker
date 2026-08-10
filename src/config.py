from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "data" / "jobs.db"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
README_PATH = PROJECT_ROOT / "README.md"

API_URL = "https://remoteok.com/api"
USER_AGENT = "job-market-tracker (personal portfolio project)"

DATA_TAGS = {
    "data science",
    "data",
    "machine learning",
    "analytics",
    "python",
    "sql",
    "engineer",
    "ai",
}
