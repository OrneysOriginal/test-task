import pytest
import json


@pytest.fixture
def sample_logs():
    return [
        {
            "@timestamp": "2025-06-22T10:00:00+00:00",
            "url": "/api/users",
            "response_time": 0.1,
        },
        {
            "@timestamp": "2025-06-22T11:00:00+00:00",
            "url": "/api/users",
            "response_time": 0.2,
        },
        {
            "@timestamp": "2025-06-23T10:00:00+00:00",
            "url": "/api/products",
            "response_time": 0.3,
        },
    ]


@pytest.fixture
def mock_log_file(monkeypatch, sample_logs):
    def mock_open_wrapper(*args, **kwargs):
        class MockFile:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                pass

            def __iter__(self):
                return iter(json.dumps(record) for record in sample_logs)

        return MockFile()

    monkeypatch.setattr("builtins.open", mock_open_wrapper)
