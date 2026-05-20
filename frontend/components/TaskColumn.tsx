"use client";

import type { Task, VibeStatus } from "@/lib/types";
import { STATUS_LABEL } from "@/lib/types";
import { TaskCard } from "./TaskCard";

interface Props {
  status: VibeStatus;
  tasks: Task[];
  onStatusChange: (id: number, status: VibeStatus) => void;
  onDelete: (id: number) => void;
  onVibeCheck: (id: number) => Promise<void>;
}

const COLUMN_STYLES: Record<VibeStatus, string> = {
  Pending: "from-amber-500/20 to-amber-500/5 border-amber-400/30",
  InProgress: "from-sky-500/20 to-sky-500/5 border-sky-400/30",
  Groovy: "from-emerald-500/20 to-emerald-500/5 border-emerald-400/30",
};

const COLUMN_ICON: Record<VibeStatus, string> = {
  Pending: "🌱",
  InProgress: "🌀",
  Groovy: "🪩",
};

export function TaskColumn({ status, tasks, onStatusChange, onDelete, onVibeCheck }: Props) {
  return (
    <section
      data-testid={`column-${status}`}
      className={`rounded-3xl border bg-gradient-to-b ${COLUMN_STYLES[status]} p-4 backdrop-blur`}
    >
      <header className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-bold tracking-wide">
          <span className="mr-2">{COLUMN_ICON[status]}</span>
          {STATUS_LABEL[status]}
        </h2>
        <span className="text-xs text-slate-300 bg-white/10 rounded-full px-2 py-0.5">
          {tasks.length}
        </span>
      </header>

      <div className="space-y-3 min-h-[8rem]">
        {tasks.length === 0 && (
          <p className="text-sm text-slate-400 italic text-center py-6">
            no vibes here yet
          </p>
        )}
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onStatusChange={onStatusChange}
            onDelete={onDelete}
            onVibeCheck={onVibeCheck}
          />
        ))}
      </div>
    </section>
  );
}
