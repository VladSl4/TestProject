import type { AnalysisHistoryItem } from "@/lib/types";
import { CategoryBadge } from "./CategoryBadge";

interface Props {
  items: AnalysisHistoryItem[];
  onDelete: (id: number) => void;
}

export function HistoryList({ items, onDelete }: Props) {
  if (items.length === 0) {
    return (
      <p className="text-sm text-slate-400 italic py-4">
        No analyses yet — paste some logs above and hit Generate Insights.
      </p>
    );
  }

  return (
    <ul data-testid="history-list" className="space-y-3">
      {items.map((item) => (
        <li
          key={item.id}
          data-testid={`history-item-${item.id}`}
          className="group rounded-2xl border border-white/10 bg-white/5 backdrop-blur p-4 hover:bg-white/10 transition"
        >
          <header className="flex items-start justify-between gap-3 mb-2">
            <div className="flex items-center gap-3">
              <CategoryBadge category={item.category} />
              <time className="text-xs text-slate-400">
                {new Date(item.created_at).toLocaleString()}
              </time>
            </div>
            <button
              onClick={() => onDelete(item.id)}
              aria-label={`Delete analysis ${item.id}`}
              className="text-slate-400 hover:text-rose-400 text-sm opacity-0 group-hover:opacity-100 transition"
            >
              ✕
            </button>
          </header>
          <p className="text-sm text-slate-200">{item.summary}</p>
        </li>
      ))}
    </ul>
  );
}
