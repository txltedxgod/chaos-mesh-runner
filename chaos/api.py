from fastapi import FastAPI
from chaos.engine import ChaosEngine

app = FastAPI(title="Chaos Mesh Runner", version="0.1.0")
chaos = ChaosEngine()

@app.post("/api/v1/chaos/latency")
def latency(min_ms: int = 50, max_ms: int = 200):
    injected = chaos.inject_latency(min_ms, max_ms)
    return {"injected_delay_ms": injected}
