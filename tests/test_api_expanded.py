from fastapi.testclient import TestClient
from falvorn.api import app


def test_persistent_run_and_subscription_routes():
    with TestClient(app) as client:
        runs=client.get('/v1/agent/runs')
        assert runs.status_code==200 and isinstance(runs.json()['runs'],list)
        assert client.get('/v1/agent/runs/not-a-run').status_code==404
        assert client.post('/v1/agent/runs/not-a-run/cancel').status_code==404
        assert client.get('/v1/monitor/subscriptions').status_code==200
        assert client.post('/v1/monitor/subscriptions',json={
            'url':'https://example.com','interval_seconds':10}).status_code==422
        assert client.get('/health').json()['capabilities']['durable_runs'] is True
