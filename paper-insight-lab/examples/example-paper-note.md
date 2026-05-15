---
title: "Adaptive Retrieval for Long-Horizon Research Notes"
authors:
  - "Example Author"
  - "Demo Researcher"
year: 2026
venue: "Synthetic Example"
doi: ""
arxiv: ""
url: ""
tags:
  - retrieval
  - research-notes
status: read
confidence: medium
---

# Adaptive Retrieval for Long-Horizon Research Notes

> Synthetic example. This note demonstrates structure only and does not describe a real paper.

## TL;DR

- 论文提出一个 adaptive retrieval workflow，用于在长期研究笔记中动态选择上下文。
- 主要证据来自两个合成任务和一个小规模用户研究。
- 最大研究缺口是缺少真实跨月研究项目中的外部效度验证。

## Problem / Motivation

长期研究笔记会不断增长，固定 top-k 检索容易把过时或局部相关的笔记塞进上下文，导致推理噪声增加。

## Core Idea

核心想法是让检索器先判断任务类型，再选择 query expansion、recency weighting 和 evidence diversity 三种策略的组合。

## Method

输入是用户问题和笔记库，输出是一组带证据类型标签的上下文片段。方法包含任务分类、候选召回、多目标重排和证据覆盖检查。

## Evidence

| Claim | Paper evidence | Notes |
| --- | --- | --- |
| Adaptive retrieval improves answer grounding | Synthetic benchmark shows higher citation precision | paper evidence |
| It may help real researchers over long projects | Small user study reports lower perceived search effort | needs verification |

## Contributions

- 提出面向长期研究笔记的 adaptive retrieval pipeline。
- 引入 evidence diversity 指标，避免上下文只来自同一类笔记。

## Limitations

### Stated by Paper

- 用户研究规模小。
- 任务集中在英文笔记。

### Inferred

- inference: 如果笔记本身质量不高，检索策略可能只会更有效地召回低质量内容。

## Research Gaps

- 在真实跨月研究项目中验证 adaptive retrieval 是否降低写作和复现实验成本。
- 测试中文、双语、公式密集型笔记下的检索稳定性。

## Innovation Candidates

| Idea | Evidence from paper | Gap or limitation | Proposed experiment | Feasibility | Risk | Next action |
| --- | --- | --- | --- | --- | --- | --- |
| Add citation-aware confidence calibration | Current evidence tags are rule-based | Confidence is not calibrated against factual error | Compare calibrated vs uncalibrated retrieval on citation precision | Medium | Needs labeled errors | Build a 50-question evaluation set |
| Evaluate on real research timelines | Paper uses mostly synthetic tasks | External validity is weak | Run a four-week diary study with active researchers | Medium | Recruiting cost | Define logging protocol |

## Reproducibility Notes

- Code: unknown
- Data: synthetic examples described, raw files unknown
- Compute: likely modest
- Key missing details: user study prompts and annotation guidelines

## Questions

- How sensitive is the method to noisy note titles?
- Does recency weighting hurt rediscovery of older foundational notes?

## Citation

```bibtex
@misc{synthetic2026adaptive,
  title = {Adaptive Retrieval for Long-Horizon Research Notes},
  author = {Example Author and Demo Researcher},
  year = {2026},
  note = {Synthetic example for Paper Insight Lab}
}
```
