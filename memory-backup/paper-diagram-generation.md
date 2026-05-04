---
name: 论文配图生成流水线
description: MBSE+PLE 论文配图全套流程：审稿→改稿→Word排版→绘图→SVG修复→Inkscape
type: project
originSessionId: 74b8df90-8071-465a-8921-68d0980f5ad4
---
# 论文配图生成项目

**项目路径**: `E:\.Claude Code Project\4.论文配图版_20260502\`
**图表源文件**: `E:\.Claude Code Project\diagrams\` (10 PNG + 10 SVG)
**原始论文**: `C:\Users\hasee\Downloads\智能汽车信息物理系统中MBSE与PLE的融合应用.docx`

## 项目内容

智能汽车信息物理系统 (IVCPS) 中 MBSE 与 PLE 融合应用的工程论文，包含：
- 论文审稿意见与修改
- Word 文档生成 (python-docx, 匹配原始格式)
- 10 张 SysML/逻辑示意图 (matplotlib 初版 → 原生 SVG 重写)
- Inkscape 安装用于 SVG 编辑

## 关键技术点

1. **python-docx 生成 Word**: 表格、图片嵌入、中文字体设置、段落格式
2. **原生 SVG 生成**: 使用 `<rect>`, `<text>`, `<line>`, `<marker>` 而非 matplotlib 渲染，确保 draw.io 可编辑
3. **PowerShell here-string 写 Python 文件**: 避免中文内容编码损坏
4. **Inkscape 安装**: `winget install Inkscape.Inkscape` → `C:\Program Files\Inkscape\bin\inkscape.exe`

## 10 张图表清单

| 编号 | 文件名 | 内容 |
|------|--------|------|
| Fig1 | Fig1_VModel_RFLP | V模型 + RFLP 融合开发流程 |
| Fig2 | Fig2_RequirementTypes | IVCPS 需求类型分解树 |
| Fig3 | Fig3_BDD | BDD 顶层模块定义 (2×4 grid) |
| Fig4 | Fig4_SC_SSC | SC-SSC 子系统分解 (IBD) |
| Fig5 | Fig5_NetworkTopology | 网络拓扑与 ECU 分配 |
| Fig6 | Fig6_TagHierarchy | PLE 三级标签体系 |
| Fig7 | Fig7_SSC_Branching | SSC 多分支版本管理 |
| Fig8 | Fig8_ECU_Model | ECU 150% 模型与变体绑定 |
| Fig9 | Fig9_SignalFeatureTag | 信号特征标签分配冲突解决 |
| Fig10 | Fig10_BaselineFlow | 基线生成与交付流水线 |

## SVG 生成脚本

- **初版**: `C:\Users\hasee\redraw_diagrams.py` (matplotlib, 不可编辑)
- **终版**: `C:\Users\hasee\gen_native_svg.py` (原生 SVG, draw.io 可编辑)
- **Word构建**: `C:\Users\hasee\build_final.py`

## 常见问题

- SVG 在 draw.io 中无法编辑 → 因为是 matplotlib 渲染模式，需用原生 SVG 元素重新生成
- PowerShell 写中文 Python 文件编码错误 → 用 here-string `@"..."@` + `Out-File -Encoding UTF8`
