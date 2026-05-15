#!/usr/bin/env python3
"""Extract paginated text and lightweight metadata from an academic PDF."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REFERENCE_HEADING = re.compile(r"(?im)^\s*(references|bibliography|参考文献)\s*$")


@dataclass
class PageText:
    page: int
    text: str


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_with_pymupdf(pdf_path: Path, max_pages: int | None) -> tuple[dict[str, Any], list[PageText]]:
    import fitz  # type: ignore

    doc = fitz.open(pdf_path)
    page_count = doc.page_count
    limit = min(page_count, max_pages) if max_pages else page_count
    pages = [
        PageText(page=index + 1, text=doc.load_page(index).get_text("text").strip())
        for index in range(limit)
    ]
    metadata = {key: value for key, value in (doc.metadata or {}).items() if value}
    return {"engine": "pymupdf", "page_count": page_count, "metadata": metadata}, pages


def extract_with_pypdf(pdf_path: Path, max_pages: int | None) -> tuple[dict[str, Any], list[PageText]]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    limit = min(page_count, max_pages) if max_pages else page_count
    pages = []
    for index in range(limit):
        text = reader.pages[index].extract_text() or ""
        pages.append(PageText(page=index + 1, text=text.strip()))
    metadata = {}
    if reader.metadata:
        metadata = {str(key).lstrip("/"): str(value) for key, value in reader.metadata.items() if value}
    return {"engine": "pypdf", "page_count": page_count, "metadata": metadata}, pages


def extract_pdf(pdf_path: Path, max_pages: int | None) -> tuple[dict[str, Any], list[PageText]]:
    try:
        return extract_with_pymupdf(pdf_path, max_pages)
    except ImportError:
        pass
    try:
        return extract_with_pypdf(pdf_path, max_pages)
    except ImportError as exc:
        raise RuntimeError(
            "Install a PDF extraction backend first: pip install pymupdf or pip install pypdf"
        ) from exc


def title_candidates(pages: list[PageText], limit: int = 8) -> list[str]:
    candidates: list[str] = []
    seen: set[str] = set()
    blocked = {
        "abstract",
        "introduction",
        "references",
        "bibliography",
        "contents",
        "keywords",
    }

    for page in pages[:2]:
        for raw_line in page.text.splitlines()[:100]:
            line = normalize_space(raw_line)
            if not line:
                continue
            lower = line.lower().strip(":")
            if lower in blocked:
                break
            if len(line) < 8 or len(line) > 180:
                continue
            if "@" in line or "http://" in lower or "https://" in lower:
                continue
            if re.match(r"^\d+(\.\d+)*\s+", line):
                continue
            if line.count(",") >= 3 and len(line.split()) <= 18:
                continue
            key = lower
            if key not in seen:
                candidates.append(line)
                seen.add(key)
            if len(candidates) >= limit:
                return candidates
    return candidates


def reference_section(pages: list[PageText]) -> dict[str, Any] | None:
    for index, page in enumerate(pages):
        match = REFERENCE_HEADING.search(page.text)
        if not match:
            continue
        section = page.text[match.start() :].strip()
        following = "\n\n".join(next_page.text for next_page in pages[index + 1 :])
        if following:
            section = f"{section}\n\n{following}"
        return {"start_page": page.page, "text": section}
    return None


def render_markdown(result: dict[str, Any]) -> str:
    metadata = result.get("pdf_metadata") or {}
    lines = [
        "# Extracted Paper Text",
        "",
        f"- Source: `{result['source']}`",
        f"- Engine: `{result['engine']}`",
        f"- Pages extracted: {result['extracted_page_count']} / {result['page_count']}",
        "",
        "## PDF Metadata",
        "",
    ]

    if metadata:
        for key, value in metadata.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("- No embedded metadata found.")

    lines.extend(["", "## Title Candidates", ""])
    candidates = result.get("title_candidates") or []
    if candidates:
        lines.extend(f"- {candidate}" for candidate in candidates)
    else:
        lines.append("- No clear title candidates found.")

    references = result.get("references") or {}
    lines.extend(["", "## References Section", ""])
    if references:
        lines.append(f"- Starts on extracted page: {references.get('start_page')}")
    else:
        lines.append("- References heading not found in extracted pages.")

    lines.extend(["", "## Pages", ""])
    for page in result["pages"]:
        lines.extend([f"### Page {page['page']}", "", page["text"] or "[No extractable text]", ""])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract paginated text from an academic PDF.")
    parser.add_argument("pdf", type=Path, help="Path to the input PDF")
    parser.add_argument("--output", type=Path, help="Markdown output path")
    parser.add_argument("--json-output", type=Path, help="JSON output path with pages and metadata")
    parser.add_argument("--max-pages", type=int, help="Limit extraction to the first N pages")
    return parser.parse_args()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    pdf_path = args.pdf.resolve()
    if not pdf_path.exists():
        print(f"[ERROR] PDF not found: {pdf_path}", file=sys.stderr)
        return 2
    if pdf_path.suffix.lower() != ".pdf":
        print(f"[ERROR] Input is not a PDF: {pdf_path}", file=sys.stderr)
        return 2
    if args.max_pages is not None and args.max_pages <= 0:
        print("[ERROR] --max-pages must be a positive integer", file=sys.stderr)
        return 2

    try:
        extraction, pages = extract_pdf(pdf_path, args.max_pages)
    except Exception as exc:
        print(f"[ERROR] Could not extract PDF text: {exc}", file=sys.stderr)
        return 3

    refs = reference_section(pages)
    result: dict[str, Any] = {
        "source": str(pdf_path),
        "engine": extraction["engine"],
        "page_count": extraction["page_count"],
        "extracted_page_count": len(pages),
        "pdf_metadata": extraction.get("metadata", {}),
        "title_candidates": title_candidates(pages),
        "references": refs,
        "pages": [asdict(page) for page in pages],
    }

    markdown = render_markdown(result)
    if args.output:
        write_text(args.output, markdown)
        print(f"[OK] Wrote Markdown extraction: {args.output}")
    else:
        sys.stdout.write(markdown)

    if args.json_output:
        write_text(args.json_output, json.dumps(result, ensure_ascii=False, indent=2))
        print(f"[OK] Wrote JSON extraction: {args.json_output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
