"""Base Agent class — all 10 specialized agents inherit from this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TYPE_CHECKING

from langgraph.graph import StateGraph

if TYPE_CHECKING:
    from aivas.integrations.llm import LLMProvider


class AgentStatus(str, Enum):
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    DONE = "done"
    ERROR = "error"


@dataclass
class AgentState:
    agent_name: str
    status: AgentStatus = AgentStatus.IDLE
    input: dict[str, Any] = field(default_factory=dict)
    output: dict[str, Any] = field(default_factory=dict)
    thinking_trace: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class ToolDefinition:
    """A tool that an agent can invoke through the Tool Registry."""
    name: str
    description: str
    parameters: dict[str, Any]  # JSON Schema for parameters
    handler: Any  # callable


class BaseAgent(ABC):
    """Abstract base for all AIVAS agents.

    Each agent has:
    - A name and description for Orchestrator routing
    - A LangGraph state machine for execution flow
    - Access to the Tool Registry for domain service calls
    - A thinking trace for UI display
    """

    name: str
    description: str
    tools: list[ToolDefinition] = []

    def __init__(self, tool_registry: "ToolRegistry | None" = None, llm: "LLMProvider | None" = None):
        self.registry = tool_registry
        self.llm = llm
        self.state = AgentState(agent_name=self.name)
        self.graph = self._build_graph()

    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph state machine for this agent's execution flow."""
        ...

    @abstractmethod
    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's primary task."""
        ...

    def think(self, message: str) -> None:
        self.state.thinking_trace.append(message)
        self.state.status = AgentStatus.THINKING

    def use_tool(self, tool_name: str, **kwargs) -> Any:
        if self.registry is None:
            raise RuntimeError("No ToolRegistry available")
        return self.registry.invoke(tool_name, **kwargs)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "status": self.state.status.value,
            "thinking_trace": self.state.thinking_trace,
        }
