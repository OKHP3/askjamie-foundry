"""Render the AJ01 post-COVID hiring reference from its adjacent Markdown."""

import argparse
from html import escape
from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Spacer
from reportlab.platypus.tableofcontents import TableOfContents


SOURCE = Path(__file__).with_name("post-covid-hiring-research-draft-2026q4.md")
SECTION = re.compile(r"^## (PC-\d{3}) [-\u2013\u2014] (.+)$")
URL = re.compile(r"https?://[^\s<>()]+")
WIDTH, HEIGHT = letter
MARGIN = 60


def inline(text):
    """Format the manuscript's links and emphasis as ReportLab markup."""
    runs = []
    end = 0
    for match in URL.finditer(text):
        runs.append(escape(text[end:match.start()]))
        url = match.group().rstrip(".,;")
        runs.append(f'<link href="{escape(url, quote=True)}">{escape(url)}</link>')
        end = match.start() + len(url)
    runs.append(escape(text[end:]))
    marked = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", "".join(runs))
    return re.sub(r"(?<!\*)\*([^*]+)\*", r"<i>\1</i>", marked)


class Reference(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "Section":
            heading = flowable.getPlainText()
            key = heading.split()[0]
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(heading, key, 0)
            self.notify("TOCEntry", (0, heading, self.page, key))


def register_fonts(directory):
    for name, filename in {
        "Body": "arial.ttf",
        "Bold": "arialbd.ttf",
        "Italic": "ariali.ttf",
        "BoldItalic": "arialbi.ttf",
    }.items():
        pdfmetrics.registerFont(TTFont(name, str(directory / filename)))
    pdfmetrics.registerFontFamily(
        "Body", normal="Body", bold="Bold", italic="Italic", boldItalic="BoldItalic"
    )


def page_furniture(canvas, document):
    canvas.setFont("Bold", 9)
    canvas.drawString(MARGIN, HEIGHT - 36, "ASKJAMIE  |  POST-COVID HIRING  |  2026 Q4")
    canvas.setStrokeColor(colors.HexColor("#3F6D79"))
    canvas.line(MARGIN, HEIGHT - 45, WIDTH - MARGIN, HEIGHT - 45)
    canvas.setFont("Body", 8)
    canvas.drawString(MARGIN, 40, "c 2025 AskJamieT and OverKill Hill P3T. All rights reserved.")
    for x, label, target in (
        (MARGIN, "https://askjamie.bot", "https://askjamie.bot"),
        (MARGIN + 98, "contact@askjamie.bot", "mailto:contact@askjamie.bot"),
    ):
        canvas.drawString(x, 25, label)
        canvas.linkURL(target, (x, 23, x + pdfmetrics.stringWidth(label, "Body", 8), 33))
    canvas.drawRightString(WIDTH - MARGIN, 25, str(document.page))


def build(output):
    _, metadata, body = SOURCE.read_text(encoding="utf-8").split("---", 2)
    fields = dict(line.split(": ", 1) for line in metadata.strip().splitlines())
    title = fields["title"].strip('"')
    subject = fields["subject"].strip('"')
    author = fields["author"].strip('"')
    document = Reference(
        str(output), title=title, subject=subject, author=author, lang="en-US",
        pagesize=letter, leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=62, bottomMargin=58,
    )
    paragraph = ParagraphStyle("Body", fontName="Body", fontSize=12, leading=17, spaceAfter=10)
    heading = ParagraphStyle(
        "Section", parent=paragraph, fontName="Bold", fontSize=19, leading=23,
        spaceAfter=16, keepWithNext=True, textColor=colors.HexColor("#244651"),
    )
    subheading = ParagraphStyle("Subheading", parent=paragraph, fontName="Bold", keepWithNext=True)
    cover = ParagraphStyle("Cover", parent=heading, fontSize=27, leading=34)
    contents = TableOfContents()
    contents.levelStyles = [
        ParagraphStyle("TOC", parent=paragraph, fontSize=10, leading=13, spaceAfter=3)
    ]
    blocks = re.split(r"\n\s*\n", body.strip())
    introduction = blocks[1]
    story = [
        Spacer(1, 80), Paragraph(escape(title), cover),
        Paragraph(inline(fields["subtitle"].strip('"')), paragraph),
        Paragraph(escape(author), paragraph),
        Paragraph(f"Source edition created {escape(fields['created'])}", paragraph),
        Spacer(1, 20), Paragraph(inline(introduction), paragraph),
        PageBreak(), Paragraph("Contents", cover), contents,
    ]
    for block in blocks[2:]:
        if block.startswith("# "):
            continue
        if match := SECTION.fullmatch(block):
            if match[1] != "PC-023":
                story.append(PageBreak())
            story.append(Paragraph(inline(f"{match[1]} - {match[2]}"), heading))
        elif block.startswith("### "):
            label, _, definition = block[4:].partition("\n")
            story.append(Paragraph(inline(label), subheading))
            story.append(Paragraph(inline(" ".join(definition.splitlines())), paragraph))
        else:
            story.append(Paragraph(inline(" ".join(block.splitlines())), paragraph))
    document.multiBuild(story, onFirstPage=page_furniture, onLaterPages=page_furniture)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font-dir", required=True, type=Path, help="Directory with Arial TTF files")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output already exists")
    register_fonts(args.font_dir)
    build(args.output)
