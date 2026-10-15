---
name: claude-model-alias-mapping
description: 本机 Claude Code 走 DeepSeek 代理，haiku/sonnet/inherit 三者映射同一模型，仅 opus 不同——做模型档位决策前必读
metadata:
  node_type: memory
  type: user
  originSessionId: c4b75c45-a383-4100-ae7a-760125b5ec82
  modified: 2026-10-15T14:31:15.138Z
---

本机 Claude Code 不直连 Anthropic，而是走 **DeepSeek 的 Anthropic 兼容端点**。`~/.claude/settings.json` 里：

```
ANTHROPIC_BASE_URL             = https://api.deepseek.com/anthropic
ANTHROPIC_DEFAULT_HAIKU_MODEL  = deepseek-flash
ANTHROPIC_DEFAULT_SONNET_MODEL = deepseek-flash
ANTHROPIC_DEFAULT_OPUS_MODEL   = deepseek-v4-pro[1M]
"model": "sonnet"          ← 会话默认
```

**决定性推论：`haiku` ＝ `sonnet` ＝ `inherit`，三者是同一枚模型。** 只有在 frontmatter / 参数里写 `opus` 才会落到更强的 `deepseek-v4-pro[1M]`。

**实测确认（2026-10-15）**：subagent frontmatter 里的 `model: opus` **确实**解析为 `deepseek-v4-pro[1M]`（派探针 subagent 实证，非推断）。

**Why:** 这个映射不读 settings.json 是看不出来的——很容易误以为 `sonnet` / `haiku` / `opus` 是三档不同模型，从而在设计 agent 成本策略时做出错误权衡（比如为了"省钱"把某角色从 `sonnet` 降到 `haiku`，实际零收益）。

**How to apply:** 任何涉及「选哪个模型档」的决定，先套这个映射，再谈取舍。要点：

- 写 `sonnet` 与写 `inherit` **今日等价**；锁 `sonnet` 的价值是**成本保险**——会话若被切到 `opus`，未锁档的 agent（尤其并行派发的那些）会被一起带贵；
- 想省钱时，降 `sonnet→haiku` **没有意义**（同一个模型）；要省只能省「调用次数」或「上下文规模」；
- 想提质时，唯一有效动作是升到 `opus`，且要单次、高价值的调用才划算（如编排/路由，而非并行铺开的检索型 agent）。

安全提示：`settings.json` 里含 `ANTHROPIC_API_KEY` 明文，**绝不可外发**（该 Key 历史上已因公开仓库泄露过一次，见 [[auto-backup-workflow]]）。

关联：[[basetech-engineer-agent]] [[user-profile]]
