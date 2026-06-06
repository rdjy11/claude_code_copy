"""Orchestrator Agent — entry point that routes user intent to specialized agents."""

from __future__ import annotations

from typing import Any, TYPE_CHECKING

from langgraph.graph import StateGraph, END

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.agents.tool_registry import ToolRegistry

if TYPE_CHECKING:
    from aivas.integrations.llm import LLMProvider

INTENTS = [
    "requirements", "functional", "logical", "physical",
    "variant", "baseline", "verification", "conversational",
]


class OrchestratorAgent(BaseAgent):
    name = "Orchestrator"
    description = "Routes user intent to specialized agents and aggregates results"

    def __init__(
        self,
        tool_registry: ToolRegistry,
        agents: dict[str, BaseAgent],
        llm: "LLMProvider | None" = None,
    ):
        super().__init__(tool_registry, llm)
        self._agents = agents

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("parse_intent", self._parse_intent)
        builder.add_node("dispatch", self._dispatch)
        builder.add_node("aggregate", self._aggregate)
        builder.set_entry_point("parse_intent")
        builder.add_edge("parse_intent", "dispatch")
        builder.add_edge("dispatch", "aggregate")
        builder.add_edge("aggregate", END)
        return builder.compile()

    async def _parse_intent(self, state: AgentState) -> AgentState:
        self.think("Classifying user intent...")
        return state

    async def _dispatch(self, state: AgentState) -> AgentState:
        self.think(f"Dispatching to agent: {state.output.get('intent', 'unknown')}")
        return state

    async def _aggregate(self, state: AgentState) -> AgentState:
        self.think("Aggregating agent results...")
        state.status = AgentStatus.DONE
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        user_message = input.get("message", "")
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        intent = await self._classify_intent(user_message)
        agent_names = self._route_to_agents(intent, user_message)

        responses: list[dict] = []
        for name in agent_names:
            agent = self._agents.get(name)
            if agent:
                self.think(f"Routing to {name}...")
                resp = await agent.execute({"message": user_message})
                responses.append({"agent": name, "result": resp})

        result = {
            "intent": intent,
            "agents_called": agent_names,
            "responses": responses,
        }
        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result

    async def _classify_intent(self, message: str) -> str:
        if self.llm:
            return await self.llm.classify_intent(message, INTENTS)
        # Fallback keyword matching
        return self._classify_intent_keywords(message)

    def _classify_intent_keywords(self, message: str) -> str:
        msg_lower = message.lower()
        if any(w in msg_lower for w in ("需求", "requirement", "req")):
            return "requirements"
        if any(w in msg_lower for w in ("功能", "function", "func", "bdd")):
            return "functional"
        if any(w in msg_lower for w in ("子系统", "subsystem", "ssc", "sc", "ibd")):
            return "logical"
        if any(w in msg_lower for w in ("ecu", "硬件", "hardware", "物理", "拓扑")):
            return "physical"
        if any(w in msg_lower for w in ("变体", "variant", "标签", "tag", "ple")):
            return "variant"
        if any(w in msg_lower for w in ("基线", "baseline", "发布")):
            return "baseline"
        if any(w in msg_lower for w in ("检查", "验证", "一致性", "validation", "verify")):
            return "verification"
        return "conversational"

    def _route_to_agents(self, intent: str, message: str) -> list[str]:
        routes = {
            "requirements": ["Requirements"],
            "functional": ["Functional"],
            "logical": ["Logical"],
            "physical": ["Physical"],
            "variant": ["PLE/Variant"],
            "baseline": ["Baseline"],
            "verification": ["Verification"],
            "conversational": ["Conversational"],
        }
        return routes.get(intent, ["Conversational"])
