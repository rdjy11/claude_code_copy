"""Conversational Agent — natural language query over the full model via LLM + structured routing."""

from typing import Any

from langgraph.graph import StateGraph, END

from aivas.agents.base import BaseAgent, AgentState, AgentStatus

SYSTEM_PROMPT = """你是一个 AIVAS 智能汽车架构系统的 AI 助手。你可以帮助用户：
1. 回答关于架构设计、RFLP方法论、PLE变体管理、基线管理的问题
2. 解释系统组件的功能和关系
3. 提供汽车电子电气架构领域的建议
4. 引导用户使用系统的各项功能（需求管理、功能分解、逻辑设计、物理映射、PLE配置、基线发布）
5. 当用户需要具体操作时，引导他们到对应的功能界面

回复使用中文。如果用户问的问题超出你的知识范围，诚实说明并建议他们查阅相关文档或使用具体功能界面。

关于本系统功能界面的指引：
- 需求管理 → 点击左侧 "需求 (Requirements)" 图标
- 功能分解 & BDD图 → 点击 "功能 (Functional)" 图标
- 逻辑层设计 & IBD图 → 点击 "逻辑 (Logical)" 图标
- 物理层映射 & 拓扑图 → 点击 "物理 (Physical)" 图标
- 标签体系管理 → 点击 "PLE 标签/变体" 图标
- 基线管理 → 点击 "基线管理" 图标
- RFLP追溯矩阵 → 点击 "追溯矩阵" 图标"""

NL2CYPHER_PROMPT = """你是一个自然语言转数据库查询专家。将用户问题转换为查询意图描述。

查询意图类型：LIST_REQUIREMENTS, LIST_FUNCTIONS, LIST_ECS, LIST_BASELINES, TRACE_MATRIX, PROJECT_SUMMARY, GENERAL_QUESTION

输出严格 JSON：{"intent": "QUERY_TYPE", "entities": ["提到的实体名"], "filters": {"project_id": "optional"}}"""


