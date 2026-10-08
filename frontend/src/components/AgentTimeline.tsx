"use client";

import React from "react";
import { CheckCircle2, Loader2, Circle, ShieldAlert, Cpu } from "lucide-react";

export interface AgentStatus {
  name: string;
  role: string;
  status: "idle" | "running" | "done" | "flagged";
  detail?: string;
}

interface AgentTimelineProps {
  agents: AgentStatus[];
}

export const AgentTimeline: React.FC<AgentTimelineProps> = ({ agents }) => {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 shadow-sm space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-bold uppercase tracking-wider text-gray-400 flex items-center gap-2">
          <Cpu className="w-4 h-4 text-purple-400" />
          LangGraph Multi-Agent Team
        </h2>
        <span className="text-[11px] font-mono text-purple-400 bg-purple-500/10 px-2 py-0.5 rounded border border-purple-500/20">
          Cyclical Graph
        </span>
      </div>

      <div className="space-y-2">
        {agents.map((agent, idx) => {
          return (
            <div
              key={idx}
              className={`p-3 rounded-lg border transition-all ${
                agent.status === "running"
                  ? "bg-blue-950/40 border-blue-500/60 shadow-[0_0_15px_rgba(59,130,246,0.2)]"
                  : agent.status === "done"
                  ? "bg-gray-950/80 border-emerald-500/30"
                  : "bg-gray-950/50 border-gray-800/60"
              }`}
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2">
                  {agent.status === "running" && (
                    <Loader2 className="w-3.5 h-3.5 text-blue-400 animate-spin" />
                  )}
                  {agent.status === "done" && (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  )}
                  {agent.status === "flagged" && (
                    <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
                  )}
                  {agent.status === "idle" && (
                    <Circle className="w-3.5 h-3.5 text-gray-600" />
                  )}
                  <span className="font-semibold text-slate-200">
                    {agent.name}
                  </span>
                </div>

                <span
                  className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded ${
                    agent.status === "running"
                      ? "text-blue-300 bg-blue-500/20"
                      : agent.status === "done"
                      ? "text-emerald-300 bg-emerald-500/20"
                      : "text-gray-400 bg-gray-800"
                  }`}
                >
                  {agent.status}
                </span>
              </div>

              <div className="text-[11px] text-gray-400 mt-1 pl-5">
                {agent.detail || agent.role}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
