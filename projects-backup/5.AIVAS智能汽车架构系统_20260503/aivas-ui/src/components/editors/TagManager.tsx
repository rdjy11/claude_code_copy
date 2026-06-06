import { useState } from "react";
import { useQuery, useMutation } from "@apollo/client";
import { GET_TAGS, CREATE_TAG } from "@/graphql/operations";
import { useProjectStore } from "@/stores/project";
import { cn } from "@/lib/utils";
import { demoTags, genDemoId } from "@/lib/demoData";
import { Trash2, ChevronRight, ChevronDown, Edit3, Check, X } from "lucide-react";

const LEVEL_LABELS: Record<number, string> = { 1: "L1 — 应用架构", 2: "L2 — 车辆平台", 3: "L3 — 基线阶段" };

interface TagItem {
  id: string;
  level: number;
  name: string;
  description: string | null;
  parentTagId: string | null;
}

interface TreeNodeData extends TagItem {
  children: TreeNodeData[];
}

function buildTagTree(tags: TagItem[]): TreeNodeData[] {
  const map = new Map<string, TreeNodeData>();
  const roots: TreeNodeData[] = [];

  for (const t of tags) {
    map.set(t.id, { ...t, children: [] });
  }
  for (const t of map.values()) {
    if (t.parentTagId && map.has(t.parentTagId)) {
      map.get(t.parentTagId)!.children.push(t);
    } else {
      roots.push(t);
    }
  }
  return roots;
}

