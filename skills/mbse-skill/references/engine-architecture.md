# 建模引擎设计参考

> 本文件为 mbse-modeler 的参考资料，包含 KerML 元模型、SysML v2 API、Graphical BNF 和 MagicGrid Solution Domain 详细流程。Agent 执行建模任务时按需查阅，不必全量加载。

---

## KerML元模型架构（引擎内核基础）

KerML是SysML v2的语义底座，分三层：

| 层 | 核心概念 | 引擎用途 |
|----|---------|---------|
| Root | Element, Relationship, Namespace, Membership, Import | 模型存储的基本数据结构 |
| Core | Type, Classifier, Feature, Specialization, Subsetting, Redefinition, FeatureTyping | 类型系统与特性推导引擎 |
| Kernel | DataType, Class, Structure, Association, Connector, Behavior, Function, Expression, Interaction | 领域语义计算 |

**关键设计原则：**
- 所有非Relationship的Element之间只能通过Relationship关联（图结构，Relationship是边）
- Element有唯一elementId（不可变）+ 可选name/shortName（可变）
- 所有权树：删除Element级联删除其ownedRelationships和ownedElements
- 三种约束：Derivation（派生属性）、Semantic（语义隐含关系）、Validation（合法性校验）

**元模型类层次：**
```
Element
├── Namespace ← Package, LibraryPackage
├── Type ← Classifier ← Class, DataType, Structure, Association, Behavior, Function
├── Feature ← Step, Expression, Connector, Multiplicity
└── Relationship ← Membership, Import, Specialization, FeatureTyping, Subsetting, Redefinition
```

**Connector语义：**
- Connector = 由Association定型的Feature，值为Links
- 连接域内相同实例的特征（instance-specific关联）
- BindingConnector: source和target必须是同一值（typed by SelfLink）
- Succession: source和target是时间有序的Occurrences（typed by HappensBefore）

## SysML v2 API & Services（引擎对外接口设计）

**架构：PIM → PSM（REST/HTTP + OSLC 3.0）**

**核心数据模型：**
```
Record (id:UUID, alias:String[], name, description)
├── Project (commits, branches, tags, defaultBranch, queries)
├── Commit (created, owningProject, previousCommits, change:DataVersion[])
├── CommitReference
│   ├── Branch (head:Commit)
│   └── Tag (taggedCommit:Commit)
├── DataIdentity (version-independent, 1:many with DataVersion)
└── DataVersion (commit, identity, payload:Data?)

Data (interface, getId():UUID)
├── Element (KerML root metaclass)
├── ExternalData (resourceIdentifier:IRI)
├── ExternalRelationship
└── ProjectUsage (usedProject, usedProjectCommit)
```

**五大服务接口：**

| Service | 关键操作 | REST端点模式 |
|---------|---------|-------------|
| ProjectService | createProject, getProjects, deleteProject | POST/GET/DELETE /projects |
| ElementNavigationService | getElements, getElementById, getRootElements, getRelationshipsByRelatedElement | GET /projects/{id}/commits/{id}/elements |
| ProjectDataVersioningService | createCommit, getBranches, createBranch, createTag, diffCommits, mergeIntoBranch | POST/GET /projects/{id}/commits |
| QueryService | createQuery, executeQuery (select/where/orderBy/scope) | POST /projects/{id}/queries |
| ExternalRelationshipService | getExternalRelationships | GET /projects/{id}/external-relationships |

**版本管理模型：**
- Git-like: Project → Branches → Commits → DataVersions
- 每个Commit包含change（创建/修改/删除的DataVersion集合）
- DataIdentity是跨版本的唯一标识，DataVersion是特定commit下的快照
- 支持diffCommits（对比两个commit差异）和mergeIntoBranch

**Query模型：**
- select: 返回哪些属性
- where: Constraint（PrimitiveConstraint = property+operator+value, CompositeConstraint = AND/OR组合）
- scope: 查询范围（默认Project全局）
- orderBy: 排序属性列表
- 运算符: =, !=, <, <=, >, >=, in, instanceOf

## Graphical BNF（可视化渲染层）

图形语法以BNF形式定义SysML v2九大图的渲染规则，核心结构：

```
general-node → definition-node | usage-node
definition-node → part-def | port-def | action-def | state-def | requirement-def | ...
usage-node → part | port | action | state | requirement | ...

每种node = name-compartment + compartment-stack
compartment → features | parts | ports | actions | states | requirements | ...
```

**关键图形元素类型：**

| 图类型 | 节点形式 | 边/关系形式 |
|--------|---------|-----------|
| 结构图(BDD/IBD) | part-def(实线矩形), part(实线矩形), port(方块贴边) | composition(实心菱形), connection(实线), binding(=号线) |
| 活动图 | action(圆角矩形), start-node(实心圆), done-node(圈中圆), fork/join(粗线), decision(菱形) | succession(箭头), flow(带三角箭头) |
| 状态机图 | state(圆角矩形), start-node, done-node | transition(箭头+trigger/guard/effect标签) |
| 需求图 | requirement(矩形+«requirement»), satisfy-requirement | satisfy-edge(虚线箭头+«satisfy»), derive-edge |
| 用例图 | use-case(椭圆形), actor(火柴人) | include-use-case-relationship |

**状态机图形语法核心：**
- state: `«state»` + name + entry/do/exit compartments
- transition: `trigger [guard] / effect` 标签在箭头上
- 复合状态: 外层state内嵌state-transition-view
- start-node/done-node/fork-node/join-node/decision-node 与活动图共享

**端口图形表示：**
- 实线边框小方块贴在part边缘 = composite port
- 虚线边框 = reference port (nested port)
- 方向箭头在port内部item上
- `~`共轭 = 翻转所有方向

## MagicGrid Solution Domain 详细流程

### S1 System Requirements（初始+最终）

1. 初始阶段：从Problem Domain分析结果导出系统需求
   - deriveReqt: System Req ← Stakeholder Need
   - refine: System Req → Problem Domain Element (Block/Activity/MoE)
2. 最终阶段：建立satisfy关系
   - satisfy: Design Element → System Requirement
   - 工具：Dependency Matrix（Derive Requirement Matrix, Satisfy Requirement Matrix）

### S3 System Structure（初始→最终）

1. 初始：基于W3逻辑架构细化为物理解决方案架构
   - 每个逻辑子系统 → 一个设计Block（含详细Value Properties + Ports）
   - IBD展示子系统间连接（通过匹配的Interface Block + Connector）
2. 最终：集成所有子系统解决方案
   - Structure Decomposition Map验证层次
   - IBD验证接口兼容性
   - Trade-off Study选择最优方案

### SS层（子系统）模型结构模式

```
SubsystemModel/
├── 1 Subsystem Requirements/
├── 2 Exchange Items/          (Signal, InterfaceBlock定义)
├── 3 System Behavior/         (Activity + StateMachine)
└── 4 System Structure/        (BDD + IBD)
```

### S4 System Parameters + Verification

- Constraint Block绑定Value Properties → 参数关系
- Parametric Diagram可视化约束网络
- Simulation Profile执行参数计算验证MoE

### 模型集成策略（多文件协作）

- Problem Domain Model → 被Solution Domain Model只读引用（Use/Mount）
- 子系统模型独立开发 → System Configuration Model集成引用
- 接口兼容性检查：IBD中connector两端port类型必须type-compatible（含共轭）
