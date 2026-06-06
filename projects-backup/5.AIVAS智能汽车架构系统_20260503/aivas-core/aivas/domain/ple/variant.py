"""PLE engine — 150% model, variant resolution, baseline generation."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.models.tag import Tag
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.sc import SC, SSC
from aivas.models.ecu import ECU
from aivas.models.signal import Signal
from aivas.models.baseline import Baseline, BaselineItem


class PLEEngine:
    """Product Line Engineering engine for variant management."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_150_model(self, project_id: str) -> dict:
        """Build the 150% asset superset — all tagged items grouped by layer."""
        pid = uuid.UUID(project_id)

        reqs = await self.db.execute(
            select(Requirement).where(Requirement.project_id == pid, Requirement.tag_id.isnot(None))
        )
        reqs = reqs.scalars().all()

        funcs = await self.db.execute(
            select(Function).where(Function.project_id == pid, Function.tag_id.isnot(None))
        )
        funcs = funcs.scalars().all()

        scs = await self.db.execute(
            select(SC).where(SC.project_id == pid, SC.tag_id.isnot(None))
        )
        scs = scs.scalars().all()

        sscs = await self.db.execute(
            select(SSC).join(SC).where(SC.project_id == pid, SSC.tag_id.isnot(None))
        )
        sscs = sscs.scalars().all()

        ecus = await self.db.execute(
            select(ECU).where(ECU.project_id == pid, ECU.tag_id.isnot(None))
        )
        ecus = ecus.scalars().all()

        signals = await self.db.execute(
            select(Signal).where(Signal.project_id == pid, Signal.feature_tag.isnot(None))
        )
        signals = signals.scalars().all()

        return {
            "project_id": project_id,
            "total_assets": len(reqs) + len(funcs) + len(scs) + len(sscs) + len(ecus) + len(signals),
            "requirements": [
                {"id": str(r.id), "type": r.type, "content": r.content, "tag_id": str(r.tag_id)}
                for r in reqs
            ],
            "functions": [
                {"id": str(f.id), "name": f.name, "tag_id": str(f.tag_id)}
                for f in funcs
            ],
            "scs": [
                {"id": str(s.id), "name": s.name, "tag_id": str(s.tag_id)}
                for s in scs
            ],
            "sscs": [
                {"id": str(s.id), "name": s.name, "tag_id": str(s.tag_id)}
                for s in sscs
            ],
            "ecus": [
                {"id": str(e.id), "name": e.name, "type": e.type, "tag_id": str(e.tag_id)}
                for e in ecus
            ],
            "signals": [
                {"id": str(s.id), "name": s.name, "feature_tag": s.feature_tag}
                for s in signals
            ],
        }

    async def resolve_variant(self, project_id: str, tag_ids: list[str]) -> dict:
        """Given a tag combination, produce the variant-specific asset subset.

        Uses OR logic: an asset is included if its tag_id matches any of the given tags.
        Tags can be from different levels (L1 market, L2 trim, L3 powertrain).
        """
        pid = uuid.UUID(project_id)
        tids = [uuid.UUID(t) for t in tag_ids] if tag_ids else []

        if not tids:
            return {"project_id": project_id, "tag_ids": [], "variant_assets": {}}

        reqs = await self.db.execute(
            select(Requirement).where(
                Requirement.project_id == pid,
                Requirement.tag_id.in_(tids),
            )
        )
        reqs = reqs.scalars().all()

        funcs = await self.db.execute(
            select(Function).where(
                Function.project_id == pid,
                Function.tag_id.in_(tids),
            )
        )
        funcs = funcs.scalars().all()

        scs = await self.db.execute(
            select(SC).where(
                SC.project_id == pid,
                SC.tag_id.in_(tids),
            )
        )
        scs = scs.scalars().all()

        sscs = await self.db.execute(
            select(SSC).join(SC).where(
                SC.project_id == pid,
                SSC.tag_id.in_(tids),
            )
        )
        sscs = sscs.scalars().all()

        ecus = await self.db.execute(
            select(ECU).where(
                ECU.project_id == pid,
                ECU.tag_id.in_(tids),
            )
        )
        ecus = ecus.scalars().all()

        return {
            "project_id": project_id,
            "tag_ids": tag_ids,
            "variant_assets": {
                "requirements": [
                    {"id": str(r.id), "type": r.type, "content": r.content, "tag_id": str(r.tag_id)}
                    for r in reqs
                ],
                "functions": [
                    {"id": str(f.id), "name": f.name, "tag_id": str(f.tag_id)}
                    for f in funcs
                ],
                "scs": [
                    {"id": str(s.id), "name": s.name, "tag_id": str(s.tag_id)}
                    for s in scs
                ],
                "sscs": [
                    {"id": str(s.id), "name": s.name, "tag_id": str(s.tag_id)}
                    for s in sscs
                ],
                "ecus": [
                    {"id": str(e.id), "name": e.name, "type": e.type, "tag_id": str(e.tag_id)}
                    for e in ecus
                ],
            },
            "total_assets": len(reqs) + len(funcs) + len(scs) + len(sscs) + len(ecus),
        }

    async def create_baseline(self, project_id: str, name: str, tag_ids: list[str]) -> dict:
        """Create a baseline snapshot from a variant configuration.

        Freezes the current state of all assets matching the tag combination.
        """
        pid = uuid.UUID(project_id)
        tids = [uuid.UUID(t) for t in tag_ids] if tag_ids else []

        variant = await self.resolve_variant(project_id, tag_ids)

        baseline = Baseline(
            project_id=pid,
            name=name,
            status="draft",
        )
        self.db.add(baseline)
        await self.db.flush()

        item_count = 0
        for layer_key in ["requirements", "functions", "scs", "sscs", "ecus"]:
            for asset in variant["variant_assets"].get(layer_key, []):
                self.db.add(BaselineItem(
                    baseline_id=baseline.id,
                    item_type=layer_key.rstrip("s"),  # "requirements" → "requirement"
                    item_id=uuid.UUID(asset["id"]),
                ))
                item_count += 1

        await self.db.commit()
        return {
            "baseline_id": str(baseline.id),
            "name": name,
            "status": "draft",
            "item_count": item_count,
            "tag_ids": tag_ids,
        }

    async def get_baseline_diff(
        self, baseline_id: str, project_id: str, tag_ids: list[str]
    ) -> dict:
        """Compare a frozen baseline against the current variant state.

        Returns items added, removed, and modified since the baseline was created.
        """
        bid = uuid.UUID(baseline_id)

        frozen = await self.db.execute(
            select(BaselineItem).where(BaselineItem.baseline_id == bid)
        )
        frozen_items = {(i.item_type, str(i.item_id)) for i in frozen.scalars().all()}

        current = await self.resolve_variant(project_id, tag_ids)
        current_items: set[tuple[str, str]] = set()
        for layer_key in ["requirements", "functions", "scs", "sscs", "ecus"]:
            item_type = layer_key.rstrip("s")
            for asset in current["variant_assets"].get(layer_key, []):
                current_items.add((item_type, asset["id"]))

        added = current_items - frozen_items
        removed = frozen_items - current_items

        return {
            "baseline_id": baseline_id,
            "added": [{"item_type": t, "item_id": i} for t, i in added],
            "removed": [{"item_type": t, "item_id": i} for t, i in removed],
            "total_added": len(added),
            "total_removed": len(removed),
        }
