import { useState } from "react";
import { useQuery } from "@apollo/client";
import { GET_TAGS } from "@/graphql/operations";
import { useProjectStore } from "@/stores/project";
import { cn } from "@/lib/utils";
import { demoTags } from "@/lib/demoData";
import {
  FileText,
  GitBranch,
  Layers,
  Cpu,
  Tags,
  Archive,
  ChevronDown,
  ChevronRight,
  Network,
} from "lucide-react";

const views = [
  { id: "requirements", label: "需求 (R)", icon: FileText },
  { id: "functional", label: "功能 (F)", icon: GitBranch },
  { id: "logical", label: "逻辑 (L)", icon: Layers },
  { id: "physical", label: "物理 (P)", icon: Cpu },
  { id: "ple", label: "PLE 标签/变体", icon: Tags },
  { id: "baselines", label: "基线管理", icon: Archive },
  { id: "trace", label: "追溯矩阵", icon: Network },
] as const;

interface TagItem {
  id: string;
  level: number;
  name: string;
  description: string | null;
  parentTagId: string | null;
}

function TagTreeItem({ tag, children, depth }: { tag: TagItem; children: TagItem[]; depth: number }) {
  const [open, setOpen] = useState(depth < 1);
  if (children.length === 0) {
    return (
      <div className="text-xs text-muted-foreground py-0.5 truncate" style={{ paddingLeft: `${depth * 12 + 8}px` }} title={tag.name}>
        {tag.name}
      </div>
    );
  }
  return (
    <div>
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center gap-0.5 text-xs text-muted-foreground py-0.5 hover:text-foreground w-full text-left"
        style={{ paddingLeft: `${depth * 12 + 4}px` }}
      >
        {open ? <ChevronDown size={12} /> : <ChevronRight size={12} />}
        <span className="truncate">{tag.name}</span>
      </button>
      {open && children.map((c) => (
        <TagTreeItem key={c.id} tag={c} children={[]} depth={depth + 1} />
      ))}
    </div>
  );
}

function buildSidebarTree(tags: TagItem[]) {
  const map = new Map<string, { tag: TagItem; children: TagItem[] }>();
  const roots: TagItem[] = [];

  for (const t of tags) {
    map.set(t.id, { tag: t, children: [] });
  }
  for (const entry of map.values()) {
    if (entry.tag.parentTagId && map.has(entry.tag.parentTagId)) {
      map.get(entry.tag.parentTagId)!.children.push(entry.tag);
    } else {
      roots.push(entry.tag);
    }
  }
  return { map, roots };
}

export function Sidebar() {
  const projectId = useProjectStore((s) => s.activeProjectId);
  const activeView = useProjectStore((s) => s.activeView);
  const setActiveView = useProjectStore((s) => s.setActiveView);
  const { data } = useQuery(GET_TAGS, {
    variables: { projectId },
    skip: !projectId,
    fetchPolicy: "cache-and-network",
  });

  const tags: TagItem[] = (!!projectId && data?.tags) ? data.tags : demoTags;
  const { map, roots } = buildSidebarTree(tags);

  return (
    <aside className="w-64 border-r border-border bg-muted/30 flex flex-col">
      <div className="p-4 border-b border-border">
        <h2 className="font-semibold text-sm">RFLP 导航</h2>
      </div>
      <nav className="p-2 space-y-1">
        {views.map((v) => (
          <button
            type="button"
            key={v.id}
            onClick={() => setActiveView(v.id)}
            className={cn(
              "w-full flex items-center gap-2 px-3 py-2 rounded-md text-sm transition-colors",
              activeView === v.id
                ? "bg-primary text-primary-foreground"
                : "hover:bg-muted text-muted-foreground",
            )}
          >
            <v.icon size={16} />
            {v.label}
          </button>
        ))}
      </nav>
      <div className="p-4 border-t border-border flex-1 overflow-y-auto">
        <h3 className="text-xs font-semibold text-muted-foreground mb-2">
          标签层级 ({tags.length})
        </h3>
        <div className="space-y-0.5">
          {roots.map((t) => (
            <TagTreeItem key={t.id} tag={t} children={map.get(t.id)?.children ?? []} depth={0} />
          ))}
        </div>
      </div>
    </aside>
  );
}
