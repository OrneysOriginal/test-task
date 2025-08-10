import argparse
import datetime
from tabulate import tabulate
from src.reports import ReportFactory
import src.average_report
import json


def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Use YYYY-MM-DD")


def read_logs(files, date_filter=None):
    """Чтение и фильтрация логов"""
    records = []
    for file_path in files:
        try:
            with open(file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        record = json.loads(line)
                        if "url" not in record or "response_time" not in record:
                            continue
                        if date_filter:
                            record_date = datetime.datetime.fromisoformat(
                                record["@timestamp"]
                            ).date()
                            if record_date != date_filter:
                                continue
                        records.append(record)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except IOError:
            continue
    return records


def main():
    parser = argparse.ArgumentParser(description="Log file analyzer")
    parser.add_argument("--file", nargs="+", required=True, help="Log files to process")
    parser.add_argument("--report", required=True, help="Report type to generate")
    parser.add_argument(
        "--date", type=parse_date, help="Filter logs by date (YYYY-MM-DD)"
    )
    args = parser.parse_args()

    records = read_logs(args.file, args.date)
    report = ReportFactory.create(args.report)
    report_data = report.generate(records)

    indexed_data = [(i, *row) for i, row in enumerate(report_data)]

    print(tabulate(indexed_data, headers=("", *report.headers()), tablefmt="plain"))


if __name__ == "__main__":
    main()
