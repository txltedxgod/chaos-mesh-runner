import pytest
from fastapi.testclient import TestClient

from chaos.api import app
from chaos.engine import ChaosEngine

client = TestClient(app)


def test_chaos() -> None:
    c = ChaosEngine()
    delay = c.inject_latency(10, 30)
    assert 10 <= delay <= 30


def test_chaos_validation_and_fault() -> None:
    c = ChaosEngine()
    with pytest.raises(ValueError, match="non-negative"):
        c.inject_latency(-1, 10)
    with pytest.raises(ValueError, match="min_ms"):
        c.inject_latency(50, 10)
    assert c.should_inject_fault(0.0) is False
    assert c.should_inject_fault(1.0) is True


def test_chaos_api() -> None:
    assert client.get("/health").json() == {"status": "ok"}

    ok_lat = client.post("/api/v1/chaos/latency?min_ms=1&max_ms=5")
    assert ok_lat.status_code == 200
    assert 1 <= ok_lat.json()["injected_delay_ms"] <= 5

    bad_lat = client.post("/api/v1/chaos/latency?min_ms=100&max_ms=10")
    assert bad_lat.status_code == 400

    fault_resp = client.post("/api/v1/chaos/fault?failure_rate=1.0&fault_status=503")
    assert fault_resp.status_code == 503

    pass_resp = client.post("/api/v1/chaos/fault?failure_rate=0.0")
    assert pass_resp.status_code == 200
    assert pass_resp.json() == {"fault_injected": False}
