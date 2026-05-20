"use client";

import { useCallback, useEffect, useState } from "react";
import * as api from "@/lib/api";
import type { Task, VibeStatus } from "@/lib/types";
import { STATUS_ORDER } from "@/lib/types";
import { CreateTaskForm } from "./CreateTaskForm";
import { TaskColumn } from "./TaskColumn";

let tempIdCounter = -1;

export function VibeBoard() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [globalError, setGlobalError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      const data = await api.listTasks();
      setTasks(data);
      setGlobalError(null);
    } catch (err) {
      setGlobalError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  // Optimistic create — render immediately with a negative temp id,
  // then reconcile with the server response (or roll back on failure).
  const handleCreate = useCallback(async (title: string, description?: string) => {
    const tempId = tempIdCounter--;
    const optimistic: Task = {
      id: tempId,
      title,
      description: description ?? null,
      status: "Pending",
      mood_emoji: null,
      created_at: new Date().toISOString(),
    };
    setTasks((prev) => [...prev, optimistic]);
    try {
      const created = await api.createTask({ title, description });
      setTasks((prev) => prev.map((t) => (t.id === tempId ? created : t)));
    } catch (err) {
      setTasks((prev) => prev.filter((t) => t.id !== tempId));
      throw err;
    }
  }, []);

  const handleStatusChange = useCallback(async (id: number, status: VibeStatus) => {
    const prevSnapshot = tasks;
    setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, status } : t)));
    try {
      const updated = await api.updateTask(id, { status });
      setTasks((prev) => prev.map((t) => (t.id === id ? updated : t)));
    } catch (err) {
      setTasks(prevSnapshot);
      setGlobalError(err instanceof Error ? err.message : "Update failed");
    }
  }, [tasks]);

  const handleDelete = useCallback(async (id: number) => {
    const prevSnapshot = tasks;
    setTasks((prev) => prev.filter((t) => t.id !== id));
    try {
      await api.deleteTask(id);
    } catch (err) {
      setTasks(prevSnapshot);
      setGlobalError(err instanceof Error ? err.message : "Delete failed");
    }
  }, [tasks]);

  const handleVibeCheck = useCallback(async (id: number) => {
    try {
      const result = await api.vibeCheck(id);
      setTasks((prev) =>
        prev.map((t) =>
          t.id === id ? { ...t, mood_emoji: result.mood_emoji } : t,
        ),
      );
    } catch (err) {
      setGlobalError(err instanceof Error ? err.message : "Vibe check failed");
    }
  }, []);

  return (
    <main className="max-w-6xl mx-auto px-6 py-10">
      <header className="mb-10">
        <h1 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-fuchsia-300 via-pink-300 to-amber-200 bg-clip-text text-transparent">
          Vibe Tasks
        </h1>
        <p className="mt-2 text-slate-300 text-sm">
          WebaResponds &middot; Phase 01 &middot; Move the energy from{" "}
          <span className="text-amber-300">Pending</span> →{" "}
          <span className="text-sky-300">In-Progress</span> →{" "}
          <span className="text-emerald-300">Groovy</span>
        </p>
      </header>

      {globalError && (
        <div className="mb-4 rounded-xl border border-rose-400/40 bg-rose-500/10 px-4 py-2 text-sm text-rose-200">
          {globalError}
        </div>
      )}

      <CreateTaskForm onCreate={handleCreate} />

      {loading ? (
        <p className="text-center text-slate-400 italic">tuning in…</p>
      ) : (
        <div
          data-testid="vibe-board"
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {STATUS_ORDER.map((status) => (
            <TaskColumn
              key={status}
              status={status}
              tasks={tasks.filter((t) => t.status === status)}
              onStatusChange={handleStatusChange}
              onDelete={handleDelete}
              onVibeCheck={handleVibeCheck}
            />
          ))}
        </div>
      )}
    </main>
  );
}
