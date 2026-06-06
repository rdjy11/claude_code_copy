---
name: mbse-modeler
version: 1.4.0
description: MBSE建模助手。基于MagicGrid方法论、SysML v1/v2语法、Cameo Systems Modeler工具知识，输出系统模型代码、架构分析、需求追溯。触发词：MBSE建模、SysML模型、系统架构、BDD、IBD、活动图、状态机、参数图、MagicGrid。不适用于：纯代码开发、非系统工程场景。
metadata:
  author: MI
  created: 2026-05-07
  updated: 2026-05-28
---

# MBSE建模助手

面向汽车电子系统（EEA/ADAS/智能座舱/域控制器），基于MagicGrid方法论和SysML v1.6/v2.0标准，输出可执行的系统模型。

## 能力范围

| 能力 | 输出物 | 典型触发 |
|------|--------|---------|
| 结构建模 | BDD + IBD（SysML v2 part def/usage） | "建模XX系统结构" |
| 行为建模 | Activity/StateMachine/Sequence | "建模XX功能流程" |
| 需求建模 | Requirement def + satisfy/verify/derive追溯 | "建模需求追溯" |
| 参数建模 | Constraint def + binding | "建模参数约束" |
| 安全分析 | HARA表 + Safety Goals + ASIL推导 | "做HARA建模" |
| MagicGrid全流程 | Problem→Solution→Implementation三域建模 | "按MagicGrid建模" |
| SysML v1↔v2转换 | 概念映射 + 代码重写 | "转换为SysML v2" |

## 核心规则

- **Do NOT** 混淆 def（类型定义）和 usage（实例化）——这是SysML v2最常见的错误
- **Do NOT** 遗漏 import 语句——SysML v2所有标准类型必须显式导入（ScalarValues::*, ISQ::*, SI::*）
- **Do NOT** 在端口本身声明方向——方向在端口内部的item/attribute上声明（`in`/`out`）
- **Do NOT** 输出不完整的模型——每个模型必须包含package声明、import、def和usage
- **输出格式**：默认SysML v2文本语法（`.sysml`），除非用户指定v1或Cameo操作指导

## MagicGrid方法论框架

```
PILLAR:      Requirements    Behavior        Structure       Parameters
─────────────────────────────────────────────────────────────────────────
Problem Domain (Black-box):
  B1-W1      Stakeholder     B2 Use Cases    B3 System       B4 MoE
             Needs                           Context
Problem Domain (White-box):
  W1         (merged↑)       W2 Functional   W3 Logical      W4 MoEs
                             Analysis        Subsystems      for Subsys
─────────────────────────────────────────────────────────────────────────
Solution Domain:
  S1         System Reqs     S2 System       S3 System       S4 System
                             Behavior        Structure       Parameters
  SS1        Subsys Reqs     SS2 Subsys      SS3 Subsys      SS4 Subsys
                             Behavior        Structure       Parameters
  C1         Component       C2 Component    C3 Component    C4 Component
             Reqs            Behavior        Structure       Parameters
─────────────────────────────────────────────────────────────────────────
Implementation Domain:
  I1         Physical Reqs   → Software / Electrical / Mechanical
```

### MagicGrid建模工作流

1. **B1-W1**: 捕获利益相关者需求（Requirement Table）
2. **B3**: 系统上下文（IBD：SoI + External Actors + 接口）
3. **B2**: 用例分析（Use Case Diagram + 场景描述）
4. **B4**: 效能度量（MoE参数定义）
5. **W2**: 功能分析（Activity Diagram → 功能分解）
6. **W3**: 逻辑子系统划分（BDD → 逻辑架构）
7. **S1-S4**: 系统需求 → 行为 → 结构 → 参数（Solution层全面细化）
8. **I1**: 物理需求分配到Software/HW/Mechanical

## SysML v2 语法速查

### 核心概念映射（v1 → v2）

| SysML v1 | SysML v2 | 说明 |
|----------|----------|------|
| `<<block>>` | `part def` | 结构类型定义 |
| Part property | `part x : Type;` | 组合（拥有） |
| Reference property | `ref part x : Type;` | 引用（不拥有） |
| `<<valueType>>` | `attribute def` | 值类型 |
| `<<flowPort>>` | `port def` + `in`/`out` items | 端口 |
| `<<activity>>` | `action def` | 行为定义 |
| `<<stateMachine>>` | `state def` | 状态机 |
| `<<requirement>>` | `requirement def` | 需求 |
| Generalization | `:>` 或 `specializes` | 泛化 |
| `{redefines}` | `:>>` 或 `redefines` | 重定义 |
| `<<satisfy>>` | `satisfy req by design;` | 满足关系 |
| `<<allocate>>` | `allocate X to Y;` | 分配关系 |

### 关键语法模式

