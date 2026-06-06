import { useQuery } from "@apollo/client";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  useNodesState,
  useEdgesState,
  BackgroundVariant,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import { GET_DIAGRAM } from "../../graphql/operations";
import { useProjectStore } from "../../stores/project";

interface DiagramCanvasProps {
  diagramType: "BDD" | "IBD" | "Topology";
}

interface ApiNode {
  id: string;
  type: string;
  data_label: string;
  data_description: string | null;
  position_x: number;
  position_y: number;
}

interface ApiEdge {
  id: string;
  source: string;
  target: string;
  animated: boolean;
  label: string | null;
}

function apiToFlowNodes(nodes: ApiNode[]): Node[] {
  return nodes.map((n) => ({
    id: n.id,
    type: n.type,
    position: { x: n.position_x, y: n.position_y },
    data: { label: n.data_label + (n.data_description ? `\n${n.data_description}` : "") },
  }));
}

function apiToFlowEdges(edges: ApiEdge[]): Edge[] {
  return edges.map((e) => ({
    id: e.id,
    source: e.source,
    target: e.target,
    animated: e.animated,
    label: e.label ?? undefined,
  }));
}

export function DiagramCanvas({ diagramType }: DiagramCanvasProps) {
  const projectId = useProjectStore((s) => s.activeProjectId);

  const { data, loading, error } = useQuery(GET_DIAGRAM, {
    variables: { projectId: projectId ?? "", diagramType },
    skip: !projectId,
    fetchPolicy: "cache-and-network",
  });

  const apiNodes: ApiNode[] = data?.diagram?.nodes ?? [];
  const apiEdges: ApiEdge[] = data?.diagram?.edges ?? [];

  const [nodes, , onNodesChange] = useNodesState(apiToFlowNodes(apiNodes));
  const [edges, , onEdgesChange] = useEdgesState(apiToFlowEdges(apiEdges));

  const title =
    diagramType === "BDD"
      ? "BDD: 顶层模块定义"
      : diagramType === "IBD"
        ? "IBD: SC-SSC 子系统分解"
        : "网络拓扑与 ECU 分配";

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b border-border">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="text-xs text-muted-foreground mt-1">
          拖拽节点编辑布局 | 双击节点编辑属性 | 滚动缩放
          {!projectId && (
            <span className="text-amber-500 ml-2">请先选择项目</span>
          )}
          {loading && (
            <span className="text-blue-400 ml-2">加载中...</span>
          )}
          {error && (
            <span className="text-red-400 ml-2">加载失败: {error.message}</span>
          )}
          {projectId && !loading && !error && apiNodes.length === 0 && (
            <span className="text-muted-foreground ml-2">暂无数据，请先创建功能/SC/ECU</span>
          )}
        </p>
      </div>
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          fitView
          attributionPosition="bottom-left"
        >
          <Background variant={BackgroundVariant.Dots} gap={20} size={1} />
          <Controls />
          <MiniMap
            nodeStrokeWidth={2}
            pannable
            zoomable
            style={{ height: 120 }}
          />
        </ReactFlow>
      </div>
    </div>
  );
}
