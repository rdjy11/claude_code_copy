import uuid

import strawberry
from sqlalchemy import text
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info
from fastapi import Depends

from aivas.database import get_db
from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
from aivas.domain.ple.variant import PLEEngine


# --- Types ---

@strawberry.type
class Project:
    id: uuid.UUID
    name: str
    description: str | None


@strawberry.type
class Tag:
    id: uuid.UUID
    project_id: uuid.UUID
    level: int
    name: str
    description: str | None
    parent_tag_id: uuid.UUID | None


@strawberry.type
class Requirement:
    id: uuid.UUID
    project_id: uuid.UUID
    type: str
    content: str
    tag_id: uuid.UUID | None
    version: int
    parent_req_id: uuid.UUID | None


@strawberry.type
class Function:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    description: str | None
    parent_func_id: uuid.UUID | None
    tag_id: uuid.UUID | None
    requirement_id: uuid.UUID | None = None


@strawberry.type
class SC:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    type: str | None
    description: str | None
    tag_id: uuid.UUID | None
    function_id: uuid.UUID | None = None


@strawberry.type
class SSC:
    id: uuid.UUID
    sc_id: uuid.UUID
    name: str
    description: str | None
    tag_id: uuid.UUID | None


@strawberry.type
class ECU:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    type: str
    description: str | None
    parent_ecu_id: uuid.UUID | None
    tag_id: uuid.UUID | None


@strawberry.type
class Signal:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    direction: str
    feature_tag: str | None
    ssc_id: uuid.UUID


@strawberry.type
class Baseline:
    id: uuid.UUID
    project_id: uuid.UUID
    name: str
    tag_id: uuid.UUID | None
    status: str


@strawberry.type
class AIResponse:
    answer: str
    sources: list[str] | None = None
    diagram: str | None = None


# --- RFLP Trace Types ---

@strawberry.type
class TraceItem:
    requirement_id: str
    requirement_type: str
    requirement_content: str
    function_id: str
    function_name: str
    sc_id: str
    sc_name: str
    ssc_id: str
    ssc_name: str
    ecus: list[str]


@strawberry.type
class TraceMatrix:
    project_id: str
    layers: list[str]
    traces: list[TraceItem]
    total_traces: int


@strawberry.type
class RFLPSummary:
    project_id: str
    requirements: int
    functions: int
    scs: int
    sscs: int
    ecus: int
    orphan_functions: int
    orphan_scs: int


# --- Diagram Types ---

@strawberry.type
class DiagramNode:
    id: str
    type: str  # "default" | "input" | "output" | "group"
    data_label: str = strawberry.field(name="data_label")
    data_description: str | None = strawberry.field(name="data_description", default=None)
    position_x: float = strawberry.field(name="position_x", default=0.0)
    position_y: float = strawberry.field(name="position_y", default=0.0)


@strawberry.type
class DiagramEdge:
    id: str
    source: str
    target: str
    animated: bool = False
    label: str | None = None


@strawberry.type
class Diagram:
    diagram_type: str
    nodes: list[DiagramNode]
    edges: list[DiagramEdge]


# --- PLE Types ---

@strawberry.type
class PLEAsset:
    id: str
    label: str
    detail: str | None = None
    tag_id: str | None = None


@strawberry.type
class PLE150Model:
    project_id: str
    total_assets: int
    requirements: list[PLEAsset]
    functions: list[PLEAsset]
    scs: list[PLEAsset]
    sscs: list[PLEAsset]
    ecus: list[PLEAsset]
    signals: list[PLEAsset]


@strawberry.type
class PLEVariant:
    project_id: str
    tag_ids: list[str]
    total_assets: int
    requirements: list[PLEAsset]
    functions: list[PLEAsset]
    scs: list[PLEAsset]
    sscs: list[PLEAsset]
    ecus: list[PLEAsset]


@strawberry.type
class BaselineResult:
    baseline_id: str
    name: str
    status: str
    item_count: int
    tag_ids: list[str]


@strawberry.type
class BaselineDiffItem:
    item_type: str
    item_id: str


@strawberry.type
class BaselineDiff:
    baseline_id: str
    added: list[BaselineDiffItem]
    removed: list[BaselineDiffItem]
    total_added: int
    total_removed: int


# --- Queries ---

