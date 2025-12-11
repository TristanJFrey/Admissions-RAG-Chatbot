"""
Convert a DOCX file to a simple Markdown file (headings, paragraphs, bullets, and basic tables).

Usage:
    python scripts/convert_docx_to_md.py input.docx output.md
"""

import sys
from pathlib import Path
from typing import List
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl


def is_heading(p: Paragraph) -> bool:
    name = p.style.name if p.style is not None else ""
    return name.startswith("Heading")


def heading_level(p: Paragraph) -> int:
    try:
        return int(p.style.name.split()[-1])
    except Exception:
        return 1


def is_list_bullet(p: Paragraph) -> bool:
    name = p.style.name if p.style is not None else ""
    return ("List Bullet" in name) or ("List Number" in name)


def paragraph_to_markdown(p: Paragraph, heading_prefix: str = "") -> str:
    text = p.text.strip()
    if not text:
        return ""
    if is_heading(p):
        lvl = heading_level(p)
        lvl = max(1, min(lvl, 6))
        return heading_prefix + "#" * lvl + " " + text
    if is_list_bullet(p):
        return f"- {text}"
    return text


def table_to_markdown(tbl: Table) -> List[str]:
    rows = tbl.rows
    if not rows:
        return []

    # Determine column count from the widest row.
    col_count = max(len(r.cells) for r in rows)

    def normalize_row(cells):
        vals = [c.text.strip() for c in cells]
        # pad to col_count
        if len(vals) < col_count:
            vals += [""] * (col_count - len(vals))
        return vals

    raw_headers = normalize_row(rows[0].cells)
    if all(not h for h in raw_headers):
        headers = [f"col_{i+1}" for i in range(col_count)]
        data_rows = [normalize_row(r.cells) for r in rows]
    else:
        headers = [h or f"col_{i+1}" for i, h in enumerate(raw_headers)]
        data_rows = [normalize_row(r.cells) for r in rows[1:]]

    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for vals in data_rows:
        lines.append("| " + " | ".join(vals) + " |")
    return lines


def convert_docx_to_md(input_path: Path, output_path: Path) -> None:
    doc = Document(str(input_path))
    out_lines: List[str] = []

    first_heading = True

    for child in doc.element.body.iterchildren():
        if isinstance(child, CT_P):
            p = Paragraph(child, doc)
            heading_prefix = ""
            if is_heading(p):
                if first_heading:
                    first_heading = False
                else:
                    heading_prefix = "---\n\n"
            md_line = paragraph_to_markdown(p, heading_prefix=heading_prefix)
            if md_line:
                out_lines.append(md_line)
        elif isinstance(child, CT_Tbl):
            tbl = Table(child, doc)
            md_lines = table_to_markdown(tbl)
            if md_lines:
                out_lines.append("\n".join(md_lines))
        else:
            continue
    output_path.write_text("\n\n".join(out_lines), encoding="utf-8")
    print(f"Converted {input_path} -> {output_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: python scripts/convert_docx_to_md.py input.docx output.md")
        sys.exit(1)
    convert_docx_to_md(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
