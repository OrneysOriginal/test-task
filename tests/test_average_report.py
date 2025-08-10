from src.average_report import AverageReport


def test_average_report_generation():
    records = [
        {"url": "/test", "response_time": 0.1},
        {"url": "/test", "response_time": 0.2},
        {"url": "/api", "response_time": 0.3},
        {"url": "/api", "response_time": 0.5},
    ]

    report = AverageReport()
    result = report.generate(records)

    # Проверяем агрегацию данных
    assert ("/test", 2, 0.15) in result
    assert ("/api", 2, 0.4) in result

    # Проверяем сортировку по количеству запросов
    assert result[0][1] >= result[1][1]


def test_average_report_empty_input():
    report = AverageReport()
    result = report.generate([])
    assert result == []


def test_average_report_headers():
    report = AverageReport()
    assert report.headers() == ("handler", "total", "avg_response_time")