@strawberry.type
class Query:
    @strawberry.field
    async def projects(self, info: Info) -> list[Project]:
        db = info.context["db"]
        result = await db.execute("SELECT * FROM projects ORDER BY created_at DESC")
        return [Project(id=r[0], name=r[1], description=r[2]) for r in result.fetchall()]

    @strawberry.field
    async def project(self, info: Info, id: uuid.UUID) -> Project | None:
        db = info.context["db"]
        result = await db.execute("SELECT * FROM projects WHERE id = $1", (id,))
        r = result.fetchone()
        if not r:
            return None
        return Project(id=r[0], name=r[1], description=r[2])

    @strawberry.field
    async def tags(self, info: Info, project_id: uuid.UUID) -> list[Tag]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT * FROM tags WHERE project_id = $1 ORDER BY level, name", (project_id,),
        )
        return [
            Tag(id=r[0], project_id=r[1], level=r[2], name=r[3], description=r[4], parent_tag_id=r[5])
            for r in result.fetchall()
        ]

    @strawberry.field
    async def requirements(
        self, info: Info, project_id: uuid.UUID, type: str | None = None
    ) -> list[Requirement]:
        db = info.context["db"]
        if type:
            result = await db.execute(
                "SELECT * FROM requirements WHERE project_id = $1 AND type = $2 ORDER BY created_at DESC",
                (project_id, type),
            )
        else:
            result = await db.execute(
                "SELECT * FROM requirements WHERE project_id = $1 ORDER BY created_at DESC",
                (project_id,),
            )
        return [
            Requirement(id=r[0], project_id=r[1], type=r[2], content=r[3], tag_id=r[4], version=r[5], parent_req_id=r[6])
            for r in result.fetchall()
        ]

    @strawberry.field
    async def functions(
        self, info: Info, project_id: uuid.UUID
    ) -> list[Function]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT * FROM functions WHERE project_id = $1 ORDER BY name", (project_id,),
        )
        return [
            Function(
                id=r[0], project_id=r[1], name=r[2], description=r[3],
                parent_func_id=r[4], tag_id=r[5], requirement_id=r[6],
            )
            for r in result.fetchall()
        ]

    @strawberry.field
    async def scs(self, info: Info, project_id: uuid.UUID) -> list[SC]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT * FROM scs WHERE project_id = $1 ORDER BY name", (project_id,),
        )
        return [
            SC(
                id=r[0], project_id=r[1], name=r[2], type=r[3],
                description=r[4], tag_id=r[5], function_id=r[6],
            )
            for r in result.fetchall()
        ]

    @strawberry.field
    async def sscs(self, info: Info, project_id: uuid.UUID) -> list[SSC]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT sscs.* FROM sscs JOIN scs ON sscs.sc_id = scs.id WHERE scs.project_id = $1 ORDER BY sscs.name",
            (project_id,),
        )
        return [
            SSC(id=r[0], sc_id=r[1], name=r[2], description=r[3], tag_id=r[4])
            for r in result.fetchall()
        ]

    @strawberry.field
    async def ecus(self, info: Info, project_id: uuid.UUID) -> list[ECU]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT * FROM ecus WHERE project_id = $1 ORDER BY name", (project_id,),
        )
        return [
            ECU(id=r[0], project_id=r[1], name=r[2], type=r[3], description=r[4], parent_ecu_id=r[5], tag_id=r[6])
            for r in result.fetchall()
        ]

    @strawberry.field
    async def baselines(self, info: Info, project_id: uuid.UUID) -> list[Baseline]:
        db = info.context["db"]
        result = await db.execute(
            "SELECT * FROM baselines WHERE project_id = $1 ORDER BY created_at DESC", (project_id,),
        )
        return [
            Baseline(id=r[0], project_id=r[1], name=r[2], tag_id=r[3], status=r[4])
            for r in result.fetchall()
        ]

    # RFLP Trace

    @strawberry.field
    async def trace_matrix(self, info: Info, project_id: str) -> TraceMatrix:
        db = info.context["db"]
        data = await get_trace_matrix(db, project_id)
        return TraceMatrix(
            project_id=data["project_id"],
            layers=data["layers"],
            traces=[TraceItem(**t) for t in data["traces"]],
            total_traces=data["total_traces"],
        )

    @strawberry.field
    async def rflp_summary(self, info: Info, project_id: str) -> RFLPSummary:
        db = info.context["db"]
        data = await get_rflp_summary(db, project_id)
        return RFLPSummary(**data)

    # Diagram data

    @strawberry.field
    async def diagram(self, info: Info, project_id: str, diagram_type: str) -> Diagram:
        db = info.context["db"]
        pid = uuid.UUID(project_id)

        if diagram_type == "BDD":
            return await _build_bdd_diagram(db, pid)
        elif diagram_type == "IBD":
            return await _build_ibd_diagram(db, pid)
        elif diagram_type == "Topology":
            return await _build_topology_diagram(db, pid)
        return Diagram(diagram_type=diagram_type, nodes=[], edges=[])

    # PLE

    @strawberry.field
    async def ple_150_model(self, info: Info, project_id: str) -> PLE150Model:
        db = info.context["db"]
        engine = PLEEngine(db)
        data = await engine.build_150_model(project_id)
        return PLE150Model(
            project_id=data["project_id"],
            total_assets=data["total_assets"],
            requirements=[PLEAsset(**r) for r in data["requirements"]],
            functions=[PLEAsset(**f) for f in data["functions"]],
            scs=[PLEAsset(**s) for s in data["scs"]],
            sscs=[PLEAsset(**s) for s in data["sscs"]],
            ecus=[PLEAsset(**e) for e in data["ecus"]],
            signals=[PLEAsset(**s) for s in data["signals"]],
        )

    @strawberry.field
    async def ple_resolve_variant(
        self, info: Info, project_id: str, tag_ids: list[str]
    ) -> PLEVariant:
        db = info.context["db"]
        engine = PLEEngine(db)
        data = await engine.resolve_variant(project_id, tag_ids)
        va = data["variant_assets"]
        return PLEVariant(
            project_id=data["project_id"],
            tag_ids=data["tag_ids"],
            total_assets=data["total_assets"],
            requirements=[PLEAsset(**r) for r in va["requirements"]],
            functions=[PLEAsset(**f) for f in va["functions"]],
            scs=[PLEAsset(**s) for s in va["scs"]],
            sscs=[PLEAsset(**s) for s in va["sscs"]],
            ecus=[PLEAsset(**e) for e in va["ecus"]],
        )


