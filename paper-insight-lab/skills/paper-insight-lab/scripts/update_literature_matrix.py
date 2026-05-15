#!/usr/bin/env python3
"""Generate a Markdown literature matrix from Paper Insight Lab notes."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}

    raw = text[4:end].splitlines()
    data: dict[str, Any] = {}
    current_list: str | None = None
    for line in raw:
        if not line.strip():
            continue
        if line.startswith("  - ") and current_list:
            data.setdefault(current_list, []).append(unquote(line[4:].strip()))
            continue
        current_list = None
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_list = key
        else:
            data[key] = unquote(value)
    return data


def section_text(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(?P<body>.*?)(?=^##\s+|\Z)"
    )
    match = pattern.search(text)
    if not match:
        return ""
    return match.group("body").strip()


def compact_section(text: str, max_items: int = 2) -> str:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("|") or line.startswith("###"):
            continue
        line = re.sub(r"^[-*]\s+", "", line)
        if line and line.upper() != "TODO":
            lines.append(line)
        if len(lines) >= max_items:
            break
    return " ".join(lines)


def table_escape(value: Any) -> str:
    text = "" if value is None else str(value)
    return text.replace("\n", " ").replace("|", "\\|").strip()


def note_rows(notes_dir: Path) -> list[list[str]]:
    rows: list[list[str]] = []
    for note_path in sorted(notes_dir.rglob("*.md")):
        if note_path.name == "literature-matrix.md":
            continue
        if ".paper-insight" in note_path.parts:
            continue
        text = note_path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        title = str(meta.get("title") or note_path.stem)
        rel = note_path.relative_to(notes_dir).as_posix()
        tags = meta.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        tldr = compact_section(section_text(text, "TL;DR"), max_items=1)
        gaps = compact_section(section_text(text, "Research Gaps"), max_items=2)
        rows.append(
            [
                f"[{table_escape(title)}]({table_escape(rel)})",
                table_escape(meta.get("year", "unknown")),
                table_escape(meta.get("venue", "unknown")),
                table_escape(meta.get("status", "unknown")),
                table_escape(", ".join(tags)),
                table_escape(tldr),
                table_escape(gaps),
            ]
        )
    return rows


def render_matrix(rows: list[list[str]]) -> str:
    lines = [
        "# Literature Matrix",
        "",
        "| Paper | Year | Venue | Status | Tags | TL;DR | Gaps |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    if rows:
        lines.extend("| " + " | ".join(row) + " |" for row in rows)
    else:
        lines.append("| No notes found | unknown | unknown | unknown |  |  |  |")
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update notes/literature-matrix.md from paper notes.")
    parser.add_argument("--notes-dir", type=Path, default=Path("notes"), help="Directory containing paper notes")
    parser.add_argument("--output", type=Path, help="Output Markdown path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    notes_dir = args.notes_dir.resolve()
    if not notes_dir.exists():
        print(f"[ERROR] Notes directory not found: {notes_dir}", file=sys.stderr)
        return 2

    output_path = args.output.resolve() if args.output else notes_dir / "literature-matrix.md"
    rows = note_rows(notes_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_matrix(rows), encoding="utf-8")
    print(f"[OK] Wrote literature matrix with {len(rows)} notes: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
