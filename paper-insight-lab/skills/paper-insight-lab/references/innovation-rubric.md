# Innovation Rubric

Use this reference when the user asks for innovation points, research gaps, future work, project ideas, or paper-based research directions.

## Research Gap Sources

Look for gaps in these places:

- Assumptions: the method depends on clean labels, fixed prompts, static data, known schema, closed-set classes, single language, or controlled users.
- Data: narrow domains, small benchmarks, synthetic data, missing long-tail cases, weak annotation quality, or unreported leakage checks.
- Evaluation: missing ablations, missing strong baselines, single metric, no robustness tests, no cost/latency analysis, no human study when user behavior matters.
- Generalization: untested domains, languages, scales, modalities, time periods, or deployment environments.
- Mechanism: unclear why the method works, missing error taxonomy, missing causal explanation, or no sensitivity analysis.
- System constraints: compute cost, memory, privacy, safety, maintainability, monitoring, or integration friction.
- User value: unclear workflow fit, no decision impact, no comparison with existing practitioner behavior.

## Idea Quality Scale

Score each idea from 1 to 5:

- 1: Vague direction with no experiment.
- 2: Plausible but too broad or weakly connected to the paper.
- 3: Testable extension with a clear baseline and metric.
- 4: Strong idea with a concrete hypothesis, feasible experiment, and meaningful expected insight.
- 5: Publication-grade direction with a sharp gap, defensible novelty, strong evaluation design, and clear risk handling.

Prefer fewer stronger ideas over many generic suggestions.

## Innovation Candidate Contract

Every candidate must include:

| Field | Meaning |
| --- | --- |
| idea | One sentence describing the proposed innovation. |
| evidence from paper | The exact paper finding, limitation, assumption, or result motivating it. |
| gap or limitation | Why the existing paper leaves room for this idea. |
| proposed experiment | A concrete experiment, ablation, prototype, or analysis. |
| feasibility | High, medium, or low, with one reason. |
| risk | The main reason it might fail or be uninteresting. |
| next action | The smallest useful next step. |

## Useful Innovation Patterns

- Replace a hidden assumption with a learnable or adaptive component.
- Move from single-domain evaluation to cross-domain stress testing.
- Add an ablation that separates representation, retrieval, optimization, and prompting effects.
- Build an error taxonomy, then target the largest error bucket.
- Compress or distill the method while tracking quality/cost tradeoffs.
- Add uncertainty estimation or confidence-aware fallback.
- Turn an offline method into an interactive workflow with user feedback.
- Reframe a benchmark so it measures the real task more directly.

## Anti-Patterns

Avoid:
- "Apply it to more datasets" without saying which datasets and why.
- "Improve accuracy" without a mechanism.
- "Use LLMs" as a complete idea.
- Ideas that require unavailable data, impossible compute, or undefined evaluation.
- Treating the paper's own future-work paragraph as automatically novel.

## Final Ranking

When ranking ideas, prioritize:

1. Tight connection to a paper limitation.
2. Clear experimental validation.
3. Feasible first step.
4. Potential to produce a publishable claim or a useful tool.
5. Low risk of being merely an implementation detail.
