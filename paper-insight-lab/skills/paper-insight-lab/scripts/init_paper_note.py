#!/usr/bin/env python3
"""Create a new Markdown paper note from the bundled template."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "templates" / "paper-note.md"


def yaml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def split_values(value: str | None) -> list[str]:
    if not value:
        return []
    parts = re.split(r"[;,]", value)
    return [part.strip() for part in parts if part.strip()]


def yaml_list(values: list[str], default: str) -> str:
    items = values or [default]
    return "\n".join(f'  - "{yaml_escape(item)}"' for item in items)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_value).strip("-").lower()
    return slug[:80].strip("-")


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace("{{" + key + "}}", value)
    return content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize a Markdown note for a paper.")
    parser.add_argument("--title", required=True, help="Paper title")
    parser.add_argument("--authors", default="", help="Authors separated by semicolon or comma")
    parser.add_argument("--year", default="unknown", help="Publication year or unknown")
    parser.add_argument("--venue", default="unknown", help="Venue name")
    parser.add_argument("--doi", default="", help="DOI")
    parser.add_argument("--arxiv", default="", help="arXiv identifier")
    parser.add_argument("--url", default="", help="Paper URL")
    parser.add_argument("--tags", default="paper-reading", help="Tags separated by semicolon or comma")
    parser.add_argument("--status", default="unread", help="Reading status")
    parser.add_argument("--confidence", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--notes-dir", type=Path, default=Path("notes"), help="Output notes directory")
    parser.add_argument("--slug", help="Override generated note slug")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE, help="Template path")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing note")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    template_path = args.template.resolve()
    if not template_path.exists():
        print(f"[ERROR] Template not found: {template_path}", file=sys.stderr)
        return 2

    slug = args.slug or slugify(args.title)
    if not slug:
        slug = f"paper-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    notes_dir = args.notes_dir.resolve()
    output_path = notes_dir / f"{slug}.md"
    if output_path.exists() and not args.force:
        print(f"[ERROR] Note already exists: {output_path}. Use --force to overwrite.", file=sys.stderr)
        return 2

    year = args.year.strip() or "unknown"
    if year != "unknown" and not re.fullmatch(r"\d{4}", year):
        print("[ERROR] --year must be a four-digit year or unknown", file=sys.stderr)
        return 2

    replacements = {
        "title": yaml_escape(args.title.strip()),
        "authors_yaml": yaml_list(split_values(args.authors), "unknown"),
        "year": year,
        "venue": yaml_escape(args.venue.strip() or "unknown"),
        "doi": yaml_escape(args.doi.strip()),
        "arxiv": yaml_escape(args.arxiv.strip()),
        "url": yaml_escape(args.url.strip()),
        "tags_yaml": yaml_list(split_values(args.tags), "paper-reading"),
        "status": args.status.strip() or "unread",
        "confidence": args.confidence,
    }

    content = render_template(template_path.read_text(encoding="utf-8"), replacements)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"[OK] Created paper note: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
