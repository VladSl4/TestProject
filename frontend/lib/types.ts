export type LogCategory = "Info" | "Warning" | "Error";

export interface AnalysisInsight {
  id: number | null;
  summary: string;
  category: LogCategory;
  recommended_action: string;
  created_at: string | null;
}

export interface AnalysisHistoryItem {
  id: number;
  raw_logs: string;
  summary: string;
  category: LogCategory;
  recommended_action: string;
  created_at: string;
}
