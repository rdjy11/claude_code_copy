import { useState } from "react";
import { cn } from "@/lib/utils";
import { Plus, X, Loader2 } from "lucide-react";
import { functionApi, scApi, sscApi, ecuApi } from "@/api/rest";

interface CreatedItem {
  id: string;
  label: string;
  detail: string;
}

interface EntityCreatorProps {
  entityType: "function" | "sc" | "ssc" | "ecu";
  projectId: string;
  parentId?: string; // sc_id for SSC, ssc_id for signal
  onCreated?: (item: CreatedItem) => void;
}

const TYPE_LABELS: Record<string, string> = {
  function: "功能模块 (Function)",
  sc: "系统组件 (SC)",
  ssc: "子系统组件 (SSC)",
  ecu: "电子控制单元 (ECU)",
};

const QUICK_OPTIONS: Record<string, string[]> = {
  function: ["感知融合", "决策规划", "车辆控制", "人机交互", "网联服务", "安全防护", "平台基础设施", "运行管理"],
  sc: ["ADAS Domain Controller", "Infotainment Controller", "Gateway Controller", "Body Domain Controller", "Powertrain Controller"],
  ecu: ["ADAS (Ethernet)", "Radar-SR (CAN-FD)", "IVI (Ethernet)", "Central Gateway (CAN-FD)", "BCM (CAN-Body)", "DCM (CAN-FD)", "HVAC (LIN)", "BMS (CAN-FD)", "EPS (CAN-FD)"],
  ssc: ["Camera Processing", "Radar Processing", "Path Planning", "Behavior Prediction", "HMI Renderer", "Audio DSP", "Navigation Engine", "Firewall", "OTA Manager", "BMS", "Motor Control", "Thermal Management"],
};

export function EntityCreator({ entityType, projectId, parentId, onCreated }: EntityCreatorProps) {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const [showQuick, setShowQuick] = useState(false);
  const [items, setItems] = useState<CreatedItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createEntity = async () => {
    if (!name.trim()) return;
    setLoading(true);
    setError(null);
    try {
      let result: any;
      const body = { name: name.trim(), description: desc.trim() || undefined };
      switch (entityType) {
        case "function":
          result = await functionApi.create(projectId, body);
          break;
        case "sc":
          result = await scApi.create(projectId, body);
          break;
        case "ssc":
          result = await sscApi.create(parentId!, body);
          break;
        case "ecu":
          result = await ecuApi.create(projectId, body);
          break;
      }
      const item = { id: result.id, label: result.name, detail: result.description ?? "" };
      setItems([item, ...items]);
      onCreated?.(item);
      setName("");
      setDesc("");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickAdd = async (label: string) => {
    setLoading(true);
    setError(null);
    try {
      let result: any;
      const body = { name: label, description: "" };
      switch (entityType) {
        case "function":
          result = await functionApi.create(projectId, body);
          break;
        case "sc":
          result = await scApi.create(projectId, body);
          break;
        case "ssc":
          result = await sscApi.create(parentId!, body);
          break;
        case "ecu":
          result = await ecuApi.create(projectId, body);
          break;
      }
      const item = { id: result.id, label: result.name, detail: result.description ?? "" };
      setItems([item, ...items]);
      onCreated?.(item);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const quickOptions = QUICK_OPTIONS[entityType];

  return (
    <div className="border-t border-border bg-muted/20 p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold">创建 {TYPE_LABELS[entityType]}</h3>
        <button
          type="button"
          onClick={() => setShowQuick(!showQuick)}
          className="text-xs text-muted-foreground hover:text-foreground"
        >
          {showQuick ? "隐藏快捷添加" : "快捷添加"}
        </button>
      </div>

      {showQuick && (
        <div className="flex flex-wrap gap-1.5 mb-3">
          {quickOptions.map((label) => (
            <button
              key={label}
              type="button"
              onClick={() => handleQuickAdd(label)}
              disabled={loading}
              className="px-2 py-1 text-xs rounded-md border border-border bg-white hover:bg-primary/5 hover:border-primary/30 transition-colors disabled:opacity-50"
            >
              <Plus size={10} className="inline mr-0.5" />
              {label}
            </button>
          ))}
        </div>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && createEntity()}
          placeholder={`${TYPE_LABELS[entityType]} 名称...`}
          disabled={loading}
          className="flex-1 text-sm border border-border rounded-md px-3 py-2 bg-white focus:outline-none focus:border-primary disabled:opacity-50"
        />
        <input
          type="text"
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          placeholder="描述/类型（可选）"
          className="w-40 text-sm border border-border rounded-md px-3 py-2 bg-white focus:outline-none focus:border-primary hidden sm:block"
        />
        <button
          type="button"
          onClick={createEntity}
          disabled={!name.trim() || loading}
          className={cn(
            "px-3 py-2 rounded-md text-sm font-medium flex items-center gap-1 transition-colors",
            name.trim() && !loading ? "bg-primary text-primary-foreground hover:bg-primary/90" : "bg-slate-200 text-slate-400 cursor-not-allowed",
          )}
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Plus size={14} />}
          创建
        </button>
      </div>

      {error && (
        <div className="mt-2 text-xs text-red-600 bg-red-50 border border-red-200 rounded px-2 py-1">
          {error}
          <button type="button" onClick={() => setError(null)} className="ml-2 text-red-400 hover:text-red-700">&times;</button>
        </div>
      )}

      {items.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {items.map((item) => (
            <span
              key={item.id}
              className="inline-flex items-center gap-1 px-2 py-0.5 text-xs rounded-full bg-primary/10 text-primary border border-primary/20"
            >
              {item.label}
              <button
                type="button"
                onClick={() => setItems(items.filter((i) => i.id !== item.id))}
                className="hover:text-red-500"
              >
                <X size={10} />
              </button>
            </span>
          ))}
          <span className="text-xs text-muted-foreground self-center">
            {items.length} 个已创建
          </span>
        </div>
      )}
    </div>
  );
}
