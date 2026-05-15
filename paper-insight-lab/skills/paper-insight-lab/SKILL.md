---
name: paper-insight-lab
description: Read, analyze, and synthesize academic papers from PDFs, arXiv links, DOI links, or paper URLs. Use when Codex needs to extract paper contributions, critique methods, identify research gaps, generate innovation candidates, create Markdown/GitHub research notes, or update a literature matrix.
---

# Paper Insight Lab

## Overview

Use this skill as a personal research assistant for paper reading. Produce Chinese-first Markdown notes, preserve important English terms, and separate paper evidence from model inference.

## Task Boundary

Handle:
- Read papers from local PDFs, extracted text, arXiv/DOI/paper URLs, or pasted content.
- Identify problem, motivation, method, evidence, contributions, limitations, and reproducibility notes.
- Generate research-gap-oriented innovation candidates with experiments and risks.
- Create or update GitHub-friendly Markdown notes and a literature matrix.

Do not:
- Invent citation metadata, benchmark results, claims, or related work.
- Claim a method is SOTA unless the paper or verified external sources support it.
- Replace formal peer review, mathematical proof checking, or full reproducibility audits.
- Download papers or browse the web unless the user asks or the task requires current external verification.

## Core Workflow

1. Resolve the input type: local PDF, local text, URL/DOI/arXiv identifier, or pasted paper content.
2. If the input is a PDF, use `scripts/extract_pdf_text.py` when text extraction is needed.
3. Follow the three-pass reading workflow in `references/reading-workflow.md` for non-trivial papers.
4. Generate the note using `assets/templates/paper-note.md`; read `references/note-schema.md` when field meaning or output shape matters.
5. For innovation discovery, read `references/innovation-rubric.md` and produce evidence-backed candidates.
6. When multiple notes exist, use `scripts/update_literature_matrix.py` to regenerate `notes/literature-matrix.md`.

## Output Contract

Default outputs:
- Single paper note: `notes/<paper-slug>.md`
- Literature matrix: `notes/literature-matrix.md`
- Optional structured summary: `notes/.paper-insight/<paper-slug>.json`

A complete paper note includes:
- Metadata
- TL;DR
- Problem / Motivation
- Core Idea
- Method
- Evidence
- Contributions
- Limitations
- Research Gaps
- Innovation Candidates
- Reproducibility Notes
- Questions
- Citation

## Quality Rules

- Mark every major conclusion as `paper evidence`, `inference`, or `needs verification`.
- Keep Chinese explanations concise; preserve English method names, dataset names, metrics, and equations.
- Do not fill unknown metadata with guessed values. Use `unknown` or leave TODO markers.
- Innovation candidates must include: idea, evidence from paper, gap or limitation, proposed experiment, feasibility, risk, and next action.
- Prefer specific, testable research gaps over broad advice.
- If extraction quality is poor, report the issue before analysis and ask for a cleaner PDF/text when necessary.

## Resource Guide

- Read `references/reading-workflow.md` for the full reading process.
- Read `references/innovation-rubric.md` when the user asks for innovation points, research gaps, project ideas, or future work.
- Read `references/note-schema.md` before creating templates, JSON summaries, or literature matrices.
- Use `assets/templates/paper-note.md` for new notes.
- Use `assets/templates/literature-matrix.md` for a new matrix.

## Completion Checklist

Before finishing, verify:
- The note is valid GitHub Markdown.
- Important claims are tied to evidence or explicitly labeled as inference.
- Innovation candidates include concrete experiments.
- Metadata was not fabricated.
- Any script output path is reported clearly to the user.
