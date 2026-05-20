"use client";

import { FormEvent, useState } from "react";

interface Props {
  onCreate: (title: string, description?: string) => Promise<void>;
}

export function CreateTaskForm({ onCreate }: Props) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!title.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      await onCreate(title.trim(), description.trim() || undefined);
      setTitle("");
      setDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-3xl bg-white/5 backdrop-blur border border-white/10 p-4 mb-8"
      data-testid="create-task-form"
    >
      <div className="flex flex-col md:flex-row gap-3">
        <input
          aria-label="Task title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What's the vibe? (e.g. Refactor the chakra)"
          className="flex-1 rounded-xl bg-white/10 border border-white/10 px-4 py-2 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-fuchsia-500/50"
          maxLength={200}
        />
        <input
          aria-label="Task description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Optional context"
          className="flex-1 rounded-xl bg-white/10 border border-white/10 px-4 py-2 text-sm placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-fuchsia-500/50"
          maxLength={2000}
        />
        <button
          type="submit"
          disabled={submitting || !title.trim()}
          className="rounded-xl bg-gradient-to-r from-fuchsia-500 to-indigo-500 px-5 py-2 font-medium text-sm shadow-vibe hover:opacity-90 disabled:opacity-40"
        >
          {submitting ? "Sending good vibes…" : "+ Add Vibe"}
        </button>
      </div>
      {error && (
        <p role="alert" className="mt-2 text-sm text-rose-300">
          {error}
        </p>
      )}
    </form>
  );
}
