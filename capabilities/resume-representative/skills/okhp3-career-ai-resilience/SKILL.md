---
name: okhp3-career-ai-resilience
description: >
  Evaluate career resilience and earning-capacity scenarios under AI-driven task
  change. Use when comparing experience, seniority, agent leverage and labor
  market exposure across 5, 10 or 25 years. Produces an evidence-tiered career
  scenario ledger and concrete positioning experiments, not a precise risk
  percentile, guaranteed salary forecast or age-based candidate ranking.
license: MIT
compatibility: Agent Skills-compatible client with access to supplied evidence. Live job, pay and labor statistics require an authorized retrieval adapter.
metadata:
  author: Jamie Hill (OverKill Hill P³)
  version: 0.1.0
  category: career-operations
  origin: okhp3/askjamie-foundry
  homepage: https://overkillhill.com
  author-github: https://github.com/OKHP3
  in_scope: "Career skill resilience, AI augmentation, task exposure, scenario planning and market positioning."
  out_of_scope: "Individual hiring decisions, unsupported salary guarantees, medical assessment, résumé changes or automatic applications."
---

# okhp3-career-ai-resilience

**OverKill Hill P³** · [overkillhill.com](https://overkillhill.com) · [github.com/OKHP3](https://github.com/OKHP3)

Translate a career history and target job family into an evidence-qualified set of resilience scenarios. Distinguish **task substitutability**, **role demand**, **market access**, **earning power** and **adaptive capacity**. AI exposure is not a probability of unemployment. Experience is valuable only when the market rewards the outcomes it enables.

## Inputs and boundary

Accept an authorized career-evidence summary, current/target role families, geography or remote constraints, compensation baseline if voluntarily supplied, evidence as-of date, 5/10/25-year horizons and the person's goals. Proceed with explicit unknowns instead of asking for sensitive personal information. Never infer capability, suitability, longevity or cognitive ability from age, degree, gender, disability or other protected traits. For cognitive concerns, frame AI as optional support for information retrieval and organization, not as a medical treatment or guaranteed prevention of decline. Do not invent accomplishments, education, salary or current employment.

## Method

1. **Set an evidence horizon.** Separate historical observed career facts, present labor-market indicators, employer statements, research hypotheses, the candidate's account and speculative future scenarios. Date every market claim and note the geography and comparator. For a request about an individual's history, compose with the existing `okhp3-career-evidence-canon` rather than changing the canonical record.
2. **Decompose roles into work.** Map recurring tasks, required outcomes, decision rights, customer/stakeholder dependence, physical-world interfaces, domain depth, security exposure and accountability. Assign `substitution pressure` and `augmentation opportunity` separately with qualitative labels and reasoning. High exposure can mean high productivity gains rather than job disappearance.
3. **Map durable capabilities.** Identify credible evidence of problem framing, tacit knowledge, technical integration, judgment under ambiguity, commercial ownership, communication, validated delivery and agent governance. Differentiate used tools from demonstrated business outcomes. AI-assisted output without independent verification is not proof of expertise.
4. **Construct three scenarios.** For each horizon (5/10/25 years), describe a favorable, reference and adverse scenario conditional on specific drivers: employer adoption, market demand, wage bargaining, regulations, available junior opportunities, tool progress, mentoring, alternative employment routes and macroeconomic conditions. Treat long-horizon estimates as increasingly uncertain. Never present a point percentile such as 'safer than 85% of workers' without a defined reference population, dataset and calibrated model.
5. **Model comparative learning pathways.** Compare an experienced professional and an early-career worker in terms of access to learning repetitions, mentorship, feedback, AI augmentation, measured proficiency and task ownership, not age-based worth. Model two opposing AI effects: automation may remove entry-level practice; AI tutoring and deliberately redesigned apprenticeships may accelerate it. Do not assume juniors are AI-naive or experienced workers will inevitably decline.
6. **Assess economic resilience.** Separate income levels, purchasing-power/inflation, wage growth, occupation switching, income volatility and employment probability. If projecting real or nominal pay, disclose base, inflation treatment, growth assumptions, source and uncertainty. Never imply that workers commonly double/triple earnings by predetermined years or fall back to starting pay without cohort evidence. Identify pathways to higher earnings tied to accountability and business impact, not agent count.
7. **Design a testable hedge.** Select 2–4 reversible career moves tied to evidence gaps: quantified AI-enabled delivery case, domain-specific portfolio example, accountable transformation ownership, stakeholder outcome, certification where genuinely earned, mentoring or cross-functional immersion. Each experiment states proof artifact, target audience, review date, potential downside and stop/pivot rule.
8. **Review and hand off.** Return the scenario ledger and an explicit uncertainty note. If current wage/job data are unavailable, mark the market component `not-verified-current`; do not manufacture statistics. Leave any résumé edit, application, networking action or external publication to the existing authorized companion skill.

## Output

Deliver: `career_scope`, `evidence_register` (claim ID, source, date, tier), `task_exposure_map`, `comparative_learning_paths`, `scenario_matrix` (horizon, conditional assumptions, range or qualitative band, triggers, disconfirming signal), `earning_capacity_levers`, `90_day_experiments`, `uncertainties`, `source_and_permission_gaps`.

Load [scenario contract](references/scenario-contract.md) for the evidence and decision vocabulary. If the user wants a tailored résumé rather than career scenario analysis, route to `okhp3-targeted-resume`; for a particular offer use `okhp3-offer-decision`; for vacancy discovery use the dedicated job-search workflow. No unapproved external actions.

## Adjudication

For consequential claims, compose with `okhp3-equilibrium-review` when available: evidence review checks attribution and cohort applicability, outcome review checks actionable decisions, safety/portability review checks discrimination, privacy, medical and forecasting limits. Record falsifiable downside cases. Human or independent agent review is valuable, but one model writing three reviews is not independent adjudication. Keep `defer-for-evidence` when critical market or identity claims are unsupported.

[Development evaluations](evals/evals.json) are synthetic, visible during authoring. No live with/without-skill comparison or unseen holdout is claimed.

## About

Built by [Jamie Hill](https://overkillhill.com) · [OverKill Hill P³](https://overkillhill.com)
Published at [github.com/OKHP3](https://github.com/OKHP3)
Part of [AskJamie FoundRy](https://github.com/OKHP3/askjamie-foundry).
MIT License -- free to use, fork, and adapt.
