from . import fetch, report, store


def main() -> None:
    raw = fetch.fetch_raw()
    jobs = fetch.normalize(raw)
    added = store.upsert(jobs)
    print(f"fetched {len(jobs)} postings, {added} new")
    report.build()
    print("dashboard updated")


if __name__ == "__main__":
    main()
