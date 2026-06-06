"""Verification Agent — real RFLP traceability check + PLE conflict detection."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
from aivas.models.signal import Signal, SignalECUAllocation
from aivas.models.ecu import ECU
from aivas.models.tag import Tag
from aivas.models.requirement import Requirement

SYSTEM_PROMPT = """你是一个汽车电子电气架构验证专家，负责 RFLP 追溯链一致性和 PLE 变体冲突检测。
你需要检查：
1. RFLP 追溯完整性 — 每个需求是否都有对应的功能→逻辑→物理实现？每层是否存在孤儿节点？
2. PLE 变体一致性 — 标签组合中是否存在功能与硬件不匹配的冲突？
3. 信号分配正确性 — 每个信号的发送方和接收方是否在同一总线上？

输出严格的 JSON 格式。"""


class VerificationAgent(BaseAgent):
    name = "Verification"
    description = "Validates RFLP traceability consistency and detects PLE conflicts with real data"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("check_traceability", self._check_traceability)
        builder.add_node("check_ple_conflicts", self._check_ple_conflicts)
        builder.add_node("check_signal_allocation", self._check_signal_allocation)
        builder.add_node("generate_report", self._generate_report)
        builder.set_entry_point("check_traceability")
        builder.add_edge("check_traceability", "check_ple_conflicts")
        builder.add_edge("check_ple_conflicts", "check_signal_allocation")
        builder.add_edge("check_signal_allocation", "generate_report")
        builder.add_edge("generate_report", END)
        return builder.compile()

    async def _check_traceability(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Checking RFLP traceability (Req→Func→Logical→Physical)...")

        if not db or not project_id:
            self.think("RFLP traceability check skipped — no DB/project_id")
            state.output["trace_data"] = {}
            state.output["trace_issues"] = []
            state.output["orphans"] = []
            return state

        try:
            trace_data = await get_trace_matrix(db, project_id)
            summary_data = await get_rflp_summary(db, project_id)
            traces = trace_data.get("traces", [])

            state.output["trace_data"] = {
                "total_traces": trace_data.get("total_traces", 0),
                "layers": trace_data.get("layers", []),
                "summary": summary_data,
            }

            issues: list[dict] = []
            orphans: list[dict] = []

            # Detect broken trace chains (missing physical layer)
            broken = [t for t in traces if not t.get("ecus")]
            if broken:
                issues.append({
                    "severity": "error",
                    "category": "traceability",
                    "layer": "Physical",
                    "description": f"{len(broken)} trace chain(s) missing ECU allocation",
                    "affected": [
                        {"requirement_id": t["requirement_id"], "ssc_name": t.get("ssc_name", "?")}
                        for t in broken[:10]
                    ],
                })

            # Detect orphan functions
            if summary_data.get("orphan_functions", 0) > 0:
                orphans.append({
                    "layer": "Function",
                    "count": summary_data["orphan_functions"],
                    "description": f"{summary_data['orphan_functions']} function(s) lack upstream requirement link",
                })

            # Detect orphan SCs
            if summary_data.get("orphan_scs", 0) > 0:
                orphans.append({
                    "layer": "SC",
                    "count": summary_data["orphan_scs"],
                    "description": f"{summary_data['orphan_scs']} SC(s) lack upstream function link",
                })

            # Detect requirements with no functions mapped
            req_ids_with_funcs = {t.get("requirement_id") for t in traces if t.get("function_id")}
            if summary_data.get("requirements", 0) > len(req_ids_with_funcs):
                missing = summary_data["requirements"] - len(req_ids_with_funcs)
                orphans.append({
                    "layer": "Requirement",
                    "count": missing,
                    "description": f"{missing} requirement(s) not mapped to any function",
                })

            state.output["trace_issues"] = issues
            state.output["orphans"] = orphans
            self.think(f"Traceability: {len(traces)} chains, {len(issues)} issues, {len(orphans)} orphan categories")
        except Exception as e:
            state.errors.append(f"check_traceability failed: {e}")
            state.output["trace_issues"] = [{"severity": "error", "category": "traceability", "description": str(e)}]
            state.output["orphans"] = []

        return state

    async def _check_ple_conflicts(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")
        tag_ids: list[str] = state.input.get("tag_ids", [])

        self.think("Detecting PLE tag conflicts and variant inconsistencies...")

        conflicts: list[dict] = []
        if not db or not project_id:
            self.think("PLE conflict check skipped — no DB/project_id")
            state.output["ple_conflicts"] = conflicts
            return state

        try:
            # Check for conflicting tag levels (L1/L2/L3 combination issues)
            if tag_ids:
                tids = [uuid.UUID(t) for t in tag_ids]
                tag_result = await db.execute(select(Tag).where(Tag.id.in_(tids)))
                tags = tag_result.scalars().all()

                levels_found: dict[int, list[str]] = {}
                for t in tags:
                    levels_found.setdefault(t.level, []).append(t.name)

                if 1 in levels_found and len(levels_found[1]) > 1:
                    conflicts.append({
                        "severity": "info",
                        "category": "tag_conflict",
                        "description": f"Multiple L1 application tags selected: {levels_found[1]}",
                        "suggestion": "通常一个产品变体只有一个 L1 应用架构标签",
                    })

            # Check for ECU-function tag mismatch
            pid = uuid.UUID(project_id)
            ecu_result = await db.execute(
                select(ECU).where(ECU.project_id == pid)
            )
            ecus = ecu_result.scalars().all()

            ecus_with_tags = [e for e in ecus if e.tag_id]
            ecus_without_tags = [e for e in ecus if not e.tag_id]

            if ecus_without_tags:
                conflicts.append({
                    "severity": "warning",
                    "category": "missing_tags",
                    "description": f"{len(ecus_without_tags)} ECU(s) have no tag assignment",
                    "affected_ecus": [e.name for e in ecus_without_tags[:5]],
                    "suggestion": "为 ECU 分配 PLE 标签以确保变体正确性",
                })

            state.output["ple_conflicts"] = conflicts
            self.think(f"PLE conflicts: {len(conflicts)} issue(s) detected")
        except Exception as e:
            state.errors.append(f"check_ple_conflicts failed: {e}")
            state.output["ple_conflicts"] = [{"severity": "error", "category": "ple_conflict", "description": str(e)}]

        return state

    async def _check_signal_allocation(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Validating signal feature tag to ECU allocations...")

        signal_issues: list[dict] = []
        if not db or not project_id:
            self.think("Signal allocation check skipped — no DB/project_id")
            state.output["signal_issues"] = signal_issues
            return state

        try:
            pid = uuid.UUID(project_id)

            # Find signals without ECU allocations
            signal_result = await db.execute(
                select(Signal).where(Signal.project_id == pid)
            )
            signals = signal_result.scalars().all()

            unallocated: list[str] = []
            for sig in signals:
                alloc_result = await db.execute(
                    select(SignalECUAllocation).where(
                        SignalECUAllocation.signal_id == sig.id
                    )
                )
                allocs = alloc_result.scalars().all()
                if not allocs:
                    unallocated.append(sig.name)

            if unallocated:
                signal_issues.append({
                    "severity": "warning",
                    "category": "signal_unallocated",
                    "description": f"{len(unallocated)} signal(s) have no ECU allocation",
                    "affected_signals": unallocated[:10],
                    "suggestion": "为每个信号分配至少一个 ECU（发送方或接收方）",
                })

            # Check for bidirectional signals with single ECU allocation
            for sig in signals:
                if sig.direction == "bidirectional":
                    alloc_result = await db.execute(
                        select(SignalECUAllocation).where(
                            SignalECUAllocation.signal_id == sig.id
                        )
                    )
                    allocs = alloc_result.scalars().all()
                    if len(allocs) < 2:
                        signal_issues.append({
                            "severity": "info",
                            "category": "bidirectional_single",
                            "description": f"Bidirectional signal '{sig.name}' has only {len(allocs)} ECU allocation(s)",
                            "suggestion": "双向信号建议至少分配两个 ECU",
                        })

            state.output["signal_issues"] = signal_issues
            self.think(f"Signal allocation: {len(signals)} signals, {len(signal_issues)} issues")
        except Exception as e:
            state.errors.append(f"check_signal_allocation failed: {e}")
            state.output["signal_issues"] = [{"severity": "error", "category": "signal_allocation", "description": str(e)}]

        return state

    async def _generate_report(self, state: AgentState) -> AgentState:
        self.think("Generating verification report...")

        trace_issues = state.output.get("trace_issues", [])
        ple_conflicts = state.output.get("ple_conflicts", [])
        signal_issues = state.output.get("signal_issues", [])
        orphans = state.output.get("orphans", [])
        trace_data = state.output.get("trace_data", {})

        all_issues = trace_issues + ple_conflicts + signal_issues
        errors = [i for i in all_issues if i.get("severity") == "error"]
        warnings = [i for i in all_issues if i.get("severity") == "warning"]
        infos = [i for i in all_issues if i.get("severity") == "info"]

        suggestions: list[str] = []
        for issue_set in all_issues:
            s = issue_set.get("suggestion")
            if s and s not in suggestions:
                suggestions.append(s)

        report = {
            "passed": len(all_issues) == 0,
            "summary": {
                "total_issues": len(all_issues),
                "errors": len(errors),
                "warnings": len(warnings),
                "info": len(infos),
                "orphan_categories": len(orphans),
            },
            "trace_matrix": {
                "total_traces": trace_data.get("total_traces", 0),
                "layers": trace_data.get("layers", []),
            },
            "rflp_summary": trace_data.get("summary", {}),
            "issues": all_issues,
            "suggestions": suggestions,
            "verdict": "PASS" if len(errors) == 0 else "FAIL",
        }

        state.output["verification_report"] = report
        state.status = AgentStatus.DONE
        self.think(f"Report: {report['verdict']} — {len(errors)}E / {len(warnings)}W / {len(infos)}I")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        project_id = input.get("project_id", "")
        db: AsyncSession | None = input.get("db")
        self.think("Running verification checks...")

        # If we have DB + project_id, run real verification
        if db and project_id:
            try:
                self.think("Querying trace matrix and summary from DB...")
                trace_data = await get_trace_matrix(db, project_id)
                summary_data = await get_rflp_summary(db, project_id)

                traces = trace_data.get("traces", [])
                orphans = []

                # Compute orphans from summary
                if summary_data.get("orphan_functions", 0) > 0:
                    orphans.append({
                        "layer": "Function",
                        "count": summary_data["orphan_functions"],
                        "label": f"{summary_data['orphan_functions']} 个功能缺少上游需求链接",
                    })
                if summary_data.get("orphan_scs", 0) > 0:
                    orphans.append({
                        "layer": "SC",
                        "count": summary_data["orphan_scs"],
                        "label": f"{summary_data['orphan_scs']} 个SC缺少上游功能链接",
                    })

                # Build issues from trace analysis
                issues: list[dict] = []
                warnings: list[dict] = []

                # Detect traces with no ECUs allocated
                broken = [t for t in traces if not t.get("ecus")]
                if broken:
                    issues.append({
                        "severity": "error",
                        "category": "traceability",
                        "description": f"{len(broken)} 条追溯链缺少 ECU 分配（物理层缺失）",
                        "suggestion": "在物理层为对应 SSC 分配 ECU",
                        "affected_chains": len(broken),
                    })

                # Check for traces missing function assignment
                req_ids = {t["requirement_id"] for t in traces}
                func_ids = {t["function_id"] for t in traces if t.get("function_id")}

                if orphans:
                    warnings.append({
                        "category": "orphan",
                        "description": f"检测到 {len(orphans)} 类孤立节点",
                        "details": orphans,
                    })

                result = {
                    "trace_matrix": {
                        "total_traces": trace_data.get("total_traces", 0),
                        "requirements_covered": len(req_ids),
                        "functions_mapped": len(func_ids),
                    },
                    "issues": issues,
                    "warnings": warnings,
                    "summary": summary_data,
                    "suggestions": [
                        f"为 {len(broken)} 条缺少 ECU 的追溯链分配物理层" if broken else None,
                        f"修复 {summary_data.get('orphan_functions', 0)} 个孤立功能" if summary_data.get("orphan_functions") else None,
                        f"修复 {summary_data.get('orphan_scs', 0)} 个孤立SC" if summary_data.get("orphan_scs") else None,
                    ],
                }
                result["suggestions"] = [s for s in result["suggestions"] if s]
            except Exception as e:
                result = {"issues": [{"severity": "error", "description": str(e)}], "warnings": [], "trace_matrix": {}, "suggestions": []}
        elif self.llm and message.strip():
            try:
                response = await self.llm.complete(
                    f"请验证项目 {project_id} 的架构一致性：\n{message}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "issues": [], "warnings": [], "trace_matrix": {}, "suggestions": [],
                }
            except Exception:
                result = {"issues": [], "warnings": [], "trace_matrix": {}, "suggestions": []}
        else:
            result = {
                "issues": [], "warnings": [],
                "trace_matrix": {}, "suggestions": [],
                "summary": "未提供 project_id/db — 无法执行真实验证。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
