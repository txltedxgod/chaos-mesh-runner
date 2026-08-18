from chaos.engine import ChaosEngine

def test_chaos():
    c = ChaosEngine()
    delay = c.inject_latency(10, 30)
    assert delay >= 10
