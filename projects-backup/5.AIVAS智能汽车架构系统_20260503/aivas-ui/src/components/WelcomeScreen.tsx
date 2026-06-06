import { useState } from "react";
import { useMutation, useQuery } from "@apollo/client";
import { GET_PROJECTS, CREATE_PROJECT } from "@/graphql/operations";
import { useProjectStore } from "@/stores/project";
import { cn } from "@/lib/utils";
import { demoProjects, genDemoId } from "@/lib/demoData";

export function WelcomeScreen() {
  const [name, setName] = useState("");
  const [desc, setDesc] = useState("");
  const { data, refetch } = useQuery(GET_PROJECTS, { fetchPolicy: "cache-and-network" });
  const [createProject] = useMutation(CREATE_PROJECT);
  const setActiveProject = useProjectStore((s) => s.setActiveProject);

  const handleCreate = async () => {
    if (!name.trim()) return;
    try {
      const res = await createProject({
        variables: { input: { name: name.trim(), description: desc || null } },
      });
      const project = res.data?.createProject;
      if (project) {
        await refetch();
        setActiveProject(project.id);
      }
    } catch {
      // Backend unavailable — create demo project locally
      const demoId = genDemoId();
      setActiveProject(demoId);
    }
  };

  const projects = data?.projects?.length > 0 ? data.projects : demoProjects;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 flex items-center justify-center">
      <div className="w-full max-w-2xl p-8">
        <h1 className="text-4xl font-bold text-white mb-2 tracking-tight">AIVAS</h1>
        <p className="text-slate-400 mb-8 text-lg">
          AI-Native Vehicle Architecture System — 智能汽车架构开发平台
        </p>

        <div className="bg-white/5 border border-white/10 rounded-xl p-6 mb-6">
          <h2 className="text-white font-semibold mb-4">创建新项目</h2>
          <div className="space-y-3">
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="项目名称..."
              className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2.5 text-white placeholder:text-slate-500 focus:outline-none focus:border-blue-500"
            />
            <input
              type="text"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              placeholder="项目描述（可选）..."
              className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2.5 text-white placeholder:text-slate-500 focus:outline-none focus:border-blue-500"
            />
            <button
              type="button"
              onClick={handleCreate}
              className={cn(
                "px-6 py-2.5 rounded-lg font-medium text-white transition-colors",
                name.trim()
                  ? "bg-blue-600 hover:bg-blue-700"
                  : "bg-slate-700 cursor-not-allowed",
              )}
            >
              开始项目
            </button>
          </div>
        </div>

        <div>
          <h3 className="text-slate-300 text-sm font-medium mb-3">最近项目</h3>
          <div className="space-y-2">
            {projects.map((p: { id: string; name: string; description: string | null }) => (
              <button
                type="button"
                key={p.id}
                onClick={() => setActiveProject(p.id)}
                className="w-full text-left bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg px-4 py-3 transition-colors"
              >
                <div className="text-white font-medium">{p.name}</div>
                {p.description && (
                  <div className="text-slate-500 text-sm mt-0.5">{p.description}</div>
                )}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
