import { useState, useRef, useEffect } from "react";
import { useMutation } from "@apollo/client";
import { useAgentStore } from "@/stores/agent";
import { useProjectStore } from "@/stores/project";
import { cn } from "@/lib/utils";
import { Send, Loader2 } from "lucide-react";
import { SEND_MESSAGE } from "@/graphql/operations";

export function AgentPanel() {
  const [input, setInput] = useState("");
  const messages = useAgentStore((s) => s.messages);
  const isThinking = useAgentStore((s) => s.isThinking);
  const thinkingTrace = useAgentStore((s) => s.thinkingTrace);
  const addMessage = useAgentStore((s) => s.addMessage);
  const setThinking = useAgentStore((s) => s.setThinking);
  const appendThinkingTrace = useAgentStore((s) => s.appendThinkingTrace);
  const clearThinking = useAgentStore((s) => s.clearThinking);
  const projectId = useProjectStore((s) => s.activeProjectId);
  const scrollRef = useRef<HTMLDivElement>(null);

  const [sendMessage] = useMutation(SEND_MESSAGE);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, thinkingTrace]);

  const handleSend = async () => {
    if (!input.trim() || isThinking) return;
    const text = input.trim();
    setInput("");
    addMessage({ role: "user", content: text, timestamp: Date.now() });

    if (!projectId) {
      addMessage({
        role: "agent",
        content: "[System] 请先创建或选择一个项目。",
        timestamp: Date.now(),
      });
      return;
    }

    setThinking(true);
    appendThinkingTrace("Orchestrator 正在分析意图...");

    try {
      const { data } = await sendMessage({
        variables: { projectId, message: text },
      });
      appendThinkingTrace("领域引擎执行完成");
      const answer = data?.sendMessage?.answer ?? "[System] 无响应";
      addMessage({ role: "agent", content: answer, timestamp: Date.now() });
    } catch (err: any) {
      addMessage({
        role: "agent",
        content: `[Error] 请求失败: ${err.message}`,
        timestamp: Date.now(),
      });
    } finally {
      clearThinking();
    }
  };

  return (
    <aside className="w-80 border-l border-border bg-muted/30 flex flex-col">
      <div className="p-4 border-b border-border">
        <h2 className="font-semibold text-sm">AI Agent 对话</h2>
        <p className="text-xs text-muted-foreground mt-1">
          Orchestrator — 10 个专业 Agent 就绪
        </p>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.length === 0 && (
          <div className="text-sm text-muted-foreground text-center py-8">
            <p>向 AI 提问或发出指令：</p>
            <ul className="mt-2 text-xs space-y-1">
              <li>"分析制动系统需求"</li>
              <li>"为 PHEV_B 车型创建变体"</li>
              <li>"哪些 ECU 使用 CAN-FD？"</li>
              <li>"生成 BL_V2.0 基线"</li>
            </ul>
          </div>
        )}
        {messages.map((m, i) => (
          <div
            key={`${m.timestamp}-${i}`}
            className={cn(
              "text-sm rounded-lg px-3 py-2 whitespace-pre-wrap",
              m.role === "user"
                ? "bg-primary text-primary-foreground ml-8"
                : "bg-muted mr-4",
            )}
          >
            {m.content}
          </div>
        ))}
        {isThinking && (
          <div className="text-xs text-muted-foreground italic px-3">
            {thinkingTrace.length > 0 ? thinkingTrace[thinkingTrace.length - 1] : "思考中..."}
            <Loader2 size={12} className="inline ml-2 animate-spin" />
          </div>
        )}
      </div>

      <div className="p-3 border-t border-border">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="输入指令或问题..."
            className="flex-1 text-sm bg-background border border-border rounded-md px-3 py-2 focus:outline-none focus:border-primary"
          />
          <button
            type="button"
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="p-2 rounded-md bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
          >
            <Send size={16} />
          </button>
        </div>
      </div>
    </aside>
  );
}
