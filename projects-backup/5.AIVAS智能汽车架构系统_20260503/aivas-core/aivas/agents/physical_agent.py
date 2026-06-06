"""Physical Agent — ECU mapping, CCP allocation, network topology via LLM + DB."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.models.ecu import ECU
from aivas.models.ccp import CCP
from aivas.models.sc import SSC

SYSTEM_PROMPT = """你是一个汽车电子电气架构物理层设计专家，负责 ECU 映射、CCP标定参数分配和网络拓扑设计。
你需要：
1. 将 SSC (子系统组件) 映射到物理 ECU
2. 为每个 ECU 分配 CCP (标定/配置参数) 类别
3. 生成网络拓扑图 — 定义 ECU 之间的总线连接 (Ethernet/CAN-FD/CAN/LIN)

输出严格的 JSON 格式：
{
  "ecu_allocation": [
    {"ssc_name": "Camera Processing", "ecu_name": "ADAS (Ethernet)", "bus": "Ethernet"}
  ],
  "ccp_allocation": [
    {"ecu_name": "ADAS (Ethernet)", "ccp_categories": ["Camera Calibration", "Fusion Parameters"]}
  ],
  "topology": {
    "nodes": [{"id": "ecu-1", "type": "ecu", "data": {"label": "ADAS (Ethernet)", "bus": "Ethernet"}, "position": {"x": 0, "y": 0}}],
    "edges": [{"id": "bus-1", "source": "ecu-1", "target": "ecu-4", "data": {"label": "Ethernet TSN"}}]
  }
}"""

MAP_ECU_PROMPT = """你是一个ECU映射专家。将SSC映射到物理ECU。
考虑：算力需求、接口类型(CSI-2/Ethernet/CAN)、功能安全等级(ASIL A/B/C/D)

输出严格 JSON：{"mappings": [{"ssc_name": "...", "ecu_name": "...", "bus": "Ethernet/CAN-FD/CAN/LIN", "rationale": "..."}]}"""

TOPOLOGY_PROMPT = """你是一个车载网络拓扑专家。根据ECU列表生成网络拓扑图。
- 每个ECU一个节点，id="ecu-0", "ecu-1"...
- ECU之间通过总线连接(Ethernet TSN/CAN-FD/CAN/LIN)
- 网关ECU居中，域ECU围绕排列
- 输出 @xyflow/react JSON：{"nodes": [...], "edges": [...]}"""


class PhysicalAgent(BaseAgent):
    name = "Physical"
    description = "Maps logical architecture to physical ECUs and generates network topology via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("map_to_ecu", self._map_to_ecu)
        builder.add_node("allocate_ccps", self._allocate_ccps)
        builder.add_node("topology", self._topology)
        builder.set_entry_point("map_to_ecu")
        builder.add_edge("map_to_ecu", "allocate_ccps")
        builder.add_edge("allocate_ccps", "topology")
        builder.add_edge("topology", END)
        return builder.compile()

    async def _map_to_ecu(self, state: AgentState) -> AgentState:
        message = state.input.get("message", "")
        project_id = state.input.get("project_id", "")
        db: AsyncSession | None = state.input.get("db")

        self.think("Mapping SSC functions to ECU hardware...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(message, system=MAP_ECU_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                mappings = json.loads(response[start:end]).get("mappings", []) if start != -1 else []
            except Exception:
                mappings = []
        elif db and project_id:
            try:
                result = await db.execute(
                    select(ECU).where(ECU.project_id == uuid.UUID(project_id))
                )
                ecus = result.scalars().all()
                mappings = [{"ecu_name": e.name, "ssc_name": "", "bus": e.type, "rationale": ""} for e in ecus]
                self.think(f"Loaded {len(mappings)} existing ECUs from DB")
            except Exception:
                mappings = []
        else:
            mappings = []

        state.output["ecu_mappings"] = mappings
        self.think(f"ECU mapping: {len(mappings)} allocation(s)")
        return state

    async def _allocate_ccps(self, state: AgentState) -> AgentState:
        project_id = state.input.get("project_id", "")
        db: AsyncSession | None = state.input.get("db")

        self.think("Allocating calibration/configuration parameters...")

        ccp_categories: list[dict] = []
        if db and project_id:
            try:
                result = await db.execute(
                    select(CCP).where(CCP.project_id == uuid.UUID(project_id))
                )
                ccps = result.scalars().all()
                # Group CCPs by SSC
                by_ssc: dict[str, list[dict]] = {}
                for c in ccps:
                    by_ssc.setdefault(str(c.ssc_id), []).append({
                        "name": c.name, "value_type": c.value_type, "id": str(c.id),
                    })

                ccp_categories = [
                    {"ssc_id": ssc_id, "ccps": vals}
                    for ssc_id, vals in by_ssc.items()
                ]
                self.think(f"CCP allocation: {len(ccps)} params across {len(by_ssc)} SSC(s)")
            except Exception:
                pass

        state.output["ccp_categories"] = ccp_categories
        return state

    async def _topology(self, state: AgentState) -> AgentState:
        mappings = state.output.get("ecu_mappings", [])
        message = state.input.get("message", "")

        self.think("Generating network topology diagram...")

        if self.llm and mappings:
            try:
                ecu_names = [m.get("ecu_name", "") for m in mappings if m.get("ecu_name")]
                response = await self.llm.complete(
                    f"ECU列表：{ecu_names}\n生成网络拓扑图。",
                    system=TOPOLOGY_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                topology = json.loads(response[start:end]) if start != -1 else {"nodes": [], "edges": []}
            except Exception:
                topology = {"nodes": [], "edges": []}
        elif mappings:
            # Build basic topology from ECU list
            nodes: list[dict] = []
            edges: list[dict] = []
            ecu_names_seen: set[str] = set()
            for i, m in enumerate(mappings):
                name = m.get("ecu_name", f"ECU-{i}")
                if name not in ecu_names_seen:
                    ecu_names_seen.add(name)
                    nodes.append({
                        "id": f"ecu-{i}", "type": "ecu",
                        "data": {"label": name, "bus": m.get("bus", "Ethernet")},
                        "position": {"x": 100 + (i % 4) * 250, "y": 100 + (i // 4) * 150},
                    })
            # Add a center gateway if multiple ECUs
            if len(nodes) > 1:
                nodes.insert(0, {
                    "id": "ecu-gw", "type": "ecu",
                    "data": {"label": "Central Gateway", "bus": "Ethernet TSN"},
                    "position": {"x": 350, "y": 50},
                })
                for n in nodes[1:]:
                    edges.append({"id": f"bus-gw-{n['id']}", "source": "ecu-gw", "target": n["id"], "data": {"label": "Ethernet TSN"}})
            topology = {"nodes": nodes, "edges": edges}
        else:
            topology = {"nodes": [], "edges": []}

        state.output["topology"] = topology
        state.status = AgentStatus.DONE
        self.think(f"Topology: {len(topology.get('nodes', []))} nodes, {len(topology.get('edges', []))} edges")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        self.think("Mapping to ECUs and generating topology...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(
                    f"基于以下逻辑架构进行物理层映射：\n\n{message}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "ecu_allocation": [], "ccp_allocation": [], "topology": {"nodes": [], "edges": []},
                }
            except Exception:
                result = {"ecu_allocation": [], "ccp_allocation": [], "topology": {"nodes": [], "edges": []}}
        else:
            result = {
                "ecu_allocation": [], "ccp_allocation": [],
                "topology": {"nodes": [], "edges": []},
                "summary": "Mock 模式 — 未进行 AI 物理映射。请通过物理界面手动添加。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
