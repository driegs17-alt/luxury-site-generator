#!/usr/bin/env python3
"""
Export collected leads (emails) to CSV for use in CRM or email campaigns.
Reads from leads/emails.json; creates the file with empty list if missing.
"""

import argparse
import csv
import json
from pathlib import Path
from typing import List

LEADS_DIR = Path(__file__).resolve().parent.parent / "leads"
DEFAULT_JSON = LEADS_DIR / "emails.json"


def load_emails(path: Path) -> List[dict]:
    """Load email entries from JSON. Each entry: at least {'email': str}, optional 'source', 'timestamp'."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_emails(path: Path, entries: List[dict]) -> None:
    """Save email entries to JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2), encoding="utf-8")


def export_csv(entries: List[dict], out_path: Path) -> None:
    """Write entries to CSV with columns email, source, timestamp."""
    if not entries:
        out_path.write_text("email,source,timestamp\n", encoding="utf-8")
        return
    keys = list(entries[0].keys()) if entries else ["email"]
    if "email" not in keys:
        keys.insert(0, "email")
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(entries)


def main() -> None:
    parser = argparse.ArgumentParser(description="Export lead emails to CSV for market growth and sales")
    parser.add_argument(
        "-i", "--input",
        default=str(DEFAULT_JSON),
        help="Input JSON file (default: leads/emails.json)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output CSV path (default: print to stdout or leads/emails.csv)",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create leads/emails.json with empty list if missing",
    )
    args = parser.parse_args()

    in_path = Path(args.input)
    if args.init:
        if not in_path.exists():
            save_emails(in_path, [])
            print(f"Created {in_path}")
        return

    entries = load_emails(in_path)
    if not entries:
        print("No leads found. Use --init to create leads/emails.json.")
        return

    out_path = Path(args.output) if args.output else in_path.with_suffix(".csv")
    export_csv(entries, out_path)
    print(f"Exported {len(entries)} leads to {out_path}")


if __name__ == "__main__":
    main()
