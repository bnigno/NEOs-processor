import unittest
from unittest.mock import patch, MagicMock

from neo_data_pipeline.api_client import NasaNeoApiClient
from neo_data_pipeline.csv_writer import CsvWriter
from neo_data_pipeline.pipeline import DataPipeline
from neo_data_pipeline.processor import Processor


class TestNeoDataPipeline(unittest.TestCase):
    @patch("neo_data_pipeline.api_client.requests.get")
    @patch("neo_data_pipeline.csv_writer.CsvWriter.save_to_csv")
    def test_run_pipeline(self, mock_save_to_csv, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "near_earth_objects": {
                "2024-05-01": [
                    {
                        "name": "Test NEO",
                        "close_approach_data": [
                            {
                                "close_approach_date": "2024-05-01",
                                "relative_velocity": {"kilometers_per_hour": "36000"},
                                "miss_distance": {"kilometers": "1000000"},
                            }
                        ],
                        "estimated_diameter": {
                            "kilometers": {
                                "estimated_diameter_min": 0.1,
                                "estimated_diameter_max": 0.2,
                            }
                        },
                        "is_potentially_hazardous_asteroid": False,
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        api_client = NasaNeoApiClient(api_key="test_key")
        data_processor = Processor()
        csv_writer = CsvWriter()

        pipeline = DataPipeline(api_client, data_processor, csv_writer)
        pipeline.run("2024-05-01", "2024-05-07", "test_output.csv")

        # Verify that the API client was called correctly
        mock_get.assert_called_once_with(
            "https://api.nasa.gov/neo/rest/v1/feed",
            params={
                "start_date": "2024-05-01",
                "end_date": "2024-05-07",
                "api_key": "test_key",
            },
        )

        # Verify that save_to_csv was called only once
        mock_save_to_csv.assert_called_once()


if __name__ == "__main__":
    unittest.main()
