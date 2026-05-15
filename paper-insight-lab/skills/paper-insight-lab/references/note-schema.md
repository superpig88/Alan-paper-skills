# Note Schema

Use this schema for Markdown notes, literature matrices, and optional JSON summaries.

## Markdown Frontmatter

```yaml
---
title: "Paper title"
authors:
  - "Author One"
  - "Author Two"
year: 2026
venue: "unknown"
doi: ""
arxiv: ""
url: ""
tags:
  - paper-reading
status: unread
confidence: medium
---
```

Rules:
- Use `unknown` for unknown venue/year when needed.
- Use empty strings for missing DOI, arXiv, or URL.
- Do not invent authors or venues.
- `status` should be one of `unread`, `skimmed`, `read`, `deep-read`, `implemented`, `cited`.
- `confidence` should be `low`, `medium`, or `high`, based on extraction quality and reading depth.

## Required Sections

Use these headings exactly for script compatibility:

```markdown
## TL;DR
## Problem / Motivation
## Core Idea
## Method
## Evidence
## Contributions
## Limitations
## Research Gaps
## Innovation Candidates
## Reproducibility Notes
## Questions
## Citation
```

## Innovation Candidate Table

```markdown
| Idea | Evidence from paper | Gap or limitation | Proposed experiment | Feasibility | Risk | Next action |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
```

## Literature Matrix Columns

Use these columns for `notes/literature-matrix.md`:

| Column | Source |
| --- | --- |
| Paper | `title` plus note link |
| Year | frontmatter `year` |
| Venue | frontmatter `venue` |
| Status | frontmatter `status` |
| Tags | frontmatter `tags` |
| TL;DR | first bullet or paragraph under `## TL;DR` |
| Gaps | compact summary under `## Research Gaps` |

## Optional JSON Summary

```json
{
  "title": "",
  "authors": [],
  "year": null,
  "venue": "",
  "source": {
    "doi": "",
    "arxiv": "",
    "url": ""
  },
  "tldr": [],
  "contributions": [],
  "limitations": [],
  "research_gaps": [],
  "innovation_candidates": [
    {
      "idea": "",
      "evidence_from_paper": "",
      "gap_or_limitation": "",
      "proposed_experiment": "",
      "feasibility": "",
      "risk": "",
      "next_action": ""
    }
  ]
}
```
