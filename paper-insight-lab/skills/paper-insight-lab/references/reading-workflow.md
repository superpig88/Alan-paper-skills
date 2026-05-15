# Reading Workflow

Use this workflow for non-trivial academic papers. Keep the final note useful for future writing, experiments, and literature comparison.

## Input Resolution

Classify the source before reading:

- Local PDF: extract text with `scripts/extract_pdf_text.py`.
- arXiv URL or ID: preserve the arXiv identifier in metadata; fetch only if browsing is available and needed.
- DOI URL or DOI string: preserve the DOI; verify metadata only when browsing or a provided citation is available.
- Paper webpage: cite the page URL and distinguish page metadata from paper content.
- Pasted text: record `source: pasted text` and do not invent missing bibliographic fields.

If the paper is inaccessible, ask for the PDF or extracted text.

## Three-Pass Reading

### Pass 1: Orientation

Extract:
- Title, authors, year, venue, URL/DOI/arXiv if available.
- Research problem and motivation.
- Main claim in one or two sentences.
- Where the evidence lives: experiments, theorem, ablation, case study, user study, dataset analysis.

Stop early if the input is clearly not a paper or extraction is unusable.

### Pass 2: Mechanism

Map the method:
- Inputs and outputs.
- Core model, algorithm, system, or theoretical construction.
- Key assumptions.
- Training/inference/evaluation pipeline if relevant.
- What is new compared with the paper's stated baselines or related work.

Write this in your own words. Quote only short phrases when terminology matters.

### Pass 3: Evidence and Boundaries

Interrogate the evidence:
- Which datasets, benchmarks, tasks, metrics, or proofs support the claims?
- Which ablations isolate the proposed contribution?
- Which comparisons are missing or weak?
- What assumptions limit external validity?
- Where might the method fail under distribution shift, scale changes, user behavior, deployment constraints, or different domains?

Classify each important judgment as:
- `paper evidence`: directly supported by the paper.
- `inference`: reasoned from the paper but not directly stated.
- `needs verification`: requires external checking or reproduction.

## Note Generation

Use `assets/templates/paper-note.md`. Keep the note skimmable:
- TL;DR should be no more than 3 bullets.
- Contributions should be evidence-backed, not marketing-style.
- Limitations should include both stated limitations and inferred limitations, labeled separately.
- Research gaps should be testable.
- Questions should be useful for a future reading group, experiment, or writing task.

## Failure Modes

- Low-quality extraction: report pages or sections that are missing; avoid over-confident analysis.
- Missing metadata: mark as `unknown`.
- Formula-heavy paper: preserve formula names and theorem numbers; avoid pretending to verify proofs unless actually checked.
- Survey paper: emphasize taxonomy, coverage, blind spots, and how it reframes the field rather than treating it like a single-method paper.
- Empirical paper without code: include reproducibility risks and required artifacts.
