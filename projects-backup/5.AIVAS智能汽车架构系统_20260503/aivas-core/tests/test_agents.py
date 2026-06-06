"""Agent unit tests — test each agent's execute() method without LLM or DB."""

import pytest

from aivas.agents.requirements_agent import RequirementsAgent
from aivas.agents.functional_agent import FunctionalAgent
from aivas.agents.logical_agent import LogicalAgent
from aivas.agents.physical_agent import PhysicalAgent
from aivas.agents.ple_variant_agent import PLEVariantAgent
from aivas.agents.baseline_agent import BaselineAgent
from aivas.agents.verification_agent import VerificationAgent
from aivas.agents.sysml_diagram_agent import SysMLDiagramAgent
from aivas.agents.learning_agent import LearningAgent
from aivas.agents.conversational_agent import ConversationalAgent


class TestRequirementsAgent:
    async def test_execute_without_llm(self):
        agent = RequirementsAgent()
        result = await agent.execute({"message": "系统应支持L3自动驾驶", "project_id": "", "db": None})
        assert "requirements" in result
        assert "summary" in result
        assert agent.state.status.value == "done"

    async def test_execute_with_text_field(self):
        agent = RequirementsAgent()
        result = await agent.execute({"text": "车辆必须具备ABS功能"})
        assert "requirements" in result

    async def test_langgraph_built(self):
        agent = RequirementsAgent()
        assert agent.graph is not None
        assert len(agent.graph.nodes) >= 4  # 4 user nodes + __start__


class TestFunctionalAgent:
    async def test_execute_without_llm(self):
        agent = FunctionalAgent()
        result = await agent.execute({"message": "设计ADAS系统"})
        assert "functions" in result
        assert "tree" in result
        assert "bdd" in result

    async def test_langgraph_built(self):
        agent = FunctionalAgent()
        assert agent.graph is not None
        assert len(agent.graph.nodes) >= 3  # 3 user nodes + __start__


class TestLogicalAgent:
    async def test_execute_without_llm(self):
        agent = LogicalAgent()
        result = await agent.execute({"message": "ADAS域控制器信号定义"})
        assert "sscs" in result
        assert "ibd" in result
        assert "signal_pool" in result

    async def test_langgraph_built(self):
        agent = LogicalAgent()
        assert agent.graph is not None
        assert len(agent.graph.nodes) >= 3


class TestPhysicalAgent:
    async def test_execute_without_llm(self):
        agent = PhysicalAgent()
        result = await agent.execute({"message": "将ADAS功能映射到ECU"})
        assert "ecu_allocation" in result
        assert "ccp_allocation" in result
        assert "topology" in result

    async def test_langgraph_built(self):
        agent = PhysicalAgent()
        assert agent.graph is not None
        assert len(agent.graph.nodes) >= 3


class TestPLEVariantAgent:
    async def test_execute_without_llm(self):
        agent = PLEVariantAgent()
        result = await agent.execute({"tag_ids": ["t1", "t2"], "message": "高配变体"})
        assert "variant_config" in result
        assert "variant_assets" in result
        assert "conflicts" in result


class TestBaselineAgent:
    async def test_execute_without_db(self):
        agent = BaselineAgent()
        result = await agent.execute({"message": "创建基线", "tag_ids": []})
        assert "baseline_name" in result
        assert "status" in result
        assert result["status"] == "draft"

    async def test_langgraph_has_6_nodes(self):
        agent = BaselineAgent()
        assert agent.graph is not None
        nodes = sorted(agent.graph.nodes.keys())
        assert "lock_tags" in nodes
        assert "freeze_snapshot" in nodes

    async def test_execute_with_tags_no_db(self):
        agent = BaselineAgent()
        result = await agent.execute({"tag_ids": ["t1", "t2", "t3"], "message": ""})
        assert "baseline_name" in result


class TestVerificationAgent:
    async def test_execute_without_db(self):
        agent = VerificationAgent()
        result = await agent.execute({"message": "验证架构一致性"})
        assert "issues" in result
        assert "warnings" in result

    async def test_langgraph_built(self):
        agent = VerificationAgent()
        assert agent.graph is not None
        assert len(agent.graph.nodes) >= 4


class TestSysMLDiagramAgent:
    async def test_execute_without_llm(self):
        agent = SysMLDiagramAgent()
        result = await agent.execute({"description": "ADAS系统BDD图", "diagram_type": "BDD"})
        assert "diagram_type" in result
        assert "nodes" in result
        assert "edges" in result

    async def test_diagram_type_inference_empty(self):
        agent = SysMLDiagramAgent()
        result = await agent.execute({"description": ""})
        assert result["diagram_type"] == "BDD"


class TestLearningAgent:
    async def test_execute_without_llm(self):
        agent = LearningAgent()
        result = await agent.execute({"message": "推荐配置"})
        assert "recommendations" in result
        assert "patterns" in result


class TestConversationalAgent:
    async def test_execute_without_llm(self):
        agent = ConversationalAgent()
        result = await agent.execute({"message": "如何创建需求？"})
        assert "answer" in result
        assert "question" in result

    async def test_execute_with_question_field(self):
        agent = ConversationalAgent()
        result = await agent.execute({"question": "AIVAS是什么？"})
        assert "answer" in result


class TestAgentState:
    async def test_thinking_trace(self):
        agent = RequirementsAgent()
        await agent.execute({"message": "测试"})
        assert len(agent.state.thinking_trace) > 0
        assert agent.state.status.value == "done"

    async def test_to_dict(self):
        agent = BaselineAgent()
        await agent.execute({"tag_ids": ["t1"]})
        d = agent.to_dict()
        assert d["name"] == "Baseline"
        assert d["status"] in ("done", "executing", "idle")
