import type { AnalysisHistoryItem, AnalysisInsight } from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

async function handle<T>(resp: Response): Promise<T> {
  if (!resp.ok) {
    const body = await resp.text();
    throw new Error(`API ${resp.status}: ${body || resp.statusText}`);
  }
  if (resp.status === 204) return undefined as T;
  return (await resp.json()) as T;
}

export async function analyzeLogs(rawLogs: string): Promise<AnalysisInsight> {
  return handle(
    await fetch(`${API_BASE_URL}/api/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ raw_logs: rawLogs }),
    }),
  );
}

export async function listAnalyses(): Promise<AnalysisHistoryItem[]> {
  return handle(
    await fetch(`${API_BASE_URL}/api/analyses`, { cache: "no-store" }),
  );
}

export async function deleteAnalysis(id: number): Promise<void> {
  return handle(
    await fetch(`${API_BASE_URL}/api/analyses/${id}`, { method: "DELETE" }),
  );
}
