import { useProjectStore } from "@/stores/project";
import { Sidebar } from "@/components/panels/Sidebar";
import { MainPanel } from "@/components/panels/MainPanel";
import { AgentPanel } from "@/components/panels/AgentPanel";
import { StatusBar } from "@/components/panels/StatusBar";
import { WelcomeScreen } from "@/components/WelcomeScreen";

export function App() {
  const activeProjectId = useProjectStore((s) => s.activeProjectId);

  if (!activeProjectId) {
    return <WelcomeScreen />;
  }

  return (
    <div className="h-screen flex flex-col">
      <div className="flex-1 flex overflow-hidden">
        <Sidebar />
        <MainPanel />
        <AgentPanel />
      </div>
      <StatusBar />
    </div>
  );
}