class ConversationalAgent(BaseAgent):
    name = "Conversational"
    description = "Answers natural language queries about the system model and guides users via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("nl_to_cypher", self._nl_to_cypher)
        builder.add_node("execute_query", self._execute_query)
        builder.add_node("format_answer", self._format_answer)
        builder.set_entry_point("nl_to_cypher")
        builder.add_edge("nl_to_cypher", "execute_query")
        builder.add_edge("execute_query", "format_answer")
        builder.add_edge("format_answer", END)
        return builder.compile()

    async def _nl_to_cypher(self, state: AgentState) -> AgentState:
        question = state.input.get("message", "") or state.input.get("question", "")

        self.think("Understanding user question...")

        query_intent = {"intent": "GENERAL_QUESTION", "entities": [], "filters": {}}

        if self.llm and question.strip():
            try:
                response = await self.llm.complete(
                    f"分析以下问题的查询意图：\n{question}",
                    system=NL2CYPHER_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    query_intent = json.loads(response[start:end])
            except Exception:
                pass
        else:
            # Keyword-based intent detection
            q_lower = question.lower()
            if any(kw in q_lower for kw in ("需求", "requirement", "req")):
                query_intent["intent"] = "LIST_REQUIREMENTS"
            elif any(kw in q_lower for kw in ("功能", "function", "func")):
                query_intent["intent"] = "LIST_FUNCTIONS"
            elif any(kw in q_lower for kw in ("ecu", "控制器", "硬件")):
                query_intent["intent"] = "LIST_ECS"
            elif any(kw in q_lower for kw in ("基线", "baseline", "快照")):
                query_intent["intent"] = "LIST_BASELINES"
            elif any(kw in q_lower for kw in ("追溯", "trace", "rflp", "矩阵")):
                query_intent["intent"] = "TRACE_MATRIX"
            elif any(kw in q_lower for kw in ("项目", "project", "总览", "概况")):
                query_intent["intent"] = "PROJECT_SUMMARY"

        state.output["query_intent"] = query_intent
        self.think(f"Intent: {query_intent['intent']}")
        return state

    async def _execute_query(self, state: AgentState) -> AgentState:
        query_intent = state.output.get("query_intent", {})
        intent = query_intent.get("intent", "GENERAL_QUESTION")
        db = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Searching knowledge...")

        result: dict[str, Any] = {"intent": intent, "data": None}

        if db and project_id:
            import uuid
            try:
                if intent == "LIST_REQUIREMENTS":
                    from sqlalchemy import select
                    from aivas.models.requirement import Requirement
                    r = await db.execute(
                        select(Requirement).where(
                            Requirement.project_id == uuid.UUID(project_id)
                        ).limit(20)
                    )
                    items = r.scalars().all()
                    result["data"] = [{"type": i.type, "content": i.content[:120]} for i in items]

                elif intent == "LIST_FUNCTIONS":
                    from sqlalchemy import select
                    from aivas.models.function import Function
                    r = await db.execute(
                        select(Function).where(
                            Function.project_id == uuid.UUID(project_id)
                        ).limit(20)
                    )
                    items = r.scalars().all()
                    result["data"] = [{"name": i.name, "description": (i.description or "")[:120]} for i in items]

                elif intent == "LIST_ECS":
                    from sqlalchemy import select
                    from aivas.models.ecu import ECU
                    r = await db.execute(
                        select(ECU).where(
                            ECU.project_id == uuid.UUID(project_id)
                        ).limit(20)
                    )
                    items = r.scalars().all()
                    result["data"] = [{"name": i.name, "type": i.type} for i in items]

                elif intent == "LIST_BASELINES":
                    from sqlalchemy import select
                    from aivas.models.baseline import Baseline
                    r = await db.execute(
                        select(Baseline).where(
                            Baseline.project_id == uuid.UUID(project_id)
                        ).limit(20)
                    )
                    items = r.scalars().all()
                    result["data"] = [{"name": i.name, "status": i.status} for i in items]

                elif intent == "TRACE_MATRIX":
                    from aivas.domain.rflp.trace import get_rflp_summary
                    summary = await get_rflp_summary(db, project_id)
                    result["data"] = summary

                elif intent == "PROJECT_SUMMARY":
                    from aivas.domain.rflp.trace import get_rflp_summary
                    summary = await get_rflp_summary(db, project_id)
                    result["data"] = summary
            except Exception as e:
                result["error"] = str(e)

        state.output["query_result"] = result
        self.think(f"Query executed: {intent} — {'data found' if result.get('data') else 'no data'}")
        return state

    async def _format_answer(self, state: AgentState) -> AgentState:
        question = state.input.get("message", "") or state.input.get("question", "")
        query_result = state.output.get("query_result", {})
        query_intent = state.output.get("query_intent", {})

        self.think("Formatting answer...")

        if self.llm and query_result.get("data"):
            try:
                answer = await self.llm.complete(
                    f"用户问题：{question}\n查询结果：{query_result['data']}\n请用中文友好回复。",
                    system=SYSTEM_PROMPT,
                )
            except Exception:
                answer = f"查询到以下结果：{query_result['data']}"
        elif query_result.get("data"):
            data = query_result["data"]
            if isinstance(data, list):
                items_text = "\n".join(
                    f"- {item.get('name', item.get('type', item.get('content', str(item))))}"
                    for item in data[:10]
                )
                answer = f"查询结果（{len(data)} 条）：\n{items_text}"
            elif isinstance(data, dict):
                items = "\n".join(f"- {k}: {v}" for k, v in data.items())
                answer = f"项目概况：\n{items}"
            else:
                answer = str(data)
        else:
            answer = (
                "我是 AIVAS 智能助手（Mock 模式）。当前未接入真实 LLM，我只能提供基础引导。\n\n"
                "你可以通过左侧导航栏访问以下功能：\n"
                "- 需求管理 — 创建和管理需求条目\n"
                "- 功能分解 — 定义功能模块和 BDD 图\n"
                "- 逻辑设计 — 分解 SC/SSC 和 IBD 图\n"
                "- 物理映射 — 映射 ECU 和拓扑图\n"
                "- PLE 标签 — 管理三级标签体系\n"
                "- 基线管理 — 创建和对比基线\n"
                "- 追溯矩阵 — 查看 RFLP 追溯链\n\n"
                "配置 LLM API Key 后，我将能提供智能化的架构建议。"
            )

        state.output["answer"] = answer
        state.output["cypher"] = query_intent.get("intent", "")
        state.output["graph_results"] = query_result.get("data")
        state.status = AgentStatus.DONE
        self.think("Answer formatted")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        question = input.get("message", "") or input.get("question", "")
        self.think("Processing conversational query...")

        if self.llm and question.strip():
            try:
                answer = await self.llm.complete(question, system=SYSTEM_PROMPT)
            except Exception:
                answer = "AI 服务暂时不可用，请稍后重试。"
        else:
            answer = (
                "我是 AIVAS 智能助手（Mock 模式）。当前未接入真实 LLM，我只能提供基础引导。\n\n"
                "你可以通过左侧导航栏访问以下功能：\n"
                "- 需求管理 — 创建和管理需求条目\n"
                "- 功能分解 — 定义功能模块和 BDD 图\n"
                "- 逻辑设计 — 分解 SC/SSC 和 IBD 图\n"
                "- 物理映射 — 映射 ECU 和拓扑图\n"
                "- PLE 标签 — 管理三级标签体系\n"
                "- 基线管理 — 创建和对比基线\n"
                "- 追溯矩阵 — 查看 RFLP 追溯链\n\n"
                "配置 LLM API Key 后，我将能提供智能化的架构建议。"
            )

        result = {
            "question": question,
            "answer": answer,
            "cypher": "",
            "graph_results": [],
            "diagram": None,
        }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
