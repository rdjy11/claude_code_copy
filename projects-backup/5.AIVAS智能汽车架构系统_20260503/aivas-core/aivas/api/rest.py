from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.database import get_db
from aivas.schemas.project import ProjectCreate, ProjectResponse
from aivas.schemas.tag import TagCreate, TagResponse
from aivas.schemas.requirement import RequirementCreate, RequirementResponse, RequirementUpdate
from aivas.schemas.function import FunctionCreate, FunctionUpdate, FunctionResponse
from aivas.schemas.sc import SCCreate, SCUpdate, SCResponse, SSCCreate, SSCUpdate, SSCResponse, SSCVersionCreate, SSCVersionResponse
from aivas.schemas.ecu import ECUCreate, ECUUpdate, ECUResponse
from aivas.schemas.signal import SignalCreate, SignalUpdate, SignalResponse, SignalECUAllocationCreate, SignalECUAllocationResponse
from aivas.schemas.baseline import BaselineCreate, BaselineUpdate, BaselineResponse, BaselineItemCreate, BaselineItemResponse
from aivas.schemas.ccp import CCPCreate, CCPUpdate, CCPResponse
from aivas.models.project import Project
from aivas.models.tag import Tag
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.sc import SC, SSC, SSCVersion
from aivas.models.ecu import ECU
from aivas.models.signal import Signal, SignalECUAllocation
from aivas.models.baseline import Baseline, BaselineItem
from aivas.models.ccp import CCP
from aivas.domain.rflp.trace import get_trace_matrix

router = APIRouter(prefix="/api", tags=["REST"])


# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------

