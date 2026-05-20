export type VibeStatus = "Pending" | "InProgress" | "Groovy";

export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: VibeStatus;
  mood_emoji: string | null;
  created_at: string;
}

export interface TaskCreatePayload {
  title: string;
  description?: string;
}

export interface TaskUpdatePayload {
  title?: string;
  description?: string;
  status?: VibeStatus;
  mood_emoji?: string;
}

export interface VibeCheckResult {
  task_id: number;
  mood_emoji: string;
  vibe_message: string;
}

export const STATUS_LABEL: Record<VibeStatus, string> = {
  Pending: "Pending",
  InProgress: "In-Progress",
  Groovy: "Groovy",
};

export const STATUS_ORDER: VibeStatus[] = ["Pending", "InProgress", "Groovy"];
