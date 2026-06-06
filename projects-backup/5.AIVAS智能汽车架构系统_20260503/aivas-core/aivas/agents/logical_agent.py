"""Logical Agent — SC/SSC decomposition, IBD generation, signal pool definition via LLM + DB."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.models.sc import SC, SSC
from aivas.models.signal import Signal

SYSTEM_PROMPT = """你是一个汽车电子电气架构逻辑层设计专家，负责SC→SSC分解、IBD内部模块图生成和信号接口定义。
你需要：
1. 将系统组件(SC)分解为子系统组件(SSC)
2. 定义 SSC 之间的信号接口（信号名称、数据类型、周期、发送方、接收方）
3. 生成 IBD (Internal Block Diagram) 节点和边结构

输出严格的 JSON 格式：
{
  "sc": {"name": "ADAS Domain Controller", "id": "sc-1"},
  "sscs": [
    {"name": "Camera Processing", "parent_sc_id": "sc-1", "description": "摄像头数据预处理"},
    {"name": "Radar Processing", "parent_sc_id": "sc-1", "description": "雷达信号处理"},
    {"name": "Path Planning", "parent_sc_id": "sc-1", "description": "路径规划算法"}
  ],
  "ibd": {
    "nodes": [{"id": "ssc-1", "type": "ssc", "data": {"label": "Camera Processing"}, "position": {"x": 0, "y": 0}}],
    "edges": [{"id": "sig-1", "source": "ssc-1", "target": "ssc-3", "data": {"label": "ObjectList"}}]
  },
  "signal_pool": [
    {"name": "ObjectList", "type": "CAN_FD", "period_ms": 50, "source": "ssc-1", "target": "ssc-3"}
  ]
}"""

DECOMPOSE_SSC_PROMPT = """你是一个系统组件分解专家。将SC分解为SSC（子系统组件）。
为每个SSC定义 name 和 description。

输出严格 JSON：{"sscs": [{"name": "...", "description": "..."}]}"""

IBD_PROMPT = """你是一个 SysML IBD 图生成专家。根据SSC列表生成 @xyflow/react IBD 图 JSON。
- 每个SSC一个节点，type="ssc"，id="ssc-0", "ssc-1"...
- SSC之间通过信号连接，边 data.label 为信号名
- 水平排列，x间隔250px
- 输出严格 JSON：{"nodes": [...], "edges": [...]}"""

SIGNAL_PROMPT = """你是一个汽车信号接口定义专家。为SSC之间的通信定义信号池。
每个信号定义：name, type(CAN/CAN-FD/Ethernet/LIN), period_ms, source(发送方SSC名), target(接收方SSC名)

输出严格 JSON：{"signal_pool": [{"name": "...", "type": "CAN-FD", "period_ms": 50, "source": "...", "target": "..."}]}"""


class LogicalAgent(BaseAgent):
    name = "Logical"
    description = "Decomposes SC→SSC, generates IBD diagrams, and defines signal pools via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("decompose_sc", self._decompose_sc)
        builder.add_node("generate_ibd", self._generate_ibd)
        builder.add_node("define_signals", self._define_signals)
        builder.set_entry_point("decompose_sc")
        builder.add_edge("decompose_sc", "generate_ibd")
        builder.add_edge("generate_ibd", "define_signals")
        builder.add_edge("define_signals", END)
        return builder.compile()

    async def _decompose_sc(self, state: AgentState) -> AgentState:
        message = state.input.get("message", "")
        project_id = state.input.get("project_id", "")
        db: AsyncSession | None = state.input.get("db")

        self.think("Analyzing SC and proposing SSC decomposition...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(message, system=DECOMPOSE_SSC_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                sscs = json.loads(response[start:end]).get("sscs", []) if start != -1 else []
            except Exception:
                sscs = []
        elif db and project_id:
            try:
                result = await db.execute(
                    select(SSC).join(SC).where(SC.project_id == uuid.UUID(project_id))
                )
                existing = result.scalars().all()
                sscs = [{"name": s.name, "description": s.description or ""} for s in existing]
                self.think(f"Loaded {len(sscs)} existing SSCs from DB")
            except Exception:
                sscs = []
        else:
            sscs = []

        state.output["sscs"] = sscs
        self.think(f"SSC decomposition: {len(sscs)} component(s)")
        return state

    async def _generate_ibd(self, state: AgentState) -> AgentState:
        sscs = state.output.get("sscs", [])
        message = state.input.get("message", "")

        self.think("Generating IBD (Internal Block Diagram)...")

        if self.llm and sscs:
            try:
                ssc_names = [s["name"] for s in sscs]
                response = await self.llm.complete(
                    f"SSC列表：{ssc_names}\n生成 IBD 图。",
                    system=IBD_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                ibd = json.loads(response[start:end]) if start != -1 else {"nodes": [], "edges": []}
            except Exception:
                ibd = {"nodes": [], "edges": []}
        elif sscs:
            nodes: list[dict] = []
            edges: list[dict] = []
            for i, s in enumerate(sscs):
                nodes.append({
                    "id": f"ssc-{i}", "type": "ssc",
                    "data": {"label": s["name"]},
                    "position": {"x": 100 + (i % 4) * 250, "y": 100 + (i // 4) * 150},
                })
            ibd = {"nodes": nodes, "edges": edges}
        else:
            ibd = {"nodes": [], "edges": []}

        state.output["ibd"] = ibd
        self.think(f"IBD: {len(ibd.get('nodes', []))} nodes, {len(ibd.get('edges', []))} edges")
        return state

    async def _define_signals(self, state: AgentState) -> AgentState:
        sscs = state.output.get("sscs", [])
        message = state.input.get("message", "")

        self.think("Defining signal pool between SSCs...")

        signal_pool: list[dict] = []
        if self.llm and len(sscs) >= 2:
            try:
                ssc_names = [s["name"] for s in sscs]
                response = await self.llm.complete(
                    f"SSC列表：{ssc_names}\n定义信号接口。",
                    system=SIGNAL_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                signal_pool = json.loads(response[start:end]).get("signal_pool", []) if start != -1 else []
            except Exception:
                signal_pool = []

        state.output["signal_pool"] = signal_pool
        state.status = AgentStatus.DONE
        self.think(f"Signal pool: {len(signal_pool)} signal(s) defined")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        self.think("Decomposing SC to SSC and defining signal interfaces...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(
                    f"基于以下功能描述进行逻辑层分解：\n\n{message}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "sc": None, "sscs": [], "ibd": {"nodes": [], "edges": []}, "signal_pool": [],
                }
            except Exception:
                result = {"sc": None, "sscs": [], "ibd": {"nodes": [], "edges": []}, "signal_pool": []}
        else:
            result = {
                "sc": None, "sscs": [],
                "ibd": {"nodes": [], "edges": []},
                "signal_pool": [],
                "summary": "Mock 模式 — 未进行 AI 逻辑分解。请通过逻辑界面手动添加。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
