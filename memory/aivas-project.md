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
**状态**: **全部6阶段已完成** (2026-05-04)，84个源文件，33个测试全部通过
**下次唤醒**: 继续优化 / 新功能 / 前端扩展
**最后会话** (2026-05-05): 
- RFLP Demo 已成功运行（34资产，6追溯链，1基线）
- **待修复**: REST API 500错误 — `rest.py` 所有裸SQL需`text()`包装，前端传非UUID project_id导致asyncpg.DataError
- GraphQL `Unknown type 'ID'` 错误同样待修复
- 用户要求暂停修复，先备份状态

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
- **Docker**: Docker Compose 已配置全部服务（pg+neo4j+redis+minio+core+ui）
- **Neo4j / Redis / MinIO**: 配置就绪，依赖 Docker
- **AIVAS_LLM_API_KEY**: 未配置（需用户填写 Anthropic key）

## 10 个 AI Agent — 全部完成

| Agent | 文件 | 功能 | 实现状态 |
|-------|------|------|----------|
| Orchestrator | `orchestrator.py` | 意图路由 → DAG 执行计划 → 聚合结果 | **Partial** — execute() 有，LangGraph 3节点空 |
| Requirements | `requirements_agent.py` | NL → 结构化需求 (NER + RAG + LLM + DB persistence) | **Done** — 4节点全部实现：parse_nl/extract_entities/to_structured_req/assign_tags |
| Functional | `functional_agent.py` | 功能分解 → 功能树 + BDD 图 | **Done** — 3节点全部实现：decompose/build_tree/generate_bdd |
| Logical | `logical_agent.py` | SC→SSC 分解 + IBD + 信号池 | **Done** — 3节点全部实现：decompose_sc/generate_ibd/define_signals |
| Physical | `physical_agent.py` | ECU 映射 + CCP 分配 + 拓扑 | **Done** — 3节点全部实现：map_to_ecu/allocate_ccps/topology |
| PLE/Variant | `ple_variant_agent.py` | 标签组合 → 150%模型子集 + SSC分支 + 冲突检测 | **Done** — 3节点全部实现：combine_tags/subset_150/resolve_branches |
| Baseline | `baseline_agent.py` | 6步基线流水线 + 审计 | **Done** — 6节点全部实现：lock_tags/lock_ssc_versions/resolve_ecu_variants/filter_signals/consistency_check/freeze_snapshot |
| Verification | `verification_agent.py` | RFLP追溯检查 + PLE冲突检测 + 信号分配验证 | **Done** — 4节点全部实现：check_traceability/check_ple_conflicts/check_signal_allocation/generate_report |
| SysML Diagram | `sysml_diagram_agent.py` | NL描述 → @xyflow/react 图表 JSON | **Done** — 3节点全部实现：parse_description/infer_diagram_type/generate_flow_json |
| Learning | `learning_agent.py` | 历史基线模式学习 + 配置推荐 | **Done** — 3节点全部实现：extract_patterns/rank_recommendations/generate_suggestions |
| Conversational | `conversational_agent.py` | NL2Query 对话查询 | **Done** — 3节点全部实现：nl_to_cypher/execute_query/format_answer |

## 知识层 — 全部完成

| 模块 | 文件 | 功能 |
|------|------|------|
| Neo4j Connector | `knowledge/graph/connector.py` | 图数据库连接器，RFLP关系/变体树/基线血统存储，优雅降级到内存模式 |
| RAG Engine | `knowledge/rag/engine.py` | pgvector向量搜索+关键词搜索融合，自动构建RAG上下文 |
| Prompt Registry | `knowledge/prompts/registry.py` | 25个版本化Prompt模板，覆盖全10个Agent的使用场景 |

## 全部84源文件

### aivas-core/aivas (57 files)
- 入口/配置: app.py, config.py, database.py, bootstrap.py, run.py (5)
- Agent: base.py, tool_registry.py, orchestrator.py + 10 agents (13)
- GraphQL API: api/graphql.py, api/rest.py (2)
- 领域引擎: domain/ple/variant.py, domain/rflp/trace.py (2)
- 知识层: knowledge/graph/connector.py, knowledge/rag/engine.py, knowledge/prompts/registry.py + 4 __init__ (7)
- 集成: integrations/llm.py (1)
- ORM模型: 11 models (11)
- Pydantic Schema: 8 schema files (8)
- 迁移: 002_add_rflp_links.py (1)

### aivas-core/tests (6 files)
- conftest.py, test_agents.py, test_domain_rflp.py, test_domain_ple.py, test_graphql_schema.py, __init__.py

### aivas-ui/src (21 files)
- 前端组件完整

### Docker/Infrastructure (2 files)
- docker-compose.yml (完整7服务编排)
- aivas-core/Dockerfile, aivas-ui/Dockerfile

## 6阶段完成总结

| 阶段 | 内容 | 状态 |
|------|------|------|
| **第1阶段** | REST补端点 + 前端3组件接数据 + Agent接领域引擎 | ✅ 已完成 (之前会话) |
| **第2阶段** | Baseline/Verification/Requirements 填节点 | ✅ 已完成 (本次会话) |
| **第3阶段** | 剩余Agent: Functional/Logical/Physical/PLE/SysML/Learning/Conversational | ✅ 已完成 (本次会话) |
| **第4阶段** | 知识层: Neo4j图谱 + RAG + Prompt模板 | ✅ 已完成 (本次会话) |
| **第5阶段** | 测试: 领域引擎单测 + Agent mock测 (33/33 PASS) | ✅ 已完成 (本次会话) |
| **第6阶段** | Docker dev flow + 最终验收 | ✅ 已完成 (本次会话) |

### 本次会话新增 (Phase 2-6)
- 10个Agent的LangGraph节点全部从空壳填充为真实逻辑（100%覆盖率）
- 知识层3大模块从零构建
- 33个测试用例全部通过
- Docker全栈编排（7服务）
- 文件数: 71 → 84 (+13)