```sysml
// 1. 包与导入
package 'SystemName' {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;
}

// 2. 结构定义
part def Vehicle {
    attribute mass :> ISQ::mass;
    part eng : Engine;          // 组合
    ref part driver : Person;   // 引用
}

// 3. 端口（方向在内部item上声明）
port def SensorPort {
    out attribute sensorData : Real;
    in attribute controlCmd : Integer;
}

// 4. 共轭（翻转所有in/out方向）
part def Controller {
    port sensorInput : ~SensorPort;  // ~ = conjugated
}

// 5. 接口与连接
interface def SensorLink {
    end sensorEnd : SensorPort;
    end ctrlEnd : ~SensorPort;
}

// 6. 动作（行为）
action def ProcessData {
    in rawData : Real;
    out result : Boolean;
}

// 7. 状态机
state def OperatingStates {
    first start then idle;
    state idle;
    accept StartSignal then running;
    state running;
    accept StopSignal then idle;
}

// 8. 需求
requirement def <'SR-001'> SafetyReq {
    doc /* 系统应在100ms内完成制动响应 */
    subject system : BrakeSystem;
}
satisfy safetyReq by brakeController;

// 9. 约束
constraint def ResponseTime {
    in actual : Real;
    in limit : Real;
    actual <= limit
}

// 10. 分配
allocate processingFunction to ecu;
```

### 易错点清单

1. **def vs usage**: `part def Vehicle` = 类型定义; `part v : Vehicle` = 实例
2. **`:>` 重载**: 在def上 = 泛化; 在usage上 = 子集
3. **`:>>` 始终 = 重定义**
4. **`ref` 关键字** = 引用（非组合），没有ref就是组合拥有
5. **`item` vs `part`**: item是流动的东西，part是系统结构
6. **端口方向** 在端口内部的item上声明，不在端口本身
7. **`~` 共轭** 翻转端口内所有方向
8. **`bind x = y`** = 同一性（同一个实例），不是赋值
9. **`first start then X`** = 初始转换，`start`是隐含的
10. **命名空间**: `::` 限定名, `.` 实例特性访问
11. **单位**: 值后缀 `[unit]`，如 `2000[kg]`, `48[h]`
12. **所有标准类型必须显式 import**: ScalarValues, ISQ, SI

## Cameo Systems Modeler 操作知识

### 9大SysML图

| 图 | 用途 | Cameo快捷操作 |
|----|------|-------------|
| BDD (Block Definition Diagram) | 定义Block及其关系 | 快捷键B创建Block |
| IBD (Internal Block Diagram) | Block内部结构、端口连接 | 选Block→smart manipulator |
| Requirement Diagram | 需求及追溯关系 | 拖拽ReqIF/Excel导入 |
| Parametric Diagram | 约束方程建模 | Constraint Block + Binding Connector |
| Activity Diagram | 功能流程、数据流 | Swimlane分配到结构 |
| Sequence Diagram | 交互时序 | Lifeline = Part Properties |
| State Machine Diagram | 状态转换 | Region→States→Transitions |
| Use Case Diagram | 功能边界、参与者 | Subject = System Block |
| Package Diagram | 模型组织 | 按MagicGrid 4-pillar组织 |

### Block建模流程

1. **BDD**: 创建Block → 定义Part Properties/Value Properties → 建立Generalization/Composition
2. **IBD**: 为Block创建IBD → 显示Parts/Ports → 创建Connector → 配置Interface Block → 定义Item Flow
3. **Ports**: Proxy Port(typed by Interface Block) / Full Port(own features) → 共轭机制兼容连接

### 功能分配（Allocation）

- **Definition mode**: Activity → Block（功能定义分配到结构定义）
- **Usage mode**: Action → Part Property（行为实例分配到结构实例）
- 可视化: SysML Allocation Matrix + Swimlane in Activity Diagram

### ISO 26262 HARA建模（Safety & Reliability Analyzer）

完整HARA工作流（在Cameo中以表格形式驱动）：

```
HazOp Table (功能 → 故障模式识别: More/Less/Unintended/Late/Early/Inverted/No)
    ↓
Operational Conditions Table (5组: Location/Road/Traffic/VehicleUsage/Environmental)
    ↓
Operational Situations Table (条件组合 + Exposure等级)
    ↓
Accident Scenarios Table (故障模式 × 运行场景 + Controllability)
    ↓
Effects Table (Vehicle Level / System Level)
    ↓
Hazards Table
    ↓
HARA Table (综合 → 自动计算ASIL)
    ↓
Safety Requirement Diagram (Safety Goal → derive → FSR/TSR/SWSR/HWSR)
    ↓
ASIL Decomposition (D→C+A, D→B+B, C→B+A, etc.)
```

## 工作流程

### 通用流程

| 步骤 | 操作 | 检查点 |
|------|------|--------|
| 1. 确认范围 | 确定建模对象、层级、适用视角 | **CP1: 范围确认** |
| 2. 选择方法 | MagicGrid域/列定位 → 确定输出图类型 | — |
| 3. 模型构建 | 按SysML v2语法输出完整模型代码 | **CP2: 语法验证** |
| 4. 追溯检查 | 验证需求→设计→验证链完整性 | **CP3: 追溯完整** |

