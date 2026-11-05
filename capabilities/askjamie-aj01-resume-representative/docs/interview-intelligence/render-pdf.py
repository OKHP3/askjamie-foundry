from pathlib import Path
import re, html, json, argparse, os
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
import fitz

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description="Render the reviewed AskJamie interview reference; requires reportlab and PyMuPDF.")
parser.add_argument('--input',type=Path,default=ROOT/'interview-intelligence.md')
parser.add_argument('--output',type=Path,default=ROOT/'interview-intelligence.rebuilt.pdf')
parser.add_argument('--font-dir',type=Path,default=Path(os.environ.get('DEJAVU_FONT_DIR','/usr/share/fonts/truetype/dejavu')))
parser.add_argument('--force',action='store_true',help='Explicitly replace the output only.')
args=parser.parse_args();SRC=args.input;OUT=args.output
if not SRC.is_file():parser.error('Input Markdown does not exist.')
if OUT.resolve()==SRC.resolve():parser.error('Output cannot replace source.')
if OUT.exists() and not args.force:parser.error('Output exists; choose another output or pass --force.')
if not args.font_dir.is_dir():parser.error('Supply --font-dir containing installed DejaVu Sans font files.')
OUT.parent.mkdir(parents=True,exist_ok=True)
for name,path in [('Body','DejaVuSans.ttf'),('Body-Bold','DejaVuSans-Bold.ttf'),('Body-Oblique','DejaVuSans-Oblique.ttf'),('Body-BoldOblique','DejaVuSans-BoldOblique.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(args.font_dir/path)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Body-Bold',italic='Body-Oblique',boldItalic='Body-BoldOblique')
W,H=letter; M=55
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.6,leading=15.2,spaceAfter=8.5,allowWidows=0,allowOrphans=0,splitLongWords=1),
 'h2':ParagraphStyle('h2',fontName='Body-Bold',fontSize=15.5,leading=20,spaceBefore=17,spaceAfter=10,keepWithNext=True,textColor=colors.HexColor('#18344b')),
 'h3':ParagraphStyle('h3',fontName='Body-Bold',fontSize=11.5,leading=15,spaceBefore=9,spaceAfter=6,keepWithNext=True),
 'title':ParagraphStyle('title',fontName='Body-Bold',fontSize=33,leading=41,textColor=colors.HexColor('#18344b'),spaceAfter=20),
 'subtitle':ParagraphStyle('subtitle',fontName='Body',fontSize=15,leading=23,spaceAfter=25),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.2,leading=13.5,spaceAfter=9),
 'toc':ParagraphStyle('toc',fontName='Body',fontSize=9.4,leading=15,leftIndent=0,firstLineIndent=0,spaceBefore=2),
 'bib':ParagraphStyle('bib',fontName='Body',fontSize=9.2,leading=13.0,spaceAfter=9,splitLongWords=1)
}

def inline(s):
    s=html.escape(s)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
    s=re.sub(r'`([^`]+)`',r'<font name="Body">\1</font>',s)
    # URLs remain readable and clickable, with line wrapping managed by ReportLab.
    def link(m):
        raw=m.group(0); url=raw.rstrip('.,;')
        return '<link href="'+url+'" color="#235b7e">'+url+'</link>'+raw[len(url):]
    s=re.sub(r'(?:https?://|mailto:)[^\s<>]+',link,s)
    return s

