import { create } from "zustand";

interface AgentMessage {
  role: "user" | "agent";
  content: string;
  timestamp: number;
}

interface AgentState {
  messages: AgentMessage[];
  isThinking: boolean;
  thinkingTrace: string[];
  addMessage: (msg: AgentMessage) => void;
  setThinking: (v: boolean) => void;
  appendThinkingTrace: (line: string) => void;
  clearThinking: () => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  messages: [],
  isThinking: false,
  thinkingTrace: [],
  addMessage: (msg) => set((s) => ({ messages: [...s.messages, msg] })),
  setThinking: (v) => set({ isThinking: v }),
  appendThinkingTrace: (line) => set((s) => ({ thinkingTrace: [...s.thinkingTrace, line] })),
  clearThinking: () => set({ thinkingTrace: [], isThinking: false }),
}));
