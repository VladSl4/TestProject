"""Unit tests for the heuristic analyzer (AI simulation)."""

import time

import proxy_analyses_pb2 as proxy_pb

from proxy_service.services.analyzer_service import AnalyzerService


def test_empty_logs_returns_info_category():
    analyzer = AnalyzerService(latency_seconds=0)
    insight = analyzer.analyze("")
    assert insight.category == proxy_pb.INFO
    assert "No log content" in insight.summary


def test_info_only_logs_returns_info_category():
    analyzer = AnalyzerService(latency_seconds=0)
    insight = analyzer.analyze(
        "2026-05-20T10:00 INFO booted\n"
        "2026-05-20T10:01 INFO heartbeat ok\n"
        "2026-05-20T10:02 INFO heartbeat ok"
    )
    assert insight.category == proxy_pb.INFO
    assert "3 log lines" in insight.summary
    assert "nominal" in insight.summary.lower()
    assert insight.recommended_action


def test_warning_logs_are_detected():
    analyzer = AnalyzerService(latency_seconds=0)
    insight = analyzer.analyze(
        "INFO booted\n"
        "WARN cache hit ratio dropped to 35%\n"
        "INFO heartbeat ok"
    )
    assert insight.category == proxy_pb.WARNING
    assert "1 warning" in insight.summary
    assert "cache hit ratio" in insight.summary


def test_error_outranks_warning():
    analyzer = AnalyzerService(latency_seconds=0)
    insight = analyzer.analyze(
        "WARN slow query\n"
        "ERROR connection pool exhausted\n"
        "WARN retry exhausted"
    )
    assert insight.category == proxy_pb.ERROR
    assert "1 error" in insight.summary
    assert "connection pool" in insight.summary
    assert "Investigate" in insight.recommended_action


def test_latency_is_applied():
    analyzer = AnalyzerService(latency_seconds=0.2)
    start = time.perf_counter()
    analyzer.analyze("INFO ok")
    elapsed = time.perf_counter() - start
    assert elapsed >= 0.2
