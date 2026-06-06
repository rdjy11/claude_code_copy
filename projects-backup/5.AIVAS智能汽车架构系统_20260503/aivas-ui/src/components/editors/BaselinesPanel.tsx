import { useState, useEffect, useCallback } from "react";
import { cn } from "@/lib/utils";
import { Lock, GitCompare, Plus, Archive, Loader2, RefreshCw } from "lucide-react";
import { baselineApi } from "@/api/rest";

interface BaselineItem {
  id: string;
  project_id: string;
  name: string;
  status: string;
  tag_id: string | null;
  locked_at: string | null;
  created_at: string;
  updated_at: string;
}

const STATUS_MAP: Record<string, { label: string; color: string }> = {
  draft: { label: "草稿", color: "bg-amber-100 text-amber-700" },
  locked: { label: "已锁定", color: "bg-blue-100 text-blue-700" },
  released: { label: "已发布", color: "bg-green-100 text-green-700" },
};

interface BaselinesPanelProps {
  projectId: string;
}

export function BaselinesPanel({ projectId }: BaselinesPanelProps) {
  const [baselines, setBaselines] = useState<BaselineItem[]>([]);
  const [showCreate, setShowCreate] = useState(false);
  const [newName, setNewName] = useState("");
  const [diffTarget, setDiffTarget] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBaselines = useCallback(async () => {
    try {
      setError(null);
      const data = await baselineApi.list(projectId);
      setBaselines(data);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => { fetchBaselines(); }, [fetchBaselines]);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    try {
      setError(null);
      const created = await baselineApi.create(projectId, { name: newName.trim() });
      setBaselines([created, ...baselines]);
      setNewName("");
      setShowCreate(false);
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleLock = async (id: string) => {
    try {
      const updated = await baselineApi.update(id, { status: "locked" });
      setBaselines((prev) => prev.map((b) => (b.id === id ? updated : b)));
    } catch (e: any) {
      setError(e.message);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await baselineApi.delete(id);
      setBaselines((prev) => prev.filter((b) => b.id !== id));
    } catch (e: any) {
      setError(e.message);
    }
  };

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">基线管理 (Baselines)</h2>
        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={fetchBaselines}
            className="p-1.5 rounded hover:bg-muted text-muted-foreground"
            title="刷新"
          >
            {loading ? <Loader2 size={14} className="animate-spin" /> : <RefreshCw size={14} />}
          </button>
          <button
            type="button"
            onClick={() => setShowCreate(!showCreate)}
            className="flex items-center gap-1 px-3 py-1.5 text-sm rounded-md bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <Plus size={14} /> 新建基线
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-3 text-xs text-red-600 bg-red-50 border border-red-200 rounded px-3 py-2">
          {error}
          <button type="button" onClick={() => setError(null)} className="ml-2 text-red-400 hover:text-red-700">&times;</button>
        </div>
      )}

      {showCreate && (
        <div className="flex gap-2 mb-4 p-3 border border-border rounded-lg bg-muted/30">
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCreate()}
            placeholder="基线名称，如 BL_中国市场豪华BEV_SOP2026Q2"
            className="flex-1 text-sm border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary"
          />
          <button
            type="button"
            onClick={handleCreate}
            className="px-4 py-2 bg-primary text-primary-foreground text-sm rounded-md"
          >
            创建
          </button>
          <button
            type="button"
            onClick={() => setShowCreate(false)}
            className="px-3 py-2 text-sm text-muted-foreground"
          >
            取消
          </button>
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        {baselines.length === 0 && !loading ? (
          <div className="text-center text-muted-foreground py-16">
            <Archive size={32} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm">暂无基线</p>
            <p className="text-xs mt-1">创建基线以冻结特定变体的架构状态</p>
          </div>
        ) : (
          <div className="space-y-3">
            {baselines.map((bl) => {
              const statusInfo = STATUS_MAP[bl.status] ?? STATUS_MAP.draft;
              return (
                <div
                  key={bl.id}
                  className={cn(
                    "border border-border rounded-lg p-4 bg-white",
                    diffTarget === bl.id && "ring-2 ring-primary",
                  )}
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-3">
                      <Archive size={18} className="text-muted-foreground" />
                      <span className="font-medium text-sm">{bl.name}</span>
                      <span className={cn("text-xs px-2 py-0.5 rounded-full", statusInfo.color)}>
                        {statusInfo.label}
                      </span>
                    </div>
                    <div className="flex items-center gap-1">
                      {bl.status === "draft" && (
                        <button
                          type="button"
                          onClick={() => handleLock(bl.id)}
                          className="p-1.5 rounded hover:bg-blue-50 text-blue-600"
                          title="锁定基线"
                        >
                          <Lock size={14} />
                        </button>
                      )}
                      <button
                        type="button"
                        onClick={() => setDiffTarget(diffTarget === bl.id ? null : bl.id)}
                        className={cn("p-1.5 rounded hover:bg-muted", diffTarget === bl.id && "bg-primary/10 text-primary")}
                        title="对比差异"
                      >
                        <GitCompare size={14} />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleDelete(bl.id)}
                        className="p-1.5 rounded hover:bg-red-50 text-red-500"
                        title="删除基线"
                      >
                        <span className="text-xs">删除</span>
                      </button>
                    </div>
                  </div>
                  <div className="flex gap-4 text-xs text-muted-foreground">
                    <span>状态: {bl.status}</span>
                    <span>创建: {new Date(bl.created_at).toLocaleDateString("zh-CN")}</span>
                    {bl.tag_id && <span>关联标签: {bl.tag_id}</span>}
                  </div>
                  {diffTarget === bl.id && (
                    <div className="mt-3 p-3 bg-muted/30 rounded-md text-xs">
                      <p className="font-medium mb-1">基线对比 (当前 vs 冻结)</p>
                      <p className="text-muted-foreground mt-1">对比功能将在接入后端后完整展示。</p>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