function TreeNode({
  node, depth, onDelete, editingId, editName, editDesc, editLevel, onStartEdit, onSaveEdit, onCancelEdit, onEditNameChange, onEditDescChange, onEditLevelChange,
}: {
  node: TreeNodeData;
  depth: number;
  onDelete: (id: string) => void;
  editingId: string | null;
  editName: string;
  editDesc: string;
  editLevel: number;
  onStartEdit: (t: TagItem) => void;
  onSaveEdit: () => void;
  onCancelEdit: () => void;
  onEditNameChange: (v: string) => void;
  onEditDescChange: (v: string) => void;
  onEditLevelChange: (v: number) => void;
}) {
  const [open, setOpen] = useState(true);
  const hasChildren = node.children.length > 0;
  const isEditing = editingId === node.id;

  return (
    <div>
      <div
        className="flex items-center gap-1 py-1 px-2 rounded hover:bg-muted/50 group text-sm"
        style={{ paddingLeft: `${depth * 16 + 8}px` }}
      >
        {hasChildren ? (
          <button type="button" onClick={() => setOpen(!open)} className="p-0.5 text-muted-foreground">
            {open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
          </button>
        ) : (
          <span className="w-5" />
        )}
        {isEditing ? (
          <div className="flex items-center gap-1 flex-1">
            <select
              value={editLevel}
              onChange={(e) => onEditLevelChange(Number(e.target.value))}
              className="text-xs border border-border rounded px-1 py-0.5 bg-background"
            >
              <option value={1}>L1</option>
              <option value={2}>L2</option>
              <option value={3}>L3</option>
            </select>
            <input
              type="text"
              value={editName}
              onChange={(e) => onEditNameChange(e.target.value)}
              className="flex-1 text-sm border border-border rounded px-2 py-0.5 focus:outline-none focus:border-primary"
            />
            <input
              type="text"
              value={editDesc}
              onChange={(e) => onEditDescChange(e.target.value)}
              placeholder="描述"
              className="w-32 text-xs border border-border rounded px-2 py-0.5 focus:outline-none focus:border-primary hidden sm:block"
            />
            <button type="button" onClick={onSaveEdit} className="p-0.5 rounded text-green-500 hover:bg-green-50"><Check size={12} /></button>
            <button type="button" onClick={onCancelEdit} className="p-0.5 rounded text-red-400 hover:bg-red-50"><X size={12} /></button>
          </div>
        ) : (
          <>
            <span className={cn("text-xs px-1.5 py-0.5 rounded font-medium", depth === 0 ? "bg-blue-100 text-blue-700" : depth === 1 ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700")}>
              L{node.level}
            </span>
            <span className="flex-1">{node.name}</span>
            {node.description && (
              <span className="text-xs text-muted-foreground hidden sm:inline">{node.description}</span>
            )}
            <div className="flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-all">
              <button
                type="button"
                onClick={() => onStartEdit(node)}
                className="p-0.5 rounded hover:bg-blue-50 text-blue-500"
                title="编辑"
              >
                <Edit3 size={12} />
              </button>
              <button
                type="button"
                onClick={() => onDelete(node.id)}
                className="p-0.5 rounded hover:bg-red-50 text-red-400 hover:text-red-600"
                title="删除"
              >
                <Trash2 size={12} />
              </button>
            </div>
          </>
        )}
      </div>
      {open && hasChildren && node.children.map((child) => (
        <TreeNode key={child.id} node={child} depth={depth + 1} onDelete={onDelete} editingId={editingId} editName={editName} editDesc={editDesc} editLevel={editLevel} onStartEdit={onStartEdit} onSaveEdit={onSaveEdit} onCancelEdit={onCancelEdit} onEditNameChange={onEditNameChange} onEditDescChange={onEditDescChange} onEditLevelChange={onEditLevelChange} />
      ))}
    </div>
  );
}

export function TagManager() {
  const projectId = useProjectStore((s) => s.activeProjectId);
  const [newName, setNewName] = useState("");
  const [newLevel, setNewLevel] = useState(1);
  const [newParentId, setNewParentId] = useState<string | null>(null);
  const [newDesc, setNewDesc] = useState("");
  const [localTags, setLocalTags] = useState<TagItem[]>(demoTags);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editName, setEditName] = useState("");
  const [editDesc, setEditDesc] = useState("");
  const [editLevel, setEditLevel] = useState(1);

  const { data, refetch } = useQuery(GET_TAGS, {
    variables: { projectId },
    skip: !projectId,
    fetchPolicy: "cache-and-network",
  });
  const [createTag] = useMutation(CREATE_TAG);

  const hasBackend = !!projectId && !!data?.tags;
  const tags: TagItem[] = hasBackend ? data.tags : localTags;
  const tree = buildTagTree(tags);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    if (projectId) {
      await createTag({
        variables: { projectId, input: { level: newLevel, name: newName.trim(), parentTagId: newParentId, description: newDesc || null } },
      });
      refetch();
    } else {
      setLocalTags([
        ...localTags,
        { id: genDemoId(), level: newLevel, name: newName.trim(), description: newDesc || null, parentTagId: newParentId },
      ]);
    }
    setNewName("");
    setNewDesc("");
  };

  const handleDelete = (id: string) => {
    setLocalTags((prev) => prev.filter((t) => t.id !== id && t.parentTagId !== id));
  };

  const startEdit = (t: TagItem) => {
    setEditingId(t.id);
    setEditName(t.name);
    setEditDesc(t.description ?? "");
    setEditLevel(t.level);
  };

  const saveEdit = () => {
    if (!editingId || !editName.trim()) return;
    setLocalTags((prev) =>
      prev.map((t) =>
        t.id === editingId ? { ...t, name: editName.trim(), description: editDesc || null, level: editLevel } : t,
      ),
    );
    setEditingId(null);
  };

  const cancelEdit = () => setEditingId(null);

  const eligibleParents = tags.filter((t) => t.level < newLevel);

  return (
    <div className="h-full flex p-6 gap-6">
      <div className="flex-1 overflow-y-auto">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">三级标签体系</h2>
          <span className="text-xs text-muted-foreground">{tags.length} 个标签</span>
        </div>
        {[1, 2, 3].map((level) => {
          const levelTags = tags.filter((t) => t.level === level);
          return (
            <div key={level} className="mb-4">
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {LEVEL_LABELS[level]} ({levelTags.length})
              </h3>
              <div className="border border-border rounded-lg bg-white overflow-hidden">
                {tree.length === 0 ? (
                  <div className="p-4 text-xs text-muted-foreground text-center">暂无标签</div>
                ) : (
                  <div className="py-1">
                    {tree.map((node) => (
                      <TreeNode key={node.id} node={node} depth={0} onDelete={handleDelete} editingId={editingId} editName={editName} editDesc={editDesc} editLevel={editLevel} onStartEdit={startEdit} onSaveEdit={saveEdit} onCancelEdit={cancelEdit} onEditNameChange={setEditName} onEditDescChange={setEditDesc} onEditLevelChange={setEditLevel} />
                    ))}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <div className="w-72 border-l border-border pl-6">
        <h3 className="text-sm font-semibold mb-3">创建标签</h3>
        <div className="space-y-3">
          <div>
            <label className="text-xs text-muted-foreground">层级</label>
            <select
              value={newLevel}
              onChange={(e) => { setNewLevel(Number(e.target.value)); setNewParentId(null); }}
              className="w-full text-sm border border-border rounded-md px-2 py-2 mt-1 bg-background"
            >
              <option value={1}>L1 — 应用架构</option>
              <option value={2}>L2 — 车辆平台</option>
              <option value={3}>L3 — 基线阶段</option>
            </select>
          </div>
          <div>
            <label className="text-xs text-muted-foreground">父标签（可选）</label>
            <select
              value={newParentId ?? ""}
              onChange={(e) => setNewParentId(e.target.value || null)}
              className="w-full text-sm border border-border rounded-md px-2 py-2 mt-1 bg-background"
            >
              <option value="">无（顶层标签）</option>
              {eligibleParents.map((t) => (
                <option key={t.id} value={t.id}>
                  L{t.level}: {t.name}
                </option>
              ))}
            </select>
          </div>
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCreate()}
            placeholder="标签名称 *"
            className="w-full text-sm border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary"
          />
          <input
            type="text"
            value={newDesc}
            onChange={(e) => setNewDesc(e.target.value)}
            placeholder="描述（可选）"
            className="w-full text-sm border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary"
          />
          <button
            type="button"
            onClick={handleCreate}
            disabled={!newName.trim()}
            className={cn(
              "w-full py-2 rounded-md text-sm font-medium transition-colors",
              newName.trim() ? "bg-primary text-primary-foreground hover:bg-primary/90" : "bg-slate-200 text-slate-400 cursor-not-allowed",
            )}
          >
            创建标签
          </button>
        </div>
      </div>
    </div>
  );
}
