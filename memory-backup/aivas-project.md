---
name: AIVAS 智能汽车架构系统
description: AI-Native 智能汽车架构开发系统 (FastAPI+React+LangGraph+Neo4j)，基于MBSE+PLE论文方法论，10个AI Agent驱动，唤醒词见下
type: project
originSessionId: 74b8df90-8071-465a-8921-68d0980f5ad4
lastAuditDate: 2026-05-04
---

# AIVAS — AI-Native Vehicle Architecture System

**项目路径**: `E:\.Claude Code Project\5.AIVAS智能汽车架构系统_20260503\`
**技术方案**: `C:\Users\hasee\.claude\plans\jazzy-finding-brook.md`
**状态**: Phase 1 MVP 基础骨架已完成 (2026-05-03)，71 个文件，审计日期 2026-05-04
**下次唤醒**: 继续执行 6 阶段开发计划（详见下方）

## 唤醒词

「AIVAS」「智能汽车架构」「AI-Native架构」「汽车架构开发系统」「MBSE系统」「PLE系统」「RFLP引擎」「150%模型」「基线流水线」「Agent汽车」

## 核心架构 (7层)

```
展示层: React 18 + @xyflow/react + shadcn/ui + Zustand
API网关: Strawberry GraphQL + FastAPI REST
应用引擎: RFLP引擎 | PLE引擎 | SSC版本管理 | 基线流水线
AI Agent: 10个专业Agent + Orchestrator路由 + LangGraph状态机
知识层: pgvector RAG + Neo4j图 + Prompt模板库
数据层: PostgreSQL 16 + Neo4j 5 + Redis 7 + MinIO
集成层: AUTOSAR/SysML v2/ReqIF
```

## 基础设施状态

- **PostgreSQL 16**: 已从 C:\ 迁移至 E:\PostgreSQL\16，服务正常运行，数据目录 `E:\PostgreSQL\16\data`
- **数据库**: `aivas` 数据库已建14张表，数据完整
- **连接**: `localhost:5432`，用户 `aivas/aivas_dev`，通过 psql 验证通过
- **Docker**: 未安装，当前使用本地 PostgreSQL
- **Neo4j / Redis / MinIO**: 未启动（依赖 Docker）
- **AIVAS_LLM_API_KEY**: 未配置（需用户填写 Anthropic key）

## 10 个 AI Agent

| Agent | 文件 | 功能 | 实现状态 |
|-------|------|------|----------|
| Orchestrator | `orchestrator.py` | 意图路由 → DAG 执行计划 → 聚合结果 | **Partial** - execute() 有，LangGraph 3节点空 |
| Requirements | `requirements_agent.py` | NL → 结构化需求 (NER + RAG) | **Stub** - 4空节点，execute()调LLM+fallback mock |
| Functional | `functional_agent.py` | 功能分解 → 功能树 + BDD 图 | **Stub** - 3空节点 |
| Logical | `logical_agent.py` | SC→SSC 分解 + IBD + 信号池 | **Stub** - 3空节点 |
| Physical | `physical_agent.py` | ECU 映射 + CCP 分配 + 拓扑 | **Stub** - 3空节点 |
| PLE/Variant | `ple_variant_agent.py` | 标签组合 → 150%模型子集 + SSC分支 | **Stub** - 3空节点 |
| Baseline | `baseline_agent.py` | 6步基线流水线 + 审计 | **Stub** - 6空节点 |
| Verification | `verification_agent.py` | RFLP追溯检查 + PLE冲突检测 | **Stub** - 4空节点 |
| SysML Diagram | `sysml_diagram_agent.py` | NL描述 → @xyflow/react 图表 JSON | **Stub** - 3空节点 |
| Learning | `learning_agent.py` | 历史基线模式学习 + 配置推荐 | **Stub** - 3空节点 |
| Conversational | `conversational_agent.py` | NL2Cypher 对话查询 | **Stub** - 3空节点 |

**共性问题**: 所有 Agent 的 LangGraph 节点处理器全是 `self.think()` 空壳，无真实DB查询/领域引擎调用。execute() 调用LLM后 try/catch 回退 mock 数据。

## 审计结果：完成度分类 (71文件)

### ✅ 已完成 (35文件)
- 入口/配置: app.py, config.py, database.py, bootstrap.py, run.py
- Agent基础: base.py, tool_registry.py
- GraphQL API: graphql.py (828行，完整CRUD+图表)
- 领域引擎: domain/ple/variant.py, domain/rflp/trace.py (真实SQL)
- ORM模型: 11个模型文件 (全链路覆盖)
- 集成: integrations/llm.py (Anthropic SDK + Mock降级)
- Pydantic Schema: project.py, requirement.py, tag.py
- 迁移: 001_initial.py, 002_add_rflp_links.py
- 前端入口: main.tsx, App.tsx, client.ts, operations.ts
- 前端组件: WelcomeScreen, Sidebar, MainPanel, StatusBar, AgentPanel, DiagramCanvas
- 前端编辑器: RequirementsEditor, TagManager (接真实API)
- 状态管理: stores/agent.ts, stores/project.ts

### ⚠️ 部分完成 (2文件)
- api/rest.py: 缺 Functions/SC/SSC/ECU/Signals/Baselines/CCPs 的 REST 端点
- agents/orchestrator.py: LangGraph 3节点空壳

### 🔧 仅骨架 (14文件)
- 10个Agent: 所有 LangGraph 节点空壳
- 前端: BaselinesPanel.tsx, TraceMatrixPanel.tsx, EntityCreator.tsx (UI完整但用本地mock数据)

### 📦 完全空白 (8项)
- knowledge/graph/ (Neo4j知识图谱)，knowledge/prompts/ (提示词模板)，knowledge/rag/ (RAG引擎)
- tests/ (零测试)，docs/ (零文档)，components/chat/ (空目录)

## 6阶段开发计划

| 阶段 | 内容 | 预计用时 | 优先级 |
|------|------|----------|--------|
| **第1阶段** | P3+P4+P5: REST补端点 + 前端3组件接数据 + Agent接领域引擎 | 3-4h | 立即 |
| **第2阶段** | P1 核心Agent: Baseline/Verification/Requirements 填节点 | 3-4h | 高 |
| **第3阶段** | P1 剩余Agent: Functional/Logical/Physical/PLE/SysML/Learning/Conversational | 3-4h | 高 |
| **第4阶段** | P2 知识层: Neo4j图谱 + RAG + Prompt模板 | 4-6h | 中 |
| **第5阶段** | P6 测试: 领域引擎单测 + GraphQL集成测 + Agent mock测 | 3-4h | 中 |
| **第6阶段** | 文档 + Docker开发流 + 最终验收 | 2-3h | 低 |

**总计纯开发时间: 18-25小时，预计4-6次会话**

## 下次唤醒指引

1. 从第1阶段开始：REST补完 → 前端接数据 → Agent接引擎
2. 具体文件入口: `aivas-core/aivas/api/rest.py`, `aivas-ui/src/components/editors/BaselinesPanel.tsx`, `aivas-core/aivas/bootstrap.py`
3. 数据库已就绪，可直接连接开发
4. 启动后端: `cd aivas-core && python run.py`
5. 启动前端: `cd aivas-ui && npm run dev`
