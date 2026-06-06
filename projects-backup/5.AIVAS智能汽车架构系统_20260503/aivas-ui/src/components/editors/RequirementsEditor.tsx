import { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { GET_REQUIREMENTS, CREATE_REQUIREMENT } from "@/graphql/operations";
import { useProjectStore } from "@/stores/project";
import { cn } from "@/lib/utils";
import { demoRequirements, genDemoId } from "@/lib/demoData";
import { Trash2, Edit3, Check, X } from "lucide-react";

const REQ_TYPES = [
  { value: "market", label: "市场需求", color: "bg-blue-100 text-blue-800" },
  { value: "functional", label: "服务及功能需求", color: "bg-green-100 text-green-800" },
  { value: "system", label: "系统功能需求", color: "bg-purple-100 text-purple-800" },
  { value: "regulation", label: "法规标准要求", color: "bg-amber-100 text-amber-800" },
  { value: "safety", label: "安全需求", color: "bg-red-100 text-red-800" },
  { value: "security", label: "网络安全需求", color: "bg-orange-100 text-orange-800" },
];

interface ReqItem {
  id: string;
  type: string;
  content: string;
  version: number;
  tagId: string | null;
  parentReqId: string | null;
}

export function RequirementsEditor() {
  const projectId = useProjectStore((s) => s.activeProjectId);
  const [filterType, setFilterType] = useState<string | null>(null);
  const [newContent, setNewContent] = useState("");
  const [newType, setNewType] = useState("functional");
  const [localReqs, setLocalReqs] = useState<ReqItem[]>(demoRequirements);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState("");
  const [editType, setEditType] = useState("");

  const { data, refetch } = useQuery(GET_REQUIREMENTS, {
    variables: { projectId, type: filterType },
    skip: !projectId,
    fetchPolicy: "cache-and-network",
  });
  const [createReq] = useMutation(CREATE_REQUIREMENT);

  const hasBackend = !!projectId && !!data?.requirements;
  const requirements: ReqItem[] = hasBackend ? data.requirements : localReqs;
  const filtered = filterType ? requirements.filter((r) => r.type === filterType) : requirements;

  const handleCreate = async () => {
    if (!newContent.trim()) return;
    if (projectId) {
      await createReq({ variables: { projectId, input: { type: newType, content: newContent.trim() } } });
      refetch();
    } else {
      setLocalReqs([{ id: genDemoId(), type: newType, content: newContent.trim(), version: 1, tagId: null, parentReqId: null }, ...localReqs]);
    }
    setNewContent("");
  };

  const handleDelete = (id: string) => {
    setLocalReqs((prev) => prev.filter((r) => r.id !== id));
  };

  const startEdit = (r: ReqItem) => {
    setEditingId(r.id);
    setEditContent(r.content);
    setEditType(r.type);
  };

  const saveEdit = () => {
    if (!editingId) return;
    setLocalReqs((prev) =>
      prev.map((r) =>
        r.id === editingId ? { ...r, content: editContent, type: editType, version: r.version + 1 } : r,
      ),
    );
    setEditingId(null);
  };

  const cancelEdit = () => setEditingId(null);

  return (
    <div className="h-full flex flex-col p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold">需求管理 (Requirement)</h2>
        <span className="text-xs text-muted-foreground">{requirements.length} 条需求</span>
      </div>

      <div className="flex gap-2 mb-4 flex-wrap">
        <button
          type="button"
          onClick={() => setFilterType(null)}
          className={cn("px-3 py-1 text-xs rounded-full transition-colors", !filterType ? "bg-slate-800 text-white" : "bg-muted hover:bg-slate-100")}
        >
          全部
        </button>
        {REQ_TYPES.map((t) => (
          <button
            type="button"
            key={t.value}
            onClick={() => setFilterType(t.value)}
            className={cn("px-3 py-1 text-xs rounded-full transition-colors", filterType === t.value ? "bg-slate-800 text-white" : cn(t.color, "hover:opacity-80"))}
          >
            {t.label}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-y-auto space-y-2 mb-4">
        {filtered.length === 0 ? (
          <div className="text-center text-muted-foreground py-16">
            <p className="text-sm">暂无需求条目</p>
            <p className="text-xs mt-1">在下方输入框中创建新的需求</p>
          </div>
        ) : (
          filtered.map((r) => {
            const isEditing = editingId === r.id;
            const typeInfo = REQ_TYPES.find((t) => t.value === r.type);
            return (
              <div key={r.id} className="border border-border rounded-lg p-3 bg-white group hover:border-primary/30 transition-colors">
                {isEditing ? (
                  <div className="space-y-2">
                    <select
                      value={editType}
                      onChange={(e) => setEditType(e.target.value)}
                      className="text-sm border border-border rounded-md px-2 py-1 bg-background"
                    >
                      {REQ_TYPES.map((t) => (
                        <option key={t.value} value={t.value}>{t.label}</option>
                      ))}
                    </select>
                    <textarea
                      value={editContent}
                      onChange={(e) => setEditContent(e.target.value)}
                      className="w-full text-sm border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary resize-none"
                      rows={3}
                    />
                    <div className="flex gap-2 justify-end">
                      <button type="button" onClick={saveEdit} className="flex items-center gap-1 px-2 py-1 text-xs rounded bg-primary text-primary-foreground hover:bg-primary/90">
                        <Check size={12} /> 保存
                      </button>
                      <button type="button" onClick={cancelEdit} className="flex items-center gap-1 px-2 py-1 text-xs rounded bg-muted hover:bg-slate-200">
                        <X size={12} /> 取消
                      </button>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="flex items-center gap-2 mb-1">
                      <span className={cn("text-xs px-2 py-0.5 rounded", typeInfo?.color)}>
                        {typeInfo?.label ?? r.type}
                      </span>
                      <span className="text-xs text-muted-foreground">v{r.version}</span>
                      <div className="ml-auto flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all">
                        <button
                          type="button"
                          onClick={() => startEdit(r)}
                          className="p-1 rounded hover:bg-blue-50 text-blue-500"
                          title="编辑"
                        >
                          <Edit3 size={14} />
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(r.id)}
                          className="p-1 rounded hover:bg-red-50 text-red-400 hover:text-red-600"
                          title="删除"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                    <p className="text-sm">{r.content}</p>
                  </>
                )}
              </div>
            );
          })
        )}
      </div>

      <div className="border-t border-border pt-4 flex gap-2">
        <select
          value={newType}
          onChange={(e) => setNewType(e.target.value)}
          className="text-sm border border-border rounded-md px-2 py-2 bg-background"
        >
          {REQ_TYPES.map((t) => (
            <option key={t.value} value={t.value}>{t.label}</option>
          ))}
        </select>
        <input
          type="text"
          value={newContent}
          onChange={(e) => setNewContent(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleCreate()}
          placeholder="输入新需求..."
          className="flex-1 text-sm border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary"
        />
        <button
          type="button"
          onClick={handleCreate}
          className="px-4 py-2 bg-primary text-primary-foreground text-sm rounded-md hover:bg-primary/90 disabled:opacity-50"
          disabled={!newContent.trim()}
        >
          添加
        </button>
      </div>
    </div>
  );
}
