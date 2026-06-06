export const demoRequirements = [
  { id: "req-001", type: "safety", content: "ADAS 系统须满足 ISO 26262 ASIL D 功能安全等级要求", version: 3, tagId: null, parentReqId: null },
  { id: "req-002", type: "functional", content: "车辆须支持 L3 级自动驾驶，含高速公路自动变道和匝道汇入", version: 2, tagId: null, parentReqId: null },
  { id: "req-003", type: "market", content: "中国市场车型须集成微信车载版和高德地图 AR 导航", version: 1, tagId: null, parentReqId: null },
  { id: "req-004", type: "regulation", content: "须满足 UN R155 网络安全法规和 UN R156 软件更新法规要求", version: 2, tagId: null, parentReqId: null },
  { id: "req-005", type: "system", content: "OTA 系统须支持差分升级，单次升级包 ≤ 500MB，升级成功率 ≥ 99.5%", version: 1, tagId: null, parentReqId: null },
  { id: "req-006", type: "security", content: "车内 CAN-FD / Ethernet 通信须支持 SecOC 安全板载通信机制", version: 2, tagId: null, parentReqId: null },
];

export const demoTags = [
  { id: "tag-001", level: 1, name: "中国市场", description: "中国本土市场车型", parentTagId: null },
  { id: "tag-002", level: 1, name: "欧洲市场", description: "欧洲出口车型", parentTagId: null },
  { id: "tag-003", level: 1, name: "北美市场", description: "北美出口车型", parentTagId: null },
  { id: "tag-004", level: 2, name: "豪华版", description: "顶配豪华版", parentTagId: "tag-001" },
  { id: "tag-005", level: 2, name: "舒适版", description: "中配舒适版", parentTagId: "tag-001" },
  { id: "tag-006", level: 2, name: "入门版", description: "低配入门版", parentTagId: "tag-001" },
  { id: "tag-007", level: 3, name: "纯电BEV", description: "纯电动力总成", parentTagId: "tag-004" },
  { id: "tag-008", level: 3, name: "混动PHEV", description: "插电混动总成", parentTagId: "tag-004" },
  { id: "tag-009", level: 3, name: "SOP-2026Q3", description: "2026年Q3 SOP基线", parentTagId: "tag-007" },
];

export const demoBaselines = [
  { id: "bl-001", name: "BL_中国市场豪华BEV_SOP2026Q2", status: "locked", tagId: "tag-008", itemCount: 47, createdAt: "2026-04-15" },
  { id: "bl-002", name: "BL_中国市场舒适PHEV_SOP2026Q3", status: "draft", tagId: "tag-009", itemCount: 32, createdAt: "2026-04-28" },
  { id: "bl-003", name: "BL_欧洲市场豪华BEV_SOP2026Q3", status: "draft", tagId: null, itemCount: 28, createdAt: "2026-05-01" },
];

export const demoRFLPSummary = {
  projectId: "demo",
  requirements: 6,
  functions: 8,
  scs: 5,
  sscs: 14,
  ecus: 9,
  orphanFunctions: 1,
  orphanScs: 2,
};

export const demoProjects = [
  { id: "proj-demo-001", name: "NEA Platform Gen2 — 智能电动架构平台", description: "第二代新能源智能架构平台，支持 BEV/PHEV/ICE 多动力总成，面向中国/欧洲/北美市场" },
  { id: "proj-demo-002", name: "City SUV 2027 — 城市SUV车型项目", description: "紧凑型城市SUV，目标2027年SOP" },
];

// Utility: generate a short UUID-like ID
let _idCounter = 100;
export function genDemoId(): string {
  return `demo-${Date.now()}-${++_idCounter}`;
}
