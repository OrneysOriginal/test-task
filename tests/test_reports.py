from src.reports import Report, ReportFactory
from src.average_report import AverageReport
import pytest


def test_report_abstract_class():
    with pytest.raises(TypeError):
        Report()


def test_report_factory_registration():
    class TestReport(Report):
        def generate(self, records):
            return []

        def headers(self):
            return ()

    ReportFactory.register("test")(TestReport)
    assert "test" in ReportFactory.registry
    assert ReportFactory.registry["test"] == TestReport


def test_report_factory_creation():
    report = ReportFactory.create("average")
    assert isinstance(report, AverageReport)


def test_report_factory_unknown_report():
    with pytest.raises(ValueError, match="Unknown report type: unknown"):
        ReportFactory.create("unknown")
