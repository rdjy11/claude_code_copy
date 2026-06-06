import { useProjectStore } from "@/stores/project";
import { RequirementsEditor } from "@/components/editors/RequirementsEditor";
import { TagManager } from "@/components/editors/TagManager";
import { BaselinesPanel } from "@/components/editors/BaselinesPanel";
import { TraceMatrixPanel } from "@/components/editors/TraceMatrixPanel";
import { EntityCreator } from "@/components/editors/EntityCreator";
import { DiagramCanvas } from "@/components/diagram/DiagramCanvas";

export function MainPanel() {
  const activeView = useProjectStore((s) => s.activeView);
  const projectId = useProjectStore((s) => s.activeProjectId);

  const renderView = () => {
    switch (activeView) {
      case "requirements":
        return <RequirementsEditor />;
      case "functional":
        return (
          <div className="h-full flex flex-col">
            <div className="flex-1"><DiagramCanvas diagramType="BDD" /></div>
            {projectId && <EntityCreator entityType="function" projectId={projectId} />}
          </div>
        );
      case "logical":
        return (
          <div className="h-full flex flex-col">
            <div className="flex-1"><DiagramCanvas diagramType="IBD" /></div>
            {projectId && <EntityCreator entityType="sc" projectId={projectId} />}
          </div>
        );
      case "physical":
        return (
          <div className="h-full flex flex-col">
            <div className="flex-1"><DiagramCanvas diagramType="Topology" /></div>
            {projectId && <EntityCreator entityType="ecu" projectId={projectId} />}
          </div>
        );
      case "ple":
        return <TagManager />;
      case "baselines":
        return projectId ? <BaselinesPanel projectId={projectId} /> : <div className="p-6 text-sm text-muted-foreground">请先选择项目</div>;
      case "trace":
        return projectId ? <TraceMatrixPanel projectId={projectId} /> : <div className="p-6 text-sm text-muted-foreground">请先选择项目</div>;
      default:
        return null;
    }
  };

  return (
    <main className="flex-1 overflow-hidden bg-background">
      {renderView()}
    </main>
  );
}
