"""Functional Agent — decomposes functions, builds BDD diagrams via LLM + DB."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.models.function import Function
from aivas.models.requirement import Requirement

SYSTEM_PROMPT = """你是一个汽车电子电气架构功能设计专家，负责功能分解和 BDD 模块定义。
你需要：
1. 从用户需求出发，分解为功能模块（感知融合、决策规划、车辆控制、人机交互、网联服务、安全防护等）
2. 为每个功能模块定义名称、描述、所属域
3. 生成 BDD (Block Definition Diagram) 的节点和边结构，用于 @xyflow/react 渲染

输出严格的 JSON 格式：
{
  "functions": [
    {"name": "感知融合", "description": "融合摄像头、雷达、激光雷达数据", "domain": "ADAS", "suggested_requirement_id": null}
  ],
  "tree": {"name": "整车功能", "children": []},
  "bdd": {
    "nodes": [{"id": "f-1", "type": "function", "data": {"label": "感知融合"}, "position": {"x": 0, "y": 0}}],
    "edges": [{"id": "e-1", "source": "parent", "target": "f-1"}]
  }
}"""

DECOMPOSE_PROMPT = """你是一个功能分解专家。请从以下需求中提取功能模块列表。
为每个功能定义：name（名称）、description（描述）、domain（所属域：ADAS/座舱/车身/底盘/动力/网联/安全）

输出严格的 JSON：{"functions": [{"name": "...", "description": "...", "domain": "..."}]}"""

BDD_PROMPT = """你是一个 SysML BDD 图生成专家。根据功能列表生成 @xyflow/react 的 BDD 图 JSON。
- 根节点 id="bdd-root", type="function", data.label="整车功能"
- 每个子功能一个节点，父→子连线
- 水平排列，x间隔250px，y从100开始每行递增150px
- 输出严格的 JSON：{"nodes": [...], "edges": [...]}"""


class FunctionalAgent(BaseAgent):
    name = "Functional"
    description = "Decomposes system-level functions into functional tree and generates BDD via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("decompose", self._decompose)
        builder.add_node("build_tree", self._build_tree)
        builder.add_node("generate_bdd", self._generate_bdd)
        builder.set_entry_point("decompose")
        builder.add_edge("decompose", "build_tree")
        builder.add_edge("build_tree", "generate_bdd")
        builder.add_edge("generate_bdd", END)
        return builder.compile()

    async def _decompose(self, state: AgentState) -> AgentState:
        message = state.input.get("message", "")
        project_id = state.input.get("project_id", "")
        db: AsyncSession | None = state.input.get("db")

        self.think("Decomposing functions from requirements...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(message, system=DECOMPOSE_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                functions = json.loads(response[start:end]).get("functions", []) if start != -1 else []
            except Exception:
                functions = []
        elif db and project_id:
            # Fallback: load existing functions from DB
            try:
                result = await db.execute(
                    select(Function).where(Function.project_id == uuid.UUID(project_id))
                )
                existing = result.scalars().all()
                functions = [{"name": f.name, "description": f.description or "", "domain": ""} for f in existing]
                self.think(f"Loaded {len(functions)} existing functions from DB")
            except Exception:
                functions = []
        else:
            functions = []

        state.output["functions"] = functions
        self.think(f"Decomposed: {len(functions)} function(s)")
        return state

    async def _build_tree(self, state: AgentState) -> AgentState:
        functions = state.output.get("functions", [])

        self.think("Building functional decomposition tree...")

        # Build tree from flat function list
        tree: dict[str, Any] = {"name": "整车功能", "children": []}
        domains: dict[str, list[dict]] = {}
        for f in functions:
            domain = f.get("domain", "Other") or "Other"
            domains.setdefault(domain, []).append(f)

        for domain_name, domain_funcs in domains.items():
            domain_node: dict[str, Any] = {"name": domain_name, "children": []}
            for df in domain_funcs:
                domain_node["children"].append({"name": df["name"], "description": df.get("description", ""), "children": []})
            tree["children"].append(domain_node)

        state.output["tree"] = tree
        self.think(f"Tree: {len(functions)} functions across {len(domains)} domain(s)")
        return state

    async def _generate_bdd(self, state: AgentState) -> AgentState:
        functions = state.output.get("functions", [])
        message = state.input.get("message", "")

        self.think("Generating BDD block definition diagram...")

        if self.llm and functions:
            try:
                func_names = [f["name"] for f in functions]
                response = await self.llm.complete(
                    f"功能列表：{func_names}\n生成 BDD 图。",
                    system=BDD_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    bdd = json.loads(response[start:end])
                else:
                    bdd = {"nodes": [], "edges": []}
            except Exception:
                bdd = {"nodes": [], "edges": []}
        elif functions:
            # Generate basic BDD from function list
            nodes: list[dict] = [
                {"id": "bdd-root", "type": "function", "data": {"label": "整车功能"}, "position": {"x": 100, "y": 50}}
            ]
            edges: list[dict] = []
            for i, f in enumerate(functions):
                fid = f"bdd-f{i}"
                nodes.append({
                    "id": fid, "type": "function",
                    "data": {"label": f["name"]},
                    "position": {"x": 100 + (i % 4) * 250, "y": 150 + (i // 4) * 150},
                })
                edges.append({"id": f"bdd-e{i}", "source": "bdd-root", "target": fid})
            bdd = {"nodes": nodes, "edges": edges}
        else:
            bdd = {"nodes": [], "edges": []}

        state.output["bdd"] = bdd
        state.status = AgentStatus.DONE
        self.think(f"BDD: {len(bdd.get('nodes', []))} nodes, {len(bdd.get('edges', []))} edges")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        self.think("Decomposing functions and generating BDD...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(
                    f"基于以下需求进行功能分解：\n\n{message}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "functions": [],
                    "tree": {},
                    "bdd": {"nodes": [], "edges": []},
                }
            except Exception:
                result = {"functions": [], "tree": {}, "bdd": {"nodes": [], "edges": []}}
        else:
            result = {
                "functions": [],
                "tree": {},
                "bdd": {"nodes": [], "edges": []},
                "summary": "Mock 模式 — 未进行 AI 功能分解。请通过功能界面手动添加。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
