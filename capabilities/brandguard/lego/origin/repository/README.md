# AskJamie-GPT-BRG01
## GPT‑BRG01: LEGO — OKHP³ BrandGuard™
**Motto:** “Only you can protect the bricks from breaking in AI.”

### What this repo is
This repository is the dedicated storage + build space for **GPT‑BRG01: LEGO — OKHP³ BrandGuard™**.  
It’s where the **prompt spine**, **public-only reference corpus**, **compiled knowledge packs**, **evaluation tests**, and **web lens page source** live—so the GPT, Project, and public page stay in sync.

### Canonical links (source of truth)
- LEGO (official): https://www.lego.com  
- Public lens page: https://askjamie.bot/lens-system/okhp3-brandguard/lego/index.html  
- Web source mirror (existing path in AskJamie repo):  
  https://github.com/OKHP3/AskJamie/blob/main/lens-system/okhp3-brandguard/lego/index.html  
- ChatGPT Project (workbench):  
  https://chatgpt.com/g/g-p-694a1990f2c48191870a266837c871b7-gpt-brg01-lego-okhp3-brandguardtm/project  
- Notion spec / ops page:  
  https://www.notion.so/overkillhill/BRG01-LEGO-BrandGuard-Sentinel-40613fd8a8f1413bb3c1e0c1055a2725  
- Custom GPT:  
  https://chatgpt.com/g/g-694adab7e534819197ebfce0f5862c21-lego  

### Current repository layout
- `/knowledge/` - 17 public-source topic sets, each in DOCX and PDF form, with `v01a` and `v01d` variants. The repository does not yet define which variant is authoritative.
- `/web/` - implemented static lens page source.
- `/ops/` - technology-version audit script and metadata.
- `/docs/` - technology inventory.
- `/.agents/` - repository-local prompts and a broad Agent Skills suite. Its catalog is generated and must remain synchronized with the packages present.
- `/skills/` - project-local skill promotion package and its evaluation/provenance records.

### Planned but not implemented
- `/prompts/` - instruction spine, tone rules, and guardrails
- `/corpus/` - curated text-first reference layer
- `/packs/` - compiled knowledge packs for uploads
- `/eval/` - regression prompts and rubrics
- `/rag-source/` - retrieval source layer
- `/releases/` - release artifacts
- `/src/` and `/tests/` - application source and automated tests, if a future implementation needs them

### Operating principles
- **Public-only**: do not store private, licensed, or internal LEGO materials here.
- **Route to official**: when uncertain, direct users to https://www.lego.com.
- **BrandGuard intent**: keep outputs aligned to tone, ethics, and identity safety.

### Update — 2025-12-23
- Initialized **AskJamie-GPT-BRG01** as the dedicated repo for BRG01.
- Next steps: seed `/prompts`, add a first `/packs/knowledge-pack.md`, and mirror the public lens page source into `/web`.

_Disclaimer: LEGO is a trademark of the LEGO Group. This project is independent and not endorsed or affiliated._
