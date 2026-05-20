import type {
  Task,
  TaskCreatePayload,
  TaskUpdatePayload,
  VibeCheckResult,
} from "./types";

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

export async function listTasks(): Promise<Task[]> {
  return handle(await fetch(`${API_BASE_URL}/api/tasks`, { cache: "no-store" }));
}

export async function createTask(payload: TaskCreatePayload): Promise<Task> {
  return handle(
    await fetch(`${API_BASE_URL}/api/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
  );
}

export async function updateTask(
  id: number,
  payload: TaskUpdatePayload,
): Promise<Task> {
  return handle(
    await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
  );
}

export async function deleteTask(id: number): Promise<void> {
  return handle(
    await fetch(`${API_BASE_URL}/api/tasks/${id}`, { method: "DELETE" }),
  );
}

export async function vibeCheck(id: number): Promise<VibeCheckResult> {
  return handle(
    await fetch(`${API_BASE_URL}/api/tasks/${id}/vibe-check`, { method: "POST" }),
  );
}
