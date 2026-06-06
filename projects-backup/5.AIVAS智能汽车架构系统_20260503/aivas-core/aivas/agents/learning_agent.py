"""Learning Agent — learns from historical baselines to recommend optimal configurations via LLM + DB."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.models.baseline import Baseline, BaselineItem
from aivas.models.tag import Tag
from aivas.models.ecu import ECU

SYSTEM_PROMPT = """你是一个汽车架构配置推荐专家，从历史基线数据中学习模式并推荐最优配置。
你需要：
1. 分析历史基线中的标签组合和ECU选择模式
2. 为当前项目推荐最优的标签/ECU配置
3. 给出置信度评分和推荐理由

输出严格的 JSON 格式：
{
  "recommendations": [
    {"type": "tag", "recommendation": "建议使用 L1-ADAS + L2-域控制器", "confidence": 0.92, "reason": "80% 的高配项目使用此组合"},
    {"type": "ecu", "recommendation": "ADAS推荐使用Orin-X平台", "confidence": 0.85, "reason": "算力需求匹配"}
  ],
  "patterns": [
    {"pattern": "L1-ADAS 高配 → 域控制器 + 激光雷达", "frequency": "15/20 基线", "trend": "增长"}
  ],
  "confidence_scores": {"overall": 0.88}
}"""

EXTRACT_PATTERNS_PROMPT = """你是一个数据模式识别专家。从历史基线数据中提取配置模式。
输出严格 JSON：{"patterns": [{"pattern": "...", "frequency": "...", "confidence": 0.XX}]}"""

RANK_PROMPT = """你是一个配置推荐排序专家。根据上下文对推荐项进行排序打分。
输出严格 JSON：{"ranked": [{"recommendation": "...", "confidence": 0.XX, "rank": 1, "reason": "..."}]}"""


class LearningAgent(BaseAgent):
    name = "Learning"
    description = "Learns patterns from historical baselines and recommends optimal configurations via LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("extract_patterns", self._extract_patterns)
        builder.add_node("rank_recommendations", self._rank_recommendations)
        builder.add_node("generate_suggestions", self._generate_suggestions)
        builder.set_entry_point("extract_patterns")
        builder.add_edge("extract_patterns", "rank_recommendations")
        builder.add_edge("rank_recommendations", "generate_suggestions")
        builder.add_edge("generate_suggestions", END)
        return builder.compile()

    async def _extract_patterns(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")

        self.think("Extracting patterns from historical baselines...")

        patterns: list[dict] = []

        if db and project_id:
            try:
                pid = uuid.UUID(project_id)

                # Count baselines and their statuses
                baseline_result = await db.execute(
                    select(Baseline).where(Baseline.project_id == pid)
                )
                baselines = baseline_result.scalars().all()

                if baselines:
                    status_counts: dict[str, int] = {}
                    for b in baselines:
                        status_counts[b.status] = status_counts.get(b.status, 0) + 1

                    patterns.append({
                        "pattern": f"Baseline status distribution: {status_counts}",
                        "frequency": f"{len(baselines)} total baselines",
                        "confidence": 1.0,
                        "source": "db",
                    })

                    # Most common tag combinations
                    tag_freq: dict[str, int] = {}
                    for b in baselines:
                        if b.tag_id:
                            tag_freq[str(b.tag_id)] = tag_freq.get(str(b.tag_id), 0) + 1

                    if tag_freq:
                        most_common_tag = max(tag_freq, key=tag_freq.get)
                        patterns.append({
                            "pattern": f"Most used tag: {most_common_tag}",
                            "frequency": f"{tag_freq[most_common_tag]}/{len(baselines)} baselines",
                            "confidence": tag_freq[most_common_tag] / len(baselines),
                            "source": "db",
                        })

                    # Average items per baseline
                    total_items = 0
                    for b in baselines:
                        item_result = await db.execute(
                            select(func.count(BaselineItem.id)).where(
                                BaselineItem.baseline_id == b.id
                            )
                        )
                        total_items += item_result.scalar() or 0
                    avg_items = total_items / len(baselines) if baselines else 0
                    patterns.append({
                        "pattern": f"Average {avg_items:.1f} items per baseline",
                        "frequency": f"Across {len(baselines)} baselines",
                        "confidence": 0.7,
                        "source": "db",
                    })

                    self.think(f"Extracted {len(patterns)} pattern(s) from {len(baselines)} baselines")
                else:
                    self.think("No historical baselines found")
            except Exception as e:
                state.errors.append(f"extract_patterns: {e}")
        else:
            self.think("No DB — skipping pattern extraction")

        state.output["patterns"] = patterns
        return state

    async def _rank_recommendations(self, state: AgentState) -> AgentState:
        patterns = state.output.get("patterns", [])
        message = state.input.get("message", "")

        self.think("Ranking configuration recommendations...")

        recommendations: list[dict] = []

        # Generate rule-based recommendations from patterns
        for p in patterns:
            if "tag" in p.get("pattern", "").lower() or "Most used tag" in p.get("pattern", ""):
                recommendations.append({
                    "type": "tag",
                    "recommendation": p["pattern"],
                    "confidence": p.get("confidence", 0.5),
                    "reason": f"Based on {p.get('frequency', 'historical data')}",
                })

        # LLM-based ranking if available
        if self.llm and recommendations:
            try:
                response = await self.llm.complete(
                    f"推荐列表：{recommendations}\n上下文：{message}",
                    system=RANK_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1:
                    ranked = json.loads(response[start:end]).get("ranked", [])
                    recommendations = ranked
            except Exception:
                pass

        # Sort by confidence
        recommendations.sort(key=lambda r: r.get("confidence", 0), reverse=True)
        state.output["recommendations"] = recommendations
        self.think(f"Ranked: {len(recommendations)} recommendation(s)")
        return state

    async def _generate_suggestions(self, state: AgentState) -> AgentState:
        recommendations = state.output.get("recommendations", [])
        patterns = state.output.get("patterns", [])

        self.think("Generating human-readable suggestions...")

        suggestions: list[str] = []

        # Top-3 actionable suggestions
        for rec in recommendations[:3]:
            rec_text = rec.get("recommendation", "")
            conf = rec.get("confidence", 0)
            reason = rec.get("reason", "")
            if conf > 0.5:
                suggestions.append(f"[高置信度 {conf:.0%}] {rec_text} — {reason}")
            elif rec_text:
                suggestions.append(f"[中置信度] {rec_text}")

        if not suggestions and patterns:
            suggestions.append(f"检测到 {len(patterns)} 个历史模式，建议积累更多基线数据以获得置信推荐。")

        if not suggestions:
            suggestions.append("暂无足够数据进行智能推荐。创建更多基线后，系统将自动学习配置模式。")

        state.output["suggestions"] = suggestions
        state.output["confidence_scores"] = {
            "overall": round(
                sum(r.get("confidence", 0) for r in recommendations) / max(len(recommendations), 1), 2
            ),
            "data_points": len(patterns),
        }
        state.status = AgentStatus.DONE
        self.think(f"Suggestions: {len(suggestions)} generated")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        message = input.get("message", "")
        self.think("Analyzing historical patterns for recommendations...")

        if self.llm and message.strip():
            try:
                response = await self.llm.complete(
                    f"基于以下上下文推荐配置：\n{message}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                result = json.loads(response[start:end]) if start != -1 and end > start else {
                    "recommendations": [], "patterns": [], "confidence_scores": {},
                }
            except Exception:
                result = {"recommendations": [], "patterns": [], "confidence_scores": {}}
        else:
            result = {
                "recommendations": [], "patterns": [],
                "confidence_scores": {},
                "summary": "Mock 模式 — 未执行 AI 模式学习。历史基线数据积累后自动启用。",
            }

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
