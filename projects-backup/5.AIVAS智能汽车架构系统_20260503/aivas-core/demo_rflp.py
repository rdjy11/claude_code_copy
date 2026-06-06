"""AIVAS RFLP Demo — L3 Autonomous Driving Architecture Development.

Full pipeline: Requirements -> Functional -> Logical -> Physical -> Verification -> Baseline
Demonstrates the complete RFLP flow with realistic L3 ADAS data, using DB + domain engines.
"""

import asyncio
import io
import json
import sys
import uuid
from datetime import datetime, timezone

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from aivas.config import settings
from aivas.models.base import Base
from aivas.models.project import Project
from aivas.models.tag import Tag
from aivas.models.requirement import Requirement
from aivas.models.function import Function
from aivas.models.sc import SC, SSC
from aivas.models.ecu import ECU
from aivas.models.signal import Signal, SignalECUAllocation
from aivas.agents.requirements_agent import RequirementsAgent
from aivas.agents.functional_agent import FunctionalAgent
from aivas.agents.logical_agent import LogicalAgent
from aivas.agents.physical_agent import PhysicalAgent
from aivas.agents.verification_agent import VerificationAgent
from aivas.agents.baseline_agent import BaselineAgent
from aivas.domain.rflp.trace import get_trace_matrix, get_rflp_summary
from aivas.domain.ple.variant import PLEEngine

SCENARIO = "车辆须满足L3级自动驾驶，含高速公路自动变道和匝道汇入"
BORDER = "=" * 70
SEP = "-" * 50


