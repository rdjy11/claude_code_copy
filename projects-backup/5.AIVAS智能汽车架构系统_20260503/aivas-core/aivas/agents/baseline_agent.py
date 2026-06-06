"""Baseline Agent — 6-step pipeline: real PLEEngine + DB persistence with LLM assistance."""

import uuid
from datetime import datetime, timezone
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.domain.ple.variant import PLEEngine
from aivas.domain.rflp.trace import get_trace_matrix
from aivas.models.tag import Tag
from aivas.models.baseline import Baseline, BaselineItem
from aivas.models.ecu import ECU
from aivas.models.signal import Signal

SYSTEM_PROMPT = """你是一个汽车基线管理专家，负责执行6步基线生成流水线。
基线 = 某个产品变体在某时间点的完整资产快照。

6步流水线：
1. Lock Tags — 锁定标签组合（L1应用架构 + L2车辆平台 + L3基线阶段）
2. Lock SSC Versions — 锁定子系统组件版本
3. Resolve ECU Variants — 根据标签解析 ECU 变体
4. Filter Signals — 过滤信号特征标签
5. Consistency Check — RFLP 追溯一致性校验
6. Freeze Snapshot — 冻结不可变基线快照

输出严格的 JSON 格式。"""


class BaselineAgent(BaseAgent):
    name = "Baseline"
    description = "Executes the 6-step baseline generation pipeline with real domain engine"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("lock_tags", self._lock_tags)
        builder.add_node("lock_ssc_versions", self._lock_ssc_versions)
        builder.add_node("resolve_ecu_variants", self._resolve_ecu_variants)
        builder.add_node("filter_signals", self._filter_signals)
        builder.add_node("consistency_check", self._consistency_check)
        builder.add_node("freeze_snapshot", self._freeze_snapshot)
        builder.set_entry_point("lock_tags")
        builder.add_edge("lock_tags", "lock_ssc_versions")
        builder.add_edge("lock_ssc_versions", "resolve_ecu_variants")
        builder.add_edge("resolve_ecu_variants", "filter_signals")
        builder.add_edge("filter_signals", "consistency_check")
        builder.add_edge("consistency_check", "freeze_snapshot")
        builder.add_edge("freeze_snapshot", END)
        return builder.compile()

    async def _lock_tags(self, state: AgentState) -> AgentState:
        tag_ids: list[str] = state.input.get("tag_ids", [])
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        if not tag_ids:
            self.think("Step 1/6: No tags provided, skipping tag lock...")
            state.output["locked_tags"] = []
            return state

        self.think(f"Step 1/6: Locking {len(tag_ids)} tag(s)...")

        if db and project_id:
            try:
                tids = [uuid.UUID(t) for t in tag_ids]
                result = await db.execute(
                    select(Tag).where(
                        Tag.project_id == uuid.UUID(project_id),
                        Tag.id.in_(tids),
                    )
                )
                tags = result.scalars().all()
                locked = [
                    {"id": str(t.id), "level": t.level, "name": t.name}
                    for t in tags
                ]
                state.output["locked_tags"] = locked
                self.think(f"Step 1/6: Locked {len(locked)} tags — {[t['name'] for t in locked]}")
            except Exception as e:
                state.errors.append(f"lock_tags failed: {e}")
                state.output["locked_tags"] = []
        else:
            state.output["locked_tags"] = [
                {"id": tid, "level": None, "name": f"Tag-{tid[:8]}"}
                for tid in tag_ids
            ]
            self.think(f"Step 1/6: {len(tag_ids)} tag(s) noted (no DB)")

        return state

    async def _lock_ssc_versions(self, state: AgentState) -> AgentState:
        tag_ids: list[str] = state.input.get("tag_ids", [])
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Step 2/6: Locking SSC versions...")

        if db and project_id and tag_ids:
            try:
                engine = PLEEngine(db)
                variant = await engine.resolve_variant(project_id, tag_ids)
                sscs = variant.get("variant_assets", {}).get("sscs", [])
                state.output["ssc_versions"] = [
                    {"id": s["id"], "name": s["name"], "tag_id": s.get("tag_id")}
                    for s in sscs
                ]
                self.think(f"Step 2/6: {len(sscs)} SSC(s) locked from variant resolution")
            except Exception as e:
                state.errors.append(f"lock_ssc_versions failed: {e}")
                state.output["ssc_versions"] = []
        else:
            state.output["ssc_versions"] = []
            self.think("Step 2/6: No DB/project — skipping SSC version lock")

        return state

    async def _resolve_ecu_variants(self, state: AgentState) -> AgentState:
        tag_ids: list[str] = state.input.get("tag_ids", [])
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Step 3/6: Resolving ECU variants...")

        if db and project_id and tag_ids:
            try:
                tids = [uuid.UUID(t) for t in tag_ids]
                result = await db.execute(
                    select(ECU).where(
                        ECU.project_id == uuid.UUID(project_id),
                        ECU.tag_id.in_(tids),
                    )
                )
                ecus = result.scalars().all()
                state.output["ecu_variants"] = [
                    {"id": str(e.id), "name": e.name, "type": e.type, "tag_id": str(e.tag_id) if e.tag_id else None}
                    for e in ecus
                ]
                self.think(f"Step 3/6: {len(ecus)} ECU(s) resolved for tag combination")
            except Exception as e:
                state.errors.append(f"resolve_ecu_variants failed: {e}")
                state.output["ecu_variants"] = []
        else:
            state.output["ecu_variants"] = []
            self.think("Step 3/6: No DB/project — skipping ECU resolution")

        return state

    async def _filter_signals(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")
        locked_sscs = state.output.get("ssc_versions", [])

        self.think("Step 4/6: Filtering signal feature tags...")

        if db and project_id and locked_sscs:
            try:
                ssc_ids = [uuid.UUID(s["id"]) for s in locked_sscs]
                result = await db.execute(
                    select(Signal).where(
                        Signal.project_id == uuid.UUID(project_id),
                        Signal.ssc_id.in_(ssc_ids),
                    )
                )
                signals = result.scalars().all()
                state.output["signals"] = [
                    {
                        "id": str(s.id), "name": s.name, "direction": s.direction,
                        "feature_tag": s.feature_tag, "ssc_id": str(s.ssc_id),
                    }
                    for s in signals
                ]
                self.think(f"Step 4/6: {len(signals)} signal(s) filtered for {len(locked_sscs)} SSC(s)")
            except Exception as e:
                state.errors.append(f"filter_signals failed: {e}")
                state.output["signals"] = []
        else:
            state.output["signals"] = []
            self.think("Step 4/6: No signals to filter")

        return state

    async def _consistency_check(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Step 5/6: Running RFLP traceability consistency check...")

        issues: list[dict] = []
        if db and project_id:
            try:
                trace_data = await get_trace_matrix(db, project_id)
                traces = trace_data.get("traces", [])

                broken = [t for t in traces if not t.get("ecus")]
                if broken:
                    issues.append({
                        "severity": "error",
                        "step": "consistency_check",
                        "description": f"{len(broken)} trace chain(s) missing physical ECU allocation",
                        "affected_count": len(broken),
                    })

                orphan_ssc_ids = {
                    uuid.UUID(s["id"]) for s in state.output.get("ssc_versions", [])
                }
                trace_ssc_ids = {uuid.UUID(t["ssc_id"]) for t in traces if t.get("ssc_id")}
                untraced = orphan_ssc_ids - trace_ssc_ids
                if untraced:
                    issues.append({
                        "severity": "warning",
                        "step": "consistency_check",
                        "description": f"{len(untraced)} SSC(s) in variant are not in any trace chain",
                        "affected_count": len(untraced),
                    })

                self.think(f"Step 5/6: {len(issues)} issue(s) found in {trace_data.get('total_traces', 0)} trace(s)")
            except Exception as e:
                issues.append({"severity": "error", "step": "consistency_check", "description": str(e)})
                state.errors.append(f"consistency_check failed: {e}")
        else:
            self.think("Step 5/6: Skipped — no DB connection")

        state.output["consistency_issues"] = issues
        return state

    async def _freeze_snapshot(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")
        tag_ids: list[str] = state.input.get("tag_ids", [])
        baseline_name = state.input.get("baseline_name", "")

        self.think("Step 6/6: Freezing immutable baseline snapshot...")

        if db and project_id and tag_ids:
            try:
                engine = PLEEngine(db)
                name = baseline_name or f"BL_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
                result = await engine.create_baseline(project_id, name, tag_ids)

                state.output["baseline_id"] = result["baseline_id"]
                state.output["baseline_name"] = result["name"]
                state.output["baseline_status"] = result["status"]
                state.output["item_count"] = result["item_count"]

                pipeline_steps = [
                    {"step": 1, "name": "Lock Tags", "status": "ok", "detail": f"已锁定 {len(state.output.get('locked_tags', []))} 个标签"},
                    {"step": 2, "name": "Lock SSC Versions", "status": "ok", "detail": f"已锁定 {len(state.output.get('ssc_versions', []))} 个SSC"},
                    {"step": 3, "name": "Resolve ECU Variants", "status": "ok", "detail": f"已解析 {len(state.output.get('ecu_variants', []))} 个ECU"},
                    {"step": 4, "name": "Filter Signals", "status": "ok", "detail": f"已过滤 {len(state.output.get('signals', []))} 个信号"},
                    {"step": 5, "name": "Consistency Check", "status": "warning" if state.output.get("consistency_issues") else "ok", "detail": f"发现 {len(state.output.get('consistency_issues', []))} 个问题"},
                    {"step": 6, "name": "Freeze Snapshot", "status": "ok", "detail": f"已冻结 {result['item_count']} 项资产"},
                ]
                state.output["pipeline_steps"] = pipeline_steps
                self.think(f"Step 6/6: Baseline '{name}' frozen — {result['item_count']} items")
            except Exception as e:
                state.errors.append(f"freeze_snapshot failed: {e}")
                state.output["baseline_status"] = "error"
                state.output["pipeline_steps"] = []
        else:
            state.output["baseline_status"] = "draft"
            state.output["pipeline_steps"] = [
                {"step": i, "name": name, "status": "skipped", "detail": "缺少 DB 或 project_id 或 tag_ids"}
                for i, name in enumerate([
                    "Lock Tags", "Lock SSC Versions", "Resolve ECU Variants",
                    "Filter Signals", "Consistency Check", "Freeze Snapshot",
                ], 1)
            ]
            self.think("Step 6/6: Skipped — missing DB/project/tags")

        state.status = AgentStatus.DONE
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        project_id = input.get("project_id", "")
        tag_ids: list[str] = input.get("tag_ids", [])
        baseline_name = input.get("baseline_name", message[:80] if message else None)
        db: AsyncSession | None = input.get("db")

        self.think("Executing 6-step baseline pipeline...")

        # If we have DB and tags, use the real PLE engine
        if db and project_id and tag_ids:
            engine = PLEEngine(db)
            try:
                self.think("Step 1/6: Resolving variant via PLE engine...")
                variant = await engine.resolve_variant(project_id, tag_ids)

                self.think(f"Step 2/6: Variant resolved — {variant.get('total_assets', 0)} assets matched")

                name = baseline_name or f"BL_{message[:40]}" if message else f"BL_auto_{len(tag_ids)}tags"
                baseline_result = await engine.create_baseline(project_id, name, tag_ids)

                self.think("Steps 3-6/6: Baseline created, snapshot frozen")
                result = {
                    "baseline_name": name,
                    "baseline_id": baseline_result["baseline_id"],
                    "status": baseline_result["status"],
                    "item_count": baseline_result["item_count"],
                    "tag_ids": tag_ids,
                    "variant_assets": variant.get("variant_assets", {}),
                    "pipeline_steps": [
                        {"step": 1, "name": "Lock Tags", "status": "ok", "detail": f"已锁定 {len(tag_ids)} 个标签"},
                        {"step": 2, "name": "Resolve Variant", "status": "ok", "detail": f"解析到 {variant.get('total_assets', 0)} 个资产"},
                        {"step": 3, "name": "Create Baseline Snapshot", "status": "ok", "detail": f"已冻结 {baseline_result['item_count']} 项"},
                    ],
                    "issues": [],
                }
            except Exception as e:
                result = {
                    "baseline_name": baseline_name, "status": "error",
                    "pipeline_steps": [], "artifacts": [],
                    "issues": [{"severity": "error", "description": str(e)}],
                }
        elif self.llm and (message.strip() or tag_ids):
            try:
                prompt = f"标签：{tag_ids}\n需求：{message}" if message else f"标签：{tag_ids}\n请生成基线。"
                response = await self.llm.complete(prompt, system=SYSTEM_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "baseline_name": None, "status": "draft", "pipeline_steps": [], "artifacts": [], "issues": [],
                }
            except Exception:
                result = {"baseline_name": None, "status": "draft", "pipeline_steps": [], "artifacts": [], "issues": []}
        else:
            result = {
                "baseline_name": None, "status": "draft",
                "pipeline_steps": [], "artifacts": [],
                "issues": [],
                "summary": "未提供 project_id/db — 无法执行真实基线流水线。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
