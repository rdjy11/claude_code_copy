"""Tool Registry — centralized catalog of all domain operations agents can invoke."""

from typing import Any, Callable


class ToolRegistry:
    """Registry of callable tools that agents use to interact with the domain layer.

    Tools are the contract between Agents (AI reasoning) and Engines (deterministic logic).
    Agents do NOT directly manipulate models — they go through tools.
    """

    def __init__(self):
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(self, name: str, fn: Callable[..., Any]) -> None:
        self._tools[name] = fn

    def invoke(self, name: str, **kwargs) -> Any:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found. Available: {list(self._tools.keys())}")
        return self._tools[name](**kwargs)

    def list_tools(self) -> list[str]:
        return list(self._tools.keys())

    def describe(self, name: str) -> str:
        fn = self._tools.get(name)
        if fn is None:
            return f"Unknown tool: {name}"
        return fn.__doc__ or f"{name}(...)"

    def describe_all(self) -> dict[str, str]:
        return {name: self.describe(name) for name in self._tools}
