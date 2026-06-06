import { create } from "zustand";

interface ProjectState {
  activeProjectId: string | null;
  activeView: "requirements" | "functional" | "logical" | "physical" | "ple" | "baselines" | "trace";
  setActiveProject: (id: string) => void;
  setActiveView: (view: ProjectState["activeView"]) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  activeProjectId: null,
  activeView: "requirements",
  setActiveProject: (id) => set({ activeProjectId: id }),
  setActiveView: (view) => set({ activeView: view }),
}));
