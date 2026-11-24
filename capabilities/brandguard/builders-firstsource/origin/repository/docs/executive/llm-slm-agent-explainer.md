# LLM vs SLM vs Agent — Executive Explainer

## Purpose

Clarify the difference between foundation models, small language models, and business-specific agents so the BFS BrandGuard work is discussed with architectural precision.

## Plain-English Definitions

| Term | What it is | What it is not | BFS relevance |
|---|---|---|---|
| LLM — Large Language Model | A cloud-scale foundation model such as GPT, Gemini, Claude, or similar. It provides broad language, reasoning, and multimodal capability. | Not a BFS-specific asset by default. | The engine beneath public GPTs, Copilot experiences, and other model-powered interfaces. |
| SLM — Small Language Model | A smaller model architecture optimized for cost, latency, privacy, edge, or private/on-prem workloads. | Not created merely by uploading files to a GPT. | Potential future option for narrow, private, cost-sensitive BFS workloads. |
| Custom GPT / Gemini Gem / Copilot Agent | A business-specific agent layer wrapping a model with instructions, knowledge, tools, workflows, and guardrails. | Not a new model architecture. | The current BFS BrandGuard prototype fits here. |

## Critical Distinction

Attaching 20 files to a Custom GPT, or hundreds of SharePoint documents to a Copilot Agent, does not create an SLM. It creates a specialized agent experience on top of an existing model.

## BFS Translation

- Copilot: internal employee productivity and workflow assistance.
- MoveWorks / Paradigm / other private assistants: internal or portal-bound employee/customer workflow helpers.
- myBLDR: transactional customer portal for orders, quotes, documents, projects, and account activity.
- BFS BrandGuard: public-facing discovery and education agent that routes users toward official BFS channels.

## Executive Soundbite

Copilot helps BFS employees work smarter. myBLDR helps BFS customers transact and manage projects. BrandGuard helps the outside world discover, understand, and route toward BFS correctly in AI-mediated search.

## Non-Negotiable Boundary

BFS BrandGuard should not be described as an SLM unless BFS actually trains, fine-tunes, or deploys a separate small model architecture. The correct description is: public-facing custom agent / GPT / Gem built on top of a foundation model.