### CP2 — 语法验证自检

- [ ] 是否有package声明
- [ ] 所有标准类型是否已import（ScalarValues, ISQ, SI）
- [ ] def和usage是否正确区分
- [ ] 端口方向是否在内部item/attribute上声明
- [ ] 连接两端的端口类型是否兼容（含共轭）
- [ ] 控制流是否有`first start then`起始
- [ ] 需求是否有`subject`声明
- [ ] 约束表达式是否使用`==`/`<=`/`>=`

### CP3 — 追溯完整性

- [ ] 每个Safety Goal是否可追溯到Hazardous Event
- [ ] 每个System Requirement是否有satisfy关系到设计元素
- [ ] 每个功能是否已allocate到结构
- [ ] 是否存在"悬挂需求"（无上游追溯或无下游分解）

---

## 汽车领域建模模板

### 整车系统上下文模板

```sysml
package VehicleSystemContext {
    private import ScalarValues::*;

    // 外部参与者
    part def Driver;
    part def Road;
    part def Infrastructure;  // V2X
    part def Environment;     // 天气、光照

    // 系统边界
    part def VehicleSystem {
        // 域控制器
        part chassisDomain : ChassisDomainController;
        part adDomain : ADDomainController;
        part cockpitDomain : CockpitDomainController;
        part bodyDomain : BodyDomainController;
        part powerDomain : PowerDomainController;
    }

    // 系统上下文实例
    part vehicleContext {
        part driver : Driver;
        part vehicle : VehicleSystem;
        part road : Road;
        part infra : Infrastructure;
        part env : Environment;

        // 接口连接
        interface driverToVehicle connect driver to vehicle;
        interface vehicleToRoad connect vehicle to road;
        interface vehicleToInfra connect vehicle to infra;
    }
}
```

### ADAS功能建模模板

```sysml
package AdasFunctionModel {
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;

    // 感知
    action def Perceive {
        in sensorData : SensorFusion;
        out environment : EnvironmentModel;
    }

    // 决策
    action def Plan {
        in environment : EnvironmentModel;
        in route : RoutePlan;
        out trajectory : Trajectory;
    }

    // 执行
    action def Act {
        in trajectory : Trajectory;
        out vehicleControl : ControlCommand;
    }

    // PPA主流程
    action adasPipeline {
        action perceive : Perceive;
        action plan : Plan;
        action act : Act;

        first start then perceive;
        then plan;
        then act;
        then done;

        flow from perceive.environment to plan.environment;
        flow from plan.trajectory to act.trajectory;
    }
}
```

---

## 建模引擎设计知识

### KerML元模型架构（引擎内核基础）

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

### SysML v2 API & Services（引擎对外接口设计）

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

### Graphical BNF（可视化渲染层）

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

### MagicGrid Solution Domain详细流程

**S1 System Requirements（初始+最终）：**
1. 初始阶段：从Problem Domain分析结果导出系统需求
   - deriveReqt: System Req ← Stakeholder Need
   - refine: System Req → Problem Domain Element (Block/Activity/MoE)
2. 最终阶段：建立satisfy关系
   - satisfy: Design Element → System Requirement
   - 工具：Dependency Matrix（Derive Requirement Matrix, Satisfy Requirement Matrix）

**S3 System Structure（初始→最终）：**
1. 初始：基于W3逻辑架构细化为物理解决方案架构
   - 每个逻辑子系统 → 一个设计Block（含详细Value Properties + Ports）
   - IBD展示子系统间连接（通过匹配的Interface Block + Connector）
2. 最终：集成所有子系统解决方案
   - Structure Decomposition Map验证层次
   - IBD验证接口兼容性
   - Trade-off Study选择最优方案

**SS层（子系统）模型结构模式：**
```
SubsystemModel/
├── 1 Subsystem Requirements/
├── 2 Exchange Items/          (Signal, InterfaceBlock定义)
├── 3 System Behavior/         (Activity + StateMachine)
└── 4 System Structure/        (BDD + IBD)
```

**S4 System Parameters + Verification：**
- Constraint Block绑定Value Properties → 参数关系
- Parametric Diagram可视化约束网络
- Simulation Profile执行参数计算验证MoE

**模型集成策略（多文件协作）：**
- Problem Domain Model → 被Solution Domain Model只读引用（Use/Mount）
- 子系统模型独立开发 → System Configuration Model集成引用
- 接口兼容性检查：IBD中connector两端port类型必须type-compatible（含共轭）

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-05-07 | 初版，基于NoMagic 2021x + SysML v2 Release 0.58.0 + MagicGrid BoK系统学习 |
| v1.1 | 2026-05-07 | 补充建模引擎设计知识：KerML元模型架构、SysML v2 API数据模型与服务接口、Graphical BNF渲染规则、MagicGrid Solution Domain详细流程 |
| v1.4.0 | 2026-05-28 | 合并安装更新，内联全部参考内容 |
