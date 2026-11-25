# AskJamie GPT and plugin inventory

On November 24, 2026, the owner's My GPTs list contained 89 entries. Four displayed titles contained `AskJamie`, ignoring capitalization. Each row identifies one original GPT. A ChatGPT migration result records the host's conversion, while an exact source capture requires the original instructions, starter text and attachment bytes. [Owner's My GPTs](https://chatgpt.com/gpts/mine) · [Integration record](https://github.com/OKHP3/askjamie-foundry/issues/234)

| GPT | Original | ChatGPT migration observed | FoundRy material |
| --- | --- | --- | --- |
| AJ01, Résumé Representative | [GPT](https://chatgpt.com/g/g-691fb05c86c881919eec171e62fe1e00) | Successfully migrated, one cloud skill. [Plugin](https://chatgpt.com/plugins/plugin_85e9ceacaf6081918bf7e533d704becb) | [Configuration and six starters](../../capabilities/resume-representative/origin/gpt-config/2026-10-29-v3/config.yaml) · [Original instructions](../../capabilities/resume-representative/origin/gpt-config/2026-10-29-v3/instructions.md) · [Portable skill](../../capabilities/resume-representative/skills/resume-representative/SKILL.md) |
| AJ02, Professional Portfolio | [GPT](https://chatgpt.com/g/g-691fa5845230819199d4ffb89b13e9ab) | Successfully migrated, one cloud skill. [Plugin](https://chatgpt.com/plugins/plugin_66eac919e61881919eac8cab7b0e9e53) | [Configuration](../../capabilities/professional-portfolio/origin/gpt-config/2026-10-29/config.yaml) · [Original instructions](../../capabilities/professional-portfolio/origin/gpt-config/2026-10-29/instructions.txt) · [Portable skill](../../capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md) |
| AJ03, Enterprise Sleuth | [GPT](https://chatgpt.com/g/g-691f9a52f5088191b4f552770ffb5886) | Verification pending | [Legacy source](../../capabilities/enterprise-sleuth/origin/source.json) |
| AJ04, OKHP3 BrandGuard | [GPT](https://chatgpt.com/g/g-691fa3532a588191b5b362f2fc07e8b3) | Verification pending | [Legacy source](../../capabilities/brandguard/origin/source.json) |

## Source coverage

The October 29 captures preserve AJ01 and AJ02's instruction text. The source Git blobs reproduce the UTF-8 captures exactly. Their SHA-256 digests are `351329c1b0f5fce5d530ea1ec252da7260133caf056c9279410a85baa1639a47` (AJ01) and `7ed808416bbca681413e1931f8a748c50c25151a4e0569bd578e2d575e75387f` (AJ02). The AJ01 configuration names two PNG attachments and lists six conversation starters. The AJ02 editor showed one PNG attachment and eight populated conversation starters. The October capture did not recover any of the three attachment originals.

AJ01's instructions refer to six additional text sources. They were absent from the GPT attachment list. Related documents in its repository and ChatGPT project have separate provenance. The two FoundRy portable skills have version-specific Replit acceptance records. Equivalence between either FoundRy procedure and its hosted ChatGPT skill requires a direct comparison. [AJ01 acceptance](../../capabilities/resume-representative/docs/skill-candidate-acceptance.md) · [AJ02 acceptance](../../capabilities/professional-portfolio/docs/skill-candidate-acceptance.md)

## Related organization titles

The public AskJamie portfolio identifies twelve BrandGuard editions by GPT ID. They cover LEGO, Starbucks, Brooks Running, PING, Costco, Hershey, LVMH, Dollar General, Coca-Cola, Discount Tire, SCHEELS and Mathews Archery. The portfolio maps LEGO to the catalog alias “Brick Toys — Billund in 1932”. It also identifies “BFS: Framing Intelligent Futures” as BFS01. The catalog also showed BLDR and Builders FirstSource. Those names alone do not establish which legacy capability or plugin each represents. [Portfolio GPT identity map](https://github.com/OKHP3/askjamie/blob/ebe80378a67adc47c3429ddb5a3adf3bc72cd00e/scripts/check-public-gpt-links.py)

The 17 Enterprise Sleuth and BrandGuard legacy-repository transfers have their own source identities and preservation records. Reconciliation of an organization's hosted GPT with those records requires the GPT ID and its saved configuration. [Legacy repository transfer](legacy-capability-transfer.md)
