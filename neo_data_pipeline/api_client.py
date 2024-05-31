import requests


class NasaNeoApiClient:
    BASE_URL = "https://api.nasa.gov/neo/rest/v1/feed"

    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_neo_data(self, start_date, end_date):
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "api_key": self.api_key,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        return response.json()["near_earth_objects"]
