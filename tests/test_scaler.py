from scaler import AutoScaler
def test_scale_out():

    scaler=AutoScaler()

    metrics={
        "cpu":90,
        "replicas":1
    }

    scaler.high_cpu_count=1

    decision=scaler.should_scale(metrics)

    assert decision["target_replicas"]==2