class Doc(BaseDocTemplate):
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        frame=Frame(M,59,W-2*M,H-132,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates(PageTemplate(id='main',frames=[frame],onPage=self.decorate))
    def decorate(self,canv,doc):
        canv.saveState()
        canv.setFillColor(colors.HexColor('#18344b'))
        canv.setFont('Body-Bold',8)
        canv.drawString(M,H-29,'AskJamie™ | Interview Intelligence | v2.0.0')
        canv.setFillColor(colors.HexColor('#555555')); canv.setFont('Body',7.2)
        canv.drawString(M,H-41,'Subject: U.S. interview preparation | Author: AskJamie™ | Created: November 5, 2026')
        canv.setStrokeColor(colors.HexColor('#cbd2d8'));canv.line(M,H-48,W-M,H-48)
        canv.line(M,47,W-M,47)
        canv.setFont('Body',7.05);canv.setFillColor(colors.HexColor('#444444'))
        canv.drawString(M,35,'© 2025 AskJamie™ and OverKill Hill P³™. All rights reserved.')
        canv.drawString(M,23,'askjamie.bot  |  contact@askjamie.bot')
        canv.linkURL('https://askjamie.bot',(M,19,M+65,30),relative=0)
        canv.linkURL('mailto:contact@askjamie.bot',(M+75,19,M+190,30),relative=0)
        canv.drawRightString(W-M,23,f'{doc.page}')
        canv.restoreState()
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and getattr(flowable,'section_key',None):
            text=flowable.getPlainText(); key=flowable.section_key
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text,key,level=0,closed=False)
            self.notify('TOCEntry',(0,text,self.page,key))

text=SRC.read_text(encoding='utf-8')
if 'version: 2.0.0\n' not in text or 'created: 2026-11-05\n' not in text:
    parser.error('This renderer is bound to edition 2.0.0 dated 2026-11-05; review and update its metadata for a renewed edition.')
text=re.sub(r'\A---\n.*?\n---\n','',text,flags=re.S)
story=[Spacer(1,47),Paragraph('AskJamie™<br/>Interview Intelligence',styles['title']),Paragraph('Evidence-led preparation, adaptive practice,<br/>and renewable career knowledge',styles['subtitle']),Paragraph('<b>United States | Review edition 2.0.0</b>',styles['body']),Paragraph('Prepared for Jamie Hill with AI assistance<br/>Created and reviewed: November 5, 2026',styles['body']),Spacer(1,20),Paragraph('A complete coaching reference: truthful candidate evidence, role research, adaptable narratives, simulations, feedback, and a quarterly or annual renewal protocol.',styles['body']),Paragraph('Public-safe methods and fictional examples. Personal candidate evidence belongs in a separate permission-controlled workspace.',styles['body']),Spacer(1,24),Paragraph('Editorial status: review candidate. File validation does not establish host deployment, candidate rehearsal, repository integration, or exact-thread archival.',styles['small']),Paragraph('The requested 2025 rights notice is retained. This edition was created in 2026.',styles['small']),PageBreak(),Paragraph('Contents',styles['h2'])]
toc=TableOfContents();toc.levelStyles=[styles['toc']];toc.dotsMinLevel=0
story+=[toc,PageBreak()]
blocks=re.split(r'\n\s*\n',text.strip())
for block in blocks:
    if block.startswith('# ') or block.startswith('Website:'):continue
    if block.startswith('## '):
        line=block.splitlines()[0][3:]
        p=Paragraph(inline(line),styles['h2']);p.section_key=line.split(' | ')[0]
        story.append(p)
        remain='\n'.join(block.splitlines()[1:]).strip()
        if remain:story.append(Paragraph(inline(remain),styles['body']))
    elif block.startswith('### '):
        story.append(Paragraph(inline(block[4:]),styles['h3']))
    else:
        sty=styles['bib'] if re.match(r'\*\*S\d{2}\.',block) else styles['body']
        para=Paragraph(inline(' '.join(block.splitlines())),sty)
        story.append(KeepTogether([para]) if sty is styles['bib'] else para)

doc=Doc(str(OUT),pagesize=letter,title='AskJamie Interview Intelligence',author='AskJamie; prepared for Jamie Hill with AI assistance',subject='U.S. employment interview preparation and AI-assisted career coaching',keywords='AskJamie, interview preparation, evidence, RAG, career coaching, 2026-11-05',pageCompression=1)
doc.multiBuild(story)
pdf=fitz.open(OUT)
print('PDF pages',len(pdf),'bytes',OUT.stat().st_size)
