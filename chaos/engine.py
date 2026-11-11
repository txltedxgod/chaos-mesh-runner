from __future__ import annotations

import random
import time


class ChaosEngine:
    """Controlled latency and fault injection helpers."""

    def inject_latency(self, min_ms: int = 100, max_ms: int = 500) -> float:
        if min_ms < 0 or max_ms < 0:
            raise ValueError("latency bounds must be non-negative")
        if min_ms > max_ms:
            raise ValueError("min_ms must not exceed max_ms")

        delay = random.uniform(min_ms, max_ms) / 1000.0
        time.sleep(delay)
        return round(delay * 1000.0, 2)

    def should_inject_fault(
        self, failure_rate: float = 0.0, rng: random.Random | None = None
    ) -> bool:
        if failure_rate < 0.0 or failure_rate > 1.0:
            raise ValueError("failure_rate must be between 0.0 and 1.0")
        source = rng if rng is not None else random
        return source.random() < failure_rate
