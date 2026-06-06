"""Prompt Template Registry — versioned, composable prompt templates for all 10 agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ─── Template definitions ───────────────────────────────────────────


@dataclass
class PromptTemplate:
    name: str
    version: str
    description: str
    system: str
    user_template: str  # {variable} placeholders
    examples: list[dict[str, str]] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)


# ─── Registry ───────────────────────────────────────────────────────

class PromptRegistry:
    """Central registry of all prompt templates with versioning and composition."""

    def __init__(self):
        self._templates: dict[str, PromptTemplate] = {}
        self._register_defaults()

    def register(self, template: PromptTemplate):
        key = f"{template.name}@{template.version}"
        self._templates[key] = template

    def get(self, name: str, version: str = "v1") -> PromptTemplate | None:
        return self._templates.get(f"{name}@{version}")

    def render(self, name: str, variables: dict[str, Any], version: str = "v1") -> str:
        tpl = self.get(name, version)
        if tpl is None:
            raise KeyError(f"Prompt template '{name}@{version}' not found")
        return tpl.user_template.format(**variables)

    def list_templates(self) -> list[dict]:
        return [
            {"name": k, "description": v.description, "version": v.version, "tags": v.tags}
            for k, v in self._templates.items()
        ]

    def _register_defaults(self):
        """Register built-in prompt templates for all AIVAS agent scenarios."""

        # ── Requirements Agent ──
        self.register(PromptTemplate(
            name="requirements.extract",
            version="v1",
            description="从自然语言中提取结构化需求",
            system="你是汽车系统需求分析师。提取结构化需求条目，标注类型和标签建议。",
            user_template="{context}\n\n从以下文本中提取需求：\n\n{text}",
            tags=["requirements", "extraction", "nlp"],
        ))
        self.register(PromptTemplate(
            name="requirements.ner",
            version="v1",
            description="从文本中提取汽车EEA命名实体",
            system="你是汽车领域NER专家。提取传感器、执行器、ECU、总线、功能模块、协议、标准等实体。",
            user_template="提取以下文本中的汽车EEA实体：\n\n{text}",
            tags=["requirements", "ner", "entities"],
        ))

        # ── Functional Agent ──
        self.register(PromptTemplate(
            name="functional.decompose",
            version="v1",
            description="从需求分解功能模块",
            system="你是功能分解专家。从需求中提取功能模块，定义名称、描述、所属域。",
            user_template="{context}\n\n需求列表：\n{requirements}\n\n请分解功能模块。",
            tags=["functional", "decomposition"],
        ))
        self.register(PromptTemplate(
            name="functional.bdd",
            version="v1",
            description="生成 BDD 模块定义图",
            system="你是SysML BDD图生成专家。根据功能列表生成@xyflow/react BDD图JSON。",
            user_template="功能列表：{functions}\n\n生成BDD图。",
            tags=["functional", "bdd", "diagram"],
        ))

        # ── Logical Agent ──
        self.register(PromptTemplate(
            name="logical.decompose_ssc",
            version="v1",
            description="将SC分解为SSC",
            system="你是系统组件分解专家。将SC分解为子系统组件SSC。",
            user_template="{context}\n\nSC: {sc_name}\n描述: {sc_description}\n\n分解SSC。",
            tags=["logical", "decomposition", "ssc"],
        ))
        self.register(PromptTemplate(
            name="logical.signals",
            version="v1",
            description="定义SSC之间的信号接口",
            system="你是汽车信号接口专家。定义SSC之间的信号：名称、类型、周期、收发方。",
            user_template="SSC列表：{sscs}\n\n定义信号接口。",
            tags=["logical", "signals", "interface"],
        ))

        # ── Physical Agent ──
        self.register(PromptTemplate(
            name="physical.ecu_mapping",
            version="v1",
            description="SSC到ECU的映射",
            system="你是ECU映射专家。根据算力、接口、安全等级将SSC映射到物理ECU。",
            user_template="{context}\n\nSSC列表：{sscs}\n\n建议ECU映射。",
            tags=["physical", "ecu", "mapping"],
        ))
        self.register(PromptTemplate(
            name="physical.topology",
            version="v1",
            description="生成车载网络拓扑图",
            system="你是车载网络拓扑专家。生成ECU之间的总线连接拓扑。",
            user_template="ECU列表：{ecus}\n\n生成网络拓扑图。",
            tags=["physical", "topology", "network"],
        ))

        # ── PLE/Variant Agent ──
        self.register(PromptTemplate(
            name="ple.variant_resolve",
            version="v1",
            description="基于标签组合裁剪150%模型",
            system="你是PLE变体管理专家。根据标签组合从150%模型中筛选变体资产并检测冲突。",
            user_template="标签：{tag_ids}\n需求：{message}\n\n解析变体配置。",
            tags=["ple", "variant", "150%", "subsetting"],
        ))
        self.register(PromptTemplate(
            name="ple.conflict_detect",
            version="v1",
            description="检测PLE变体冲突",
            system="你是PLE冲突检测专家。检查功能-ECU匹配、总线兼容性、安全等级匹配。",
            user_template="变体资产：{assets}\n\n检测冲突。",
            tags=["ple", "conflict", "validation"],
        ))

        # ── Baseline Agent ──
        self.register(PromptTemplate(
            name="baseline.generate",
            version="v1",
            description="执行6步基线生成流水线",
            system="你是基线管理专家。执行6步流水线：标签锁定→SSC版本锁定→ECU解析→信号过滤→一致性校验→快照冻结。",
            user_template="标签：{tag_ids}\n需求：{message}",
            tags=["baseline", "pipeline", "snapshot"],
        ))
        self.register(PromptTemplate(
            name="baseline.diff",
            version="v1",
            description="基线对比分析",
            system="你是基线对比分析专家。对比两个基线的差异，识别新增/删除/变更项。",
            user_template="基线A: {baseline_a}\n基线B: {baseline_b}\n\n对比分析。",
            tags=["baseline", "diff", "comparison"],
        ))

        # ── Verification Agent ──
        self.register(PromptTemplate(
            name="verification.rflp_check",
            version="v1",
            description="RFLP追溯链一致性检查",
            system="你是EEA验证专家。检查RFLP追溯链完整性、PLE变体一致性、信号分配正确性。",
            user_template="项目ID: {project_id}\n上下文: {message}",
            tags=["verification", "rflp", "traceability"],
        ))
        self.register(PromptTemplate(
            name="verification.report",
            version="v1",
            description="生成验证报告",
            system="你是验证报告生成专家。汇总所有检查结果生成结构化验证报告。",
            user_template="检查结果：\n- 追溯性: {traceability}\n- PLE冲突: {ple_conflicts}\n- 信号分配: {signal_allocation}",
            tags=["verification", "report"],
        ))

        # ── SysML Diagram Agent ──
        self.register(PromptTemplate(
            name="sysml.generate",
            version="v1",
            description="从描述生成SysML图表JSON",
            system="你是SysML建模专家。将自然语言描述转换为@xyflow/react流程图JSON。",
            user_template="图类型：{diagram_type}\n描述：{description}",
            tags=["sysml", "diagram", "bdd", "ibd", "topology"],
        ))

        # ── Learning Agent ──
        self.register(PromptTemplate(
            name="learning.patterns",
            version="v1",
            description="从历史基线提取配置模式",
            system="你是数据模式识别专家。从历史基线数据中提取标签组合和ECU选择模式。",
            user_template="基线数据：{baselines}\n上下文：{message}",
            tags=["learning", "patterns", "recommendation"],
        ))
        self.register(PromptTemplate(
            name="learning.recommend",
            version="v1",
            description="推荐最优配置",
            system="你是配置推荐专家。基于历史模式为当前项目推荐最优标签/ECU配置并给出置信度。",
            user_template="模式：{patterns}\n项目上下文：{message}",
            tags=["learning", "recommendation", "ranking"],
        ))

        # ── Conversational Agent ──
        self.register(PromptTemplate(
            name="conversational.navigate",
            version="v1",
            description="AIVAS对话助手",
            system="你是AIVAS智能助手。用中文引导用户使用各项功能。",
            user_template="{question}",
            tags=["conversational", "help", "navigation"],
        ))
        self.register(PromptTemplate(
            name="conversational.nl2query",
            version="v1",
            description="自然语言转查询意图",
            system="你是自然语言转查询专家。分析用户问题，识别查询意图类型。",
            user_template="分析以下问题的查询意图：\n{question}",
            tags=["conversational", "nlp", "intent"],
        ))


# ─── Singleton ──────────────────────────────────────────────────────

_prompt_registry: PromptRegistry | None = None


def get_prompt_registry() -> PromptRegistry:
    global _prompt_registry
    if _prompt_registry is None:
        _prompt_registry = PromptRegistry()
    return _prompt_registry
