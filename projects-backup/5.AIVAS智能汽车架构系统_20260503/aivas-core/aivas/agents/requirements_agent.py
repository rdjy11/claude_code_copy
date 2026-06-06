"""Requirements Agent — NL to structured requirements with LLM + DB persistence."""

import uuid
from typing import Any

from langgraph.graph import StateGraph, END
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from aivas.agents.base import BaseAgent, AgentState, AgentStatus
from aivas.models.requirement import Requirement
from aivas.models.tag import Tag

SYSTEM_PROMPT = """你是一个汽车系统需求分析师，负责从自然语言描述中提取结构化需求条目。
你需要：
1. 识别功能需求、非功能需求、安全需求、法规需求、网络安全需求
2. 为每条需求标注类型：market(市场)/functional(服务及功能)/system(系统功能)/regulation(法规标准)/safety(安全)/security(网络安全)
3. 提取关键实体：传感器、执行器、ECU、通信总线、功能模块
4. 建议三级标签：L1应用架构 / L2车辆平台 / L3基线阶段

输出严格的 JSON 格式，不要包含其他文本：
{
  "requirements": [
    {"type": "functional", "content": "系统应提供自适应巡航控制功能", "suggested_tags": ["L1-ADAS", "L2-域控制器", "L3-量产基线"]}
  ],
  "extracted_entities": ["ACC", "Radar", "ADAS Controller"],
  "summary": "从输入中提取了 N 条需求"
}"""

NER_SYSTEM_PROMPT = """你是一个汽车领域NER（命名实体识别）专家。从输入文本中提取所有汽车电子电气架构相关的实体。
实体类型：SENSOR（传感器）、ACTUATOR（执行器）、ECU（电子控制单元）、BUS（通信总线）、FUNCTION（功能模块）、PROTOCOL（通信协议）、STANDARD（标准法规）

输出严格的 JSON 格式：
{
  "entities": [
    {"name": "毫米波雷达", "type": "SENSOR", "confidence": 0.95},
    {"name": "CAN-FD", "type": "BUS", "confidence": 0.90}
  ]
}"""

TAG_SUGGESTION_PROMPT = """你是一个汽车产品线标签专家。为每条需求建议三级标签(L1/L2/L3)。

L1 应用架构标签示例：ADAS、智能座舱、车身域、底盘域、动力域、网联服务
L2 车辆平台标签示例：域控制器、集中式计算、分布式ECU、区域网关
L3 基线阶段标签示例：概念基线、开发基线、量产基线、售后基线

输出严格的 JSON 格式：
{
  "suggestions": [
    {"requirement_index": 0, "tags": [{"level": 1, "name": "ADAS"}, {"level": 2, "name": "域控制器"}, {"level": 3, "name": "量产基线"}]}
  ]
}"""


