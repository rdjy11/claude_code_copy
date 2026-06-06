import { useQuery } from "@apollo/client";
import { useProjectStore } from "@/stores/project";
import { useAgentStore } from "@/stores/agent";
import { GET_RFLP_SUMMARY } from "@/graphql/operations";
import { demoRFLPSummary } from "@/lib/demoData";

const VIEW_LABELS: Record<string, string> = {
  requirements: "需求 (R)",
  functional: "功能 (F)",
  logical: "逻辑 (L)",
  physical: "物理 (P)",
  ple: "PLE 标签/变体",
  baselines: "基线管理",
  trace: "RFLP 追溯矩阵",
};

export function StatusBar() {
  const activeView = useProjectStore((s) => s.activeView);
  const projectId = useProjectStore((s) => s.activeProjectId);
  const messageCount = useAgentStore((s) => s.messages.length);

  const { data } = useQuery(GET_RFLP_SUMMARY, {
    variables: { projectId: projectId ?? "" },
    skip: !projectId,
    fetchPolicy: "cache-and-network",
  });

  const summary = data?.rflpSummary ?? demoRFLPSummary;

  return (
    <div className="h-8 border-t border-border bg-muted/50 flex items-center px-4 text-xs text-muted-foreground gap-4">
      <span className="font-medium">AIVAS v0.1.0</span>
      <span>视图: {VIEW_LABELS[activeView] ?? activeView}</span>
      <span className="text-muted-foreground/60">|</span>
      <span title="需求 / 功能 / SC / SSC / ECU">
        R:{summary.requirements} F:{summary.functions} L:{summary.scs}/{summary.sscs} P:{summary.ecus}
      </span>
      <span className="text-muted-foreground/60">|</span>
      <span>对话: {messageCount} 条</span>
      <span className="ml-auto">MBSE + PLE | AI-Native</span>
    </div>
  );
}
