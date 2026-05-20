"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import * as api from "@/lib/api";
import type { AnalysisHistoryItem, AnalysisInsight } from "@/lib/types";
import { InsightCard } from "./InsightCard";
import { HistoryList } from "./HistoryList";

const SAMPLE = `2026-05-20T10:14:22Z INFO  api  request id=abc-123 GET /health 200 12ms
2026-05-20T10:14:23Z WARN  api  slow query detected (812ms) on table=orders
2026-05-20T10:14:24Z ERROR db   connection pool exhausted (max=20)
2026-05-20T10:14:24Z ERROR api  request id=abc-124 POST /orders 500 — Internal Server Error
`;

export function LogAnalyzer() {
  const [logs, setLogs] = useState("");
  const [insight, setInsight] = useState<AnalysisInsight | null>(null);
  const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshHistory = useCallback(async () => {
    try {
      const items = await api.listAnalyses();
      setHistory(items);
    } catch {
      // History is best-effort; surfacing the analyze error is more important.
    }
  }, []);

  useEffect(() => {
    void refreshHistory();
  }, [refreshHistory]);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!logs.trim() || loading) return;
    setLoading(true);
    setError(null);
    try {
      const result = await api.analyzeLogs(logs);
      setInsight(result);
      await refreshHistory();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyze logs");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    const previous = history;
    setHistory((items) => items.filter((item) => item.id !== id));
    try {
      await api.deleteAnalysis(id);
    } catch {
      setHistory(previous);
    }
  };

  return (
    <main className="max-w-5xl mx-auto px-6 py-10">
      <header className="mb-8">
        <h1 className="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-cyan-300 via-sky-300 to-indigo-300 bg-clip-text text-transparent">
          VibeLog
        </h1>
        <p className="mt-2 text-slate-300 text-sm">
          AI-powered log analyzer — paste raw logs, get a distilled summary,
          category and recommended action.
        </p>
      </header>

      <form
        onSubmit={handleSubmit}
        data-testid="analyze-form"
        className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur p-5 mb-6"
      >
        <label htmlFor="raw-logs" className="block text-xs font-semibold uppercase tracking-widest text-slate-400 mb-2">
          Raw logs
        </label>
        <textarea
          id="raw-logs"
          data-testid="raw-logs-input"
          value={logs}
          onChange={(e) => setLogs(e.target.value)}
          placeholder={SAMPLE}
          rows={10}
          className="w-full rounded-2xl bg-slate-950/60 border border-white/10 px-4 py-3 text-sm font-mono text-slate-100 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-cyan-500/40 resize-y"
          maxLength={200000}
          disabled={loading}
        />

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="submit"
            data-testid="generate-insights-button"
            disabled={loading || !logs.trim()}
            className="rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-500 px-5 py-2.5 font-medium text-sm shadow-card hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed transition"
          >
            {loading ? "Analyzing…" : "Generate Insights"}
          </button>

          <button
            type="button"
            onClick={() => setLogs(SAMPLE)}
            disabled={loading}
            className="rounded-xl bg-white/5 border border-white/10 px-4 py-2.5 text-sm text-slate-300 hover:bg-white/10 disabled:opacity-40"
          >
            Paste sample
          </button>

          {loading && (
            <span
              role="status"
              data-testid="loading-indicator"
              className="text-sm text-cyan-300 animate-pulse"
            >
              Talking to the AI…
            </span>
          )}
        </div>
      </form>

      {error && (
        <div
          role="alert"
          data-testid="error-banner"
          className="mb-6 rounded-2xl border border-rose-400/30 bg-rose-500/10 px-4 py-3 text-sm text-rose-200"
        >
          <strong className="font-semibold">Could not analyze logs:</strong> {error}
        </div>
      )}

      {insight && !loading && (
        <div className="mb-8">
          <InsightCard insight={insight} />
        </div>
      )}

      <section>
        <h2 className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-3">
          Recent analyses
        </h2>
        <HistoryList items={history} onDelete={handleDelete} />
      </section>
    </main>
  );
}
