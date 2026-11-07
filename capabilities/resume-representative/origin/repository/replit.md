# AskJamie - GPT-AJ01: Resume Representative

## Project Overview

This is a documentation and prompt repository for a custom AI agent (GPT) designed to represent a user's professional background. It is NOT a runnable web application.

The project serves as the source of truth for:
- AI agent system prompts (`prompts/`)
- Knowledge base documents (`knowledge/`, `rag-source/`)
- Evaluation tests and rubrics (`eval/`)
- Release checklists (`ops/`)
- Project metadata (`gpt_manifest.yaml`)

## Structure

- `prompts/` - Instruction architecture, role definitions, tone, guardrails
- `knowledge/` - Starter kit for hiring patterns and ATS-friendly structures
- `rag-source/` - Original documents for Retrieval-Augmented Generation
- `eval/` - Regression prompts and rubrics
- `ops/` - Release checklists and maintenance notes
- `site/` / `web/` - Placeholders for potential future web frontends
- `gpt_manifest.yaml` - Central tracking file for versioning and metadata

## Usage

This repository is managed manually. The "build" process involves compiling prompt templates and knowledge documents for upload to the OpenAI Custom GPT interface.

## User Preferences

- Follow brand rules defined in `AGENTS.md` and `CLAUDE.md`
- No em dashes
- Follow the ROY principle as defined in AGENTS.md
