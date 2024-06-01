import unittest
from unittest.mock import patch, MagicMock

from requests.exceptions import RequestException

from neo_data_pipeline.api_client import NasaNeoApiClient


class TestNasaNeoApiClient(unittest.TestCase):
    @patch("neo_data_pipeline.api_client.requests.get")
    def test_fetch_neo_data_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"near_earth_objects": {"2024-05-01": []}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = NasaNeoApiClient("test_key")
        neo_data = client.fetch_neo_data("2024-05-01", "2024-05-07")

        self.assertIn("2024-05-01", neo_data)
        mock_get.assert_called_once_with(
            "https://api.nasa.gov/neo/rest/v1/feed",
            params={
                "start_date": "2024-05-01",
                "end_date": "2024-05-07",
                "api_key": "test_key",
            },
        )

    @patch("neo_data_pipeline.api_client.requests.get")
    def test_fetch_neo_data_failure(self, mock_get):
        mock_get.side_effect = RequestException()
        client = NasaNeoApiClient("invalid_key")
        with self.assertRaises(RequestException):
            client.fetch_neo_data("2024-05-01", "2024-05-07")


if __name__ == "__main__":
    unittest.main()
