import type { AnalysisInsight } from "@/lib/types";
import { CategoryBadge } from "./CategoryBadge";

export function InsightCard({ insight }: { insight: AnalysisInsight }) {
  return (
    <article
      data-testid="insight-card"
      className="rounded-3xl border border-white/10 bg-white/5 backdrop-blur p-6 shadow-card"
    >
      <header className="flex items-start justify-between gap-4 mb-4">
        <h2 className="text-lg font-bold tracking-wide text-slate-100">
          AI Insight
        </h2>
        <CategoryBadge category={insight.category} />
      </header>

      <section className="space-y-4">
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
            Summary
          </h3>
          <p data-testid="insight-summary" className="text-slate-100 leading-relaxed">
            {insight.summary}
          </p>
        </div>

        <div>
          <h3 className="text-xs font-semibold uppercase tracking-widest text-slate-400 mb-1">
            Recommended Action
          </h3>
          <p
            data-testid="insight-action"
            className="text-slate-200 leading-relaxed"
          >
            {insight.recommended_action}
          </p>
        </div>
      </section>
    </article>
  );
}
