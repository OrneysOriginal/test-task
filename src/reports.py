from abc import ABC, abstractmethod


class Report(ABC):
    @abstractmethod
    def generate(self, records):
        pass

    @abstractmethod
    def headers(self):
        pass


class ReportFactory:
    registry = {}

    @classmethod
    def register(cls, report_type):
        def wrapper(report_class):
            cls.registry[report_type] = report_class
            return report_class

        return wrapper

    @classmethod
    def create(cls, report_type):
        report_class = cls.registry.get(report_type)
        if not report_class:
            raise ValueError(f"Unknown report type: {report_type}")
        return report_class()
