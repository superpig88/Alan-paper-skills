# Paper Insight Lab

Paper Insight Lab 是一个面向个人研究工作的 Codex Skill，用来帮助你阅读论文、提炼贡献、发现研究缺口、生成 Markdown 笔记，并维护 GitHub 友好的文献矩阵。

它的设计目标不是替你“快速总结一篇论文”这么简单，而是把论文阅读变成一个可复用的研究流程：先抓住问题和证据，再判断方法边界，最后产出可继续推进的创新点候选。

## What It Does

- 从 PDF、本地路径、arXiv/DOI/论文 URL 开始阅读任务
- 提取论文核心问题、方法、实验、贡献和限制
- 生成中文为主的 Markdown 论文笔记，保留英文术语、公式和关键原文短语
- 从论文假设、数据、方法、评估和应用边界中寻找研究缺口
- 输出带证据、风险和实验方案的创新点候选
- 扫描笔记目录并生成 `literature-matrix.md`

## Repository Layout

```text
paper-insight-lab/
  README.md
  requirements.txt
  examples/
    example-paper-note.md
    literature-matrix.md
  skills/
    paper-insight-lab/
      SKILL.md
      agents/
        openai.yaml
      references/
        reading-workflow.md
        innovation-rubric.md
        note-schema.md
      assets/
        templates/
          paper-note.md
          literature-matrix.md
      scripts/
        extract_pdf_text.py
        init_paper_note.py
        update_literature_matrix.py
```

## Install

To use this as a Codex Skill, copy or symlink `skills/paper-insight-lab` into your Codex skills directory.

```powershell
# Windows example
Copy-Item -Recurse .\skills\paper-insight-lab $env:USERPROFILE\.codex\skills\
```

Optional PDF extraction dependencies:

```bash
pip install -r requirements.txt
```

The skill can still guide reading from already extracted text or pasted paper content without these dependencies.

## Quick Start

Create a note from metadata:

```bash
python skills/paper-insight-lab/scripts/init_paper_note.py ^
  --title "Your Paper Title" ^
  --authors "A. Author; B. Author" ^
  --year 2026 ^
  --venue "arXiv" ^
  --tags "llm,reasoning,paper-reading"
```

Extract text from a PDF:

```bash
python skills/paper-insight-lab/scripts/extract_pdf_text.py paper.pdf --output notes/extracted/paper.md
```

Update the literature matrix:

```bash
python skills/paper-insight-lab/scripts/update_literature_matrix.py --notes-dir notes
```

## Output Philosophy

Every strong claim should be tied to paper evidence. Every speculative idea should be labeled as inference. Every innovation candidate should include a concrete validation path, not just a nice-sounding direction.

The default note language is Chinese, but important English terms should stay visible so the note remains useful for writing, searching, and discussion.

## Example

See:

- [Example paper note](examples/example-paper-note.md)
- [Example literature matrix](examples/literature-matrix.md)

The examples are synthetic and meant to show structure, not cite real findings.