class RequirementsAgent(BaseAgent):
    name = "Requirements"
    description = "Extracts structured requirements from natural language documents using LLM"

    def _build_graph(self) -> StateGraph:
        builder = StateGraph(AgentState)
        builder.add_node("parse_nl", self._parse_nl)
        builder.add_node("extract_entities", self._extract_entities)
        builder.add_node("to_structured_req", self._to_structured_req)
        builder.add_node("assign_tags", self._assign_tags)
        builder.set_entry_point("parse_nl")
        builder.add_edge("parse_nl", "extract_entities")
        builder.add_edge("extract_entities", "to_structured_req")
        builder.add_edge("to_structured_req", "assign_tags")
        builder.add_edge("assign_tags", END)
        return builder.compile()

    async def _parse_nl(self, state: AgentState) -> AgentState:
        nl_text = state.input.get("message", "") or state.input.get("text", "")
        self.think(f"Parsing NL input ({len(nl_text)} chars)...")

        if not nl_text.strip():
            state.output["parsed"] = {"requirements": [], "summary": "空输入"}
            return state

        if self.llm:
            try:
                response = await self.llm.complete(
                    f"从以下文本中提取需求：\n\n{nl_text}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    parsed = json.loads(response[start:end])
                else:
                    parsed = {"requirements": [], "extracted_entities": [], "summary": response[:200]}
            except Exception:
                parsed = {"requirements": [], "extracted_entities": [], "summary": "LLM 解析失败"}
        else:
            # Fallback: basic sentence splitting
            sentences = [s.strip() for s in nl_text.replace("\n", ".").split(".") if s.strip()]
            parsed = {
                "requirements": [
                    {"type": "functional", "content": s, "suggested_tags": []}
                    for s in sentences[:20]
                ],
                "extracted_entities": [],
                "summary": f"基础分句提取了 {len(sentences[:20])} 条候选需求 (无 LLM)",
            }

        state.output["parsed"] = parsed
        self.think(f"Parsed: {len(parsed.get('requirements', []))} requirements extracted")
        return state

    async def _extract_entities(self, state: AgentState) -> AgentState:
        nl_text = state.input.get("message", "") or state.input.get("text", "")
        parsed = state.output.get("parsed", {})

        self.think("Extracting named entities...")

        # Use LLM-extracted entities if available
        if parsed.get("extracted_entities"):
            state.output["entities"] = [
                {"name": e, "type": "UNKNOWN", "confidence": 0.8}
                for e in parsed["extracted_entities"]
            ]
            self.think(f"Entities: {len(state.output['entities'])} from LLM extraction")
            return state

        # Run dedicated NER pass if LLM available
        if self.llm and nl_text.strip():
            try:
                response = await self.llm.complete(
                    f"提取以下文本中的汽车EEA实体：\n\n{nl_text[:3000]}",
                    system=NER_SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    ner_result = json.loads(response[start:end])
                    state.output["entities"] = ner_result.get("entities", [])
                else:
                    state.output["entities"] = []
            except Exception:
                state.output["entities"] = []
        else:
            state.output["entities"] = []

        self.think(f"Entities: {len(state.output.get('entities', []))} extracted")
        return state

    async def _to_structured_req(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")
        parsed = state.output.get("parsed", {})
        req_data = parsed.get("requirements", [])

        self.think(f"Structuring {len(req_data)} requirement(s)...")

        structured: list[dict] = []
        persisted_ids: list[str] = []

        for i, rd in enumerate(req_data):
            req_type = rd.get("type", "functional")
            if req_type not in ("market", "functional", "system", "regulation", "safety", "security"):
                req_type = "functional"

            req_entry = {
                "index": i,
                "type": req_type,
                "content": rd.get("content", ""),
                "suggested_tags": rd.get("suggested_tags", []),
            }
            structured.append(req_entry)

            # Persist to DB if available
            if db and project_id and rd.get("content"):
                try:
                    req = Requirement(
                        project_id=uuid.UUID(project_id),
                        type=req_type,
                        content=rd["content"],
                    )
                    db.add(req)
                    await db.flush()
                    req_entry["persisted_id"] = str(req.id)
                    persisted_ids.append(str(req.id))
                except Exception as e:
                    req_entry["persist_error"] = str(e)

        if persisted_ids:
            try:
                await db.commit()
            except Exception as e:
                state.errors.append(f"commit failed: {e}")

        state.output["structured_requirements"] = structured
        state.output["persisted_count"] = len(persisted_ids)
        self.think(f"Structured: {len(structured)} reqs, {len(persisted_ids)} persisted")
        return state

    async def _assign_tags(self, state: AgentState) -> AgentState:
        db: AsyncSession | None = state.input.get("db")
        project_id = state.input.get("project_id", "")
        structured = state.output.get("structured_requirements", [])

        self.think(f"Assigning 3-level tags to {len(structured)} requirement(s)...")

        if not structured:
            state.status = AgentStatus.DONE
            return state

        tag_assignments: list[dict] = []

        # Try LLM-based tag suggestion
        if self.llm:
            try:
                req_texts = [
                    {"index": r["index"], "type": r["type"], "content": r["content"][:200]}
                    for r in structured
                ]
                response = await self.llm.complete(
                    f"为以下需求建议标签：\n{req_texts}",
                    system=TAG_SUGGESTION_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    suggestions = json.loads(response[start:end]).get("suggestions", [])
                else:
                    suggestions = []
            except Exception:
                suggestions = []
        else:
            suggestions = []

        # Apply suggestions and resolve against DB tags
        for req in structured:
            assignment = {"requirement_index": req["index"], "assigned_tags": []}

            # Find LLM suggestion for this req
            suggestion = next(
                (s for s in suggestions if s.get("requirement_index") == req["index"]),
                None,
            )

            if suggestion and db and project_id:
                for tag_info in suggestion.get("tags", []):
                    try:
                        result = await db.execute(
                            select(Tag).where(
                                Tag.project_id == uuid.UUID(project_id),
                                Tag.level == tag_info["level"],
                                Tag.name == tag_info["name"],
                            )
                        )
                        existing_tag = result.scalars().first()
                        if existing_tag:
                            assignment["assigned_tags"].append({
                                "level": existing_tag.level,
                                "name": existing_tag.name,
                                "id": str(existing_tag.id),
                            })
                            # Update the persisted requirement with tag
                            persisted_id = req.get("persisted_id")
                            if persisted_id:
                                await db.execute(
                                    Requirement.__table__.update()
                                    .where(Requirement.id == uuid.UUID(persisted_id))
                                    .values(tag_id=existing_tag.id)
                                )
                    except Exception:
                        continue

            tag_assignments.append(assignment)

        if db and project_id:
            try:
                await db.commit()
            except Exception:
                pass

        state.output["tag_assignments"] = tag_assignments
        state.output["tagged_count"] = sum(
            1 for a in tag_assignments if a["assigned_tags"]
        )
        state.status = AgentStatus.DONE
        self.think(f"Tags assigned: {state.output['tagged_count']} requirements tagged")
        return state

    async def execute(self, input: dict[str, Any]) -> dict[str, Any]:
        self.state.input = input
        self.state.status = AgentStatus.EXECUTING

        nl_text = input.get("message", "") or input.get("text", "")
        project_id = input.get("project_id", "")
        db: AsyncSession | None = input.get("db")

        self.think("Analyzing input text for requirements extraction...")

        # Step 1: Extract via LLM (or fallback)
        if self.llm and nl_text.strip():
            try:
                response = await self.llm.complete(
                    f"从以下文本中提取需求：\n\n{nl_text}",
                    system=SYSTEM_PROMPT,
                )
                import json
                start = response.find("{")
                end = response.rfind("}") + 1
                if start != -1 and end > start:
                    result = json.loads(response[start:end])
                else:
                    result = {"requirements": [], "extracted_entities": [], "summary": response[:200]}
            except Exception:
                result = {"requirements": [], "extracted_entities": [], "summary": "LLM 解析失败，请重试"}
        else:
            result = {
                "requirements": [],
                "extracted_entities": [],
                "summary": f"已接收输入文本 ({len(nl_text)} chars). 未进行 AI 提取。",
            }

        # Step 2: Persist extracted requirements to DB if project_id and db are available
        persisted: list[str] = []
        if db and project_id:
            self.think("Persisting extracted requirements to database...")
            for req_data in result.get("requirements", []):
                try:
                    req = Requirement(
                        project_id=uuid.UUID(project_id),
                        type=req_data.get("type", "functional"),
                        content=req_data.get("content", ""),
                    )
                    db.add(req)
                    await db.commit()
                    await db.refresh(req)
                    persisted.append(str(req.id))
                except Exception as e:
                    persisted.append(f"error: {e}")
            result["persisted_ids"] = persisted

        self.state.output = result
        self.state.status = AgentStatus.DONE
        return result
