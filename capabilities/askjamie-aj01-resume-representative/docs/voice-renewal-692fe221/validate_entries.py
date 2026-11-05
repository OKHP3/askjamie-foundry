"""Supplemental, read-only glossary checks. Not a semantic or host acceptance test.
Usage: python validate_entries.py entries.jsonl sources.json [--public]
Sources must be the frozen analysis subset, with source_id and text fields.
"""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REQUIRED = {'entry_id','term','meaning','evidence_class','evidence','frequency',
            'would','should','could','would_not','should_not','could_not',
            'synthetic_example','review_status','privacy','public_use_approved'}
CLASSES = {'OBSERVED','DECLARED','ADOPTED','INFERRED','PROPOSED'}

def validate(entries: list[dict[str, Any]], sources: list[dict[str, Any]],
             public: bool = False) -> list[str]:
    errors: list[str] = []
    if not isinstance(entries, list) or not isinstance(sources, list):
        return ['entries and sources must be lists']
    if any(not isinstance(s, dict) or not isinstance(s.get('source_id'), str)
           or not s['source_id'].strip() or not isinstance(s.get('text'), str)
           for s in sources):
        return ['sources require nonempty string source_id and string text']
    smap = {s['source_id']: s for s in sources}
    if len(smap) != len(sources):
        errors.append('duplicate source IDs')
    ids: set[str] = set()
    terms: set[str] = set()
    for i, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f'row-{i}: entry must be an object')
            continue
        label = str(entry.get('entry_id', f'row-{i}'))
        missing = REQUIRED - entry.keys()
        if missing:
            errors.append(f'{label}: missing {sorted(missing)}')
            continue
        if label in ids:
            errors.append(f'{label}: duplicate entry ID')
        ids.add(label)
        term = str(entry['term']).strip()
        if not term:
            errors.append(f'{label}: empty term')
        if term.casefold() in terms:
            errors.append(f'{label}: duplicate canonical term')
        terms.add(term.casefold())
        if entry['evidence_class'] not in CLASSES:
            errors.append(f'{label}: invalid evidence class')
        if public and (entry['privacy'] != 'public' or entry['public_use_approved'] is not True):
            errors.append(f'{label}: public distribution not approved in record')
        evidence = entry['evidence']
        if not isinstance(evidence, list):
            errors.append(f'{label}: evidence must be a list')
            continue
        if entry['evidence_class'] == 'OBSERVED' and not evidence:
            errors.append(f'{label}: observed entry has no evidence')
        for e in evidence:
            if not isinstance(e, dict):
                errors.append(f'{label}: evidence item must be an object')
                continue
            source = smap.get(e.get('source_id'))
            if source is None:
                errors.append(f'{label}: unresolved source ID')
                continue
            quote = e.get('quote', '')
            text = source.get('text', '')
            if not isinstance(quote, str) or not quote or quote not in text:
                errors.append(f'{label}: quotation not in source')
            if 'match_start' in e and 'match_end' in e:
                start, end = e['match_start'], e['match_end']
                if not isinstance(start, int) or not isinstance(end, int) or start < 0 or end < start or text[start:end] != quote:
                    errors.append(f'{label}: quotation offset mismatch')
        f = entry['frequency']
        if not isinstance(f, dict):
            errors.append(f'{label}: frequency must be an object')
            continue
        for field in ('occurrences', 'independent_source_count'):
            value = f.get(field)
            if value is not None and (type(value) is not int or value < 0):
                errors.append(f'{label}: {field} must be a nonnegative integer or null')
        if entry['evidence_class'] == 'PROPOSED' and f.get('occurrences') is not None:
            errors.append(f'{label}: proposed wording has historical count')
        if entry['evidence_class'] == 'OBSERVED':
            pattern = re.compile(r'(?<!\w)' + re.escape(term) + r'(?!\w)', re.I)
            counts = [len(pattern.findall(s['text'])) for s in sources]
            if f.get('occurrences') is not None and f['occurrences'] != sum(counts):
                errors.append(f'{label}: occurrence count mismatch')
            if f.get('independent_source_count') is not None and f['independent_source_count'] != sum(n > 0 for n in counts):
                errors.append(f'{label}: source count mismatch')
        for field in ('meaning','would','should','could','would_not','should_not','could_not','synthetic_example'):
            if not isinstance(entry[field], str) or not entry[field].strip():
                errors.append(f'{label}: empty or invalid {field}')
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('entries', type=Path)
    parser.add_argument('sources', type=Path)
    parser.add_argument('--public', action='store_true')
    args = parser.parse_args()
    try:
        entries = [json.loads(line) for line in args.entries.read_text(encoding='utf-8').splitlines() if line.strip()]
        sources = json.loads(args.sources.read_text(encoding='utf-8'))
        errors = validate(entries, sources, args.public)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({'status':'ERROR','message':str(exc)}))
        return 2
    print(json.dumps({'status':'FAIL' if errors else 'PASS','entries':len(entries),
                      'sources':len(sources) if isinstance(sources, list) else None,'errors':errors,
                      'limits':'Does not verify authorship, actual permission, semantic quality, host retrieval, or owner approval.'},indent=2))
    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
