"""Re-run local artifact checks. This is not a hosted-agent or legal validation."""
from pathlib import Path
import re,json,unicodedata
import fitz
from pypdf import PdfReader

P=Path(__file__).resolve().parent
md=(P/'us-hiring-knowledge-2026q4.md').read_text(encoding='utf-8')
pdf=P/'us-hiring-knowledge-2026q4.pdf'
if not pdf.is_file():
    raise SystemExit('Run python3 build_pdf.py to generate the PDF before validating it.')
sources=json.loads((P/'sources.json').read_text(encoding='utf-8'))['sources']
doc=fitz.open(str(pdf))
reader=PdfReader(str(pdf))
text='\n'.join(pg.get_text() for pg in doc)
body='\n'.join(pg.get_text(clip=fitz.Rect(45,55,568,733)) for pg in doc[3:])
def norm(x):return re.sub(r'\s+','',unicodedata.normalize('NFKC',x))
keys={s['citation_key'] for s in sources}
citations=[]
for group in re.findall(r'\(([^()]+)\)',md.split('## 36.')[0]):
 if re.search(r'\b(?:19|20)\d{2}\b|n\.d\.',group):
  citations += [c.strip() for c in group.split(';')]
unknown=[c for c in citations if c not in keys]
ids=re.findall(r'Section-ID: (HIR-\d{3})',md)
checks={
'pdf_opens_two_libraries':len(doc)==len(reader.pages),
'pdf_at_least_20_pages':len(doc)>=20,
'markdown_at_least_10000_words':len(md.split())>=10000,
'all_36_section_ids_unique':len(ids)==len(set(ids))==36,
'all_section_ids_in_pdf':all(i in text for i in ids),
'no_raster_images':sum(len(pg.get_images()) for pg in doc)==0,
'no_encryption':not reader.is_encrypted,
'no_unicode_replacement_characters':'\ufffd' not in text,
'all_inline_citations_resolve':not unknown,
'all_sources_cited':all(s['citation_key'] in citations for s in sources),
'all_sources_in_bibliography':all(f"[{s['id']}]" in md for s in sources),
'no_legacy_tool_citation_tokens':not re.search(r'【||turn\d+(?:search|file|view)',md),
'pdf_title_metadata':reader.metadata.title=='U.S. Hiring Documents and Selection Processes',
'pdf_author_metadata':'AskJamie' in reader.metadata.author,
'pdf_subject_metadata':bool(reader.metadata.subject),
'copyright_marks_present':all(s in text for s in ['© 2025','AskJamie™','OverKill Hill P³™']),
'website_and_email_present':all(s in text for s in ['https://askjamie.bot','contact@askjamie.bot']),
'creation_date_present':'2026-11-05' in text,
'outlines_present':len(doc.get_toc())>=36,
'no_blank_pages':all(len(pg.get_text().strip())>500 for pg in doc),
}
# Compare prose, excluding presentation metadata and link syntax, across page boundaries.
prose=md.split('---',2)[2].strip()
paras=[]
for block in re.split(r'\n\s*\n',prose):
 if block.startswith('#') or block.startswith('Section-ID:'):continue
 clean=re.sub(r'\[([^\]]+)\]\([^\)]+\)',r'\1',block).replace('**','')
 paras.append(clean)
miss=[p[:130] for p in paras if norm(p) not in norm(body)]
checks['all_prose_paragraphs_preserved_in_pdf']=not miss
outside=[]
for i,pg in enumerate(doc):
 for b in pg.get_text('dict')['blocks']:
  for l in b.get('lines',[]):
   for s in l['spans']:
    x0,y0,x1,y1=s['bbox']
    if x0<-1 or y0<-1 or x1>pg.rect.width+1 or y1>pg.rect.height+1:outside.append((i+1,s['text'][:80]))
checks['no_text_outside_page_bounds']=not outside
# Local lexical search over independently useful section chunks.
parts=re.split(r'(?=^## \d{2}\.)',md,flags=re.M)[1:]
chunks=[]
for part in parts:
 m=re.search(r'Section-ID: (HIR-\d{3})',part)
 if m and m.group(1)!='HIR-036':chunks.append((m.group(1),part))
queries=[('ATS parsing failure automatic rejection','HIR-011'),('federal USAJOBS two-page resume','HIR-009'),('FCRA background pre-adverse action','HIR-021'),('Form 8850 WOTC December 31','HIR-024'),('Colorado January 1 2027','HIR-026'),('curriculum vitae CV academic','HIR-009'),('pre-offer disability medical examinations','HIR-020'),('I-9 Section 1 work authorization','HIR-023'),('pay transparency salary history','HIR-025'),('RAG chunking metadata source','HIR-033')]
stop={'the','a','an','in','on','and','or','of','to','for','as','is','it','with','not','this','that','be','by'}
def toks(x):return [w for w in re.findall(r'[a-z0-9]+',x.lower()) if w not in stop]
# TF-IDF ranking is a smoke test, not an embedding or answer-quality evaluation.
import math,collections
cs=[collections.Counter(toks(c)) for _,c in chunks];df=collections.Counter(t for c in cs for t in c)
retr=[]
for q,target in queries:
 scores=[sum((1+math.log(c[t]))*math.log(1+len(cs)/(1+df[t])) for t in set(toks(q)) if c[t]) for c in cs]
 ranked=[chunks[i][0] for i in sorted(range(len(scores)),key=lambda i:scores[i],reverse=True)[:3]]
 retr.append({'query':q,'expected_section':target,'top_3':ranked,'pass':target in ranked})
checks['lexical_retrieval_top3_all_queries']=all(r['pass'] for r in retr)
result={'pass_name':'A: local mechanical artifact validation','run_date':'2026-11-05','page_count':len(doc),'markdown_words_whitespace_delimited':len(md.split()),'source_count':len(sources),'section_count':len(ids),'checks':checks,'unknown_citations':unknown,'missing_pdf_paragraphs':miss,'out_of_bounds_spans':outside,'retrieval_smoke_test':retr,'limits':['No hosted GPT or agent evaluation.','No PDF/UA accessibility conformance certification.','No exhaustive live HTTP link audit; source access depth is recorded separately.','No independent human legal review.','Remote persistence and integration are separate checks.']}
(P/'validation-pass-a.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n', encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
if not all(checks.values()): raise SystemExit(1)
