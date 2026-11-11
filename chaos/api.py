from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query, status

from chaos.engine import ChaosEngine

app = FastAPI(title="Chaos Mesh Runner", version="0.1.0")
chaos = ChaosEngine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/v1/chaos/latency")
def latency(
    min_ms: int = Query(default=50, ge=0, le=30000),
    max_ms: int = Query(default=200, ge=0, le=30000),
) -> dict[str, float]:
    try:
        injected = chaos.inject_latency(min_ms, max_ms)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return {"injected_delay_ms": injected}


@app.post("/api/v1/chaos/fault")
def inject_fault(
    failure_rate: float = Query(default=0.5, ge=0.0, le=1.0),
    fault_status: int = Query(default=503, ge=400, le=599),
) -> dict[str, bool]:
    if chaos.should_inject_fault(failure_rate):
        raise HTTPException(status_code=fault_status, detail="Injected chaos fault")
    return {"fault_injected": False}
