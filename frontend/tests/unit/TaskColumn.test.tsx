import { describe, expect, it, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { TaskColumn } from "@/components/TaskColumn";
import type { Task } from "@/lib/types";

const makeTask = (overrides: Partial<Task> = {}): Task => ({
  id: 1,
  title: "Refactor the chakra",
  description: null,
  status: "Pending",
  mood_emoji: null,
  created_at: new Date().toISOString(),
  ...overrides,
});

describe("TaskColumn list rendering", () => {
  it("renders every task title passed in", () => {
    const tasks = [
      makeTask({ id: 1, title: "Task A" }),
      makeTask({ id: 2, title: "Task B" }),
      makeTask({ id: 3, title: "Task C" }),
    ];

    render(
      <TaskColumn
        status="Pending"
        tasks={tasks}
        onStatusChange={vi.fn()}
        onDelete={vi.fn()}
        onVibeCheck={vi.fn()}
      />,
    );

    expect(screen.getByText("Task A")).toBeInTheDocument();
    expect(screen.getByText("Task B")).toBeInTheDocument();
    expect(screen.getByText("Task C")).toBeInTheDocument();
    expect(screen.getByTestId("column-Pending")).toBeInTheDocument();
  });

  it("renders the empty-state message when there are no tasks", () => {
    render(
      <TaskColumn
        status="Groovy"
        tasks={[]}
        onStatusChange={vi.fn()}
        onDelete={vi.fn()}
        onVibeCheck={vi.fn()}
      />,
    );
    expect(screen.getByText(/no vibes here yet/i)).toBeInTheDocument();
  });

  it("shows the mood emoji when set", () => {
    render(
      <TaskColumn
        status="InProgress"
        tasks={[makeTask({ status: "InProgress", mood_emoji: "🚀" })]}
        onStatusChange={vi.fn()}
        onDelete={vi.fn()}
        onVibeCheck={vi.fn()}
      />,
    );
    expect(screen.getByLabelText("mood")).toHaveTextContent("🚀");
  });
});
