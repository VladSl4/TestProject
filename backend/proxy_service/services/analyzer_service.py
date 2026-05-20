"""Heuristic log analyzer that simulates an LLM call.

Sleeps for a configurable delay and classifies the input using simple
keyword matching. Pure and deterministic given the same input + zero
latency, which makes it cheap to unit-test.
"""

from __future__ import annotations

import re
import time

import proxy_analyses_pb2 as proxy_pb

from proxy_service.interfaces.analyzer_service import (
    AbstractAnalyzerService,
    AnalysisInsight,
)


_ERROR_PATTERN = re.compile(
    r"\b(error|exception|fatal|critical|panic|traceback|stacktrace|fail(?:ed|ure)?)\b",
    re.IGNORECASE,
)
_WARNING_PATTERN = re.compile(r"\b(warn|warning|deprecat\w*)\b", re.IGNORECASE)

_PREVIEW_LEN = 140


def _preview(line: str) -> str:
    line = line.strip()
    return (line[: _PREVIEW_LEN - 1] + "…") if len(line) > _PREVIEW_LEN else line


class AnalyzerService(AbstractAnalyzerService):
    def __init__(self, latency_seconds: float = 1.0) -> None:
        self._latency = max(0.0, latency_seconds)

    def analyze(self, raw_logs: str) -> AnalysisInsight:
        if self._latency:
            time.sleep(self._latency)

        lines = [line for line in raw_logs.splitlines() if line.strip()]
        total = len(lines)
        errors = [line for line in lines if _ERROR_PATTERN.search(line)]
        warnings = [line for line in lines if _WARNING_PATTERN.search(line)]

        if errors:
            category = proxy_pb.ERROR
            summary = (
                f"{len(errors)} error{'s' if len(errors) != 1 else ''} detected "
                f"across {total} log line{'s' if total != 1 else ''}. "
                f"First error: {_preview(errors[0])}"
            )
            recommended_action = (
                "Investigate the failing component, capture the full stack trace, "
                "and check recent deployments or config changes that could have "
                "introduced the regression."
            )
        elif warnings:
            category = proxy_pb.WARNING
            summary = (
                f"{len(warnings)} warning{'s' if len(warnings) != 1 else ''} found "
                f"across {total} log line{'s' if total != 1 else ''}. "
                f"First warning: {_preview(warnings[0])}"
            )
            recommended_action = (
                "Monitor the system, review the warning conditions, and adjust "
                "alert thresholds or fix the underlying behaviour before it "
                "escalates."
            )
        elif total == 0:
            category = proxy_pb.INFO
            summary = "No log content provided."
            recommended_action = "Paste at least one log line to receive an analysis."
        else:
            category = proxy_pb.INFO
            summary = (
                f"{total} log line{'s' if total != 1 else ''} processed. "
                "No errors or warnings detected — system appears nominal."
            )
            recommended_action = "No action required; continue routine monitoring."

        return AnalysisInsight(
            summary=summary,
            category=category,
            recommended_action=recommended_action,
        )
