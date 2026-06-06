"""Unit tests for RFLP traceability engine."""

import uuid

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.sc import SC, SSC
from aivas.models.ecu import ECU
from aivas.models.signal import Signal, SignalECUAllocation
from aivas.models.project import Project


class TestGetRFLPSummary:
    async def test_empty_project(self, db_session: AsyncSession, sample_project_id):
        summary = await get_rflp_summary(db_session, sample_project_id)
        assert summary["project_id"] == sample_project_id
        assert summary["requirements"] == 0
        assert summary["functions"] == 0
        assert summary["scs"] == 0

    async def test_with_requirements(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        # Need project to exist for FK
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        for i in range(3):
            db_session.add(Requirement(project_id=pid, type="functional", content=f"REQ-{i}"))
        await db_session.flush()

        summary = await get_rflp_summary(db_session, sample_project_id)
        assert summary["requirements"] == 3
        assert summary["functions"] == 0

    async def test_detects_orphans(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        f = Function(project_id=pid, name="OrphanFunc", requirement_id=None)
        db_session.add(f)
        await db_session.flush()

        summary = await get_rflp_summary(db_session, sample_project_id)
        assert summary["orphan_functions"] == 1


class TestGetTraceMatrix:
    async def test_empty_project(self, db_session: AsyncSession, sample_project_id):
        trace_data = await get_trace_matrix(db_session, sample_project_id)
        assert trace_data["total_traces"] == 0
        assert trace_data["traces"] == []

    async def test_complete_rflp_chain(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        # Build a full RFLP chain
        req = Requirement(project_id=pid, type="functional", content="ACC shall maintain speed")
        db_session.add(req)
        await db_session.flush()

        func = Function(project_id=pid, name="Adaptive Cruise Control", requirement_id=req.id)
        db_session.add(func)
        await db_session.flush()

        sc = SC(project_id=pid, name="ACC Controller", function_id=func.id)
        db_session.add(sc)
        await db_session.flush()

        ssc = SSC(sc_id=sc.id, name="Speed Controller")
        db_session.add(ssc)
        await db_session.flush()

        signal = Signal(project_id=pid, name="TargetSpeed", direction="output", ssc_id=ssc.id)
        db_session.add(signal)
        await db_session.flush()

        ecu = ECU(project_id=pid, name="ADAS-ECU", type="adas")
        db_session.add(ecu)
        await db_session.flush()

        alloc = SignalECUAllocation(signal_id=signal.id, ecu_id=ecu.id)
        db_session.add(alloc)
        await db_session.flush()

        trace_data = await get_trace_matrix(db_session, sample_project_id)
        assert trace_data["total_traces"] == 1
        trace = trace_data["traces"][0]
        assert trace["requirement_content"] == "ACC shall maintain speed"
        assert trace["function_name"] == "Adaptive Cruise Control"
        assert trace["sc_name"] == "ACC Controller"
        assert trace["ssc_name"] == "Speed Controller"
        assert "ADAS-ECU" in trace["ecus"]
