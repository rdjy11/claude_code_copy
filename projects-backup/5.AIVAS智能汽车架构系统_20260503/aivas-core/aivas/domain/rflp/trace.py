"""RFLP traceability engine — Requirement → Function → Logical → Physical links."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.sc import SC, SSC
from aivas.models.signal import Signal, SignalECUAllocation
from aivas.models.ecu import ECU


async def get_trace_matrix(db: AsyncSession, project_id: str) -> dict:
    """Return the RFLP traceability matrix for a project.

    Traverses: Requirement → Function → SC → SSC → Signal → ECU
    Returns a list of complete trace chains across all four RFLP layers.
    """
    pid = uuid.UUID(project_id)

    reqs = await db.execute(
        select(Requirement)
        .where(Requirement.project_id == pid)
        .options(
            selectinload(Requirement.functions)
            .selectinload(Function.scs)
            .selectinload(SC.sscs)
            .selectinload(SSC.signals)
            .selectinload(Signal.ecu_allocations)
            .selectinload(SignalECUAllocation.ecu),
        )
    )
    reqs = reqs.scalars().all()

    traces: list[dict] = []
    for req in reqs:
        for func in req.functions:
            for sc in func.scs:
                for ssc in sc.sscs:
                    ecu_names = list({
                        alloc.ecu.name
                        for sig in ssc.signals
                        for alloc in sig.ecu_allocations
                    })
                    traces.append({
                        "requirement_id": str(req.id),
                        "requirement_type": req.type,
                        "requirement_content": req.content,
                        "function_id": str(func.id),
                        "function_name": func.name,
                        "sc_id": str(sc.id),
                        "sc_name": sc.name,
                        "ssc_id": str(ssc.id),
                        "ssc_name": ssc.name,
                        "ecus": ecu_names,
                    })

    return {
        "project_id": project_id,
        "layers": ["Requirement", "Functional", "Logical", "Physical"],
        "traces": traces,
        "total_traces": len(traces),
    }


async def get_rflp_summary(db: AsyncSession, project_id: str) -> dict:
    """Return per-layer counts and orphan counts for the project."""
    pid = uuid.UUID(project_id)

    req_count = (await db.execute(
        select(Requirement).where(Requirement.project_id == pid)
    )).scalars().all()

    funcs_raw = await db.execute(
        select(Function)
        .where(Function.project_id == pid)
        .options(selectinload(Function.requirement))
    )
    funcs = funcs_raw.scalars().all()

    scs_raw = await db.execute(
        select(SC)
        .where(SC.project_id == pid)
        .options(selectinload(SC.function))
    )
    scs = scs_raw.scalars().all()

    sscs_raw = await db.execute(
        select(SSC).join(SC).where(SC.project_id == pid)
    )
    sscs = sscs_raw.scalars().all()

    ecus = await db.execute(
        select(ECU).where(ECU.project_id == pid)
    )
    ecus = ecus.scalars().all()

    orphan_funcs = sum(1 for f in funcs if f.requirement_id is None)
    orphan_scs = sum(1 for s in scs if s.function_id is None)

    return {
        "project_id": project_id,
        "requirements": len(req_count),
        "functions": len(funcs),
        "scs": len(scs),
        "sscs": len(sscs),
        "ecus": len(ecus),
        "orphan_functions": orphan_funcs,
        "orphan_scs": orphan_scs,
    }
