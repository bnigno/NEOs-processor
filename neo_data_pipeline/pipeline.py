import requests

from neo_data_pipeline.api_client import NasaNeoApiClient
from neo_data_pipeline.csv_writer import CsvWriter
from neo_data_pipeline.processor import Processor


class DataPipeline:
    """
    A data pipeline for fetching, processing, and saving Near Earth Object (NEO) data.

    This class orchestrates the fetching of NEO data from NASA's API, processes the data,
    and saves the results to a CSV file.

    Attributes:
        api_client (NasaNeoApiClient): The client for accessing NASA's NEO API.
        data_processor (Processor): The processor for handling and transforming the NEO data.
        csv_writer (CsvWriter): The writer for saving data to a CSV file.
        fieldnames (list of str): The list of field names for the CSV file.
    """

    def __init__(self, api_key):
        """
        Initialize the DataPipeline with the NASA API key.

        Args:
            api_key (str): The NASA API key.
        """
        self.api_client = NasaNeoApiClient(api_key)
        self.data_processor = Processor()
        self.csv_writer = CsvWriter()
        self.fieldnames = [
            "Nome",
            "Data de Aproximação",
            "Diâmetro Mínimo (km)",
            "Diâmetro Máximo (km)",
            "Velocidade (m/s)",
            "Distância da Terra (km)",
            "Categoria Diâmetro",
            "Categoria Proximidade",
            "Potencialmente Perigoso",
            "Tipo de Órbita",
        ]

    def run(self, start_date, end_date, output_filename="neo_data.csv"):
        """
        Runs the data pipeline to fetch, process, and save NEO data.

        Args:
            start_date (str): The start date in YYYY-MM-DD format for fetching NEO data.
            end_date (str): The end date in YYYY-MM-DD format for fetching NEO data.
            output_filename (str, optional): The name of the file to which the processed data will be saved. Defaults to "neo_data.csv".
        """
        try:
            neo_data = self.api_client.fetch_neo_data(start_date, end_date)
            processed_data = self.data_processor.process(neo_data, self.api_client)
            self.csv_writer.save_to_csv(
                processed_data, self.fieldnames, output_filename
            )
            print(f"Data successfully saved to {output_filename}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred while fetching data from the NASA API: {e}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from the NASA API: {e}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
