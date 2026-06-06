import { useState, useEffect, useCallback } from "react";
import { cn } from "@/lib/utils";
import { ArrowRight, AlertTriangle, CheckCircle2, Filter, Loader2, RefreshCw } from "lucide-react";
import { traceApi } from "@/api/rest";

interface TraceItem {
  requirement_id: string;
  requirement_type: string;
  requirement_content: string;
  function_id: string;
  function_name: string;
  sc_id: string;
  sc_name: string;
  ssc_id: string;
  ssc_name: string;
  ecus: string[];
}

const TYPE_LABELS: Record<string, string> = {
  safety: "安全需求",
  functional: "功能需求",
  market: "市场需求",
  regulation: "法规要求",
  system: "系统需求",
  security: "安全需求",
};

interface TraceMatrixPanelProps {
  projectId: string;
}

export function TraceMatrixPanel({ projectId }: TraceMatrixPanelProps) {
  const [traces, setTraces] = useState<TraceItem[]>([]);
  const [orphans, setOrphans] = useState<{ layer: string; id: string; label: string }[]>([]);
  const [expandedReq, setExpandedReq] = useState<string | null>(null);
  const [showOrphans, setShowOrphans] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTraces = useCallback(async () => {
    try {
      setError(null);
      setLoading(true);
      const data = await traceApi.matrix(projectId);
      setTraces(data.traces ?? []);
      setOrphans(data.orphans ?? []);
    } catch (e: any) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => { fetchTraces(); }, [fetchTraces]);

  const grouped = new Map<string, TraceItem[]>();
  for (const t of traces) {
    const key = t.requirement_id;
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key)!.push(t);
  }

  const coveragePct = traces.length > 0
    ? Math.round((grouped.size / (grouped.size + orphans.filter(o => o.layer === "Requirement").length)) * 100)
    : 0;

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">RFLP 追溯矩阵</h2>
        <div className="flex items-center gap-3 text-xs text-muted-foreground">
          <button
            type="button"
            onClick={fetchTraces}
            className="p-1 rounded hover:bg-muted"
            title="刷新"
          >
            {loading ? <Loader2 size={12} className="animate-spin" /> : <RefreshCw size={12} />}
          </button>
          <span>{traces.length} 条追溯链</span>
          <span className="text-green-600 flex items-center gap-1">
            <CheckCircle2 size={12} /> {grouped.size} 需求已覆盖
          </span>
          {orphans.length > 0 && (
            <span className="text-amber-600 flex items-center gap-1">
              <AlertTriangle size={12} /> {orphans.length} 个孤立项
            </span>
          )}
        </div>
      </div>

      {error && (
        <div className="mb-3 text-xs text-red-600 bg-red-50 border border-red-200 rounded px-3 py-2">
          {error}
          <button type="button" onClick={() => setError(null)} className="ml-2 text-red-400 hover:text-red-700">&times;</button>
        </div>
      )}

      {showOrphans && orphans.length > 0 && (
        <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg">
          <div className="flex items-center justify-between mb-1">
            <h3 className="text-sm font-medium text-amber-800 flex items-center gap-1">
              <AlertTriangle size={14} /> 孤立项检测
            </h3>
            <button
              type="button"
              onClick={() => setShowOrphans(false)}
              className="text-xs text-amber-600 hover:text-amber-800"
            >
              忽略
            </button>
          </div>
          <div className="space-y-1">
            {orphans.map((o) => (
              <div key={o.id} className="text-xs text-amber-700 flex items-center gap-2">
                <span className="px-1.5 py-0.5 bg-amber-200 rounded text-amber-800 font-medium">{o.layer}</span>
                {o.label}
              </div>
            ))}
          </div>
        </div>
      )}

      {loading && traces.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground">
          <Loader2 size={24} className="animate-spin mr-2" /> 加载追溯数据...
        </div>
      ) : traces.length === 0 ? (
        <div className="flex-1 flex items-center justify-center text-muted-foreground text-sm">
          暂无追溯数据，请先创建需求和功能。
        </div>
      ) : (
        <div className="flex-1 overflow-auto border border-border rounded-lg">
          <table className="w-full text-sm">
            <thead className="bg-muted/50 sticky top-0">
              <tr className="border-b border-border">
                <th className="text-left px-3 py-2 font-medium text-muted-foreground w-8"></th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground">R: 需求</th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground w-6"></th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground">F: 功能</th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground w-6"></th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground">L: 逻辑 (SC/SSC)</th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground w-6"></th>
                <th className="text-left px-3 py-2 font-medium text-muted-foreground">P: 物理 (ECU)</th>
              </tr>
            </thead>
            <tbody>
              {Array.from(grouped.entries()).map(([reqId, traceItems]) => {
                const first = traceItems[0];
                const isExpanded = expandedReq === reqId;
                return (
                  <>
                    <tr
                      key={reqId}
                      className="border-b border-border hover:bg-muted/20 cursor-pointer transition-colors"
                      onClick={() => setExpandedReq(isExpanded ? null : reqId)}
                    >
                      <td className="px-3 py-2">
                        <span className="text-xs text-muted-foreground">{isExpanded ? "−" : "+"}</span>
                      </td>
                      <td className="px-3 py-2">
                        <span className={cn("text-xs px-1.5 py-0.5 rounded", "bg-blue-100 text-blue-700")}>
                          {TYPE_LABELS[first.requirement_type] ?? first.requirement_type}
                        </span>
                        <span className="ml-2">{first.requirement_content.slice(0, 40)}{first.requirement_content.length > 40 ? "..." : ""}</span>
                      </td>
                      <td className="px-1 py-2 text-muted-foreground"><ArrowRight size={14} /></td>
                      <td className="px-3 py-2 font-medium">{first.function_name}</td>
                      <td className="px-1 py-2 text-muted-foreground"><ArrowRight size={14} /></td>
                      <td className="px-3 py-2">
                        <div className="font-medium">{first.sc_name}</div>
                        <div className="text-xs text-muted-foreground">
                          {traceItems.map((t) => t.ssc_name).join(", ")}
                        </div>
                      </td>
                      <td className="px-1 py-2 text-muted-foreground"><ArrowRight size={14} /></td>
                      <td className="px-3 py-2 text-xs">
                        {traceItems[0].ecus.join(", ")}
                      </td>
                    </tr>
                    {isExpanded && traceItems.map((t, i) => (
                      <tr key={`${reqId}-${i}`} className="border-b border-border bg-muted/10">
                        <td colSpan={8} className="px-8 py-2 text-xs">
                          <div className="flex items-center gap-6 text-muted-foreground">
                            <span>Req: <span className="font-mono">{t.requirement_id}</span></span>
                            <span>Func: <span className="font-mono">{t.function_id}</span></span>
                            <span>SC: <span className="font-mono">{t.sc_id}</span></span>
                            <span>SSC: <span className="font-mono">{t.ssc_id}</span></span>
                            <span>信号数: {t.ecus.length}</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {traces.length > 0 && (
        <div className="mt-4 border-t border-border pt-3">
          <div className="flex items-center gap-4 text-xs text-muted-foreground">
            <span className="flex items-center gap-1"><Filter size={12} /> 覆盖率:</span>
            <div className="flex-1 h-2 bg-muted rounded-full overflow-hidden flex">
              <div className="h-full bg-green-500 rounded-l-full" style={{ width: `${coveragePct}%` }} title="已覆盖" />
              <div className="h-full bg-amber-400" style={{ width: `${Math.min(100 - coveragePct, 12)}%` }} title="部分覆盖" />
              <div className="h-full bg-red-400 rounded-r-full" style={{ width: `${Math.max(100 - coveragePct - 12, 0)}%` }} title="未覆盖" />
            </div>
            <span>{coveragePct}% 完整 | {orphans.length} 个孤立项</span>
          </div>
        </div>
      )}
    </div>
  );
}
