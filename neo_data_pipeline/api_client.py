from datetime import datetime, timedelta

import requests


class NasaNeoApiClient:
    BASE_URL = "https://api.nasa.gov/neo/rest/v1"

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def validate_dates(start_date, end_date):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end - start > timedelta(days=7):
            raise ValueError(
                "The period between start_date and end_date must be no more than 7 days."
            )
        return start_date, end_date

    def fetch_neo_data(self, start_date, end_date):
        self.validate_dates(start_date, end_date)
        url = f"{self.BASE_URL}/feed"
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("near_earth_objects")

    def fetch_neo_orbit_type(self, neo_id):
        url = f"{self.BASE_URL}/neo/{neo_id}"
        params = {
            "api_key": self.api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return (
            response.json()
            .get("orbital_data", {})
            .get("orbit_class", {})
            .get("orbit_class_type")
        )