# --- Mutations ---

@strawberry.input
class ProjectInput:
    name: str
    description: str | None = None


@strawberry.input
class TagInput:
    level: int
    name: str
    description: str | None = None
    parent_tag_id: uuid.UUID | None = None


@strawberry.input
class RequirementInput:
    type: str
    content: str
    tag_id: uuid.UUID | None = None
    parent_req_id: uuid.UUID | None = None


@strawberry.input
class FunctionInput:
    name: str
    description: str | None = None
    requirement_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None
    parent_func_id: uuid.UUID | None = None


@strawberry.input
class SCInput:
    name: str
    type: str | None = None
    description: str | None = None
    function_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None


@strawberry.input
class ECUInput:
    name: str
    type: str = "generic"
    description: str | None = None
    parent_ecu_id: uuid.UUID | None = None
    tag_id: uuid.UUID | None = None


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_project(self, info: Info, input: ProjectInput) -> Project:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO projects (name, description) VALUES ($1, $2) RETURNING *",
            (input.name, input.description),
        )
        r = result.fetchone()
        return Project(id=r[0], name=r[1], description=r[2])

    @strawberry.mutation
    async def create_tag(self, info: Info, project_id: uuid.UUID, input: TagInput) -> Tag:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO tags (project_id, level, name, description, parent_tag_id) VALUES ($1, $2, $3, $4, $5) RETURNING *",
            (project_id, input.level, input.name, input.description, input.parent_tag_id),
        )
        r = result.fetchone()
        return Tag(id=r[0], project_id=r[1], level=r[2], name=r[3], description=r[4], parent_tag_id=r[5])

    @strawberry.mutation
    async def create_requirement(
        self, info: Info, project_id: uuid.UUID, input: RequirementInput
    ) -> Requirement:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO requirements (project_id, type, content, tag_id, parent_req_id) VALUES ($1, $2, $3, $4, $5) RETURNING *",
            (project_id, input.type, input.content, input.tag_id, input.parent_req_id),
        )
        r = result.fetchone()
        return Requirement(id=r[0], project_id=r[1], type=r[2], content=r[3], tag_id=r[4], version=r[5], parent_req_id=r[6])

    @strawberry.mutation
    async def create_function(
        self, info: Info, project_id: uuid.UUID, input: FunctionInput
    ) -> Function:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO functions (project_id, name, description, requirement_id, tag_id, parent_func_id) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            (project_id, input.name, input.description, input.requirement_id, input.tag_id, input.parent_func_id),
        )
        r = result.fetchone()
        return Function(
            id=r[0], project_id=r[1], name=r[2], description=r[3],
            parent_func_id=r[4], tag_id=r[5], requirement_id=r[6],
        )

    @strawberry.mutation
    async def create_sc(self, info: Info, project_id: uuid.UUID, input: SCInput) -> SC:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO scs (project_id, name, type, description, function_id, tag_id) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            (project_id, input.name, input.type, input.description, input.function_id, input.tag_id),
        )
        r = result.fetchone()
        return SC(
            id=r[0], project_id=r[1], name=r[2], type=r[3],
            description=r[4], tag_id=r[5], function_id=r[6],
        )

    @strawberry.mutation
    async def create_ecu(self, info: Info, project_id: uuid.UUID, input: ECUInput) -> ECU:
        db = info.context["db"]
        result = await db.execute(
            "INSERT INTO ecus (project_id, name, type, description, parent_ecu_id, tag_id) VALUES ($1, $2, $3, $4, $5, $6) RETURNING *",
            (project_id, input.name, input.type, input.description, input.parent_ecu_id, input.tag_id),
        )
        r = result.fetchone()
        return ECU(id=r[0], project_id=r[1], name=r[2], type=r[3], description=r[4], parent_ecu_id=r[5], tag_id=r[6])

    @strawberry.mutation
    async def create_baseline(
        self, info: Info, project_id: str, name: str, tag_ids: list[str]
    ) -> BaselineResult:
        db = info.context["db"]
        engine = PLEEngine(db)
        data = await engine.create_baseline(project_id, name, tag_ids)
        return BaselineResult(**data)

    @strawberry.mutation
    async def baseline_diff(
        self, info: Info, baseline_id: str, project_id: str, tag_ids: list[str]
    ) -> BaselineDiff:
        db = info.context["db"]
        engine = PLEEngine(db)
        data = await engine.get_baseline_diff(baseline_id, project_id, tag_ids)
        return BaselineDiff(
            baseline_id=data["baseline_id"],
            added=[BaselineDiffItem(**a) for a in data["added"]],
            removed=[BaselineDiffItem(**r) for r in data["removed"]],
            total_added=data["total_added"],
            total_removed=data["total_removed"],
        )

    @strawberry.mutation
    async def send_message(
        self, info: Info, project_id: str, message: str
    ) -> AIResponse:
        """Agent message endpoint — routes through orchestrator to specialized agents."""
        db = info.context["db"]

        from aivas.integrations.llm import get_llm_provider
        from aivas.bootstrap import build_agent_system

        llm = get_llm_provider()
        intent = await llm.classify_intent(message, [
            "requirements", "functional", "logical", "physical",
            "variant", "baseline", "verification", "conversational",
        ])

        # Route intent to agent key name
        agent_route = {
            "requirements": "Requirements",
            "functional": "Functional",
            "logical": "Logical",
            "physical": "Physical",
            "variant": "PLE/Variant",
            "baseline": "Baseline",
            "verification": "Verification",
            "conversational": "Conversational",
        }
        agent_name = agent_route.get(intent, "Conversational")

        # Try agent system execution with LLM
        try:
            orchestrator, _ = build_agent_system()
            result = await orchestrator.execute({
                "message": message,
                "project_id": project_id,
            })

            # Extract answer from the dispatched agent's response
            for resp in result.get("responses", []):
                agent_result = resp.get("result", {})
                if agent_result.get("answer"):
                    return AIResponse(
                        answer=agent_result["answer"],
                        sources=[],
                        diagram=None,
                    )
                if agent_result.get("summary"):
                    return AIResponse(
                        answer=agent_result["summary"],
                        sources=[],
                        diagram=None,
                    )

            # Fallback: build summary from orchestrator result
            agents_called = result.get("agents_called", [])
            return AIResponse(
                answer=f"[{llm.model_name}] 已路由至 {', '.join(agents_called)} 处理: \"{message[:100]}\"",
                sources=[],
                diagram=None,
            )
        except Exception:
            pass

        # DB-based fallback (Mock mode or agent system unavailable)
        from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
        from aivas.domain.ple.variant import PLEEngine

        if intent == "verification":
            summary = await get_rflp_summary(db, project_id)
            matrix = await get_trace_matrix(db, project_id)
            answer = (
                f"RFLP 追溯完整性检查完成。\n"
                f"需求: {summary['requirements']} | 功能: {summary['functions']} "
                f"| SC: {summary['scs']} | SSC: {summary['sscs']} | ECU: {summary['ecus']}\n"
                f"完整追溯链: {matrix['total_traces']} 条\n"
                f"孤立功能(无需求链接): {summary['orphan_functions']} | "
                f"孤立SC(无功能链接): {summary['orphan_scs']}"
            )

        elif intent == "variant":
            engine = PLEEngine(db)
            tags = await db.execute(
                "SELECT id, name, level FROM tags WHERE project_id = $1 ORDER BY level, name",
                (uuid.UUID(project_id),),
            )
            tag_rows = tags.fetchall()
            if tag_rows:
                tag_list = "\n".join(f"  L{r[2]}: {r[1]} ({r[0]})" for r in tag_rows[:10])
                model = await engine.build_150_model(project_id)
                answer = (
                    f"PLE 变体管理概览。\n"
                    f"可用标签 ({len(tag_rows)} 个):\n{tag_list}\n"
                    f"150%模型总资产: {model['total_assets']} 个"
                )
            else:
                answer = "项目暂无标签定义。请先在 PLE 标签/变体 视图中创建标签树。"

        elif intent == "baseline":
            engine = PLEEngine(db)
            baselines = await db.execute(
                "SELECT id, name, status FROM baselines WHERE project_id = $1 ORDER BY created_at DESC",
                (uuid.UUID(project_id),),
            )
            bl_rows = baselines.fetchall()
            if bl_rows:
                bl_list = "\n".join(f"  [{r[2]}] {r[1]} ({r[0]})" for r in bl_rows[:10])
                answer = f"基线列表 ({len(bl_rows)} 个):\n{bl_list}"
            else:
                answer = "项目暂无基线。请在 PLE 视图中选择标签后创建基线。"

        elif intent == "requirements":
            reqs = await db.execute(
                "SELECT type, COUNT(*) FROM requirements WHERE project_id = $1 GROUP BY type",
                (uuid.UUID(project_id),),
            )
            counts = {r[0]: r[1] for r in reqs.fetchall()}
            if counts:
                detail = " | ".join(f"{t}: {c}" for t, c in counts.items())
                answer = f"需求概览 (总计 {sum(counts.values())} 条): {detail}"
            else:
                answer = "项目暂无需求。请在需求视图中创建需求条目。"

        elif intent == "functional":
            funcs = await db.execute(
                "SELECT COUNT(*) FROM functions WHERE project_id = $1", (uuid.UUID(project_id),),
            )
            count = funcs.fetchone()[0]
            answer = f"功能层共 {count} 个功能模块。请在 BDD 视图中查看功能框图。"

        elif intent == "logical":
            scs = await db.execute(
                "SELECT COUNT(*) FROM scs WHERE project_id = $1", (uuid.UUID(project_id),),
            )
            sscs = await db.execute(
                "SELECT COUNT(*) FROM sscs JOIN scs ON sscs.sc_id = scs.id WHERE scs.project_id = $1",
                (uuid.UUID(project_id),),
            )
            answer = f"逻辑层共 {scs.fetchone()[0]} 个SC, {sscs.fetchone()[0]} 个SSC。请在 IBD 视图中查看子系统分解。"

        elif intent == "physical":
            ecus = await db.execute(
                "SELECT COUNT(*) FROM ecus WHERE project_id = $1", (uuid.UUID(project_id),),
            )
            answer = f"物理层共 {ecus.fetchone()[0]} 个ECU。请在拓扑视图中查看网络拓扑。"

        else:
            summary = await get_rflp_summary(db, project_id)
            answer = (
                f"AIVAS 项目概览 (model: {llm.model_name}):\n"
                f"R层需求: {summary['requirements']} | F层功能: {summary['functions']} "
                f"| L层SC: {summary['scs']} | P层ECU: {summary['ecus']}\n"
                f"请选择具体操作：需求分析 / 功能设计 / 逻辑架构 / 物理拓扑 / 变体管理 / 追溯验证"
            )

        return AIResponse(answer=answer, sources=[], diagram=None)


