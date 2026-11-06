"""Build the text-only reference PDF from the adjacent Markdown source.
Requires reportlab and pypdf. Fonts are discovered locally and are not distributed.
"""
from __future__ import annotations
from pathlib import Path
import re, html, sys
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'us-hiring-knowledge-2026q4.md'
OUT=ROOT/'us-hiring-knowledge-2026q4.pdf'
FONT_ROOTS=[Path('/usr/share/fonts/truetype/dejavu'),Path('/usr/local/share/fonts')]
def find_font(name: str)->Path:
 for root in FONT_ROOTS:
  if (root/name).exists(): return root/name
 raise FileNotFoundError(f'Install DejaVu fonts or configure FONT_ROOTS; missing {name}')
for name,fn in [('Body','DejaVuSans.ttf'),('BodyBold','DejaVuSans-Bold.ttf'),('BodyItalic','DejaVuSans-Oblique.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(find_font(fn))))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Text',fontName='Body',fontSize=10.1,leading=14.4,spaceAfter=7.2,allowWidows=0,allowOrphans=0))
styles.add(ParagraphStyle(name='Meta',fontName='Body',fontSize=8.1,leading=11.4,spaceAfter=10,textColor=colors.HexColor('#444444')))
styles.add(ParagraphStyle(name='Chapter',fontName='BodyBold',fontSize=15,leading=19,spaceBefore=17,spaceAfter=10,keepWithNext=True))
styles.add(ParagraphStyle(name='Sub',fontName='BodyBold',fontSize=11.5,leading=15,spaceBefore=12,spaceAfter=6,keepWithNext=True))
styles.add(ParagraphStyle(name='Cover',fontName='BodyBold',fontSize=27,leading=34,spaceAfter=19))
styles.add(ParagraphStyle(name='Deck',fontName='Body',fontSize=14,leading=20,spaceAfter=18))
styles.add(ParagraphStyle(name='Bib',fontName='Body',fontSize=8.5,leading=12.2,spaceAfter=10,splitLongWords=True))
styles.add(ParagraphStyle(name='TOC0',fontName='Body',fontSize=10,leading=14,spaceBefore=5,leftIndent=0,firstLineIndent=0))

def inline(s:str)->str:
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'\[([^\]]+)\]\((https?://[^\s)]+|mailto:[^\s)]+)\)',r'<link href="\2">\1</link>',s)
 s=re.sub(r'(?<![="\w])(https?://[^\s<]+)',lambda m:f'<link href="{m.group(1).rstrip(".")}">{m.group(1)}</link>',s)
 return s

class Book(BaseDocTemplate):
 def afterFlowable(self,flow):
  if isinstance(flow,Paragraph) and flow.style.name=='Chapter':
   text=flow.getPlainText(); key='s-'+re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')
   self.canv.bookmarkPage(key)
   self.canv.addOutlineEntry(text,key,0,False)
   self.notify('TOCEntry',(0,text,self.page,key))

def furniture(c,doc):
 w,h=letter
 c.saveState()
 c.setFont('BodyBold',8)
 c.drawString(49,h-27,'ASKJAMIE™  |  U.S. Hiring Documents and Selection Processes')
 c.setFont('Body',7)
 c.drawString(49,h-39,'Subject: U.S. hiring artifacts and selection workflows  |  Edition 2026.Q4')
 c.setStrokeColor(colors.HexColor('#777777')); c.setLineWidth(.35); c.line(49,h-46,w-49,h-46)
 c.setFont('Body',6.8)
 c.drawString(49,43,'Author: AskJamie™ | AI-assisted research synthesis  •  Created: 2026-11-05')
 c.drawString(49,32,'© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved.')
 c.drawString(49,21,'https://askjamie.bot  |  contact@askjamie.bot')
 c.linkURL('https://askjamie.bot',(49,18,142,29),relative=0)
 c.linkURL('mailto:contact@askjamie.bot',(153,18,264,29),relative=0)
 c.drawRightString(w-49,21,f'{doc.page}')
 c.restoreState()

def build():
 text=SRC.read_text(encoding='utf-8')
 if not text.startswith('---\n'): raise ValueError('Required metadata block missing')
 body=text.split('---',2)[2].strip()
 doc=Book(str(OUT),pagesize=letter,leftMargin=49,rightMargin=49,topMargin=63,bottomMargin=61,
          title='U.S. Hiring Documents and Selection Processes',author='AskJamie™ | AI-assisted research synthesis prepared for Jamie',
          subject='U.S. CVs, resumes, applications, ATS, interviews and selection paperwork; 2000–2026 and outlook to 2035',
          pageCompression=1)
 doc.addPageTemplates(PageTemplate(id='body',frames=[Frame(49,61,letter[0]-98,letter[1]-124,id='normal')],onPage=furniture))
 story=[Spacer(1,51),Paragraph('U.S. Hiring Documents<br/>and Selection Processes',styles['Cover']),
        Paragraph('Historical development, current practice,<br/>and evidence-bounded outlook',styles['Deck']),
        Paragraph('A text-only professional reference and retrieval-ready knowledge resource',styles['Text']),Spacer(1,20)]
 for t in ['Edition 2026.Q4 • Version 2.0.0','Historical scope: 2000–2026 • Forecast scope: 2027–2035','Evidence review boundary: November 5, 2026','Prepared by AskJamie™ through AI-assisted research synthesis for Jamie','United States, with selected state and local examples','Short Chicago author-date citations • Full source register and bibliography','Research edition: not individualized legal advice or proof of host deployment','© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved.','https://askjamie.bot | contact@askjamie.bot']:
  story.append(Paragraph(inline(t),styles['Meta']))
 story += [PageBreak(),Paragraph('Contents',styles['Chapter'])]
 toc=TableOfContents(); toc.levelStyles=[styles['TOC0']]; toc.dotsMinLevel=0
 story += [toc,PageBreak()]
 for block in re.split(r'\n\s*\n',body):
  block=block.strip()
  if not block: continue
  if block.startswith('# '): continue
  if block.startswith('## '): story.append(Paragraph(inline(block[3:]),styles['Chapter']))
  elif block.startswith('### '): story.append(Paragraph(inline(block[4:]),styles['Sub']))
  else:
   style=styles['Meta'] if block.startswith('Section-ID:') else styles['Bib'] if re.match(r'\[S\d+\]',block) else styles['Text']
   story.append(Paragraph(inline(' '.join(block.splitlines())),style))
 doc.multiBuild(story)
 reader=PdfReader(str(OUT)); writer=PdfWriter(); writer.clone_document_from_reader(reader)
 writer.add_metadata({'/Title':'U.S. Hiring Documents and Selection Processes','/Subject':'U.S. hiring artifacts, selection workflows, historical development and outlook','/Author':'AskJamie™ | AI-assisted research synthesis prepared for Jamie','/CreationDate':"D:20261105000000-06'00'",'/ModDate':"D:20261105000000-06'00'",'/Keywords':'AskJamie; AJ01; US hiring; resumes; curriculum vitae; ATS; interviews; RAG; 2026.Q4'})
 from pypdf.generic import NameObject,TextStringObject
 writer._root_object.update({NameObject('/Lang'):TextStringObject('en-US')})
 temp=OUT.with_suffix('.tmp.pdf')
 with temp.open('wb') as f: writer.write(f)
 temp.replace(OUT)
 print(f'{OUT.name}: {len(reader.pages)} pages, {OUT.stat().st_size} bytes')

if __name__=='__main__':
 try: build()
 except Exception as exc:
  print(f'Build failed: {exc}',file=sys.stderr); raise
