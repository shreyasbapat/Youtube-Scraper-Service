from datetime import datetime, timezone


def parse_timestamp(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
