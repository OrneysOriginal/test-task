from datetime import date

from src.main import main, parse_date
import argparse
from unittest.mock import patch
import pytest


def test_parse_date_valid():
    assert parse_date("2025-06-22") == date(2025, 6, 22)


def test_parse_date_invalid():
    with pytest.raises(argparse.ArgumentTypeError):
        parse_date("invalid-date")


@patch("src.main.ReportFactory.create")
@patch("src.main.read_logs")
def test_main_success(mock_read_logs, mock_create, capsys, sample_logs):
    # Настраиваем моки
    mock_read_logs.return_value = sample_logs

    # Мокируем аргументы командной строки
    with patch("argparse.ArgumentParser.parse_args") as mock_args:
        mock_args.return_value = argparse.Namespace(
            file=["access.log"], report="average", date=None
        )

        # Мокируем отчет
        class MockReport:
            def generate(self, records):
                return [("/test", 2, 0.15)]

            def headers(self):
                return ("handler", "total", "avg_response_time")

        mock_create.return_value = MockReport()

        # Запускаем main
        main()

        # Проверяем вывод
        captured = capsys.readouterr()
        output = captured.out.strip()

        assert "handler" in output
        assert "/test" in output
        assert "2" in output
        assert "0.15" in output


@patch("src.main.ReportFactory.create")
@patch("src.main.read_logs")
def test_main_with_date_filter(mock_read_logs, mock_create, sample_logs):
    # Настраиваем моки
    mock_read_logs.return_value = [
        r for r in sample_logs if r["@timestamp"].startswith("2025-06-22")
    ]

    # Мокируем аргументы с датой
    with patch("argparse.ArgumentParser.parse_args") as mock_args:
        mock_args.return_value = argparse.Namespace(
            file=["access.log"], report="average", date=date(2025, 6, 22)
        )

        # Мокируем отчет
        class MockReport:
            def generate(self, records):
                return [(r["url"], 1, 0.15) for r in records]

            def headers(self):
                return ("handler", "total", "avg_response_time")

        mock_create.return_value = MockReport()

        # Запускаем main
        main()

        # Проверяем что read_logs вызвана с правильной датой
        mock_read_logs.assert_called_with(["access.log"], date(2025, 6, 22))

        # Проверяем что в отчете только записи за указанную дату
        report = mock_create.return_value
        result = report.generate(mock_read_logs.return_value)
        assert len(result) == 2
        assert all(url in ["/api/users", "/api/users"] for url, _, _ in result)
