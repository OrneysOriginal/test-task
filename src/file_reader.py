import json
import datetime


def read_logs(files, date_filter=None):
    """
    Чтение лог-файлов с фильтрацией по дате
    """
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
                        if not validate_record(record):
                            continue
                        if date_filter and not filter_by_date(record, date_filter):
                            continue
                        records.append(record)
                    except json.JSONDecodeError:
                        continue
        except IOError:
            continue
    return records


def validate_record(record):
    return "url" in record and "response_time" in record and "@timestamp" in record


def filter_by_date(record, target_date):
    try:
        record_date = datetime.datetime.fromisoformat(record["@timestamp"]).date()
        return record_date == target_date
    except (ValueError, TypeError):
        return False
