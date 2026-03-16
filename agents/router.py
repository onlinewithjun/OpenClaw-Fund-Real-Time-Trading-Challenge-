#!/usr/bin/env python3
"""
Multi-Agent Router for OpenClaw

This module provides intent detection and routing logic for the multi-agent architecture.
It supports keyword-based routing, context-aware routing, and cross-agent call tracking.

Usage:
    from agent_router import Router
    router = Router()
    domain = router.detect_domain("基金挑战今天收益如何")
    # Returns: "finance-agent"
"""

import json
import re
import time
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class AgentRouter:
    """Multi-agent intent detection and routing."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the router.

        Args:
            config_path: Path to routing.json config file.
                        Defaults to agents/routing.json in workspace.
        """
        if config_path is None:
            workspace = Path(__file__).parent.parent
            config_path = workspace / "agents" / "routing.json"

        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.context: List[Dict] = []
        self.last_domain = self.config.get("fallback", {}).get("domain", "ops-agent")
        self.metrics: Dict = {"requests": [], "cross_agent_calls": []}

    def _load_config(self) -> Dict:
        """Load routing configuration from JSON file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in config: {e}")
            return self._default_config()

    def _default_config(self) -> Dict:
        """Return default configuration if config file is missing."""
        return {
            "routing": {
                "mode": "keyword",
                "fallback": "ops-agent",
                "context_window": 5,
                "stickiness_ms": 300000
            },
            "domains": {
                "ops-agent": {"is_fallback": True}
            }
        }

    def detect_domain(self, query: str, history: Optional[List[str]] = None) -> str:
        """
        Detect the target domain for a user query.

        Args:
            query: User's input query
            history: Optional list of recent messages for context

        Returns:
            Domain name (e.g., "code-agent", "finance-agent", "ops-agent")
        """
        start_time = time.time()

        # 1. Check for explicit agent mention (highest priority)
        domain = self._check_explicit_mention(query)
        if domain:
            self._record_metric(query, domain, time.time() - start_time, "explicit")
            return domain

        # 2. Check priority rules
        domain = self._check_priority_rules(query)
        if domain:
            self._record_metric(query, domain, time.time() - start_time, "priority")
            return domain

        # 3. Keyword matching
        domain = self._keyword_match(query)
        if domain:
            # Check context for consistency
            if self._should_use_context(history):
                context_domain = self._context_match(history)
                if context_domain and context_domain == domain:
                    self._record_metric(query, domain, time.time() - start_time, "context")
                    return domain

            self._record_metric(query, domain, time.time() - start_time, "keyword")
            self.last_domain = domain
            return domain

        # 4. Context-based routing (if no keyword match)
        if self._should_use_context(history):
            domain = self._context_match(history)
            if domain:
                self._record_metric(query, domain, time.time() - start_time, "context_fallback")
                return domain

        # 5. Fallback to default
        domain = self.config.get("fallback", {}).get("domain", "ops-agent")
        self._record_metric(query, domain, time.time() - start_time, "fallback")
        return domain

    def _check_explicit_mention(self, query: str) -> Optional[str]:
        """Check if user explicitly mentions an agent name."""
        pattern = r"(code|finance|ops).*agent"
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return f"{match.group(1).lower()}-agent"
        return None

    def _check_priority_rules(self, query: str) -> Optional[str]:
        """Check priority rules for special cases."""
        priority_rules = self.config.get("priority_rules", [])

        for rule in sorted(priority_rules, key=lambda x: x.get("priority", 0), reverse=True):
            # Check pattern match
            if "pattern" in rule:
                if re.search(rule["pattern"], query, re.IGNORECASE):
                    return rule["target"]

            # Check keyword match
            if "keywords" in rule:
                if any(kw in query for kw in rule["keywords"]):
                    return rule["target"]

        return None

    def _keyword_match(self, query: str) -> Optional[str]:
        """Match query keywords to domains."""
        domains = self.config.get("domains", {})

        # Count keyword matches per domain
        domain_scores: Dict[str, int] = {}

        for domain_name, domain_config in domains.items():
            keywords = domain_config.get("keywords", [])
            score = sum(1 for kw in keywords if kw.lower() in query.lower())
            if score > 0:
                domain_scores[domain_name] = score

        if not domain_scores:
            return None

        # Return domain with highest score
        best_domain = max(domain_scores, key=domain_scores.get)
        return best_domain

    def _should_use_context(self, history: Optional[List[str]]) -> bool:
        """Check if context-based routing should be used."""
        context_config = self.config.get("context_rules", {})
        if not context_config.get("enabled", True):
            return False

        if not history or len(history) == 0:
            return False

        # Check stickiness (time since last request)
        if self.metrics.get("requests"):
            last_request = self.metrics["requests"][-1]
            elapsed = time.time() - last_request.get("timestamp", 0)
            stickiness_ms = context_config.get("stickiness_ms", 300000)
            if elapsed * 1000 > stickiness_ms:
                return False

        return True

    def _context_match(self, history: Optional[List[str]]) -> Optional[str]:
        """Match based on conversation context."""
        if not history:
            return self.last_domain

        # Use the last domain from context
        return self.last_domain

    def _record_metric(self, query: str, domain: str, duration_ms: float, method: str):
        """Record routing metric for analysis."""
        metrics_config = self.config.get("metrics", {})
        if not metrics_config.get("enabled", True):
            return

        self.metrics["requests"].append({
            "timestamp": time.time(),
            "query": query[:100],  # Truncate for privacy
            "domain": domain,
            "duration_ms": round(duration_ms * 1000, 2),
            "method": method
        })

        # Keep only last 1000 requests
        if len(self.metrics["requests"]) > 1000:
            self.metrics["requests"] = self.metrics["requests"][-1000:]

    def get_metrics(self) -> Dict:
        """Get routing metrics."""
        return {
            "total_requests": len(self.metrics["requests"]),
            "requests_by_domain": self._count_by_domain(),
            "requests_by_method": self._count_by_method(),
            "avg_duration_ms": self._avg_duration(),
            "fallback_rate": self._fallback_rate()
        }

    def _count_by_domain(self) -> Dict[str, int]:
        """Count requests per domain."""
        counts: Dict[str, int] = {}
        for req in self.metrics["requests"]:
            domain = req["domain"]
            counts[domain] = counts.get(domain, 0) + 1
        return counts

    def _count_by_method(self) -> Dict[str, int]:
        """Count requests per detection method."""
        counts: Dict[str, int] = {}
        for req in self.metrics["requests"]:
            method = req["method"]
            counts[method] = counts.get(method, 0) + 1
        return counts

    def _avg_duration(self) -> float:
        """Calculate average routing duration."""
        if not self.metrics["requests"]:
            return 0.0
        durations = [r["duration_ms"] for r in self.metrics["requests"]]
        return round(sum(durations) / len(durations), 2)

    def _fallback_rate(self) -> float:
        """Calculate fallback rate."""
        if not self.metrics["requests"]:
            return 0.0
        fallbacks = sum(1 for r in self.metrics["requests"] if r["method"] == "fallback")
        return round(fallbacks / len(self.metrics["requests"]), 4)

    def save_metrics(self, output_path: Optional[str] = None):
        """Save metrics to file."""
        if output_path is None:
            metrics_config = self.config.get("metrics", {})
            output_path = metrics_config.get("log_path", "memory/ops/routing-metrics.json")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "metrics": self.get_metrics(),
                "recent_requests": self.metrics["requests"][-100:]
            }, f, indent=2, ensure_ascii=False)

    def run_tests(self) -> Tuple[int, int]:
        """
        Run test queries and report accuracy.

        Returns:
            Tuple of (passed, total) test results
        """
        test_config = self.config.get("testing", {})
        sample_queries = test_config.get("sample_queries", [])

        if not sample_queries:
            print("No test queries found in config")
            return 0, 0

        passed = 0
        total = len(sample_queries)

        print(f"Running {total} test queries...\n")

        for test in sample_queries:
            query = test["query"]
            expected = test["expected"]
            result = self.detect_domain(query)

            status = "PASS" if result == expected else "FAIL"
            if result == expected:
                passed += 1

            print(f"[{status}] Query: {query}")
            print(f"  Expected: {expected}, Got: {result}\n")

        accuracy = passed / total if total > 0 else 0
        target = test_config.get("target_accuracy", 0.95)

        print(f"Results: {passed}/{total} ({accuracy:.1%} accuracy)")
        print(f"Target: {target:.1%}")
        print(f"Status: {'PASS' if accuracy >= target else 'NEEDS IMPROVEMENT'}")

        return passed, total


def main():
    """Main entry point for testing."""
    router = AgentRouter()

    # Run tests
    print("=" * 60)
    print("Multi-Agent Router - Test Suite")
    print("=" * 60 + "\n")

    passed, total = router.run_tests()

    # Save metrics
    router.save_metrics()
    print(f"\nMetrics saved to memory/ops/routing-metrics.json")

    # Interactive mode
    print("\n" + "=" * 60)
    print("Interactive Mode (type 'quit' to exit)")
    print("=" * 60 + "\n")

    while True:
        try:
            query = input("Query: ").strip()
            if query.lower() in ("quit", "exit", "q"):
                break

            domain = router.detect_domain(query)
            print(f"→ Routed to: {domain}\n")
        except (KeyboardInterrupt, EOFError):
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
