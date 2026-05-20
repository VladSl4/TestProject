/**
 * Integration test: pastes raw logs, clicks "Generate Insights",
 * mocks the backend `fetch`, and asserts the dashboard renders the
 * insight that came back.
 */

import { describe, expect, it, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { LogAnalyzer } from "@/components/LogAnalyzer";

const fakeInsight = {
  id: 42,
  summary: "1 error detected across 3 log lines. First error: ERROR pool exhausted",
  category: "Error" as const,
  recommended_action: "Investigate the failing component, capture the full stack trace.",
  created_at: "2026-05-20T11:00:00Z",
};

const fakeHistory = [
  {
    id: 42,
    raw_logs: "ERROR pool exhausted",
    summary: fakeInsight.summary,
    category: "Error" as const,
    recommended_action: fakeInsight.recommended_action,
    created_at: fakeInsight.created_at,
  },
];

function mockFetch(responses: Record<string, unknown>) {
  return vi.fn(async (input: RequestInfo | URL) => {
    const url = typeof input === "string" ? input : input.toString();
    for (const [pattern, body] of Object.entries(responses)) {
      if (url.includes(pattern)) {
        return new Response(JSON.stringify(body), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        });
      }
    }
    return new Response("[]", { status: 200 });
  });
}

describe("LogAnalyzer dashboard", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "fetch",
      mockFetch({
        "/api/analyze": fakeInsight,
        "/api/analyses": fakeHistory,
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("renders the backend insight after Generate Insights is clicked", async () => {
    render(<LogAnalyzer />);

    fireEvent.change(screen.getByTestId("raw-logs-input"), {
      target: { value: "ERROR pool exhausted" },
    });
    fireEvent.click(screen.getByTestId("generate-insights-button"));

    // Loading state appears
    expect(screen.getByTestId("loading-indicator")).toBeInTheDocument();

    // Insight card shows up once the mocked API resolves
    const card = await screen.findByTestId("insight-card");
    expect(card).toBeInTheDocument();

    expect(screen.getByTestId("insight-summary")).toHaveTextContent(
      "1 error detected across 3 log lines",
    );
    expect(screen.getByTestId("insight-action")).toHaveTextContent(
      "Investigate the failing component",
    );
    // Both the insight card and the history list show an Error badge after the
    // backend reply lands — assert at least one is rendered.
    expect(screen.getAllByTestId("category-badge-Error").length).toBeGreaterThan(0);
  });

  it("shows an error banner when the backend fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) => {
        const url = typeof input === "string" ? input : input.toString();
        if (url.includes("/api/analyze")) {
          return new Response("boom", { status: 500 });
        }
        return new Response("[]", { status: 200 });
      }),
    );

    render(<LogAnalyzer />);
    fireEvent.change(screen.getByTestId("raw-logs-input"), {
      target: { value: "ERROR pool exhausted" },
    });
    fireEvent.click(screen.getByTestId("generate-insights-button"));

    const banner = await screen.findByTestId("error-banner");
    expect(banner).toHaveTextContent(/Could not analyze logs/i);
    expect(screen.queryByTestId("insight-card")).not.toBeInTheDocument();
  });

  it("disables the button while loading", async () => {
    render(<LogAnalyzer />);
    fireEvent.change(screen.getByTestId("raw-logs-input"), {
      target: { value: "INFO ok" },
    });
    const button = screen.getByTestId("generate-insights-button");
    fireEvent.click(button);
    expect(button).toBeDisabled();
    await waitFor(() => expect(button).not.toBeDisabled());
  });
});
