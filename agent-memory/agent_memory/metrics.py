"""Metrics module for agent-memory.

Provides simple metrics collection with file-based persistence.
"""

import json
import time
from typing import Dict
from datetime import datetime
from pathlib import Path


# Metrics file path
METRICS_FILE = Path.home() / ".openclaw/workspace/logs/metrics.json"
METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)


def _get_metrics() -> Dict:
    """Get or initialize metrics from file."""
    # Always load from file (no caching across imports)
    if METRICS_FILE.exists():
        with open(METRICS_FILE) as f:
            metrics = json.load(f)
            # Validate and fix if structure is incomplete
            required_fields = ["latencies", "total_requests", "successful_requests", "failed_requests", "api_health_checks", "last_api_success"]
            for field in required_fields:
                if field not in metrics:
                    metrics[field] = [] if field == "latencies" or field == "api_health_checks" else 0
            return metrics
    else:
        # Initialize new metrics
        return {
            "latencies": [],
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "api_health_checks": [],
            "last_api_success": None
        }


def _save_metrics(metrics: Dict):
    """Save metrics to file."""
    with open(METRICS_FILE, "w") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)


def record_metric(latency_ms: int, success: bool):
    """
    Record a request metric.

    Args:
        latency_ms: Request latency in milliseconds
        success: Whether request was successful
    """
    metrics = _get_metrics()
    metrics["total_requests"] += 1
    metrics["latencies"].append(latency_ms)

    if success:
        metrics["successful_requests"] += 1
    else:
        metrics["failed_requests"] += 1

    _save_metrics(metrics)


def record_health_check(healthy: bool):
    """
    Record an API health check.

    Args:
        healthy: Whether API is healthy
    """
    metrics = _get_metrics()
    metrics["api_health_checks"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "healthy": healthy
    })

    if healthy:
        metrics["last_api_success"] = datetime.utcnow().isoformat() + "Z"

    _save_metrics(metrics)


def get_latency_metrics() -> Dict[str, float]:
    """Get latency percentiles."""
    metrics = _get_metrics()
    latencies = metrics["latencies"]
    if not latencies:
        return {"p50": 0, "p95": 0, "p99": 0, "avg": 0}

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)

    p50 = sorted_latencies[int(n * 0.5)] if n > 0 else 0
    p95 = sorted_latencies[int(n * 0.95)] if n > 0 else 0
    p99 = sorted_latencies[int(n * 0.99)] if n > 0 else 0
    avg = sum(latencies) / len(latencies)

    return {"p50": p50, "p95": p95, "p99": p99, "avg": avg}


def get_success_rate() -> Dict[str, any]:
    """Get success rate metrics."""
    metrics = _get_metrics()
    total = metrics["total_requests"]
    successful = metrics["successful_requests"]
    failed = metrics["failed_requests"]
    error_rate = (failed / total) * 100 if total > 0 else 0.0

    return {
        "total": total,
        "successful": successful,
        "failed": failed,
        "error_rate": error_rate
    }


def get_api_health() -> Dict[str, any]:
    """Get API health metrics."""
    metrics = _get_metrics()
    health_checks = metrics["api_health_checks"]
    if not health_checks:
        return {"uptime_percentage": 100.0, "last_success": None}

    healthy_count = sum(1 for c in health_checks if c["healthy"])
    total_count = len(health_checks)
    uptime = (healthy_count / total_count) * 100 if total_count > 0 else 100.0

    return {
        "uptime_percentage": uptime,
        "last_success": metrics["last_api_success"]
    }


def get_all_metrics() -> Dict[str, any]:
    """Get all metrics for export."""
    latency = get_latency_metrics()
    success = get_success_rate()
    health = get_api_health()

    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "latency_ms": latency,
        "requests": success,
        "api_health": health
    }