# --- Diagram builders ---

async def _build_bdd_diagram(db, project_id: uuid.UUID) -> Diagram:
    """Block Definition Diagram — top-level function blocks."""
    result = await db.execute(
        "SELECT id, name, description, parent_func_id FROM functions WHERE project_id = $1 ORDER BY name",
        (project_id,),
    )
    rows = result.fetchall()
    nodes: list[DiagramNode] = []
    edges: list[DiagramEdge] = []
    for i, r in enumerate(rows):
        nodes.append(DiagramNode(
            id=str(r[0]), type="default",
            data_label=r[1], data_description=r[2],
            position_x=(i % 4) * 220, position_y=(i // 4) * 120,
        ))
        if r[3]:  # has parent
            edges.append(DiagramEdge(
                id=f"e-{r[3]}-{r[0]}", source=str(r[3]), target=str(r[0]), animated=False,
            ))
    return Diagram(diagram_type="BDD", nodes=nodes, edges=edges)


async def _build_ibd_diagram(db, project_id: uuid.UUID) -> Diagram:
    """Internal Block Diagram — SC/SSC decomposition."""
    sc_result = await db.execute(
        "SELECT id, name FROM scs WHERE project_id = $1 ORDER BY name", (project_id,),
    )
    scs = sc_result.fetchall()
    ssc_result = await db.execute(
        "SELECT sscs.id, sscs.name, sscs.sc_id FROM sscs JOIN scs ON sscs.sc_id = scs.id WHERE scs.project_id = $1 ORDER BY sscs.name",
        (project_id,),
    )
    sscs = ssc_result.fetchall()

    nodes: list[DiagramNode] = []
    edges: list[DiagramEdge] = []
    for i, sc in enumerate(scs):
        nodes.append(DiagramNode(
            id=str(sc[0]), type="group", data_label=sc[1], data_description=None,
            position_x=i * 280, position_y=0,
        ))
    for j, ssc in enumerate(sscs):
        nodes.append(DiagramNode(
            id=str(ssc[0]), type="default", data_label=ssc[1], data_description=None,
            position_x=j * 200, position_y=200,
        ))
        edges.append(DiagramEdge(
            id=f"e-{ssc[2]}-{ssc[0]}", source=str(ssc[2]), target=str(ssc[0]),
        ))
    return Diagram(diagram_type="IBD", nodes=nodes, edges=edges)


async def _build_topology_diagram(db, project_id: uuid.UUID) -> Diagram:
    """Network topology — ECU nodes and signal edges."""
    ecu_result = await db.execute(
        "SELECT id, name, type, parent_ecu_id FROM ecus WHERE project_id = $1 ORDER BY name",
        (project_id,),
    )
    ecus = ecu_result.fetchall()
    sig_result = await db.execute(
        """SELECT s.id, s.name, s.direction, s.feature_tag, a.ecu_id
           FROM signals s
           JOIN signal_ecu_allocations a ON a.signal_id = s.id
           WHERE s.project_id = $1""",
        (project_id,),
    )
    signals = sig_result.fetchall()

    nodes: list[DiagramNode] = []
    edges: list[DiagramEdge] = []
    placed_ecus: set[str] = set()

    for i, ecu in enumerate(ecus):
        nodes.append(DiagramNode(
            id=str(ecu[0]), type="default", data_label=ecu[1], data_description=ecu[2],
            position_x=(i % 3) * 280, position_y=(i // 3) * 150,
        ))
        placed_ecus.add(str(ecu[0]))

    for sig in signals:
        sig_id = str(sig[0])
        ecu_id = str(sig[4])
        if ecu_id in placed_ecus:
            edges.append(DiagramEdge(
                id=f"e-sig-{sig_id}-{ecu_id}",
                source=sig_id, target=ecu_id,
                animated=sig[2] == "bidirectional",
                label=sig[1],
            ))
    return Diagram(diagram_type="Topology", nodes=nodes, edges=edges)


# --- Router ---

schema = strawberry.Schema(query=Query, mutation=Mutation)


async def get_graphql_context(db=Depends(get_db)):
    return {"db": db}


graphql_app = GraphQLRouter(schema, context_getter=get_graphql_context)