@router.get("/projects", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM projects ORDER BY created_at DESC")
    return [ProjectResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(payload: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return ProjectResponse.model_validate(project)


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/tags", response_model=list[TagResponse])
async def list_tags(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM tags WHERE project_id = $1 ORDER BY level, name", (project_id,)
    )
    return [TagResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/tags", response_model=TagResponse, status_code=201)
async def create_tag(project_id: str, payload: TagCreate, db: AsyncSession = Depends(get_db)):
    tag = Tag(project_id=project_id, **payload.model_dump())
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return TagResponse.model_validate(tag)


# ---------------------------------------------------------------------------
# Requirements
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/requirements", response_model=list[RequirementResponse])
async def list_requirements(
    project_id: str,
    type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
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
    return [RequirementResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/requirements", response_model=RequirementResponse, status_code=201)
async def create_requirement(
    project_id: str,
    payload: RequirementCreate,
    db: AsyncSession = Depends(get_db),
):
    req = Requirement(project_id=project_id, **payload.model_dump())
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return RequirementResponse.model_validate(req)


@router.get("/requirements/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(requirement_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM requirements WHERE id = $1", (requirement_id,)
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return RequirementResponse.model_validate(row)


@router.patch("/requirements/{requirement_id}", response_model=RequirementResponse)
async def update_requirement(
    requirement_id: str,
    payload: RequirementUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        "SELECT * FROM requirements WHERE id = $1", (requirement_id,)
    )
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Requirement not found")
    await db.execute(
        "UPDATE requirements SET type=COALESCE($1,type), content=COALESCE($2,content), tag_id=COALESCE($3,tag_id) WHERE id=$4",
        (payload.type, payload.content, payload.tag_id, requirement_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM requirements WHERE id = $1", (requirement_id,))
    return RequirementResponse.model_validate(result.fetchone())


@router.delete("/requirements/{requirement_id}", status_code=204)
async def delete_requirement(requirement_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM requirements WHERE id = $1", (requirement_id,)
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Requirement not found")
    await db.execute("DELETE FROM requirements WHERE id = $1", (requirement_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# Functions
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/functions", response_model=list[FunctionResponse])
async def list_functions(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM functions WHERE project_id = $1 ORDER BY created_at DESC",
        (project_id,),
    )
    return [FunctionResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/functions", response_model=FunctionResponse, status_code=201)
async def create_function(project_id: str, payload: FunctionCreate, db: AsyncSession = Depends(get_db)):
    func = Function(project_id=project_id, **payload.model_dump())
    db.add(func)
    await db.commit()
    await db.refresh(func)
    return FunctionResponse.model_validate(func)


@router.get("/functions/{function_id}", response_model=FunctionResponse)
async def get_function(function_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM functions WHERE id = $1", (function_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Function not found")
    return FunctionResponse.model_validate(row)


@router.patch("/functions/{function_id}", response_model=FunctionResponse)
async def update_function(function_id: str, payload: FunctionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM functions WHERE id = $1", (function_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Function not found")
    await db.execute(
        "UPDATE functions SET name=COALESCE($1,name), description=COALESCE($2,description), "
        "tag_id=COALESCE($3,tag_id), requirement_id=COALESCE($4,requirement_id) WHERE id=$5",
        (payload.name, payload.description, payload.tag_id, payload.requirement_id, function_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM functions WHERE id = $1", (function_id,))
    return FunctionResponse.model_validate(result.fetchone())


@router.delete("/functions/{function_id}", status_code=204)
async def delete_function(function_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM functions WHERE id = $1", (function_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Function not found")
    await db.execute("DELETE FROM functions WHERE id = $1", (function_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# SCs
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/scs", response_model=list[SCResponse])
async def list_scs(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM scs WHERE project_id = $1 ORDER BY created_at DESC",
        (project_id,),
    )
    return [SCResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/scs", response_model=SCResponse, status_code=201)
async def create_sc(project_id: str, payload: SCCreate, db: AsyncSession = Depends(get_db)):
    sc = SC(project_id=project_id, **payload.model_dump())
    db.add(sc)
    await db.commit()
    await db.refresh(sc)
    return SCResponse.model_validate(sc)


@router.get("/scs/{sc_id}", response_model=SCResponse)
async def get_sc(sc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM scs WHERE id = $1", (sc_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="SC not found")
    return SCResponse.model_validate(row)


@router.patch("/scs/{sc_id}", response_model=SCResponse)
async def update_sc(sc_id: str, payload: SCUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM scs WHERE id = $1", (sc_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="SC not found")
    await db.execute(
        "UPDATE scs SET name=COALESCE($1,name), type=COALESCE($2,type), "
        "description=COALESCE($3,description), tag_id=COALESCE($4,tag_id), "
        "function_id=COALESCE($5,function_id) WHERE id=$6",
        (payload.name, payload.type, payload.description, payload.tag_id, payload.function_id, sc_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM scs WHERE id = $1", (sc_id,))
    return SCResponse.model_validate(result.fetchone())


@router.delete("/scs/{sc_id}", status_code=204)
async def delete_sc(sc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM scs WHERE id = $1", (sc_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="SC not found")
    await db.execute("DELETE FROM scs WHERE id = $1", (sc_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# SSCs (nested under SC)
# ---------------------------------------------------------------------------

@router.get("/scs/{sc_id}/sscs", response_model=list[SSCResponse])
async def list_sscs(sc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM sscs WHERE sc_id = $1 ORDER BY created_at DESC",
        (sc_id,),
    )
    return [SSCResponse.model_validate(r) for r in result.fetchall()]


@router.post("/scs/{sc_id}/sscs", response_model=SSCResponse, status_code=201)
async def create_ssc(sc_id: str, payload: SSCCreate, db: AsyncSession = Depends(get_db)):
    ssc = SSC(sc_id=sc_id, **payload.model_dump())
    db.add(ssc)
    await db.commit()
    await db.refresh(ssc)
    return SSCResponse.model_validate(ssc)


@router.get("/sscs/{ssc_id}", response_model=SSCResponse)
async def get_ssc(ssc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM sscs WHERE id = $1", (ssc_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="SSC not found")
    return SSCResponse.model_validate(row)


@router.patch("/sscs/{ssc_id}", response_model=SSCResponse)
async def update_ssc(ssc_id: str, payload: SSCUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM sscs WHERE id = $1", (ssc_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="SSC not found")
    await db.execute(
        "UPDATE sscs SET name=COALESCE($1,name), description=COALESCE($2,description), "
        "tag_id=COALESCE($3,tag_id) WHERE id=$4",
        (payload.name, payload.description, payload.tag_id, ssc_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM sscs WHERE id = $1", (ssc_id,))
    return SSCResponse.model_validate(result.fetchone())


@router.delete("/sscs/{ssc_id}", status_code=204)
async def delete_ssc(ssc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM sscs WHERE id = $1", (ssc_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="SSC not found")
    await db.execute("DELETE FROM sscs WHERE id = $1", (ssc_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# SSC Versions
# ---------------------------------------------------------------------------

@router.get("/sscs/{ssc_id}/versions", response_model=list[SSCVersionResponse])
async def list_ssc_versions(ssc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM ssc_versions WHERE ssc_id = $1 ORDER BY created_at DESC",
        (ssc_id,),
    )
    return [SSCVersionResponse.model_validate(r) for r in result.fetchall()]


@router.post("/sscs/{ssc_id}/versions", response_model=SSCVersionResponse, status_code=201)
async def create_ssc_version(ssc_id: str, payload: SSCVersionCreate, db: AsyncSession = Depends(get_db)):
    ver = SSCVersion(ssc_id=ssc_id, **payload.model_dump())
    db.add(ver)
    await db.commit()
    await db.refresh(ver)
    return SSCVersionResponse.model_validate(ver)


# ---------------------------------------------------------------------------
# ECUs
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/ecus", response_model=list[ECUResponse])
async def list_ecus(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM ecus WHERE project_id = $1 ORDER BY created_at DESC",
        (project_id,),
    )
    return [ECUResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/ecus", response_model=ECUResponse, status_code=201)
async def create_ecu(project_id: str, payload: ECUCreate, db: AsyncSession = Depends(get_db)):
    ecu = ECU(project_id=project_id, **payload.model_dump())
    db.add(ecu)
    await db.commit()
    await db.refresh(ecu)
    return ECUResponse.model_validate(ecu)


@router.get("/ecus/{ecu_id}", response_model=ECUResponse)
async def get_ecu(ecu_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ecus WHERE id = $1", (ecu_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="ECU not found")
    return ECUResponse.model_validate(row)


@router.patch("/ecus/{ecu_id}", response_model=ECUResponse)
async def update_ecu(ecu_id: str, payload: ECUUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ecus WHERE id = $1", (ecu_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="ECU not found")
    await db.execute(
        "UPDATE ecus SET name=COALESCE($1,name), type=COALESCE($2,type), "
        "description=COALESCE($3,description), tag_id=COALESCE($4,tag_id) WHERE id=$5",
        (payload.name, payload.type, payload.description, payload.tag_id, ecu_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM ecus WHERE id = $1", (ecu_id,))
    return ECUResponse.model_validate(result.fetchone())


@router.delete("/ecus/{ecu_id}", status_code=204)
async def delete_ecu(ecu_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ecus WHERE id = $1", (ecu_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="ECU not found")
    await db.execute("DELETE FROM ecus WHERE id = $1", (ecu_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# Signals
# ---------------------------------------------------------------------------

@router.get("/sscs/{ssc_id}/signals", response_model=list[SignalResponse])
async def list_signals(ssc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM signals WHERE ssc_id = $1 ORDER BY created_at DESC",
        (ssc_id,),
    )
    return [SignalResponse.model_validate(r) for r in result.fetchall()]


@router.post("/sscs/{ssc_id}/signals", response_model=SignalResponse, status_code=201)
async def create_signal(ssc_id: str, payload: SignalCreate, db: AsyncSession = Depends(get_db)):
    sig = Signal(ssc_id=ssc_id, **payload.model_dump())
    db.add(sig)
    await db.commit()
    await db.refresh(sig)
    return SignalResponse.model_validate(sig)


@router.get("/signals/{signal_id}", response_model=SignalResponse)
async def get_signal(signal_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM signals WHERE id = $1", (signal_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Signal not found")
    return SignalResponse.model_validate(row)


@router.patch("/signals/{signal_id}", response_model=SignalResponse)
async def update_signal(signal_id: str, payload: SignalUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM signals WHERE id = $1", (signal_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Signal not found")
    await db.execute(
        "UPDATE signals SET name=COALESCE($1,name), direction=COALESCE($2,direction), "
        "feature_tag=COALESCE($3,feature_tag) WHERE id=$4",
        (payload.name, payload.direction, payload.feature_tag, signal_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM signals WHERE id = $1", (signal_id,))
    return SignalResponse.model_validate(result.fetchone())


@router.delete("/signals/{signal_id}", status_code=204)
async def delete_signal(signal_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM signals WHERE id = $1", (signal_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Signal not found")
    await db.execute("DELETE FROM signals WHERE id = $1", (signal_id,))
    await db.commit()


# --- Signal-ECU Allocations ---

@router.get("/signals/{signal_id}/allocations", response_model=list[SignalECUAllocationResponse])
async def list_signal_allocations(signal_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM signal_ecu_allocations WHERE signal_id = $1 ORDER BY created_at DESC",
        (signal_id,),
    )
    return [SignalECUAllocationResponse.model_validate(r) for r in result.fetchall()]


@router.post("/signals/{signal_id}/allocations", response_model=SignalECUAllocationResponse, status_code=201)
async def create_signal_allocation(
    signal_id: str, payload: SignalECUAllocationCreate, db: AsyncSession = Depends(get_db)
):
    alloc = SignalECUAllocation(signal_id=signal_id, **payload.model_dump())
    db.add(alloc)
    await db.commit()
    await db.refresh(alloc)
    return SignalECUAllocationResponse.model_validate(alloc)


@router.delete("/allocations/{allocation_id}", status_code=204)
async def delete_signal_allocation(allocation_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM signal_ecu_allocations WHERE id = $1", (allocation_id,)
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Allocation not found")
    await db.execute("DELETE FROM signal_ecu_allocations WHERE id = $1", (allocation_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# Baselines
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/baselines", response_model=list[BaselineResponse])
async def list_baselines(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM baselines WHERE project_id = $1 ORDER BY created_at DESC",
        (project_id,),
    )
    return [BaselineResponse.model_validate(r) for r in result.fetchall()]


@router.post("/projects/{project_id}/baselines", response_model=BaselineResponse, status_code=201)
async def create_baseline(project_id: str, payload: BaselineCreate, db: AsyncSession = Depends(get_db)):
    bl = Baseline(project_id=project_id, **payload.model_dump())
    db.add(bl)
    await db.commit()
    await db.refresh(bl)
    return BaselineResponse.model_validate(bl)


@router.get("/baselines/{baseline_id}", response_model=BaselineResponse)
async def get_baseline(baseline_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM baselines WHERE id = $1", (baseline_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Baseline not found")
    return BaselineResponse.model_validate(row)


@router.patch("/baselines/{baseline_id}", response_model=BaselineResponse)
async def update_baseline(baseline_id: str, payload: BaselineUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM baselines WHERE id = $1", (baseline_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Baseline not found")
    await db.execute(
        "UPDATE baselines SET name=COALESCE($1,name), status=COALESCE($2,status) WHERE id=$3",
        (payload.name, payload.status, baseline_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM baselines WHERE id = $1", (baseline_id,))
    return BaselineResponse.model_validate(result.fetchone())


@router.delete("/baselines/{baseline_id}", status_code=204)
async def delete_baseline(baseline_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM baselines WHERE id = $1", (baseline_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Baseline not found")
    await db.execute("DELETE FROM baselines WHERE id = $1", (baseline_id,))
    await db.commit()


# --- Baseline Items ---

@router.get("/baselines/{baseline_id}/items", response_model=list[BaselineItemResponse])
async def list_baseline_items(baseline_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM baseline_items WHERE baseline_id = $1 ORDER BY created_at DESC",
        (baseline_id,),
    )
    return [BaselineItemResponse.model_validate(r) for r in result.fetchall()]


@router.post("/baselines/{baseline_id}/items", response_model=BaselineItemResponse, status_code=201)
async def create_baseline_item(
    baseline_id: str, payload: BaselineItemCreate, db: AsyncSession = Depends(get_db)
):
    item = BaselineItem(baseline_id=baseline_id, **payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return BaselineItemResponse.model_validate(item)


@router.delete("/baselines/items/{item_id}", status_code=204)
async def delete_baseline_item(item_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM baseline_items WHERE id = $1", (item_id,)
    )
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="Baseline item not found")
    await db.execute("DELETE FROM baseline_items WHERE id = $1", (item_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# CCPs
# ---------------------------------------------------------------------------

@router.get("/sscs/{ssc_id}/ccps", response_model=list[CCPResponse])
async def list_ccps(ssc_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        "SELECT * FROM ccps WHERE ssc_id = $1 ORDER BY created_at DESC",
        (ssc_id,),
    )
    return [CCPResponse.model_validate(r) for r in result.fetchall()]


@router.post("/sscs/{ssc_id}/ccps", response_model=CCPResponse, status_code=201)
async def create_ccp(ssc_id: str, payload: CCPCreate, db: AsyncSession = Depends(get_db)):
    ccp = CCP(ssc_id=ssc_id, **payload.model_dump())
    db.add(ccp)
    await db.commit()
    await db.refresh(ccp)
    return CCPResponse.model_validate(ccp)


@router.get("/ccps/{ccp_id}", response_model=CCPResponse)
async def get_ccp(ccp_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ccps WHERE id = $1", (ccp_id,))
    row = result.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="CCP not found")
    return CCPResponse.model_validate(row)


@router.patch("/ccps/{ccp_id}", response_model=CCPResponse)
async def update_ccp(ccp_id: str, payload: CCPUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ccps WHERE id = $1", (ccp_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="CCP not found")
    await db.execute(
        "UPDATE ccps SET name=COALESCE($1,name), value_type=COALESCE($2,value_type) WHERE id=$3",
        (payload.name, payload.value_type, ccp_id),
    )
    await db.commit()
    result = await db.execute("SELECT * FROM ccps WHERE id = $1", (ccp_id,))
    return CCPResponse.model_validate(result.fetchone())


@router.delete("/ccps/{ccp_id}", status_code=204)
async def delete_ccp(ccp_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM ccps WHERE id = $1", (ccp_id,))
    if not result.fetchone():
        raise HTTPException(status_code=404, detail="CCP not found")
    await db.execute("DELETE FROM ccps WHERE id = $1", (ccp_id,))
    await db.commit()


# ---------------------------------------------------------------------------
# Traceability
# ---------------------------------------------------------------------------

@router.get("/projects/{project_id}/trace-matrix")
async def get_trace(project_id: str, db: AsyncSession = Depends(get_db)):
    return await get_trace_matrix(db, project_id)
