import type { LogCategory } from "@/lib/types";

const STYLES: Record<LogCategory, string> = {
  Info: "bg-cyan-500/15 text-cyan-300 border-cyan-400/30",
  Warning: "bg-amber-500/15 text-amber-300 border-amber-400/30",
  Error: "bg-rose-500/15 text-rose-300 border-rose-400/30",
};

const ICONS: Record<LogCategory, string> = {
  Info: "ℹ",
  Warning: "⚠",
  Error: "✖",
};

export function CategoryBadge({ category }: { category: LogCategory }) {
  return (
    <span
      data-testid={`category-badge-${category}`}
      className={`inline-flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wider ${STYLES[category]}`}
    >
      <span aria-hidden>{ICONS[category]}</span>
      {category}
    </span>
  );
}
