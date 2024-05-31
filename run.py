import sys
from datetime import datetime, timedelta

from neo_data_pipeline.api_client import NasaNeoApiClient


def validate_dates(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    if end - start > timedelta(days=7):
        raise ValueError(
            "The period between start_date and end_date must be no more than 7 days."
        )
    return start_date, end_date


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python run.py <api_key> <start_date> <end_date>")
        sys.exit(1)

    api_key = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]

    try:
        start_date, end_date = validate_dates(start_date, end_date)
    except ValueError as e:
        print(e)
        sys.exit(1)

    api_client = NasaNeoApiClient(api_key)
    neo_data = api_client.fetch_neo_data(start_date, end_date)
    print(neo_data)
