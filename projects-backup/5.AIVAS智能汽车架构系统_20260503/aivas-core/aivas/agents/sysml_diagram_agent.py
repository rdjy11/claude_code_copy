"""SysML Diagram Agent — generates editable diagram JSON from text descriptions via LLM + fallback layout."""

from typing import Any

from langgraph.graph import StateGraph, END

from aivas.agents.base import BaseAgent, AgentState, AgentStatus

SYSTEM_PROMPT = """你是一个 SysML 建模专家，将自然语言描述转换为 @xyflow/react 流程图 JSON。
支持的图类型：BDD (Block Definition Diagram), IBD (Internal Block Diagram), Topology (网络拓扑图)

输出规则：
- 每个节点必须有唯一的 id (如 "bdd-1", "ibd-3", "topo-5")
- 每个节点有 type 字段: "function"/"sc"/"ssc"/"ecu"/"sensor"/"actuator"
- 每个节点有 data.label 作为显示文本
- 每个节点有 position: {"x": number, "y": number}，水平排列节点，间距 250px
- 每条边有 id, source, target, 可选 data.label

输出严格的 JSON 格式（不要包含 ```json 包裹）：
{
  "diagram_type": "BDD",
  "nodes": [
    {"id": "bdd-1", "type": "function", "data": {"label": "感知融合"}, "position": {"x": 100, "y": 100}},
    {"id": "bdd-2", "type": "function", "data": {"label": "决策规划"}, "position": {"x": 350, "y": 100}}
  ],
  "edges": [
    {"id": "edge-1", "source": "bdd-1", "target": "bdd-2", "data": {"label": "ObjectList"}}
  ],
  "viewport": {"x": 0, "y": 0, "zoom": 1}
}"""

TYPE_KEYWORDS = {
    "BDD": ["bdd", "block definition", "模块定义", "功能分解", "block diagram"],
    "IBD": ["ibd", "internal block", "内部模块", "信号", "接口", "port", "connector"],
    "Topology": ["topology", "拓扑", "网络", "总线", "ecu", "can", "ethernet", "lin", "网关"],
    "Activity": ["activity", "活动", "流程", "sequence", "时序", "状态机"],
    "StateMachine": ["state machine", "状态机", "状态转换", "mode", "transition"],
}


class SysMLDiagramAgent(BaseAgent):
    name = "SysML Diagram"
    description = "Generates SysML diagrams (BDD, IBD, Topology) as @xyflow/react JSON via LLM"

    DIAGRAM_TYPES = ["BDD", "IBD", "Topology", "Activity", "StateMachine"]

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("parse_description", self._parse_description)
        builder.add_node("infer_diagram_type", self._infer_diagram_type)
        builder.add_node("generate_flow_json", self._generate_flow_json)
        builder.set_entry_point("parse_description")
        builder.add_edge("parse_description", "infer_diagram_type")
        builder.add_edge("infer_diagram_type", "generate_flow_json")
        builder.add_edge("generate_flow_json", END)
        return builder.compile()

    async def _parse_description(self, state: AgentState) -> AgentState:
        description = state.input.get("message", "") or state.input.get("description", "")

        self.think("Parsing diagram description...")

        # Extract key terms for later use
        keywords: list[str] = []
        text_lower = description.lower()
        for kw in ["adas", "ecu", "sensor", "camera", "radar", "lidar", "gateway",
                     "domain", "controller", "bus", "can", "ethernet", "lin",
                     "function", "signal", "bdd", "ibd", "topology", "sc", "ssc"]:
            if kw in text_lower:
                keywords.append(kw)

        state.output["parsed_keywords"] = keywords
        state.output["char_count"] = len(description)
        self.think(f"Description parsed: {len(description)} chars, keywords: {keywords[:5]}")
        return state

    async def _infer_diagram_type(self, state: AgentState) -> AgentState:
        description = state.input.get("message", "") or state.input.get("description", "")
        explicit_type = state.input.get("diagram_type", "")

        self.think("Inferring diagram type...")

        if explicit_type and explicit_type in self.DIAGRAM_TYPES:
            diagram_type = explicit_type
        else:
            text_lower = description.lower()
            scores: dict[str, int] = {}
            for dtype, kws in TYPE_KEYWORDS.items():
                scores[dtype] = sum(1 for kw in kws if kw in text_lower)

            best = max(scores, key=scores.get) if scores else "BDD"
            diagram_type = best if scores[best] > 0 else "BDD"

        state.output["diagram_type"] = diagram_type
        self.think(f"Diagram type: {diagram_type}")
        return state

    async def _generate_flow_json(self, state: AgentState) -> AgentState:
        description = state.input.get("message", "") or state.input.get("description", "")
        diagram_type = state.output.get("diagram_type", "BDD")

        self.think(f"Generating {diagram_type} @xyflow/react diagram JSON...")

        if self.llm and description.strip():
            try:
                response = await self.llm.complete(
                    f"图类型：{diagram_type}\n描述：{description}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    result = json.loads(response[start:end])
                else:
                    result = {
                        "diagram_type": diagram_type,
                        "nodes": [], "edges": [],
                        "viewport": {"x": 0, "y": 0, "zoom": 1},
                    }
            except Exception:
                result = {
                    "diagram_type": diagram_type,
                    "nodes": [], "edges": [],
                    "viewport": {"x": 0, "y": 0, "zoom": 1},
                    "error": "LLM generation failed",
                }
        else:
            # Fallback: return empty diagram with the correct type
            result = {
                "diagram_type": diagram_type,
                "nodes": [], "edges": [],
                "viewport": {"x": 0, "y": 0, "zoom": 1},
                "summary": f"无 LLM 连接 — 返回空白 {diagram_type} 画布。请通过图示界面手动编辑。",
            }

        state.output["nodes"] = result.get("nodes", [])
        state.output["edges"] = result.get("edges", [])
        state.output["viewport"] = result.get("viewport", {"x": 0, "y": 0, "zoom": 1})
        state.status = AgentStatus.DONE
        self.think(f"Generated {diagram_type}: {len(result.get('nodes', []))} nodes, {len(result.get('edges', []))} edges")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        description = input.get("message", "") or input.get("description", "")
        diagram_type = input.get("diagram_type", "BDD")
        self.think(f"Generating {diagram_type} diagram from description...")

        if self.llm and description.strip():
            try:
                response = await self.llm.complete(
                    f"图类型：{diagram_type}\n描述：{description}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "diagram_type": diagram_type, "nodes": [], "edges": [], "viewport": {"x": 0, "y": 0, "zoom": 1},
                }
            except Exception:
                result = {"diagram_type": diagram_type, "nodes": [], "edges": [], "viewport": {"x": 0, "y": 0, "zoom": 1}}
        else:
            result = {
                "diagram_type": diagram_type,
                "nodes": [], "edges": [],
                "viewport": {"x": 0, "y": 0, "zoom": 1},
                "summary": f"Mock 模式 — 未生成 AI {diagram_type} 图。请通过图示界面手动编辑。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
