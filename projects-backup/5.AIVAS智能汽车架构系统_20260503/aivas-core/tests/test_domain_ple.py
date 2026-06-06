"""Unit tests for PLE variant engine."""

import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.domain.ple.variant import PLEEngine
from aivas.models.tag import Tag
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.ecu import ECU
from aivas.models.project import Project


class TestBuild150Model:
    async def test_empty_project(self, db_session: AsyncSession, sample_project_id):
        engine = PLEEngine(db_session)
        model = await engine.build_150_model(sample_project_id)
        assert model["total_assets"] == 0

    async def test_with_tagged_assets(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        tag = Tag(project_id=pid, level=1, name="L1-ADAS")
        db_session.add(tag)
        await db_session.flush()

        req = Requirement(project_id=pid, type="functional", content="REQ-1", tag_id=tag.id)
        db_session.add(req)
        func = Function(project_id=pid, name="Func-1", tag_id=tag.id)
        db_session.add(func)
        ecus = ECU(project_id=pid, name="ECU-1", type="adas", tag_id=tag.id)
        db_session.add(ecus)
        await db_session.flush()

        engine = PLEEngine(db_session)
        model = await engine.build_150_model(sample_project_id)
        assert model["total_assets"] == 3
        assert len(model["requirements"]) == 1
        assert len(model["functions"]) == 1
        assert len(model["ecus"]) == 1


class TestResolveVariant:
    async def test_empty_tag_list(self, db_session: AsyncSession, sample_project_id):
        engine = PLEEngine(db_session)
        variant = await engine.resolve_variant(sample_project_id, [])
        assert variant["tag_ids"] == []
        assert variant.get("total_assets", 0) == 0

    async def test_resolves_matching_assets(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        tag_a = Tag(project_id=pid, level=1, name="L1-ADAS")
        tag_b = Tag(project_id=pid, level=2, name="L2-High")
        db_session.add_all([tag_a, tag_b])
        await db_session.flush()

        req_a = Requirement(project_id=pid, type="functional", content="High-end feature", tag_id=tag_a.id)
        req_b = Requirement(project_id=pid, type="functional", content="Base feature", tag_id=tag_b.id)
        db_session.add_all([req_a, req_b])
        await db_session.flush()

        engine = PLEEngine(db_session)
        variant = await engine.resolve_variant(sample_project_id, [str(tag_a.id)])
        assert variant["total_assets"] == 1
        assets = variant["variant_assets"]["requirements"]
        assert len(assets) == 1
        assert assets[0]["content"] == "High-end feature"


class TestCreateBaseline:
    async def test_creates_baseline_with_items(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        tag = Tag(project_id=pid, level=1, name="L1-ADAS")
        db_session.add(tag)
        await db_session.flush()

        req = Requirement(project_id=pid, type="functional", content="ACC REQ", tag_id=tag.id)
        db_session.add(req)
        await db_session.flush()

        engine = PLEEngine(db_session)
        result = await engine.create_baseline(sample_project_id, "BL-Test", [str(tag.id)])

        assert result["name"] == "BL-Test"
        assert result["status"] == "draft"
        assert result["item_count"] == 1
        assert result["baseline_id"] is not None


class TestGetBaselineDiff:
    async def test_detects_additions_and_removals(self, db_session: AsyncSession, sample_project_id):
        pid = uuid.UUID(sample_project_id)
        proj = Project(id=pid, name="test-proj", created_at=None, updated_at=None)
        db_session.add(proj)
        await db_session.flush()

        tag_a = Tag(project_id=pid, level=1, name="L1-ADAS")
        db_session.add(tag_a)
        await db_session.flush()

        req_a = Requirement(project_id=pid, type="functional", content="Original REQ", tag_id=tag_a.id)
        db_session.add(req_a)
        await db_session.flush()

        engine = PLEEngine(db_session)
        baseline = await engine.create_baseline(sample_project_id, "BL-V1", [str(tag_a.id)])

        # Add a new requirement with a new tag
        tag_b = Tag(project_id=pid, level=2, name="L2-New")
        db_session.add(tag_b)
        await db_session.flush()
        req_b = Requirement(project_id=pid, type="functional", content="New REQ", tag_id=tag_b.id)
        db_session.add(req_b)
        await db_session.flush()

        diff = await engine.get_baseline_diff(
            baseline["baseline_id"], sample_project_id,
            [str(tag_a.id), str(tag_b.id)],
        )
        assert diff["total_added"] == 1
        assert diff["total_removed"] == 0
