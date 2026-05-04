---
name: Installed Skills (2026-04-26)
description: Skills installed on 2026-04-26 covering academic paper, patent, and book distillation workflows
type: project
---

Installed 5 Claude Code skills on 2026-04-26:

1. **cangjie-skill** - book2skill: distill books into executable agent skills (RIA-TV++ methodology)
   - GitHub: https://github.com/rdjy11/cangjie-skill

2. **cn-patent-disclosure** - Chinese patent disclosure document writing with Markdown/DOCX delivery
   - GitHub: https://github.com/cycloneha/cn-patent-disclosure-writing-skill

3. **ljg-xray-paper** - Paper X-ray: deconstruct academic papers into cognitive delta cards + ASCII art diagrams
   - GitHub: https://github.com/lijigang/ljg-skill-xray-paper
   - Note: archived repo (read-only, no longer maintained)

4. **academic-paper-strategist** - Academic paper strategist: platform analysis → literature gap → outline with 7-dimension reviewer scoring
   - GitHub: https://github.com/lishix520/academic-paper-skills

5. **academic-paper-composer** - Academic paper composer: from outline to full draft with per-chapter quality checks
   - GitHub: https://github.com/lishix520/academic-paper-skills

**Why:** User wanted to set up a toolkit for academic paper reading/writing, patent disclosure, and book distillation workflows.

**How to apply:** These skills are available in the system. User may ask to use them for paper analysis, paper writing, patent drafting, or book distillation tasks.

## Overlap boundaries (set 2026-04-30)

### cangjie-skill ↔ huashu-nuwa (🔴 resolved)
- **cangjie-skill**: triggered ONLY by explicit BOOK references ("拆书", "把《XX》做成skill", book file paths). NOT for person distillation.
- **huashu-nuwa**: triggered by person names / fuzzy needs. "蒸馏XX" only fires when XX is clearly a person.
- **Ambiguity rule**: When input "蒸馏XX" could be either (e.g., "蒸馏芒格" = person name "Munger" or could refer to "Poor Charlie's Almanack"), MUST ask the user to clarify before proceeding.
- Both SKILL.md files updated with disambiguation sections and mutual references.

### update-config ⊃ fewer-permission-prompts (🟡 kept)
- Keep both. `fewer-permission-prompts` is a high-frequency sub-operation of `update-config`. No merge needed.

### Paper trio (xray / strategist / composer) (🟢 no conflict)
- Natural pipeline: analyze → plan → write. Clear separation of concerns.

### superpowers (obra/superpowers) — 14 skills (🟢 installed 2026-04-30)
- **Repo**: https://github.com/obra/superpowers
- **Version**: 5.0.7
- **Type**: Software development methodology framework (mandatory workflow for code tasks)
- **Domain**: brainstorm → design approval → worktree → plan → TDD → execute → review → finish
- **14 skills installed**: brainstorming, using-git-worktrees, writing-plans, subagent-driven-development, executing-plans, dispatching-parallel-agents, test-driven-development, requesting-code-review, receiving-code-review, systematic-debugging, verification-before-completion, finishing-a-development-branch, writing-skills, using-superpowers
- **Agent installed**: code-reviewer (at ~/.claude/agents/)
- **Hook installed**: SessionStart (injects `using-superpowers` context at session start)
- **Marketplace registered**: obra/superpowers-marketplace

### superpowers ↔ existing skills boundary
- Superpowers = **软件开发方法论** (mandatory for code tasks)
- nuwa/cangjie/xray/patent/composer/strategist/boss-perspective = **知识工作工具** (on-demand, no Superpowers gate)
- **Ambiguity rule**: Software dev → Superpowers; Knowledge work → domain skills; **Unsure → ask user**
- Rules documented in both CLAUDE.md and ~/.claude/CLAUDE.md
