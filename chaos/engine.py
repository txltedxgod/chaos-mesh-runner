import time
import random
from typing import Dict, Any

class ChaosEngine:
    def inject_latency(self, min_ms: int = 100, max_ms: int = 500) -> float:
        delay = random.uniform(min_ms, max_ms) / 1000.0
        time.sleep(delay)
        return round(delay * 1000.0, 2)
