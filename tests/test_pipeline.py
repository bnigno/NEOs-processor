import unittest
from unittest.mock import patch

import requests

from neo_data_pipeline.pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):

    @patch("neo_data_pipeline.pipeline.NasaNeoApiClient")
    @patch("neo_data_pipeline.pipeline.Processor")
    @patch("neo_data_pipeline.pipeline.CsvWriter")
    def setUp(self, MockCsvWriter, MockProcessor, MockNasaNeoApiClient):
        self.mock_api_client = MockNasaNeoApiClient.return_value
        self.mock_processor = MockProcessor.return_value
        self.mock_csv_writer = MockCsvWriter.return_value

        self.data_pipeline = DataPipeline(api_key="test-key")

    def test_run_success(self):
        mock_neo_data = {"2024-06-01": [{"id": "1", "name": "Test NEO"}]}
        self.mock_api_client.fetch_neo_data.return_value = mock_neo_data

        mock_processed_data = [
            {
                "Nome": "Test NEO",
                "Data de Aproximação": "2021-01-01",
                "Diâmetro Mínimo (km)": 0.1,
                "Diâmetro Máximo (km)": 0.5,
                "Velocidade (m/s)": 10,
                "Distância da Terra (km)": 500000,
                "Categoria Diâmetro": "Médio",
                "Categoria Proximidade": "Muito Próximo",
                "Potencialmente Perigoso": True,
                "Tipo de Órbita": "Orbit Type",
            }
        ]
        self.mock_processor.process.return_value = mock_processed_data

        self.data_pipeline.run(
            "2024-06-01", "2024-06-02", output_filename="test_output.csv"
        )

        # Assert the API client was called correctly
        self.mock_api_client.fetch_neo_data.assert_called_once_with(
            "2024-06-01", "2024-06-02"
        )

        # Assert the processor was called correctly
        self.mock_processor.process.assert_called_once_with(
            mock_neo_data, self.mock_api_client
        )

        # Assert the CSV writer was called correctly
        self.mock_csv_writer.save_to_csv.assert_called_once_with(
            mock_processed_data, self.data_pipeline.fieldnames, "test_output.csv"
        )

    @patch("builtins.print")
    def test_run_http_error(self, mock_print):
        # Setup mock to raise HTTPError
        self.mock_api_client.fetch_neo_data.side_effect = requests.exceptions.HTTPError(
            "HTTP Error"
        )

        self.data_pipeline.run("2024-06-01", "2024-06-02")

        mock_print.assert_called_with(
            "HTTP error occurred while fetching data from the NASA API: HTTP Error"
        )

    @patch("builtins.print")
    def test_run_request_exception(self, mock_print):
        # Setup mock to raise RequestException
        self.mock_api_client.fetch_neo_data.side_effect = (
            requests.exceptions.RequestException("Request Exception")
        )

        self.data_pipeline.run("2024-06-01", "2024-06-02")

        mock_print.assert_called_with(
            "An error occurred while fetching data from the NASA API: Request Exception"
        )

    @patch("builtins.print")
    def test_run_value_error(self, mock_print):
        # Setup mock to raise ValueError
        e = ValueError("Value Error")
        self.mock_api_client.fetch_neo_data.side_effect = e

        self.data_pipeline.run("2024-06-01", "2024-06-02")

        mock_print.assert_called_with(e)

    @patch("builtins.print")
    def test_run_unexpected_exception(self, mock_print):
        # Setup mock to raise a generic exception
        self.mock_api_client.fetch_neo_data.side_effect = Exception("Unexpected Error")

        self.data_pipeline.run("2024-06-01", "2024-06-02")

        mock_print.assert_called_with("An unexpected error occurred: Unexpected Error")


if __name__ == "__main__":
    unittest.main()
