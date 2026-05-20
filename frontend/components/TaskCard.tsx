"use client";

import { useState } from "react";
import type { Task, VibeStatus } from "@/lib/types";

interface Props {
  task: Task;
  onStatusChange: (id: number, status: VibeStatus) => void;
  onDelete: (id: number) => void;
  onVibeCheck: (id: number) => Promise<void>;
}

const NEXT_STATUS: Record<VibeStatus, VibeStatus | null> = {
  Pending: "InProgress",
  InProgress: "Groovy",
  Groovy: null,
};

const NEXT_LABEL: Record<VibeStatus, string> = {
  Pending: "Start the vibe",
  InProgress: "Mark Groovy",
  Groovy: "✓ Already groovy",
};

export function TaskCard({ task, onStatusChange, onDelete, onVibeCheck }: Props) {
  const [vibing, setVibing] = useState(false);
  const next = NEXT_STATUS[task.status];

  const handleVibe = async () => {
    setVibing(true);
    try {
      await onVibeCheck(task.id);
    } finally {
      setVibing(false);
    }
  };

  return (
    <article
      data-testid={`task-card-${task.id}`}
      className="group rounded-2xl bg-white/5 backdrop-blur border border-white/10 p-4 shadow-vibe hover:bg-white/10 transition"
    >
      <header className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-lg leading-tight">
          {task.mood_emoji && (
            <span className="mr-2 text-2xl" aria-label="mood">
              {task.mood_emoji}
            </span>
          )}
          {task.title}
        </h3>
        <button
          onClick={() => onDelete(task.id)}
          aria-label="Delete task"
          className="text-slate-400 hover:text-rose-400 text-sm opacity-0 group-hover:opacity-100 transition"
        >
          ✕
        </button>
      </header>

      {task.description && (
        <p className="mt-2 text-sm text-slate-300">{task.description}</p>
      )}

      <div className="mt-4 flex flex-wrap gap-2">
        <button
          onClick={handleVibe}
          disabled={vibing}
          className="rounded-full bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-3 py-1.5 text-xs font-medium hover:opacity-90 disabled:opacity-50"
        >
          {vibing ? "Checking…" : "✨ Vibe Check"}
        </button>

        {next && (
          <button
            onClick={() => onStatusChange(task.id, next)}
            className="rounded-full bg-white/10 hover:bg-white/20 px-3 py-1.5 text-xs font-medium"
          >
            {NEXT_LABEL[task.status]}
          </button>
        )}
        {!next && (
          <span className="rounded-full bg-emerald-500/20 text-emerald-300 px-3 py-1.5 text-xs font-medium">
            {NEXT_LABEL[task.status]}
          </span>
        )}
      </div>
    </article>
  );
}
