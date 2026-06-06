"""PLE Variant Agent — tag combination, 150% model subsetting, variant resolution via LLM + PLEEngine."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.domain.ple.variant import PLEEngine
from aivas.models.tag import Tag
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.ecu import ECU

SYSTEM_PROMPT = """你是一个汽车产品线工程(PLE)变体管理专家，负责基于150%模型进行变体裁剪和冲突检测。
你需要：
1. 根据用户选定的标签组合（L1应用/L2平台/L3基线），从150%全量模型中筛选适用的变体资产
2. 检测标签组合中的冲突（例如：选了高配功能但选了低配ECU）
3. 建议 SSC 分支选择（高配/中配/低配）

150%模型包含所有可能配置的资产。变体裁剪 = 根据标签筛选出某个具体车型配置适用的资产子集。

输出严格的 JSON 格式：
{
  "variant_config": {"name": "高配-域集中-量产", "tag_ids": ["t1", "t2", "t3"]},
  "variant_assets": [
    {"asset_type": "function", "asset_name": "高速NOA", "matched_tags": ["L1-ADAS", "L2-域控制器"]}
  ],
  "conflicts": [
    {"description": "高速NOA需要激光雷达，但当前配置中未包含激光雷达ECU", "severity": "warning"}
  ]
}"""

COMBINE_PROMPT = """你是一个汽车产品配置专家。分析标签组合(L1/L2/L3)并生成变体配置。
L1=应用架构标签，L2=车辆平台标签，L3=基线阶段标签。

输出严格 JSON：{"config_name": "...", "config_description": "...", "level_breakdown": {"L1": [...], "L2": [...], "L3": [...]}}"""

CONFLICT_PROMPT = """你是一个PLE冲突检测专家。检查标签-资产匹配中的冲突：
1. 功能-ECU匹配冲突（高配功能需高配ECU）
2. 总线不兼容冲突
3. 安全等级不匹配

