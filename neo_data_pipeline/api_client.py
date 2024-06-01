from datetime import datetime, timedelta

import requests


class NasaNeoApiClient:
    """
    Client for NASA's Near Earth Object (NEO) API.

    This class provides methods to fetch data about near earth objects
    from NASA's NEO API.

    Attributes:
        api_key (str): The API key for accessing NASA's NEO API.
    """

    BASE_URL = "https://api.nasa.gov/neo/rest/v1"

    def __init__(self, api_key):
        """
        Initialize the NasaNeoApiClient.

        Args:
            api_key (str): The API key for accessing NASA's NEO API.
        """
        self.api_key = api_key

    @staticmethod
    def validate_dates(start_date, end_date):
        """
        Validates that the difference between start_date and end_date is no more than 7 days.

        Args:
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.

        Returns:
            tuple: The validated start_date and end_date.

        Raises:
            ValueError: If the difference between start_date and end_date is more than 7 days.
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end - start > timedelta(days=7):
            raise ValueError(
                "The period between start_date and end_date must be no more than 7 days."
            )
        return start_date, end_date

    def fetch_neo_data(self, start_date, end_date):
        """
        Fetches data about near earth objects from NASA's NEO API.

        Args:
            start_date (str): The start date in YYYY-MM-DD format.
            end_date (str): The end date in YYYY-MM-DD format.

        Returns:
            dict: A dictionary containing data about near earth objects.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.RequestException: For other request-related issues.
        """
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
        """
        Fetches the orbit type of a specific NEO from NASA's API.

        Args:
            neo_id (str): The ID of the near earth object.

        Returns:
            str, None: The orbit class type of the NEO, or None if not available.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.RequestException: For other request-related issues.
        """
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
