#!/usr/bin/env python3
"""Render this Markdown reference to an inspectable PDF.

Usage: python render.py [knowledge-file.md] [knowledge-file.pdf]
Requires: reportlab, PyYAML. Writes only the selected PDF and build-info.json.
This renderer is a document utility, not a FoundRy runtime dependency.
"""
from __future__ import annotations
import hashlib
import html
import json
import os
from datetime import datetime, timezone
import re
import sys
from pathlib import Path

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer,
)
from reportlab.platypus.tableofcontents import TableOfContents

TITLE = 'AskJamie™ Evidence-Led Cover Letter Strategy'
SUBJECT = 'Research-grounded candidate positioning and retrieval-ready cover-letter operations'
NOTICE = '© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved.'
NAVY = colors.HexColor('#17324D')
TEAL = colors.HexColor('#28676B')
GREY = colors.HexColor('#53616B')


def inline(text: str) -> str:
    """Escape content before adding only known inline markup and safe links."""
    text = html.escape(text, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
    def link(match: re.Match[str]) -> str:
        raw = match.group(0)
        url = raw.rstrip('.,;')
        suffix = raw[len(url):]
        return f'<link href="{html.escape(url, quote=True)}" color="#28676B">{url}</link>{suffix}'
    return re.sub(r'https://[^\s<>]+', link, text)


class ReferenceDoc(BaseDocTemplate):
    def __init__(self, path: Path, metadata: dict):
        super().__init__(str(path), pagesize=letter,
                         leftMargin=54, rightMargin=54,
                         topMargin=88, bottomMargin=72,
                         title=metadata['title'], author=metadata['author'],
                         subject=metadata['subject'],
                         creator='AskJamie reference renderer 1.0',
                         pageCompression=1, invariant=1)
        self.meta = metadata
        self.heading_index = 0
        self.heading_pages: list[dict] = []
        frame = Frame(54, 72, 504, 632, leftPadding=0, rightPadding=0,
                      topPadding=0, bottomPadding=0, id='body')
        self.addPageTemplates(PageTemplate(id='reference', frames=[frame],
                                          onPage=self.decorate))

    def beforeDocument(self):
        self.heading_index = 0
        self.heading_pages = []

    def decorate(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.setFont('Helvetica-Bold', 8.4)
        canvas.drawString(54, 760, str(self.meta['title']))
        canvas.setFillColor(GREY)
        canvas.setFont('Helvetica', 7.2)
        canvas.drawString(54, 748, str(self.meta['subject']))
        canvas.drawString(54, 736, f"Author: {self.meta['author']}   •   Created: {self.meta['created']}")
        canvas.setStrokeColor(TEAL)
        canvas.setLineWidth(0.5)
        canvas.line(54, 726, 558, 726)
        canvas.setStrokeColor(colors.HexColor('#CAD3D8'))
        canvas.line(54, 61, 558, 61)
        canvas.setFillColor(GREY)
        canvas.setFont('Helvetica', 7.2)
        canvas.drawString(54, 49, str(self.meta['copyright']))
        canvas.drawString(54, 37, f"{self.meta['website']}   |   {self.meta['contact']}")
        canvas.linkURL(str(self.meta['website']), (54, 34, 126, 45), relative=0)
        canvas.linkURL('mailto:'+str(self.meta['contact']), (139, 34, 238, 45), relative=0)
        canvas.drawRightString(558, 37, f"Reference edition {self.meta['version']}   |   Page {doc.page}")
        canvas.restoreState()

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ('H2', 'H3'):
            text = flowable.getPlainText()
            level = 0 if flowable.style.name == 'H2' else 1
            self.heading_index += 1
            key = f'h{self.heading_index}'
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text, key, level=level, closed=False)
            self.heading_pages.append({'heading': text, 'page': self.page})
            if text.startswith('CL-') and level == 0:
                self.notify('TOCEntry', (0, text, self.page, key))


def render(source: Path, output: Path) -> dict:
    raw = source.read_bytes()
    text = raw.decode('utf-8')
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if match is None:
        raise ValueError('Missing YAML front matter')
    meta = yaml.safe_load(match.group(1))
    # Use the documented edition date, not ReportLab's invariant year-2000 default.
    epoch = datetime.fromisoformat(str(meta['edition_date'])).replace(tzinfo=timezone.utc)
    os.environ['SOURCE_DATE_EPOCH'] = str(int(epoch.timestamp()))
    body = text[match.end():].strip()
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle('Body', fontName='Times-Roman', fontSize=11,
                                leading=15.2, spaceAfter=8, alignment=TA_LEFT,
                                allowWidows=0, allowOrphans=0)
    styles.add(body_style)
    styles.add(ParagraphStyle('TitleMain', fontName='Helvetica-Bold', fontSize=27,
                              leading=34, textColor=NAVY, spaceBefore=62,
                              spaceAfter=28, keepWithNext=True))
    styles.add(ParagraphStyle('H2', fontName='Helvetica-Bold', fontSize=15,
                              leading=19, textColor=NAVY, spaceBefore=18,
                              spaceAfter=11, keepWithNext=True))
    styles.add(ParagraphStyle('H3', fontName='Helvetica-Bold', fontSize=11.6,
                              leading=15.5, textColor=TEAL, spaceBefore=12,
                              spaceAfter=7, keepWithNext=True))
    styles.add(ParagraphStyle('Meta', parent=body_style, fontName='Helvetica',
                              fontSize=9.6, leading=15, textColor=GREY,
                              spaceAfter=14))
    styles.add(ParagraphStyle('Retrieval', parent=body_style, fontName='Helvetica',
                              fontSize=8.4, leading=12, textColor=GREY,
                              spaceAfter=10, keepWithNext=True))
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle('TOCItem', fontName='Helvetica', fontSize=8.6,
                                      leading=11.4, spaceBefore=0, leftIndent=0,
                                      firstLineIndent=0, rightIndent=18)]
    story = []
    front = True
    blocks = re.split(r'\n\s*\n', body)
    skip_contents = False
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block == '## Contents':
            story += [PageBreak(), Paragraph('Contents', styles['H2']), toc, PageBreak()]
            skip_contents = True
            continue
        if skip_contents and block.startswith('- CL-'):
            continue
        skip_contents = False
        if block.startswith('## Executive summary'):
            story.append(PageBreak())
            front = False
        if block.startswith('# '):
            story.append(Paragraph(inline(block[2:]), styles['TitleMain']))
        elif block.startswith('## '):
            story.append(Paragraph(inline(block[3:]), styles['H2']))
        elif block.startswith('### '):
            story.append(Paragraph(inline(block[4:]), styles['H3']))
        elif block.startswith('**Retrieval terms:**'):
            story.append(Paragraph(inline(block), styles['Retrieval']))
        else:
            formatted = '<br/>'.join(inline(line.rstrip()) for line in block.splitlines())
            story.append(Paragraph(formatted, styles['Meta'] if front else styles['Body']))
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = ReferenceDoc(output, meta)
    doc.multiBuild(story)
    info = {
        'source': source.name, 'source_sha256': hashlib.sha256(raw).hexdigest(),
        'source_git_blob_sha1': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
        'output': output.name, 'output_sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
        'word_count_including_metadata': len(re.findall(r"\b[\w'-]+\b", text)),
        'pages': doc.page, 'heading_pages': doc.heading_pages,
        'renderer': 'ReportLab', 'style': 'US Letter; 11 pt Times; 15.2 pt leading',
        'metadata': {k: str(v) for k, v in meta.items()},
    }
    (output.parent/'build-info.json').write_text(json.dumps(info, indent=2, ensure_ascii=False)+'\n')
    return info


if __name__ == '__main__':
    here = Path(__file__).resolve().parent
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else here/'knowledge-file.md'
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else here/'knowledge-file.pdf'
    try:
        result = render(src, out)
    except (OSError, ValueError) as exc:
        raise SystemExit(f'Render failed: {exc}') from exc
    print(json.dumps({k: result[k] for k in ('source_sha256','output_sha256','pages','word_count_including_metadata')}, indent=2))
