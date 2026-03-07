#!/usr/bin/env python3
"""Backup Google Sheets tabs as local CSV files using the gws CLI.

Exports each tab from a Google Spreadsheet to a separate CSV file in the
specified output directory. Useful for creating accountant-ready backups.

Usage:
  python scripts/backup-sheets.py --spreadsheet-id SHEET_ID --output-dir ./backups
  python scripts/backup-sheets.py --spreadsheet-id SHEET_ID --output-dir ./backups --tabs "Sheet1,VAT-Period-1"
  python scripts/backup-sheets.py --help

Requires: gws CLI (npm install -g @google/gws) with valid authentication.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_gws(args: list[str]) -> str:
    """Run a gws CLI command and return stdout."""
    cmd = ["gws"] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            print(f"Error running gws: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        return result.stdout
    except FileNotFoundError:
        print("Error: gws CLI not found. Install with: npm install -g @google/gws", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("Error: gws command timed out after 60 seconds.", file=sys.stderr)
        sys.exit(1)


def export_tab(spreadsheet_id: str, tab_name: str, output_dir: Path) -> str:
    """Export a single sheet tab as CSV."""
    safe_name = tab_name.replace(" ", "_").replace("/", "-")
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = f"{safe_name}_{timestamp}.csv"
    output_path = output_dir / filename

    csv_data = run_gws([
        "sheets", "read",
        "--spreadsheet-id", spreadsheet_id,
        "--range", f"'{tab_name}'",
        "--output", "csv",
    ])

    output_path.write_text(csv_data, encoding="utf-8")
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Backup Google Sheets tabs as local CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  %(prog)s --spreadsheet-id abc123 --output-dir ./backups\n"
            "  %(prog)s --spreadsheet-id abc123 --output-dir ./backups --tabs 'Sheet1,Summary'\n"
        ),
    )
    parser.add_argument(
        "--spreadsheet-id",
        required=True,
        help="Google Spreadsheet ID (from the URL)",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory to save CSV files",
    )
    parser.add_argument(
        "--tabs",
        help="Comma-separated list of tab names to export (default: all)",
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.tabs:
        tab_names = [t.strip() for t in args.tabs.split(",")]
    else:
        tab_names = ["Sheet1"]
        print("No --tabs specified, defaulting to 'Sheet1'.", file=sys.stderr)
        print("Tip: specify tabs with --tabs 'Sheet1,VAT-Period-1,Summary'", file=sys.stderr)

    print(f"Backing up {len(tab_names)} tab(s) to: {output_dir}/")
    exported = []

    for tab in tab_names:
        try:
            path = export_tab(args.spreadsheet_id, tab, output_dir)
            exported.append(path)
            print(f"  Exported: {tab} -> {path}")
        except Exception as e:
            print(f"  Failed: {tab} - {e}", file=sys.stderr)

    print(f"\nBackup complete: {len(exported)}/{len(tab_names)} tabs exported.")


if __name__ == "__main__":
    main()
