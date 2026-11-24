#!/usr/bin/env python3
"""Create or check historical Markdown companions without changing DOCX/PDF pairs."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
W = "{" + NS["w"] + "}"


def plain(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.iter(W + "t")).replace("\u2014", " - ")


def companion(source: Path) -> str:
    with ZipFile(source) as archive:
        body = ET.fromstring(archive.read("word/document.xml")).find("w:body", NS)
    if body is None:
        raise ValueError(f"Missing document body: {source}")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    parts = [
        f"# {source.stem}",
        "",
        "Historical text companion generated from the existing DOCX. Source content is dated "
        "2026-01-02 and has not been verified as current. Original canonical labels, assertions, "
        "analysis, and proposals below describe the source, not a new approval.",
        "",
        "Unofficial educational resource. Not affiliated with or endorsed by Mathews Archery.",
        "",
        f"- Source DOCX: [original](../{source.name})",
        f"- Paired PDF: [original](../{source.with_suffix('.pdf').name})",
        f"- Source DOCX SHA-256: `{digest}`",
        "- Companion method: `python3 ops/extract-knowledge-text.py --write`",
        "- Formatting: DOCX paragraph order, headings, and tables retained; em dashes normalized to hyphens. "
        "This is a text transcription, not a visual facsimile.",
        "- Use restrictions and unresolved conflicts: [corpus review](../../docs/knowledge-corpus-review.md)",
        "",
        "---",
        "",
    ]
    for child in body:
        if child.tag == W + "p":
            text = plain(child).strip()
            if not text:
                continue
            style = child.find("w:pPr/w:pStyle", NS)
            name = style.get(W + "val", "") if style is not None else ""
            if name.startswith("Heading") and name[-1:].isdigit():
                text = "#" * min(int(name[-1]) + 1, 6) + " " + text
            elif child.find("w:pPr/w:numPr", NS) is not None:
                text = "- " + text
            parts.extend([text, ""])
        elif child.tag == W + "tbl":
            rows = []
            for row in child.findall("w:tr", NS):
                rows.append([
                    "<br>".join(plain(p).strip() for p in cell.findall("w:p", NS)).replace("|", "\\|")
                    for cell in row.findall("w:tc", NS)
                ])
            if rows:
                width = max(map(len, rows))
                for index, row in enumerate(rows):
                    parts.append("| " + " | ".join(row + [""] * (width - len(row))) + " |")
                    if index == 0:
                        parts.append("| " + " | ".join(["---"] * width) + " |")
                parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write mechanical companions; default checks only")
    args = parser.parse_args()
    sources = sorted((ROOT / "knowledge").glob("BRG12-KNOW*.docx"))
    if not sources:
        raise ValueError("No knowledge DOCX files found")
    failures = []
    for source in sources:
        if not source.with_suffix(".pdf").is_file():
            raise ValueError(f"Missing paired PDF: {source}")
        target = ROOT / "knowledge" / "text" / (source.stem + ".md")
        expected = companion(source)
        if args.write:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected, encoding="utf-8")
        elif not target.is_file() or target.read_text(encoding="utf-8") != expected:
            failures.append(target.relative_to(ROOT).as_posix())
    if failures:
        print("Missing or stale companions:\n" + "\n".join(failures))
        return 1
    print(f"{'Wrote' if args.write else 'Verified'} {len(sources)} historical text companions; DOCX/PDF originals unchanged.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
