# 飞书文档输出规范

> 流程文档写入飞书云文档的排版标准、Callout 语法和输出策略。

## 排版标准

- **标题层级**：H1 流程名 → H2 模块标题 → H3 子模块
- **表格**：表头加粗，关键数据加粗
- **Callout 必须用 emoji + background-color 语法**：

| 用途 | 语法 |
|------|------|
| 目的/概要 | `<callout emoji="🎯" background-color="light-blue">` |
| KCP 关键控制点 | `<callout emoji="🚨" background-color="light-red">` |
| 注意事项 | `<callout emoji="⚠️" background-color="light-yellow">` |
| 最佳实践 | `<callout emoji="✅" background-color="light-green">` |

## 输出策略

1. `doc_create` 创建文档（标题 + 模块一~三）
2. `doc_append` 逐段追加模块四~七、九~十（每段 ≤3000 字，防 400 错误）
3. **模块八**：飞书内嵌泳道表格 + 流转路径 Callout（`doc_append`），Canvas 泳道图另存 HTML 文件
4. 如需 Mermaid 内嵌：创建独立文档 `doc_create` 写第一段 + `doc_append` 后续段

## 飞书原生泳道表格

飞书文档中嵌入角色×活动矩阵表：

| | ACT-01 | ACT-02 | ... | ACT-N |
|---|---|---|---|---|
| **角色A** | 活动名 | | ... | |
| **角色B** | | 活动名 | ... | |

表格下方 Callout 补充流转路径：

```
<callout emoji="🔄" background-color="light-blue">
**流转路径**
步骤1 → 步骤2 → **KCP1**（不通过 ← 退回） → 步骤3 → ...
</callout>
```

## Mermaid 白板（备选，限飞书内嵌）

- 只有 `doc_create`/`doc_append` 触发渲染
- 回退箭头必须虚线 `-.->|不通过|`
- ≥8 节点必须拆分，每段 ≤6 节点
- `graph LR` 横向，subgraph 标题加引号
- 特殊字符（≤ ≥ % ：）导致解析失败，用中文替代