输出严格 JSON：{"conflicts": [{"severity": "warning/error", "description": "...", "suggestion": "..."}]}"""


class PLEVariantAgent(BaseAgent):
    name = "PLE/Variant"
    description = "Combines 3-level tags to resolve variants from the 150% model via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("combine_tags", self._combine_tags)
        builder.add_node("subset_150", self._subset_150)
        builder.add_node("resolve_branches", self._resolve_branches)
        builder.set_entry_point("combine_tags")
        builder.add_edge("combine_tags", "subset_150")
        builder.add_edge("subset_150", "resolve_branches")
        builder.add_edge("resolve_branches", END)
        return builder.compile()

    async def _combine_tags(self, state: AgentState) -> AgentState:
        tag_ids: list[str] = state.input.get("tag_ids", [])
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Combining 3-level tags to form variant configuration...")

        if db and tag_ids:
            try:
                tids = [uuid.UUID(t) for t in tag_ids]
                result = await db.execute(select(Tag).where(Tag.id.in_(tids)))
                tags = result.scalars().all()

                level_breakdown: dict[int, list[dict]] = {1: [], 2: [], 3: []}
                for t in tags:
                    level_breakdown.setdefault(t.level, []).append({
                        "id": str(t.id), "name": t.name, "description": t.description,
                    })

                config = {
                    "tag_ids": tag_ids,
                    "level_breakdown": level_breakdown,
                    "config_name": " / ".join(
                        ", ".join(v["name"] for v in level_breakdown[lv])
                        for lv in sorted(level_breakdown)
                        if level_breakdown[lv]
                    ) or "未命名配置",
                }
                self.think(f"Tag combination: {config['config_name']}")
            except Exception as e:
                config = {"tag_ids": tag_ids, "level_breakdown": {}, "config_name": "Tag解析失败"}
                state.errors.append(f"combine_tags: {e}")
        elif self.llm and tag_ids:
            try:
                response = await self.llm.complete(f"标签ID列表：{tag_ids}", system=COMBINE_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                config = json.loads(response[start:end]) if start != -1 else {"tag_ids": tag_ids, "level_breakdown": {}, "config_name": "LLM建议配置"}
            except Exception:
                config = {"tag_ids": tag_ids, "level_breakdown": {}, "config_name": str(tag_ids)}
        else:
            config = {"tag_ids": tag_ids, "level_breakdown": {}, "config_name": "无标签配置"}

        state.output["variant_config"] = config
        return state

    async def _subset_150(self, state: AgentState) -> AgentState:
        tag_ids: list[str] = state.input.get("tag_ids", [])
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Subsetting 150% model based on tag combination...")

        if db and project_id and tag_ids:
            try:
                engine = PLEEngine(db)
                variant = await engine.resolve_variant(project_id, tag_ids)
                assets = variant.get("variant_assets", {})

                # Flatten to asset list
                asset_list: list[dict] = []
                for layer_key, items in assets.items():
                    asset_type = layer_key.rstrip("s")
                    for item in items:
                        asset_list.append({
                            "asset_type": asset_type,
                            "asset_name": item.get("name") or item.get("content", "")[:80],
                            "asset_id": item.get("id"),
                            "tag_id": item.get("tag_id"),
                        })

                state.output["variant_assets"] = asset_list
                state.output["total_assets"] = variant.get("total_assets", 0)
                self.think(f"150% subset: {len(asset_list)} assets from {variant.get('total_assets', 0)} total")
            except Exception as e:
                state.errors.append(f"subset_150: {e}")
                state.output["variant_assets"] = []
        else:
            state.output["variant_assets"] = []
            self.think("150% subset skipped — no DB/project/tags")

        return state

    async def _resolve_branches(self, state: AgentState) -> AgentState:
        text = state.input.get("message", "")
        variant_assets = state.output.get("variant_assets", [])

        self.think("Resolving SSC branches and conflicts...")

        conflicts: list[dict] = []

        # Rule-based conflict detection
        if variant_assets:
            ecu_names = [a["asset_name"] for a in variant_assets if a["asset_type"] == "ecu"]
            func_names = [a["asset_name"] for a in variant_assets if a["asset_type"] == "function"]

            # Basic heuristic: NOA/ADAS functions need specific ECUs
            adas_funcs = [f for f in func_names if any(k in f.lower() for k in ("noa", "adas", "acc", "lka", "aeb"))]
            adas_ecus = [e for e in ecu_names if any(k in e.lower() for k in ("adas", "orIN", "xavier", "domain"))]
            if adas_funcs and not adas_ecus:
                conflicts.append({
                    "severity": "warning",
                    "description": f"ADAS functions ({', '.join(adas_funcs[:3])}) detected but no ADAS ECU in variant",
                    "suggestion": "添加 ADAS 域控制器 ECU 或 Orin-X 等计算平台",
                })

        # LLM-based conflict detection for complex cases
        if self.llm and variant_assets and len(variant_assets) > 3:
            try:
                response = await self.llm.complete(
                    f"变体资产：{variant_assets[:20]}\n检测冲突。",
                    system=CONFLICT_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1:
                    llm_conflicts = json.loads(response[start:end]).get("conflicts", [])
                    conflicts.extend(llm_conflicts)
            except Exception:
                pass

        state.output["conflicts"] = conflicts
        state.status = AgentStatus.DONE
        self.think(f"Branch resolution: {len(conflicts)} conflict(s) found")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        tag_ids = input.get("tag_ids", [])
        message = input.get("message", "")
        self.think("Resolving variant from 150% model...")

        if self.llm and (tag_ids or message.strip()):
            try:
                prompt = f"标签配置：{tag_ids}\n用户需求：{message}" if message else f"标签配置：{tag_ids}"
                response = await self.llm.complete(prompt, system=SYSTEM_PROMPT)
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "variant_config": {"tag_ids": tag_ids}, "variant_assets": [], "conflicts": [],
                }
            except Exception:
                result = {"variant_config": {"tag_ids": tag_ids}, "variant_assets": [], "conflicts": []}
        else:
            result = {
                "variant_config": {"tag_ids": tag_ids},
                "variant_assets": [],
                "conflicts": [],
                "summary": "Mock 模式 — 未进行 AI 变体裁剪。请通过 PLE 界面手动配置。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
