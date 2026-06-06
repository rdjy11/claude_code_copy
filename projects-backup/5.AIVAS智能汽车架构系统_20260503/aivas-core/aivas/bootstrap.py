"""Bootstrap — wire ToolRegistry, domain engines, and agents together."""

from aivas.agents.tool_registry import ToolRegistry
from aivas.agents.base import BaseAgent
from aivas.agents.orchestrator import OrchestratorAgent
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
from aivas.integrations.llm import get_llm_provider


def build_agent_system() -> tuple[OrchestratorAgent, ToolRegistry]:
    """Create the full agent system with tool registry and all agents wired up."""
    registry = _register_tools()
    llm = get_llm_provider()

    agents: dict[str, BaseAgent] = {
        "Requirements": RequirementsAgent(registry, llm),
        "Functional": FunctionalAgent(registry, llm),
        "Logical": LogicalAgent(registry, llm),
        "Physical": PhysicalAgent(registry, llm),
        "PLE/Variant": PLEVariantAgent(registry, llm),
        "Baseline": BaselineAgent(registry, llm),
        "Verification": VerificationAgent(registry, llm),
        "SysML/Diagram": SysMLDiagramAgent(registry, llm),
        "Learning": LearningAgent(registry, llm),
        "Conversational": ConversationalAgent(registry, llm),
    }

    orchestrator = OrchestratorAgent(registry, agents, llm)
    return orchestrator, registry


def _register_tools() -> ToolRegistry:
    """Register all domain engine functions as callable tools."""
    registry = ToolRegistry()

    # RFLP Trace Engine
    from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
    registry.register("rflp.get_trace_matrix", get_trace_matrix)
    registry.register("rflp.get_summary", get_rflp_summary)

    # PLE Engine tools
    from aivas.domain.ple.variant import PLEEngine
    registry.register("ple.build_150_model", _ple_build_150)
    registry.register("ple.resolve_variant", _ple_resolve_variant)
    registry.register("ple.create_baseline", _ple_create_baseline)
    registry.register("ple.get_baseline_diff", _ple_get_baseline_diff)

    # DB query tools (generic)
    registry.register("db.list_requirements", _db_list_requirements)
    registry.register("db.list_functions", _db_list_functions)
    registry.register("db.list_scs", _db_list_scs)
    registry.register("db.list_sscs", _db_list_sscs)
    registry.register("db.list_ecus", _db_list_ecus)
    registry.register("db.list_signals", _db_list_signals)
    registry.register("db.list_baselines", _db_list_baselines)
    registry.register("db.list_ccps", _db_list_ccps)

    # Knowledge layer tools
    registry.register("knowledge.rag_search", _knowledge_rag_search)
    registry.register("knowledge.prompt_render", _knowledge_prompt_render)

    return registry


# ---------- PLE Tool wrappers (lazy-initialize PLEEngine with db) ----------

async def _ple_build_150(db, project_id: str) -> dict:
    from aivas.domain.ple.variant import PLEEngine
    return await PLEEngine(db).build_150_model(project_id)


async def _ple_resolve_variant(db, project_id: str, tag_ids: list[str]) -> dict:
    from aivas.domain.ple.variant import PLEEngine
    return await PLEEngine(db).resolve_variant(project_id, tag_ids)


async def _ple_create_baseline(db, project_id: str, name: str, tag_ids: list[str]) -> dict:
    from aivas.domain.ple.variant import PLEEngine
    return await PLEEngine(db).create_baseline(project_id, name, tag_ids)


async def _ple_get_baseline_diff(db, baseline_id: str, project_id: str, tag_ids: list[str]) -> dict:
    from aivas.domain.ple.variant import PLEEngine
    return await PLEEngine(db).get_baseline_diff(baseline_id, project_id, tag_ids)


# ---------- Generic DB list tools ----------

async def _db_list_requirements(db, project_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.requirement import Requirement
    import uuid
    result = await db.execute(
        select(Requirement).where(Requirement.project_id == uuid.UUID(project_id))
    )
    return [{"id": str(r.id), "type": r.type, "content": r.content} for r in result.scalars().all()]


async def _db_list_functions(db, project_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.function import Function
    import uuid
    result = await db.execute(
        select(Function).where(Function.project_id == uuid.UUID(project_id))
    )
    return [{"id": str(f.id), "name": f.name, "description": f.description} for f in result.scalars().all()]


async def _db_list_scs(db, project_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.sc import SC
    import uuid
    result = await db.execute(
        select(SC).where(SC.project_id == uuid.UUID(project_id))
    )
    return [{"id": str(s.id), "name": s.name, "type": s.type} for s in result.scalars().all()]


async def _db_list_sscs(db, sc_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.sc import SSC
    import uuid
    result = await db.execute(
        select(SSC).where(SSC.sc_id == uuid.UUID(sc_id))
    )
    return [{"id": str(s.id), "name": s.name, "description": s.description} for s in result.scalars().all()]


async def _db_list_ecus(db, project_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.ecu import ECU
    import uuid
    result = await db.execute(
        select(ECU).where(ECU.project_id == uuid.UUID(project_id))
    )
    return [{"id": str(e.id), "name": e.name, "type": e.type} for e in result.scalars().all()]


async def _db_list_signals(db, ssc_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.signal import Signal
    import uuid
    result = await db.execute(
        select(Signal).where(Signal.ssc_id == uuid.UUID(ssc_id))
    )
    return [{"id": str(s.id), "name": s.name, "direction": s.direction} for s in result.scalars().all()]


async def _db_list_baselines(db, project_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.baseline import Baseline
    import uuid
    result = await db.execute(
        select(Baseline).where(Baseline.project_id == uuid.UUID(project_id))
    )
    return [{"id": str(b.id), "name": b.name, "status": b.status} for b in result.scalars().all()]


async def _db_list_ccps(db, ssc_id: str) -> list:
    from sqlalchemy import select
    from aivas.models.ccp import CCP
    import uuid
    result = await db.execute(
        select(CCP).where(CCP.ssc_id == uuid.UUID(ssc_id))
    )
    return [{"id": str(c.id), "name": c.name, "value_type": c.value_type} for c in result.scalars().all()]


# ---------- Knowledge layer tool wrappers ----------

async def _knowledge_rag_search(db, project_id: str, query: str, top_k: int = 5) -> dict:
    from aivas.knowledge.rag import get_rag_engine
    engine = get_rag_engine(db)
    return await engine.hybrid_search(project_id, query, top_k=top_k)


async def _knowledge_prompt_render(name: str, variables: dict, version: str = "v1") -> str:
    from aivas.knowledge.prompts import get_prompt_registry
    registry = get_prompt_registry()
    return registry.render(name, variables, version)
