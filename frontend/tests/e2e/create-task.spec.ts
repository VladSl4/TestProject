import { test, expect } from "@playwright/test";

// End-to-end: user opens the app, creates a Vibe Task, and sees it land in the Pending column.
// Prerequisite: all three backend microservices and the Next.js dev server are running.

test("user can create a Vibe Task and see it in the Pending column", async ({ page }) => {
  const uniqueTitle = `E2E vibe ${Date.now()}`;

  await page.goto("/");
  await expect(page.getByRole("heading", { name: /vibe tasks/i })).toBeVisible();

  await page.getByLabel("Task title").fill(uniqueTitle);
  await page.getByLabel("Task description").fill("created by playwright");
  await page.getByRole("button", { name: /add vibe/i }).click();

  const pendingColumn = page.getByTestId("column-Pending");
  await expect(pendingColumn.getByText(uniqueTitle)).toBeVisible({ timeout: 5000 });
  await expect(pendingColumn.getByText("created by playwright")).toBeVisible();
});