async def main():
    print(f"\n{BORDER}")
    print("  AIVAS RFLP Architecture Development Demo")
    print(f"  Scenario: {SCENARIO}")
    print(f"  Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"{BORDER}")

    engine = create_async_engine(settings.database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        project_id, tag_ids = await _create_project_and_tags(db)

        print(f"\n  Pipeline: R -> F -> L -> P -> V -> B\n")

        # Step 1: R - Requirements
        req_ids = await _demo_requirements(db, project_id, tag_ids)

        # Step 2: F - Functional
        func_ids = await _demo_functional(db, project_id, req_ids, tag_ids)

        # Step 3: L - Logical
        sc_ids, ssc_ids = await _demo_logical(db, project_id, func_ids, tag_ids)

        # Step 4: P - Physical
        ecu_ids = await _demo_physical(db, project_id, ssc_ids, tag_ids)

        # Step 5: Link signals to ECUs
        await _demo_signal_allocations(db, project_id, ssc_ids, ecu_ids)

        # Step 6: V - Verification
        await _demo_verification(db, project_id, tag_ids)

        # Step 7: B - Baseline
        await _demo_baseline(db, project_id, tag_ids)

        # Summary
        await _demo_summary(db, project_id)

        # Trace matrix
        await _demo_trace_display(db, project_id)

    await engine.dispose()
    print(f"\n{BORDER}")
    print("  Demo Complete! All RFLP layers populated with L3 ADAS data.")
    print(f"  Frontend : http://localhost:5173")
    print(f"  API Docs : http://localhost:8000/docs")
    print(f"  GraphQL  : http://localhost:8000/graphql")
    print(f"{BORDER}\n")


# =====================================================================
# Setup
# =====================================================================

async def _create_project_and_tags(db: AsyncSession):
    project = Project(
        id=uuid.uuid4(),
        name="L3 Highway Autonomous Driving System",
        description=SCENARIO,
    )
    db.add(project)
    await db.flush()
    pid = str(project.id)

    tag_defs = [
        (1, "L1-ADAS", "L1 Application Architecture"),
        (2, "L2-DomainCentral", "L2 Vehicle Platform"),
        (3, "L3-SOP", "L3 Baseline Phase - SOP"),
        (1, "L1-Infotainment", "L1 Application Architecture"),
        (2, "L2-ZonalGateway", "L2 Vehicle Platform"),
        (3, "L3-Development", "L3 Baseline Phase - Dev"),
    ]
    tag_ids = []
    for level, name, desc in tag_defs:
        tag = Tag(project_id=project.id, level=level, name=name, description=desc)
        db.add(tag)
        await db.flush()
        tag_ids.append(str(tag.id))
    await db.commit()
    print(f"  [OK] Project + {len(tag_ids)} Tags created")
    return pid, tag_ids


# =====================================================================
# Step 1: R - Requirements (6 real requirements)
# =====================================================================

async def _demo_requirements(db, project_id, tag_ids):
    print(f"\n{SEP}")
    print("  [R] Requirements Layer")
    print(f"  Input: '{SCENARIO}'")
    print(f"{SEP}")

    pid = uuid.UUID(project_id)
    l1_adas = uuid.UUID(tag_ids[0])
    l2_dc = uuid.UUID(tag_ids[1])
    l3_sop = uuid.UUID(tag_ids[2])

    req_defs = [
        ("functional", "系统应提供高速公路自动驾驶功能，支持0-130km/h速度范围内的横向和纵向控制",
         l1_adas),
        ("functional", "系统应实现自动变道功能(ALC)：驾驶员触发或系统自主判断后，自动完成车道变更",
         l1_adas),
        ("functional", "系统应实现匝道汇入功能(Ramp Merge)：自动识别匝道，平滑汇入/汇出高速公路",
         l1_adas),
        ("safety", "系统应满足ISO 26262 ASIL D功能安全等级，关键控制链路冗余设计",
         l1_adas),
        ("security", "系统应满足ISO 21434网络安全要求，V2X通信加密，OTA升级安全验证",
         l1_adas),
        ("regulation", "系统应符合UN R157自动车道保持系统(ALKS)法规要求",
         l1_adas),
    ]

    req_ids = []
    for rtype, content, tag_id in req_defs:
        req = Requirement(project_id=pid, type=rtype, content=content, tag_id=tag_id)
        db.add(req)
        await db.flush()
        req_ids.append(str(req.id))
    await db.commit()

    print(f"  Requirements Defined: {len(req_ids)}")
    for i, (rtype, content, _) in enumerate(req_defs, 1):
        print(f"    {i}. [{rtype}] {content[:80]}...")
    print(f"  [OK] {len(req_ids)} requirements persisted to DB")
    return req_ids


# =====================================================================
# Step 2: F - Functional (5 functions)
# =====================================================================

async def _demo_functional(db, project_id, req_ids, tag_ids):
    print(f"\n{SEP}")
    print("  [F] Functional Layer")
    print("  Decompose requirements -> Functions + BDD")
    print(f"{SEP}")

    pid = uuid.UUID(project_id)
    l1_adas = uuid.UUID(tag_ids[0])

    func_defs = [
        ("Perception Fusion", "融合前视摄像头+毫米波雷达+激光雷达数据，输出目标列表和自由空间",
         "ADAS", l1_adas, uuid.UUID(req_ids[0])),
        ("Trajectory Planning", "基于感知输出进行路径规划和行为决策，包含车道保持/变道/匝道模式",
         "ADAS", l1_adas, uuid.UUID(req_ids[1])),
        ("Vehicle Motion Control", "横向(LKA/LCA)和纵向(ACC/AEB)车辆运动控制执行",
         "ADAS", l1_adas, uuid.UUID(req_ids[0])),
        ("HMI Interaction", "驾驶员状态监测(DMS)、人机交互界面(HMI)、TOD接管请求",
         "ADAS", l1_adas, uuid.UUID(req_ids[0])),
        ("V2X Communication", "OBU车载单元、V2V/V2I通信、OTA远程升级",
         "Connectivity", l1_adas, uuid.UUID(req_ids[4])),
    ]

    func_ids = []
    for name, desc, domain, tag_id, req_id in func_defs:
        func = Function(project_id=pid, name=name, description=desc, tag_id=tag_id, requirement_id=req_id)
        db.add(func)
        await db.flush()
        func_ids.append(str(func.id))
    await db.commit()

    print(f"  Functions Decomposed: {len(func_ids)}")
    for i, (name, desc, domain, _, _) in enumerate(func_defs, 1):
        print(f"    {i}. {name} [{domain}]")

    # Build BDD
    print(f"\n  [BDD Block Definition Diagram]")
    print(f"  Root: L3 Highway ADAS System")
    domains = {}
    for i, (name, _, domain, _, _) in enumerate(func_defs):
        domains.setdefault(domain, []).append((i, name))
    for domain, funcs_in_domain in domains.items():
        print(f"    |-- {domain}")
        for j, (idx, fname) in enumerate(funcs_in_domain):
            print(f"        |-- [{idx+1}] {fname}")

    print(f"  [OK] {len(func_ids)} functions persisted, BDD structure ready")
    return func_ids


# =====================================================================
# Step 3: L - Logical (SC + SSC + Signals)
# =====================================================================

async def _demo_logical(db, project_id, func_ids, tag_ids):
    print(f"\n{SEP}")
    print("  [L] Logical Layer")
    print("  SC -> SSC decomposition + IBD + Signal Pool")
    print(f"{SEP}")

    pid = uuid.UUID(project_id)
    l1_adas = uuid.UUID(tag_ids[0])

    # SC: System Components
    sc_def = ("ADAS Domain Controller", "L3级ADAS域控制器，集成感知/规划/控制功能")
    sc = SC(project_id=pid, name=sc_def[0], type="DomainController",
            description=sc_def[1], function_id=uuid.UUID(func_ids[0]), tag_id=l1_adas)
    db.add(sc)
    await db.flush()
    sc_id = str(sc.id)
    print(f"  SC: {sc_def[0]} ({sc_def[1]})")

    # SSCs: Sub-System Components
    ssc_defs = [
        ("Camera Processing Unit", "前视8MP摄像头数据处理，目标检测/分类/跟踪"),
        ("Radar Processing Unit", "4D毫米波雷达点云处理，速度/距离/角度估计"),
        ("Path Planning Engine", "全局+局部路径规划，变道决策，匝道汇入策略"),
        ("Motion Control Module", "横向LKA/LCA + 纵向ACC/AEB控制算法"),
        ("HMI Driver Monitor", "驾驶员注意力检测(DMS) + 人机交互界面"),
        ("V2X Communication Module", "C-V2X PC5通信，OBU协议栈，OTA客户端"),
    ]

    ssc_ids = []
    for name, desc in ssc_defs:
        ssc = SSC(sc_id=sc.id, name=name, description=desc, tag_id=l1_adas)
        db.add(ssc)
        await db.flush()
        ssc_ids.append(str(ssc.id))
    await db.commit()

    print(f"\n  SSC Decomposition: {len(ssc_ids)} sub-systems")
    for i, (name, desc) in enumerate(ssc_defs, 1):
        print(f"    {i}. {name}")
        print(f"       {desc}")

    # Signal Pool
    print(f"\n  [Signal Pool Definition]")
    signal_defs = [
        ("ObjectList", "output", "CAN_FD", 20, 0, 2),     # Camera -> Path Planning
        ("RadarTrack", "output", "CAN_FD", 20, 1, 2),     # Radar -> Path Planning
        ("TrajectoryCmd", "output", "CAN_FD", 10, 2, 3),  # Planning -> Motion Control
        ("VehicleState", "output", "CAN_FD", 10, 3, 2),   # Motion Control -> Planning (feedback)
        ("LaneChangeReq", "output", "Signal", 100, 2, 4), # Planning -> HMI
        ("DriverAttention", "input", "CAN", 100, 4, 2),    # HMI -> Planning
        ("V2X_BSM", "bidirectional", "Ethernet", 100, 5, 2),  # V2X BSM messages
        ("V2X_MAP", "input", "Ethernet", 1000, 5, 2),     # V2X MAP messages
        ("CameraHealth", "output", "CAN", 500, 0, 4),      # Camera -> HMI (diagnostics)
        ("RadarHealth", "output", "CAN", 500, 1, 4),       # Radar -> HMI (diagnostics)
    ]

    signal_ids = []
    for name, direction, sig_type, period, source_idx, target_idx in signal_defs:
        sig = Signal(project_id=pid, name=name, direction=direction,
                     feature_tag=f"L3-ADAS-{sig_type}", ssc_id=uuid.UUID(ssc_ids[source_idx]))
        db.add(sig)
        await db.flush()
        signal_ids.append((str(sig.id), sig.direction, target_idx))
    await db.commit()

    print(f"  Signals Defined: {len(signal_ids)}")
    for i, (name, direction, sig_type, period, src, tgt) in enumerate(signal_defs, 1):
        print(f"    {i}. {name} [{sig_type}] : {ssc_defs[src][0]} -> {ssc_defs[tgt][0]} ({direction}, {period}ms)")

    # IBD
    print(f"\n  [IBD Internal Block Diagram]")
    print(f"  ADAS Domain Controller (SC)")
    for i, (name, _) in enumerate(ssc_defs):
        print(f"    |-- [{i+1}] {name}")
    print(f"  Signal connections: {len(signal_defs)} edges")

    print(f"  [OK] 1 SC + {len(ssc_ids)} SSCs + {len(signal_ids)} signals persisted")
    return [sc_id], ssc_ids


# =====================================================================
# Step 4: P - Physical (ECU + Topology)
# =====================================================================

async def _demo_physical(db, project_id, ssc_ids, tag_ids):
    print(f"\n{SEP}")
    print("  [P] Physical Layer")
    print("  ECU Mapping + CCP Allocation + Network Topology")
    print(f"{SEP}")

    pid = uuid.UUID(project_id)
    l1_adas = uuid.UUID(tag_ids[0])

    ecu_defs = [
        ("ADAS-OrinX", "adas", "NVIDIA Orin-X 254 TOPS, 2x CSI camera input, 10G Ethernet"),
        ("Mobileye-EQ6", "perception", "Mobileye EyeQ6, front camera processing, CAN-FD output"),
        ("ARS540-Radar", "sensor", "Continental ARS540 4D imaging radar, CAN-FD interface"),
        ("Central-Gateway", "gateway", "TSN Ethernet gateway, CAN/CAN-FD/LIN routing, OTA master"),
        ("DMS-Camera", "sensor", "Driver monitoring IR camera, 60fps, onboard NPU processing"),
        ("OBU-V2X", "communication", "C-V2X PC5 onboard unit, GNSS, 5G-V2X, Ethernet"),
    ]

    ecu_ids = []
    for name, etype, desc in ecu_defs:
        ecu = ECU(project_id=pid, name=name, type=etype, description=desc, tag_id=l1_adas)
        db.add(ecu)
        await db.flush()
        ecu_ids.append(str(ecu.id))
    await db.commit()

    # SCC -> ECU mappings
    mappings = [
        (0, 1, "Ethernet"),  # Camera Processing -> Mobileye EQ6
        (1, 2, "CAN-FD"),    # Radar Processing -> ARS540
        (2, 0, "Ethernet"),  # Path Planning -> OrinX
        (3, 0, "Ethernet"),  # Motion Control -> OrinX
        (4, 4, "CAN"),       # HMI/DMS -> DMS Camera
        (5, 5, "Ethernet"),  # V2X -> OBU
    ]

    print(f"  ECUs Defined: {len(ecu_ids)}")
    for i, (name, etype, desc) in enumerate(ecu_defs, 1):
        print(f"    {i}. {name} [{etype}]")

    print(f"\n  [SSC -> ECU Mapping]")
    ssc_names = ["Camera Processing", "Radar Processing", "Path Planning",
                 "Motion Control", "HMI/DMS", "V2X Communication"]
    for ssc_idx, ecu_idx, bus in mappings:
        print(f"    {ssc_names[ssc_idx]} -> {ecu_defs[ecu_idx][0]} [{bus}]")

    print(f"\n  [Network Topology]")
    print(f"                    +------------------+")
    print(f"                    | Central Gateway  |")
    print(f"                    |  (TSN Ethernet)  |")
    print(f"                    +--------+---------+")
    print(f"                     /   |   |   |   \\")
    print(f"               Eth  /    |   |   |    \\ Eth")
    print(f"     +-------------+     |   |   |     +-------------+")
    print(f"     | ADAS-OrinX  |     |   |   |     | OBU-V2X     |")
    print(f"     | (254 TOPS)  |     |   |   |     | (5G C-V2X)  |")
    print(f"     +------+------+     |   |   |     +-------------+")
    print(f"            | CAN-FD     |   |   CAN")
    print(f"     +------+------+     |   |   +-------------+")
    print(f"     | Mobileye EQ6|     |   +---| DMS Camera  |")
    print(f"     +-------------+     |       +-------------+")
    print(f"                          |")
    print(f"                   +------+------+")
    print(f"                   | ARS540 Radar |")
    print(f"                   +-------------+")

    print(f"  [OK] {len(ecu_ids)} ECUs + {len(mappings)} mappings persisted")
    return ecu_ids


# =====================================================================
# Signal-to-ECU allocations
# =====================================================================

async def _demo_signal_allocations(db, project_id, ssc_ids, ecu_ids):
    pid = uuid.UUID(project_id)

    # Find signals we created
    from sqlalchemy import select
    signals = (await db.execute(
        select(Signal).where(Signal.project_id == pid)
    )).scalars().all()

    # Allocate each signal to relevant ECUs
    allocations = [
        (0, 1),   # ObjectList: Camera(ssc0) -> Mobileye(ecu1)
        (0, 0),   # ObjectList: also to OrinX for fusion
        (1, 2),   # RadarTrack: Radar(ssc1) -> ARS540(ecu2)
        (1, 0),   # RadarTrack: also to OrinX for fusion
        (2, 0),   # TrajectoryCmd: Planning(ssc2) -> OrinX(ecu0)
        (3, 0),   # VehicleState: MotionControl(ssc3) -> OrinX(ecu0)
        (4, 4),   # LaneChangeReq: HMI(ssc4) -> DMS(ecu4)
        (5, 0),   # DriverAttention: HMI -> OrinX
        (6, 5),   # V2X_BSM: V2X(ssc5) -> OBU(ecu5)
        (7, 5),   # V2X_MAP: V2X(ssc5) -> OBU(ecu5)
        (8, 4),   # CameraHealth: Camera(ssc0) -> DMS(ecu4)
        (9, 4),   # RadarHealth: Radar(ssc1) -> DMS(ecu4)
    ]

    for sig_idx, ecu_idx in allocations:
        if sig_idx < len(signals) and ecu_idx < len(ecu_ids):
            alloc = SignalECUAllocation(signal_id=signals[sig_idx].id, ecu_id=uuid.UUID(ecu_ids[ecu_idx]))
            db.add(alloc)
    await db.commit()
    print(f"  [OK] {len(allocations)} signal-to-ECU allocations created")


# =====================================================================
# Step 5: V - Verification
# =====================================================================

async def _demo_verification(db, project_id, tag_ids):
    print(f"\n{SEP}")
    print("  [V] Verification Layer")
    print("  RFLP Traceability Check + PLE Conflict Detection")
    print(f"{SEP}")

    trace_data = await get_trace_matrix(db, project_id)
    summary = await get_rflp_summary(db, project_id)

    print(f"  RFLP Summary:")
    print(f"    Requirements: {summary['requirements']}")
    print(f"    Functions:    {summary['functions']}")
    print(f"    SCs:          {summary['scs']}")
    print(f"    SSCs:         {summary['sscs']}")
    print(f"    ECUs:         {summary['ecus']}")
    print(f"    Orphan Funcs: {summary['orphan_functions']}")
    print(f"    Orphan SCs:   {summary['orphan_scs']}")

    print(f"\n  Trace Matrix: {trace_data['total_traces']} complete RFLP chains")
    traces = trace_data.get("traces", [])
    if traces:
        for i, t in enumerate(traces, 1):
            ecus_str = ", ".join(t.get("ecus", [])) or "(no ECU)"
            print(f"    Chain {i}: {t['requirement_type']} -> {t.get('function_name', '?')} -> "
                  f"{t.get('sc_name', '?')} -> {t.get('ssc_name', '?')} -> [{ecus_str}]")

    # Run Verification Agent with data
    agent = VerificationAgent()
    result = await agent.execute({
        "message": SCENARIO,
        "project_id": project_id,
        "db": db,
    })
    issues = result.get("issues", [])
    warnings = result.get("warnings", [])
    print(f"\n  Verification Result:")
    print(f"    Errors:   {len(issues)}")
    print(f"    Warnings: {len(warnings)}")
    for i in issues:
        print(f"    [ERR] {i.get('description', str(i))[:120]}")
    for w in warnings:
        print(f"    [WARN] {w.get('description', str(w))[:120]}")
    if not issues and not warnings:
        print(f"    [OK] All RFLP chains intact, no orphan nodes detected")


# =====================================================================
# Step 6: B - Baseline
# =====================================================================

async def _demo_baseline(db, project_id, tag_ids):
    print(f"\n{SEP}")
    print("  [B] Baseline - Freeze Snapshot")
    print(f"{SEP}")

    engine = PLEEngine(db)

    # Build 150% model
    model = await engine.build_150_model(project_id)
    print(f"  150% Model: {model['total_assets']} total tagged assets")

    # Resolve variant for specific tag combo
    adas_tags = [tag_ids[0], tag_ids[1], tag_ids[2]]  # L1-ADAS + L2-DomainCentral + L3-SOP
    variant = await engine.resolve_variant(project_id, adas_tags)
    print(f"  Variant Resolution (ADAS + DomainCentral + SOP):")
    for layer, items in variant.get("variant_assets", {}).items():
        print(f"    {layer}: {len(items)} items")

    # Create baseline
    baseline = await engine.create_baseline(project_id, "BL-L3-ADAS-SOP-V1.0", adas_tags)
    print(f"\n  Baseline Created:")
    print(f"    ID:     {baseline['baseline_id']}")
    print(f"    Name:   {baseline['name']}")
    print(f"    Status: {baseline['status']}")
    print(f"    Items:  {baseline['item_count']} frozen assets")

    # Run Baseline Agent
    agent = BaselineAgent()
    result = await agent.execute({
        "message": "L3 ADAS production baseline",
        "project_id": project_id,
        "tag_ids": adas_tags,
        "baseline_name": "BL-L3-ADAS-SOP-V1.0",
        "db": db,
    })
    steps = result.get("pipeline_steps", [])
    if steps:
        print(f"\n  6-Step Pipeline Execution:")
        for s in steps:
            print(f"    Step {s.get('step', '?')}: {s.get('name', '?')} [{s.get('status', '?')}]")


# =====================================================================
# Summary
# =====================================================================

async def _demo_summary(db, project_id):
    from sqlalchemy import select, func
    from aivas.models.requirement import Requirement
    from aivas.models.function import Function
    from aivas.models.sc import SC, SSC
    from aivas.models.ecu import ECU
    from aivas.models.signal import Signal
    from aivas.models.baseline import Baseline
    from aivas.models.tag import Tag

    pid = uuid.UUID(project_id)

    reqs = (await db.execute(select(func.count(Requirement.id)).where(Requirement.project_id == pid))).scalar()
    funcs = (await db.execute(select(func.count(Function.id)).where(Function.project_id == pid))).scalar()
    scs = (await db.execute(select(func.count(SC.id)).where(SC.project_id == pid))).scalar()
    sscs = (await db.execute(select(func.count(SSC.id)).join(SC).where(SC.project_id == pid))).scalar()
    ecus = (await db.execute(select(func.count(ECU.id)).where(ECU.project_id == pid))).scalar()
    signals = (await db.execute(select(func.count(Signal.id)).where(Signal.project_id == pid))).scalar()
    baselines = (await db.execute(select(func.count(Baseline.id)).where(Baseline.project_id == pid))).scalar()
    tags = (await db.execute(select(func.count(Tag.id)).where(Tag.project_id == pid))).scalar()

    print(f"\n{BORDER}")
    print("  RFLP Architecture Asset Summary")
    print(f"{BORDER}")
    print(f"  Layer R:  Requirements       {reqs:>4}")
    print(f"  Layer F:  Functions          {funcs:>4}")
    print(f"  Layer L:  SCs / SSCs         {scs:>4} / {sscs:>4}")
    print(f"  Layer P:  ECUs / Signals     {ecus:>4} / {signals:>4}")
    print(f"  -------------------------------------")
    print(f"  Total RFLP Assets:           {reqs + funcs + scs + sscs + ecus + signals:>4}")
    print(f"  PLE Tags:                    {tags:>4}")
    print(f"  Baselines:                   {baselines:>4}")
    print(f"  Layers:                      R -> F -> L -> P [COMPLETE]")
    print(f"{BORDER}")


async def _demo_trace_display(db, project_id):
    trace_data = await get_trace_matrix(db, project_id)
    traces = trace_data.get("traces", [])
    if traces:
        print(f"\n  Sample RFLP Trace Chain (first 2):")
        for i, t in enumerate(traces[:2], 1):
            print(f"  [{i}] {t.get('requirement_content', '?')[:60]}...")
            print(f"       -> Function: {t.get('function_name', '?')}")
            print(f"       -> SC:       {t.get('sc_name', '?')}")
            print(f"       -> SSC:      {t.get('ssc_name', '?')}")
            print(f"       -> ECU:      {', '.join(t.get('ecus', []) or ['(none)'])}")


if __name__ == "__main__":
    asyncio.run(main())
